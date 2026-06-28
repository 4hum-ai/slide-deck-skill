#!/usr/bin/env python3
"""Generate the 'The Mathematics of Machine Learning' deck.

Dark, elegant, mathematical theme: deep near-black navy background, electric-blue
primary, lime/gold accent — a palette that makes KaTeX formulas feel at home.

This deck is a quality test of three object types specifically:
  - latex_text  (Slide 3: cross-entropy loss + gradient-descent update)
  - frame browser (Slide 5: live TensorFlow Playground)
  - frame phone  (Slide 6: Teachable Machine mobile mockup)
  - video        (Slide 7: closing explainer .mp4)

Contrast discipline (v1.14.0): cover text overlaps a full-bleed generated photo,
so it gets a semi-transparent dark scrim shape() AND explicit white rich_text
runs (primaryForeground == #ffffff) so dark text never lands on a dark photo.
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
    frame,
    grid,
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

# Generated, content-relevant cover image (scripts/generate_image.py)
COVER_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/8c2d12b0-a06f-4ecb-bccd-a10e380d38cd.png"

# Public-domain test mp4 (Elephants Dream — Blender open movie); stands in for the
# 3Blue1Brown explainer per the closing-slide spec (no YouTube embed).
VIDEO_SRC = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"


def white(content: str, weight: int = 400):
    # primaryForeground == #ffffff in this theme; token ref keeps the validator
    # happy while guaranteeing white text over the dark scrim on the hero slide.
    return [{"kind": "span", "text": content, "style": {"color": token("primaryForeground"), "fontWeight": weight}}]


def build_deck() -> dict:
    # --- Mathematical theme: deep navy/near-black bg, electric blue primary, lime accent
    theme = dark_tech_theme(
        overrides={
            "theme": {
                "name": "Mathematics of ML",
                "fonts": {"display": "Space Grotesk", "heading": "Space Grotesk", "body": "Inter", "mono": "JetBrains Mono"},
            },
            "colors": {
                "background": "#070a14",        # near-black deep navy
                "surface": "#121829",
                "foreground": "#eef2fb",
                "mutedForeground": "#8b97b3",
                "primary": "#2563eb",           # electric blue (AA-safe white-on-blue header)
                "primaryForeground": "#ffffff",
                "accent": "#c4f035",            # lime/electric chartreuse accent
                "accentForeground": "#070a14",
                "border": "#27304a",
            },
        }
    )

    # ----------------------------------------------------------------- Slide 1: Cover
    cover = slide(
        [
            image(COVER_IMG, 0, 0, 1920, 1080, fit="cover"),
            shape(0, 0, 1920, 1080, "background", shape="rectangle", stroke_width=0, opacity=0.62),
            *title_chip("THE MATHEMATICS OF MACHINE LEARNING", 100, 90, 620),
            text("title", 100, 320, 1560, 290,
                 [{"kind": "block", "runs": white("Every Model Is Just", 700)},
                  {"kind": "block", "runs": white("Math That Learns", 700)}]),
            rich_text("subtitle", 104, 640, 1320, 110,
                      white("Loss functions, gradients, and optimization — the equations that turn "
                            "raw data into predictions.")),
            line(104, 800, 660, 4, stroke="accent", stroke_width=6),
            rich_text("caption", 106, 840, 1200, 46,
                      [{"kind": "span", "text": "A visual tour of the calculus and statistics under the hood.",
                        "style": {"color": token("mutedForeground")}}]),
        ],
        notes="Machine learning is not magic — it is optimization over a loss surface. This deck "
              "walks through the core mathematics: the loss function we minimize, the gradient that "
              "tells us which way to step, and the learning dynamics that emerge.",
        speaker_notes="Cover. Hero is AI-generated (neural net, data streams, dark navy). Title is "
                      "explicit white over a 0.62 dark scrim.",
        background={"kind": "solid", "color": token("background")},
        transitions={"effect": "zoom", "durationMs": 500},
    )

    # ----------------------------------------------------------------- Slide 2: Why math matters (KPIs + chart)
    why = slide(
        [
            *title_chip("01 / WHY THE MATH MATTERS", 92, 72, 480),
            text("heading", 100, 150, 1720, 80, "More data, lower loss — the math is what scales"),
            *grid(
                [
                    lambda x, y, w, h: kpi_card("∇L", "The gradient drives every weight update", x, y, w, h),
                    lambda x, y, w, h: kpi_card("10^9+", "Parameters tuned by gradient descent in large models", x, y, w, h),
                    lambda x, y, w, h: kpi_card("1 goal", "Minimize a single scalar: the loss", x, y, w, h),
                ],
                cols=3, x=100, y=320, total_w=1720, total_h=210,
            ),
            chart(
                100, 575, 1720, 300,
                ["1k", "10k", "100k", "1M", "10M"],
                [{"name": "Model accuracy vs. training-set size (%)", "values": [62, 74, 83, 90, 94],
                  "color": token("primary")}],
                chart_type="line",
            ),
            text("caption", 100, 940, 1720, 40,
                 "Illustrative scaling curve: accuracy rises with data as the optimizer better minimizes empirical loss."),
        ],
        notes="The reason ML works at scale is mathematical: every prediction error is summarized as a "
              "single scalar loss, and the gradient of that loss tells the optimizer exactly how to "
              "adjust billions of parameters. More data gives a better estimate of the true loss "
              "surface, so accuracy climbs as data grows.",
        speaker_notes="KPIs frame the three pillars: the gradient, parameter count, and the single "
                      "scalar objective. Chart is an illustrative accuracy-vs-data scaling curve.",
    )

    # ----------------------------------------------------------------- Slide 3: Core loss & gradient (LaTeX)
    loss_formula = r"L(\theta) = -\frac{1}{n}\sum_{i=1}^{n}[y_i\log\hat{y}_i + (1-y_i)\log(1-\hat{y}_i)]"
    grad_formula = r"\theta \leftarrow \theta - \alpha \nabla_\theta L(\theta)"
    core = slide(
        [
            *title_chip("02 / THE CORE EQUATIONS", 92, 72, 420),
            text("heading", 100, 150, 1720, 72, "Two equations run the entire training loop"),
            # --- Loss: label above, then the formula box (w=700, h=120)
            text("subtitle", 100, 250, 1720, 44, "Binary cross-entropy loss — what we minimize"),
            latex_text(loss_formula, 100, 300, 700, 120, role="body", text_align="left"),
            # --- Gradient: label above, then the formula box (w=700, h=120)
            text("subtitle", 100, 470, 1720, 44, "Gradient-descent update — how we minimize it"),
            latex_text(grad_formula, 100, 520, 700, 120, role="body", text_align="left"),
            line(100, 680, 1720, 3, stroke="border", stroke_width=2),
            bullet_list(
                [
                    "Loss L(θ) measures how wrong the model is, averaged over n samples.",
                    "∇L is the slope of the loss surface at the current weights θ.",
                    "We step downhill: subtract α (learning rate) times the gradient.",
                    "Repeat until the gradient flattens — that is convergence.",
                ],
                100, 710, 1720, 220, role="body",
            ),
            text("caption", 100, 940, 1720, 40,
                 "Cross-entropy is the maximum-likelihood loss for Bernoulli outputs; gradient descent is first-order optimization."),
        ],
        notes="Two equations drive supervised learning. The binary cross-entropy loss scores how far "
              "predictions ŷ are from labels y. Its gradient ∇L points uphill on the loss surface, so "
              "we step in the opposite direction, scaled by the learning rate α. Iterating this update "
              "is gradient descent — the algorithm at the heart of almost all neural-net training.",
        speaker_notes="Two latex_text objects (w=700, h=120 each) with a subtitle label above each: "
                      "binary cross-entropy loss and the gradient-descent update rule.",
    )

    # ----------------------------------------------------------------- Slide 4: The learning curve (chart)
    epochs = ["0", "10", "20", "30", "40", "50", "60", "70"]
    curve = slide(
        [
            *title_chip("03 / LEARNING DYNAMICS", 92, 72, 420),
            text("heading", 100, 150, 1720, 72, "Watch validation loss to catch overfitting early"),
            chart(
                100, 280, 1080, 580,
                epochs,
                [
                    {"name": "Training loss", "values": [1.80, 0.95, 0.62, 0.44, 0.33, 0.26, 0.21, 0.18],
                     "color": token("primary")},
                    {"name": "Validation loss", "values": [1.82, 1.02, 0.74, 0.61, 0.58, 0.60, 0.66, 0.74],
                     "color": token("accent")},
                ],
                chart_type="line",
            ),
            bullet_list(
                [
                    "Both losses fall fast early — the model is learning signal.",
                    "Training loss keeps dropping toward zero.",
                    "Validation loss bottoms out, then rises: overfitting.",
                    "The gap between the curves is the generalization error.",
                    "Stop at the validation minimum (early stopping).",
                ],
                1220, 300, 600, 540, role="body",
            ),
            text("caption", 100, 940, 1720, 40,
                 "Illustrative train/validation loss over epochs — the classic overfitting signature."),
        ],
        notes="The learning curve tells the real story. Training loss falls monotonically toward zero "
              "as the model memorizes the data, but validation loss bottoms out and then climbs — that "
              "turning point is where overfitting begins. The widening gap between the two curves is "
              "the generalization error; early stopping halts training at the validation minimum.",
        speaker_notes="Train (blue) vs validation (lime) loss over 70 epochs. Validation bottoms "
                      "around epoch 30-40 then rises — the overfitting signature.",
    )

    # ----------------------------------------------------------------- Slide 5: Browser frame (TF Playground)
    playground = slide(
        [
            *title_chip("04 / SEE IT IN THE BROWSER", 92, 72, 460),
            text("heading", 100, 150, 820, 130, "Tune a neural net live in TensorFlow Playground"),
            bullet_list(
                [
                    "Drag features and layers; watch the decision boundary form.",
                    "The learning rate slider is α from our update rule.",
                    "Loss curves update live as the network trains.",
                    "Color shows each neuron's learned weight sign.",
                    "No code — pure intuition for backpropagation.",
                ],
                100, 340, 820, 460, role="body",
            ),
            line(100, 820, 700, 4, stroke="accent", stroke_width=5),
            rich_text("body", 100, 850, 820, 80,
                      [{"kind": "span", "text": "It is gradient descent you can watch happen.",
                        "style": {"color": token("foreground"), "fontWeight": 600}}]),
            # --- Browser frame (the object under test)
            frame(960, 200, 880, 700, frame_kind="browser",
                  src="https://playground.tensorflow.org", media_fit="cover"),
            text("caption", 960, 915, 880, 40,
                 "TensorFlow Playground — interactive neural net in the browser",
                 text_align="center"),
        ],
        notes="TensorFlow Playground is the best way to build intuition for what the equations do. You "
              "drag features and hidden layers, set the learning rate (our α), and watch the decision "
              "boundary and loss curves update in real time as gradient descent runs. It turns the "
              "abstract math into something you can see move.",
        speaker_notes="frame(frameKind='browser') at x=960 y=200 w=880 h=700, src TF Playground. "
                      "Bullets on the left explain what the playground shows. Caption below the frame.",
    )

    # ----------------------------------------------------------------- Slide 6: Phone frame (Mobile ML)
    mobile = slide(
        [
            *title_chip("05 / ML IN YOUR POCKET", 92, 72, 400),
            text("heading", 100, 150, 1720, 72, "The same math now trains models on a phone"),
            # Left context column: what it is
            text("subtitle", 100, 280, 540, 44, "What it is"),
            bullet_list(
                [
                    "Teachable Machine trains a classifier from your camera.",
                    "Examples in, a model out — no setup.",
                    "Transfer learning reuses pretrained features.",
                    "Runs entirely in the browser, even on mobile.",
                ],
                100, 340, 540, 460, role="body",
            ),
            # --- Phone frame (the object under test), centered
            frame(760, 150, 400, 700, frame_kind="phone",
                  src="https://teachablemachine.withgoogle.com", media_fit="cover"),
            # Right context column: why it matters
            text("subtitle", 1280, 280, 540, 44, "Why it matters"),
            bullet_list(
                [
                    "Lowers the barrier: anyone can build a model.",
                    "On-device inference keeps data private.",
                    "Same loss + gradient math, smaller footprint.",
                    "ML literacy spreads beyond researchers.",
                ],
                1280, 340, 540, 460, role="body",
            ),
            text("caption", 100, 940, 1720, 40,
                 "Teachable Machine (Google) — train and run a model entirely on a mobile device."),
        ],
        notes="The mathematics does not change when the device shrinks. Tools like Teachable Machine "
              "let anyone train an image, sound, or pose classifier directly from a phone camera, "
              "running the same loss-minimization in-browser via transfer learning. On-device inference "
              "keeps data private and spreads ML literacy far beyond research labs.",
        speaker_notes="frame(frameKind='phone') centered at x=760 y=150 w=400 h=700, src Teachable "
                      "Machine. Left column = what it is; right column = why it matters.",
    )

    # ----------------------------------------------------------------- Slide 7: Closing with video
    closing = slide(
        [
            *title_chip("KEEP LEARNING", 92, 72, 340),
            text("heading", 100, 200, 820, 130, "Watch the gradient descend"),
            rich_text("subtitle", 100, 350, 820, 80,
                      [{"kind": "span", "text": "From equations to animation — see learning as motion.",
                        "style": {"color": token("mutedForeground")}}]),
            bullet_list(
                [
                    "A neural net is a function approximator.",
                    "Training is descent on a loss surface.",
                    "Backprop is just the chain rule at scale.",
                ],
                100, 460, 820, 320, role="body",
            ),
            qr_code("https://playground.tensorflow.org", 100, 760, 200,
                    foreground="#ffffff", background="#070a14"),
            rich_text("caption", 320, 820, 480, 60,
                      [{"kind": "span", "text": "Scan to open TensorFlow Playground and try it yourself.",
                        "style": {"color": token("mutedForeground")}}]),
            # --- Video object (the object under test)
            video(VIDEO_SRC, 960, 200, 880, 500, controls=True, muted=False, autoplay=False),
            text("caption", 960, 715, 880, 40,
                 "3Blue1Brown: Neural Networks — visualizing learning",
                 text_align="center"),
        ],
        notes="To close, see the math in motion. The video visualizes how a network learns by descending "
              "its loss surface — exactly the gradient-descent update from slide 3, animated. Scan the "
              "QR to open TensorFlow Playground and run gradient descent yourself.",
        speaker_notes="video() object at x=960 y=200 w=880 h=500 (public-domain test mp4 stand-in for "
                      "the 3Blue1Brown explainer). Title + 3 bullets + QR on the left. Caption under video.",
        background={"kind": "solid", "color": token("background")},
        transitions={"effect": "fade", "durationMs": 400},
    )

    return deck(
        "The Mathematics of Machine Learning",
        [
            section("Foundations", [cover, why, core]),
            section("Dynamics & Tools", [curve, playground, mobile]),
            section("Synthesis", [closing]),
        ],
        theme=theme,
    )


if __name__ == "__main__":
    print(json.dumps(build_deck()))
