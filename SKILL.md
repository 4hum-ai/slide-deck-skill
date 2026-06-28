---
name: deck-4hum-ai
description: >
  Create, edit, and publish professional slide decks on deck-4hum-ai.
  Claude generates the deckJson structure directly from the slide-scene-graph
  v0.4.0 schema, then saves it via the API. Use this skill when the user asks to
  make a presentation, slide deck, or slideshow — or to iteratively improve one.
license: MIT
compatibility: Python 3.8+
metadata:
  platform: deck-4hum-ai
  api: https://open-academy-api-mz4xquo5lq-as.a.run.app
  app: https://deck.4hum.ai
  when_to_use: >
    Use when the user wants to create, update, generate, or iteratively improve
    a slide deck. Also use when asked to list existing decks or open a deck.
  argument-hint: "<topic or title for the deck>"
---

# deck-4hum-ai Skill

You (Claude) are the slide-content generator. **You write the `deckJson`
directly** using the slide-scene-graph v0.4.0 schema below — you do not call a
backend LLM for content. The Python scripts only save/update/list decks via the
REST API.

## Workflow

1. **Pick a theme.** Read the content topic and tone, then select the most
   suitable preset from **Theme Presets** below. Briefly tell the user which
   theme you chose and why (one sentence). Customise palette/fonts if needed.
   **All object colors must use theme tokens** (see **Color & Font Tokens**
   below) — never hardcode hex on objects. Hex lives only in `theme.colors`.
2. **Web search for facts** *(when the topic involves factual claims, statistics,
   or current events)*. Search before writing content. Collect source URLs and
   cite them in `speakerNotes` on slides that use those facts. Skip for
   purely creative, fictional, or template decks.
3. **Plan** the deck structure (sections, slides, key messages per slide). Note which slides need images and write a one-line visual prompt for each.
4. **Generate images** *(when slides need custom visuals)*. Call `generate_image` once per image before writing the deckJson — collect the returned `file_url` values. Use the deck topic and theme to write prompts that match the visual style (e.g. dark-tech theme → "dramatic dark background, blue neon accent, photorealistic"). Only skip this if the user asked for a text-only deck or quick draft.
5. **Generate** the full `deckJson` using the chosen theme and the schema below.
   Place objects with pixel-precise x/y/width/height on the 1920×1080 canvas.
   Keep backgrounds and accents consistent with the theme palette throughout.
   Use the `file_url` values from step 4 as image `src` fields.
   Additionally, based on context:
   - `notes` *(narration script)* — include when the user mentions presenting,
     video, audio, voiceover, or TTS; or when the deck is educational/training
     content that benefits from a spoken guide (see **Narration Script** below)
   - `speakerNotes` — include when facts were sourced via web search, or when
     the deck will be presented live and talking-point reminders help
   - `animations` — include when the deck is meant to be presented live or as
     a video; skip for reference/document-style decks (see **Animations** below)
   - `transitions` — include alongside animations; a simple `fade` is fine
6. **Save** the deck:
   ```bash
   python $CLAUDE_SKILL_DIR/scripts/save_deck.py "Title" '<deckJson>'
   ```
7. **Show the URL to the user.** The script prints a line like:
   ```
   Deck saved: https://deck.4hum.ai/app/decks/<id>/edit
   ```
   **Always surface this URL in your reply** so the user can open and review the
   deck immediately. Format it as a clickable Markdown link:
   `[Open deck](https://deck.4hum.ai/app/decks/<id>/edit)`
8. **Evaluate** the result. If iterating, fetch the deck, refine the JSON, and
   call `update_deck.py` with the improved JSON. Each update also prints a URL —
   show it again after every update.
9. To automate the generate → evaluate → improve loop:
   ```bash
   python $CLAUDE_SKILL_DIR/scripts/improve_loop.py "$ARGUMENTS" --threshold 8
   ```

---

## Theme Presets

Choose the preset that best matches the content's tone and audience.
Copy the `theme` block directly into `deck.theme`.

**Every preset below includes `textStyles`** — this is the typography scale the
renderer resolves when a text object sets `"role": "title"` etc. Always copy the
full block including `textStyles`; omitting it means all text renders at the same
default size with no hierarchy.

**Set `role` on every text object** to wire it to the theme scale:
```json
{ "id": "<uuid>", "type": "text", "role": "title", "x": 80, "y": 300, "width": 1760, "height": 200, "content": "Slide Title", "textAlign": "center" }
```
Roles: `title` · `subtitle` · `heading` · `body` · `caption` · `code`

The `textStyles` block uses token refs for color so the full typography scale
re-themes automatically when the user switches themes.

### How to pick

