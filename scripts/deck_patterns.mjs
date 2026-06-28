import { randomUUID } from "node:crypto";

export const token = (name) => ({ token: name });

export function darkTechTheme(overrides = {}) {
  return {
    id: randomUUID(),
    name: "Dark Tech",
    fonts: { display: "Inter", heading: "Inter", body: "Inter", mono: "JetBrains Mono" },
    colors: {
      background: "#0f172a",
      surface: "#1e293b",
      foreground: "#f8fafc",
      mutedForeground: "#94a3b8",
      primary: "#6366f1",
      primaryForeground: "#ffffff",
      accent: "#f59e0b",
      accentForeground: "#000000",
      border: "#334155",
      success: "#22c55e",
      warning: "#f59e0b",
      destructive: "#ef4444",
      ...(overrides.colors ?? {})
    },
    textStyles: {
      title: { fontFamily: "heading", fontSize: 72, fontWeight: 700, color: token("foreground") },
      subtitle: { fontFamily: "body", fontSize: 36, fontWeight: 400, color: token("mutedForeground") },
      heading: { fontFamily: "heading", fontSize: 48, fontWeight: 700, color: token("foreground") },
      body: { fontFamily: "body", fontSize: 28, fontWeight: 400, color: token("foreground") },
      caption: { fontFamily: "body", fontSize: 20, fontWeight: 400, color: token("mutedForeground") },
      code: { fontFamily: "mono", fontSize: 22, fontWeight: 400, color: token("accent") },
      ...(overrides.textStyles ?? {})
    },
    ...(overrides.theme ?? {})
  };
}

export function text(role, x, y, width, height, content, options = {}) {
  return {
    id: randomUUID(),
    type: "text",
    role,
    x,
    y,
    width: Math.max(1, width),
    height: Math.max(1, height),
    content,
    textAlign: options.textAlign ?? "left",
    verticalAlign: options.verticalAlign ?? "top",
    autoFit: options.autoFit ?? "shrink"
  };
}

export function richText(role, x, y, width, height, runs, options = {}) {
  return text(role, x, y, width, height, [{ kind: "block", runs }], options);
}

export function shape(x, y, width, height, fill = "surface", options = {}) {
  return {
    id: randomUUID(),
    type: "shape",
    x,
    y,
    width: Math.max(1, width),
    height: Math.max(1, height),
    shape: options.shape ?? "roundedRectangle",
    fill: token(fill),
    stroke: token(options.stroke ?? "border"),
    strokeWidth: options.strokeWidth ?? 1,
    cornerRadius: options.cornerRadius ?? 18,
    ...(options.opacity == null ? {} : { opacity: options.opacity })
  };
}

export function line(x, y, width, height = 2, options = {}) {
  const safeWidth = Math.max(1, width);
  const safeHeight = Math.max(1, height);
  return {
    id: randomUUID(),
    type: "line",
    x,
    y,
    width: safeWidth,
    height: safeHeight,
    line: options.line ?? "straight",
    start: { x: 0, y: 0 },
    end: { x: safeWidth, y: height <= 2 ? 0 : safeHeight },
    stroke: token(options.stroke ?? "border"),
    strokeWidth: options.strokeWidth ?? 2
  };
}

export function image(seedOrUrl, x, y, width, height, options = {}) {
  const isUrl = /^https?:\/\//.test(seedOrUrl);
  return {
    id: randomUUID(),
    type: "image",
    x,
    y,
    width: Math.max(1, width),
    height: Math.max(1, height),
    src: isUrl ? seedOrUrl : `https://picsum.photos/seed/${encodeURIComponent(seedOrUrl)}/1920/1080`,
    fit: options.fit ?? "cover",
    opacity: options.opacity ?? 1
  };
}

export function diagram(x, y, width, height, source) {
  return {
    id: randomUUID(),
    type: "diagram",
    x,
    y,
    width: Math.max(1, width),
    height: Math.max(1, height),
    engine: "mermaid",
    source
  };
}

export function chart(x, y, width, height, categories, series, chartType = "bar") {
  return {
    id: randomUUID(),
    type: "chart",
    x,
    y,
    width: Math.max(1, width),
    height: Math.max(1, height),
    chart: chartType,
    categories,
    series
  };
}

