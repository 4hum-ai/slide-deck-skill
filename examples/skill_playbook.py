#!/usr/bin/env python3
"""
Skill Playbook -- A Field Guide
12-slide practitioner walkthrough of the slide-deck-skill.
Theme: Warm editorial -- cream / deep ink / signal orange / forest green
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from block_builder import (
    text, rich_text, shape, line, image, table, diagram,
    bullet_list, card, process_flow, grid,
    slide, section, deck, token,
)


def _ctext(role: str, x: float, y: float, w: float, h: float,
           lines: list[str], color: str, **opts) -> dict:
    """Colored multi-line text — splits lines into separate blocks so no span contains a newline."""
    blocks = [
        {"kind": "block", "runs": [{"kind": "span", "text": ln, "style": {"color": token(color)}}]}
        for ln in lines
    ]
    return text(role, x, y, w, h, blocks, **opts)

# ─── Assets ───────────────────────────────────────────────────────────────────
COVER_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/8a7f4028-5d94-4d66-8136-1043a0a8d808.png"
SPLIT_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/7308b8b6-21e7-470b-8472-8548554bad4e.png"


# ─── Theme ────────────────────────────────────────────────────────────────────
def field_guide_theme() -> dict:
    return {
        "id": str(uuid4()),
        "name": "Field Guide",
        "fonts": {
            "display": "Zilla Slab",
            "heading": "Nunito Sans",
            "body":    "Nunito Sans",
            "mono":    "JetBrains Mono",
        },
        "colors": {
            "background":        "#f7f3ec",
            "surface":           "#ede8de",
            "foreground":        "#1a1208",
            "mutedForeground":   "#7a6a52",
            "primary":           "#e8611a",
            "primaryForeground": "#ffffff",
            "accent":            "#2d6a4f",
            "accentForeground":  "#ffffff",
            "border":            "#d4c9b8",
            "success":           "#a3e635",  # bright lime -- used as code highlight on dark cards
            "warning":           "#f59e0b",  # amber warning
            "destructive":       "#dc2626",  # red for "avoid" labels
        },
        "textStyles": {
            "title":    {"fontFamily": "display", "fontSize": 72, "fontWeight": 700, "color": token("foreground")},
            "subtitle": {"fontFamily": "body",    "fontSize": 32, "fontWeight": 400, "color": token("mutedForeground")},
            "heading":  {"fontFamily": "heading", "fontSize": 48, "fontWeight": 700, "color": token("foreground")},
            "body":     {"fontFamily": "body",    "fontSize": 28, "fontWeight": 400, "color": token("foreground")},
            "caption":  {"fontFamily": "body",    "fontSize": 20, "fontWeight": 400, "color": token("mutedForeground")},
            "code":     {"fontFamily": "mono",    "fontSize": 20, "fontWeight": 400, "color": token("success")},
        },
    }


# ─── Helper: dark terminal card ───────────────────────────────────────────────
def dark_card(x: float, y: float, w: float, h: float,
              label: str | None = None,
              code: str | None = None) -> list[dict]:
    objects: list[dict] = [
        shape(x, y, w, h, "foreground", corner_radius=12, stroke="foreground", stroke_width=0),
    ]
    if label:
        objects.append(
            rich_text("caption", x + 20, y + 16, w - 40, 32,
                [{"kind": "span", "text": label,
                  "style": {"color": token("primary"), "fontWeight": 700}}])
        )
    if code:
        code_y = y + (56 if label else 24)
        code_h = h - (72 if label else 40)
        # Use plain text (string content) so multi-line code doesn't hit TextSpan newline restriction
        objects.append(
            text("code", x + 20, code_y, w - 40, code_h, code,
                 text_align="left", vertical_align="top")
        )
    return objects


# ─── Section 1: Start ─────────────────────────────────────────────────────────

def s_cover() -> dict:
    return slide([
        image(COVER_IMG, 0, 0, 1920, 1080),
        shape(0, 330, 1920, 750, "foreground", corner_radius=0, opacity=0.76,
              stroke="foreground", stroke_width=0),
        rich_text("caption", 100, 354, 360, 36,
            [{"kind": "span", "text": "FIELD GUIDE  ·  v1.19",
              "style": {"color": token("primary"), "fontWeight": 700}}]),
        shape(100, 404, 160, 6, "primary", corner_radius=3, stroke="primary", stroke_width=0),
        _ctext("title", 100, 420, 1720, 240,
               ["From Prompt", "to Presenter"], "primaryForeground",
               text_align="left", vertical_align="top"),
        _ctext("subtitle", 100, 674, 1060, 100,
               ["The practitioner's guide to building beautiful",
                "slide decks with Claude and the slide-deck-skill."],
               "border", text_align="left"),
        rich_text("caption", 100, 958, 1200, 40,
            [{"kind": "span",
              "text": "deck.4hum.ai  ·  slide-deck-skill  ·  Generated with claude-sonnet-4-6",
              "style": {"color": token("mutedForeground")}}]),
    ])


def s_quickstart() -> dict:
    commands = (
        "# 1. Authenticate once\n"
        "python scripts/auth.py\n\n"
        "# 2. Write a generator and save to the API\n"
        "python examples/my_deck.py | python scripts/save_deck.py 'My Deck Title'\n\n"
        "# 3. Inspect the saved deck (screenshots + structure)\n"
        "python scripts/preview_deck.py <deck-id>\n\n"
        "# 4. Patch a single slide -- no full rebuild needed\n"
        "echo '[{...}]' | python scripts/patch_slide.py <deck-id> 3\n\n"
        "# 5. Generate an AI image, use the returned URL as image.src\n"
        'python scripts/generate_image.py "city at golden hour" --size 1920x1080'
    )
    return slide([
        text("heading", 100, 82, 1400, 70, "Your First Deck in 5 Commands"),
        text("caption", 100, 162, 1400, 44,
             "Authenticate once. Write a generator. Save and preview. Live in under 2 minutes."),
        shape(80, 220, 1760, 798, "foreground", corner_radius=16, stroke="foreground", stroke_width=0),
        shape(116, 244, 16, 16, "primary", corner_radius=8, stroke="primary", stroke_width=0),
        shape(148, 244, 16, 16, "accent",  corner_radius=8, stroke="accent",  stroke_width=0),
        shape(180, 244, 16, 16, "border",  corner_radius=8, stroke="border",  stroke_width=0),
        text("code", 120, 278, 1680, 720, commands,
             text_align="left", vertical_align="top"),
    ], notes="Five commands, complete workflow. The API returns deck_id and an edit URL immediately. Iterate with patch_slide or merge_deck rather than full rebuilds.")


# ─── Section 2: Images ────────────────────────────────────────────────────────

def s_prompt_formula() -> dict:
    formula = (
        "flowchart LR\n"
        "  A[\"① Subject\\nBusy downtown street\"] --> "
        "B[\"② Style\\nCinematic photography\"] --> "
        "C[\"③ Lighting\\nGolden afternoon\"] --> "
        "D[\"④ Palette\\nAmber & slate-blue\"] --> "
        "E[\"⑤ Composition\\nRule of thirds\"]"
    )
    example = (
        '"Busy downtown street scene, cinematic wide-angle photography,\n'
        " golden afternoon light, warm amber and slate-blue palette,\n"
        ' rule-of-thirds composition, 8K, photorealistic"'
    )
    return slide([
        text("heading", 100, 82, 1720, 70, "The Prompt Formula That Always Works"),
        text("caption", 100, 160, 1600, 44, "Five parts. Stack them in order. Generate confidently."),
        diagram(80, 218, 1760, 440, formula),
        text("caption", 100, 676, 440, 36, "Assembled result:"),
        *dark_card(80, 716, 1760, 250, code=example),
        text("caption", 100, 982, 1720, 44,
             "Be specific in every part -- vague prompts return generic images. Use real place names, artist styles, exact lighting rigs."),
    ], notes="Subject + Style + Lighting + Palette + Composition. Each part narrows the model's search space. Specificity in any one part improves the whole output.")


def s_size_picker() -> dict:
    rows = [
        ["Slide zone",           "Best for",                      "Generate size",  "CLI flag"],
        ["Full-bleed hero",      "Cover, section header",         "1920 x 1080",    "--size 1920x1080"],
        ["Half panel (L or R)",  "Split-panel story slide",       "960 x 1080",     "--size 960x1080"],
        ["Portrait card",        "Speaker, character, product",   "720 x 900",      "--size 720x900"],
        ["Square thumbnail",     "Icon, logo, step marker",       "600 x 600",      "--size 600x600"],
        ["Wide accent strip",    "Textured banner, section bg",   "1920 x 400",     "--size 1920x400"],
    ]
    return slide([
        text("heading", 100, 82, 1400, 70, "Pick the Right Image Size"),
        text("caption", 100, 160, 1600, 44,
             "Match size to display region -- the renderer crops to fit, not stretches. Wrong size = quality loss."),
        table(80, 218, 1760, 720, rows),
        text("caption", 100, 952, 1720, 44,
             "Rate limit: ~1 req / 2 s. On a 429 error, wait 15 s and retry. Never generate in parallel -- calls queue poorly."),
    ], notes="Generating at exact display size avoids upscaling/downscaling quality loss. Always use --size explicitly.")


def s_image_gallery() -> dict:
    left_prompt = (
        '"A beautifully designed slide deck on a monitor in a sunlit studio,\n'
        " editorial photography, warm golden afternoon light, cream and\n"
        ' wood tones, shallow depth of field, Leica M11, film grain"\n'
        "--size 1920x1080"
    )
    right_prompt = (
        '"Split-panel: Python code on dark terminal (left), resulting\n'
        " slide on bright monitor (right), editorial composition,\n"
        ' warm studio lighting, cream and amber tones"\n'
        "--size 960x1080"
    )
    return slide([
        text("heading", 100, 82, 1720, 70, "What a Real Prompt Creates"),
        text("caption", 100, 160, 1720, 44,
             "These two images were generated by the prompts shown -- actual outputs from this session."),
        image(COVER_IMG, 80, 216, 860, 484),
        image(SPLIT_IMG, 980, 216, 860, 484),
        *dark_card(80,  712, 860, 300, label="HERO BACKGROUND  (1920x1080)", code=left_prompt),
        *dark_card(980, 712, 860, 300, label="SPLIT PANEL  (960x1080)",      code=right_prompt),
    ], notes="Generated in this session using generate_image.py. Left: editorial studio for a warm cover. Right: code-to-slide split panel for a demo slide.")


def s_prompt_templates() -> dict:
    t_hero = (
        "# Cover / section hero\n"
        '"[Subject], cinematic wide-angle shot,\n'
        " [dramatic | warm | moody] lighting,\n"
        " [primary color] and [accent color] palette,\n"
        ' rule-of-thirds, 8K, photorealistic"\n'
        "--size 1920x1080"
    )
    t_portrait = (
        "# Portrait / speaker card\n"
        '"[Name or description] professional portrait,\n'
        " [soft studio | warm conference | outdoor] lighting,\n"
        " shallow depth of field, [background color] bg,\n"
        ' editorial photography style"\n'
        "--size 720x900"
    )
    t_concept = (
        "# Abstract / concept\n"
        '"[Concept e.g. Quantum], glowing particles,\n'
        " network mesh, dark [indigo | navy | forest] bg,\n"
        " [neon color] accents, 3D render, futuristic,\n"
        ' cinematic depth of field"\n'
        "--size 1920x1080"
    )
    t_icon = (
        "# Icon / step marker\n"
        '"Minimal flat icon of [subject],\n'
        " clean vector style, [brand color] on white,\n"
        " simple geometric shapes, no gradients,\n"
        ' SVG illustration style"\n'
        "--size 600x600"
    )
    return slide([
        text("heading", 100, 82, 1400, 70, "4 Copy-Paste Prompt Templates"),
        text("caption", 100, 160, 1600, 44,
             "Replace the [bracketed] parts. Keep the rest -- the structure is proven."),
        *dark_card(80,  218, 860, 390, label="HERO BACKGROUND",         code=t_hero),
        *dark_card(980, 218, 860, 390, label="PORTRAIT / SPEAKER CARD", code=t_portrait),
        *dark_card(80,  626, 860, 390, label="ABSTRACT / CONCEPT",      code=t_concept),
        *dark_card(980, 626, 860, 390, label="ICON / STEP MARKER",      code=t_icon),
    ], notes="Four templates cover 90% of slide image needs. Keep structural keywords and swap the subject and colors.")


# ─── Section 3: Voice ─────────────────────────────────────────────────────────

def s_writing_for_voice() -> dict:
    rules = [
        "One idea per narration -- finish the thought before the slide transitions",
        "Conversational tempo -- write how you'd speak it, not how you'd type it",
        "Active voice -- 'Revenue grew 18%' beats 'An 18% growth was observed'",
        "Breath-length sentences -- if it takes more than 6 s to say, split it",
    ]
    return slide([
        text("heading", 100, 82, 1720, 70, "Writing Narration That Actually Works"),
        text("caption", 100, 160, 1600, 44,
             "TTS reads what you write. Four rules make the difference between robotic and natural."),
        bullet_list(rules, 100, 222, 1720, 360, role="body"),
        line(100, 596, 1720, 2, stroke="border"),
        shape(80,   618, 840, 230, "surface", corner_radius=12, stroke="border"),
        rich_text("caption", 100, 634, 320, 36,
            [{"kind": "span", "text": "AVOID",
              "style": {"color": token("destructive"), "fontWeight": 700}}]),
        text("body", 100, 678, 800, 156,
             "The following slide will present data regarding quarterly performance metrics across multiple business units."),
        shape(1000, 618, 840, 230, "surface", corner_radius=12, stroke="border"),
        rich_text("caption", 1020, 634, 320, 36,
            [{"kind": "span", "text": "WRITE THIS",
              "style": {"color": token("accent"), "fontWeight": 700}}]),
        text("body", 1020, 678, 800, 156,
             "Q3 hit its targets -- and three teams drove it. Here's what's behind the numbers."),
        text("caption", 100, 862, 1720, 44,
             "Rule of thumb: read it aloud before generating. If you stumble, the listener will too."),
        text("caption", 100, 940, 1720, 56,
             "Text limit: 8 000 chars per generate_audio.py call. For longer scripts, split across slides and generate separately."),
    ], notes="Short sentences, active voice, one idea per slide. Write the narration before designing the slide -- it forces clarity about what the slide's single claim actually is.")


def s_narration_pipeline() -> dict:
    pipe = (
        "flowchart LR\n"
        "  A[\"Write narration\\n(per-slide text)\"] --\"echo / heredoc\"--> "
        "B[\"generate_audio.py\\n--voice-id UUID\"] --\"pipe ( | )\"--> "
        "C[\"patch_slide.py\\nDECK_ID SLIDE_IDX\\n--add-narration-track -\"] --> "
        "D[\"NarrationTrack\\nattached to slide\"]"
    )
    cmd = (
        "# One command per slide -- pipe generate_audio into patch_slide:\n"
        "python scripts/generate_audio.py \"Revenue grew 18% -- here's what drove it.\" \\\n"
        "    --voice-id 2a30f00d-e001-40ce-9f14-cdc181b6efe5 \\\n"
        "  | python scripts/patch_slide.py $DECK_ID 2 --add-narration-track -\n\n"
        "# List available voices:\n"
        "python scripts/generate_audio.py --list-voices\n\n"
        "# Add deck-level background music:\n"
        "python scripts/set_deck_music.py $DECK_ID \\\n"
        "    --url \"https://your-cdn.com/ambient.mp3\" --loop --volume 0.12"
    )
    return slide([
        text("heading", 100, 82, 1720, 70, "The Narration Pipeline"),
        text("caption", 100, 160, 1600, 44,
             "One pipe command adds a synchronized narration track to any slide."),
        diagram(80, 218, 1760, 420, pipe),
        *dark_card(80, 650, 1760, 344, label="SHELL COMMANDS", code=cmd),
    ], notes="generate_audio.py outputs JSON to stdout. patch_slide.py reads it via stdin and auto-converts to a NarrationTrack. set_deck_music.py handles deck-level background audio.")


# ─── Section 4: Pro Patterns ──────────────────────────────────────────────────

def s_object_picker() -> dict:
    rows = [
        ["You have...",          "Use this object",          "Avoid"],
        ["Numbers / metrics",    "chart()",                  "table() -- charts show change visually"],
        ["A process / steps",    "diagram() -- Mermaid",     "process_flow() -- too many objects at 5+"],
        ["A/B comparison",       "comparison_columns()",     "two separate card() stacks"],
        ["Styled inline text",   "rich_text() with runs",    "text() -- can't style spans individually"],
        ["Code / commands",      "text(role='code')",        "bullet_list() -- loses monospace alignment"],
        ["Math equation",        "latex_text()",             "text() -- formula won't render as math"],
        ["Video content",        "video() + image() poster", "embed() -- YouTube blocks in iframes"],
    ]
    return slide([
        text("heading", 100, 82, 1400, 70, "Object Picker: Use the Right Tool"),
        text("caption", 100, 160, 1720, 44,
             "The wrong object type is the most common source of layout and rendering bugs."),
        table(80, 218, 1760, 730, rows),
        text("caption", 100, 962, 1720, 44,
             "When in doubt: fewer objects > more objects. bullet_list() is 1 object; 5x card() is 15."),
    ], notes="The Object Picker answers 'which object do I reach for?' The Avoid column is just as important as the Use column.")


def s_patch_dont_rebuild() -> dict:
    # Explicit 3-column layout (avoids process_flow animated arrows at canvas origin)
    card_w, card_h, card_y = 560, 480, 218
    gap = 30
    x1, x2, x3 = 80, 80 + card_w + gap, 80 + 2 * (card_w + gap)
    body1 = (
        "~800 tokens per call\n\n"
        "Change: one slide's objects,\nchart data, or copy.\n\n"
        "echo '[...]' |\n"
        "python scripts/patch_slide.py DECK 3"
    )
    body2 = (
        "~200 tokens per call\n\n"
        "Change: theme, deck title,\nor global settings.\n\n"
        'echo \'{"deck":{"title":"New"}}\' |\n'
        "python scripts/merge_deck.py DECK"
    )
    body3 = (
        "6 000-8 000 tokens\n\n"
        "Change: structure, new\nsections, new layout.\n\n"
        "python examples/my_deck.py |\n"
        "python scripts/save_deck.py 'T'"
    )
    return slide([
        text("heading", 100, 82, 1400, 70, "Patch, Don't Rebuild"),
        text("caption", 100, 160, 1720, 44,
             "Full regeneration costs 10x more tokens than a patch. Match the tool to the scope of the change."),
        *card(x1, card_y, card_w, card_h, "patch_slide.py", body1),
        *card(x2, card_y, card_w, card_h, "merge_deck.py", body2),
        *card(x3, card_y, card_w, card_h, "Full regeneration", body3),
        text("caption", 100, 720, 1720, 44,
             "If the change fits in one slide or one JSON fragment, patch or merge. Regenerate only when the structure changes."),
    ], notes="Token efficiency matters on long sessions. A 12-slide deck costs 6,000-8,000 tokens to regenerate. patch_slide reads only one section (~800 tokens) and writes just that slide back.")


def s_pitfalls() -> dict:
    rows = [
        ["Pitfall",                                 "Fix"],
        ["picsum.photos for content images",
         "Use generate_image.py -- random seeds may return wrong subject (food for 'lab', fashion for 'city')."],
        ["Literal font name in fontFamily",
         "Use the slot name: 'mono' not 'JetBrains Mono'. Validator rejects literal names."],
        ["Canvas overflow (x+width > 1920)",
         "Check x+width <= 1920, y+height <= 1080. Set autoFit:'shrink' to clip long text."],
        ["YouTube inside an embed object",
         "Use qr_code() pointing to the URL, or frame() with a static screenshot + play button shape."],
        ["Text invisible on a background image",
         "Add a scrim shape (opacity 0.55) between image and text, or use rich_text with color: primaryForeground."],
    ]
    return slide([
        text("heading", 100, 82, 1400, 70, "5 Pitfalls and How to Fix Them"),
        text("caption", 100, 160, 1720, 44,
             "These account for 80% of validator errors and rendering surprises."),
        table(80, 218, 1760, 730, rows),
        text("caption", 100, 962, 1720, 44,
             "Run  python scripts/preview_deck.py --theme-check  after every new theme -- WCAG contrast failures appear immediately."),
    ], notes="Common pitfalls in order: wrong image source, font family error, canvas overflow, broken embed, invisible text. The validator catches most before a network call.")


# ─── Section 5: Go Build ──────────────────────────────────────────────────────

def s_closing() -> dict:
    return slide(
        [
            rich_text("title", 100, 310, 1720, 210,
                [{"kind": "span", "text": "Now go build.",
                  "style": {"color": token("primaryForeground")}}],
                text_align="center", vertical_align="middle"),
            shape(820, 538, 280, 8, "primary", corner_radius=4, stroke="primary", stroke_width=0),
            rich_text("body", 100, 562, 1720, 70,
                [{"kind": "span", "text": "deck.4hum.ai  ·  examples/  ·  references/",
                  "style": {"color": token("primary")}}],
                text_align="center"),
            rich_text("caption", 100, 650, 1720, 60,
                [{"kind": "span", "text": "Copy an example, change the topic, run it. That's the whole workflow.",
                  "style": {"color": token("mutedForeground")}}],
                text_align="center"),
            rich_text("caption", 100, 940, 1720, 60,
                [{"kind": "span", "text": "slide-deck-skill  v1.19  ·  Maintained by 4hum.ai",
                  "style": {"color": token("mutedForeground")}}],
                text_align="center"),
        ],
        background={"kind": "solid", "color": token("foreground")},
    )


# ─── Assemble ─────────────────────────────────────────────────────────────────

def build() -> dict:
    return deck(
        "Slide Deck Skill -- A Field Guide",
        [
            section("Start",        [s_cover(), s_quickstart()]),
            section("Images",       [s_prompt_formula(), s_size_picker(),
                                     s_image_gallery(), s_prompt_templates()]),
            section("Voice",        [s_writing_for_voice(), s_narration_pipeline()]),
            section("Pro Patterns", [s_object_picker(), s_patch_dont_rebuild(), s_pitfalls()]),
            section("Go Build",     [s_closing()]),
        ],
        theme=field_guide_theme(),
    )


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
