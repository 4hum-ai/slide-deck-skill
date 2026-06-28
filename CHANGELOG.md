# Changelog

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
