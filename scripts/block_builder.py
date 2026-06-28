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


def light_corporate_theme(overrides: dict | None = None) -> dict:
    overrides = overrides or {}
    colors = {
        "background": "#ffffff",
        "surface": "#f8fafc",
        "foreground": "#0f172a",
        "mutedForeground": "#64748b",
        "primary": "#2563eb",
        "primaryForeground": "#ffffff",
        "accent": "#f59e0b",
        "accentForeground": "#000000",
        "border": "#e2e8f0",
        "success": "#16a34a",
        "warning": "#d97706",
        "destructive": "#dc2626",
    }
    colors.update(overrides.get("colors", {}))
    text_styles = {
        "title": {"fontFamily": "heading", "fontSize": 72, "fontWeight": 700, "color": token("foreground")},
        "subtitle": {"fontFamily": "body", "fontSize": 36, "fontWeight": 400, "color": token("mutedForeground")},
        "heading": {"fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": token("foreground")},
        "body": {"fontFamily": "body", "fontSize": 28, "fontWeight": 400, "color": token("foreground")},
        "caption": {"fontFamily": "body", "fontSize": 20, "fontWeight": 400, "color": token("mutedForeground")},
        "code": {"fontFamily": "mono", "fontSize": 22, "fontWeight": 400, "color": token("primary")},
    }
    text_styles.update(overrides.get("textStyles", {}))
    theme = {
        "id": _id(),
        "name": "Light Corporate",
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


def video(src: str, x: float, y: float, width: float, height: float, **options) -> dict:
    obj = {
        "id": _id(),
        "type": "video",
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "src": src,
        "autoplay": options.get("autoplay", False),
        "loop": options.get("loop", False),
        "muted": options.get("muted", False),
        "controls": options.get("controls", True),
    }
    if "poster" in options:
        obj["poster"] = options["poster"]
    if options.get("shape") in ("rectangle", "circle"):
        obj["shape"] = options["shape"]
    return obj


def embed(url: str, x: float, y: float, width: float, height: float, **options) -> dict:
    obj = {
        "id": _id(),
        "type": "embed",
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "url": url,
    }
    if "embed_kind" in options or "embedKind" in options:
        obj["embedKind"] = options.get("embed_kind", options.get("embedKind"))
    if "autoplay" in options:
        obj["autoplay"] = options["autoplay"]
    return obj


def qr_code(value: str, x: float, y: float, size: float = 260, **options) -> dict:
    return {
        "id": _id(),
        "type": "qr",
        "x": x,
        "y": y,
        "width": size,
        "height": size,
        "mode": "url",
        "value": value,
        "errorCorrection": options.get("error_correction", options.get("errorCorrection", "M")),
        "foreground": options.get("foreground", "#000000"),
        "background": options.get("background", "#ffffff"),
    }


def qr_vcard(contact: dict, x: float, y: float, size: float = 260, **options) -> dict:
    return {
        "id": _id(),
        "type": "qr",
        "x": x,
        "y": y,
        "width": size,
        "height": size,
        "mode": "vcard",
        "contact": contact,
        "errorCorrection": options.get("error_correction", options.get("errorCorrection", "H")),
        "foreground": options.get("foreground", "#000000"),
        "background": options.get("background", "#ffffff"),
    }


def frame(x: float, y: float, width: float, height: float, **options) -> dict:
    obj = {
        "id": _id(),
        "type": "frame",
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "frameKind": options.get("frame_kind", options.get("frameKind", "browser")),
        "mediaFit": options.get("media_fit", options.get("mediaFit", "cover")),
    }
    if "src" in options:
        obj["src"] = options["src"]
    if "media_scale" in options or "mediaScale" in options:
        obj["mediaScale"] = options.get("media_scale", options.get("mediaScale"))
    if "stroke" in options:
        obj["stroke"] = token(options["stroke"]) if isinstance(options["stroke"], str) else options["stroke"]
    if "stroke_width" in options or "strokeWidth" in options:
        obj["strokeWidth"] = options.get("stroke_width", options.get("strokeWidth", 1))
    return obj


def latex_text(formula: str, x: float, y: float, width: float, height: float, **options) -> dict:
    return {
        "id": _id(),
        "type": "text",
        "role": options.get("role", "body"),
        "x": x,
        "y": y,
        "width": max(1, width),
        "height": max(1, height),
        "content": formula,
        "latex": formula,
        "textAlign": options.get("text_align", options.get("textAlign", "center")),
        "verticalAlign": options.get("vertical_align", options.get("verticalAlign", "middle")),
        "autoFit": "shrink",
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
    animate = options.get("animate", True)
    animatable = [obj for obj in objects if obj.get("type") != "image"][: options.get("max_animations", 8)]
    animations = (
        [
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
        ]
        if animate
        else []
    )
    result = {
        "id": _id(),
        "background": options.get("background", {"kind": "solid", "color": token("background")}),
        "objects": objects,
        "animations": animations,
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


def portrait_card(
    image_url: str,
    name: str,
    subtitle: str,
    body: str,
    x: float,
    y: float,
    w: float,
    h: float,
    **options,
) -> list[dict]:
    """Vertical card with a portrait image at the top followed by name, subtitle, and body text.

    Default proportions (tested on 390×440 cards in a 4-column layout):
        - Card background shape fills the full card
        - Portrait image occupies the top ~66 % (cover fit)
        - Name (heading), subtitle (caption), body text stack below the image
    """
    img_h = round(h * 0.66)
    text_top = y + img_h
    text_x = x + 16
    text_w = w - 32
    name_h = min(52, round(h * 0.12))
    sub_h = min(36, round(h * 0.08))
    body_h = max(24, h - img_h - name_h - sub_h - 24)
    return [
        shape(x, y, w, h, options.get("fill", "surface"),
              corner_radius=options.get("corner_radius", 18),
              opacity=options.get("opacity", 1)),
        image(image_url, x, y, w, img_h, fit="cover"),
        text("heading", text_x, text_top + 8, text_w, name_h, name,
             text_align="center", vertical_align="middle"),
        text("caption", text_x, text_top + 8 + name_h, text_w, sub_h, subtitle,
             text_align="center", vertical_align="middle"),
        text("body", text_x, text_top + 8 + name_h + sub_h, text_w, body_h, body,
             text_align="center", vertical_align="top"),
    ]


def kpi_card(
    value: str,
    label: str,
    x: float,
    y: float,
    w: float,
    h: float,
    **options,
) -> list[dict]:
    """Large KPI / metric card with a prominent value and a small descriptive label below."""
    val_h = round(h * 0.55)
    lbl_h = max(28, h - val_h - 16)
    return [
        shape(x, y, w, h, options.get("fill", "surface"),
              corner_radius=options.get("corner_radius", 18)),
        text("title", x + 16, y + 8, w - 32, val_h, value,
             text_align="center", vertical_align="middle"),
        text("caption", x + 16, y + 8 + val_h, w - 32, lbl_h, label,
             text_align="center", vertical_align="top"),
    ]


def grid(
    items,
    cols: int,
    x: float,
    y: float,
    total_w: float,
    total_h: float,
    gap: float = 24,
) -> list[dict]:
    """Distribute items into a uniform grid and return a flat objects list.

    items can be:
    - A list of callables ``(x, y, w, h) -> list[dict]``  (use a lambda or functools.partial)
    - A list of dicts with keys ``'heading'`` and ``'body'`` (auto-creates card objects)

    Example::

        grid(
            [lambda x,y,w,h: kpi_card("$1.2B", "Revenue", x,y,w,h) for _ in stats],
            cols=4, x=80, y=300, total_w=1760, total_h=300
        )
    """
    rows = -(-len(items) // cols)  # ceiling division
    cell_w = (total_w - gap * (cols - 1)) / cols
    cell_h = (total_h - gap * (rows - 1)) / rows
    objects: list[dict] = []
    for idx, item in enumerate(items):
        col = idx % cols
        row = idx // cols
        cx = x + col * (cell_w + gap)
        cy = y + row * (cell_h + gap)
        if callable(item):
            objects.extend(item(cx, cy, cell_w, cell_h))
        elif isinstance(item, dict):
            objects.extend(card(cx, cy, cell_w, cell_h,
                                item.get("heading", ""), item.get("body", "")))
        else:
            raise TypeError(f"grid item must be callable or dict, got {type(item)}")
    return objects


def bullet_list(
    items: list,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    numbered: bool = False,
    bullet: str = "•",
    **options,
) -> dict:
    """Single text object containing a bullet or numbered list.

    Prefer this over repeating shape+text pairs when you have 4+ items — it
    keeps object count low and the layout clean.

    Args:
        items: List of strings (simple items) or dicts with ``"title"`` and
               optional ``"body"`` keys (two-line items).
        numbered: If True, use "1.", "2.", … instead of ``bullet``.
        bullet: The bullet character. Defaults to "•".

    Example::

        bullet_list(
            ["Early Cancer Detection", "Predictive Analytics", "Drug Discovery"],
            x=100, y=300, width=760, height=500,
            role="body",
        )
    """
    lines: list[str] = []
    for i, item in enumerate(items):
        prefix = f"{i + 1}." if numbered else bullet
        if isinstance(item, str):
            lines.append(f"{prefix}  {item}")
        elif isinstance(item, dict):
            title = item.get("title", item.get("heading", ""))
            body = item.get("body", item.get("description", ""))
            if body:
                lines.append(f"{prefix}  {title}: {body}")
            else:
                lines.append(f"{prefix}  {title}")
    content = "\n".join(lines)
    return text(
        options.pop("role", "body"),
        x, y, width, height,
        content,
        **options,
    )


def numbered_list(items: list, x: float, y: float, width: float, height: float, **options) -> dict:
    """Numbered list — convenience wrapper around bullet_list(numbered=True)."""
    return bullet_list(items, x, y, width, height, numbered=True, **options)


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