| Tone / Topic | Preset |
|---|---|
| Tech, AI/ML, dev tools, data science | **Dark Tech** |
| Business, finance, corporate, reports | **Light Corporate** |
| Creative, marketing, education, lifestyle | **Warm Creative** |
| Minimalist, design portfolio, keynote | **Midnight Minimal** |
| Sustainability, health, nature, wellness | **Forest Green** |
| Gaming, entertainment, innovation, bold | **Neon Purple** |

---

### Dark Tech
```json
{
  "id": "<uuid>",
  "name": "Dark Tech",
  "fonts": { "display": "Inter", "heading": "Inter", "body": "Inter", "mono": "JetBrains Mono" },
  "colors": {
    "background": "#0f172a",
    "surface": "#1e293b",
    "foreground": "#f8fafc",
    "mutedForeground": "#94a3b8",
    "primary": "#6366f1",
    "primaryForeground": "#ffffff",
    "accent": "#f59e0b",
    "accentForeground": "#000000",
    "border": "#334155"
  },
  "textStyles": {
    "title":    { "fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body",    "fontSize": 36, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "heading":  { "fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": { "token": "foreground" } },
    "body":     { "fontFamily": "body",    "fontSize": 28, "fontWeight": 400, "color": { "token": "foreground" } },
    "caption":  { "fontFamily": "body",    "fontSize": 20, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "code":     { "fontFamily": "mono",    "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```
Slide backgrounds: `{"kind":"solid","color":{"token":"background"}}` (base) or `{"kind":"solid","color":{"token":"surface"}}`. Title slide gradient:
`{"kind":"gradient","gradient":{"kind":"linear","angle":135,"stops":[{"color":{"token":"background"},"offset":0},{"color":{"token":"surface"},"offset":1}]}}`

---

### Light Corporate
```json
{
  "id": "<uuid>",
  "name": "Light Corporate",
  "fonts": { "heading": "Inter", "body": "Inter" },
  "colors": {
    "background": "#ffffff",
    "surface": "#f8fafc",
    "foreground": "#0f172a",
    "mutedForeground": "#64748b",
    "primary": "#2563eb",
    "primaryForeground": "#ffffff",
    "accent": "#f59e0b",
    "accentForeground": "#000000",
    "border": "#e2e8f0",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "destructive": "#ef4444"
  },
  "textStyles": {
    "title":    { "fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body",    "fontSize": 36, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "heading":  { "fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": { "token": "foreground" } },
    "body":     { "fontFamily": "body",    "fontSize": 28, "fontWeight": 400, "color": { "token": "foreground" } },
    "caption":  { "fontFamily": "body",    "fontSize": 20, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "code":     { "fontFamily": "mono",    "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```
Slide backgrounds: `{"kind":"solid","color":{"token":"background"}}` (main) or `{"kind":"solid","color":{"token":"surface"}}`. Title slide gradient:
`{"kind":"gradient","gradient":{"kind":"linear","angle":160,"stops":[{"color":{"token":"primary"},"offset":0},{"color":{"token":"accent"},"offset":1}]}}`

---

### Warm Creative
```json
{
  "id": "<uuid>",
  "name": "Warm Creative",
  "fonts": { "heading": "Inter", "body": "Inter" },
  "colors": {
    "background": "#fef9f0",
    "surface": "#fff7ed",
    "foreground": "#1c1917",
    "mutedForeground": "#78716c",
    "primary": "#ea580c",
    "primaryForeground": "#ffffff",
    "accent": "#d97706",
    "accentForeground": "#ffffff",
    "border": "#fed7aa"
  },
  "textStyles": {
    "title":    { "fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body",    "fontSize": 36, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "heading":  { "fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": { "token": "foreground" } },
    "body":     { "fontFamily": "body",    "fontSize": 28, "fontWeight": 400, "color": { "token": "foreground" } },
    "caption":  { "fontFamily": "body",    "fontSize": 20, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "code":     { "fontFamily": "mono",    "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```
Slide backgrounds: `{"kind":"solid","color":{"token":"background"}}` (light) or `{"kind":"solid","color":{"token":"surface"}}`. Title slide gradient:
`{"kind":"gradient","gradient":{"kind":"linear","angle":135,"stops":[{"color":{"token":"primary"},"offset":0},{"color":{"token":"accent"},"offset":1}]}}`

---

### Midnight Minimal
```json
{
  "id": "<uuid>",
  "name": "Midnight Minimal",
  "fonts": { "heading": "Inter", "body": "Inter" },
  "colors": {
    "background": "#000000",
    "surface": "#111111",
    "foreground": "#ffffff",
    "mutedForeground": "#737373",
    "primary": "#ffffff",
    "primaryForeground": "#000000",
    "accent": "#22d3ee",
    "accentForeground": "#000000",
    "border": "#262626"
  },
  "textStyles": {
    "title":    { "fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body",    "fontSize": 36, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "heading":  { "fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": { "token": "foreground" } },
    "body":     { "fontFamily": "body",    "fontSize": 28, "fontWeight": 400, "color": { "token": "foreground" } },
    "caption":  { "fontFamily": "body",    "fontSize": 20, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "code":     { "fontFamily": "mono",    "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```
