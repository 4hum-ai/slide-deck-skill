#!/usr/bin/env python3
"""The Slide Deck Agent Playbook — practical guide to building great decks.

This deck is written for agents, not developers. Each slide delivers a specific,
actionable technique an agent can apply immediately. No API references — just
patterns, prompts, and decisions that produce better presentations.

Structure (5 sections, 12 slides):
  Section 1: Quick Start
    0. Cover
    1. Your First Deck in 5 Minutes
  Section 2: Mastering Images
    2. The Image Prompt Formula
    3. Size & Format Guide
    4. Prompt Gallery — 4 Visual Archetypes
    5. The Prompt Text: Copy-Paste Ready
  Section 3: Voice & Audio
    6. Writing Narration That Lands
    7. Voice Selection + Background Music
  Section 4: Choosing the Right Object
    8. Right Object, Right Data
  Section 5: Production Tips
    9. Patch vs Merge vs Regenerate
   10. 5 Pitfalls That Waste Time
   11. Closing

Theme: Blueprint (Space Grotesk, dark navy #0d1117, violet #6d28d9, amber #f59e0b)
Deck ID: aa73d17b-de26-4e83-90bc-2ef97011bd26
Edit URL: https://deck.4hum.ai/app/decks/aa73d17b-de26-4e83-90bc-2ef97011bd26/edit

Images used:
  COVER_IMG    — generated hero: dark navy abstract agent blueprint (1920x1080)
  PORTRAIT_IMG — generated: professional split-panel portrait (960x1080)
  CONCEPT_IMG  — generated: abstract glowing data network (1920x1080)
  NIGHT_IMG    — reused from urban_mobility_2030.py closing night city (1920x1080)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from block_builder import (  # noqa: E402
    bullet_list,
    chart,
    dark_tech_theme,
    deck,
    diagram,
    image,
    kpi_card,
    line,
    numbered_list,
    rich_text,
    section,
    shape,
    slide,
    table,
    text,
    title_chip,
    token,
)

COVER_IMG    = "https://storage.googleapis.com/open-academy-media/ai-images/df48d0c4-40fe-41f8-a3c3-7ca25d547695.png"
PORTRAIT_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/e4439828-17fe-4112-ba60-78a90c8420a4.png"
CONCEPT_IMG  = "https://storage.googleapis.com/open-academy-media/ai-images/5d693140-0a6d-4736-831a-cfdd5881ed61.png"
NIGHT_IMG    = "https://storage.googleapis.com/open-academy-media/ai-images/19b1d1c9-547c-4519-b144-44796526709a.png"


def build_deck() -> dict:
    theme = dark_tech_theme(
        overrides={
            "theme": {
                "name": "Playbook Blueprint",
                "fonts": {
                    "display": "Space Grotesk",
                    "heading": "Space Grotesk",
                    "body": "Inter",
                    "mono": "JetBrains Mono",
                },
            },
            "colors": {
                "background": "#0d1117",
                "surface":    "#161b22",
                "foreground": "#e6edf3",
                "mutedForeground": "#8b949e",
                "primary":    "#6d28d9",
                "primaryForeground": "#ffffff",
                "accent":     "#f59e0b",
                "accentForeground": "#0d1117",
                "border":     "#30363d",
            },
        }
    )

    def w(text_: str, weight: int = 400):
        return [{"kind": "span", "text": text_, "style": {
            "color": token("primaryForeground"), "fontWeight": weight,
        }}]

    def amber(text_: str, weight: int = 700):
        return [{"kind": "span", "text": text_, "style": {
            "color": token("accent"), "fontWeight": weight,
        }}]

    def muted(text_: str):
        return [{"kind": "span", "text": text_, "style": {"color": token("mutedForeground")}}]

    def label_chip(label: str, x: int, y: int, color: str = "accent") -> list:
        return [
            shape(x, y, len(label) * 11 + 32, 36, color, shape="rectangle",
                  stroke_width=0, opacity=1),
            rich_text("caption", x + 12, y + 6, len(label) * 11 + 8, 26,
                      [{"kind": "span", "text": label, "style": {
                          "color": token("accentForeground"), "fontWeight": 700,
                          "fontSize": 13,
                      }}]),
        ]

    # ───────────────────────── 0  COVER
    cover = slide(
        [
            image(COVER_IMG, 0, 0, 1920, 1080, fit="cover"),
            shape(0, 0, 1920, 1080, "background", shape="rectangle", stroke_width=0, opacity=0.62),
            *title_chip("THE AGENT PLAYBOOK", 100, 82, 440),
            text("title", 100, 270, 1600, 300,
                 [{"kind": "block", "runs": w("Slide Decks That", 700)},
                  {"kind": "block", "runs": w("Work First Time", 700)}]),
            rich_text("subtitle", 104, 580, 1280, 90,
                      w("Practical patterns for building beautiful, narrated presentations — "
                        "images, audio, object choices, and production shortcuts.")),
            line(104, 714, 480, 4, stroke="accent", stroke_width=6),
            rich_text("caption", 104, 760, 1100, 46,
                      muted("12 slides · 5 sections · every technique demonstrated live in this deck")),
        ],
        notes="This playbook is for agents building slide decks with the slide-deck-skill. "
              "It covers image prompting, format sizing, narration writing, voice selection, "
              "object choice, and production shortcuts — all demonstrated in this very deck.",
        background={"kind": "solid", "color": token("background")},
        transitions={"effect": "zoom", "durationMs": 500},
    )

    # ───────────────────────── 1  QUICK START
    quickstart = slide(
        [
            *title_chip("QUICK START", 100, 80, 280),
            text("heading", 100, 150, 1720, 70, "Your first deck in 5 minutes"),
            text("subtitle", 100, 232, 1500, 52,
                 "Copy these commands. Swap topic and theme. Everything else is defaults."),
            shape(100, 310, 1720, 560, "surface", shape="rectangle", stroke_width=1),
            numbered_list(
                [
                    "Authenticate once:  python scripts/auth.py",
                    "Generate a hero image:  python scripts/generate_image.py \"TOPIC, dramatic lighting, dark background\" --size 1920x1080  →  copy the file_url",
                    "Write your deck — one Python file. Use dark_tech_theme() and the HERO_IMG constant. "
                    "Follow urban_mobility_2030.py or quantum_computing.py as templates.",
                    "Validate before saving:  python my_deck.py | python scripts/deck_validator.py  (must print 'Validation passed')",
                    "Save:  python my_deck.py | python scripts/save_deck.py \"My Deck Title\"  →  copy the deck_id",
                    "Add narration one slide at a time:  python scripts/generate_audio.py \"Slide 0 narration.\" --default-voice | python scripts/patch_slide.py DECK_ID 0 --add-narration-track -",
                ],
                120, 330, 1680, 520, role="body",
            ),
            rich_text("caption", 100, 940, 1720, 40,
                      [*amber("Tip: "), *muted("Keep each step in a shell script named after your deck. "
                                               "You'll re-run steps 4–6 every time you iterate.")]),
        ],
        notes="The quickstart is six numbered steps: auth, generate image, write deck JSON, validate, "
              "save, add narration. The key habit: keep a shell script per deck so you can re-run "
              "the save+narrate cycle without re-typing commands.",
    )

    # ───────────────────────── 2  PROMPT FORMULA
    formula = slide(
        [
            *title_chip("SECTION 2 · MASTERING IMAGES", 100, 80, 540),
            text("heading", 100, 150, 1720, 70, "The Image Prompt Formula"),
            text("subtitle", 100, 232, 1500, 52,
                 "Five components. Use all five — vague prompts waste generation credits."),
            table(
                100, 310, 1720, 380,
                [
                    ["Component", "What it does", "Example values"],
                    ["Subject", "What is in the frame", "Scientist examining DNA, aerial city skyline, abstract data graph"],
                    ["Style / medium", "Visual treatment and realism level",
                     "cinematic photography, 3D render, flat illustration, editorial photo"],
                    ["Lighting", "Defines mood and depth",
                     "golden-hour, volumetric studio, dramatic side-light, soft overcast"],
                    ["Colour palette", "Ties image to your slide theme",
                     "deep navy and cyan, warm amber and white, monochrome with red accent"],
                    ["Composition", "How the camera frames the subject",
                     "wide shot, close-up, aerial, portrait, rule-of-thirds foreground"],
                ],
            ),
            shape(100, 720, 1720, 2, "border", shape="rectangle", stroke_width=0),
            rich_text("body", 100, 734, 1720, 60,
                      [*amber("Good: "),
                       *[{"kind": "span",
                          "text": '"Scientist examining glowing DNA strands in a modern lab, '
                                  'editorial photography, clean overhead lighting, cool blue and white, '
                                  'close-up with shallow depth of field"',
                          "style": {"color": token("foreground")}}]]),
            rich_text("body", 100, 806, 1720, 56,
                      [*amber("Avoid: "),
                       *[{"kind": "span",
                          "text": '"Show a DNA molecule" or "a scientist" — no style, no light, no palette, no composition.',
                          "style": {"color": token("mutedForeground")}}]]),
            text("caption", 100, 940, 1720, 40,
                 "Add 'no text, no watermarks, no logos' at the end if the model adds unwanted overlays."),
        ],
        notes="The five components of a great image prompt are subject, style/medium, lighting, "
              "colour palette, and composition. All five together give the model a clear mental "
              "picture; missing any one leads to generic output.",
    )

    # ───────────────────────── 3  SIZE GUIDE
    sizes = slide(
        [
            *title_chip("IMAGE SIZING", 100, 80, 300),
            text("heading", 100, 150, 1720, 70, "Generate at display size — never upscale"),
            text("subtitle", 100, 232, 1500, 52,
                 "Match --size to where the image actually appears. Wrong size = soft edges or letterboxing."),
            table(
                100, 310, 1060, 540,
                [
                    ["Slide use case", "Display region", "--size flag"],
                    ["Full-bleed background (hero, cover, closing)", "1920 × 1080", "1920x1080"],
                    ["Left or right split panel", "960 × 1080", "960x1080"],
                    ["Portrait card (speaker / profile)", "720 × 900 px area", "720x900"],
                    ["Square icon / thumbnail", "≤ 300 × 300", "600x600"],
                    ["Wide banner / accent strip", "1920 × 400", "1920x400"],
                    ["Section divider background", "1920 × 540", "1920x540"],
                ],
            ),
            bullet_list(
                [
                    "Always use fit='cover' on full-bleed and split-panel images — it crops to fill without stretching.",
                    "For portraits: generate at 720x900 (4:5) and display inside a 600×800 card — room to reposition.",
                    "Do not use picsum.photos for content images. Seeds are random — a 'lab' prompt may return a boutique photo.",
                    "Rate limit: allow 2 s between calls. On a 429, wait 15 s then retry.",
                ],
                1200, 310, 620, 540, role="body",
            ),
            rich_text("caption", 100, 940, 1720, 40,
                      [*amber("Rule: "),
                       *muted("One generate_image.py call per slide position. Never reuse a hero image as a "
                               "split panel — the aspect ratio will not match.")]),
        ],
        notes="Generate images at the exact display size. A 1920x1080 hero forced into a 960-wide "
              "split panel loses resolution and crops badly. Always pair image() with fit='cover' "
              "for full-bleed and split-panel positions. Never use picsum for content-relevant images.",
    )

    # ───────────────────────── 4  PROMPT GALLERY — VISUAL
    gallery_visual = slide(
        [
            *title_chip("PROMPT GALLERY", 100, 80, 320),
            text("heading", 100, 150, 1720, 70, "Four archetypes — generated images shown below"),
            # ── TL: Cover / Hero  (full-bleed dark concept image)
            image(COVER_IMG, 80, 250, 840, 360, fit="cover"),
            *label_chip("HERO / COVER", 100, 268),
            # ── TR: Split panel portrait
            image(PORTRAIT_IMG, 1000, 250, 840, 360, fit="cover"),
            *label_chip("SPLIT PANEL · PORTRAIT", 1020, 268),
            # ── BL: Data / concept
            image(CONCEPT_IMG, 80, 640, 840, 360, fit="cover"),
            *label_chip("DATA CONCEPT", 100, 658),
            # ── BR: Night / closing CTA
            image(NIGHT_IMG, 1000, 640, 840, 360, fit="cover"),
            *label_chip("CLOSING / CTA", 1020, 658),
        ],
        notes="Four visual archetypes: hero/cover (dramatic dark wide shot), split-panel portrait "
              "(person + shallow depth of field), data concept (abstract glowing network), "
              "and closing/CTA (night city aerial). Each is generated at the correct --size "
              "for its position. The prompts are on the next slide.",
    )

    # ───────────────────────── 5  PROMPT GALLERY — TEXT
    gallery_text = slide(
        [
            *title_chip("THE PROMPTS", 100, 80, 280),
            text("heading", 100, 150, 1720, 70, "Copy-paste ready — swap the subject, keep the structure"),
            # Hero
            shape(100, 250, 1720, 170, "surface", shape="rectangle", stroke_width=1),
            rich_text("subtitle", 120, 265, 400, 40, amber("Hero / Cover  ·  --size 1920x1080")),
            rich_text("body", 120, 308, 1680, 100,
                      [{"kind": "span",
                        "text": '"[TOPIC/SUBJECT], dramatic wide-angle view, cinematic photography, '
                                'volumetric [COLOR]-[COLOR2] light, dark moody background, '
                                '16:9 panoramic composition, no text no watermarks"',
                        "style": {"color": token("foreground"), "fontFamily": "mono", "fontSize": 14}}]),
            # Split panel
            shape(100, 440, 1720, 170, "surface", shape="rectangle", stroke_width=1),
            rich_text("subtitle", 120, 455, 500, 40, amber("Split Panel · Portrait  ·  --size 960x1080")),
            rich_text("body", 120, 498, 1680, 100,
                      [{"kind": "span",
                        "text": '"[PERSON / ROLE] in [SETTING], professional editorial photography, '
                                'clean studio lighting, shallow depth of field, neutral [COLOR] tones, '
                                'portrait orientation, no text"',
                        "style": {"color": token("foreground"), "fontFamily": "mono", "fontSize": 14}}]),
            # Data concept
            shape(100, 630, 1720, 170, "surface", shape="rectangle", stroke_width=1),
            rich_text("subtitle", 120, 645, 500, 40, amber("Data Concept  ·  --size 1920x1080")),
            rich_text("body", 120, 688, 1680, 100,
                      [{"kind": "span",
                        "text": '"Abstract [CONCEPT] visualization, glowing [COLOR] nodes and connections, '
                                'dark navy background, particle field, wide cinematic 16:9, '
                                'data visualization aesthetic, no text"',
                        "style": {"color": token("foreground"), "fontFamily": "mono", "fontSize": 14}}]),
            # Closing
            shape(100, 820, 1720, 100, "surface", shape="rectangle", stroke_width=1),
            rich_text("subtitle", 120, 835, 500, 40, amber("Closing / CTA  ·  --size 1920x1080")),
            rich_text("body", 120, 868, 1680, 46,
                      [{"kind": "span",
                        "text": '"Aerial view of [CITY/SETTING] at night, golden light trails, deep indigo sky, cinematic, no text"',
                        "style": {"color": token("foreground"), "fontFamily": "mono", "fontSize": 14}}]),
        ],
        notes="Four copy-paste prompt templates. Replace the bracketed placeholders with your topic. "
              "The structure — subject, style, lighting, palette, composition — stays constant. "
              "Always append 'no text no watermarks' to avoid unwanted overlays.",
    )

    # ───────────────────────── 6  WRITING NARRATION
    narration_tips = slide(
        [
            *title_chip("SECTION 3 · VOICE & AUDIO", 100, 80, 500),
            text("heading", 100, 150, 1720, 70, "Writing Narration That Lands"),
            text("subtitle", 100, 232, 1500, 52,
                 "Narration adds the voice. The slide has the visual. They should not repeat each other."),
            table(
                100, 310, 1720, 300,
                [
                    ["Rule", "Why it matters", "Example"],
                    ["Write for ears, not eyes",
                     "Listeners can't re-read — be linear and direct",
                     "Say 'The chart shows a 30% drop' not 'As shown above'"],
                    ["15–25 seconds per slide",
                     "~40–70 words. Long enough to explain, short enough to hold attention",
                     "Count words before generating — 60 words ≈ 20 s at normal pace"],
                    ["Lead with the insight",
                     "Listeners tune out during build-up",
                     "Start with 'Congestion costs $166 billion a year' not 'Let's look at congestion'"],
                    ["Don't read the slide",
                     "If narration echoes every bullet, it feels like a slideshow from 1998",
                     "Add context, backstory, or implication the slide doesn't show"],
                ],
            ),
            bullet_list(
                [
                    "Use 'we' and 'you' — conversational tone keeps listeners engaged.",
                    "Avoid bullet-list sentence structure in narration — write in flowing prose.",
                    "Test by reading aloud before generating — if you stumble, rewrite it.",
                    "Speed 0.85–0.9 for educational content; 1.0 for pitch/sales; 1.1 for upbeat summaries.",
                ],
                100, 640, 1720, 280, role="body",
            ),
            text("caption", 100, 940, 1720, 40,
                 "Pipe narration directly: generate_audio.py 'text' --voice-id ID | patch_slide.py DECK 0 --add-narration-track -"),
        ],
        notes="Great narration adds context the slide doesn't show. Lead with the insight, "
              "keep it to 15-25 seconds, write flowing prose not bullet-list sentences, "
              "and never repeat what's already visible on screen.",
    )

    # ───────────────────────── 7  VOICE SELECTION + MUSIC
    voice_music = slide(
        [
            *title_chip("VOICE + BACKGROUND MUSIC", 100, 80, 480),
            text("heading", 100, 150, 1720, 70, "Match the voice to the deck's emotional register"),
            table(
                100, 250, 1060, 360,
                [
                    ["Voice (English)", "Personality", "Best for"],
                    ["George", "Warm, captivating storyteller", "Educational, documentary, keynote"],
                    ["Sarah", "Mature, reassuring, confident", "Corporate, investor, professional"],
                    ["Charlie", "Deep, confident, energetic", "Sales, product launch, promo"],
                    ["Alice", "Clear, engaging educator", "Training, explainer, onboarding"],
                    ["River", "Relaxed, neutral, informative", "Background ambient, voiceover bed"],
                    ["Bill", "Wise, mature, balanced", "Thought leadership, strategy, exec brief"],
                ],
            ),
            shape(1160, 250, 660, 360, "surface", shape="rectangle", stroke_width=1),
            rich_text("subtitle", 1178, 265, 620, 40, amber("Background Music Tips")),
            bullet_list(
                [
                    "Volume 0.1–0.2 keeps music under the narrator.",
                    "Use --loop for beds that fill the full deck.",
                    "Use River or a slow-paced TTS for ambient voice beds.",
                    "Real music: pass any royalty-free MP3 URL via --url.",
                    "Remove with: set_deck_music.py DECK_ID --clear",
                ],
                1178, 315, 620, 280, role="body",
            ),
            line(100, 640, 1720, 2, stroke="border", stroke_width=2),
            rich_text("body", 100, 660, 1720, 60,
                      [*amber("Tip: "),
                       *[{"kind": "span",
                          "text": "Run --list-voices first, copy the voice id you want, "
                                  "then use --voice-id consistently across all slides. "
                                  "Using --default-voice is fine for prototyping but may change "
                                  "between runs if voices are reordered.",
                          "style": {"color": token("foreground")}}]]),
            text("caption", 100, 780, 1720, 40,
                 "Generate: python scripts/generate_audio.py --list-voices   →   copy the 'id' field"),
            text("caption", 100, 830, 1720, 40,
                 "Add music: python scripts/set_deck_music.py DECK_ID --url 'https://…/music.mp3' --loop --volume 0.15"),
        ],
        notes="Match the voice to the deck's emotional register. George for storytelling, "
              "Sarah for corporate confidence, Charlie for energy. Background music sits at "
              "0.1-0.2 volume, loops=true, using any direct MP3 URL. Use --list-voices to "
              "find voice IDs before starting a long narration session.",
    )

    # ───────────────────────── 8  RIGHT OBJECT RIGHT DATA
    object_choice = slide(
        [
            *title_chip("SECTION 4 · OBJECT MASTERY", 100, 80, 480),
            text("heading", 100, 150, 1720, 70, "Right Object, Right Data"),
            text("subtitle", 100, 232, 1500, 52, "Every object type has a data shape it's designed for. Pick wrong and the audience works harder."),
            table(
                100, 310, 1720, 560,
                [
                    ["If your data is…", "Use…", "Not…", "Because…"],
                    ["Numbers that need comparison",
                     "chart(chart_type='bar')",
                     "table()",
                     "Bars pre-compute the comparison visually"],
                    ["Items with 3+ attributes each",
                     "table()",
                     "bullet_list()",
                     "Tables align attributes across rows; bullets can't"],
                    ["A sequence of steps",
                     "numbered_list() or process_flow()",
                     "bullet_list()",
                     "Numbering signals order; bullets signal equivalence"],
                    ["A single headline stat",
                     "kpi_card()",
                     "text() at large font",
                     "kpi_card() adds label and context — text() alone lacks hierarchy"],
                    ["Relationships between nodes",
                     "diagram() with Mermaid",
                     "bullet_list()",
                     "Spatial layout makes topology readable; bullets flatten it"],
                    ["3–5 key points with no order",
                     "bullet_list()",
                     "chart() or table()",
                     "Bullets are the lightest container for unstructured text"],
                    ["One big concept, visual reinforcement",
                     "image() or video()",
                     "text() alone",
                     "A photo or clip replaces a hundred words when subject = visual"],
                ],
            ),
            text("caption", 100, 940, 1720, 40,
                 "Max 10 objects per slide. If you need more, split into two slides with a shared heading."),
        ],
        notes="Object choice is a data-structure decision. Charts pre-compute comparisons visually. "
              "Tables align multi-attribute items. Numbered lists signal sequence. kpi_card adds "
              "the label and context that raw text lacks. Diagrams make topology readable. "
              "Max 10 objects per slide — if you need more, split the slide.",
    )

    # ───────────────────────── 9  PATCH vs MERGE vs REGENERATE
    iteration = slide(
        [
            *title_chip("SECTION 5 · PRODUCTION", 100, 80, 340),
            text("heading", 100, 150, 1720, 70, "Patch, Merge, or Regenerate?"),
            text("subtitle", 100, 232, 1500, 52, "Three tools for three kinds of change. Using the wrong one wastes time and credits."),
            table(
                100, 310, 1720, 340,
                [
                    ["Script", "When to use it", "What it touches", "Speed"],
                    ["patch_slide.py", "Fix 1–2 slides: wrong text, bad objects, add narration",
                     "One slide's objects or notes field",  "~3 s"],
                    ["merge_deck.py", "Change theme, title, or a shared property across all slides",
                     "Deck-level fields: title, theme, transitions",  "~4 s"],
                    ["update_deck.py", "Rewrite 3+ slides or restructure sections",
                     "Entire deckJson replaced",  "~5 s"],
                    ["save_deck.py", "Brand-new deck from scratch",
                     "Creates new deck_id",  "~5 s"],
                ],
            ),
            line(100, 680, 1720, 2, stroke="border", stroke_width=2),
            rich_text("body", 100, 698, 1720, 60,
                      [*amber("Decision rule: "),
                       *[{"kind": "span",
                          "text": "1–2 slides broken → patch_slide. Theme looks wrong → merge_deck. "
                                  "More than 3 slides need changing → regenerate the whole file and update_deck. "
                                  "Never hand-edit the saved JSON — always regenerate from the Python source.",
                          "style": {"color": token("foreground")}}]]),
            bullet_list(
                [
                    "Keep your generator .py file as the source of truth — the saved deck is a build artifact.",
                    "After patch_slide, run preview_deck.py to confirm the structure is still valid.",
                    "Use merge_deck.py to swap themes when a client wants a different colour palette.",
                ],
                100, 778, 1720, 152, role="body",
            ),
        ],
        notes="Three tools for three kinds of change. patch_slide for 1-2 slides. merge_deck for "
              "theme and deck-level properties. update_deck when 3+ slides change. "
              "The key discipline: keep the Python generator as source of truth and treat "
              "the saved deckJson as a build artifact.",
    )

    # ───────────────────────── 10  5 PITFALLS
    pitfalls = slide(
        [
            *title_chip("5 PITFALLS & FIXES", 100, 80, 360),
            text("heading", 100, 150, 1720, 70, "Mistakes that cost time — and how to avoid them"),
            table(
                100, 250, 1720, 620,
                [
                    ["Pitfall", "Symptom", "Fix"],
                    ["Live URL in frame(src=…)",
                     "Device bezel appears but content area is blank",
                     "Generate a screenshot with generate_image.py and use that PNG as src"],
                    ["No poster image behind video()",
                     "Slides show a red error box in screenshots and previews",
                     "Add image(poster_url, …) at same x/y/w/h before the video() object"],
                    ["Using picsum.photos for content images",
                     "A 'genomics lab' slide shows a fashion boutique photo",
                     "Use generate_image.py with a specific subject prompt"],
                    ["Object count > 12 per slide",
                     "Validator passes but slide looks cluttered; render is slow",
                     "Split content across two slides; use bullet_list() to group items"],
                    ["Narration repeats the slide text verbatim",
                     "Listener feels lectured at; attention drops",
                     "Write narration to ADD context, not echo bullets. One paragraph, flowing prose."],
                ],
            ),
            rich_text("caption", 100, 940, 1720, 40,
                      [*amber("Bonus: "),
                       *muted("run  python my_deck.py | python scripts/deck_validator.py  before every save. "
                               "It catches missing ids, bad token refs, and out-of-canvas objects.")]),
        ],
        notes="Five pitfalls: live URL in frame (fix: static image), no poster behind video "
              "(fix: image layer), picsum for content (fix: generate_image.py), too many objects "
              "(fix: split slide), narration echoes slide (fix: add context not bullets). "
              "Run deck_validator.py before every save.",
    )

    # ───────────────────────── 11  CLOSING
    closing = slide(
        [
            image(NIGHT_IMG, 0, 0, 1920, 1080, fit="cover"),
            shape(0, 0, 1920, 1080, "background", shape="rectangle", stroke_width=0, opacity=0.62),
            *title_chip("READY TO BUILD", 100, 80, 340),
            rich_text("title", 100, 250, 1500, 200, w("Every great deck", 700)),
            rich_text("title", 100, 430, 1400, 90,
                      [{"kind": "span", "text": "starts with one good prompt.",
                        "style": {"color": token("accent"), "fontWeight": 700}}]),
            bullet_list(
                [
                    "Use the 5-part prompt formula — subject, style, lighting, palette, composition.",
                    "Generate images at display size — never upscale.",
                    "Write narration to add context, not echo the slide.",
                    "Match your voice to the deck's emotional register.",
                    "patch_slide for small fixes; regenerate when 3+ slides change.",
                ],
                100, 550, 1400, 330, role="body",
            ),
            rich_text("caption", 100, 940, 1200, 40,
                      muted("examples/  ·  urban_mobility_2030.py  ·  quantum_computing.py  "
                            "·  agent_skills_marketplace.py  ·  renewable_transition.py")),
        ],
        notes="Five takeaways: the prompt formula, size-matching, narration discipline, voice "
              "matching, and the patch-vs-regenerate decision. The examples folder has four "
              "working decks to learn from.",
        background={"kind": "solid", "color": token("background")},
        transitions={"effect": "fade", "durationMs": 400},
    )

    return deck(
        "The Slide Deck Agent Playbook",
        [
            section("Quick Start", [cover, quickstart]),
            section("Mastering Images", [formula, sizes, gallery_visual, gallery_text]),
            section("Voice & Audio", [narration_tips, voice_music]),
            section("Object Mastery", [object_choice]),
            section("Production Tips", [iteration, pitfalls, closing]),
        ],
        theme=theme,
    )


if __name__ == "__main__":
    print(json.dumps(build_deck()))
