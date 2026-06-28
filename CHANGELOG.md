# Changelog

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.10.0] — 2026-06-28

### Fixed

- **`block_builder.py` — `bullet_list()` two-tier format**: `{"title": "...", "body": "..."}` dict
  items now render as `• Title: body text` on a single line, not `• Title\n     body` with an
  indented continuation line that wraps awkwardly. The `: ` separator lets text flow naturally.

### Added

- **`references/objects-guide.md` — embed limitations**: YouTube and Vimeo enforce CSP/referrer
  restrictions that show "Error 153" in sandboxed iframes and headless browsers. Prefer `qr`
  (always works), `video` (direct .mp4 URL), or `frame` + thumbnail + play-button overlay.
  Reserve `embed` for sources that explicitly support iframe embedding (internal dashboards,
  Figma prototypes, Google Slides "Publish to web").
- **`references/objects-guide.md` — Mermaid theme config**: Added `%%{init: ...}%%` header
  pattern so agents can match Mermaid diagram colors to the slide theme (node fill, border,
  arrows). Default Mermaid palette (amber/yellow) clashes with most custom slide themes.
- **`SKILL.md` — "Embed Caution" section**: Pre-flight warning about YouTube/Vimeo embed
  failures, with three always-reliable alternatives (QR, video, frame+thumbnail).

## [1.9.0] — 2026-06-28

### Added

- **`block_builder.py`** — `bullet_list(items, x, y, w, h, numbered=False)` and
  `numbered_list()`: single text objects for bullet/numbered lists. Replaces the
  anti-pattern of repeating `card()` for each item (7 cards = 21 objects → 1
  `bullet_list()` = 1 object). Items can be plain strings or
  `{"title": "…", "body": "…"}` dicts for two-line entries.
- **`SKILL.md`**: "Slide Density Rules" section — explicit "≤12 objects per slide,
  max 14" rule, per-slide image rule (at least 1 image per 3 slides), and
  "max 4 feature cards per slide" guideline with an anti-pattern table.
- **`deck_validator.py`**: object density warning in `--strict` mode — flags slides
  with > 14 objects and suggests `bullet_list()` or `grid()` as the fix.
- **`references/commands.md`**: documents `bullet_list()` and `numbered_list()`
  under "List objects" category; clarifies `grid()` column guidance (cols=2,
  max 4 items for feature grids).

## [1.7.0] — 2026-06-28

### Fixed

- **`generate_image.py`, `save_deck.py`, `update_deck.py`**: human-readable
  status lines now go to `stderr`; only the JSON result object goes to
  `stdout`. This prevents `"Image generated: ..."` and `"Deck saved: ..."`
  strings from corrupting downstream JSON parsing when scripts are piped.
- **`generate_image.py`, `save_deck.py`, `update_deck.py`**: added
  `sys.stdout/stderr.reconfigure(encoding="utf-8")` guard (already present in
  the other scripts) so Windows cp1252 doesn't corrupt non-ASCII output.
- **`deck_validator.py`**: custom theme tokens (colors defined in
  `theme.colors` beyond the standard set) no longer trigger a validation error.
  `validate_deck()` now extracts the deck's own token names and allows them in
  all color fields — enabling themes with custom palette entries like
  `"highlight"` or `"gradientStart"`.

### Added

- **`block_builder.py`** — `light_corporate_theme(overrides=None)`: a
  ready-to-call light-background preset matching the Light Corporate JSON
  example in `references/theme-presets.md`. Accepts the same `overrides` dict
  as `dark_tech_theme()`.
- **`block_builder.py`** — `slide()` now accepts `animate=True` keyword
  argument. Pass `animate=False` to produce a slide with an empty animations
  list, suitable for reference-style documents where entrance effects are
  distracting.
- **`references/commands.md`**: token cost guide for `get_deck.py` modes
  (outline ≈ 200, slide ≈ 800, full deck ≈ 3000–8000 tokens).

### Changed

- **`references/commands.md`**: removed the dangerous "Option B" (Python
  `exec()` on file content) from the Windows PowerShell stdin workarounds.
  Option A (Bash tool) is now the recommended path; Option B is a safe
  `Get-Content -Raw` temp-file approach.
- **`references/theme-presets.md`**: added a note that both presets are
  callable as `dark_tech_theme()` / `light_corporate_theme()` in
  `block_builder.py` with an `overrides` dict.