Slide backgrounds: `{"kind":"solid","color":{"token":"background"}}` (base) or `{"kind":"solid","color":{"token":"surface"}}`. Use `{"token":"foreground"}` text, `{"token":"border"}` dividers. Accent (`{"token":"accent"}`) sparingly — one highlight per slide max.

---

### Forest Green
```json
{
  "id": "<uuid>",
  "name": "Forest Green",
  "fonts": { "heading": "Inter", "body": "Inter" },
  "colors": {
    "background": "#0d1f1a",
    "surface": "#132b24",
    "foreground": "#ecfdf5",
    "mutedForeground": "#6ee7b7",
    "primary": "#10b981",
    "primaryForeground": "#ffffff",
    "accent": "#fbbf24",
    "accentForeground": "#000000",
    "border": "#1f4538",
    "success": "#34d399"
  },
  "textStyles": {
    "title":    { "fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body",    "fontSize": 36, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "heading":  { "fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": { "token": "foreground" } },
    "body":     { "fontFamily": "body",    "fontSize": 28, "fontWeight": 400, "color": { "token": "foreground" } },
    "caption":  { "fontFamily": "body",    "fontSize": 20, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "code":     { "fontFamily": "mono",    "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```
Slide backgrounds: `{"kind":"solid","color":{"token":"background"}}` (base) or `{"kind":"solid","color":{"token":"surface"}}`. Title slide gradient:
`{"kind":"gradient","gradient":{"kind":"linear","angle":135,"stops":[{"color":{"token":"background"},"offset":0},{"color":{"token":"surface"},"offset":1}]}}`

---

### Neon Purple
```json
{
  "id": "<uuid>",
  "name": "Neon Purple",
  "fonts": { "heading": "Inter", "body": "Inter" },
  "colors": {
    "background": "#0f0a1e",
    "surface": "#1a1030",
    "foreground": "#f5f3ff",
    "mutedForeground": "#a78bfa",
    "primary": "#8b5cf6",
    "primaryForeground": "#ffffff",
    "accent": "#ec4899",
    "accentForeground": "#ffffff",
    "border": "#2d1b69"
  },
  "textStyles": {
    "title":    { "fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body",    "fontSize": 36, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "heading":  { "fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": { "token": "foreground" } },
    "body":     { "fontFamily": "body",    "fontSize": 28, "fontWeight": 400, "color": { "token": "foreground" } },
    "caption":  { "fontFamily": "body",    "fontSize": 20, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "code":     { "fontFamily": "mono",    "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```
Slide backgrounds: `{"kind":"solid","color":{"token":"background"}}` (base) or `{"kind":"solid","color":{"token":"surface"}}`. Title slide gradient:
`{"kind":"gradient","gradient":{"kind":"linear","angle":135,"stops":[{"color":{"token":"background"},"offset":0},{"color":{"token":"surface"},"offset":1}]}}`

---

### Custom theme tips

- Swap `primary` to any brand color; adjust `primaryForeground` for contrast.
- For a two-color accent scheme, use `primary` for CTAs/titles and `accent` for highlights.
- `surface` should be 1–2 steps lighter (or darker) than `background` — it's used for cards and alt slides.
- `mutedForeground` should pass 3:1 contrast ratio against `background` for readable body captions.

## First-time setup (automatic)

No environment variables needed. On first use, the script will print a URL:

```
deck-4hum-ai: authorization required.

  Open this URL in your browser:
  https://deck.4hum.ai/auth/device?code=WXYZ-2345

  Confirmation code: WXYZ-2345

  Waiting for authorization...
```

Open the URL, confirm the code matches, click **Authorize**. The CLI receives
a long-lived API key (`sk-oa-…`) saved to `~/.open-academy/config.json` and
all future commands run without prompting.

To log out: `python $CLAUDE_SKILL_DIR/scripts/auth.py logout`

## Commands

### Save a deck you've generated

```bash
python $CLAUDE_SKILL_DIR/scripts/save_deck.py "My Title" '<deckJson>'
# or pipe from stdin:
echo '<deckJson>' | python $CLAUDE_SKILL_DIR/scripts/save_deck.py "My Title"
```

Prints JSON: `{ "deck_id": "...", "deck_url": "..." }`

### Update an existing deck

```bash
python $CLAUDE_SKILL_DIR/scripts/update_deck.py "<deck_id>" '<deckJson>'
```

### Create a blank deck

