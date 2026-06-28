#!/usr/bin/env python3
"""
Add, list, or remove background music / deck-level media tracks.

DeckMediaTrack fields live at deck.mediaTracks[] and play alongside slides
in the timeline — ideal for background music, ambient sound, or soundtrack beds.

Usage:
    # List current deck-level media tracks:
    python scripts/set_deck_music.py <deck-id> --list

    # Add a background music track from a URL:
    python scripts/set_deck_music.py <deck-id> \
        --url "https://storage.googleapis.com/…/music.mp3" \
        --loop --volume 0.15 --name "Background music"

    # Pipe a generate_audio.py output as background audio:
    python scripts/generate_audio.py "Text…" --default-voice | \
        python scripts/set_deck_music.py <deck-id> --add-track - --loop --volume 0.15

    # Add from a JSON object (DeckMediaTrack or generate_audio.py output):
    python scripts/set_deck_music.py <deck-id> --add-track '{"url":"…","loop":true,"volume":0.15}'

    # Remove all deck-level media tracks:
    python scripts/set_deck_music.py <deck-id> --clear

    # Remove a specific track by id:
    python scripts/set_deck_music.py <deck-id> --remove-track <track-id>

DeckMediaTrack schema (full):
    id          str      UUID (auto-assigned if absent)
    kind        str      "audio" | "video"
    url         str      MP3 / WAV / MP4 URL
    startMs     int      Offset from deck start (ms); 0 for music beds
    durationMs  int?     Length in ms (optional — probed from file when absent)
    name        str?     Display label ("Background music", filename, etc.)
    volume      float?   Playback gain 0.0–1.0 (default 1.0; use 0.1–0.2 for beds)
    loop        bool?    Loop to fill the deck duration (ideal for music beds)
    lane        int?     Stacking row within the kind lane (default 0)
    layout      str?     "fullscreen" | "pip" (video kind only)
    position    str?     "bottom-right" etc. (pip layout, video only)
    size        float?   PiP size as fraction of output height 0.1–0.5 (video only)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid as _uuid
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth import get_credentials

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

API_URL = os.environ.get("OPEN_ACADEMY_API_URL", "https://open-academy-api-mz4xquo5lq-as.a.run.app")
APP_URL = os.environ.get("OPEN_ACADEMY_APP_URL", "https://deck.4hum.ai")


def _fetch(deck_id: str, token: str, workspace_id: str) -> dict:
    req = urllib.request.Request(
        f"{API_URL}/api/decks/{deck_id}",
        headers={"Authorization": f"Bearer {token}", "x-workspace-id": workspace_id},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e
    row = data.get("data") or data
    raw = row.get("deckJson") or row
    return json.loads(raw) if isinstance(raw, str) else raw


def _put(deck_id: str, deck_json: dict, token: str, workspace_id: str) -> None:
    payload = json.dumps({"deckJson": deck_json}).encode()
    req = urllib.request.Request(
        f"{API_URL}/api/decks/{deck_id}",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "x-workspace-id": workspace_id,
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e


def _load_json_arg(value: str) -> object:
    if value == "-":
        raw = sys.stdin.read().strip()
    else:
        p = Path(value)
        if p.exists():
            raw = p.read_text(encoding="utf-8").strip()
        else:
            raw = value
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)


def _normalise_track(obj: dict, *, loop: bool | None = None, volume: float | None = None,
                     name: str | None = None, kind: str = "audio") -> dict:
    """Convert generate_audio.py output or partial dict to a full DeckMediaTrack."""
    if "audio_url" in obj and "url" not in obj:
        # generate_audio.py format
        track: dict = {
            "id": str(_uuid.uuid4()),
            "kind": kind,
            "url": obj["audio_url"],
            "startMs": 0,
        }
        if obj.get("duration_ms") is not None:
            track["durationMs"] = obj["duration_ms"]
    else:
        track = dict(obj)
        if "id" not in track:
            track["id"] = str(_uuid.uuid4())
        if "kind" not in track:
            track["kind"] = kind
        if "startMs" not in track:
            track["startMs"] = 0

    if loop is not None:
        track["loop"] = loop
    if volume is not None:
        track["volume"] = round(volume, 3)
    if name is not None:
        track["name"] = name
    return track


def _get_deck_root(deck_json: dict) -> dict:
    return deck_json.get("deck", deck_json)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage deck-level background music / media tracks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("deck_id", help="Deck UUID")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="Print current deck mediaTracks as JSON")
    group.add_argument("--clear", action="store_true", help="Remove all deck mediaTracks")
    group.add_argument(
        "--remove-track", dest="remove_track", metavar="TRACK_ID",
        help="Remove the track with this id",
    )
    group.add_argument(
        "--add-track", dest="add_track", metavar="JSON_OR_FILE_OR_-",
        help=(
            "Append a media track. Accepts a JSON object, a file path, or '-' for stdin. "
            "Auto-converts generate_audio.py output ({audio_url, duration_ms}) to DeckMediaTrack."
        ),
    )
    group.add_argument(
        "--url", dest="url", metavar="URL",
        help="Add a track from a plain URL (combine with --loop, --volume, --name)",
    )

    parser.add_argument("--loop", action="store_true", default=None,
                        help="Set loop=true on the new track (ideal for music beds)")
    parser.add_argument("--volume", type=float, default=None, metavar="0-1",
                        help="Playback gain 0.0–1.0 (default 1.0; use 0.1–0.2 for beds)")
    parser.add_argument("--name", default=None, metavar="LABEL",
                        help="Display label for the track")
    parser.add_argument("--kind", default="audio", choices=["audio", "video"],
                        help="Media kind (default: audio)")
    parser.add_argument("--start-ms", dest="start_ms", type=int, default=None,
                        help="Start offset from deck begin in ms (default 0)")

    args = parser.parse_args()

    token, workspace_id = get_credentials()
    print(f"Fetching deck {args.deck_id} …", file=sys.stderr)
    deck_json = _fetch(args.deck_id, token, workspace_id)
    deck = _get_deck_root(deck_json)

    if args.list:
        tracks = deck.get("mediaTracks", [])
        print(json.dumps(tracks, indent=2))
        return

    if args.clear:
        deck["mediaTracks"] = []
        print("Cleared all media tracks.", file=sys.stderr)

    elif args.remove_track:
        tracks = deck.get("mediaTracks", [])
        before = len(tracks)
        deck["mediaTracks"] = [t for t in tracks if t.get("id") != args.remove_track]
        after = len(deck["mediaTracks"])
        if before == after:
            print(f"Warning: no track found with id {args.remove_track}", file=sys.stderr)
        else:
            print(f"Removed track {args.remove_track}.", file=sys.stderr)

    elif args.add_track:
        raw_obj = _load_json_arg(args.add_track)
        if not isinstance(raw_obj, dict):
            print("Error: --add-track must be a JSON object", file=sys.stderr)
            sys.exit(1)
        track = _normalise_track(
            raw_obj,
            loop=True if args.loop else None,
            volume=args.volume,
            name=args.name,
            kind=args.kind,
        )
        if args.start_ms is not None:
            track["startMs"] = args.start_ms
        if "mediaTracks" not in deck:
            deck["mediaTracks"] = []
        deck["mediaTracks"].append(track)
        print(f"Added {track['kind']} track: {track.get('url', '?')[:60]}…", file=sys.stderr)

    elif args.url:
        track = _normalise_track(
            {"url": args.url},
            loop=True if args.loop else None,
            volume=args.volume,
            name=args.name or "Background music",
            kind=args.kind,
        )
        if args.start_ms is not None:
            track["startMs"] = args.start_ms
        if "mediaTracks" not in deck:
            deck["mediaTracks"] = []
        deck["mediaTracks"].append(track)
        print(f"Added {track['kind']} track: {track['url'][:60]}…", file=sys.stderr)

    print("Updating deck …", file=sys.stderr)
    _put(args.deck_id, deck_json, token, workspace_id)
    edit_url = f"{APP_URL}/app/decks/{args.deck_id}/edit"
    print(f"Updated: {edit_url}")


if __name__ == "__main__":
    main()
