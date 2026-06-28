# Changelog

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
