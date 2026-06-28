#!/usr/bin/env python3
"""
Local preflight validation for deck-4hum-ai scene-graph JSON.

This validator is intentionally conservative. It catches common authoring
mistakes before save_deck.py posts to the API, and reports paths in the same
shape as API errors so failures are easy to locate.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from typing import Any


VALID_TEXT_ROLES = {"title", "subtitle", "heading", "body", "caption", "code"}
VALID_OBJECT_TYPES = {
    "text",
    "shape",
    "image",
    "chart",
    "table",
    "diagram",
    "embed",
    "qr",
    "line",
    "frame",
    "placeholder",
}
VALID_LINE_TYPES = {"straight", "arrow", "doubleArrow", "curve", "connector"}
VALID_SHAPES = {
    "rectangle",
    "roundedRectangle",
    "ellipse",
    "triangle",
    "rightTriangle",
    "diamond",
    "parallelogram",
    "trapezoid",
    "pentagon",
    "hexagon",
    "star",
    "arrow",
    "callout",
    "customPath",
}
VALID_IMAGE_FITS = {"cover", "contain", "fill"}
VALID_CHARTS = {
    "bar",
    "line",
    "area",
    "pie",
    "doughnut",
    "rose",
    "scatter",
    "radar",
    "funnel",
    "gauge",
    "heatmap",
}
VALID_DIAGRAM_ENGINES = {"mermaid", "drawio", "vueflow"}
VALID_COLOR_TOKENS = {
    "background",
    "surface",
    "foreground",
    "mutedForeground",
    "primary",
    "primaryForeground",
    "accent",
    "accentForeground",
    "border",
    "success",
    "warning",
    "destructive",
    "text",
    "mutedText",
    "line",
    "danger",
}
HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

# Populated by validate_deck() with the custom token names defined in theme.colors.
# This allows custom tokens (e.g. "highlight", "gradientStart") to pass validation.
_deck_custom_tokens: frozenset = frozenset()


@dataclass
class ValidationIssue:
    path: str
    message: str

    def format(self) -> str:
        return f"{self.path}: {self.message}"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _add(issues: list[ValidationIssue], path: str, message: str) -> None:
    issues.append(ValidationIssue(path, message))


def _require_dict(value: Any, path: str, issues: list[ValidationIssue]) -> bool:
    if isinstance(value, dict):
        return True
    _add(issues, path, "must be an object")
    return False


def _require_list(value: Any, path: str, issues: list[ValidationIssue]) -> bool:
    if isinstance(value, list):
        return True
    _add(issues, path, "must be an array")
    return False


def _require_string(parent: dict[str, Any], key: str, path: str, issues: list[ValidationIssue]) -> None:
    if not isinstance(parent.get(key), str) or not parent.get(key):
        _add(issues, f"{path}.{key}", "must be a non-empty string")


def _require_number(parent: dict[str, Any], key: str, path: str, issues: list[ValidationIssue]) -> None:
    if not _is_number(parent.get(key)):
        _add(issues, f"{path}.{key}", "must be a number")


def _validate_color(value: Any, path: str, issues: list[ValidationIssue], *, allow_hex: bool = False) -> None:
    if isinstance(value, dict):
        token = value.get("token")
        if token not in VALID_COLOR_TOKENS and token not in _deck_custom_tokens:
            _add(issues, path, "must be a theme token reference such as {'token': 'foreground'}")
        return
    if isinstance(value, str) and allow_hex and HEX_RE.match(value):
        return
    _add(issues, path, "must be a theme token reference")


def _validate_text_style(style: Any, path: str, issues: list[ValidationIssue]) -> None:
    if not isinstance(style, dict):
        return
    if "color" in style:
        _validate_color(style["color"], f"{path}.color", issues)
    if "fontFamily" in style and style["fontFamily"] not in {"display", "heading", "body", "mono"}:
        _add(issues, f"{path}.fontFamily", "must use a theme font slot, not a literal font name")


def _validate_text_content(content: Any, path: str, issues: list[ValidationIssue]) -> None:
    if isinstance(content, str):
        return
    if isinstance(content, dict):
        blocks = content.get("content")
        if blocks is not None:
            _validate_text_content(blocks, f"{path}.content", issues)
            return
    if not isinstance(content, list):
        _add(issues, path, "must be a string or TextContent block array")
        return
    for block_index, block in enumerate(content):
        block_path = f"{path}.{block_index}"
        if not _require_dict(block, block_path, issues):
            continue
        if block.get("kind") != "block":
            _add(issues, f"{block_path}.kind", "must be 'block'")
        runs = block.get("runs")
        if not _require_list(runs, f"{block_path}.runs", issues):
            continue
        for run_index, run in enumerate(runs):
            run_path = f"{block_path}.runs.{run_index}"
            if not _require_dict(run, run_path, issues):
                continue
            if run.get("kind") not in {"span", "softBreak"}:
                _add(issues, f"{run_path}.kind", "must be 'span' or 'softBreak'")
            if run.get("kind") == "span" and not isinstance(run.get("text"), str):
                _add(issues, f"{run_path}.text", "must be a string")
            _validate_text_style(run.get("style"), f"{run_path}.style", issues)


def _validate_common_object(obj: dict[str, Any], path: str, issues: list[ValidationIssue]) -> None:
    _require_string(obj, "id", path, issues)
    obj_type = obj.get("type")
    if obj_type not in VALID_OBJECT_TYPES:
        _add(issues, f"{path}.type", f"must be one of {sorted(VALID_OBJECT_TYPES)}")
    for key in ("x", "y", "width", "height"):
        _require_number(obj, key, path, issues)
    for key in ("width", "height"):
        if _is_number(obj.get(key)) and obj[key] < 0:
            _add(issues, f"{path}.{key}", "must be greater than or equal to 0")


def _validate_table(obj: dict[str, Any], path: str, issues: list[ValidationIssue]) -> None:
    rows = obj.get("rows")
    cols = obj.get("cols")
    if not isinstance(rows, int) or rows <= 0:
        _add(issues, f"{path}.rows", "must be a positive integer")
    if not isinstance(cols, int) or cols <= 0:
        _add(issues, f"{path}.cols", "must be a positive integer")
    cells = obj.get("cells")
    if not _require_list(cells, f"{path}.cells", issues):
        return
    if isinstance(rows, int) and len(cells) != rows:
        _add(issues, f"{path}.cells", f"must contain exactly rows={rows} row arrays")
    for row_index, row in enumerate(cells):
        row_path = f"{path}.cells.{row_index}"
        if not _require_list(row, row_path, issues):
            continue
        if isinstance(cols, int) and len(row) != cols:
            _add(issues, row_path, f"must contain exactly cols={cols} cell objects")
        for col_index, cell in enumerate(row):
            cell_path = f"{row_path}.{col_index}"
            if not _require_dict(cell, cell_path, issues):
                continue
            if "text" not in cell:
                _add(issues, f"{cell_path}.text", "is required")
            elif not isinstance(cell["text"], str):
                _add(issues, f"{cell_path}.text", "must be a string")
    styling = obj.get("styling")
    if not _require_dict(styling, f"{path}.styling", issues):
        return
    for color_key in ("headerFill", "bodyFill", "borderColor", "accentFill"):
        if color_key in styling:
            _validate_color(styling[color_key], f"{path}.styling.{color_key}", issues)
    for text_key in ("headerText", "bodyText"):
        style = styling.get(text_key)
        if not isinstance(style, dict):
            _add(issues, f"{path}.styling.{text_key}", "must include a text style object")
            continue
        if "color" not in style:
            _add(issues, f"{path}.styling.{text_key}.color", "is required so table text is readable")
        else:
            _validate_color(style["color"], f"{path}.styling.{text_key}.color", issues)


def _validate_object(obj: Any, path: str, issues: list[ValidationIssue]) -> None:
    if not _require_dict(obj, path, issues):
        return
    _validate_common_object(obj, path, issues)
    obj_type = obj.get("type")

    if obj_type == "text":
        role = obj.get("role")
        if role not in VALID_TEXT_ROLES:
            _add(issues, f"{path}.role", f"must be one of {sorted(VALID_TEXT_ROLES)}")
        if "content" not in obj:
            _add(issues, f"{path}.content", "is required")
        else:
            _validate_text_content(obj["content"], f"{path}.content", issues)
        for style_key in ("color",):
            if style_key in obj:
                _validate_color(obj[style_key], f"{path}.{style_key}", issues)
    elif obj_type == "shape":
        if obj.get("shape") not in VALID_SHAPES:
            _add(issues, f"{path}.shape", f"must be one of {sorted(VALID_SHAPES)}")
        if "fill" in obj:
            _validate_color(obj["fill"], f"{path}.fill", issues, allow_hex=False)
        if "stroke" in obj:
            _validate_color(obj["stroke"], f"{path}.stroke", issues, allow_hex=False)
    elif obj_type == "image":
        _require_string(obj, "src", path, issues)
        if obj.get("fit") is not None and obj["fit"] not in VALID_IMAGE_FITS:
            _add(issues, f"{path}.fit", f"must be one of {sorted(VALID_IMAGE_FITS)}")
    elif obj_type == "chart":
        if obj.get("chart") not in VALID_CHARTS:
            _add(issues, f"{path}.chart", f"must be one of {sorted(VALID_CHARTS)}")
        if not isinstance(obj.get("categories"), list):
            _add(issues, f"{path}.categories", "must be an array")
        series = obj.get("series")
        if not _require_list(series, f"{path}.series", issues):
            return
        for index, item in enumerate(series):
            item_path = f"{path}.series.{index}"
            if not _require_dict(item, item_path, issues):
                continue
            _require_string(item, "name", item_path, issues)
            values = item.get("values")
            if not isinstance(values, list) or not all(_is_number(value) for value in values):
                _add(issues, f"{item_path}.values", "must be an array of numbers")
            if "color" in item:
                _validate_color(item["color"], f"{item_path}.color", issues)
    elif obj_type == "table":
        _validate_table(obj, path, issues)
    elif obj_type == "diagram":
        if obj.get("engine") not in VALID_DIAGRAM_ENGINES:
            _add(issues, f"{path}.engine", f"must be one of {sorted(VALID_DIAGRAM_ENGINES)}")
        _require_string(obj, "source", path, issues)
    elif obj_type == "line":
        if obj.get("line") not in VALID_LINE_TYPES:
            _add(issues, f"{path}.line", f"must be one of {sorted(VALID_LINE_TYPES)}")
        for point_key in ("start", "end"):
            point = obj.get(point_key)
            point_path = f"{path}.{point_key}"
            if not _require_dict(point, point_path, issues):
                continue
            _require_number(point, "x", point_path, issues)
            _require_number(point, "y", point_path, issues)
        if _is_number(obj.get("width")) and _is_number(obj.get("height")) and obj["width"] == 0 and obj["height"] == 0:
            _add(issues, path, "line bounds cannot have both width and height equal to 0")
        if "stroke" in obj:
            _validate_color(obj["stroke"], f"{path}.stroke", issues, allow_hex=True)


def _validate_background(background: Any, path: str, issues: list[ValidationIssue]) -> None:
    if not _require_dict(background, path, issues):
        return
    kind = background.get("kind")
    if kind not in {"none", "solid", "gradient", "image"}:
        _add(issues, f"{path}.kind", "must be one of ['none', 'solid', 'gradient', 'image']")
    if kind == "solid" and "color" in background:
        _validate_color(background["color"], f"{path}.color", issues)
    if kind == "gradient":
        gradient = background.get("gradient")
        if not _require_dict(gradient, f"{path}.gradient", issues):
            return
        stops = gradient.get("stops")
        if not _require_list(stops, f"{path}.gradient.stops", issues):
            return
        for index, stop in enumerate(stops):
            stop_path = f"{path}.gradient.stops.{index}"
            if not _require_dict(stop, stop_path, issues):
                continue
            if "color" in stop:
                _validate_color(stop["color"], f"{stop_path}.color", issues)
            else:
                _add(issues, f"{stop_path}.color", "is required")
    if kind == "image":
        _require_string(background, "src", path, issues)


def _validate_theme(theme: Any, path: str, issues: list[ValidationIssue]) -> None:
    if not _require_dict(theme, path, issues):
        return
    _require_string(theme, "id", path, issues)
    _require_string(theme, "name", path, issues)
    colors = theme.get("colors")
    if _require_dict(colors, f"{path}.colors", issues):
        for key, value in colors.items():
            if not isinstance(value, str) or not HEX_RE.match(value):
                _add(issues, f"{path}.colors.{key}", "must be a hex color string")
    text_styles = theme.get("textStyles")
    if _require_dict(text_styles, f"{path}.textStyles", issues):
        for role in VALID_TEXT_ROLES:
            if role not in text_styles:
                _add(issues, f"{path}.textStyles.{role}", "is recommended so text roles render with hierarchy")
        for role, style in text_styles.items():
            if isinstance(style, dict):
                _validate_text_style(style, f"{path}.textStyles.{role}", issues)


def validate_deck(deck_json: Any) -> list[ValidationIssue]:
    global _deck_custom_tokens
    issues: list[ValidationIssue] = []
    if not _require_dict(deck_json, "deckJson", issues):
        return issues

    # Collect the deck's own theme token names so custom tokens pass color validation.
    _deck_custom_tokens = frozenset(
        (deck_json.get("deck") or {}).get("theme", {}).get("colors", {}).keys()
    )

    if deck_json.get("schema") != "open-academy.slide-scene-graph":
        _add(issues, "deckJson.schema", "must be 'open-academy.slide-scene-graph'")
    if deck_json.get("schemaVersion") != "0.4.0":
        _add(issues, "deckJson.schemaVersion", "must be '0.4.0'")

    deck = deck_json.get("deck")
    if not _require_dict(deck, "deckJson.deck", issues):
        return issues
    _require_string(deck, "id", "deckJson.deck", issues)
    _require_string(deck, "title", "deckJson.deck", issues)
    for key in ("width", "height"):
        _require_number(deck, key, "deckJson.deck", issues)
        if _is_number(deck.get(key)) and deck[key] <= 0:
            _add(issues, f"deckJson.deck.{key}", "must be greater than 0")
    _validate_theme(deck.get("theme"), "deckJson.deck.theme", issues)

    sections = deck.get("sections")
    if not _require_list(sections, "deckJson.deck.sections", issues):
        return issues
    if not sections:
        _add(issues, "deckJson.deck.sections", "must contain at least one section")
    for section_index, section in enumerate(sections):
        section_path = f"deckJson.deck.sections.{section_index}"
        if not _require_dict(section, section_path, issues):
            continue
        _require_string(section, "id", section_path, issues)
        _require_string(section, "title", section_path, issues)
        slides = section.get("slides")
        if not _require_list(slides, f"{section_path}.slides", issues):
            continue
        for slide_index, slide in enumerate(slides):
            slide_path = f"{section_path}.slides.{slide_index}"
            if not _require_dict(slide, slide_path, issues):
                continue
            _require_string(slide, "id", slide_path, issues)
            if "background" in slide:
                _validate_background(slide["background"], f"{slide_path}.background", issues)
            objects = slide.get("objects")
            if not _require_list(objects, f"{slide_path}.objects", issues):
                continue
            for object_index, obj in enumerate(objects):
                _validate_object(obj, f"{slide_path}.objects.{object_index}", issues)
    return issues


def format_validation_errors(issues: list[ValidationIssue]) -> str:
    lines = ["Validation failed:"]
    lines.extend(f"- {issue.format()}" for issue in issues)
    return "\n".join(lines)


def _strict_checks(deck_json: Any) -> list[ValidationIssue]:
    """Quality checks enabled by --strict.

    These are not schema violations but reduce presentation quality:
    small font sizes in the theme, missing notes on content slides,
    missing slide transitions, and full-bleed images without a contrast overlay.
    """
    issues: list[ValidationIssue] = []
    deck = deck_json.get("deck", deck_json)

    text_styles = deck.get("theme", {}).get("textStyles", {})
    for role, style in text_styles.items():
        if isinstance(style, dict) and isinstance(style.get("fontSize"), (int, float)):
            if style["fontSize"] < 20:
                issues.append(ValidationIssue(
                    f"deckJson.deck.theme.textStyles.{role}.fontSize",
                    f"is {style['fontSize']} — below 20 px may render unreadably small at 1920×1080",
                ))

    slide_n = 0
    for si, section in enumerate(deck.get("sections", [])):
        for li, slide in enumerate(section.get("slides", [])):
            slide_n += 1
            slide_path = f"deckJson.deck.sections.{si}.slides.{li}"
            objs = slide.get("objects", [])

            text_objs = [o for o in objs if o.get("type") == "text"]
            if text_objs and not slide.get("notes") and not slide.get("speakerNotes"):
                issues.append(ValidationIssue(
                    slide_path,
                    f"slide {slide_n} has {len(text_objs)} text object(s) but no notes or speakerNotes "
                    "(add presenter notes or remove --strict to silence)",
                ))

            if not slide.get("transitions"):
                issues.append(ValidationIssue(
                    f"{slide_path}.transitions",
                    f"slide {slide_n} has no transition — add {{\"effect\":\"fade\",\"durationMs\":400}}",
                ))

            for obj in objs:
                if (
                    obj.get("type") == "image"
                    and obj.get("width", 0) >= 1000
                    and obj.get("height", 0) >= 400
                    and obj.get("opacity", 1) >= 1.0
                ):
                    has_overlay = any(
                        o.get("type") == "shape" and o.get("opacity", 1) < 1.0
                        for o in objs
                    )
                    if not has_overlay:
                        oid = obj.get("id", "?")[:8]
                        issues.append(ValidationIssue(
                            f"{slide_path} obj:{oid}",
                            f"slide {slide_n} has a large image (opacity=1) with no semi-transparent shape "
                            "overlay — text placed on top may be unreadable",
                        ))

    return issues


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Validate a deck JSON.")
    parser.add_argument("--strict", action="store_true",
                        help="Run additional quality checks (notes, transitions, font sizes, overlays)")
    args, _ = parser.parse_known_args()

    raw = sys.stdin.read().strip()
    if not raw:
        print("Error: deckJson is empty.", file=sys.stderr)
        return 1
    try:
        deck_json = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: deckJson is not valid JSON: {e}", file=sys.stderr)
        return 1
    issues = validate_deck(deck_json)
    if args.strict:
        issues.extend(_strict_checks(deck_json))
    if issues:
        print(format_validation_errors(issues), file=sys.stderr)
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
