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

Prints JSON to stdout (human-readable lines go to stderr):

```text
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
automatically, but if you still hit encoding issues:

```powershell
# Option A (recommended) — use Bash tool instead of PowerShell for piping:
# In Claude Code, prefix with `bash -c` or use the Bash tool directly.
echo '{"deck":{"title":"New"}}' | python scripts/merge_deck.py "<id>"

# Option B — write JSON to a UTF-8 temp file then pipe:
Set-Content -Path patch.json -Value '{"deck":{"title":"New"}}' -Encoding utf8
Get-Content -Raw patch.json | python scripts/merge_deck.py "<id>"
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

**Themes:**
- `dark_tech_theme(overrides=None)`, `light_corporate_theme(overrides=None)`

**Primitive objects:**
- `text(role, x, y, w, h, content)`, `rich_text(role, x, y, w, h, runs)`
- `shape(x, y, w, h, fill_token)`, `line(x, y, w)`
- `image(seed_or_url, x, y, w, h)`
- `video(src, x, y, w, h)` — native video file
- `embed(url, x, y, w, h)` — YouTube / Vimeo / iframe
- `frame(x, y, w, h, frameKind=…, src=…)` — device/picture-frame mockup
- `qr_code(url, x, y, size)`, `qr_vcard(contact, x, y, size)` — QR codes
- `latex_text(formula, x, y, w, h)` — KaTeX equation

**Data objects:**
- `chart(x, y, w, h, categories, series, chart_type="bar")`
- `table(x, y, w, h, rows)` — 2D list of strings
- `diagram(x, y, w, h, source)` — Mermaid source string

**Composite layouts:**
- `card(x, y, w, h, heading, body)` → list of objects
- `title_chip(label, x, y, width)`, `portrait_card(…)`, `kpi_card(…)`
- `process_flow(items, x, y, w, h)`, `comparison_columns(columns, x, y, w, h)`
- `grid(items, cols, x, y, total_w, total_h)`

**Slide structure:**
- `slide(objects, notes="", speaker_notes="", animate=True)`
- `section(title, slides)`, `deck(title, sections, theme=…)`

Pass `animate=False` to `slide()` for reference-style decks where entrance
animations would be distracting.

See `references/objects-guide.md` for full field reference and design patterns.

Use the example generator as a template:

```bash
python examples/agent_skills_marketplace.py
```
