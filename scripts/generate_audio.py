#!/usr/bin/env python3
"""
Generate AI narration audio using a TTS voice.

Usage:
    # List available voices first:
    python scripts/generate_audio.py --list-voices

    # Generate from inline text:
    python scripts/generate_audio.py "Welcome to the deck." --voice-id <uuid>

    # Generate from stdin (long narration scripts):
    echo "Long narration..." | python scripts/generate_audio.py --voice-id <uuid>

    # Use the default system voice (first in the list):
    python scripts/generate_audio.py "Text." --default-voice

    # Control speed:
    python scripts/generate_audio.py "Text." --voice-id <uuid> --speed 0.9

Prints JSON to stdout: { "audio_url": "...", "duration_ms": N, "voice_id": "...", "text_hash": "..." }

Use audio_url as the `url` field in a NarrationTrack, then attach to a slide
with `patch_slide.py --add-narration-track`:

    python scripts/generate_audio.py "Script text" --voice-id <uuid> > audio.json
    python scripts/patch_slide.py <deck-id> <slide-index> --add-narration-track audio.json

Or pipe directly:
    python scripts/generate_audio.py "Script text" --voice-id <uuid> | \\
      python scripts/patch_slide.py <deck-id> <slide-index> --add-narration-track -

Text limits: 1–8 000 characters per call. For longer narration, split across
multiple calls and patch each slide separately.
"""
import argparse
import json
import os
import sys
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


def _get(path: str, token: str, workspace_id: str) -> dict:
    req = urllib.request.Request(
        f"{API_URL}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "x-workspace-id": workspace_id,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body)
            raise RuntimeError(f"HTTP {e.code}: {err.get('message', body)}") from e
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body}") from e


def _post(path: str, body: dict, token: str, workspace_id: str) -> dict:
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{API_URL}{path}",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "x-workspace-id": workspace_id,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body)
            raise RuntimeError(f"HTTP {e.code}: {err.get('message', body)}") from e
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body}") from e


def list_voices(token: str, workspace_id: str) -> list[dict]:
    result = _get("/api/media/voices", token, workspace_id)
    data = result.get("data") or result
    voices = data.get("voices") or data if isinstance(data, list) else data.get("voices", [])
    warning = data.get("warning") if isinstance(data, dict) else None
    if warning:
        print(f"Warning: {warning}", file=sys.stderr)
    return voices


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI narration audio for a slide",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  List voices:
    python scripts/generate_audio.py --list-voices

  Generate narration with a specific voice:
    python scripts/generate_audio.py "Quantum entanglement is one of nature's most remarkable phenomena." \\
      --voice-id <uuid>

  Use default system voice:
    python scripts/generate_audio.py "Welcome to our deck." --default-voice

  Slower, more deliberate pace:
    python scripts/generate_audio.py "Text here" --voice-id <uuid> --speed 0.85

  Pipe the result directly to patch_slide:
    python scripts/generate_audio.py "Narration..." --voice-id <uuid> | \\
      python scripts/patch_slide.py <deck-id> 2 --add-narration-track -
        """,
    )
    parser.add_argument(
        "text", nargs="?", default=None,
        help="Narration text (max 8 000 chars). Omit to read from stdin.",
    )
    parser.add_argument(
        "--voice-id", dest="voice_id", default=None,
        help="UUID of the voice to use. Run --list-voices to find IDs.",
    )
    parser.add_argument(
        "--default-voice", action="store_true",
        help="Use the first available system voice. Convenient shortcut; "
             "use --voice-id for production decks.",
    )
    parser.add_argument(
        "--list-voices", action="store_true",
        help="Print available voices as JSON and exit.",
    )
    parser.add_argument(
        "--speed", type=float, default=None,
        help="Speech rate multiplier, 0.5 (slowest) – 2.0 (fastest). Default: 1.0.",
    )
    parser.add_argument(
        "--deck-id", dest="deck_id", default=None,
        help="Associate this audio with a deck (logged for analytics, optional).",
    )
    parser.add_argument(
        "--slide-id", dest="slide_id", default=None,
        help="Associate this audio with a specific slide (optional).",
    )
    args = parser.parse_args()

    token, workspace_id = get_credentials()

    # --list-voices mode
    if args.list_voices:
        voices = list_voices(token, workspace_id)
        if not voices:
            print("No voices available. Check that a TTS provider is configured "
                  "(ELEVENLABS_API_KEY or similar).", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(voices, indent=2))
        return

    # Resolve text (arg or stdin)
    text = args.text
    if not text:
        if sys.stdin.isatty():
            print("No text provided. Pass text as an argument or pipe to stdin.", file=sys.stderr)
            parser.print_help(sys.stderr)
            sys.exit(1)
        text = sys.stdin.read().strip()

    if not text:
        print("Error: narration text is empty.", file=sys.stderr)
        sys.exit(1)
    if len(text) > 8000:
        print(f"Error: text is {len(text)} chars; limit is 8 000. "
              "Split narration across multiple slides.", file=sys.stderr)
        sys.exit(1)

    # Resolve voice ID
    voice_id = args.voice_id
    if not voice_id:
        if args.default_voice:
            voices = list_voices(token, workspace_id)
            if not voices:
                print("No voices available — cannot use --default-voice.", file=sys.stderr)
                sys.exit(1)
            voice_id = voices[0]["id"]
            print(f"Using default voice: {voices[0]['displayName']} (id={voice_id})", file=sys.stderr)
        else:
            print("Error: --voice-id required (or use --default-voice). "
                  "Run --list-voices to see options.", file=sys.stderr)
            sys.exit(1)

    preview = text[:80] + ("…" if len(text) > 80 else "")
    print(f"Generating narration ({len(text)} chars): {preview!r}", file=sys.stderr)

    req_body: dict = {
        "text": text,
        "workspaceId": workspace_id,
    }
    if args.speed is not None:
        req_body["speed"] = args.speed
    if args.deck_id:
        req_body["deckId"] = args.deck_id
    if args.slide_id:
        req_body["slideId"] = args.slide_id

    result = _post(f"/api/media/voices/{voice_id}/generate", req_body, token, workspace_id)
    data = result.get("data") or result

    audio_url = data.get("audioUrl")
    duration_ms = data.get("durationMs")
    returned_voice_id = data.get("voiceId", voice_id)
    text_hash = data.get("textHash")

    if not audio_url:
        print(f"Error: unexpected response — no audioUrl: {result}", file=sys.stderr)
        sys.exit(1)

    duration_s = f"{duration_ms / 1000:.1f}s" if duration_ms else "unknown"
    print(f"Audio ready ({duration_s}): {audio_url}", file=sys.stderr)

    print(json.dumps({
        "audio_url": audio_url,
        "duration_ms": duration_ms,
        "voice_id": returned_voice_id,
        "text_hash": text_hash,
    }))


if __name__ == "__main__":
    main()
