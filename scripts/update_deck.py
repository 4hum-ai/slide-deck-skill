#!/usr/bin/env python3
"""
Update an existing deck with a new Claude-generated deckJson.

Usage:
    python update_deck.py <deck_id> '<deckJson JSON string>'
    echo '<deckJson>' | python update_deck.py <deck_id>

Prints JSON: { "deck_id": "...", "deck_url": "..." }
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth import get_credentials

# Windows cp1252 guard
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

API_URL = os.environ.get("OPEN_ACADEMY_API_URL", "https://open-academy-api-mz4xquo5lq-as.a.run.app")
APP_URL = os.environ.get("OPEN_ACADEMY_APP_URL", "https://deck.4hum.ai")


def _put(path: str, body: dict, token: str, workspace_id: str) -> dict:
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{API_URL}{path}",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "x-workspace-id": workspace_id,
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            raise RuntimeError(f"HTTP {e.code}: {err.get('message', body_text)}") from e
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body_text}") from e


def main():
    if len(sys.argv) < 2:
        print("Usage: update_deck.py <deck_id> [<deckJson>]", file=sys.stderr)
        print("       echo '<deckJson>' | update_deck.py <deck_id>", file=sys.stderr)
        sys.exit(1)

    deck_id = sys.argv[1]

    if len(sys.argv) >= 3:
        raw = sys.argv[2]
    else:
        raw = sys.stdin.read().strip()

    if not raw:
        print("Error: deckJson is empty. Pass it as the second argument or pipe it via stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        deck_json = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: deckJson is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    token, workspace_id = get_credentials()

    result = _put(f"/api/decks/{deck_id}", {"deckJson": deck_json}, token, workspace_id)

    out_id = result.get("id") or deck_id
    deck_url = f"{APP_URL}/app/decks/{out_id}/edit"
    print(f"Deck updated: {deck_url}", file=sys.stderr)
    print(json.dumps({"deck_id": out_id, "deck_url": deck_url}))


if __name__ == "__main__":
    main()
