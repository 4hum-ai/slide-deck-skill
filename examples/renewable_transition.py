#!/usr/bin/env python3
"""Generate a deck on The Renewable Energy Transition."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from block_builder import (  # noqa: E402
    bullet_list,
    chart,
    deck,
    diagram,
    image,
    kpi_card,
    light_corporate_theme,
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

# GENERATED hero/lifestyle image URLs (from scripts/generate_image.py)
COVER_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/d7a3a10a-a909-4d4e-a1bb-6fa6c13e13c5.png"
WORKERS_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/4e389409-87ed-4899-8b71-bcc7a4cf5601.png"
CITY_NIGHT_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/1f78bbaf-2e84-4383-9e31-275ef2f5ce14.png"


def build_deck() -> dict:
    # Clean, optimistic theme: white background, electric green primary, solar amber accent.
    theme = light_corporate_theme(
        overrides={
            "theme": {"name": "Clean Energy Optimist"},
            "colors": {
                "primary": "#16a34a",
                "primaryForeground": "#ffffff",
                "accent": "#f59e0b",
                "accentForeground": "#000000",
                "success": "#16a34a",
                "warning": "#f59e0b",
            },
        }
    )

    # ---- Slide 1: Cover -------------------------------------------------
    cover = slide(
        [
            image(COVER_IMG, 0, 0, 1920, 1080, opacity=1),
            shape(0, 0, 1920, 1080, "foreground", shape="rectangle", stroke_width=0, opacity=0.42),
            *title_chip("THE RENEWABLE ENERGY TRANSITION", 92, 84, 540),
            text("title", 100, 360, 1500, 220,
                 "Clean energy already won on cost",
                 textAlign="left"),
            text("subtitle", 104, 600, 1320, 130,
                 "How collapsing solar and wind prices, cheap storage, and EVs are rewriting the global energy map.",
                 textAlign="left"),
            line(106, 770, 640, 4, stroke="accent", stroke_width=6),
            text("caption", 108, 940, 1400, 40,
                 "Sources: IRENA Renewable Power Generation Costs 2023; BloombergNEF; IEA Global EV Outlook 2024.",
                 textAlign="left"),
        ],
        notes=(
            "The renewable transition is no longer a subsidy story — it is an economics story. "
            "Solar and wind are now the cheapest sources of new electricity across most of the world."
        ),
        speaker_notes=(
            "Cover. IRENA 2023: utility solar LCOE down ~90% since 2010; onshore wind ~70%. "
            "BNEF battery packs ~$139/kWh in 2023. IEA: ~18% of new cars sold in 2023 were electric."
        ),
        background={
            "kind": "gradient",
            "gradient": {
                "kind": "linear",
                "angle": 135,
                "stops": [{"color": token("surface"), "offset": 0}, {"color": token("background"), "offset": 1}],
            },
        },
        transitions={"effect": "zoom", "durationMs": 500},
    )

    # ---- Slide 2: Cost collapse ----------------------------------------
    kpis = [
        lambda x, y, w, h: kpi_card("-90%", "Utility solar LCOE, 2010 to 2023 (IRENA)", x, y, w, h, fill="surface"),
        lambda x, y, w, h: kpi_card("-70%", "Onshore wind LCOE, 2010 to 2023 (IRENA)", x, y, w, h, fill="surface"),
        lambda x, y, w, h: kpi_card("~$0.04", "Global avg utility solar, $/kWh in 2023", x, y, w, h, fill="surface"),
    ]
    from block_builder import grid  # local import to keep top tidy

    cost = slide(
        [
            *title_chip("01 / COST COLLAPSE", 92, 72, 340),
            text("heading", 100, 150, 1500, 72, "New solar and wind are now the cheapest power"),
            *grid(kpis, cols=3, x=100, y=300, total_w=1720, total_h=210),
            chart(
                100, 560, 1720, 330,
                ["2010", "2013", "2016", "2019", "2022", "2024"],
                [
                    {"name": "Utility solar PV ($/MWh)", "values": [378, 230, 110, 68, 49, 44], "color": token("primary")},
                    {"name": "Onshore wind ($/MWh)", "values": [102, 86, 70, 53, 41, 33], "color": token("accent")},
                ],
                chart_type="line",
            ),
            text("caption", 102, 940, 1600, 40,
                 "Source: IRENA, Renewable Power Generation Costs in 2023 (global weighted-average LCOE).",
                 textAlign="left"),
        ],
        notes=(
            "Between 2010 and 2024 the cost of utility-scale solar fell roughly 90% and onshore wind "
            "around 70%. Both now sit below the cost of running many existing fossil plants."
        ),
        speaker_notes="IRENA RPGC 2023. Values are global weighted-average LCOE in 2023 USD/MWh; 2024 estimated.",
    )

    # ---- Slide 3: Grid & storage ---------------------------------------
    mermaid = (
        '%%{init: {"theme":"base","themeVariables":{'
        '"primaryColor":"#dcfce7","primaryTextColor":"#0f172a","primaryBorderColor":"#16a34a",'
        '"lineColor":"#f59e0b","fontSize":"22px","fontFamily":"Inter"}}}%%\n'
        "flowchart LR\n"
        "  S[Solar PV]:::gen --> G((Grid))\n"
        "  W[Wind]:::gen --> G\n"
        "  G --> B[Battery storage]:::store\n"
        "  B --> G\n"
        "  G --> L[Homes, EVs and industry]:::load\n"
        "  classDef gen fill:#dcfce7,stroke:#16a34a,stroke-width:2px;\n"
        "  classDef store fill:#fef3c7,stroke:#f59e0b,stroke-width:2px;\n"
        "  classDef load fill:#e2e8f0,stroke:#64748b,stroke-width:2px;"
    )
    storage = slide(
        [
            *title_chip("02 / GRID & STORAGE", 92, 72, 360),
            text("heading", 100, 150, 1720, 72, "Cheap batteries turn intermittent power into firm power"),
            diagram(100, 300, 980, 470, mermaid),
            text("heading", 1130, 300, 700, 56, "Why storage changes everything"),
            bullet_list(
                [
                    "Battery pack prices fell ~90% from 2010 to 2023",
                    "BloombergNEF: ~$139 per kWh average in 2023",
                    "Storage shifts midday solar into the evening peak",
                    "Four-hour batteries now beat new gas peaker plants",
                    "Grid-scale capacity is doubling roughly every two years",
                ],
                x=1130, y=370, width=710, height=400, role="body",
            ),
            line(1130, 790, 710, 3, stroke="accent", stroke_width=5),
            text("body", 1130, 820, 710, 90,
                 "Result: solar plus storage now bids to replace baseload, not just peakers.",
                 textAlign="left"),
            text("caption", 1130, 940, 710, 40,
                 "Sources: BloombergNEF Battery Price Survey 2023; IEA.",
                 textAlign="left"),
        ],
        notes=(
            "Solar and wind generate when the sun shines and the wind blows. Cheap batteries are what "
            "convert that variable output into reliable, dispatchable power for the grid."
        ),
        speaker_notes="BNEF 2023 lithium-ion pack price ~$139/kWh, down from >$1,200/kWh in 2010.",
    )

    # ---- Slide 4: EV adoption ------------------------------------------
    ev = slide(
        [
            *title_chip("03 / EV ADOPTION", 92, 72, 320),
            text("heading", 100, 150, 1720, 72, "Electric vehicles are crossing the tipping point"),
            text("subtitle", 102, 232, 1500, 60,
                 "Share of new passenger cars sold that are electric, with policy phase-out targets."),
            table(
                100, 320, 1100, 470,
                [
                    ["Market", "EV share of new sales", "Petrol phase-out target"],
                    ["Norway", "~90%", "2025"],
                    ["China", "~38%", "no national ban yet"],
                    ["European Union", "~22%", "2035"],
                    ["United States", "~10%", "varies by state"],
                    ["World (average)", "~18%", "—"],
                ],
            ),
            shape(1240, 320, 580, 470, "surface", corner_radius=18),
            text("heading", 1276, 350, 508, 60, "Key insight", textAlign="left"),
            text("body", 1276, 420, 508, 340,
                 "Norway shows the endpoint: once total cost of ownership flips, adoption is fast and "
                 "near-total. Most major markets are now on the steep part of the S-curve, and global "
                 "EV sales passed one in six new cars in 2023.",
                 textAlign="left"),
            text("caption", 102, 940, 1600, 40,
                 "Source: IEA Global EV Outlook 2024 (2023 sales shares); national policy announcements.",
                 textAlign="left"),
        ],
        notes=(
            "EV adoption is following a classic S-curve. Norway is already past 90% of new sales; China and "
            "the EU are climbing steeply; the global average reached roughly 18% in 2023."
        ),
        speaker_notes="IEA Global EV Outlook 2024: 2023 BEV+PHEV new-sales shares.",
    )

    # ---- Slide 5: The economics (split panel, GENERATED half image) ----
    TEXT_X = 720  # text panel start; source x must live here, not in image panel
    econ = slide(
        [
            image(WORKERS_IMG, 0, 0, 700, 1080, opacity=1),
            *title_chip("04 / THE ECONOMICS", TEXT_X, 84, 360),
            text("heading", TEXT_X, 170, 1120, 130,
                 "Clean energy is now the low-cost, job-rich choice", textAlign="left"),
            bullet_list(
                [
                    "Cheapest new power across two-thirds of the world",
                    "No fuel cost — sunlight and wind are free inputs",
                    "Falling cost of capital rewards zero-fuel assets",
                    "~16 million clean-energy jobs worldwide in 2023",
                    "Solar PV is the single largest energy-jobs employer",
                    "Local installation work cannot be offshored",
                ],
                x=TEXT_X, y=340, width=1100, height=360, role="body",
            ),
            line(TEXT_X, 720, 1100, 3, stroke="accent", stroke_width=5),
            text("body", TEXT_X, 752, 1100, 150,
                 "The economic logic has flipped: clean energy wins on price first, and climate second.",
                 textAlign="left"),
            text("caption", TEXT_X, 940, 1100, 40,
                 "Sources: IRENA & ILO, Renewable Energy and Jobs Annual Review 2023; Lazard LCOE 2023.",
                 textAlign="left"),
        ],
        notes=(
            "The economics now favor clean energy on cost alone. With no fuel bill, renewables are "
            "insulated from price shocks, and they support millions of local, non-exportable jobs."
        ),
        speaker_notes="IRENA/ILO 2023: ~16.2 million renewable-energy jobs globally; solar PV largest share.",
    )

    # ---- Slide 6: Policy landscape -------------------------------------
    policy = slide(
        [
            *title_chip("05 / POLICY", 92, 72, 220),
            text("heading", 100, 150, 1720, 72, "Policy is accelerating an already-cheap technology"),
            text("subtitle", 102, 232, 1500, 60,
                 "Major economies have committed historic public investment to clean energy."),
            chart(
                100, 320, 980, 470,
                ["US IRA", "EU Green Deal", "China 14th Plan", "India PLI"],
                [{"name": "Headline clean-energy support ($B)", "values": [369, 270, 280, 30], "color": token("primary")}],
                chart_type="bar",
            ),
            text("heading", 1140, 320, 700, 56, "What policy is doing", textAlign="left"),
            bullet_list(
                [
                    "Tax credits cut the cost of capital for projects",
                    "2035 combustion-engine bans pull EV demand forward",
                    "Carbon pricing raises the cost of fossil alternatives",
                    "Permitting reform is the next big bottleneck to clear",
                ],
                x=1140, y=400, width=700, height=300, role="body",
            ),
            text("caption", 102, 940, 1700, 40,
                 "Sources: US Inflation Reduction Act (2022); EU Green Deal Industrial Plan; IEA policy tracker.",
                 textAlign="left"),
        ],
        notes=(
            "Policy is no longer propping up an expensive technology — it is accelerating a cheap one. "
            "The IRA, EU Green Deal, and China's plans direct hundreds of billions toward deployment."
        ),
        speaker_notes="Figures are headline/announced support, not strictly comparable accounting; US IRA ~$369B clean-energy provisions.",
    )

    # ---- Slide 7: Closing CTA (GENERATED dark hero + QR) ---------------
    closing = slide(
        [
            image(CITY_NIGHT_IMG, 0, 0, 1920, 1080, opacity=1),
            shape(0, 0, 1920, 1080, "foreground", shape="rectangle", stroke_width=0, opacity=0.55),
            *title_chip("THE TAKEAWAY", 92, 84, 280),
            text("title", 100, 290, 1320, 170, "The transition is an economic certainty"),
            bullet_list(
                [
                    "Solar and wind already beat fossil power on price",
                    "Cheap storage makes clean power firm and dispatchable",
                    "EVs are racing up the adoption S-curve",
                    "Policy is now an accelerant, not a crutch",
                ],
                x=104, y=500, width=1280, height=320, role="body",
                textAlign="left",
            ),
            text("caption", 108, 940, 1200, 40,
                 "Scan for IEA & IRENA data dashboards. Sources cited on each slide.",
                 textAlign="left"),
            shape(1560, 470, 300, 300, "background", corner_radius=18),
            qr_code("https://www.iea.org/data-and-statistics", 1585, 495, 250),
        ],
        notes=(
            "The renewable transition is no longer a question of if, but how fast. The cost curves, "
            "storage economics, EV adoption, and policy all point the same direction."
        ),
        speaker_notes="Closing. QR links to the IEA data and statistics portal.",
        background={
            "kind": "gradient",
            "gradient": {
                "kind": "linear",
                "angle": 135,
                "stops": [{"color": token("background"), "offset": 0}, {"color": token("surface"), "offset": 1}],
            },
        },
        transitions={"effect": "fade", "durationMs": 400},
    )

    return deck(
        "The Renewable Energy Transition",
        [
            section("The Cost Story", [cover, cost, storage]),
            section("Adoption & Economics", [ev, econ, policy]),
            section("Outlook", [closing]),
        ],
        theme=theme,
    )


if __name__ == "__main__":
    print(json.dumps(build_deck()))
