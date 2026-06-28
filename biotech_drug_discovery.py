#!/usr/bin/env python3
"""Generate a professional deck on Biotech Drug Discovery.

Theme: deep science aesthetic — dark navy / deep teal background, electric
cyan primary, lime-gold accent. Built on dark_tech_theme() overrides.

Constraints honored:
- Source citations anchored at y=940, height=40 (never y~720).
- Vertical fill: secondary insight elements in the y=700-860 zone before source.
- Bullet char limits per panel width.
- 5-12 objects/slide, never > 14.
- Mermaid diagram uses %%{init}%% themeVariables to match slide colors.
- No embed for video — QR code used for the FDA/NIH resource.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[0] / "scripts"))

from block_builder import (  # noqa: E402
    bullet_list,
    chart,
    dark_tech_theme,
    deck,
    diagram,
    image,
    kpi_card,
    line,
    qr_code,
    section,
    shape,
    slide,
    table,
    text,
    title_chip,
    token,
)

# ---------------------------------------------------------------------------
# Theme: "Deep Genome" — deep teal-navy canvas, electric cyan primary,
# lime-gold accent for highlights. Inter display for clean data register.
# ---------------------------------------------------------------------------
THEME = dark_tech_theme(
    {
        "theme": {"name": "Deep Genome"},
        "colors": {
            "background": "#06141b",   # deep teal-navy
            "surface": "#0d2430",      # raised teal panel
            "foreground": "#eef7fb",   # near-white
            "mutedForeground": "#8fb4c4",  # muted cyan-grey
            "primary": "#22d3ee",      # electric cyan
            "primaryForeground": "#04141a",
            "accent": "#bef264",       # lime-gold
            "accentForeground": "#0a1f0a",
            "border": "#1e4452",       # teal border
            "success": "#34d399",
            "warning": "#fbbf24",
            "destructive": "#fb7185",
        },
    }
)

# Hosted hero images (deterministic picsum seeds tuned for a science register).
HERO_LAB = "https://picsum.photos/seed/dna-helix-lab-blue/1920/1080"
GENOMICS_IMG = "https://picsum.photos/seed/genomics-sequencer-cyan/960/1080"
CTA_IMG = "https://picsum.photos/seed/biotech-future-lab/1920/1080"

GRADIENT_BG = {
    "kind": "gradient",
    "gradient": {
        "kind": "linear",
        "angle": 135,
        "stops": [
            {"color": token("background"), "offset": 0},
            {"color": token("surface"), "offset": 1},
        ],
    },
}


def src_caption(content: str, y: float = 940) -> dict:
    """Source/footnote citation anchored at the very bottom (y=940, h=40)."""
    return text("caption", 100, y, 1720, 40, content)


# ---------------------------------------------------------------------------
# Slide 1 — Cover
# ---------------------------------------------------------------------------
def cover() -> dict:
    return slide(
        [
            image(HERO_LAB, 0, 0, 1920, 1080, opacity=0.38),
            shape(0, 0, 1920, 1080, "background", shape="rectangle", stroke_width=0, opacity=0.68),
            *title_chip("THE BIOTECH FRONTIER", 100, 90, 420),
            text("title", 100, 330, 1500, 190, "Drug Discovery Is Being Rewritten in Code"),
            text(
                "subtitle",
                104,
                540,
                1320,
                130,
                "How AI, mRNA platforms, genomics, and CRISPR are collapsing the path from molecule to medicine.",
            ),
            line(104, 720, 640, 4, stroke="accent", stroke_width=6),
            text("caption", 106, 760, 1200, 60, "AI-accelerated discovery  •  mRNA platforms  •  Personalized medicine"),
        ],
        notes=(
            "Cover slide. Thesis: the drug discovery process is shifting from a "
            "slow, attrition-heavy pipeline to a faster, data-driven, programmable one."
        ),
        speaker_notes="Open with the scale of the problem before showing the new tools.",
        background=GRADIENT_BG,
        transitions={"effect": "zoom", "durationMs": 500},
    )


# ---------------------------------------------------------------------------
# Slide 2 — The pipeline crisis (KPIs + bar chart)
# ---------------------------------------------------------------------------
def pipeline_crisis() -> dict:
    kpis = [
        *kpi_card("$2.6B", "Avg. cost to bring one new drug to market", 100, 300, 540, 200),
        *kpi_card("10-15 yrs", "Time from discovery to FDA approval", 690, 300, 540, 200),
        *kpi_card("~7.9%", "Phase I candidates that reach approval", 1280, 300, 540, 200),
    ]
    return slide(
        [
            *title_chip("01 / THE PROBLEM", 100, 74, 300),
            text("heading", 100, 150, 1500, 70, "The traditional pipeline is slow, costly, and lossy"),
            *kpis,
            chart(
                100,
                560,
                1720,
                340,
                ["Phase I", "Phase II", "Phase III", "Approval"],
                [
                    {
                        "name": "Candidates surviving (% of Phase I)",
                        "values": [100, 63, 31, 8],
                        "color": token("primary"),
                    }
                ],
                chart_type="bar",
            ),
            src_caption(
                "Source: Tufts CSDD (DiMasi et al., 2016) for cost/timeline; BIO/Informa "
                "clinical development success rates 2011-2020 for attrition.",
            ),
        ],
        notes=(
            "Only ~8 in 100 drugs that enter Phase I clinical trials are ultimately "
            "approved. Each failure compounds the cost carried by the survivors."
        ),
        speaker_notes=(
            "Cost ~$2.6B (Tufts CSDD 2016). Timeline 10-15 yrs (FDA/PhRMA). "
            "Phase I to approval ~7.9% (BIO/Informa, 2011-2020 dataset)."
        ),
    )


# ---------------------------------------------------------------------------
# Slide 3 — AI acceleration (Mermaid diagram + bullet list)
# ---------------------------------------------------------------------------
def ai_acceleration() -> dict:
    mermaid = (
        '%%{init: {"theme":"base","themeVariables":{'
        '"primaryColor":"#0d2430",'
        '"primaryTextColor":"#eef7fb",'
        '"primaryBorderColor":"#22d3ee",'
        '"lineColor":"#bef264",'
        '"secondaryColor":"#06141b",'
        '"tertiaryColor":"#0d2430",'
        '"fontSize":"20px"}}}%%\n'
        "flowchart LR\n"
        "  A[Target ID] --> B[Hit discovery]\n"
        "  B --> C[Lead optimization]\n"
        "  C --> D[Preclinical]\n"
        "  D --> E[Clinical trials]\n"
        "  AI1([AI: target scoring]):::ai --> A\n"
        "  AI2([AI: generative chemistry]):::ai --> B\n"
        "  AI3([AI: ADMET prediction]):::ai --> C\n"
        "  AI4([AI: trial design]):::ai --> E\n"
        "  classDef ai fill:#22d3ee,stroke:#bef264,color:#04141a,stroke-width:2px;"
    )
    return slide(
        [
            *title_chip("02 / AI ACCELERATION", 100, 74, 360),
            text("heading", 100, 150, 1500, 70, "AI compresses every stage of the pipeline"),
            diagram(100, 250, 1130, 470, mermaid),
            bullet_list(
                [
                    {"title": "Target ID", "body": "graph models rank disease drivers"},
                    {"title": "Generative", "body": "novel molecules designed in silico"},
                    {"title": "ADMET", "body": "toxicity flagged before the bench"},
                    {"title": "First in clinic", "body": "AI molecule hit Phase II (2023)"},
                ],
                1270,
                270,
                560,
                430,
                role="body",
            ),
            line(100, 760, 1720, 3, stroke="accent", stroke_width=4),
            text(
                "subtitle",
                100,
                790,
                1720,
                90,
                "Insilico Medicine's INS018_055 went from target to Phase II in under 30 months.",
            ),
            src_caption("Source: Insilico Medicine clinical pipeline disclosures, 2023; Nature Biotechnology coverage."),
        ],
        notes=(
            "AI does not replace the pipeline — it attacks the bottlenecks: which "
            "target, which molecule, which liabilities, and which trial design."
        ),
        speaker_notes=(
            "INS018_055 (idiopathic pulmonary fibrosis) is widely cited as the first "
            "fully generative-AI-discovered drug to reach Phase II (2023)."
        ),
    )


# ---------------------------------------------------------------------------
# Slide 4 — mRNA & genomics platform (table + secondary insight + source)
# ---------------------------------------------------------------------------
def mrna_genomics() -> dict:
    return slide(
        [
            *title_chip("03 / PLATFORMS", 100, 74, 280),
            text("heading", 100, 150, 1620, 70, "One platform, many diseases: mRNA goes programmable"),
            text(
                "subtitle",
                102,
                232,
                1500,
                70,
                "The same delivery chassis is re-coded for new targets — drug design becomes software.",
            ),
            table(
                100,
                330,
                1720,
                360,
                [
                    ["Platform", "Disease area", "Stage (2024-25)"],
                    ["mRNA vaccine", "COVID-19", "Approved (2020-21)"],
                    ["mRNA vaccine", "RSV (mRESVIA)", "Approved (2024)"],
                    ["mRNA + neoantigen", "Melanoma (personalized)", "Phase III"],
                    ["CRISPR (Casgevy)", "Sickle cell / beta-thalassemia", "Approved (2023)"],
                ],
            ),
            line(100, 740, 1720, 3, stroke="accent", stroke_width=4),
            text(
                "subtitle",
                100,
                770,
                1720,
                90,
                "Key insight: a validated platform turns each new disease into a coding problem, not a 10-year restart.",
            ),
            src_caption("Source: FDA approval records; Moderna & BioNTech pipeline disclosures, 2023-2025."),
        ],
        notes=(
            "mRNA and CRISPR are platforms, not single products. Once the delivery and "
            "manufacturing are validated, new indications reuse the same chassis."
        ),
        speaker_notes=(
            "mRESVIA (mRNA-1345) FDA-approved May 2024. Casgevy (exa-cel) FDA-approved "
            "Dec 2023 — first CRISPR-based therapy. Personalized melanoma mRNA (mRNA-4157/"
            "V940 + pembrolizumab) in Phase III."
        ),
    )


# ---------------------------------------------------------------------------
# Slide 5 — Personalized medicine (image + bullet_list, strict char limits)
# ---------------------------------------------------------------------------
def personalized_medicine() -> dict:
    # Right panel width ~ 860 (half panel) -> 55 char bullet limit.
    bullets = [
        "Tumor DNA decoded into a patient-specific vaccine",
        "Pharmacogenomics matches drug and dose to your genes",
        "Liquid biopsies catch relapse from a blood draw",
        "Genome cost fell from $100M to a few hundred dollars",
    ]
    for b in bullets:
        assert len(b) <= 55, f"bullet too long ({len(b)}): {b}"
    return slide(
        [
            image(GENOMICS_IMG, 0, 0, 900, 1080, opacity=1, fit="cover"),
            shape(900, 0, 1020, 1080, "background", shape="rectangle", stroke_width=0, opacity=1),
            *title_chip("04 / PERSONALIZED", 960, 90, 320),
            text("heading", 960, 200, 880, 130, "Medicine tailored to a single genome"),
            bullet_list(bullets, 960, 360, 880, 360, role="body"),
            line(960, 760, 880, 3, stroke="accent", stroke_width=4),
            text(
                "subtitle",
                960,
                792,
                880,
                90,
                "From one-size-fits-all to N-of-1: the patient's biology is the spec.",
            ),
            src_caption("Source: NHGRI sequencing cost data; FDA pharmacogenomics biomarker tables, 2024.", y=940),
        ],
        notes=(
            "Personalized medicine reframes the patient's own genome and tumor as the "
            "design input — vaccines and dosing are computed per individual."
        ),
        speaker_notes=(
            "NHGRI: sequencing a human genome dropped from ~$100M (2001) to a few hundred "
            "dollars today. FDA lists 200+ pharmacogenomic biomarkers in drug labeling."
        ),
    )


# ---------------------------------------------------------------------------
# Slide 6 — The economics (line chart + bullet_list)
# ---------------------------------------------------------------------------
def economics() -> dict:
    # Right bullets panel ~ 560 wide (half) -> 55 char limit.
    bullets = [
        "Genome sequencing cost down ~6 orders of magnitude",
        "AI shrinks discovery timelines by an estimated 1-2 yrs",
        "Platform reuse spreads fixed cost across indications",
        "Cheaper data unlocks rare-disease economics",
    ]
    for b in bullets:
        assert len(b) <= 55, f"bullet too long ({len(b)}): {b}"
    return slide(
        [
            *title_chip("05 / ECONOMICS", 100, 74, 290),
            text("heading", 100, 150, 1620, 70, "Falling data costs change what is fundable"),
            chart(
                100,
                270,
                1080,
                470,
                ["2001", "2007", "2010", "2015", "2020", "2024"],
                [
                    {
                        "name": "Cost to sequence a genome (USD, log-scale feel)",
                        "values": [100000000, 10000000, 50000, 1500, 600, 300],
                        "color": token("primary"),
                    }
                ],
                chart_type="line",
            ),
            bullet_list(bullets, 1220, 290, 600, 430, role="body"),
            line(100, 760, 1720, 3, stroke="accent", stroke_width=4),
            text(
                "subtitle",
                100,
                790,
                1720,
                90,
                "When inputs get 100,000x cheaper, the set of economically viable diseases expands.",
            ),
            src_caption("Source: NHGRI Genome Sequencing Program cost data, 2001-2024."),
        ],
        notes=(
            "The genome-cost curve outpaced Moore's law. Combined with AI and platform "
            "reuse, the unit economics of discovery have fundamentally shifted."
        ),
        speaker_notes="NHGRI cost-per-genome series is the canonical chart here.",
    )


# ---------------------------------------------------------------------------
# Slide 7 — Closing CTA (hero image + takeaways + QR)
# ---------------------------------------------------------------------------
def closing() -> dict:
    takeaways = [
        "AI attacks the pipeline's worst bottlenecks, not just the bench",
        "mRNA and CRISPR are reusable platforms, not single products",
        "Cheap genomics makes personalized, N-of-1 medicine fundable",
    ]
    for t in takeaways:
        assert len(t) <= 75, f"takeaway too long ({len(t)}): {t}"
    return slide(
        [
            image(CTA_IMG, 0, 0, 1920, 1080, opacity=0.30),
            shape(0, 0, 1920, 1080, "background", shape="rectangle", stroke_width=0, opacity=0.74),
            *title_chip("06 / THE TAKEAWAY", 100, 74, 320),
            text("title", 100, 250, 1280, 170, "From slow attrition to programmable medicine"),
            bullet_list(takeaways, 100, 470, 1200, 250, role="body"),
            qr_code("https://www.fda.gov/drugs/development-approval-process-drugs", 1480, 250, 300),
            text("caption", 1440, 570, 380, 60, "Scan: FDA drug development & approval process", text_align="center"),
            line(100, 770, 1240, 3, stroke="accent", stroke_width=4),
            text(
                "subtitle",
                100,
                800,
                1240,
                90,
                "The constraint is shifting from chemistry to code — and from years to months.",
            ),
            src_caption("Resource: U.S. FDA — Development & Approval Process (Drugs); NIH/NHGRI public data."),
        ],
        notes=(
            "Close on the synthesis: the rate-limiting step of drug discovery is moving "
            "upstream into data and design. Scan the QR for the FDA primer."
        ),
        speaker_notes="QR links to the FDA drug development/approval overview.",
        background=GRADIENT_BG,
        transitions={"effect": "fade", "durationMs": 450},
    )


def build_deck() -> dict:
    return deck(
        "Biotech Drug Discovery",
        [
            section("The Problem", [cover(), pipeline_crisis()]),
            section("The New Toolkit", [ai_acceleration(), mrna_genomics(), personalized_medicine()]),
            section("Outlook", [economics(), closing()]),
        ],
        theme=THEME,
    )


if __name__ == "__main__":
    print(json.dumps(build_deck()))
