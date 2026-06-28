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

## Font Mood Reference

Choose display/heading fonts to match the emotional register of the topic:

| Font | Mood / Best for | Pair with (body) |
|---|---|---|
| **Inter** | Clean, neutral, universal | Inter (same) |
| **Oswald** | Bold, sport, urgency, impact | Inter, Roboto |
| **Bebas Neue** | Aggressive, gaming, streetwear, posters | Inter, Open Sans |
| **Playfair Display** | Editorial, luxury, culture, journalism | Lato, Georgia |
| **Georgia** | Academic, trust, warmth, education | Georgia (same) |
| **Montserrat** | Modern corporate, fashion, lifestyle | Open Sans |
| **Raleway** | Elegant, minimalist, premium | Raleway Light (same) |
| **JetBrains Mono** | Tech, code, developer tools | JetBrains Mono |
| **Inter (300 weight)** | Ultra-minimal, portfolio, keynote | Inter Light |

**Quick rules:**
- Sports / competition → Oswald or Bebas Neue display, Inter body
- Editorial / culture → Playfair Display heading, Georgia body
- Tech / AI / data → Inter heading, JetBrains Mono for code role
- Minimal / design → Inter Light or Raleway, large whitespace
- Warm / education → Georgia display+body (same family = cohesion)

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
  "fonts": { "display": "Inter", "heading": "Inter", "body": "Inter", "mono": "JetBrains Mono" },
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

Title slide background:

```json
{"kind":"gradient","gradient":{"kind":"linear","angle":180,"stops":[{"color":{"token":"surface"},"offset":0},{"color":{"token":"background"},"offset":1}]}}
```

## Warm Creative

```json
{
  "id": "<uuid>",
  "name": "Warm Creative",
  "fonts": { "display": "Georgia", "heading": "Georgia", "body": "Inter", "mono": "JetBrains Mono" },
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

## Midnight Minimal

```json
{
  "id": "<uuid>",
  "name": "Midnight Minimal",
  "fonts": { "display": "Inter", "heading": "Inter", "body": "Inter", "mono": "JetBrains Mono" },
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
    "title": { "fontFamily": "heading", "fontSize": 72, "fontWeight": 300, "color": { "token": "foreground" } },
    "subtitle": { "fontFamily": "body", "fontSize": 36, "fontWeight": 300, "color": { "token": "mutedForeground" } },
    "heading": { "fontFamily": "heading", "fontSize": 48, "fontWeight": 400, "color": { "token": "foreground" } },
    "body": { "fontFamily": "body", "fontSize": 28, "fontWeight": 300, "color": { "token": "foreground" } },
    "caption": { "fontFamily": "body", "fontSize": 20, "fontWeight": 300, "color": { "token": "mutedForeground" } },
    "code": { "fontFamily": "mono", "fontSize": 22, "fontWeight": 400, "color": { "token": "accent" } }
  }
}
```

Title slide background:

```json
{"kind":"solid","color":{"token":"background"}}
```

## Forest Green

```json
{
  "id": "<uuid>",
  "name": "Forest Green",
  "fonts": { "display": "Inter", "heading": "Inter", "body": "Inter", "mono": "JetBrains Mono" },
  "colors": {
    "background": "#f0fdf4",
    "surface": "#dcfce7",
    "foreground": "#14532d",
    "mutedForeground": "#166534",
    "primary": "#16a34a",
    "primaryForeground": "#ffffff",
    "accent": "#84cc16",
    "accentForeground": "#14532d",
    "border": "#bbf7d0"
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
{"kind":"gradient","gradient":{"kind":"linear","angle":160,"stops":[{"color":{"token":"background"},"offset":0},{"color":{"token":"surface"},"offset":1}]}}
```

## Neon Purple

```json
{
  "id": "<uuid>",
  "name": "Neon Purple",
  "fonts": { "display": "Inter", "heading": "Inter", "body": "Inter", "mono": "JetBrains Mono" },
  "colors": {
    "background": "#0a0014",
    "surface": "#1a0b2e",
    "foreground": "#faf5ff",
    "mutedForeground": "#c084fc",
    "primary": "#a855f7",
    "primaryForeground": "#ffffff",
    "accent": "#06b6d4",
    "accentForeground": "#000000",
    "border": "#581c87"
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
