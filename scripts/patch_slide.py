#!/usr/bin/env python3
"""
Patch a single slide in an existing deck.

Avoids re-generating the full deck when only one slide needs updating, inserting,
or deleting — much faster than update_deck.py for targeted edits.

Usage:
    # Replace objects on slide 7 (0-based global index):
    echo '[{"type":"text",...}]' | python scripts/patch_slide.py <deck-id> 7

    # Delete slide 3:
    python scripts/patch_slide.py <deck-id> 3 --delete

    # Insert a new slide after slide 4 (stdin = full slide JSON object):
    echo '{"id":"...","background":{},"objects":[...]}' | python scripts/patch_slide.py <deck-id> 4 --insert-after

Options:
    --delete          Delete the slide at the given index.
    --insert-after    Insert a new slide after the given index; stdin = full slide JSON.
    (default)         Replace the objects array; stdin = JSON array of objects.

Validates the deck locally after the edit and aborts on any error before updating.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth import get_credentials
from deck_validator import validate_deck, format_validation_errors

# Windows cp1252 guard
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
        raise RuntimeError(f"HTTP {e.code} fetching deck: {e.read().decode()}") from e
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
    """Load a JSON arg that may be a raw string, a file path, or '-' for stdin."""
    if value == "-":
        raw = sys.stdin.read().strip()
    elif value.endswith(".json") or (value.startswith("{") is False and value.startswith("[") is False):
        p = Path(value)
        if p.exists():
            raw = p.read_text(encoding="utf-8").strip()
        else:
            raw = value
    else:
        raw = value
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON — {e}\nInput was: {raw[:120]}", file=sys.stderr)
        sys.exit(1)


def _to_narration_track(obj: dict) -> dict:
    """Convert a generate_audio.py output dict into a NarrationTrack if needed."""
    import uuid as _uuid
    if "audio_url" in obj and "url" not in obj:
        # generate_audio.py format → NarrationTrack
        track = {
            "id": str(_uuid.uuid4()),
            "kind": "audio",
            "url": obj["audio_url"],
            "startMs": 0,
            "source": "tts",
        }
        if obj.get("duration_ms") is not None:
            track["durationMs"] = obj["duration_ms"]
        if obj.get("voice_id"):
            track["voiceId"] = obj["voice_id"]
        if obj.get("text_hash"):
            track["textHash"] = obj["text_hash"]
        return track
    # Already a NarrationTrack shape — ensure it has an id
    if "id" not in obj:
        import uuid as _uuid
        obj = dict(obj, id=str(_uuid.uuid4()))
    return obj


def _all_slides(deck_json: dict) -> list[tuple[int, int]]:
    """Return (section_idx, slide_idx_within_section) for every slide in order."""
    result = []
    deck = deck_json.get("deck", deck_json)
    for si, section in enumerate(deck.get("sections", [])):
        for li in range(len(section.get("slides", []))):
            result.append((si, li))
    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Patch a single slide in a deck.")
    parser.add_argument("deck_id", help="Deck UUID")
    parser.add_argument("slide_index", type=int, help="0-based global slide index")
    parser.add_argument("--delete", action="store_true", help="Delete the slide at the given index")
    parser.add_argument("--insert-after", action="store_true", dest="insert_after",
                        help="Insert a new slide after the given index; stdin = full slide JSON object")
    parser.add_argument("--notes", metavar="TEXT",
                        help="Set or replace the slide's notes field (TTS / narration text)")
    parser.add_argument("--speaker-notes", dest="speaker_notes", metavar="TEXT",
                        help="Set or replace the slide's speakerNotes (presenter-only reminders)")
    parser.add_argument(
        "--add-narration-track", dest="add_narration_track", metavar="JSON_OR_FILE_OR_-",
        help=(
            "Append a NarrationTrack to the slide's narrationTracks array. "
            "Accepts: a JSON string, a path to a JSON file, or '-' to read from stdin. "
            "If the value looks like a generate_audio.py output object, it is automatically "
            "converted to a NarrationTrack ({audio_url,duration_ms,voice_id} → {kind,url,durationMs,voiceId,source:'tts'}). "
            "Example: --add-narration-track '{\"kind\":\"audio\",\"url\":\"...\",\"startMs\":0}'"
        ),
    )
    parser.add_argument(
        "--set-narration-tracks", dest="set_narration_tracks", metavar="JSON_OR_FILE_OR_-",
        help=(
            "Replace the slide's entire narrationTracks array. "
            "Accepts: a JSON array string, a file path, or '-' for stdin."
        ),
    )
    args = parser.parse_args()

    token, workspace_id = get_credentials()

    print(f"Fetching deck {args.deck_id} …", file=sys.stderr)
    deck_json = _fetch(args.deck_id, token, workspace_id)
    deck = deck_json.get("deck", deck_json)
    positions = _all_slides(deck_json)

    if args.slide_index >= len(positions):
        print(
            f"Error: slide index {args.slide_index} out of range "
            f"(deck has {len(positions)} slides, 0-based)",
            file=sys.stderr,
        )
        sys.exit(1)

    si, li = positions[args.slide_index]

    if args.delete:
        removed = deck["sections"][si]["slides"].pop(li)
        print(f"Deleted slide {args.slide_index} (section {si}, slide {li}): {removed.get('id', '?')[:8]}…")

    elif args.insert_after:
        raw = sys.stdin.read().strip()
        if not raw:
            print("Error: pipe a slide JSON object to stdin for --insert-after", file=sys.stderr)
            sys.exit(1)
        try:
            new_slide = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON from stdin — {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(new_slide, dict):
            print("Error: stdin must be a JSON object representing a slide", file=sys.stderr)
            sys.exit(1)
        deck["sections"][si]["slides"].insert(li + 1, new_slide)
        print(f"Inserted new slide after index {args.slide_index} in section {si}")

    else:
        has_notes_update = args.notes is not None or args.speaker_notes is not None
        has_narration_update = args.add_narration_track is not None or args.set_narration_tracks is not None
        # Read stdin only when it is piped (not a TTY). This lets --notes work
        # standalone without blocking on interactive stdin.
        try:
            piped = not sys.stdin.isatty()
        except Exception:
            piped = True

        raw = sys.stdin.read().strip() if piped else ""

        if raw:
            try:
                new_objects = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"Error: invalid JSON from stdin — {e}", file=sys.stderr)
                sys.exit(1)
            if not isinstance(new_objects, list):
                print("Error: stdin must be a JSON array of slide objects", file=sys.stderr)
                sys.exit(1)
            deck["sections"][si]["slides"][li]["objects"] = new_objects
            print(f"Replaced {len(new_objects)} object(s) on slide {args.slide_index} (section {si}, slide {li})")
        elif not has_notes_update and not has_narration_update:
            print(
                "Error: pipe a JSON array of slide objects to stdin, "
                "or use --notes / --speaker-notes / --add-narration-track / --set-narration-tracks for a field-only update",
                file=sys.stderr,
            )
            sys.exit(1)

    # Apply notes and narration track updates (work alone or combined with object replacement).
    if not args.delete and not args.insert_after:
        slide = deck["sections"][si]["slides"][li]

        if args.notes is not None:
            slide["notes"] = args.notes
            print(f"Updated notes on slide {args.slide_index}")
        if args.speaker_notes is not None:
            slide["speakerNotes"] = {"content": args.speaker_notes}
            print(f"Updated speakerNotes on slide {args.slide_index}")

        if args.add_narration_track is not None:
            raw_track = _load_json_arg(args.add_narration_track)
            if not isinstance(raw_track, dict):
                print("Error: --add-narration-track must be a JSON object", file=sys.stderr)
                sys.exit(1)
            track = _to_narration_track(raw_track)
            if "narrationTracks" not in slide:
                slide["narrationTracks"] = []
            slide["narrationTracks"].append(track)
            preview = track.get("url", "?")[:60]
            print(f"Added {track.get('kind', 'audio')} narration track to slide {args.slide_index}: {preview}…")

        if args.set_narration_tracks is not None:
            raw_tracks = _load_json_arg(args.set_narration_tracks)
            if not isinstance(raw_tracks, list):
                print("Error: --set-narration-tracks must be a JSON array", file=sys.stderr)
                sys.exit(1)
            tracks = [_to_narration_track(t) if isinstance(t, dict) else t for t in raw_tracks]
            slide["narrationTracks"] = tracks
            print(f"Set {len(tracks)} narration track(s) on slide {args.slide_index}")

    issues = validate_deck(deck_json)
    if issues:
        print(format_validation_errors(issues), file=sys.stderr)
        sys.exit(1)

    print("Validation passed. Updating deck …", file=sys.stderr)
    _put(args.deck_id, deck_json, token, workspace_id)

    edit_url = f"{APP_URL}/app/decks/{args.deck_id}/edit"
    print(f"Updated: {edit_url}")


if __name__ == "__main__":
    main()
