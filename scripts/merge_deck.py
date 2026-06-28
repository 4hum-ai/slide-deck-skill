#!/usr/bin/env python3
"""
Deep-merge a partial deck JSON fragment into an existing deck and PUT the result.

This is the token-efficient update path when only part of the deck changes —
the agent outputs only the changed subtree; this script fetches the existing deck,
merges, validates, and PUTs.

The merge follows RFC 7396 (JSON Merge Patch) semantics:
  - Objects are merged recursively (only the provided keys are updated)
  - Any value set to null removes the key from the target
  - Lists REPLACE (not append) — to modify a single item in a list use patch_slide.py

Usage:
    # Change a single theme color:
    echo '{"deck":{"theme":{"colors":{"accent":"#f97316"}}}}' | python scripts/merge_deck.py <deck-id>

    # Add or update speaker notes on one slide (include the full sections path):
    echo '{"deck":{"sections":[...partial...]}}' | python scripts/merge_deck.py <deck-id>

    # Rename the deck:
    echo '{"deck":{"title":"New Title"}}' | python scripts/merge_deck.py <deck-id>

Tip — combine with get_deck.py for a token-efficient edit loop:
    python scripts/get_deck.py <id> --theme   # read only the theme
    # ... edit the relevant fields ...
    echo '{"deck":{"theme":{...}}}' | python scripts/merge_deck.py <id>
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
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()}") from e
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


def _merge_patch(target: dict, patch: dict) -> dict:
    """Apply JSON Merge Patch (RFC 7396) recursively."""
    result = dict(target)
    for key, value in patch.items():
        if value is None:
            result.pop(key, None)
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge_patch(result[key], value)
        else:
            result[key] = value
    return result


def main() -> None:
    deck_id = sys.argv[1] if len(sys.argv) >= 2 else None
    if not deck_id:
        print("Usage: merge_deck.py <deck-id> < patch.json", file=sys.stderr)
        sys.exit(1)

    raw = sys.stdin.read().strip()
    if not raw:
        print("Error: pipe a partial deck JSON fragment to stdin", file=sys.stderr)
        sys.exit(1)
    try:
        patch = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    token, workspace_id = get_credentials()

    print(f"Fetching deck {deck_id} …", file=sys.stderr)
    existing = _fetch(deck_id, token, workspace_id)

    merged = _merge_patch(existing, patch)

    issues = validate_deck(merged)
    if issues:
        print(format_validation_errors(issues), file=sys.stderr)
        sys.exit(1)

    print("Validation passed. Merging …", file=sys.stderr)
    _put(deck_id, merged, token, workspace_id)

    edit_url = f"{APP_URL}/app/decks/{deck_id}/edit"
    print(f"Updated: {edit_url}")


if __name__ == "__main__":
    main()
