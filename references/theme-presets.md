# Theme Presets

Use a preset that matches the deck tone, then copy the full `theme` object into
`deck.theme`. Every preset must include `textStyles`; every text object should
set a `role` so the renderer applies the typography scale.

## Selection

| Tone / Topic | Preset |
|---|---|
| Tech, AI/ML, dev tools, data science | Dark Tech |
| Business, finance, corporate, reports | Light Corporate |
| Creative, marketing, education, lifestyle | Warm Creative |
| Minimalist, design portfolio, keynote | Midnight Minimal |
| Sustainability, health, nature, wellness | Forest Green |
| Gaming, entertainment, innovation, bold | Neon Purple |

## Dark Tech

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
    "title": { "fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body", "fontSize": 36, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "heading": { "fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": { "token": "foreground" } },
    "body": { "fontFamily": "body", "fontSize": 28, "fontWeight": 400, "color": { "token": "foreground" } },
    "caption": { "fontFamily": "body", "fontSize": 20, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "code": { "fontFamily": "mono", "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```

Title slide background:

```json
{"kind":"gradient","gradient":{"kind":"linear","angle":135,"stops":[{"color":{"token":"background"},"offset":0},{"color":{"token":"surface"},"offset":1}]}}
```

## Light Corporate

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
    "border": "#e2e8f0"
  },
  "textStyles": {
    "title": { "fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body", "fontSize": 36, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "heading": { "fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": { "token": "foreground" } },
    "body": { "fontFamily": "body", "fontSize": 28, "fontWeight": 400, "color": { "token": "foreground" } },
    "caption": { "fontFamily": "body", "fontSize": 20, "fontWeight": 400, "color": { "token": "mutedForeground" } },
    "code": { "fontFamily": "mono", "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```

## Warm Creative

Use for creative, education, and lifestyle decks. Base colors: `background`
`#fef9f0`, `surface` `#fff7ed`, `foreground` `#1c1917`, `primary`
`#ea580c`, `accent` `#d97706`, `border` `#fed7aa`. Use the same text style
scale as Light Corporate.

## Midnight Minimal

Use for minimalist keynotes and design portfolios. Base colors: `background`
`#000000`, `surface` `#111111`, `foreground` `#ffffff`, `mutedForeground`
`#737373`, `primary` `#ffffff`, `accent` `#22d3ee`, `border` `#262626`.

## Forest Green

Use for sustainability, health, nature, and wellness. Base colors: `background`
`#f0fdf4`, `surface` `#dcfce7`, `foreground` `#14532d`, `mutedForeground`
`#166534`, `primary` `#16a34a`, `accent` `#84cc16`, `border` `#bbf7d0`.

## Neon Purple

Use for gaming, entertainment, bold innovation, and high-energy topics. Base
colors: `background` `#0a0014`, `surface` `#1a0b2e`, `foreground` `#faf5ff`,
`mutedForeground` `#c084fc`, `primary` `#a855f7`, `accent` `#06b6d4`,
`border` `#581c87`.

## Color Tokens

Use token refs anywhere a color field appears:

```json
{"token":"foreground"}
```

Valid tokens: `background`, `surface`, `foreground`, `mutedForeground`,
`primary`, `primaryForeground`, `accent`, `accentForeground`, `border`,
`success`, `warning`, `destructive`.

Aliases accepted by the renderer: `text` = `foreground`, `mutedText` =
`mutedForeground`, `line` = `border`, `danger` = `destructive`.

Raw hex should live in `theme.colors`, not directly on slide objects.
