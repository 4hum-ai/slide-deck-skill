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
  version: "1.18.0"
  argument-hint: "<topic or title for the deck>"
---

# slide-deck-skill

You are the slide-content generator. Scripts available to authenticate, validate,
generate hosted images, save decks, and update decks through the REST API.

## References

Load these only when needed:

- `references/theme-presets.md` - theme choice, color tokens, typography scale.
- `references/scene-graph.md` - envelope, object schemas, animations, notes.
- `references/objects-guide.md` - **all object types** with examples, design tips, and slide patterns. Load this when choosing which object types to use on a slide, or when using `video`, `embed`, `frame`, `qr`, `placeholder`, or `latex`.
- `references/commands.md` - Python script commands, environment variables, helper API.

Use `scripts/block_builder.py` for common block layouts when writing a generator.
See `examples/*` for a complete example.

## Workflow

1. **Domain research.** Run one or two broad searches to get oriented: key
   themes, main actors, tone, narrative angle, and what kind of audience this
   topic speaks to. The goal is understanding, not fact-gathering — what you
   learn here feeds directly into the deck plan and theme choices (sport →
   bold/high-contrast, finance → formal/neutral, culture → editorial/warm).
   Skip this step only for purely fictional or hypothetical topics.
2. **Plan the deck.** Define sections, slide titles, one claim per slide, and
   which slides need images. Write a one-line visual prompt for each custom
   image. Be specific: each slide title should be a concrete assertion, not a
   label.
3. **Fact-check the outline.** For every slide whose claim depends on a
   statistic, named figure, date, or current event, run a targeted search and
   confirm the number. Cite the source URL in `speakerNotes`. This is narrower
   than step 1 — you already know what you need; now you're verifying it.
4. **Design a custom theme.** With the topic, plan, and facts in hand, open
   `references/theme-presets.md`. Two ready-to-call helpers exist —
   `dark_tech_theme()` and `light_corporate_theme()` in `block_builder.py` —
   use them as starting points and pass `overrides` to customize colors and
   fonts, or build a fully custom theme using the structural reference. Create a
   theme that fits the topic, audience, and emotional tone established in steps
   1–3:

   - **Color psychology**: blue/indigo = trust/tech, green = growth/nature,
     orange = energy/creativity, purple = innovation/bold, neutral dark = minimal
     keynote, white = formal/corporate.
   - **Font pairing**: use display/heading for impact titles, body for
     readability, mono only for code examples. See the Font Mood Reference in
     `references/theme-presets.md` for proven font–topic pairings.
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
5. **Generate images, videos, and audio when useful.** Use the generation scripts
   before writing final `deckJson`. All scripts print JSON to stdout; human-readable
   lines go to stderr.

   **Images:** `python scripts/generate_image.py "PROMPT" --size 1920x1080`
   Returns `{"file_url":"..."}`. Use as `image.src`.

   **Videos:** `python scripts/generate_video.py "PROMPT" --size 1280x720 --duration 5`
   Returns `{"file_url":"...","duration_seconds":N}`. Use as `video.src`.
   Always also place a matching `image()` at the same position behind the video as
   a headless fallback (see the Video Slide Pattern in `references/commands.md`).

   **Audio / narration:** `python scripts/generate_audio.py "NARRATION TEXT" --default-voice`
   Returns `{"audio_url":"...","duration_ms":N,...}`. Pipe directly to `patch_slide.py` after
   saving the deck to attach a synchronized narration track:
   ```bash
   python scripts/generate_audio.py "Slide narration here." --default-voice | \
     python scripts/patch_slide.py <deck-id> <slide-index> --add-narration-track -
   ```
   Run `--list-voices` first to choose a voice; use `--voice-id` in production.

   **Do NOT use `picsum.photos` for content-relevant images.** `picsum.photos`
   serves random photos from a seeded pool — a seed intended for a "lab" or
   "genomics" shot may return a fashion boutique, a mountain, or a food photo.
   Use `generate_image.py` for any image whose subject matters to the slide
   (hero covers, half-panel lifestyle shots, portraits, section backgrounds).
   Reserve `picsum.photos` only for texture fills or placeholder regions where
   the subject is completely irrelevant (e.g. a pure-color background).
