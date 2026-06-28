# Objects Guide — All Slide Object Types

Use this guide to choose the right object type for the content on each slide.
Every object inherits `id`, `type`, `x`, `y`, `width`, `height` (required) plus
optional `opacity`, `rotation`, `z` (stacking order).

Canvas: **1920 × 1080 px**. Safe inner margins: 80 px on all sides.
Recommended zones:
- Header / chip: `y 60–160`
- Main content: `y 160–900`
- Footer caption: `y 900–1000`

---

## text

**When:** Any readable content — titles, body, bullet lists, captions, code.
Use the `latex` field to render a math equation.

```json
{
  "id": "<uuid>", "type": "text",
  "role": "heading",
  "x": 80, "y": 160, "width": 1760, "height": 80,
  "content": "Slide headline",
  "textAlign": "left",
  "verticalAlign": "top",
  "autoFit": "shrink"
}
```

**Roles:** `title` (72 px), `subtitle` (36 px), `heading` (48 px), `body` (28 px),
`caption` (20 px), `code` (22 px, mono).

**Rich text (mixed styles):**
```json
"content": [
  { "kind": "block", "runs": [
    { "kind": "span", "text": "Key term", "style": { "fontWeight": 700, "color": { "token": "accent" } } },
    { "kind": "span", "text": " — supporting detail" }
  ]}
]
```

**LaTeX equation** (rendered by KaTeX):
```json
{
  "id": "<uuid>", "type": "text",
  "role": "body",
  "x": 240, "y": 400, "width": 1440, "height": 200,
  "content": "E = mc^2",
  "latex": "E = mc^2"
}
```
Set both `content` (plain-text fallback for export) and `latex` (rendered formula).

**Tips:**
- Use `autoFit: "shrink"` on all text boxes — it prevents clipping when content is long.
- Keep title text under 60 characters; body bullets under 90 characters per line.
- Use `role: "code"` + the `mono` font slot for code snippets. Wrap in a dark shape for contrast.

---

## shape

**When:** Background panels, card backs, dividers, decorative accent elements,
semi-transparent overlays on images.

```json
{
  "id": "<uuid>", "type": "shape",
  "x": 80, "y": 200, "width": 800, "height": 600,
  "shape": "roundedRectangle",
  "fill": { "token": "surface" },
  "stroke": { "token": "border" },
  "strokeWidth": 1,
  "cornerRadius": 24
}
```

**Shapes:** `rectangle`, `roundedRectangle`, `ellipse`, `triangle`,
`rightTriangle`, `diamond`, `parallelogram`, `trapezoid`, `pentagon`,
`hexagon`, `star`, `arrow`, `callout`, `customPath`.

**Semi-transparent image overlay** (ensures text contrast):
```json
{
  "id": "<uuid>", "type": "shape",
  "x": 0, "y": 0, "width": 1920, "height": 1080,
  "shape": "rectangle", "fill": { "token": "background" },
  "stroke": { "token": "background" }, "strokeWidth": 0,
  "opacity": 0.65
}
```

**Tips:**
- Layer order: image → semi-transparent shape overlay → text objects.
- Use `strokeWidth: 0` on full-bleed background shapes to avoid a hairline border artifact.
- `ellipse` works well as an avatar placeholder or decorative dot accent.

---

## image

**When:** Hero backgrounds, portrait photos, product screenshots, section
dividers, decorative visuals.

```json
{
  "id": "<uuid>", "type": "image",
  "x": 960, "y": 0, "width": 960, "height": 1080,
  "src": "https://...",
  "fit": "cover",
  "opacity": 1
}
```

**Fits:** `cover` (fills, crops edges), `contain` (shows all, may letterbox),
`fill` (stretches to bounds).

**Common layouts:**
- Full-bleed hero: `x=0 y=0 w=1920 h=1080 fit=cover` + dark shape overlay at 60% opacity.
- Split left/right: image at `x=960 w=960 h=1080`, content at `x=0 w=880`.
- Portrait card column: `w=300 h=370` per card at top, text below.

**Tips:**
- Always add a shape overlay when placing text on an image — contrast fails at `opacity: 1`.
- Use `generate_image.py` for AI-generated assets; `picsum.photos` for placeholder drafts only.
- Match `--size` to the display region: `1920x1080` hero, `720x900` portrait, `960x1080` half-panel.

---

## video

**When:** Product demos, recorded talks, animated explainers stored as video
files accessible via URL (mp4, webm).

```json
{
  "id": "<uuid>", "type": "video",
  "x": 200, "y": 200, "width": 1520, "height": 760,
  "src": "https://example.com/demo.mp4",
  "poster": "https://example.com/demo-poster.jpg",
  "autoplay": false,
  "loop": false,
  "muted": true,
  "controls": true
}
```