- **`SKILL.md`**: step 4 (theme design) now mentions the two callable helpers
  as starting points; step 5 (image generation) and step 8 (save) clarify the
  stdout-only JSON output contract.

## [1.6.0] — 2026-06-28

### Changed

- `SKILL.md` workflow now has **11 steps** with a two-phase research model:
  - **Step 1 — Domain research**: one or two broad searches to understand the
    topic, tone, and narrative angle before planning anything.
  - **Step 3 — Fact-check the outline**: after planning, a second narrower
    search verifying each specific claim/statistic/date in the outline. Source
    URLs cited in `speakerNotes`.
  - Theme design is now step 4 (was step 3), informed by all three prior steps.
  - Steps 5–11 renumbered from the previous 4–10 (no content changes).

## [1.5.0] — 2026-06-28

### Changed

- `references/theme-presets.md` trimmed from 6 presets to 2 (Dark Tech + Light
  Corporate). The other four presets (Warm Creative, Midnight Minimal, Forest
  Green, Neon Purple) are removed — they added token weight without adding
  structural value, since the workflow instructs agents to create fully custom
  themes anyway. The Font Mood Reference table and Color Tokens section are
  retained. The selection table is updated to frame the two examples as dark-vs-
  light starting points, not a fixed pick list.
- `SKILL.md` workflow reordered: **facts (step 1) → plan (step 2) → theme
  (step 3)**. Previously theme design was step 1, before the agent understood
  the topic or structure. The reorder ensures content knowledge informs the
  aesthetic — the sport/finance/culture of the subject drives font and color
  choices, not the reverse. Steps 4–10 are unchanged.

## [1.4.0] — 2026-06-28

### Added

- `scripts/patch_slide.py --notes TEXT` and `--speaker-notes TEXT` — update a
  slide's narration text or presenter notes without touching objects; works
  standalone or combined with object replacement. stdin is now optional when
  only notes are being updated.
- `references/commands.md` — "Visual evaluation via browser tools" section with
  the exact mcp__claude-in-chrome__ screenshot pattern for render URLs;
  "Windows / PowerShell notes" section documenting the UTF-16 BOM workaround for
  `echo '...' | python scripts/merge_deck.py` on PowerShell.

### Fixed

- **Windows encoding bug (critical)**: all scripts crashed on Windows cp1252
  consoles when printing characters such as `…`, `×`, `⚠`, or `•`. Fixed by
  adding `sys.stdout/stderr.reconfigure(encoding='utf-8', errors='replace')` at
  the top of every script (`preview_deck.py`, `patch_slide.py`, `merge_deck.py`,
  `get_deck.py`).
- **PowerShell BOM bug in `merge_deck.py`**: `echo '...' | python scripts/merge_deck.py`
  failed because PowerShell outputs UTF-16 with a BOM. `merge_deck.py` now reads
  from `sys.stdin.buffer` and strips UTF-16/UTF-8 BOMs automatically before
  JSON-decoding.
- `preview_deck.py` now prints per-slide render URLs
  (`/slides/:deckId/:slideIndex/render`) for visual evaluation via browser tools,
  replacing the generic "open the Edit URL" instruction.

## [1.3.0] — 2026-06-28

### Added

- `scripts/get_deck.py` — projection fetch: prints only the requested slice of a
  deck (use `--outline` for a compact index, `--slide N` for one slide's full
  JSON, `--theme` for the theme object, `--section N` for one section). Avoids
  putting the entire deck JSON in the agent's context for targeted edits.
- `scripts/merge_deck.py` — RFC 7396 JSON Merge Patch writer: accepts a partial
  deck fragment from stdin, deep-merges into the live deck, validates, and PUTs.
  The agent outputs only the changed subtree rather than the full deck.
- `SKILL.md` — "Token-Efficient Edit Pattern" section documenting the new
  sparse-read + targeted-write workflow.

### Changed

- `scripts/deck_patterns.py` renamed to `scripts/block_builder.py` to align
  with the UI's "block" concept (each helper returns a list of slide objects).
  `deck_patterns.py` kept as a re-export shim for backwards compatibility.
- All references updated to `block_builder.py` in SKILL.md, README.md, commands.md,
  and the example generator.

## [1.2.0] — 2026-06-28

### Added

