# Python Commands and API Scripts

All operational tooling in this skill is Python.

## Authentication

```bash
python scripts/auth.py
```

Credentials are saved to `~/.open-academy/config.json`.

Environment overrides:

| Variable | Purpose |
|---|---|
| `OPEN_ACADEMY_TOKEN` | API token override |
| `OPEN_ACADEMY_WORKSPACE_ID` | Workspace UUID override |
| `OPEN_ACADEMY_API_URL` | API base URL |
| `OPEN_ACADEMY_APP_URL` | App base URL |

## Validate

```bash
python examples/agent_skills_marketplace.py | python scripts/deck_validator.py
```

`save_deck.py` also runs this validator automatically before auth/network calls.

## Save

```bash
python scripts/save_deck.py "My Deck Title" < deck.json
```

The script prints:

```text
Deck saved: https://deck.4hum.ai/app/decks/<id>/edit
{"deck_id":"<id>","deck_url":"https://deck.4hum.ai/app/decks/<id>/edit"}
```

## Update

```bash
python scripts/update_deck.py "<deck-id>" < deck.json
```

## Generate Image

```bash
python scripts/generate_image.py "Futuristic server room, dark neon lighting" --size 1920x1080
```

Use the returned `file_url` as an image object's `src`.

## Python Layout Helpers

`scripts/deck_patterns.py` includes schema-safe builders for:

- `dark_tech_theme`
- `text`, `rich_text`, `shape`, `line`, `image`
- `chart`, `table`, `diagram`
- `card`, `title_chip`, `process_flow`, `comparison_columns`
- `slide`, `section`, `deck`

Use the example generator as a template:

```bash
python examples/agent_skills_marketplace.py
```