**Fields:**
| Field | Type | Default | Notes |
|---|---|---|---|
| `src` | string | — | Required. MP4 or WebM URL. |
| `poster` | string | — | Thumbnail shown before play. |
| `autoplay` | boolean | `false` | Mute must be true for autoplay to work in most browsers. |
| `loop` | boolean | `false` | |
| `muted` | boolean | `false` | Set true for background/ambient loops. |
| `controls` | boolean | `false` | Show native playback controls. |
| `shape` | string | — | `"circle"` clips to circular mask (cover fit). |

**Tips:**
- For presentation delivery: `controls: true, muted: false, autoplay: false`.
- For looping background ambience: `autoplay: true, loop: true, muted: true, controls: false`.
- Set `poster` so slides look good before the video loads.

---

## embed

**When:** Embedding YouTube or Vimeo videos by URL; embedding any external web
content via iframe (live dashboards, interactive demos, web apps).

```json
{
  "id": "<uuid>", "type": "embed",
  "x": 200, "y": 200, "width": 1520, "height": 760,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "embedKind": "youtube",
  "autoplay": false
}
```

**Fields:**
| Field | Type | Default | Notes |
|---|---|---|---|
| `url` | string | — | Required. YouTube/Vimeo share URL or arbitrary HTTPS URL. |
| `embedKind` | enum | auto-detected | `"youtube"`, `"vimeo"`, `"iframe"`. Omit to auto-detect from URL. |
| `autoplay` | boolean | `false` | YouTube/Vimeo only; obeys browser autoplay policy. |

**Tips:**
- Use `embed` for YouTube/Vimeo links. Use `video` for direct file URLs.
- `iframe` kind can embed live web pages — useful for live dashboards or Figma prototypes.
- Always size to 16:9 (`w=1520 h=855`) for YouTube/Vimeo to avoid letterboxing.

---

## chart

**When:** Data comparison, trend visualization, part-of-whole, progress
indicators, rankings, distribution.

```json
{
  "id": "<uuid>", "type": "chart",
  "x": 120, "y": 280, "width": 1680, "height": 600,
  "chart": "bar",
  "categories": ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
  "series": [
    { "name": "Revenue", "values": [1.2, 1.8, 2.1, 2.6], "color": { "token": "primary" } },
    { "name": "Target", "values": [1.5, 1.5, 2.0, 2.5], "color": { "token": "accent" } }
  ]
}
```

**Chart types and when to use:**
| Type | Use for | Notes |
|---|---|---|
| `bar` | Category comparison | Default. Vertical bars. Add multiple series for grouped bars. |
| `line` | Trends over time | Use for continuous data. Works with dates as categories. |
| `area` | Volume trends | Like line, filled under the curve. Stack multiple series. |
| `pie` | Part-of-whole (≤6 segments) | Use `doughnut` for cleaner look with center label space. |
| `doughnut` | Part-of-whole with center space | Center can hold a KPI label via text overlay. |
| `rose` | Polar category comparison | Good for cyclical data (months, compass directions). |
| `scatter` | Correlation / distribution | Each series item = one point; use `x` and `y` values. |
| `radar` | Multi-attribute comparison | 5–8 categories ideal. Good for skill/capability profiles. |
| `funnel` | Pipeline / conversion | Categories = stages top to bottom. |
| `gauge` | Single KPI vs target | One series, one value. Pair with a `kpi_card` for context. |
| `heatmap` | Matrix intensity | Categories = X axis; series rows = Y rows. |

**Tips:**
- One chart per slide — never more than two (one primary + one reference).
- Use `{ "token": "primary" }` for the main series, `{ "token": "accent" }` for highlights or targets.
- Place chart title as a `text` object above the chart (role `heading`), not inside the chart.
- Pair with a `kpi_card` (from `block_builder`) for the headline number beside the chart.

---

## table

**When:** Structured comparison, feature matrix, schedule, pricing, data lookup.

```json
{
  "id": "<uuid>", "type": "table",
  "x": 120, "y": 280, "width": 1680, "height": 560,
  "rows": 4, "cols": 3,
  "headerRow": true,
  "styling": {
    "headerFill": { "token": "primary" },
    "headerText": { "color": { "token": "primaryForeground" }, "fontWeight": 700 },
    "bodyFill": { "token": "surface" },
    "bodyText": { "color": { "token": "foreground" } },
    "borderColor": { "token": "border" },
    "borderWidth": 1,
    "cellPadding": "m",
    "stripedRows": true
  },
  "cells": [
    [{ "text": "Feature" },   { "text": "Free" },    { "text": "Pro" }],
    [{ "text": "Storage" },   { "text": "1 GB" },    { "text": "100 GB" }],
    [{ "text": "Users" },     { "text": "3" },       { "text": "Unlimited" }],
    [{ "text": "Analytics" }, { "text": "Basic" },   { "text": "Advanced" }]
  ]
}
```

