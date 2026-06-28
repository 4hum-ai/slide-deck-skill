# Slide Scene-Graph v0.4.0 Reference

All coordinates are pixels on a 1920 x 1080 canvas. Pass the complete envelope.

## Envelope

```json
{
  "schema": "open-academy.slide-scene-graph",
  "schemaVersion": "0.4.0",
  "deck": {
    "id": "<uuid-v4>",
    "title": "Deck Title",
    "width": 1920,
    "height": 1080,
    "theme": {},
    "sections": []
  }
}
```

## Sections and Slides

```json
{
  "id": "<uuid-v4>",
  "title": "Section Name",
  "slides": [
    {
      "id": "<uuid-v4>",
      "background": { "kind": "solid", "color": { "token": "background" } },
      "objects": [],
      "transitions": { "effect": "fade", "durationMs": 400 }
    }
  ]
}
```

Background kinds: `none`, `solid`, `gradient`, `image`.

## Shared Object Fields

Every object needs:

```json
{ "id": "<uuid>", "type": "...", "x": 80, "y": 120, "width": 400, "height": 200 }
```

`width` and `height` must be non-negative. Prefer positive bounds for all visible
objects, including divider lines.

## Text

```json
{
  "id": "<uuid>",
  "type": "text",
  "role": "heading",
  "x": 80,
  "y": 120,
  "width": 1760,
  "height": 100,
  "content": "Slide title",
  "textAlign": "left",
  "verticalAlign": "top",
  "autoFit": "shrink"
}
```

Roles: `title`, `subtitle`, `heading`, `body`, `caption`, `code`.

Rich text:

```json
"content": [
  {
    "kind": "block",
    "runs": [
      { "kind": "span", "text": "Important", "style": { "fontWeight": 700, "color": { "token": "accent" } } }
    ]
  }
]
```

Use theme font slots (`heading`, `body`, `mono`, `display`) rather than literal
font names on runs.

## Shape

```json
{
  "id": "<uuid>",
  "type": "shape",
  "x": 100,
  "y": 100,
  "width": 400,
  "height": 200,
  "shape": "roundedRectangle",
  "fill": { "token": "surface" },
  "stroke": { "token": "border" },
  "strokeWidth": 1,
  "cornerRadius": 16
}
```

Shapes: `rectangle`, `roundedRectangle`, `ellipse`, `triangle`,
`rightTriangle`, `diamond`, `parallelogram`, `trapezoid`, `pentagon`,
`hexagon`, `star`, `arrow`, `callout`, `customPath`.

## Image

```json
{
  "id": "<uuid>",
  "type": "image",
  "x": 960,
  "y": 0,
  "width": 960,
  "height": 1080,
  "src": "https://picsum.photos/seed/technology/1920/1080",
  "fit": "cover",
  "opacity": 1
}
```

Fits: `cover`, `contain`, `fill`. Use generated image `file_url` values when
custom visuals are needed.

## Chart

```json
{
  "id": "<uuid>",
  "type": "chart",
  "x": 200,
  "y": 220,
  "width": 1200,
  "height": 600,
  "chart": "bar",
  "categories": ["Q1", "Q2"],
  "series": [{ "name": "Revenue", "values": [120, 145], "color": { "token": "primary" } }]
}
```

Charts: `bar`, `line`, `area`, `pie`, `doughnut`, `rose`, `scatter`, `radar`,
`funnel`, `gauge`, `heatmap`. Series use `values`, not `data`.

## Table

```json
{
  "id": "<uuid>",
  "type": "table",
  "x": 160,
  "y": 240,
  "width": 1600,
  "height": 520,
  "rows": 2,
  "cols": 2,
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
    [{ "text": "Header 1" }, { "text": "Header 2" }],
    [{ "text": "Body 1" }, { "text": "Body 2" }]
  ]
}
```

`cells` must be a rectangular 2D array matching `rows` and `cols`.

## Diagram

```json
{
  "id": "<uuid>",
  "type": "diagram",
  "x": 200,
  "y": 240,
  "width": 1520,
  "height": 600,
  "engine": "mermaid",
  "source": "flowchart LR\n  A[Start] --> B[End]"
}
```

Engines: `mermaid`, `drawio`, `vueflow`.

## Line

```json
{
  "id": "<uuid>",
  "type": "line",
  "x": 80,
  "y": 540,
  "width": 1760,
  "height": 2,
  "line": "straight",
  "start": { "x": 0, "y": 0 },
  "end": { "x": 1760, "y": 0 },
  "stroke": { "token": "border" },
  "strokeWidth": 2
}
```

Line types: `straight`, `arrow`, `doubleArrow`, `curve`, `connector`.

## Animations and Transitions

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
],
"transitions": { "effect": "fade", "durationMs": 400 }
```

Animation categories: `entrance`, `emphasis`, `exit`. Effects: `fade`, `fly`,
`float`, `zoom`, `grow`, `spin`, `bounce`, `pulse`, `teeter`, `flash`,
`shrink`. Triggers: `onEnter`, `onClick`, `afterPrevious`, `withPrevious`.

## Notes and Speaker Notes

Use `notes` for narration/TTS and `speakerNotes.content` for presenter notes
and source citations.

Citation format:

```text
Source: <Author/Org>, '<Title>', <Month Year> - <URL>
```
