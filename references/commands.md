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

## Preview / Inspect

```bash
# Fetch a saved deck by ID and print a per-slide structural summary:
python scripts/preview_deck.py "<deck-id>"

# Include WCAG contrast check for the theme:
python scripts/preview_deck.py "<deck-id>" --theme-check

# Inspect fresh JSON from a generator without saving:
python my_generator.py | python scripts/preview_deck.py
```

The script prints:
- Theme name + WCAG contrast report (with `--theme-check`)
- Per-slide: headline text, object-type counts (e.g. `2×text  1×image  1×chart`)
- Bounding-box warnings (non-positive sizes, canvas overflow)
- Edit URL
- **Per-slide render URLs** for browser-based screenshot evaluation:
  `https://deck.4hum.ai/slides/<deck-id>/<n>/render`

### Visual evaluation via browser tools

Each render URL renders a single slide at 1920×1080 with no chrome:

```
1. mcp__claude-in-chrome__navigate  → https://deck.4hum.ai/slides/<id>/<n>/render
2. mcp__claude-in-chrome__javascript_tool → wait for renderReady signal:
   await new Promise(r => {
     const iv = setInterval(() => {
       if (document.body.dataset.renderReady === 'true') { clearInterval(iv); r(); }
     }, 100)
   })
3. mcp__claude-in-chrome__computer  → screenshot
```

### Windows / PowerShell notes

On Windows, `echo '{...}' | python scripts/merge_deck.py` may fail because
PowerShell's `echo` outputs UTF-16 (with BOM). The scripts now handle BOMs
automatically, but if you still hit encoding issues use one of these
alternatives:

```powershell
# Option A — write JSON to a UTF-8 temp file:
Set-Content -Path patch.json -Value '{"deck":{"title":"New"}}' -Encoding utf8
Get-Content patch.json | python scripts/merge_deck.py "<id>"

# Option B — use Python inline to avoid shell encoding entirely:
python -c "import sys; sys.stdin = open(0,'rb'); exec(open('scripts/merge_deck.py').read())"

# Option C (simplest) — use Bash tool instead of PowerShell for piping:
echo '{"deck":{"title":"New"}}' | python scripts/merge_deck.py "<id>"
```

## Patch a Single Slide

```bash
# Replace objects on slide 7 (0-based global index):
echo '[{"type":"text",...}]' | python scripts/patch_slide.py <deck-id> 7

# Delete slide 3:
python scripts/patch_slide.py <deck-id> 3 --delete

# Insert a new slide after slide 4 (stdin = full slide JSON object):
echo '{"id":"...","background":{},"objects":[...]}' | python scripts/patch_slide.py <deck-id> 4 --insert-after
```

Fetches the live deck, applies the change, validates locally, then PUTs the
updated deck. Faster than regenerating and replacing the full deck.

## Image Sizing Guide

Pass `--size WxH` to `generate_image.py`. Match the size to the display region
so the renderer crops to fit without quality loss.

| Use case | Width | Height | Aspect | `--size` flag |
|---|---|---|---|---|
| Hero background (full slide) | 1920 | 1080 | 16:9 | `1920x1080` |
| Half-slide panel (left or right half) | 960 | 1080 | 9:16 | `960x1080` |
| Portrait card (player / speaker) | 720 | 900 | 4:5 | `720x900` |
| Square thumbnail / icon | 600 | 600 | 1:1 | `600x600` |
| Wide banner / accent strip | 1920 | 400 | — | `1920x400` |
| Section title background | 1920 | 540 | 32:9 | `1920x540` |

**Rate limit:** The API enforces ~1 req/2 s. Generate portrait images
sequentially (not in parallel) to avoid 429 errors. Retry after 15 s on a 429.

See `references/image-prompts.md` for proven prompt templates per image type.

## Python Layout Helpers

`scripts/block_builder.py` includes schema-safe block builders for:

- `dark_tech_theme`
- `text`, `rich_text`, `shape`, `line`, `image`
- `chart`, `table`, `diagram`
- `card`, `title_chip`, `process_flow`, `comparison_columns`
- `portrait_card`, `kpi_card`, `grid`
- `slide`, `section`, `deck`

Use the example generator as a template:

```bash
python examples/agent_skills_marketplace.py
```
