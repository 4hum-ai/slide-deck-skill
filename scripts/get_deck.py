#!/usr/bin/env python3
"""
Fetch a specific slice of a deck so the agent only reads what it needs.

Token-efficient alternative to fetching the full deckJson when the agent
only needs to inspect one slide, the theme, or the high-level outline.

Usage:
    python scripts/get_deck.py <deck-id> --outline        # section/slide titles only
    python scripts/get_deck.py <deck-id> --theme          # theme object only
    python scripts/get_deck.py <deck-id> --slide N        # one slide's objects (0-based)
    python scripts/get_deck.py <deck-id> --section N      # all slides in one section (0-based)
    python scripts/get_deck.py <deck-id>                  # full deckJson (no filter)

Output is JSON — pipe to jq or straight into patch_slide.py / merge_deck.py:
    python scripts/get_deck.py <id> --slide 7 | jq '.objects | length'
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

API_URL = os.environ.get("OPEN_ACADEMY_API_URL", "https://open-academy-api-mz4xquo5lq-as.a.run.app")


def _fetch(deck_id: str, token: str, workspace_id: str) -> dict:
    req = urllib.request.Request(
        f"{API_URL}/api/decks/{deck_id}",
        headers={"Authorization": f"Bearer {token}", "x-workspace-id": workspace_id},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()}") from e
    row = data.get("data") or data
    raw = row.get("deckJson") or row
    return json.loads(raw) if isinstance(raw, str) else raw


def _outline(deck_json: dict) -> list[dict]:
    """Return a compact outline: section titles + per-slide index, title, object counts."""
    deck = deck_json.get("deck", deck_json)
    result = []
    slide_n = 0
    for si, sec in enumerate(deck.get("sections", [])):
        slides_out = []
        for li, slide in enumerate(sec.get("slides", [])):
            objs = slide.get("objects", [])
            from collections import Counter
            counts = dict(Counter(o.get("type", "?") for o in objs))
            heading = next(
                (o.get("content", "") if isinstance(o.get("content"), str)
                 else "".join(r.get("text", "") for b in o.get("content", []) for r in b.get("runs", []))
                 for o in objs if o.get("role") in ("title", "heading")),
                "",
            )
            slides_out.append({
                "globalIndex": slide_n,
                "sectionIndex": si,
                "slideIndex": li,
                "id": slide.get("id", ""),
                "heading": heading[:80],
                "objectCounts": counts,
            })
            slide_n += 1
        result.append({
            "sectionIndex": si,
            "title": sec.get("title", ""),
            "slides": slides_out,
        })
    return result


def _all_slides(deck_json: dict) -> list[tuple[int, int]]:
    deck = deck_json.get("deck", deck_json)
    result = []
    for si, sec in enumerate(deck.get("sections", [])):
        for li in range(len(sec.get("slides", []))):
            result.append((si, li))
    return result


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Fetch a slice of a deck JSON.")
    parser.add_argument("deck_id", help="Deck UUID")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--outline", action="store_true",
                       help="Print compact section/slide outline (smallest output)")
    group.add_argument("--theme", action="store_true",
                       help="Print just the theme object")
    group.add_argument("--slide", type=int, metavar="N",
                       help="Print one slide's data (0-based global index)")
    group.add_argument("--section", type=int, metavar="N",
                       help="Print all slides in one section (0-based index)")
    args = parser.parse_args()

    token, workspace_id = get_credentials()
    print(f"Fetching deck {args.deck_id} …", file=sys.stderr)
    deck_json = _fetch(args.deck_id, token, workspace_id)
    deck = deck_json.get("deck", deck_json)

    if args.outline:
        print(json.dumps(_outline(deck_json), indent=2))

    elif args.theme:
        print(json.dumps(deck.get("theme", {}), indent=2))

    elif args.slide is not None:
        positions = _all_slides(deck_json)
        if args.slide >= len(positions):
            print(f"Error: slide index {args.slide} out of range "
                  f"(deck has {len(positions)} slides)", file=sys.stderr)
            sys.exit(1)
        si, li = positions[args.slide]
        slide = deck["sections"][si]["slides"][li]
        print(json.dumps(slide, indent=2))

    elif args.section is not None:
        sections = deck.get("sections", [])
        if args.section >= len(sections):
            print(f"Error: section index {args.section} out of range "
                  f"(deck has {len(sections)} sections)", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(sections[args.section], indent=2))

    else:
        print(json.dumps(deck_json, indent=2))


if __name__ == "__main__":
    main()
