#!/usr/bin/env python3
"""
Generate an AI image and store it in the workspace media library.

Usage:
    python generate_image.py "A futuristic server room, blue neon lighting, 4K"
    python generate_image.py "prompt text" --size 1920x1080 --style photorealistic

Prints JSON: { "media_id": "...", "file_url": "..." }
Use file_url as the "src" field on an image object in the deck JSON.
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

API_URL = os.environ.get("OPEN_ACADEMY_API_URL", "https://open-academy-api-mz4xquo5lq-as.a.run.app")


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
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            raise RuntimeError(f"HTTP {e.code}: {err.get('message', body_text)}") from e
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body_text}") from e


def main():
    parser = argparse.ArgumentParser(description="Generate an AI image for a slide deck")
    parser.add_argument("prompt", help="Detailed visual description of the image")
    parser.add_argument("--size", default="1920x1080", help="WIDTHxHEIGHT, e.g. 1920x1080 (default)")
    parser.add_argument("--style", default=None, help="Style hint: photorealistic, illustration, flat design, etc.")
    args = parser.parse_args()

    token, workspace_id = get_credentials()

    body = {
        "prompt": args.prompt,
        "size": args.size,
        "workspaceId": workspace_id,
    }
    if args.style:
        body["style"] = args.style

    result = _post("/api/media/generate-image", body, token, workspace_id)

    media = result.get("data") or result
    media_id = media.get("id")
    file_url = media.get("fileUrl") or media.get("url")

    if not file_url:
        print(f"Error: unexpected response: {result}", file=sys.stderr)
        sys.exit(1)

    print(f"Image generated: {file_url}")
    print(json.dumps({"media_id": media_id, "file_url": file_url}))


if __name__ == "__main__":
    main()