```bash
python $CLAUDE_SKILL_DIR/scripts/create_deck.py "My Title"
```

### List your decks

```bash
python $CLAUDE_SKILL_DIR/scripts/list_decks.py
```

### Export a deck as an MP4 video

```bash
python $CLAUDE_SKILL_DIR/scripts/export_video.py "<deck_id>" [--out ./my-deck.mp4]
```

Options:
- `--resolution 1080p|720p` — output resolution (default: 1080p)
- `--fps 24|30` — frame rate (default: 30)
- `--no-animate` — disable per-object animations (static transitions only)
- `--captions vtt|srt` — also download a captions sidecar file
- `--timeout N` — max seconds to wait for encoding (default: 300)
- `--headed` — show the browser window (useful for debugging)

Requires Playwright + Chromium (one-time setup):
```bash
pip install playwright
playwright install chromium
```

The export is fully client-side — the browser encodes H.264 + AAC via WebCodecs
(with a ffmpeg.wasm fallback) and downloads the blob directly. No API upload.

**UAT bypass**: if `UAT_BYPASS_TOKEN` is set in the environment, the script skips
Firebase login — same token used by `uat-agent.mjs`.

```bash
# Example — export the RTX 5060 deck as 1080p 30fps MP4:
UAT_BYPASS_TOKEN=<token> python $CLAUDE_SKILL_DIR/scripts/export_video.py \
  a80e23e5-b48c-415c-b078-39463c50143c --out rtx5060.mp4
```

Prints the saved file path on success.

### Improve a deck iteratively (autonomous loop)

```bash
python $CLAUDE_SKILL_DIR/scripts/improve_loop.py "$ARGUMENTS" --threshold 8
```

Options:
- `--criteria "<text>"` — quality criteria (default: professional quality, clear messaging, good layout)
- `--max-iterations N` — cap on cycles (default: 5)
- `--threshold N` — stop when score reaches N out of 10 (default: 7)
- `--model <id>` — Claude model for generation+evaluation (default: claude-sonnet-4-6)

## Usage examples

- "Create a deck about machine learning fundamentals" → generate deckJson → `save_deck.py`
- "Make a blank deck called Q3 Roadmap" → `create_deck.py "Q3 Roadmap"`
- "List my decks" → `list_decks.py`
- "Generate the best possible deck about neural networks, score ≥ 8/10" → `improve_loop.py "neural networks" --threshold 8`

---

## Color & Font Tokens

**This is the #1 quality rule.** Every color on every object must be a **theme
token reference** — not a hardcoded hex string. Token refs let the user switch
themes and have the whole deck re-color instantly. Hardcoded hex freezes objects
out of theme switching permanently.

### Token syntax

```json
{ "token": "primary" }
```

Use this anywhere a color value is accepted: `fill`, `stroke`, `color` in text
style, background `color`, gradient stop `color`.

### Valid token names

| Token | Typical use |
|---|---|
| `background` | Slide/canvas background |
| `surface` | Cards, panels, alt-slide bg |
| `foreground` | Primary text, icons |
| `mutedForeground` | Captions, secondary text |
| `primary` | CTA shapes, key headings, progress fills |
| `primaryForeground` | Text on `primary`-filled shapes |
| `accent` | Highlight shapes, badges, one per slide |
| `accentForeground` | Text on `accent`-filled shapes |
| `border` | Dividers, strokes, subtle outlines |
| `success` | Positive indicators |
| `warning` | Caution indicators |
| `destructive` | Error/negative indicators |

Aliases also accepted: `text` (= `foreground`), `mutedText` (= `mutedForeground`), `line` (= `border`), `danger` (= `destructive`).

Custom tokens: `custom.<name>` (e.g. `custom.brand`) when defined in `theme.colors.custom`.

### Font family tokens

- **Omit `fontFamily`** on text runs → inherits the `body` font from the theme.
- Set `"fontFamily": "heading"` for titles and section headers.
- **Never** put a literal font name (e.g. `"Inter"`) on a text run — literal
  names belong only in `theme.fonts`.

### Quick-reference mapping

| Object property | Use this token |
|---|---|
| Slide background (main) | `{"kind":"solid","color":{"token":"background"}}` |
| Slide background (alt/card) | `{"kind":"solid","color":{"token":"surface"}}` |
| Title text | `{"token":"foreground"}` + `"fontFamily":"heading"` |
| Body / bullet text | `{"token":"foreground"}` (omit fontFamily) |
| Caption / label | `{"token":"mutedForeground"}` |
| Primary shape fill | `{"token":"primary"}` |
| Text on primary shape | `{"token":"primaryForeground"}` |
| Accent shape fill | `{"token":"accent"}` |
| Text on accent shape | `{"token":"accentForeground"}` |
| Card / panel shape fill | `{"token":"surface"}` |
| Divider / border stroke | `{"token":"border"}` |
| Gradient title bg | stops: `{"token":"background"}` → `{"token":"surface"}` |
| Primary gradient bg | stops: `{"token":"primary"}` → `{"token":"accent"}` |
| Table header fill | `{"token":"primary"}` |
| Table header text | `{"token":"primaryForeground"}` |
| Table body fill | `{"token":"surface"}` |
| Table body text | `{"token":"foreground"}` ← **required or text is invisible on dark themes** |
| Table border | `{"token":"border"}` |

