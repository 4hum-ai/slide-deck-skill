# Changelog

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.18.0] — 2026-06-29

### Added

- **`scripts/set_deck_music.py`**: New script for managing deck-level `mediaTracks[]` — the
  background music / ambient audio layer that plays across the full timeline. Modes: `--list`
  (print current tracks), `--url URL` (add a track from a URL with `--loop`, `--volume`,
  `--name`), `--add-track JSON_OR_FILE_OR_-` (append from JSON / file / stdin, auto-converts
  `generate_audio.py` output), `--remove-track <id>` (remove by id), `--clear` (remove all).
  Auto-normalises partial dicts and `generate_audio.py` format to `DeckMediaTrack` with all
  required fields (`id`, `kind`, `startMs`). Supports `--kind audio|video`, `--start-ms`,
  `--volume 0.0–1.0`, `--loop` for music beds.

- **`examples/skill_playbook.py`**: New 9-slide "Slide Deck Agent Playbook" meta-deck (deck ID
  `48389dc0-9543-4622-817d-8c8fa7347845`). Demonstrates all advanced skill capabilities:
  the full toolkit table, 9-step Mermaid workflow, object-types chart+table, AI asset generation
  comparison, narration track flow diagram, background music diagram, advanced patterns
  (frame, LaTeX, QR, diagram), and a 4-item roadmap. Theme: Skill Blueprint (Space Grotesk,
  dark navy `#0d1117`, purple `#7c3aed`, cyan `#06b6d4`). Ships with per-slide narration
  (George, 9 tracks) and deck-level background ambience (`deck.mediaTracks[]`, River voice,
  loop=true, volume=0.12).

## [1.17.0] — 2026-06-29

### Added

- **`scripts/generate_audio.py`**: New script for AI narration / TTS audio generation.
  Calls `GET /api/media/voices` to list available voices and `POST /api/media/voices/:id/generate`
  (synchronous — no polling) to generate audio. Flags: `--list-voices`, `--voice-id <uuid>`,
  `--default-voice` (uses first available system voice), `--speed 0.5–2.0`, and `--deck-id` /
  `--slide-id` for analytics association. Reads text from a positional argument or stdin (pipes).
  Prints `{"audio_url":"...","duration_ms":N,"voice_id":"...","text_hash":"..."}` to stdout,
  compatible with `patch_slide.py --add-narration-track` for zero-reshaping piping.

- **`scripts/patch_slide.py` — narration track operations**:
  - `--add-narration-track JSON_OR_FILE_OR_-`: appends a `NarrationTrack` to `slide.narrationTracks[]`.
    Accepts a JSON string, a file path to a `.json` file, or `-` for stdin. Auto-converts
    `generate_audio.py` output format (`{audio_url, duration_ms, voice_id, text_hash}`) to a
    proper `NarrationTrack` (`{id, kind:"audio", url, startMs:0, durationMs, source:"tts", voiceId, textHash}`).
  - `--set-narration-tracks JSON_OR_FILE_OR_-`: replaces the slide's entire `narrationTracks` array.
  - Narration track operations work standalone (no stdin objects required) or combined with object replacement.

- **`references/objects-guide.md` — `audio` object type and `narrationTracks` section**:
  Full field reference for the `audio` canvas object type (src, autoplay, loop, muted, controls)
  and a new `narrationTracks` slide-level field section showing the complete `NarrationTrack` schema,
  the `patch_slide.py --add-narration-track` workflow, and the pipe pattern from `generate_audio.py`.

- **`references/commands.md` — "Generate Audio" section**: Full voice discovery and generation usage,
  both `--voice-id` and `--default-voice` modes, pipe-to-patch-slide pattern, and a multi-slide
  narration loop template. Also added `audio(src, x, y, w, h)` to the Python Layout Helpers list.

## [1.16.0] — 2026-06-29

### Added