export function table(x, y, width, height, rows, options = {}) {
  return {
    id: randomUUID(),
    type: "table",
    x,
    y,
    width: Math.max(1, width),
    height: Math.max(1, height),
    rows: rows.length,
    cols: rows[0]?.length ?? 0,
    headerRow: options.headerRow ?? true,
    styling: {
      headerFill: token(options.headerFill ?? "primary"),
      headerText: { color: token("primaryForeground"), fontWeight: 700 },
      bodyFill: token(options.bodyFill ?? "surface"),
      bodyText: { color: token("foreground") },
      borderColor: token("border"),
      borderWidth: 1,
      cellPadding: "m",
      stripedRows: true
    },
    cells: rows.map((row) => row.map((cell) => ({ text: String(cell) })))
  };
}

export function card(x, y, width, height, heading, body, options = {}) {
  const base = shape(x, y, width, height, options.fill ?? "surface", {
    cornerRadius: options.cornerRadius ?? 18,
    opacity: options.opacity ?? 1
  });
  if (height <= 170) {
    return [
      base,
      text("body", x + 28, y + 20, width - 56, 40, heading),
      text("caption", x + 28, y + 68, width - 56, Math.max(32, height - 84), body)
    ];
  }
  if (height <= 240) {
    return [
      base,
      text("body", x + 30, y + 24, width - 60, 44, heading),
      text("caption", x + 30, y + 78, width - 60, Math.max(60, height - 98), body)
    ];
  }
  return [
    base,
    text("heading", x + 34, y + 30, width - 68, 64, heading),
    text("body", x + 34, y + 112, width - 68, Math.max(60, height - 140), body)
  ];
}

export function titleChip(label, x = 92, y = 74, width = 300) {
  return [
    shape(x, y, width, 46, "accent", { stroke: "accent", strokeWidth: 0, cornerRadius: 23 }),
    richText(
      "caption",
      x + 20,
      y + 8,
      width - 40,
      28,
      [{ kind: "span", text: label, style: { color: token("accentForeground"), fontWeight: 700 } }],
      { textAlign: "center", verticalAlign: "middle" }
    )
  ];
}

export function slide(objects, notes = "", speakerNotes = "", options = {}) {
  const animatable = objects.filter((object) => object.type !== "image").slice(0, options.maxAnimations ?? 8);
  return {
    id: randomUUID(),
    background: options.background ?? { kind: "solid", color: token("background") },
    objects,
    ...(notes ? { notes } : {}),
    ...(speakerNotes ? { speakerNotes: { content: speakerNotes } } : {}),
    animations: animatable.map((object, index) => ({
      id: randomUUID(),
      targetId: object.id,
      category: "entrance",
      effect: index === 0 ? "fade" : "float",
      trigger: index === 0 ? "onEnter" : "withPrevious",
      durationMs: index === 0 ? 600 : 420,
      delayMs: index * 90,
      easing: "easeOut"
    })),
    transitions: options.transitions ?? { effect: "fade", durationMs: 400 }
  };
}

export function section(title, slides) {
  return { id: randomUUID(), title, slides };
}

export function deck(title, sections, options = {}) {
  return {
    schema: "open-academy.slide-scene-graph",
    schemaVersion: "0.4.0",
    deck: {
      id: randomUUID(),
      title,
      width: 1920,
      height: 1080,
      theme: options.theme ?? darkTechTheme(),
      sections
    }
  };
}

export function processFlow(labels, x, y, width, height) {
  const gap = 36;
  const stepWidth = (width - gap * (labels.length - 1)) / labels.length;
  return labels.flatMap((item, index) => {
    const left = x + index * (stepWidth + gap);
    const objects = card(left, y, stepWidth, height, item.title, item.body);
    if (index < labels.length - 1) {
      objects.push(line(left + stepWidth, y + height / 2, gap, 2, { line: "arrow", stroke: "accent", strokeWidth: 4 }));
    }
    return objects;
  });
}

export function comparisonColumns(columns, x, y, width, height) {
  const gap = 46;
  const colWidth = (width - gap * (columns.length - 1)) / columns.length;
  return columns.flatMap((column, index) => {
    const left = x + index * (colWidth + gap);
    return card(left, y, colWidth, height, column.title, column.body, column.options ?? {});
  });
}
