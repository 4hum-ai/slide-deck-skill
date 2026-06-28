#!/usr/bin/env python3
"""Generate the 'Urban Mobility 2030' deck.

Bold, urban dark theme: near-black background, electric-blue primary,
vivid coral/orange accent. Custom overrides on dark_tech_theme().

Contrast discipline (v1.14.0): every slide whose text overlaps a full-bleed
generated photo gets a semi-transparent dark scrim shape() AND explicit
white rich_text runs (#ffffff) so dark text never lands on a dark photo.
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
    grid,
    image,
    kpi_card,
    line,
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

# Generated, content-relevant images (scripts/generate_image.py)
COVER_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/2b76e0ea-7dc3-4d66-9b90-1dde16d0db84.png"
MICRO_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/46b42c4a-28a8-429c-b7a3-d7582dfae499.png"
NIGHT_IMG = "https://storage.googleapis.com/open-academy-media/ai-images/19b1d1c9-547c-4519-b144-44796526709a.png"


def white(content: str, weight: int = 400):
    # primaryForeground == #ffffff in this theme; token ref keeps the validator happy
    # while guaranteeing white text over the dark scrim on hero slides.
    return [{"kind": "span", "text": content, "style": {"color": token("primaryForeground"), "fontWeight": weight}}]


def build_deck() -> dict:
    # --- Urban theme: near-black bg, electric blue primary, coral/orange accent
    theme = dark_tech_theme(
        overrides={
            "theme": {"name": "Urban Mobility 2030", "fonts": {"display": "Oswald", "heading": "Oswald", "body": "Inter", "mono": "JetBrains Mono"}},
            "colors": {
                "background": "#0a0c10",
                "surface": "#161a22",
                "foreground": "#f5f7fa",
                "mutedForeground": "#9aa6b8",
                "primary": "#1668c0",          # electric blue (AA-safe for white-on-blue table header)
                "primaryForeground": "#ffffff",
                "accent": "#ff5a36",           # vivid coral/orange
                "accentForeground": "#0a0c10",
                "border": "#2a3140",
            },
        }
    )

    # ----------------------------------------------------------------- Slide 1: Cover
    cover = slide(
        [
            image(COVER_IMG, 0, 0, 1920, 1080, fit="cover"),
            # dark scrim for readable white text over the photo
            shape(0, 0, 1920, 1080, "background", shape="rectangle", stroke_width=0, opacity=0.6),
            *title_chip("URBAN MOBILITY 2030", 100, 90, 420),
            # title stacked as two blocks (server forbids literal \n inside a single run)
            text("title", 100, 320, 1500, 280,
                 [{"kind": "block", "runs": white("How Cities Will Move", 700)},
                  {"kind": "block", "runs": white("in the Next Decade", 700)}]),
            rich_text("subtitle", 104, 640, 1300, 110,
                      white("Autonomous vehicles, transit reinvention, micro-mobility, "
                            "congestion pricing, and the 15-minute city.")),
            line(104, 800, 640, 4, stroke="accent", stroke_width=6),
            rich_text("caption", 106, 840, 1200, 46,
                      [{"kind": "span", "text": "A 2030 outlook on the redesign of how cities move.",
                        "style": {"color": token("mutedForeground")}}]),
        ],
        notes="Urban mobility is being redesigned on five fronts at once: autonomy, public "
              "transit, micro-mobility, pricing, and urban form. This deck frames the 2030 outlook.",
        speaker_notes="Cover. Hero image is AI-generated. Title text is explicit white over a 0.6 dark scrim.",
        background={"kind": "solid", "color": token("background")},
        transitions={"effect": "zoom", "durationMs": 500},
    )

    # ----------------------------------------------------------------- Slide 2: The crisis
    crisis = slide(
        [
            *title_chip("01 / THE MOBILITY CRISIS", 92, 72, 420),
            text("heading", 100, 150, 1500, 110, "Congestion is a multi-billion-dollar drag on cities"),
            *grid(
                [
                    lambda x, y, w, h: kpi_card("$166B", "Annual U.S. cost of congestion (2022)", x, y, w, h),
                    lambda x, y, w, h: kpi_card("51 hrs", "Time lost per U.S. driver per year", x, y, w, h),
                    lambda x, y, w, h: kpi_card("55%", "Share of humanity living in cities (2018)", x, y, w, h),
                ],
                cols=3, x=100, y=320, total_w=1720, total_h=210,
            ),
            chart(
                100, 575, 1720, 300,
                ["Istanbul", "Mexico City", "London", "New York", "Paris"],
                [{"name": "Hours lost in traffic per year (2023)", "values": [105, 96, 99, 101, 97],
                  "color": token("primary")}],
                chart_type="bar",
            ),
            text("caption", 100, 940, 1720, 40,
                 "Sources: INRIX 2022/2023 Global Traffic Scorecard; UN DESA World Urbanization Prospects 2018."),
        ],
        notes="The cost of congestion is measured in money, time, and emissions. INRIX put the 2022 "
              "U.S. cost at $166B and 51 hours lost per driver; the UN projects two-thirds of people "
              "urban by 2050, up from 55% in 2018. Top cities lose ~100 hours per driver per year.",
        speaker_notes="INRIX 2022 Scorecard: $166B, 51 hours. INRIX 2023: Istanbul 105h, NYC 101h, "
                      "London 99h, Paris 97h, Mexico City 96h. UN DESA 2018: 55% urban.",
    )

    # ----------------------------------------------------------------- Slide 3: AVs (Mermaid)
    av_diagram = (
        "flowchart LR\n"
        "  L0[\"L0\\nNo automation\"] --> L1[\"L1\\nDriver assist\"]\n"
        "  L1 --> L2[\"L2\\nPartial automation\"]\n"
        "  L2 --> L3[\"L3\\nConditional\"]\n"
        "  L3 --> L4[\"L4\\nHigh automation\"]\n"
        "  L4 --> L5[\"L5\\nFull automation\"]\n"
        "  classDef human fill:#161a22,stroke:#2a3140,color:#9aa6b8;\n"
        "  classDef machine fill:#1668c0,stroke:#1668c0,color:#ffffff;\n"
        "  classDef goal fill:#ff5a36,stroke:#ff5a36,color:#0a0c10;\n"
        "  class L0,L1,L2 human;\n"
        "  class L3,L4 machine;\n"
        "  class L5 goal;"
    )
    avs = slide(
        [
            *title_chip("02 / AUTONOMOUS VEHICLES", 92, 72, 420),
            text("heading", 100, 150, 1720, 72, "The line of control shifts from human to machine"),
            diagram(100, 270, 1720, 300, av_diagram),
            bullet_list(
                [
                    "L0-L2: the human still drives; software only assists.",
                    "L3 is the legal handoff - the car drives, you take over on request.",
                    "L4 robotaxis already run commercially in Phoenix and SF.",
                    "L5 (drive anywhere, no wheel) remains unproven at scale by 2030.",
                ],
                100, 610, 1720, 240, role="body",
            ),
            text("caption", 100, 940, 1720, 40,
                 "Source: SAE J3016 levels of driving automation; Waymo commercial robotaxi operations."),
        ],
        notes="The SAE J3016 standard defines six levels. The critical jump is L2 to L3, where "
              "responsibility legally moves from human to system. Waymo runs paid L4 robotaxis in "
              "Phoenix and San Francisco today; true L5 anywhere-driving is not expected at scale by 2030.",
        speaker_notes="SAE J3016 defines L0-L5. Waymo: commercial driverless rides in Phoenix (2020) "
                      "and San Francisco. Diagram colors: human grey, machine blue, full-auto coral.",
    )

    # ----------------------------------------------------------------- Slide 4: Transit (table)
    transit = slide(
        [
            *title_chip("03 / TRANSIT REINVENTION", 92, 72, 420),
            text("heading", 100, 150, 1720, 72, "Bold transit bets are pulling riders back"),
            text("subtitle", 102, 232, 1620, 60, "Free fares, bus rapid transit, and new metro lines move the ridership needle."),
            table(
                100, 320, 1720, 380,
                [
                    ["City", "Innovation", "Ridership change"],
                    ["Tallinn", "Free public transit for residents", "+10% in first year"],
                    ["Bogota", "TransMilenio bus rapid transit", "~2.4M trips/day"],
                    ["Paris", "Grand Paris Express metro expansion", "+200km, 4 new lines"],
                    ["Luxembourg", "Nationwide fare-free transit (2020)", "Ridership growth post-COVID"],
                ],
            ),
            line(100, 740, 1720, 3, stroke="border", stroke_width=2),
            rich_text("body", 100, 770, 1720, 120,
                      [{"kind": "span", "text": "Insight:  ", "style": {"color": token("accent"), "fontWeight": 700}},
                       {"kind": "span", "text": "Removing friction - on price and on speed - moves more riders "
                        "than new technology alone.", "style": {"color": token("foreground")}}]),
            text("caption", 100, 940, 1720, 40,
                 "Sources: City of Tallinn; TransMilenio S.A.; Societe du Grand Paris; Luxembourg Ministry of Mobility."),
        ],
        notes="Transit revival is driven by removing friction, not just new tech. Tallinn made transit "
              "free for residents in 2013 (~10% ridership lift); Bogota's TransMilenio BRT carries "
              "millions daily; Paris is adding 200km of metro via Grand Paris Express; Luxembourg went "
              "fully fare-free nationwide in 2020.",
        speaker_notes="Tallinn free transit 2013, ~10% lift. TransMilenio ~2.4M trips/day. Grand Paris "
                      "Express: ~200km, 4 new lines. Luxembourg fare-free March 2020.",
    )

    # ----------------------------------------------------------------- Slide 5: Micro-mobility (image left)
    # image x=0..900 (half panel), text panel starts x=960
    micro = slide(
        [
            image(MICRO_IMG, 0, 0, 900, 1080, fit="cover"),
            *title_chip("04 / MICRO-MOBILITY", 960, 90, 380),
            text("heading", 960, 200, 880, 130, "The last mile goes electric and human-scale"),
            bullet_list(
                [
                    "E-scooters and e-bikes fill trips too short to drive.",
                    "Shared fleets cut car use for sub-3-km journeys.",
                    "Protected lanes are the safety prerequisite.",
                    "Docked + dockless models now coexist in most cities.",
                    "Most micro-trips replace a car or ride-hail leg.",
                ],
                960, 360, 880, 380, role="body",
            ),
            line(960, 770, 700, 3, stroke="accent", stroke_width=5),
            rich_text("body", 960, 800, 880, 110,
                      [{"kind": "span", "text": "Half of all urban car trips are under 5 km - prime "
                        "micro-mobility territory.", "style": {"color": token("foreground")}}]),
            text("caption", 960, 940, 880, 40,
                 "Source: NACTO Shared Micromobility data; OECD/ITF urban trip-length studies."),
        ],
        notes="Micro-mobility targets the short trips cars serve badly. A large share of urban car "
              "trips are under 5km - exactly the range e-bikes and e-scooters cover well. Safe uptake "
              "depends on protected lanes; docked and dockless fleets now coexist in most major cities.",
        speaker_notes="NACTO tracks shared micromobility ridership. OECD/ITF: large share of urban trips "
                      "under 5km. Source at x=960 (text panel), y=940. Image occupies x=0-900.",
    )

    # ----------------------------------------------------------------- Slide 6: 15-minute city (chart)
    fifteen = slide(
        [
            *title_chip("05 / URBAN DESIGN", 92, 72, 340),
            text("heading", 100, 150, 1720, 72, "The 15-minute city brings destinations to the door"),
            text("subtitle", 102, 232, 1620, 60, "Daily needs within a short walk or ride - and congestion pricing funds the shift."),
            chart(
                100, 320, 880, 540,
                ["Groceries", "School", "Healthcare", "Work hub", "Green space"],
                [{"name": "Target minutes by foot/bike", "values": [5, 10, 12, 15, 8], "color": token("accent")}],
                chart_type="bar",
            ),
            bullet_list(
                [
                    "Mixed-use zoning puts homes near jobs and services.",
                    "Congestion pricing prices scarce road space honestly.",
                    "London's charge cut central traffic ~15-30%.",
                    "Revenue reinvests in transit, lanes, and public realm.",
                    "Less car dependence means cleaner, quieter streets.",
                ],
                1020, 320, 800, 540, role="body",
            ),
            text("caption", 100, 940, 1720, 40,
                 "Sources: Carlos Moreno / C40 'Paris 15-minute city'; Transport for London congestion charge evaluations."),
        ],
        notes="The 15-minute city (Carlos Moreno; championed by Paris and C40) puts daily needs within "
              "a short walk or ride. Congestion pricing complements it: London's charge cut central "
              "traffic by roughly 15-30% and funds transit reinvestment.",
        speaker_notes="Carlos Moreno coined '15-minute city'; Paris/C40 adopted it. TfL: congestion "
                      "charge reduced central London traffic ~15-30% and funds transit.",
    )

    # ----------------------------------------------------------------- Slide 7: Closing (night hero)
    closing = slide(
        [
            image(NIGHT_IMG, 0, 0, 1920, 1080, fit="cover"),
            shape(0, 0, 1920, 1080, "background", shape="rectangle", stroke_width=0, opacity=0.6),
            *title_chip("THE 2030 CITY", 100, 90, 320),
            rich_text("title", 100, 230, 1400, 150, white("Mobility is being redesigned", 700)),
            rich_text("subtitle", 104, 400, 1200, 70,
                      white("Five shifts, one outcome: cities that move people, not just cars.")),
            # bullets via bullet_list (plain text() allows \n); body role color is the
            # theme's light foreground (#f5f7fa) which stays readable on the dark scrim
            bullet_list(
                [
                    "Autonomy: L4 robotaxis scale; L5 stays aspirational.",
                    "Transit: remove friction on price and on speed.",
                    "Micro-mobility: own the under-5-km trip.",
                    "Pricing + design: price roads, build 15-minute cities.",
                ],
                100, 500, 1400, 360, role="body",
            ),
            qr_code("https://deck.4hum.ai", 1560, 700, 220),
            rich_text("caption", 1540, 932, 260, 40,
                      [{"kind": "span", "text": "Scan to explore the themes.",
                        "style": {"color": token("mutedForeground")}}], text_align="center"),
        ],
        notes="The 2030 city is the product of five overlapping shifts. None alone is sufficient; "
              "together they redesign cities to move people rather than cars. Scan the QR to revisit "
              "the themes.",
        speaker_notes="Closing. Night hero is AI-generated. Title/subtitle are explicit white over a "
                      "0.6 dark scrim. Bullets use the theme body color (light) on the scrim. QR bottom-right.",
        background={"kind": "solid", "color": token("background")},
        transitions={"effect": "fade", "durationMs": 400},
    )

    return deck(
        "Urban Mobility 2030",
        [
            section("The Outlook", [cover, crisis]),
            section("The Five Shifts", [avs, transit, micro, fifteen]),
            section("Synthesis", [closing]),
        ],
        theme=theme,
    )


if __name__ == "__main__":
    print(json.dumps(build_deck()))
