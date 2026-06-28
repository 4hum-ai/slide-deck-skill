# Theme Presets

Two example themes showing the complete required structure. Use them as
structural references when designing a **custom** theme for the current deck
— derive colors, fonts, and emotional register from the topic and audience
(do not copy them verbatim).

The Font Mood Reference below guides the key creative decision (typeface
selection). The color psychology guidance lives in SKILL.md step 3.

## Selection table

| Background | When to start here |
|---|---|
| Dark (Dark Tech) | Tech, AI/ML, sport, entertainment, gaming, bold statements |
| Light (Light Corporate) | Finance, corporate reports, academic, formal presentations |

For any other tone — warm/creative, minimal/portfolio, nature/wellness —
create a fully custom theme using the Font Mood Reference and color tokens
below. The two examples above are structure templates, not the full palette.

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