**Sizing guide:**
- 3–5 rows: height 400–500 px
- 6–8 rows: height 550–700 px
- Width 1400–1680 px for 3–4 columns; 1680–1760 px for 5+ columns.
- Cell padding options: `"s"` (tight), `"m"` (normal), `"l"` (airy).

**Tips:**
- Keep tables to 3–5 columns. Split wide tables across two slides.
- Use `stripedRows: true` for readability on light-background themes.
- Add a caption text object below the table to cite the data source.

---

## diagram

**When:** Flowcharts, architecture diagrams, sequences, mind maps, ER diagrams,
entity relationships — anything that needs structured connected nodes.

**Mermaid (recommended for most diagrams):**
```json
{
  "id": "<uuid>", "type": "diagram",
  "x": 120, "y": 280, "width": 1680, "height": 600,
  "engine": "mermaid",
  "source": "flowchart LR\n  A[Input] --> B{Validate?}\n  B -->|yes| C[Process]\n  B -->|no| D[Reject]\n  C --> E[Output]"
}
```

**Mermaid diagram types:**
| Syntax keyword | Type |
|---|---|
| `flowchart LR` / `TD` | Flowchart (left-right / top-down) |
| `sequenceDiagram` | Sequence / interaction |
| `classDiagram` | Class / ER |
| `gantt` | Timeline / Gantt |
| `mindmap` | Mind map |
| `pie` | Pie chart (text-based) |
| `erDiagram` | Entity-relationship |
| `stateDiagram-v2` | State machine |

**VueFlow (interactive node graph):**
```json
{
  "id": "<uuid>", "type": "diagram",
  "engine": "vueflow",
  "x": 120, "y": 280, "width": 1680, "height": 600,
  "source": "{ \"nodes\": [{\"id\":\"1\",\"label\":\"Start\",\"position\":{\"x\":0,\"y\":0}}], \"edges\": [] }"
}
```

**Tips:**
- Keep Mermaid diagrams to 6–8 nodes per slide. Dense graphs → split into detail sub-slides.
- Use `flowchart LR` for process flows (horizontal reads left-to-right naturally).
- Use `sequenceDiagram` for API interactions, user journeys, multi-actor processes.
- Wrap long `source` strings as multiline using `\n` — Mermaid requires newlines between statements.

---

## line

**When:** Dividers between content regions, decorative accent lines, flow
arrows between content blocks.

```json
{
  "id": "<uuid>", "type": "line",
  "x": 80, "y": 200, "width": 1760, "height": 2,
  "line": "straight",
  "start": { "x": 0, "y": 0 },
  "end": { "x": 1760, "y": 0 },
  "stroke": { "token": "border" },
  "strokeWidth": 2
}
```

**Line types:** `straight`, `arrow`, `doubleArrow`, `curve`, `connector`.

**Common patterns:**
```json
// Accent underline below a title (use accent token, thick stroke):
{ ..., "width": 640, "height": 4, "line": "straight",
  "start": { "x": 0, "y": 0 }, "end": { "x": 640, "y": 0 },
  "stroke": { "token": "accent" }, "strokeWidth": 5 }

// Step connector arrow between process cards:
{ ..., "width": 40, "height": 2, "line": "arrow",
  "start": { "x": 0, "y": 0 }, "end": { "x": 40, "y": 0 },
  "stroke": { "token": "accent" }, "strokeWidth": 4 }
```

**Tips:**
- Horizontal divider: always `start.y=0, end.y=0, height=2–4`.
- Arrow connector between cards: width = gap between cards, `line: "arrow"`.
- Decorative accent: use `stroke: accent` and `strokeWidth: 4–8` for visual punch.

---

## frame

**When:** Product mockups, app screenshots shown inside a device frame,
image presented in a polaroid or picture-frame style.

```json
{
  "id": "<uuid>", "type": "frame",
  "x": 600, "y": 120, "width": 720, "height": 540,
  "frameKind": "browser",
  "src": "https://your-screenshot-url.png",
  "mediaFit": "cover"
}
```

**Frame templates:**
| `frameKind` | Best for | Aspect ratio |
|---|---|---|
| `laptop` | Desktop app / web screenshots | 16:9 content area |
| `desktop` | Monitor mockups | 16:9 content area |
| `phone` | Mobile app screenshots | 9:19.5 content area |
| `tablet` | Tablet UI mockups | 4:3 content area |
| `browser` | Web app / website screenshots | 16:9 content area |
| `pictureClassic` | Photos, maps, editorial | Any |
| `polaroid` | Retro-style photo showcase | Square content area |

**Fields:**
| Field | Notes |
|---|---|
| `src` | URL of the screenshot/image to display inside the frame. |
| `mediaFit` | `"cover"` (fills, may crop) or `"contain"` (shows all, may letterbox). |
| `mediaScale` | Zoom factor; `1` = default fit. |
| `mediaOffsetX/Y` | Pan the media within the frame (slide px). |
| `stroke`, `strokeWidth` | Optional border on the frame shape itself. |

