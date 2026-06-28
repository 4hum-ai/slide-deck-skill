#!/usr/bin/env node
import {
  card,
  chart,
  comparisonColumns,
  darkTechTheme,
  deck,
  diagram,
  image,
  line,
  processFlow,
  section,
  shape,
  slide,
  table,
  text,
  titleChip,
  token
} from "../scripts/deck_patterns.mjs";

const theme = darkTechTheme();

const intro = slide(
  [
    image("agent-skills-marketplace-neural-library", 0, 0, 1920, 1080, { opacity: 0.35 }),
    shape(0, 0, 1920, 1080, "background", { shape: "rectangle", strokeWidth: 0, opacity: 0.7 }),
    ...titleChip("OPEN ACADEMY AGENTS", 92, 74, 350),
    text("title", 100, 330, 1120, 180, "Agent Skills & Skills Marketplace"),
    text("subtitle", 104, 535, 980, 120, "A practical operating model for packaging repeatable agent expertise."),
    line(104, 710, 620, 3, { stroke: "accent", strokeWidth: 5 }),
    text("caption", 106, 750, 900, 58, "Generated from examples/agent-skills-marketplace.mjs.")
  ],
  "This deck introduces agent skills and the skills marketplace. The core idea is that repeatable agent workflows should be packaged, discovered, installed, governed, and improved.",
  "Example deck for the slide-deck-skill repository.",
  {
    background: {
      kind: "gradient",
      gradient: {
        kind: "linear",
        angle: 135,
        stops: [{ color: token("background"), offset: 0 }, { color: token("surface"), offset: 1 }]
      }
    },
    transitions: { effect: "zoom", durationMs: 500 }
  }
);

const whySkills = slide(
  [
    ...titleChip("01 / WHY SKILLS", 92, 72, 260),
    text("heading", 100, 150, 1120, 72, "Agents need executable know-how"),
    text("subtitle", 102, 230, 1180, 90, "A skill turns an expert workflow into a reusable capability bundle."),
    ...comparisonColumns(
      [
        { title: "Prompt only", body: "Helpful context, but too broad to preserve exact steps, assets, tooling, and validation." },
        { title: "Skill package", body: "Instructions plus scripts, assets, examples, and task-specific quality gates." },
        { title: "Marketplace", body: "Discovery, installation, updates, provenance, and governance across teams." }
      ],
      110,
      390,
      1700,
      340
    ),
    text("caption", 112, 840, 1500, 58, "The shift is from conversational advice to packaged operating procedure.")
  ],
  "A prompt can describe a process, but a skill packages the actual procedure. A marketplace then makes that package available across teams.",
  "Use this slide to contrast prompt guidance with packaged capability."
);

const anatomy = slide(
  [
    ...titleChip("02 / ANATOMY", 92, 72, 250),
    text("heading", 100, 150, 1120, 72, "A good skill is small, opinionated, and testable"),
    chart(120, 315, 780, 520, ["Trigger", "Workflow", "Assets", "Validation", "Handoff"], [
      { name: "Reliability contribution", values: [85, 95, 70, 90, 80], color: token("primary") }
    ]),
    ...card(1000, 305, 760, 120, "Trigger", "When to load the skill, and when to skip it."),
    ...card(1000, 455, 760, 120, "Workflow", "The actual expert procedure, not generic advice."),
    ...card(1000, 605, 760, 120, "Verification", "Checks that prove the result is ready to hand off.")
  ],
  "The best skills are narrow enough to trust and complete enough to finish the job.",
  "The bar chart is illustrative, not measured data."
);

const runtime = slide(
  [
    ...titleChip("03 / RUNTIME FLOW", 92, 72, 310),
    text("heading", 100, 150, 1120, 70, "How an agent uses a skill"),
    diagram(
      175,
      330,
      1500,
      460,
      "flowchart LR\n  U[User request] --> M{Match skill?}\n  M -->|yes| L[Load instructions]\n  M -->|no| B[Base behavior]\n  L --> R[Read references]\n  R --> T[Run tools]\n  T --> V[Verify output]\n  V --> H[Handoff]"
    ),
    ...processFlow(
      [
        { title: "Selective context", body: "Load only what the task needs." },
        { title: "Tool-backed work", body: "Prefer scripts over fragile retyping." },
        { title: "Visible result", body: "Return artifacts, links, and checks." }
      ],
      150,
      820,
      1620,
      120
    )
  ],
  "At runtime, the agent matches the request to a skill, loads the relevant context, runs the needed tools, verifies the result, and hands off the artifact.",
  "Runtime flow for agent skill invocation."
);

const marketplace = slide(
  [
    ...titleChip("04 / MARKETPLACE", 92, 72, 300),
    text("heading", 100, 150, 1180, 70, "The marketplace is the operating layer"),
    text("subtitle", 102, 230, 1210, 72, "It makes reusable capabilities discoverable, installable, governable, and improvable."),
    table(120, 355, 1680, 420, [
      ["Marketplace job", "What it answers", "Why it matters"],
      ["Discover", "Which skill solves this task?", "Reduces duplicate work"],
      ["Install", "How do I add it safely?", "Lowers adoption friction"],
      ["Trust", "Who built it and what can it do?", "Supports governance"],
      ["Update", "What changed between versions?", "Keeps workflows current"]
    ]),
    text("caption", 122, 840, 1500, 60, "A marketplace turns isolated prompt craft into shared capability.")
  ],
  "The marketplace answers what exists, how to install it, why to trust it, and how to keep it updated.",
  "Marketplace framing slide."
);

const takeaway = slide(
  [
    image("futuristic-workbench-agent-skills", 0, 0, 1920, 1080, { opacity: 0.28 }),
    shape(0, 0, 1920, 1080, "background", { shape: "rectangle", strokeWidth: 0, opacity: 0.75 }),
    ...titleChip("05 / TAKEAWAY", 92, 72, 275),
    text("title", 120, 290, 1220, 180, "Skills turn agent work into product capability"),
    text("subtitle", 124, 500, 1080, 125, "The marketplace makes those capabilities discoverable, trusted, and continuously improved."),
    ...processFlow(
      [
        { title: "Package", body: "Capture the workflow." },
        { title: "Distribute", body: "Install through a marketplace." },
        { title: "Improve", body: "Use feedback to raise quality." }
      ],
      124,
      715,
      1672,
      150
    )
  ],
  "Skills package expert workflows so agents can perform them consistently. The marketplace distributes those capabilities and creates a path for ongoing improvement.",
  "Closing synthesis."
);

const deckJson = deck("Agent Skills & Skills Marketplace", [
  section("Agent Skills", [intro, whySkills, anatomy, runtime]),
  section("Skills Marketplace", [marketplace, takeaway])
], { theme });

process.stdout.write(JSON.stringify(deckJson));
