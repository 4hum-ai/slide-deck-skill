#!/usr/bin/env python3
"""
Generate an AI video and store it in the workspace media library.

Usage:
    python generate_video.py "quantum particles entangle, purple energy beams"
    python generate_video.py "prompt" --size 1280x720 --duration 5
    python generate_video.py "prompt" --provider qwen --duration 5
    python generate_video.py "prompt" --provider openai --duration 8
    python generate_video.py "prompt" --image https://... --duration 5

Prints JSON to stdout: { "media_id": "...", "file_url": "...", "duration_seconds": N }
Use file_url as the "src" field on a video object in the deck JSON.

Combine with an image() at the same position as a poster fallback in headless previews
(see objects-guide.md — VideoRenderer shows an error box, not the poster, in headless).

Providers and supported sizes:
  qwen        Alibaba Wan   — 1280x720, 1920x1080, 480x832 — 5s
  byteplus    Seedance      — 1280x720, 1920x1080, 720x1280 — 5s, 10s
  openai      Sora          — 1280x720, 720x1280 — 4s, 8s, 12s
  gemini-veo  Google Veo    — 1280x720, 1920x1080, 720x1280 — 8s (fixed)
"""
import argparse
import json
import os
import sys
import time
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

POLL_INTERVAL = 6    # seconds between status polls
POLL_TIMEOUT  = 360  # give up after 6 minutes


def _request(method: str, path: str, body: dict | None, token: str, workspace_id: str) -> dict:
    payload = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(
        f"{API_URL}{path}",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "x-workspace-id": workspace_id,
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            raise RuntimeError(f"HTTP {e.code}: {err.get('message', body_text)}") from e
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body_text}") from e


def poll_until_ready(media_id: str, token: str, workspace_id: str) -> dict:
    deadline = time.time() + POLL_TIMEOUT
    attempt = 0
    while time.time() < deadline:
        result = _request("GET", f"/api/media/{media_id}", None, token, workspace_id)
        media = result.get("data") or result
        status = media.get("status")
        if status == "uploaded":
            print("", file=sys.stderr)  # newline after progress dots
            return media
        if status in ("failed", "error"):
            raise RuntimeError(f"Video generation failed: {media.get('error', media.get('message', 'unknown'))}")
        attempt += 1
        dots = "." * (attempt % 4 + 1)
        elapsed = int(time.time() - (deadline - POLL_TIMEOUT))
        print(f"\r  Generating{dots:<4} ({elapsed}s elapsed)  ", end="", file=sys.stderr)
        time.sleep(POLL_INTERVAL)
    raise RuntimeError(f"Video generation timed out after {POLL_TIMEOUT}s — check the media library for status.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate an AI video for a slide deck",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Providers:
  qwen        Qwen Wan 2.2 (default) — fast, good motion quality, 5s clips
  byteplus    BytePlus Seedance — good realism, 5s or 10s
  openai      OpenAI Sora 2 — cinematic quality, 4–12s, higher credits
  gemini-veo  Google Veo 3 — photorealistic, 8s fixed duration

Size guidance for slide decks:
  1280x720  (default) — widescreen panel, half-slide or two-thirds width
  1920x1080           — full-slide background video (use with overlay text)
  720x1280            — vertical/portrait format, side panel

Rate limit: allow ~30s between generate_video calls to avoid 429 errors.
        """,
    )
    parser.add_argument("prompt", help="Detailed visual description of the video (be specific about motion, lighting, style)")
    parser.add_argument(
        "--size", default="1280x720",
        help="WIDTHxHEIGHT (default: 1280x720). Auto-snapped to nearest provider-supported size.",
    )
    parser.add_argument(
        "--duration", type=int, default=5,
        help="Duration in seconds (default: 5). Auto-snapped to provider's supported values.",
    )
    parser.add_argument(
        "--provider", choices=["qwen", "byteplus", "openai", "gemini-veo"], default=None,
        help="Video generation provider (default: workspace default, usually qwen).",
    )
    parser.add_argument(
        "--model", default=None,
        help="Provider-specific model override (advanced). Omit to use the provider's default model.",
    )
    parser.add_argument(
        "--image", default=None, dest="reference_image_url",
        help="Reference image URL for image-to-video. The video animates from this image.",
    )
    parser.add_argument(
        "--negative", default=None, dest="negative_prompt",
        help="Negative prompt — describe what to avoid (e.g. 'text, watermarks, blurry').",
    )
    args = parser.parse_args()

    token, workspace_id = get_credentials()

    body: dict = {
        "prompt": args.prompt,
        "size": args.size,
        "durationSeconds": args.duration,
        "workspaceId": workspace_id,
        "async": True,  # always async — video gen takes 30s–4min depending on provider
    }
    if args.provider:
        body["provider"] = args.provider
    if args.model:
        body["model"] = args.model
    if args.reference_image_url:
        body["referenceImageUrl"] = args.reference_image_url
    if args.negative_prompt:
        body["negativePrompt"] = args.negative_prompt

    prompt_preview = args.prompt[:80] + ("…" if len(args.prompt) > 80 else "")
    print(f"Submitting video generation: {prompt_preview}", file=sys.stderr)
    if args.provider:
        print(f"  Provider: {args.provider} | Size: {args.size} | Duration: {args.duration}s", file=sys.stderr)

    result = _request("POST", "/api/media/generate-video", body, token, workspace_id)
    media = result.get("data") or result
    media_id = media.get("id")

    if not media_id:
        print(f"Error: unexpected response — no media ID: {result}", file=sys.stderr)
        sys.exit(1)

    print(f"Video queued (id={media_id}). Polling for completion…", file=sys.stderr)
    media = poll_until_ready(media_id, token, workspace_id)

    file_url = media.get("fileUrl") or media.get("url")
    if not file_url:
        print(f"Error: no URL in completed media object: {media}", file=sys.stderr)
        sys.exit(1)

    duration = media.get("durationSeconds") or args.duration
    provider_used = media.get("providerId", args.provider or "default")
    print(f"Video ready! Provider: {provider_used} | Duration: {duration}s", file=sys.stderr)
    print(f"  URL: {file_url}", file=sys.stderr)

    print(json.dumps({"media_id": media_id, "file_url": file_url, "duration_seconds": duration}))


if __name__ == "__main__":
    main()