6. **Generate deck JSON.** Use the slide-scene-graph envelope and object shapes
   in `references/scene-graph.md`. Prefer `scripts/block_builder.py` for
   schema-safe blocks: cards, portrait cards, KPI cards, grids, lines, tables,
   diagrams, sections, and deck envelopes.
7. **Preflight validate.** Run the local validator and fix every issue:
   ```bash
   python examples/urban_mobility_2030.py | python scripts/deck_validator.py
   ```
   Replace the first command with your own generator. `save_deck.py` also runs
   validation automatically before auth or network calls.
8. **Save.**
   ```bash
   python scripts/save_deck.py "Title" < deck.json
   ```
   Or pipe generator output directly:
   ```bash
   python examples/urban_mobility_2030.py | python scripts/save_deck.py "Agent Skills & Skills Marketplace"
   ```
   Prints JSON to stdout: `{"deck_id":"...","deck_url":"..."}`. Human-readable
   status lines go to stderr. Parse stdout for the deck ID.
9. **Preview and evaluate.** After saving, use `scripts/preview_deck.py` to
   capture screenshots of the rendered slides. Review each slide image; fix
   layout, contrast, or content issues before delivering to the user.
   ```bash
   python scripts/preview_deck.py "<deck-id>"
   ```
   The script prints per-slide render URLs. If browser tools are available,
   navigate to each render URL and screenshot after the `renderReady` signal.
10. **Return the URL.** Always surface the edit URL printed by the script:
    `[Open deck](https://deck.4hum.ai/app/decks/<id>/edit)`.
11. **Iterate.** If the preview reveals issues or the user requests changes,
    fix the JSON and call `scripts/update_deck.py`, then re-preview:
    ```bash
    python scripts/update_deck.py "<deck-id>" < deck.json
    python scripts/preview_deck.py "<deck-id>"
    ```

## Slide Density Rules

**Object count: aim for 5–12 objects per slide. Never exceed 14.**

Too many objects = visual clutter and slow rendering. The two most common
violations and their fixes:

| Anti-pattern | Fix |
|---|---|
| 7 feature boxes (shape + title + caption each) = 21 objects | Use `bullet_list()` (1 object) OR `grid()` with max 4 items (12 objects) |
| Repeating card() for every bullet point | Use a single `text()` / `bullet_list()` object with `\n`-separated lines |

**Per-slide image rule:** Include at least one `image()` object in every
third slide (so slides 0, 2–3, 5–6 in a 7-slide deck have images). Don't
reserve images only for the cover and closing slides.

**Max features per slide:** Show at most **4 feature cards** per slide. If
you have more items, either use `bullet_list()` or split into two slides.

## Text Length and Whitespace Rules

**Bullet list character limits** (prevent mid-word wrapping inside `bullet_list()`):

| Panel width | Max chars per bullet |
|---|---|
| Half panel (w ≤ 900 px) | 55 characters |
| Two-thirds panel (w ≤ 1200 px) | 75 characters |
| Full width (w > 1400 px) | 100 characters |

Count from the start of the text, NOT including the bullet prefix. If a
bullet would exceed the limit, split the sentence or use shorter phrasing.
Wrapping mid-sentence (`• Long bullet that breaks\n  mid-phrase`) looks worse
than a tighter, punchier bullet.

**Fill the vertical canvas.** The slide canvas is 1080 px tall with an 80 px
safe margin on each side (content zone: y=80 to y=1000). Don't cluster all
objects in the top 600 px and leave the bottom 400 px empty. Options:
- Add a `caption` text at `y=920–960` with a source citation or key insight.
- Extend the chart or table height to fill the space.
- Use the bottom zone for a divider line + secondary stat.

