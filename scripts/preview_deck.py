#!/usr/bin/env python3
"""
Inspect a deck and print a per-slide structural summary so the agent can
evaluate layout, content, and object distribution before delivering to the user.

Usage:
    python scripts/preview_deck.py <deck-id>          # fetch from API by ID
    python my_generator.py | python scripts/preview_deck.py   # inspect fresh JSON from stdin

Output:
    - Per-slide breakdown: title text, object type counts, bounding-box warnings
    - Deck edit URL (when fetching by ID)
    - Instructions for visual inspection via browser tools
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.error
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

API_URL = os.environ.get("OPEN_ACADEMY_API_URL", "https://open-academy-api-mz4xquo5lq-as.a.run.app")
APP_URL = os.environ.get("OPEN_ACADEMY_APP_URL", "https://deck.4hum.ai")


def _fetch_deck(deck_id: str) -> dict:
    from auth import get_credentials  # noqa: PLC0415

    token, workspace_id = get_credentials()
    req = urllib.request.Request(
        f"{API_URL}/api/decks/{deck_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "x-workspace-id": workspace_id,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} fetching deck {deck_id}: {e.read().decode()}") from e

    row = data.get("data") or data
    raw = row.get("deckJson") or row
    if isinstance(raw, str):
        raw = json.loads(raw)
    return raw


def _text_preview(obj: dict) -> str:
    content = obj.get("content", "")
    if isinstance(content, str):
        return content[:60].replace("\n", " ")
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            for run in block.get("runs", []):
                parts.append(run.get("text", ""))
        return "".join(parts)[:60].replace("\n", " ")
    return ""


def _bounds_warning(obj: dict) -> str | None:
    w = obj.get("width", 1)
    h = obj.get("height", 1)
    x = obj.get("x", 0)
    y = obj.get("y", 0)
    if w <= 0 or h <= 0:
        return f"non-positive size ({w}×{h})"
    if x + w > 1940 or y + h > 1100:
        return f"overflows canvas (x={x} y={y} w={w} h={h})"
    return None


def summarize(deck_json: dict) -> str:
    out: list[str] = []
    deck = deck_json.get("deck", deck_json)

    title = deck.get("title", "(untitled)")
    w = deck.get("width", 1920)
    h = deck.get("height", 1080)
    schema_ver = deck_json.get("schemaVersion", "?")
    out.append(f"Deck: {title!r}  canvas={w}×{h}  schema={schema_ver}")

    theme = deck.get("theme", {})
    out.append(f"Theme: {theme.get('name', '(unnamed)')}")
    out.append("")

    sections = deck.get("sections", [])
    warnings: list[str] = []
    slide_n = 0

    for sec in sections:
        out.append(f"── {sec.get('title', '(section)')}")
        for slide in sec.get("slides", []):
            slide_n += 1
            objs = slide.get("objects", [])
            counts = Counter(o.get("type", "?") for o in objs)
            count_str = "  ".join(f"{v}×{k}" for k, v in sorted(counts.items()))

            headline = next(
                (_text_preview(o) for o in objs if o.get("role") in ("title", "heading")),
                "",
            )
            out.append(f"  {slide_n:02d}  {headline[:48]!r}")
            out.append(f"      [{count_str or 'no objects'}]")

            for obj in objs:
                w_ = _bounds_warning(obj)
                if w_:
                    oid = obj.get("id", "?")[:8]
                    warnings.append(f"  Slide {slide_n:02d} obj {oid}: ⚠ {w_}")

    out.append("")
    out.append(f"Total: {slide_n} slides in {len(sections)} section(s)")

    if warnings:
        out.append("")
        out.append("Layout warnings (fix before delivering):")
        out.extend(warnings)
    else:
        out.append("No layout warnings.")

    return "\n".join(out)


def main() -> None:
    deck_id: str | None = None
    edit_url: str | None = None

    if len(sys.argv) >= 2 and not sys.argv[1].startswith("-"):
        deck_id = sys.argv[1]
        print(f"Fetching deck {deck_id} …", file=sys.stderr)
        try:
            deck_json = _fetch_deck(deck_id)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        edit_url = f"{APP_URL}/app/decks/{deck_id}/edit"
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            print(
                "Usage:\n"
                "  python scripts/preview_deck.py <deck-id>\n"
                "  python my_generator.py | python scripts/preview_deck.py",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            deck_json = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"Error: invalid JSON — {exc}", file=sys.stderr)
            sys.exit(1)

    print(summarize(deck_json))

    if edit_url:
        print(f"\nEdit URL:  {edit_url}")

    print(
        "\nVisual inspection:"
        "\n  • Open the Edit URL in a browser to see rendered slides."
        "\n  • In Claude Code, use the browser tools (mcp__claude-in-chrome__navigate +"
        "\n    mcp__claude-in-chrome__computer) to screenshot each slide and evaluate"
        "\n    layout, contrast, and content quality before closing the task."
    )


if __name__ == "__main__":
    main()