**Exception:** Raw hex is allowed only for deliberate one-offs that must NOT
follow the theme (e.g. a brand color extracted from a user's logo).

---

## Slide Scene-Graph v0.4.0 Schema Reference

Use this schema to generate the `deckJson` object. All coordinates are in
pixels on a **1920×1080** canvas (16:9). Pass the complete envelope.

### Envelope

```json
{
  "schema": "open-academy.slide-scene-graph",
  "schemaVersion": "0.4.0",
  "deck": { ... }
}
```

### Deck (required fields)

```json
{
  "id": "<uuid-v4>",
  "title": "Deck Title",
  "width": 1920,
  "height": 1080,
  "theme": { ... },
  "sections": [ ... ]
}
```

### Theme

```json
{
  "id": "<uuid-v4>",
  "name": "My Theme",
  "fonts": {
    "display": "Inter",
    "heading": "Inter",
    "body": "Inter",
    "mono": "JetBrains Mono"
  },
  "colors": {
    "background": "#ffffff",
    "surface": "#f8fafc",
    "foreground": "#0f172a",
    "mutedForeground": "#64748b",
    "primary": "#6366f1",
    "primaryForeground": "#ffffff",
    "accent": "#f59e0b",
    "accentForeground": "#ffffff",
    "border": "#e2e8f0"
  }
}
```

Color fields in `colors`: `background`, `surface`, `foreground`, `mutedForeground`,
`primary`, `primaryForeground`, `accent`, `accentForeground`, `border`, `success`,
`warning`, `destructive`. All optional hex strings.

Font slots in `fonts`: `display`, `heading`, `body`, `mono`. All optional strings.

### Section

```json
{
  "id": "<uuid-v4>",
  "title": "Section Name",
  "slides": [ ... ]
}
```

### Slide

```json
{
  "id": "<uuid-v4>",
  "background": { "kind": "solid", "color": { "token": "background" } },
  "objects": [ ... ]
}
```

Background kinds:
- `{ "kind": "none" }`
- `{ "kind": "solid", "color": { "token": "background" } }`
- `{ "kind": "gradient", "gradient": { "kind": "linear", "angle": 135, "stops": [{"color":{"token":"background"},"offset":0}, {"color":{"token":"surface"},"offset":1}] } }`
- `{ "kind": "image", "src": "https://...", "fit": "cover", "opacity": 0.5 }`

Use `{"token":"surface"}` for alternate/panel slides, `{"token":"primary"}` or
`{"token":"accent"}` for bold accent slides. Raw hex only for image overlays.

### Object Types (14 variants)

All objects share: `id` (uuid), `x`, `y`, `width`, `height` (pixels), `type`.

#### text
```json
{
  "id": "<uuid>", "type": "text",
  "role": "title",
  "x": 80, "y": 120, "width": 1760, "height": 200,
  "content": [
    {
      "kind": "block",
      "runs": [{ "kind": "span", "text": "Hello World" }]
    }
  ],
  "textAlign": "center",
  "verticalAlign": "middle"
}
```
**`role`** ∈ `"title" | "subtitle" | "heading" | "body" | "caption" | "code"` — **always set this**. The renderer resolves `theme.textStyles[role]` to apply the correct font, size, weight, and color token. Without `role`, the object falls back to an unstyled default ("theme default").

`content` may also be a plain string: `"content": "Hello World"` (top-level style fields apply).

When `role` is set you do **not** need to repeat font/size/color in the run `style` — the `textStyles` preset covers them. Only add run-level `style` fields to override a specific word (e.g. bold emphasis, inline code color).

`TextBlockSchema.kind` **must** be `"block"`.
`TextRunSchema.kind` **must** be `"span"` (or `"softBreak"` for a line break).
`style.fontWeight` is a number (100–900): use `700` for bold, **not** `"bold": true`.
`style.color` **must** be a token ref: `{"token":"foreground"}` for body text, `{"token":"mutedForeground"}` for captions, `{"token":"primaryForeground"}` for text on a primary-filled shape.
`style.fontFamily`: use `"heading"` for titles/headers, omit for body text. **Never** a literal font name like `"Inter"`.
`style` fields: `fontFamily`, `fontSize`, `fontWeight`, `fontStyle`, `letterSpacing`, `lineHeight`, `color`, `textAlign`, `textDecoration`.
`textAlign` ∈ `left | center | right | justify`
`verticalAlign` ∈ `top | middle | bottom`
`fontStyle` ∈ `normal | italic`
`textDecoration` ∈ `none | underline | line-through`
`autoFit` ∈ `none | shrink | resize`

#### shape
```json
{
  "id": "<uuid>", "type": "shape",
  "x": 100, "y": 100, "width": 400, "height": 200,
  "shape": "roundedRectangle",
  "fill": { "token": "primary" },
  "stroke": { "token": "border" },
  "strokeWidth": 2,
  "cornerRadius": 16
}
```
`fill` and `stroke` accept either a token ref `{"token":"primary"}` **or** a plain hex string for brand-specific one-offs.
`strokeWidth` is a separate top-level number field.
Common fill tokens: `primary` (CTA), `accent` (highlight), `surface` (card/panel), `background` (ghost).
Common stroke tokens: `border` (default), `primary`, `accent`.
`shape` ∈ `rectangle | roundedRectangle | ellipse | triangle | rightTriangle | diamond | parallelogram | trapezoid | pentagon | hexagon | star | arrow | callout | customPath`

#### image
```json
{
  "id": "<uuid>", "type": "image",
  "x": 960, "y": 100, "width": 880, "height": 880,
  "src": "https://picsum.photos/seed/technology/1920/1080",
  "fit": "cover",
  "opacity": 1.0
}
```
`fit` ∈ `cover | contain | fill`
`opacity` 0–1 (default 1). Use `0.15`–`0.4` for background overlays.

**Always include images** on title slides, section covers, and content slides where a photo adds meaning. Do not skip images because a URL is needed — generate one or use a seed URL.

**Sourcing image URLs — three options, in order of preference:**

**Option A — AI-generated image (best quality, custom to topic):**
Call `generate_image` before building the deckJson:
```
generate_image({
  prompt: "A futuristic server room, blue neon lighting, dramatic angle, photorealistic, 4K",
  size: "1920x1080",
  style: "photorealistic"
})
```
The tool returns `{ media_id, file_url }`. Use `file_url` as the image `src`. Generate all images first, collect the URLs, then assemble the deckJson in one pass.

Write prompts that specify: **subject + style + mood + lighting + color palette**. Match the palette to the deck's theme tokens (e.g. dark-tech deck → "dramatic dark background, blue accent lighting").

**Option B — picsum.photos (instant, no credits, good for placeholders):**
```
https://picsum.photos/seed/{keyword}/1920/1080
```
Replace `{keyword}` with a descriptive word (`technology`, `teamwork`, `nature`, `city`, etc.). Deterministic — same keyword always returns the same image.

Use this when the deck does not need custom visuals or when you want a quick first draft before generating real images.

**Option C — Unsplash (stock photos, requires web search for a live ID):**
```
https://images.unsplash.com/photo-{photo-id}?w=1920&q=80
```
Unsplash photo IDs go stale — **do not hardcode IDs**. Use `web_search` with `site:unsplash.com {topic} photo` and extract a photo ID from a live result URL retrieved in the current session.

**Layout patterns with images:**
- **Half-split**: image right `x=960,w=960,h=1080` + text left `x=80,w=840`
- **Full bleed hero**: image `x=0,y=0,w=1920,h=1080,fit=cover` + dark overlay shape `fill={"token":"background"},opacity=0.6` + text on top
- **Card thumbnail**: image `w=400,h=300,fit=cover` with rounded shape beneath for caption

#### chart
```json
{
  "id": "<uuid>", "type": "chart",
  "x": 200, "y": 200, "width": 1200, "height": 600,
  "chart": "bar",
  "categories": ["Q1", "Q2", "Q3", "Q4"],
  "series": [
    { "name": "Revenue", "values": [120, 145, 160, 190] }
  ]
}
```
`ChartSeriesSchema` fields: `name` (string), `values` (number array), `color` (optional — use a token ref `{"token":"primary"}` / `{"token":"accent"}` or omit to let the theme auto-color each series). The field is `values`, **not** `data`.
`chart` ∈ `bar | line | area | pie | doughnut | rose | scatter | radar | funnel | gauge | heatmap`

#### table
```json
{
  "id": "<uuid>", "type": "table",
  "x": 160, "y": 200, "width": 1600, "height": 600,
  "rows": 3, "cols": 3,
  "headerRow": true,
  "styling": {
    "headerFill": { "token": "primary" },
    "headerText": { "color": { "token": "primaryForeground" }, "fontWeight": 700 },
    "bodyFill": { "token": "surface" },
    "bodyText": { "color": { "token": "foreground" } },
    "borderColor": { "token": "border" },
    "borderWidth": 1,
    "cellPadding": "m"
  },
  "cells": [
    [{"text": "Header 1"}, {"text": "Header 2"}, {"text": "Header 3"}],
    [{"text": "Row 1 A"}, {"text": "Row 1 B"}, {"text": "Row 1 C"}],
    [{"text": "Row 2 A"}, {"text": "Row 2 B"}, {"text": "Row 2 C"}]
  ]
}
```
**Always include `styling`** — without `bodyText.color` and `headerText.color`, cell text has no color token and will be invisible on dark themes.

`styling` fields (all optional, all colors accept token refs):
- `headerFill` / `bodyFill` — row background colors
- `headerText` / `bodyText` — default `TextStylePreset` for header/body cells (set `color` here)
- `borderColor` / `borderWidth` — table grid lines
- `cellPadding` ∈ `s | m | l`
- `stripedRows` / `stripedColumns` — alternating row/column shading
- `accentFill` — accent color for striped rows/columns
- `totalRow` / `firstColumn` / `lastColumn` — special styling for summary rows/columns, each has `*Fill` and `*Text` variants

`cells` is a **2D array**: outer array = rows, inner array = cells per row. Outer length **must** equal `rows`; inner length **must** equal `cols`.
Each cell: `{ "text": "..." }` using the `text` field — **not** `content`. No `row`/`col`/`isHeader` fields.
`headerRow: true` marks the first row as using `styling.headerText` / `styling.headerFill`.
`rowSpan`/`colSpan` are per-cell optional ints. **Even with colSpan, every row must still have exactly `cols` cell objects** — pad spanned-over positions with `{"text": ""}`.
Per-cell overrides: `textStyle` (overrides `bodyText`/`headerText`) and `fill` (overrides `bodyFill`/`headerFill`) — both accept token refs.

#### diagram (Mermaid)
```json
{
  "id": "<uuid>", "type": "diagram",
  "x": 200, "y": 200, "width": 1520, "height": 680,
  "engine": "mermaid",
  "source": "graph TD\n  A[Start] --> B{Decision}\n  B --> C[End]"
}
```
`engine` ∈ `mermaid | drawio | vueflow`

#### embed
```json
{
  "id": "<uuid>", "type": "embed",
  "x": 200, "y": 200, "width": 1520, "height": 680,
  "url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
  "embedKind": "youtube"
}
```
`embedKind` ∈ `youtube | vimeo | iframe`

#### qr
```json
{
  "id": "<uuid>", "type": "qr",
  "x": 760, "y": 340, "width": 400, "height": 400,
  "mode": "url", "value": "https://deck.4hum.ai"
}
```
`value` holds the URL string for `mode: "url"`. For `mode: "vcard"`, use the `contact` object instead:
`contact: { name, title, company, phone, email, url }` (all optional strings).
`foreground` / `background` override QR code colors (hex strings).
`errorCorrection` ∈ `L | M | Q | H`.

#### line
```json
{
  "id": "<uuid>", "type": "line",
  "x": 80, "y": 540, "width": 1760, "height": 2,
  "line": "straight",
  "start": { "x": 0, "y": 0 },
  "end": { "x": 1760, "y": 0 },
  "stroke": { "token": "border" },
  "strokeWidth": 2
}
```
`stroke` accepts a token ref or plain hex. Use `{"token":"border"}` for dividers, `{"token":"primary"}` for accent lines. `strokeWidth` is a separate number field.
`line` ∈ `straight | arrow | doubleArrow | curve | connector`

#### frame
```json
{
  "id": "<uuid>", "type": "frame",
  "x": 300, "y": 200, "width": 1320, "height": 680,
  "frameKind": "browser",
  "src": "https://deck.4hum.ai"
}
```
`frameKind` ∈ `laptop | desktop | phone | tablet | browser | pictureClassic | polaroid`

#### placeholder
```json
{
  "id": "<uuid>", "type": "placeholder",
  "x": 80, "y": 120, "width": 1760, "height": 200,
  "role": "title"
}
```
`role` ∈ `title | subtitle | body | image | chart | table | media`

### Layout tips for 1920×1080

- **Title slide**: title text `y=360, height=200`, subtitle `y=580, height=100` — centered
- **Content slide**: title bar `y=60, height=120`, body content `y=220, height=760`
- **Two-column**: left column `x=80, width=840`, right column `x=1000, width=840`
- **Safe margins**: 80px on all sides
- **Large title font**: 72–96px; body text: 32–40px; caption: 24px

---

## Animations

Add an `animations` array to each slide to bring objects in on entrance. Each
entry targets one object by its `id`.

```json
"animations": [
  {
    "id": "<uuid>",
    "targetId": "<object-id>",
    "category": "entrance",
    "effect": "fade",
    "trigger": "onEnter",
    "durationMs": 500,
    "delayMs": 0,
    "easing": "easeOut"
  }
]
```

`category` ∈ `entrance | emphasis | exit`
`effect` ∈ `fade | fly | float | zoom | grow | spin | bounce | pulse | teeter | flash | shrink`
`trigger` ∈ `onEnter | onClick | afterPrevious | withPrevious`
`easing` ∈ `linear | ease | easeIn | easeOut | easeInOut`

### Recipes

**Title slide** — fade in title, then subtitle after:
```json
[
  {"id":"<a1>","targetId":"<title-id>","category":"entrance","effect":"fade","trigger":"onEnter","durationMs":600,"delayMs":0,"easing":"easeOut"},
  {"id":"<a2>","targetId":"<subtitle-id>","category":"entrance","effect":"float","trigger":"afterPrevious","durationMs":500,"delayMs":200,"easing":"easeOut"}
]
```

**Staggered bullet list** — each bullet flies in with 150ms gap (use `withPrevious` + increasing `delayMs`):
```json
[
  {"id":"<a1>","targetId":"<bullet1-id>","category":"entrance","effect":"fly","trigger":"onEnter","durationMs":400,"delayMs":0},
  {"id":"<a2>","targetId":"<bullet2-id>","category":"entrance","effect":"fly","trigger":"withPrevious","durationMs":400,"delayMs":150},
  {"id":"<a3>","targetId":"<bullet3-id>","category":"entrance","effect":"fly","trigger":"withPrevious","durationMs":400,"delayMs":300}
]
```

**Chart entrance** — zoom in chart after title:
```json
{"id":"<a1>","targetId":"<chart-id>","category":"entrance","effect":"zoom","trigger":"afterPrevious","durationMs":700,"delayMs":100,"easing":"easeOut"}
```

**Shape pulse** (emphasis after entrance):
```json
{"id":"<a1>","targetId":"<shape-id>","category":"emphasis","effect":"pulse","trigger":"afterPrevious","durationMs":600}
```

### Slide transitions

Add a `transitions` object to each slide for the slide-in effect:
```json
"transitions": { "effect": "fade", "durationMs": 400 }
```
`effect` ∈ `none | fade | slide | push | wipe | zoom | flip | blur`
`direction` ∈ `left | right | up | down` (for `slide`, `push`, `wipe`)

Recommended defaults: `fade` (400ms) for content slides, `zoom` (500ms) for section openers, `slide` for step-by-step sequences.

---

## Narration Script & Speaker Notes

Every slide has two distinct text fields for presenter/TTS use:

### `notes` — narration script (spoken aloud)

A plain string written as natural spoken language — this is what TTS or a
presenter reads aloud. Aim for **30–90 seconds** per slide (~75–225 words).
Write in first person, conversational, present tense.

```json
"notes": "Welcome to our deep dive into machine learning. On this slide you can see the three core pillars that underpin every modern ML system: data quality, model architecture, and training methodology. Let's explore why each one matters."
```

Guidelines:
- Expand abbreviations (say "machine learning" not "ML" on first mention)
- Describe what's *on screen* for accessibility: "The chart on the right shows…"
- End each slide with a bridge to the next: "In the next section, we'll look at…"
- Cite sources naturally if the slide includes a statistic: "According to McKinsey's 2024 report…"

### `speakerNotes` — presenter view (not spoken)

Structured notes visible only in presenter view. Use for references, talking
points, and questions. Accepts `TextContentSchema` (plain string or blocks).

```json
"speakerNotes": {
  "content": "Key point: emphasise the 40% productivity stat.\nSource: McKinsey Global Institute, 'The Age of AI', Jan 2024 — https://mckinsey.com/...\nQ&A prompt: 'Which pillar is hardest for your team?'"
}
```

**Citation format in `speakerNotes`:**
```
Source: <Author/Org>, '<Title>', <Month Year> — <URL>
```
Add one `Source:` line per fact used on that slide. When web search found the
URL, use the exact URL. When the source is well-known but no URL was retrieved,
use `<Title>, <Year>` without a URL rather than inventing one.

---

## Optional env overrides

| Variable | Default | Purpose |
|---|---|---|
| `OPEN_ACADEMY_TOKEN` | *(from config)* | Override the saved API key |
| `OPEN_ACADEMY_WORKSPACE_ID` | *(from config)* | Override the saved workspace ID |
| `OPEN_ACADEMY_API_URL` | `https://open-academy-api-mz4xquo5lq-as.a.run.app` | Self-hosted API |
| `OPEN_ACADEMY_APP_URL` | `https://deck.4hum.ai` | Self-hosted app |

## API reference

See `references/api-reference.md` for full endpoint documentation.