**Source citations must anchor the very bottom.** Place source/footnote
text at `y=940, height=40` (not y=700–730). A source at y=720 still leaves
280 px of dead white space below it — the same problem the rule is meant to
fix. If your main content ends before y=700, add a second fill element
(divider + secondary stat, `key insight` body text, or a sub-caption) in
the y=700–860 zone, then anchor the source at y=940.

**On split-panel slides (image left + text right):** the source citation
`x` must be inside the text panel, not inside the image panel. If the image
occupies x=0–700 and text occupies x=720–1840, set the source at
`x=720, y=940`. A source at x=80 inside an image panel will render behind
or over the image.

## Text on Background Images

When slide text sits directly on top of a full-bleed background image (cover,
closing hero), the theme's `foreground` token may be the wrong color:

- **Light theme + dark image** → `foreground` is dark navy, invisible on a
  dark photo. Text appears to vanish.
- **Dark theme + bright image** → `foreground` is white, washed out on a
  bright photo.

**Rule:** For any text that overlaps a background image, do one of:

1. **Add a semi-transparent scrim shape first.** Place a `shape()` object
   before the text objects with `fillOpacity: 0.55` (dark scrim for light
   text, light scrim for dark text). Size it to cover the text region only.
2. **Use explicit white or black text.** In `rich_text()` runs, set
   `color: "#ffffff"` (over dark images) or `color: "#1a1a1a"` (over light
   images) instead of relying on a theme token.
3. **Use `primaryForeground` token.** Both dark and light presets define
   `primaryForeground` as a light/white color (it's the text that appears on
   the primary button). It's safer than `foreground` for hero overlays.

Apply this to cover slides and any closing/section slide that uses a hero
image as its background.

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

## Embed Caution

`embed` objects that use YouTube/Vimeo URLs often render as **"Error 153"** in the slide renderer — YouTube enforces CSP/referrer restrictions that block embedding in many contexts (sandboxed iframes, localhost dev, headless browsers). **Do not use `embed` for YouTube/Vimeo by default.**

Preferred alternatives (always work):
- `qr` code pointing to the video URL — audience scans with their phone.
- `video` object with a direct `.mp4` or `.webm` file URL (e.g. from Cloudflare Stream, S3, or GCS).
- `frame` object (`frameKind: "browser"`) showing a static thumbnail screenshot + play-button shape overlay.

Reserve `embed` for contexts where the target content explicitly supports iframe embedding (e.g. internal Grafana dashboards, Figma prototypes, Google Slides set to "Publish to web").

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

## Token-Efficient Edit Pattern

Prefer targeted scripts over full-deck regeneration — the agent only reads and
writes the affected slice, saving both input and output tokens:

```bash
# 1. Read only what you need (cost guide: outline ≈ 200 tokens, slide ≈ 800 tokens, full deck ≈ 3000–8000 tokens):
python scripts/get_deck.py "<deck-id>" --outline        # compact section/slide index
python scripts/get_deck.py "<deck-id>" --slide 7        # one slide's full JSON
python scripts/get_deck.py "<deck-id>" --theme          # theme object only

# 2. Write only what changed:
# Replace one slide's objects (stdin = JSON array):
echo '[...]' | python scripts/patch_slide.py "<deck-id>" 7

# Deep-merge a partial JSON fragment (stdin = only the changed keys):
echo '{"deck":{"theme":{"colors":{"accent":"#f97316"}}}}' | python scripts/merge_deck.py "<deck-id>"
echo '{"deck":{"title":"New Title"}}' | python scripts/merge_deck.py "<deck-id>"

# Quality validate with optional strict checks:
python my_generator.py | python scripts/deck_validator.py --strict

# Theme contrast check (WCAG AA/AAA):
python scripts/preview_deck.py "<deck-id>" --theme-check
```

## Common Commands

```bash
python scripts/auth.py
python scripts/preview_deck.py "<deck-id>"               # inspect a saved deck
python my_generator.py | python scripts/preview_deck.py  # inspect before saving
python scripts/update_deck.py "<deck-id>" < deck.json
python scripts/generate_image.py "A futuristic server room, blue accent lighting" --size 1920x1080
```