- `scripts/patch_slide.py` — targeted single-slide editor: fetch a live deck,
  replace objects, insert a new slide after a given index, or delete a slide,
  then validate and PUT — much faster than regenerating the full deck.
- `scripts/deck_patterns.py` — three new layout helpers:
  - `portrait_card(image_url, name, subtitle, body, x, y, w, h)` — vertical
    card with a portrait photo on top and name/subtitle/body text below.
  - `kpi_card(value, label, x, y, w, h)` — large KPI number with a small
    descriptive label.
  - `grid(items, cols, x, y, total_w, total_h, gap)` — uniform grid
    distributing callable or dict items into rows × cols, returning a flat
    objects list.
- `scripts/deck_validator.py --strict` — optional quality pass: warns on
  missing notes on content slides, missing transitions, theme textStyle
  fontSize below 20 px, and full-bleed images without a contrast overlay.
- `scripts/preview_deck.py --theme-check` — WCAG contrast ratio check for the
  five key theme token pairs (foreground/background, foreground/surface,
  muted/background, primary pair, accent pair); reports AA / AAA pass/fail.
- `references/image-prompts.md` — proven prompt templates for portrait images,
  hero backgrounds, section divider strips, icons, and data visualization
  elements; includes sizing guide, rate-limit notes, and retry advice.
- `references/commands.md` — image sizing table (use-case → `--size` flag) and
  `patch_slide.py` usage section.
- `references/theme-presets.md` — font mood reference table: eight typeface
  families mapped to emotional register and best-pairing body font.

## [1.1.0] — 2026-06-28

### Added

- `scripts/preview_deck.py` — per-slide structural inspector: fetches a saved
  deck by ID or reads fresh JSON from stdin; prints theme name, per-slide
  headline text and object-type counts, bounding-box warnings, the edit URL,
  and visual inspection instructions for browser tools.
- `references/commands.md` — Preview / Inspect section documenting the new
  script.
- `README.md` — install instructions for OpenAI Codex, GitHub Copilot (VS
  Code), Cursor, Gemini CLI, and Roo Code; "Updating the skill" section
  (pull latest + update deck content + maintainer version bump).

### Changed

- `SKILL.md` Workflow step 1 changed from "pick a preset theme" to "design a
  custom theme": agent now derives a new theme object matched to the topic's
  tone, audience, and color psychology using the six presets as inspiration
  rather than a fixed pick list.
- `SKILL.md` Workflow adds step 8 "Preview and evaluate" (run `preview_deck.py`
  after saving, use browser tools to screenshot, fix issues before delivery)
  and renames the old step 9 "Evaluate and iterate" to step 10 "Iterate"
  (re-preview after update).
- `README.md` "What it does" updated to reflect custom theme design and
  preview-evaluate loop.
- `SKILL.md` Common Commands section updated with `preview_deck.py` examples.

## [1.0.0] — 2025-10-01

### Added

- `SKILL.md` with full workflow: theme selection, fact search, deck planning,
  image generation, JSON authoring, preflight validation, save, and iterate.
- Six theme presets in `references/theme-presets.md`: Dark Tech, Light
  Corporate, Warm Creative, Midnight Minimal, Forest Green, Neon Purple.
- Slide scene-graph v0.4.0 reference in `references/scene-graph.md`: envelope,
  text, shape, image, chart, table, diagram, line, animations, transitions,
  notes.
- Python layout helpers in `scripts/deck_patterns.py`: `text`, `rich_text`,
  `shape`, `line`, `image`, `chart`, `table`, `diagram`, `card`, `title_chip`,
  `process_flow`, `comparison_columns`, `slide`, `section`, `deck`,
  `dark_tech_theme`.
- `scripts/auth.py` — credential management (`~/.open-academy/config.json`,
  env-var overrides).
- `scripts/deck_validator.py` — local preflight validator; checks required
  fields, non-negative dimensions, text roles, line points, color token usage,
  table cell shape.
- `scripts/save_deck.py` — pipe or pass deckJson, validates, then POSTs to
  `/api/decks`; prints edit URL.
- `scripts/update_deck.py` — PATCH an existing deck by ID.
- `scripts/generate_image.py` — generate a hosted image via the API and return
  its `file_url` for use as an image object `src`.
- `examples/agent_skills_marketplace.py` — complete five-slide deck generator
  demonstrating all major object types.
