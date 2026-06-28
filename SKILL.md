---
name: slide-deck-skill
description: >
  Create, edit, and publish professional slide decks on deck.4hum.ai. Generates
  deckJson from the slide-scene-graph v0.4.0 schema, validates locally, and
  saves via Python scripts. Use when the user asks to make a presentation, slide
  deck, slideshow, pitch deck, or iteratively improve one. Covers themes,
  charts, tables, diagrams, speaker notes, animations, and AI-generated images.
license: MIT — see LICENSE
compatibility: >
  Python 3.8+. Requires network access to the deck.4hum.ai API. Designed for
  Claude Code and agentskills.io-compatible agent implementations.
allowed-tools: Bash Read
metadata:
  platform: deck-4hum-ai
  author: phong.nguyen@4hum.ai
  version: "1.1.0"
  argument-hint: "<topic or title for the deck>"
---

# slide-deck-skill

You are the slide-content generator. Scripts available to authenticate, validate,
generate hosted images, save decks, and update decks through the REST API.

## References

Load these only when needed:

- `references/theme-presets.md` - theme choice, color tokens, typography scale.
- `references/scene-graph.md` - envelope, object schemas, animations, notes.
- `references/commands.md` - Python script commands, environment variables, helper API.

Use `scripts/deck_patterns.py` for common layouts when writing a generator. See
`examples/agent_skills_marketplace.py` for a complete Python example.

## Workflow

1. **Design a custom theme.** Read `references/theme-presets.md` to understand
   the six example presets — treat them as inspiration, not a pick list. Create
   a new theme object that fits the topic, audience, and emotional tone:

   - **Color psychology**: blue/indigo = trust/tech, green = growth/nature,
     orange = energy/creativity, purple = innovation/bold, neutral dark = minimal
     keynote, white = formal/corporate.
   - **Font pairing**: use display/heading for impact titles, body for
     readability, mono only for code examples. Reference presets for proven pairs
     (Inter, Georgia, JetBrains Mono).
   - **Structural requirements**: the theme object must include `id` (new uuid),
     `name` (descriptive string), `fonts` (display, heading, body, mono), all
     required `colors` tokens (`background`, `surface`, `foreground`,
     `mutedForeground`, `primary`, `primaryForeground`, `accent`,
     `accentForeground`, `border`), and all six `textStyles` roles (`title`,
     `subtitle`, `heading`, `body`, `caption`, `code`).
   - Raw hex values go inside `theme.colors` only; every object color field
     must use `{"token":"<name>"}` references.
   - Tell the user the theme name and the one-sentence rationale (color mood +
     typography) before generating the full JSON.

2. **Search for facts when needed.** If the topic involves factual claims,
   statistics, current events, product details, laws, or other changeable
   information, search first and cite source URLs in `speakerNotes`.
3. **Plan the deck.** Define sections, slide titles, one claim per slide, and
   which slides need images. Write a one-line visual prompt for each custom
   image.
4. **Generate images when useful.** Use `scripts/generate_image.py` or the
   available image tool before writing final `deckJson`. Collect `file_url`
   values and use them as image `src` fields. Use deterministic `picsum.photos`
   URLs only for quick drafts or non-critical placeholders.
5. **Generate deck JSON.** Use the slide-scene-graph envelope and object shapes
   in `references/scene-graph.md`. Prefer `scripts/deck_patterns.py` for
   schema-safe cards, lines, tables, diagrams, sections, and deck envelopes.
6. **Preflight validate.** Run the local validator and fix every issue:
   ```bash
   python examples/agent_skills_marketplace.py | python scripts/deck_validator.py
   ```
   Replace the first command with your own generator. `save_deck.py` also runs
   validation automatically before auth or network calls.
7. **Save.**
   ```bash
   python scripts/save_deck.py "Title" < deck.json
   ```
   Or pipe generator output directly:
   ```bash
   python examples/agent_skills_marketplace.py | python scripts/save_deck.py "Agent Skills & Skills Marketplace"
   ```
8. **Preview and evaluate.** After saving, use `scripts/preview_deck.py` to
   capture screenshots of the rendered slides. Review each slide image; fix
   layout, contrast, or content issues before delivering to the user.
   ```bash
   python scripts/preview_deck.py "<deck-id>"
   ```
   The script opens each slide in the browser and saves PNGs locally. If
   browser tools are available in the session, use them to inspect individual
   slides at `https://deck.4hum.ai/app/decks/<id>/edit`.
9. **Return the URL.** Always surface the edit URL printed by the script:
   `[Open deck](https://deck.4hum.ai/app/decks/<id>/edit)`.
10. **Iterate.** If the preview reveals issues or the user requests changes,
    fix the JSON and call `scripts/update_deck.py`, then re-preview:
    ```bash
    python scripts/update_deck.py "<deck-id>" < deck.json
    python scripts/preview_deck.py "<deck-id>"
    ```

## Preflight Rules

The validator catches many of these, but follow them while authoring:

- Every object needs `id`, `type`, `x`, `y`, `width`, and `height`.
- `width` and `height` must never be negative. Use positive bounds for visible
  objects, including divider lines.
- Every text object must set `role`: `title`, `subtitle`, `heading`, `body`,
  `caption`, or `code`.
- Compact cards should use `body` or `caption` text roles, not large `heading`
  text.
- Every line object must include `start` and `end` points.
- Use token refs for object colors, such as `{"token":"foreground"}`.
- Tables must include `styling.headerText.color` and
  `styling.bodyText.color`.
- Table `cells` must be a rectangular 2D array matching `rows` and `cols`.

## Content Rules

- Use `notes` when the deck is educational, training-oriented, for live
  presentation, or likely to be used with narration/TTS.
- Use `speakerNotes.content` for citations, talking points, and presenter-only
  reminders.
- Use simple transitions by default: `{"effect":"fade","durationMs":400}`.
- Include animations for live-presentation decks; omit them for reference-style
  documents unless they clarify sequencing.
- Keep layouts on the 1920 x 1080 canvas and leave enough whitespace for text to
  render without clipping.

## Common Commands

```bash
python scripts/auth.py
python examples/agent_skills_marketplace.py | python scripts/deck_validator.py
python examples/agent_skills_marketplace.py | python scripts/save_deck.py "Agent Skills & Skills Marketplace"
python scripts/preview_deck.py "<deck-id>"               # inspect a saved deck
python my_generator.py | python scripts/preview_deck.py  # inspect before saving
python scripts/update_deck.py "<deck-id>" < deck.json
python scripts/generate_image.py "A futuristic server room, blue accent lighting" --size 1920x1080
```
