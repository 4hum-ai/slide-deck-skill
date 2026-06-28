#!/usr/bin/env python3
"""Generate 'The Slide Deck Agent Playbook' — a meta-deck about this skill.

Theme: Skill Blueprint — dark navy with electric purple primary and cyan accent.
Fonts: Space Grotesk display/heading, Inter body, JetBrains Mono code.

Demonstrates advanced skill features:
  - AI asset generation (generate_image, generate_video, generate_audio)
  - Per-slide narration tracks via patch_slide.py --add-narration-track
  - Deck-level background music via set_deck_music.py
  - All major object types: text, chart, table, diagram, frame, qr, latex, bullet_list
  - Mermaid workflow diagram
  - Code-style bullet lists

Deck ID: 48389dc0-9543-4622-817d-8c8fa7347845
Edit URL: https://deck.4hum.ai/app/decks/48389dc0-9543-4622-817d-8c8fa7347845/edit

Narration voice: George — Warm, Captivating Storyteller
  Voice ID: 2a30f00d-e001-40ce-9f14-cdc181b6efe5

To add narration + background music after saving:
  DECK_ID=<id>
  VOICE_ID=2a30f00d-e001-40ce-9f14-cdc181b6efe5

  # Per-slide narration (run for each slide index 0–8):
  python scripts/generate_audio.py "NARRATION TEXT" --voice-id $VOICE_ID | \\
    python scripts/patch_slide.py $DECK_ID <slide-index> --add-narration-track -

  # Deck-level background music (ambient audio looping at low volume):
  python scripts/generate_audio.py "AMBIENT TEXT" --voice-id $VOICE_ID | \\
    python scripts/set_deck_music.py $DECK_ID --add-track - --loop --volume 0.12 \\
    --name "Background ambience"
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
    frame,
    image,
    kpi_card,
    latex_text,
    line,
    numbered_list,
    qr_code,
    rich_text,
    section,
    shape,
    slide,
    table,
    text,
    title_chip,
    token,
)

# Cover hero — AI-generated abstract agent blueprint
COVER_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/df48d0c4-40fe-41f8-a3c3-7ca25d547695.png"


def build_deck() -> dict:
    theme = dark_tech_theme(
        overrides={
            "theme": {
                "name": "Skill Blueprint",
                "fonts": {
                    "display": "Space Grotesk",
                    "heading": "Space Grotesk",
                    "body": "Inter",
                    "mono": "JetBrains Mono",
                },
            },
            "colors": {
                "background": "#0d1117",
                "surface": "#161b22",
                "foreground": "#e6edf3",
                "mutedForeground": "#8b949e",
                "primary": "#7c3aed",
                "primaryForeground": "#ffffff",
                "accent": "#06b6d4",
                "accentForeground": "#0d1117",
                "border": "#30363d",
            },
        }
    )

    def white(content: str, weight: int = 400):
        return [{"kind": "span", "text": content, "style": {
            "color": token("primaryForeground"), "fontWeight": weight,
        }}]

    def cyan(content: str, weight: int = 700):
        return [{"kind": "span", "text": content, "style": {
            "color": token("accent"), "fontWeight": weight,
        }}]

    def purple(content: str, weight: int = 700):
        return [{"kind": "span", "text": content, "style": {
            "color": token("primary"), "fontWeight": weight,
        }}]

    # ------------------------------------------------ Slide 0: Cover
    cover = slide(
        [
            image(COVER_IMG, 0, 0, 1920, 1080, fit="cover"),
            shape(0, 0, 1920, 1080, "background", shape="rectangle", stroke_width=0, opacity=0.65),
            *title_chip("SLIDE DECK AGENT SKILL", 100, 80, 500),
            text("title", 100, 260, 1600, 300,
                 [{"kind": "block", "runs": white("The Slide Deck", 700)},
                  {"kind": "block", "runs": white("Agent Playbook", 700)}]),
            rich_text("subtitle", 104, 580, 1300, 90,
                      white("A complete guide to building beautiful, narrated slide decks "
                            "with AI agents — from first token to finished presentation.")),
            line(104, 710, 560, 4, stroke="accent", stroke_width=6),
            rich_text("caption", 104, 760, 1200, 46,
                      [{"kind": "span", "text": "Covers: asset generation · object types · "
                        "narration · background music · advanced patterns",
                        "style": {"color": token("mutedForeground")}}]),
        ],
        notes="This playbook covers the full lifecycle of building AI-generated slide decks: "
              "choosing themes, generating images/video/audio, all object types, "
              "per-slide narration, deck-level background music, and advanced patterns.",
        background={"kind": "solid", "color": token("background")},
        transitions={"effect": "zoom", "durationMs": 500},
    )

    # ------------------------------------------------ Slide 1: The Toolkit
    script_rows = [
        ["Script", "Purpose", "Output"],
        ["auth.py", "Authenticate and save credentials", "~/.open-academy/config.json"],
        ["save_deck.py", "Create a new deck from JSON", "deck_id + edit URL"],
        ["update_deck.py", "Replace entire deck JSON", "edit URL"],
        ["patch_slide.py", "Patch one slide + narration tracks", "edit URL"],
        ["merge_deck.py", "Merge partial JSON into existing deck", "edit URL"],
        ["generate_image.py", "AI image generation (Flux/SD3)", "{file_url}"],
        ["generate_video.py", "AI video generation (Wan/Sora/Veo)", "{file_url, duration_seconds}"],
        ["generate_audio.py", "TTS narration via ElevenLabs", "{audio_url, duration_ms}"],
        ["set_deck_music.py", "Background music / deck media tracks", "edit URL"],
        ["preview_deck.py", "Structural summary + render URLs", "stdout report"],
        ["deck_validator.py", "Schema validation before save", "PASS / error list"],
    ]
    toolkit = slide(
        [
            *title_chip("THE TOOLKIT", 92, 72, 280),
            text("heading", 100, 150, 1720, 72, "Twelve scripts cover the full deck lifecycle"),
            table(100, 260, 1720, 660, script_rows),
        ],
        notes="Twelve Python scripts cover the full lifecycle: auth, save, update, patch, merge, "
              "image/video/audio generation, background music, preview, and validation. "
              "All scripts read credentials from ~/.open-academy/config.json (set by auth.py).",
    )

    # ------------------------------------------------ Slide 2: The Workflow
    workflow_diagram = (
        "flowchart LR\n"
        "  A[\"1. Auth\"] --> B[\"2. Theme\"]\n"
        "  B --> C[\"3. Generate\\nAssets\"]\n"
        "  C --> D[\"4. Build\\ndeckJson\"]\n"
        "  D --> E[\"5. Validate\"]\n"
        "  E --> F[\"6. Save\\ndeck\"]\n"
        "  F --> G[\"7. Patch\\nSlides\"]\n"
        "  G --> H[\"8. Add\\nNarration\"]\n"
        "  H --> I[\"9. Add\\nMusic\"]\n"
        "  classDef setup fill:#161b22,stroke:#30363d,color:#8b949e;\n"
        "  classDef generate fill:#7c3aed,stroke:#7c3aed,color:#ffffff;\n"
        "  classDef save fill:#06b6d4,stroke:#06b6d4,color:#0d1117;\n"
        "  classDef audio fill:#10b981,stroke:#10b981,color:#ffffff;\n"
        "  class A,B setup;\n"
        "  class C,D,E generate;\n"
        "  class F,G save;\n"
        "  class H,I audio;"
    )
    workflow = slide(
        [
            *title_chip("THE WORKFLOW", 92, 72, 300),
            text("heading", 100, 150, 1720, 72, "Nine steps from idea to narrated presentation"),
            diagram(100, 260, 1720, 320, workflow_diagram),
            table(
                100, 620, 1720, 300,
                [
                    ["Phase", "Steps", "Key scripts"],
                    ["Setup", "Auth + theme selection", "auth.py"],
                    ["Generate", "Assets + JSON + validate", "generate_image/video/audio.py, deck_validator.py"],
                    ["Save", "Create deck + patch slides", "save_deck.py, patch_slide.py"],
                    ["Narrate", "Per-slide voice + background music", "generate_audio.py, set_deck_music.py"],
                ],
            ),
        ],
        notes="The workflow has four phases: Setup (auth + theme), Generate (AI assets + deckJson + "
              "validation), Save (create deck + patch slides), Narrate (per-slide voice + background "
              "music). The Mermaid diagram shows all nine steps in sequence.",
    )

    # ------------------------------------------------ Slide 3: Object Types
    object_types_data = {
        "categories": ["Text", "Media", "Data", "Layout", "Interactive"],
        "series": [{"name": "Object types per category", "values": [3, 5, 3, 4, 2],
                    "color": token("primary")}],
    }
    objects_slide = slide(
        [
            *title_chip("OBJECT TYPES", 92, 72, 300),
            text("heading", 100, 150, 1720, 72, "17 object types cover every presentation need"),
            chart(100, 260, 700, 380, **object_types_data, chart_type="bar"),
            table(
                840, 260, 980, 440,
                [
                    ["Category", "Types"],
                    ["Text", "text · rich_text · latex_text"],
                    ["Media", "image · video · audio · embed · frame"],
                    ["Data", "chart · table · diagram"],
                    ["Layout", "shape · line · qr_code · placeholder"],
                    ["Composite", "card · kpi_card · process_flow"],
                ],
            ),
            rich_text("body", 100, 680, 1720, 110,
                      [{"kind": "span", "text": "Rule:  ", "style": {
                          "color": token("accent"), "fontWeight": 700,
                      }},
                       {"kind": "span", "text": "Choose the type that matches the data structure, "
                        "not the visual output. A bar chart is more maintainable than a shaped image.",
                        "style": {"color": token("foreground")}}]),
            text("caption", 100, 940, 1720, 40,
                 "Composite helpers (card, kpi_card, etc.) expand to primitive objects — "
                 "inspect with preview_deck.py to see the resolved structure."),
        ],
        notes="17 object types cover text, media, data visualisation, layout, and interactive "
              "elements. Composite helpers like kpi_card() and process_flow() expand to primitives "
              "at save time. Choose type by data shape, not appearance.",
    )

    # ------------------------------------------------ Slide 4: AI Asset Generation
    generation_slide = slide(
        [
            *title_chip("AI ASSET GENERATION", 92, 72, 420),
            text("heading", 100, 150, 1720, 72, "Three generation scripts, three asset types"),
            table(
                100, 260, 1720, 340,
                [
                    ["Script", "API endpoint", "Providers", "Output"],
                    ["generate_image.py", "POST /api/media/generate-image", "Flux 1.1 Pro, SD3.5",
                     '{"file_url":"…"}'],
                    ["generate_video.py", "POST /api/media/generate-video",
                     "Qwen Wan, BytePlus, Sora 2, Veo 3", '{"file_url":"…","duration_seconds":N}'],
                    ["generate_audio.py", "POST /api/media/voices/:id/generate",
                     "ElevenLabs (20+ voices)", '{"audio_url":"…","duration_ms":N}'],
                ],
            ),
            bullet_list(
                [
                    "All scripts print JSON to stdout only — human-readable logs go to stderr.",
                    "Pipe directly: generate_audio.py output → patch_slide.py --add-narration-track -",
                    "Rate limits: image ~1 req/2s · video ~30s gap · audio: no stated limit.",
                    "Always use a static image as a poster/fallback behind every video object.",
                    "Use --default-voice for quick prototyping; --voice-id in production decks.",
                ],
                100, 640, 1720, 280, role="body",
            ),
        ],
        notes="Three generation scripts target different asset types: generate_image.py for static "
              "backgrounds and illustrations, generate_video.py for animated sequences, and "
              "generate_audio.py for TTS narration. All output pipe-friendly JSON to stdout.",
    )

    # ------------------------------------------------ Slide 5: Narration Tracks
    narration_diagram = (
        "flowchart LR\n"
        "  A[\"generate_audio.py\\n'Slide text…' --voice-id\"] --> B[\"stdout JSON\\n{audio_url, duration_ms}\"]\n"
        "  B --> C[\"patch_slide.py\\n--add-narration-track -\"]\n"
        "  C --> D[\"slide.narrationTracks[]\\n{id, kind, url, startMs, source:'tts'}\"]\n"
        "  classDef gen fill:#7c3aed,stroke:#7c3aed,color:#ffffff;\n"
        "  classDef data fill:#161b22,stroke:#30363d,color:#8b949e;\n"
        "  classDef write fill:#06b6d4,stroke:#06b6d4,color:#0d1117;\n"
        "  class A gen; class B data; class C write; class D data;"
    )
    narration_slide = slide(
        [
            *title_chip("PER-SLIDE NARRATION", 92, 72, 400),
            text("heading", 100, 150, 1720, 72, "One pipe command adds a voice track to any slide"),
            diagram(100, 260, 1720, 280, narration_diagram),
            table(
                100, 580, 1720, 300,
                [
                    ["NarrationTrack field", "Type", "Notes"],
                    ["kind", "audio | video", '"audio" for TTS; "video" for avatar overlays'],
                    ["url", "string", "MP3/WAV URL from generate_audio.py"],
                    ["startMs", "number", "0 = plays from slide start"],
                    ["durationMs", "number?", "From generate_audio.py output — auto-fills timeline"],
                    ["source", "tts | recorded", 'auto-set to "tts" by patch_slide.py'],
                    ["voiceId", "string?", "ElevenLabs voice UUID — enables cache/dedup"],
                ],
            ),
            text("caption", 100, 940, 1720, 40,
                 "patch_slide.py auto-converts generate_audio.py output → NarrationTrack. "
                 "No JSON reshaping needed."),
        ],
        notes="Per-slide narration is a single pipe command: generate_audio.py output flows directly "
              "to patch_slide.py via stdin. patch_slide auto-converts the audio JSON to a NarrationTrack "
              "with a generated UUID, kind='audio', startMs=0, source='tts'.",
    )

    # ------------------------------------------------ Slide 6: Background Music
    music_diagram = (
        "flowchart LR\n"
        "  A[\"generate_audio.py\\n'ambient text' --voice-id\"] --> B[\"stdout JSON\"]\n"
        "  B --> C[\"set_deck_music.py\\n--add-track - --loop --volume 0.12\"]\n"
        "  C --> D[\"deck.mediaTracks[]\\n{id, kind, url, loop:true, volume:0.12}\"]\n"
        "  E[\"--url 'https://music.mp3'\"] --> C\n"
        "  classDef gen fill:#7c3aed,stroke:#7c3aed,color:#ffffff;\n"
        "  classDef data fill:#161b22,stroke:#30363d,color:#8b949e;\n"
        "  classDef write fill:#06b6d4,stroke:#06b6d4,color:#0d1117;\n"
        "  classDef alt fill:#10b981,stroke:#10b981,color:#ffffff;\n"
        "  class A gen; class B,D data; class C write; class E alt;"
    )
    music_slide = slide(
        [
            *title_chip("BACKGROUND MUSIC", 92, 72, 380),
            text("heading", 100, 150, 1720, 72, "deck.mediaTracks[] plays across the full timeline"),
            diagram(100, 260, 1720, 280, music_diagram),
            table(
                100, 580, 920, 320,
                [
                    ["DeckMediaTrack field", "Purpose"],
                    ["url", "MP3/WAV/MP4 direct file URL"],
                    ["loop: true", "Loops to fill deck duration (music beds)"],
                    ["volume: 0.1–0.2", "Low mix under narration voice"],
                    ["startMs: 0", "Begins at deck start"],
                    ["name", "Label shown in timeline UI"],
                ],
            ),
            bullet_list(
                [
                    "Use --loop for music beds; omit for one-shot sound effects.",
                    "Volume 0.1–0.2 keeps music under narration voice.",
                    "Use --url for royalty-free music; pipe generate_audio.py for TTS ambient.",
                    "Multiple tracks stack in separate lanes — parallel playback.",
                    "Remove with --clear or --remove-track <id>.",
                ],
                1060, 580, 760, 320, role="body",
            ),
            text("caption", 100, 940, 1720, 40,
                 "set_deck_music.py --list shows all current deck mediaTracks. "
                 "Tracks persist as part of the deck JSON — same PUT endpoint as slides."),
        ],
        notes="Deck-level background music lives in deck.mediaTracks[]. set_deck_music.py adds, "
              "lists, or removes these tracks. For music beds: loop=true, volume=0.1-0.2. "
              "Multiple tracks stack in separate lanes for parallel playback.",
    )

    # ------------------------------------------------ Slide 7: Advanced Patterns
    latex_formula = r"\hat{H}|\psi\rangle = i\hbar\frac{\partial}{\partial t}|\psi\rangle"
    advanced_slide = slide(
        [
            *title_chip("ADVANCED PATTERNS", 92, 72, 380),
            text("heading", 100, 150, 1720, 72, "Frames, LaTeX, QR codes, and live diagrams"),
            # Left column: frame (device mockup with a purple placeholder rectangle simulating a screen)
            shape(100, 260, 560, 400, "surface", shape="rectangle", stroke_width=2),
            rich_text("caption", 100, 260, 560, 40,
                      [{"kind": "span", "text": "frame(frameKind='browser', src=static_img_url)",
                        "style": {"color": token("accent"), "fontWeight": 600}}]),
            shape(120, 310, 520, 330, "primary", shape="rectangle", stroke_width=0, opacity=0.15),
            rich_text("body", 200, 430, 360, 120,
                      [{"kind": "span", "text": "src must be a static image URL — not a live site. "
                        "Generate a screenshot with generate_image.py first.",
                        "style": {"color": token("mutedForeground")}}]),
            # Middle column: LaTeX
            shape(720, 260, 560, 180, "surface", shape="rectangle", stroke_width=2),
            rich_text("caption", 720, 260, 560, 40,
                      [{"kind": "span", "text": "latex_text(formula)",
                        "style": {"color": token("accent"), "fontWeight": 600}}]),
            latex_text(latex_formula, 740, 310, 520, 100),
            # Middle column: QR
            shape(720, 470, 560, 200, "surface", shape="rectangle", stroke_width=2),
            rich_text("caption", 720, 470, 560, 40,
                      [{"kind": "span", "text": "qr_code(url, x, y, size)",
                        "style": {"color": token("accent"), "fontWeight": 600}}]),
            qr_code("https://deck.4hum.ai", 860, 516, 140),
            # Right column: diagram
            shape(1340, 260, 380, 400, "surface", shape="rectangle", stroke_width=2),
            rich_text("caption", 1340, 260, 380, 40,
                      [{"kind": "span", "text": "diagram(source, engine='mermaid')",
                        "style": {"color": token("accent"), "fontWeight": 600}}]),
            diagram(1360, 310, 340, 330, "graph TD\n  A[Input] --> B[Process]\n  B --> C[Output]"),
            # Tips row
            line(100, 700, 1720, 3, stroke="border", stroke_width=2),
            bullet_list(
                [
                    "frame() — always use static image URL as src; generate_image.py creates perfect device screenshots.",
                    "latex_text() — renders via KaTeX; escape backslashes in Python with raw strings r'\\formula'.",
                    "diagram() — Mermaid source; classDef adds theme-matched colors via token() references.",
                ],
                100, 720, 1720, 200, role="body",
            ),
        ],
        notes="Three advanced object types: frame() for device mockups (browser/phone/laptop chrome), "
              "latex_text() for KaTeX math rendering, and diagram() for Mermaid diagrams. "
              "Frame src must be a static image, not a live URL. Use r-strings for LaTeX formulas.",
    )

    # ------------------------------------------------ Slide 8: What's Next
    roadmap_items = [
        {"title": "upload_media.py", "body": "Upload locally-generated images/audio/video to GCS and return a stable URL — enables local GPU pipelines."},
        {"title": "Music generation API", "body": "POST /api/media/generate-music endpoint (Udio/Suno integration) — so agents can create royalty-free score beds."},
        {"title": "Podcast export", "body": "POST /api/decks/:id/podcast — concatenates all slide narration tracks into a single MP3 with slide titles."},
        {"title": "Slide templates", "body": "A library of slide() templates (comparison, SWOT, timeline, org chart) as block_builder helpers."},
    ]
    roadmap_slide = slide(
        [
            *title_chip("WHAT'S NEXT", 92, 72, 280),
            text("heading", 100, 150, 1720, 72, "Four capabilities that unlock the next level"),
            *[
                obj
                for i, item in enumerate(roadmap_items)
                for obj in [
                    shape(
                        100 + (i % 2) * 860, 260 + (i // 2) * 330,
                        800, 290, "surface", shape="rectangle", stroke_width=2,
                    ),
                    rich_text("subtitle", 120 + (i % 2) * 860, 275 + (i // 2) * 330, 760, 52,
                              [{"kind": "span", "text": f"{i + 1:02d}  {item['title']}",
                                "style": {"color": token("accent"), "fontWeight": 700}}]),
                    rich_text("body", 120 + (i % 2) * 860, 335 + (i // 2) * 330, 760, 100,
                              [{"kind": "span", "text": item["body"],
                                "style": {"color": token("foreground")}}]),
                ]
            ],
            qr_code("https://deck.4hum.ai", 1640, 880, 180),
            rich_text("caption", 1600, 932, 260, 40,
                      [{"kind": "span", "text": "Explore the skill",
                        "style": {"color": token("mutedForeground")}}], text_align="center"),
        ],
        notes="Four capabilities on the roadmap: upload_media.py for local GPU pipelines, "
              "music generation API for royalty-free score beds, podcast export from narration tracks, "
              "and a template library of block_builder helpers for common slide patterns.",
        background={"kind": "solid", "color": token("background")},
        transitions={"effect": "fade", "durationMs": 400},
    )

    return deck(
        "The Slide Deck Agent Playbook",
        [
            section("Introduction", [cover, toolkit, workflow]),
            section("Core Capabilities", [objects_slide, generation_slide]),
            section("Audio & Narration", [narration_slide, music_slide]),
            section("Advanced & Roadmap", [advanced_slide, roadmap_slide]),
        ],
        theme=theme,
    )


if __name__ == "__main__":
    print(json.dumps(build_deck()))