- **`scripts/generate_video.py`**: New script mirroring `generate_image.py` for video
  generation. POSTs to `/api/media/generate-video` (always async), polls until the
  video is ready, and prints `{"media_id":"...","file_url":"...","duration_seconds":N}` to
  stdout. Supports all 4 API providers: `qwen` (Wan 2.2, default), `byteplus` (Seedance),
  `openai` (Sora 2), `gemini-veo` (Veo 3). Flags: `--size`, `--duration`, `--provider`,
  `--model`, `--image` (image-to-video), `--negative`.
- **`references/commands.md` — "Generate Video" section**: Full provider/size/duration
  table, image-to-video usage, and the canonical "poster image behind video" workflow
  pattern so agents generate the poster first, then the video, and layer them correctly.
- **`SKILL.md` — step 5**: Updated to mention `generate_video.py` alongside
  `generate_image.py`; documents the layered image+video pattern.

## [1.15.0] — 2026-06-29

### Fixed

- **`references/objects-guide.md` — frame `src` must be a static image URL**: Iteration 8
  (ML Mathematics, slide 6) used a live website URL (`https://teachablemachine.withgoogle.com`)
  as the frame `src`. The device bezel rendered correctly but the content area was blank —
  the frame renderer displays a static image, not a live iframe. Added explicit "Critical"
  callout with correct vs. wrong usage examples. Solution: screenshot the site (or generate
  a representative image) and use that PNG as `src`.

- **`references/objects-guide.md` — video layer workaround for headless preview**:
  `VideoRenderer.vue` shows a bare red error box (not the poster) when video fails to load in
  headless Playwright. Setting `poster` alone does NOT fix this. Verified workaround: layer a
  matching `image()` object directly behind the video at the same coordinates — in headless the
  image shows; in the production app the `<video>` overlays and plays. Added code pattern to
  objects-guide. Also added URL requirements: use CDN URLs you control (Cloudflare Stream,
  S3, GCS) — archive.org and streaming services have CORS restrictions.

## [1.14.0] — 2026-06-29

### Added

- **`SKILL.md` — "Text on Background Images" section**: Light-theme slides
  with dark hero images produce invisible text because `{"token":"foreground"}`
  resolves to dark navy. Iteration 6 (Renewable Energy) showed the cover title
  and closing-slide bullets were unreadable over the dark generated photos.
  New rule: add a semi-transparent scrim shape, use explicit `#ffffff`/`#1a1a1a`
  text, or use `primaryForeground` token (safe for both dark and light themes)
  for any text object that overlaps a full-bleed background image.

## [1.13.0] — 2026-06-29

### Fixed

- **`SKILL.md` — picsum.photos anti-pattern**: Agents were using
  `picsum.photos` with a content-specific seed (e.g. "lab", "genomics") and
  receiving completely unrelated images (fashion boutiques, mountains). Added
  explicit prohibition: never use `picsum.photos` for slides where image
  subject matters — use `generate_image.py` instead. Reserve `picsum.photos`
  only for texture fills where subject is irrelevant.
- **`SKILL.md` — source citation x-position on split-panel slides**: Added
  rule that the source footnote `x` must be inside the text panel, not inside
  the image panel. Source text at `x=80` inside a left-image panel renders
  over the image.

## [1.12.0] — 2026-06-29

### Fixed

- **`SKILL.md` — source citation y-position**: Added explicit rule that source/footnote
  text must be placed at `y=940` (not y=700–730). Agents were adding source captions
  at y≈720, which still left ~280 px of dead whitespace below — the same problem the
  "fill the vertical canvas" rule is meant to prevent. The rule now states: if main
  content ends before y=700, add a secondary fill element (insight text, divider + stat)
  in y=700–860, then anchor the source at y=940.

## [1.11.0] — 2026-06-28

### Added

- **`SKILL.md` — "Text Length and Whitespace Rules" section**: Bullet list
  character limits by panel width (55 chars for half-panel, 75 for two-thirds,
  100 for full-width) prevent mid-sentence wrapping inside `bullet_list()`.
  "Fill the vertical canvas" guidance: content zone is y=80–1000; don't cluster
  objects in the top 600 px and leave 400 px of empty black at the bottom — use
  a caption, extend charts/tables, or add a divider + secondary stat.

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
