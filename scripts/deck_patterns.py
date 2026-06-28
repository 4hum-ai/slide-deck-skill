#!/usr/bin/env python3
"""Reusable Python helpers for generating slide-scene-graph deck JSON."""
from __future__ import annotations

from uuid import uuid4


def _id() -> str:
    return str(uuid4())


def token(name: str) -> dict:
    return {"token": name}


def dark_tech_theme(overrides: dict | None = None) -> dict:
    overrides = overrides or {}
    colors = {
        "background": "#0f172a",
        "surface": "#1e293b",
        "foreground": "#f8fafc",
        "mutedForeground": "#94a3b8",
        "primary": "#6366f1",
        "primaryForeground": "#ffffff",
        "accent": "#f59e0b",
        "accentForeground": "#000000",
        "border": "#334155",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "destructive": "#ef4444",
    }
    colors.update(overrides.get("colors", {}))
    text_styles = {
        "title": {"fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": token("foreground")},
        "subtitle": {"fontFamily": "body", "fontSize": 36, "fontWeight": 400, "color": token("mutedForeground")},
        "heading": {"fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": token("foreground")},
        "body": {"fontFamily": "body", "fontSize": 28, "fontWeight": 400, "color": token("foreground")},
        "caption": {"fontFamily": "body", "fontSize": 20, "fontWeight": 400, "color": token("mutedForeground")},
        "code": {"fontFamily": "mono", "fontSize": 22, "fontWeight": 400, "color": token("accent")},
    }
    text_styles.update(overrides.get("textStyles", {}))
    theme = {
        "id": _id(),
        "name": "Dark Tech",
        "fonts": {"display": "Inter", "heading": "Inter", "body": "Inter", "mono": "JetBrains Mono"},
        "colors": colors,
        "textStyles": text_styles,
    }
    theme.update(overrides.get("theme", {}))
    return theme


def text(role: str, x: float, y: float, width: float, height: float, content, **options) -> dict:
    return {
        "id": _id(),
        "type": "text",
        "role": role,
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "content": content,
        "textAlign": options.get("text_align", options.get("textAlign", "left")),
        "verticalAlign": options.get("vertical_align", options.get("verticalAlign", "top")),
        "autoFit": options.get("auto_fit", options.get("autoFit", "shrink")),
    }


def rich_text(role: str, x: float, y: float, width: float, height: float, runs: list[dict], **options) -> dict:
    return text(role, x, y, width, height, [{"kind": "block", "runs": runs}], **options)


def shape(x: float, y: float, width: float, height: float, fill: str = "surface", **options) -> dict:
    obj = {
        "id": _id(),
        "type": "shape",
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "shape": options.get("shape_kind", options.get("shape", "roundedRectangle")),
        "fill": token(fill),
        "stroke": token(options.get("stroke", "border")),
        "strokeWidth": options.get("stroke_width", options.get("strokeWidth", 1)),
        "cornerRadius": options.get("corner_radius", options.get("cornerRadius", 18)),
    }
    if "opacity" in options:
        obj["opacity"] = options["opacity"]
    return obj


def line(x: float, y: float, width: float, height: float = 2, **options) -> dict:
    safe_width = max(1, width)
    safe_height = max(1, height)
    return {
        "id": _id(),
        "type": "line",
        "x": x,
        "y": y,
        "width": safe_width,
        "height": safe_height,
        "line": options.get("line_kind", options.get("line", "straight")),
        "start": {"x": 0, "y": 0},
        "end": {"x": safe_width, "y": 0 if height <= 2 else safe_height},
        "stroke": token(options.get("stroke", "border")),
        "strokeWidth": options.get("stroke_width", options.get("strokeWidth", 2)),
    }


def image(seed_or_url: str, x: float, y: float, width: float, height: float, **options) -> dict:
    src = seed_or_url if seed_or_url.startswith(("http://", "https://")) else f"https://picsum.photos/seed/{seed_or_url}/1920/1080"
    return {
        "id": _id(),
        "type": "image",
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "src": src,
        "fit": options.get("fit", "cover"),
        "opacity": options.get("opacity", 1),
    }


def diagram(x: float, y: float, width: float, height: float, source: str) -> dict:
    return {
        "id": _id(),
        "type": "diagram",
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "engine": "mermaid",
        "source": source,
    }


def chart(x: float, y: float, width: float, height: float, categories: list[str], series: list[dict], chart_type: str = "bar") -> dict:
    return {
        "id": _id(),
        "type": "chart",
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "chart": chart_type,
        "categories": categories,
        "series": series,
    }


