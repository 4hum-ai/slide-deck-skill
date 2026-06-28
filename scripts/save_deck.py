#!/usr/bin/env python3
"""
Save a Claude-generated deckJson to deck-4hum-ai.

Usage:
    python save_deck.py "My Title" '<deckJson JSON string>'
    echo '<deckJson>' | python save_deck.py "My Title"
    python save_deck.py "My Title"    # reads deckJson from stdin

Prints JSON: { "deck_id": "...", "deck_url": "..." }

The deckJson must follow the slide-scene-graph v0.4.0 envelope:
  {
    "schema": "open-academy.slide-scene-graph",
    "schemaVersion": "0.4.0",
    "deck": { "id": "...", "title": "...", ... }
  }
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth import get_credentials

API_URL = os.environ.get("OPEN_ACADEMY_API_URL", "https://open-academy-api-mz4xquo5lq-as.a.run.app")
APP_URL = os.environ.get("OPEN_ACADEMY_APP_URL", "https://deck.4hum.ai")


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
        print("Usage: save_deck.py <title> [<deckJson>]", file=sys.stderr)
        print("       echo '<deckJson>' | save_deck.py <title>", file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1]

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

    result = _post(
        "/api/decks",
        {"workspaceId": workspace_id, "title": title, "deckJson": deck_json},
        token,
        workspace_id,
    )

    deck_id = result.get("id") or (result.get("data") or {}).get("id")
    if not deck_id:
        print(f"Error: unexpected response: {result}", file=sys.stderr)
        sys.exit(1)

    deck_url = f"{APP_URL}/app/decks/{deck_id}/edit"
    print(f"Deck saved: {deck_url}")
    print(json.dumps({"deck_id": deck_id, "deck_url": deck_url}))


if __name__ == "__main__":
    main()