**Common layout — two-panel mockup:**
```json
// Left: content text at x=80, right: phone frame at x=1060
{ "id": "<uuid>", "type": "frame", "frameKind": "phone",
  "x": 1080, "y": 80, "width": 380, "height": 760,
  "src": "https://...", "mediaFit": "cover" }
```

**Tips:**
- Use `browser` or `laptop` for web/desktop UI reveals; use `phone` for mobile screenshots.
- `polaroid` or `pictureClassic` adds visual personality to photo-driven slides.
- Combine two frames side-by-side (before/after comparison) with an arrow `line` between them.

---

## qr

**When:** Sharing a URL, resource link, or contact card with an audience.
Place in the bottom-right corner of a CTA or closing slide.

```json
{
  "id": "<uuid>", "type": "qr",
  "x": 1580, "y": 740, "width": 260, "height": 260,
  "mode": "url",
  "value": "https://example.com/resource",
  "errorCorrection": "M",
  "foreground": "#000000",
  "background": "#ffffff"
}
```

**Modes:**
| `mode` | Field | Use |
|---|---|---|
| `"url"` | `value` | Encodes any URL or plain text string |
| `"vcard"` | `contact` | Encodes a vCard contact (name, org, email, phone, url) |

**vCard example:**
```json
{
  "id": "<uuid>", "type": "qr",
  "x": 1600, "y": 760, "width": 240, "height": 240,
  "mode": "vcard",
  "contact": {
    "name": "Jane Smith",
    "org": "Acme Corp",
    "title": "Head of Product",
    "email": "jane@acme.com",
    "phone": "+1-555-0100",
    "url": "https://acme.com"
  },
  "errorCorrection": "H"
}
```

**Error correction levels:** `"L"` (7%), `"M"` (15%, default), `"Q"` (25%),
`"H"` (30%). Use `"H"` for small QR codes or when the image will be printed
and may be partially obscured.

**Tips:**
- Minimum size: 200 × 200 px for reliable scanning; 260 × 260 px recommended.
- On dark-background slides, set `foreground: "#ffffff"` and `background: "#000000"` (or
  use a white `shape` backing at the QR position).
- Add a `caption` text label below the QR: `"Scan to access the resource"`.

---

## placeholder

**When:** Building slide templates where the AI will fill in the content later,
or when storyboarding a slide structure before generating the final assets.

```json
{
  "id": "<uuid>", "type": "placeholder",
  "x": 80, "y": 200, "width": 880, "height": 600,
  "role": "image",
  "prompt": "Hero image: crowd at a tech conference, wide angle"
}
```

**Roles:** `"title"`, `"subtitle"`, `"body"`, `"image"`, `"chart"`, `"table"`, `"media"`.

**Tips:**
- Use `placeholder` in the first pass of a template to mark where content will go.
- Set `prompt` to the generation instruction — it shows as a hint in the editor.
- Replace placeholders with real objects before saving the final deck.

---

## Combinations and Slide Patterns

### Data story slide
```
[heading text]  +  [kpi_card]  +  [bar chart]  +  [caption text]
```
- Heading at `y=160`, KPI card at top-right `x=1400 y=160 w=440 h=160`,
  chart at `y=340 h=580`, caption at `y=940`.

### Process slide
```
[heading]  +  [process_flow cards]  +  [divider line]  +  [caption]
```
- Use `process_flow()` from `block_builder` for card + arrow sequences.

### Split slide (image + content)
```
[full-height image at x=1040]  +  [content stack at x=80 w=880]
```
- Image: `x=1040 y=0 w=880 h=1080 fit=cover`
- Content left: heading + body bullets + optional line accent + CTA

### Device mockup slide
```
[heading]  +  [frame: browser/phone]  +  [feature bullets]
```
- Frame at right half `x=980 y=120 w=860 h=680`
- 3–4 feature bullet cards stacked at left `x=80 w=840`

### Architecture diagram slide
```
[heading]  +  [diagram: mermaid]  +  [caption: source/context]
```
- Diagram: `x=80 y=240 w=1760 h=680`, engine `mermaid`
- No other objects — diagrams need space to breathe.

### Closing / CTA slide
```
[hero image full-bleed]  +  [shape overlay]  +  [title]  +  [subtitle]  +  [qr bottom-right]
```
- QR at `x=1600 y=760 w=240 h=240`, label caption below it.

### Formula / equation slide
```
[heading]  +  [text with latex]  +  [body explanation]
```
- Latex text centered: `x=240 y=320 w=1440 h=240 textAlign=center`
- Explanation body below: `x=240 y=580 w=1440 h=200`