def table(x: float, y: float, width: float, height: float, rows: list[list[str]], **options) -> dict:
    return {
        "id": _id(),
        "type": "table",
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "rows": len(rows),
        "cols": len(rows[0]) if rows else 0,
        "headerRow": options.get("header_row", options.get("headerRow", True)),
        "styling": {
            "headerFill": token(options.get("header_fill", "primary")),
            "headerText": {"color": token("primaryForeground"), "fontWeight": 700},
            "bodyFill": token(options.get("body_fill", "surface")),
            "bodyText": {"color": token("foreground")},
            "borderColor": token("border"),
            "borderWidth": 1,
            "cellPadding": "m",
            "stripedRows": True,
        },
        "cells": [[{"text": str(cell)} for cell in row] for row in rows],
    }


def card(x: float, y: float, width: float, height: float, heading: str, body: str, **options) -> list[dict]:
    base = shape(x, y, width, height, options.get("fill", "surface"), corner_radius=options.get("corner_radius", 18), opacity=options.get("opacity", 1))
    if height <= 170:
        return [
            base,
            text("body", x + 28, y + 20, width - 56, 40, heading),
            text("caption", x + 28, y + 68, width - 56, max(32, height - 84), body),
        ]
    if height <= 240:
        return [
            base,
            text("body", x + 30, y + 24, width - 60, 44, heading),
            text("caption", x + 30, y + 78, width - 60, max(60, height - 98), body),
        ]
    return [
        base,
        text("heading", x + 34, y + 30, width - 68, 64, heading),
        text("body", x + 34, y + 112, width - 68, max(60, height - 140), body),
    ]


def title_chip(label: str, x: float = 92, y: float = 74, width: float = 300) -> list[dict]:
    return [
        shape(x, y, width, 46, "accent", stroke="accent", stroke_width=0, corner_radius=23),
        rich_text(
            "caption",
            x + 20,
            y + 8,
            width - 40,
            28,
            [{"kind": "span", "text": label, "style": {"color": token("accentForeground"), "fontWeight": 700}}],
            text_align="center",
            vertical_align="middle",
        ),
    ]


def slide(objects: list[dict], notes: str = "", speaker_notes: str = "", **options) -> dict:
    animatable = [obj for obj in objects if obj.get("type") != "image"][: options.get("max_animations", 8)]
    result = {
        "id": _id(),
        "background": options.get("background", {"kind": "solid", "color": token("background")}),
        "objects": objects,
        "animations": [
            {
                "id": _id(),
                "targetId": obj["id"],
                "category": "entrance",
                "effect": "fade" if index == 0 else "float",
                "trigger": "onEnter" if index == 0 else "withPrevious",
                "durationMs": 600 if index == 0 else 420,
                "delayMs": index * 90,
                "easing": "easeOut",
            }
            for index, obj in enumerate(animatable)
        ],
        "transitions": options.get("transitions", {"effect": "fade", "durationMs": 400}),
    }
    if notes:
        result["notes"] = notes
    if speaker_notes:
        result["speakerNotes"] = {"content": speaker_notes}
    return result


def section(title: str, slides: list[dict]) -> dict:
    return {"id": _id(), "title": title, "slides": slides}


def deck(title: str, sections: list[dict], **options) -> dict:
    return {
        "schema": "open-academy.slide-scene-graph",
        "schemaVersion": "0.4.0",
        "deck": {
            "id": _id(),
            "title": title,
            "width": 1920,
            "height": 1080,
            "theme": options.get("theme", dark_tech_theme()),
            "sections": sections,
        },
    }


def process_flow(items: list[dict], x: float, y: float, width: float, height: float) -> list[dict]:
    gap = 36
    step_width = (width - gap * (len(items) - 1)) / len(items)
    objects: list[dict] = []
    for index, item in enumerate(items):
        left = x + index * (step_width + gap)
        objects.extend(card(left, y, step_width, height, item["title"], item["body"]))
        if index < len(items) - 1:
            objects.append(line(left + step_width, y + height / 2, gap, 2, line="arrow", stroke="accent", stroke_width=4))
    return objects


def comparison_columns(columns: list[dict], x: float, y: float, width: float, height: float) -> list[dict]:
    gap = 46
    col_width = (width - gap * (len(columns) - 1)) / len(columns)
    objects: list[dict] = []
    for index, column in enumerate(columns):
        left = x + index * (col_width + gap)
        objects.extend(card(left, y, col_width, height, column["title"], column["body"], **column.get("options", {})))
    return objects
