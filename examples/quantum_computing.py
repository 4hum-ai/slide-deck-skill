#!/usr/bin/env python3
"""Quantum Computing for Everyone — a 7-slide educational deck.

Exercises latex_text, frame(browser) + frame(phone) with static image src,
and a video object with a poster thumbnail. Dark futuristic quantum theme.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from block_builder import (  # noqa: E402
    bullet_list,
    dark_tech_theme,
    deck,
    diagram,
    frame,
    image,
    kpi_card,
    latex_text,
    line,
    qr_code,
    rich_text,
    section,
    shape,
    slide,
    text,
    title_chip,
    token,
    video,
)

# ---------------------------------------------------------------------------
# Generated, hosted image assets (created via scripts/generate_image.py)
# ---------------------------------------------------------------------------
HERO_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/cb01d4cf-d849-44fb-9df6-1c49b79463e6.png"
CIRCUIT_UI_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/0cd4df5c-00a9-4b42-bcd5-ca479a209df6.png"
PHONE_APP_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/9233ecca-32d4-4726-9000-f3ed3933bffb.png"
VIDEO_POSTER_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/d9ad85ec-20b5-4cdc-acfe-4d60facc6e50.png"

# Well-known public test MP4 (Big Buck Bunny) — direct file URL, no CORS auth.
VIDEO_SRC = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

# ---------------------------------------------------------------------------
# Theme — deep navy / indigo with a quantum-purple accent.
# ---------------------------------------------------------------------------
THEME = dark_tech_theme(
    overrides={
        "theme": {"name": "Quantum Nightfall"},
        "colors": {
            "background": "#0a0e27",
            "surface": "#161b3d",
            "foreground": "#eef0ff",
            "mutedForeground": "#9aa3d4",
            "primary": "#6d4aff",
            "primaryForeground": "#ffffff",
            "accent": "#b388ff",
            "accentForeground": "#0a0e27",
            "border": "#2c3470",
        },
    }
)

SOURCE = "Source: IBM Quantum · Nielsen & Chuang, Quantum Computation and Quantum Information (2010)"


def src_caption(text_str, x=80, width=1760):
    return text("caption", x, 940, width, 40, text_str, vertical_align="middle")


# ---------------------------------------------------------------------------
# Slide 1 — Cover
# ---------------------------------------------------------------------------
def slide_cover():
    objs = [
        image(HERO_IMG, 0, 0, 1920, 1080, fit="cover"),
        # Dark scrim so the title reads against the hero image.
        shape(0, 0, 1920, 1080, "background", stroke="background",
              stroke_width=0, corner_radius=0, opacity=0.55),
        *title_chip("AN INTRODUCTION", x=140, y=300, width=320),
        text(
            "title", 140, 380, 1500, 220,
            [
                {"kind": "block", "runs": [{"kind": "span", "text": "Quantum Computing",
                  "style": {"color": token("primaryForeground"), "fontWeight": 700}}]},
                {"kind": "block", "runs": [{"kind": "span", "text": "for Everyone",
                  "style": {"color": token("primaryForeground"), "fontWeight": 700}}]},
            ],
        ),
        rich_text(
            "subtitle", 144, 620, 1400, 80,
            [{"kind": "span",
              "text": "From qubits to entanglement — the ideas behind the "
                      "next computing revolution, explained simply.",
              "style": {"color": token("primaryForeground")}}],
        ),
    ]
    return slide(
        objs,
        notes="Welcome. Today we demystify quantum computing — no physics "
              "degree required. We'll build from the qubit up to entanglement.",
        speaker_notes="Set the tone: curiosity over intimidation. Audience is "
                      "general / non-specialist.",
    )


# ---------------------------------------------------------------------------
# Slide 2 — What makes a qubit different (bullets + KPI card)
# ---------------------------------------------------------------------------
def slide_qubit():
    objs = [
        *title_chip("THE QUBIT", x=92, y=74, width=240),
        text("heading", 80, 150, 1760, 80, "What makes a qubit different?"),
        line(80, 240, 360, 4, line="straight", stroke="accent", stroke_width=5),
        bullet_list(
            [
                "A classical bit is strictly 0 or 1 — one value at a time.",
                "A qubit holds a superposition of 0 and 1 at once.",
                "n qubits represent 2^n states simultaneously.",
                "Measurement collapses the qubit to a single outcome.",
                "Entangled qubits share state across any distance.",
            ],
            x=80, y=300, width=1100, height=520, role="body",
        ),
        # KPI card — speed comparison.
        *kpi_card("2^300", "states in just 300 qubits — more than atoms in the "
                  "observable universe", x=1240, y=300, w=600, h=300),
        shape(1240, 640, 600, 180, "surface", corner_radius=18),
        text(
            "body", 1276, 668, 528, 130,
            [
                {"kind": "block", "runs": [{"kind": "span", "text": "Why it matters",
                  "style": {"color": token("accent"), "fontWeight": 700}}]},
                {"kind": "block", "runs": [{"kind": "span",
                  "text": "Some problems — factoring, molecular simulation, "
                          "search — scale exponentially better.",
                  "style": {"color": token("foreground")}}]},
            ],
        ),
        src_caption(SOURCE),
    ]
    return slide(
        objs,
        notes="A bit is a coin lying flat: heads or tails. A qubit is the coin "
              "spinning — both at once, until it lands when you measure it. "
              "That parallelism is the whole game.",
        speaker_notes="Don't over-claim speed: quantum is faster only for "
                      "specific problem classes, not everything.",
    )


# ---------------------------------------------------------------------------
# Slide 3 — The math behind superposition (LATEX SLIDE)
# ---------------------------------------------------------------------------
def slide_latex():
    objs = [
        *title_chip("THE MATH", x=92, y=74, width=220),
        text("heading", 80, 150, 1760, 80, "The math behind superposition"),
        line(80, 240, 360, 4, line="straight", stroke="accent", stroke_width=5),
        # Primary state-vector equation.
        shape(240, 300, 1440, 200, "surface", corner_radius=24),
        latex_text(
            r"|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle",
            260, 320, 1400, 160, role="title",
        ),
        # Normalisation / probability-amplitude constraint.
        shape(240, 540, 1440, 160, "surface", corner_radius=24),
        latex_text(
            r"|\alpha|^2 + |\beta|^2 = 1",
            260, 560, 1400, 120, role="heading",
        ),
        bullet_list(
            [
                "alpha and beta are complex probability amplitudes.",
                "|alpha|^2 is the probability of measuring 0; |beta|^2 of measuring 1.",
                "The amplitudes must square-sum to 1 — total probability is conserved.",
                "Until measured, the qubit is genuinely both states at once.",
            ],
            x=240, y=730, width=1440, height=190, role="body",
        ),
        src_caption(SOURCE, x=240, width=1440),
    ]
    return slide(
        objs,
        notes="Don't fear the symbols. Psi is the qubit's state. Alpha and beta "
              "are weights — how much 0 and how much 1. Their squares are "
              "probabilities, and probabilities must add to one.",
        speaker_notes="KaTeX: |psi> = alpha|0> + beta|1>; |alpha|^2 + |beta|^2 = 1.",
    )


# ---------------------------------------------------------------------------
# Slide 4 — Quantum gates as transformations (Mermaid diagram)
# ---------------------------------------------------------------------------
def slide_gates():
    mermaid = (
        '%%{init: {"theme": "base", "themeVariables": {'
        '"primaryColor": "#161b3d", "primaryTextColor": "#eef0ff", '
        '"primaryBorderColor": "#6d4aff", "lineColor": "#b388ff", '
        '"secondaryColor": "#2c3470", "tertiaryColor": "#0a0e27", '
        '"fontSize": "20px"}}}%%\n'
        "flowchart LR\n"
        '  A["|0⟩ input"] --> B["Hadamard H<br/>create superposition"]\n'
        '  B --> C["CNOT<br/>entangle two qubits"]\n'
        '  C --> D["Measure<br/>collapse to 0 or 1"]\n'
        '  D --> E["Classical result"]'
    )
    objs = [
        *title_chip("GATES", x=92, y=74, width=200),
        text("heading", 80, 150, 1760, 80, "Quantum gates as transformations"),
        line(80, 240, 360, 4, line="straight", stroke="accent", stroke_width=5),
        diagram(80, 290, 1760, 470, mermaid),
        rich_text(
            "body", 80, 800, 1760, 110,
            [
                {"kind": "span", "text": "Gates are reversible rotations of the "
                 "state vector. ", "style": {"color": token("foreground")}},
                {"kind": "span", "text": "Hadamard ", "style": {"color": token("accent"), "fontWeight": 700}},
                {"kind": "span", "text": "builds superposition; ", "style": {"color": token("foreground")}},
                {"kind": "span", "text": "CNOT ", "style": {"color": token("accent"), "fontWeight": 700}},
                {"kind": "span", "text": "creates entanglement; ", "style": {"color": token("foreground")}},
                {"kind": "span", "text": "measurement ", "style": {"color": token("accent"), "fontWeight": 700}},
                {"kind": "span", "text": "is the only irreversible step.",
                 "style": {"color": token("foreground")}},
            ],
        ),
        src_caption(SOURCE),
    ]
    return slide(
        objs,
        notes="A quantum program is a circuit. Hadamard puts a qubit into "
              "superposition, CNOT entangles a pair, and measurement reads out "
              "a classical answer — that last step is where the magic collapses.",
        speaker_notes="Circuit order: H -> CNOT -> Measure. Only measurement is "
                      "irreversible.",
    )


# ---------------------------------------------------------------------------
# Slide 5 — Quantum circuit simulator (FRAME: browser)
# ---------------------------------------------------------------------------
def slide_simulator():
    objs = [
        *title_chip("HANDS-ON", x=92, y=74, width=240),
        text("heading", 80, 150, 880, 140, "Explore a quantum\ncircuit simulator"),
        line(80, 290, 360, 4, line="straight", stroke="accent", stroke_width=5),
        bullet_list(
            [
                "Drag gates onto qubit wires to build a circuit.",
                "Watch amplitudes update on the live waveform.",
                "Run shots and read the measurement histogram.",
                "No install — it runs in your browser.",
            ],
            x=80, y=350, width=860, height=420, role="body",
        ),
        # Browser frame with a STATIC IMAGE src (generated mockup, not a live URL).
        frame(
            x=1000, y=200, width=840, height=630,
            frame_kind="browser", src=CIRCUIT_UI_IMG, media_fit="cover",
            stroke="border", stroke_width=1,
        ),
        src_caption("Mockup of a browser-based circuit simulator (e.g. IBM "
                    "Quantum Composer). " + SOURCE),
    ]
    return slide(
        objs,
        notes="The best way to learn quantum is to play. Browser simulators let "
              "you drag gates onto wires and instantly see how the amplitudes "
              "and the measurement histogram change.",
        speaker_notes="Frame src is a generated static screenshot mockup, not a "
                      "live website (frame renders an image, not an iframe).",
    )


# ---------------------------------------------------------------------------
# Slide 6 — Quantum computing in your pocket (FRAME: phone)
# ---------------------------------------------------------------------------
def slide_phone():
    objs = [
        *title_chip("ON MOBILE", x=92, y=74, width=240),
        text("heading", 80, 150, 700, 130, "Quantum computing\nin your pocket"),
        line(80, 290, 360, 4, line="straight", stroke="accent", stroke_width=5),
        # Left panel bullets.
        shape(80, 300, 640, 520, "surface", corner_radius=18),
        text("body", 116, 326, 568, 44, "Visualize", text_align="left"),
        bullet_list(
            [
                "Bloch sphere shows a qubit's full state.",
                "Rotate the state vector with simple gestures.",
                "See superposition as a tilt, not a 0 or 1.",
            ],
            x=116, y=380, width=568, height=420, role="body",
        ),
        # Phone frame in the centre with a STATIC IMAGE src.
        frame(
            x=810, y=180, width=300, height=660,
            frame_kind="phone", src=PHONE_APP_IMG, media_fit="cover",
        ),
        # Right panel bullets.
        shape(1200, 300, 640, 520, "surface", corner_radius=18),
        text("body", 1236, 326, 568, 44, "Learn anywhere", text_align="left"),
        bullet_list(
            [
                "Bite-size lessons between gates and concepts.",
                "Run small circuits on real cloud quantum hardware.",
                "Share results and compare measurement outcomes.",
            ],
            x=1236, y=380, width=568, height=420, role="body",
        ),
        src_caption(SOURCE),
    ]
    return slide(
        objs,
        notes="You don't need a lab. Mobile apps put a Bloch sphere — the "
              "geometric picture of a single qubit — in your hand, and some can "
              "even queue small jobs on real cloud quantum hardware.",
        speaker_notes="Phone frame src is a generated static mockup image.",
    )


# ---------------------------------------------------------------------------
# Slide 7 — See entanglement in action (VIDEO + QR)
# ---------------------------------------------------------------------------
def slide_video():
    objs = [
        *title_chip("WATCH", x=92, y=74, width=200),
        text("heading", 80, 150, 1760, 80, "See entanglement in action"),
        line(80, 240, 360, 4, line="straight", stroke="accent", stroke_width=5),
        # Poster image laid behind the video so the slide stays visually complete
        # even where the <video> element can't fetch the file (headless preview).
        image(VIDEO_POSTER_IMG, 80, 300, 1380, 600, fit="cover"),
        video(
            VIDEO_SRC, 80, 300, 1380, 600,
            poster=VIDEO_POSTER_IMG, controls=True, muted=True, autoplay=False,
        ),
        # QR backing + code -> IBM Quantum.
        shape(1540, 540, 300, 320, "surface", corner_radius=18),
        qr_code("https://quantum.ibm.com", 1560, 560, size=260,
                foreground="#0a0e27", background="#ffffff", error_correction="H"),
        text("caption", 1540, 832, 300, 36, "Scan to start on IBM Quantum",
             text_align="center", vertical_align="middle"),
        src_caption("Demo clip is a placeholder. Run real experiments at "
                    "quantum.ibm.com. " + SOURCE),
    ]
    return slide(
        objs,
        notes="Entanglement is the strangest idea of all: two qubits sharing a "
              "single state, so measuring one instantly tells you about the "
              "other. Scan the code to start running your own experiments.",
        speaker_notes="Video src is a known-good public MP4; poster carries the "
                      "visual in headless previews. QR -> https://quantum.ibm.com.",
    )


def build():
    sections = [
        section("Quantum Computing for Everyone", [
            slide_cover(),
            slide_qubit(),
            slide_latex(),
            slide_gates(),
            slide_simulator(),
            slide_phone(),
            slide_video(),
        ]),
    ]
    return deck("Quantum Computing for Everyone", sections, theme=THEME)


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
