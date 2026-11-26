import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const here = dirname(fileURLToPath(import.meta.url));
const paper = resolve(here, "..");
const output = process.argv[2] ? resolve(process.argv[2]) : paper;
const dataPath = join(here, "study-results-2026-11-15.json");
const payload = await readFile(dataPath);
const data = JSON.parse(payload);
const dataHash = createHash("sha256").update(payload).digest("hex");
const WIDTH = 960;
const MIN_FONT = 16;
const MODELS = ["claude-sonnet-5.5", "gemini-4-argon", "gpt-6.1-sol"];
const ARMS = ["A", "B", "C", "D", "E"];
const ARM_COLOURS = {
  A: "#b8332a", B: "#1b5e20", C: "#5c2d91", D: "#b26a00", E: "#00695c",
};
const ARM_DASH = { A: "", B: "", C: "5,3", D: "2,2", E: "7,3,2,3" };
const MODEL_LABELS = {
  "claude-sonnet-5.5": "Claude Sonnet 5.5",
  "gemini-4-argon": "Gemini 4 Argon",
  "gpt-6.1-sol": "GPT 6.1 Sol",
};

function esc(value) {
  return String(value).replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function text(lines, x, y, value, { size = MIN_FONT, anchor = "start",
  bold = false, colour = "#222222", transform = "" } = {}) {
  lines.push(`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" font-weight="${bold ? "bold" : "normal"}" fill="${colour}"${transform ? ` transform="${transform}"` : ""}>${esc(value)}</text>`);
}

function line(lines, x1, y1, x2, y2, colour = "#e6ebf1", width = 0.8, dash = "") {
  lines.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${colour}" stroke-width="${width}"${dash ? ` stroke-dasharray="${dash}"` : ""}/>`);
}

function panel(lines, x, y, width, height) {
  lines.push(`<rect x="${x}" y="${y}" width="${width}" height="${height}" fill="#fafafa" stroke="#d0d7de"/>`);
}

function startSvg(height) {
  return [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${height}" viewBox="0 0 ${WIDTH} ${height}" data-source-sha256="${dataHash}" data-final-width-cm="16" data-min-font-size="${MIN_FONT}" style="font-family: Georgia, 'Times New Roman', serif; background: #ffffff;">`,
    `<rect width="${WIDTH}" height="${height}" fill="#ffffff"/>`,
  ];
}

function buildTrajectoriesSvg() {
  const height = 800;
  const lines = startSvg(height);
  const legend = [
    ["A", "Arm A: Feature only (30m)", 24, 24],
    ["B", "Arm B: Consolidation + ./tcr (30+15m)", 480, 24],
    ["C", "Arm C: Read-only review (30+15m)", 24, 50],
    ["D", "Arm D: Longer session (45m)", 480, 50],
    ["E", "Arm E: Visible-spec repair (30+15m)", 24, 76],
  ];
  for (const [arm, label, x, y] of legend) {
    line(lines, x, y - 5, x + 24, y - 5, ARM_COLOURS[arm], 2.4, ARM_DASH[arm]);
    lines.push(`<circle cx="${x + 12}" cy="${y - 5}" r="3.2" fill="${ARM_COLOURS[arm]}"/>`);
    text(lines, x + 32, y, label);
  }
  const panelW = 250;
  const panelH = 180;
  const complexityMaximum = Math.ceil(Math.max(1, ...MODELS.flatMap(model =>
    ARMS.flatMap(arm => data.series_means[model][arm].map(pt => pt.share_ccn_over_10_pct)))));

  MODELS.forEach((model, index) => {
    const x0 = 85 + index * 300;
    text(lines, x0 + panelW / 2, 110, MODEL_LABELS[model],
      { size: 19, anchor: "middle", bold: true, colour: "#1f4e79" });
    text(lines, x0 + panelW / 2, 132, "n = 21/arm", { anchor: "middle" });
    for (const [metric, y0, min, max, ticks] of [
      ["pass_rate", 145, 88, 100.5, [88, 90, 92, 94, 96, 98, 100]],
      ["share_ccn_over_10_pct", 484, 0, complexityMaximum,
        Array.from({ length: complexityMaximum + 1 }, (_, i) => i)],
    ]) {
      const xOfK = k => x0 + (k - 1) / 9 * panelW;
      const yOfValue = value => y0 + panelH - (value - min) / (max - min) * panelH;
      if (metric !== "pass_rate") {
        text(lines, x0 + panelW / 2, y0 - 14, MODEL_LABELS[model],
          { size: 19, anchor: "middle", bold: true, colour: "#1f4e79" });
      }
      panel(lines, x0, y0, panelW, panelH);
      for (const tick of ticks) {
        const y = yOfValue(tick);
        line(lines, x0, y, x0 + panelW, y);
        if (index === 0) text(lines, x0 - 8, y + 5, `${tick}%`, { anchor: "end" });
      }
      for (let k = 1; k <= 10; k++) {
        const x = xOfK(k);
        line(lines, x, y0, x, y0 + panelH, "#f0f3f6", 0.7);
        text(lines, x + (k === 10 ? 5 : 0), y0 + panelH + 24, `F${k}`, { anchor: "middle" });
      }
      if (index === 0) {
        const y = y0 + panelH / 2;
        text(lines, 19, y,
          metric === "pass_rate" ? "Hidden pass rate (%)" : "Functions > CCN 10 (%)",
          { size: 17, anchor: "middle", bold: true, transform: `rotate(-90 19 ${y})` });
      }
      for (const arm of ARMS) {
        const points = data.series_means[model][arm];
        const path = points.map((pt, i) =>
          `${i ? "L" : "M"}${xOfK(pt.k).toFixed(1)},${yOfValue(pt[metric]).toFixed(1)}`).join(" ");
        lines.push(`<path data-model="${model}" data-arm="${arm}" data-metric="${metric}" d="${path}" fill="none" stroke="${ARM_COLOURS[arm]}" stroke-width="${arm === "B" ? 2.5 : 1.8}"${ARM_DASH[arm] ? ` stroke-dasharray="${ARM_DASH[arm]}"` : ""}/>`);
        for (const pt of points) {
          lines.push(`<circle cx="${xOfK(pt.k).toFixed(1)}" cy="${yOfValue(pt[metric]).toFixed(1)}" r="${arm === "B" ? 3 : 2.3}" fill="${ARM_COLOURS[arm]}"/>`);
        }
      }
    }
  });
  text(lines, WIDTH / 2, 378, "Higher pass rate is better; lines are 21-run means",
    { anchor: "middle" });
  text(lines, WIDTH / 2, 407, "GPT F9 ranking allowlist lock (k = 9..10): B & E = 95.28% (12/21 runs at 100%);",
    { anchor: "middle", bold: true });
  text(lines, WIDTH / 2, 431, "C = 93.18% (8/21) · D = 92.13% · A = 91.60%.", { anchor: "middle" });
  text(lines, WIDTH / 2, 717, "Lower is better: B at P10 = 0% (21 runs per model)",
    { anchor: "middle", bold: true, colour: "#1b5e20" });
  text(lines, WIDTH / 2, 751,
    "P1..P10: 3,150 end-of-cycle states; 315 completed trajectories, owner-attested unassisted.",
    { anchor: "middle" });
  text(lines, WIDTH / 2, 777,
    "P10 open regressions: 0/252 trajectories in Arms A-D; 1/21 in Gemini E.",
    { anchor: "middle" });
  return [...lines, "</svg>"].join("\n");
}

function buildOutcomesCostsSvg() {
  const height = 980;
  const lines = startSvg(height);
  const ax0 = 215, ay0 = 54, aw = 215, ah = 340;
  const xOfDiff = value => ax0 + (value + 3.8) / 14.4 * aw;
  text(lines, 230, 25, "(a) P10 coverage contrasts (95% CI)",
    { size: 19, anchor: "middle", bold: true, colour: "#1f4e79" });
  panel(lines, ax0, ay0, aw, ah);
  for (const tick of [-3, 0, 3, 6, 10]) {
    const x = xOfDiff(tick);
    const reference = tick === 0 || tick === 10;
    line(lines, x, ay0, x, ay0 + ah,
      tick === 10 ? "#b8332a" : tick === 0 ? "#333333" : "#e6ebf1",
      reference ? 1.2 : 0.8, reference ? "3,2" : "");
    text(lines, x, 418, tick > 0 ? `+${tick}` : tick, { anchor: "middle" });
  }
  text(lines, xOfDiff(10) - 5, 73, "Target +10 pp",
    { anchor: "end", bold: true, colour: "#b8332a" });
  const forestRows = [
    ["Pooled B - D (primary)", null, "B-D", "#1b5e20", true],
    ["Pooled B - A", null, "B-A", "#1b5e20", false],
    ["Pooled B - C", null, "B-C", "#5c2d91", false],
    ["Pooled E - B", null, "E-B", "#00695c", false],
    ["Sonnet B - D", MODELS[0], "B-D", "#1f4e79", false],
    ["Sonnet B - A", MODELS[0], "B-A", "#1f4e79", false],
    ["Gemini B - D", MODELS[1], "B-D", "#8a5a00", false],
    ["Gemini B - A", MODELS[1], "B-A", "#8a5a00", false],
    ["GPT 6.1 B - D", MODELS[2], "B-D", "#b8332a", true],
    ["GPT 6.1 B - A", MODELS[2], "B-A", "#b8332a", true],
    ["GPT 6.1 B - C", MODELS[2], "B-C", "#b8332a", false],
  ];
  forestRows.forEach(([label, model, contrast, colour, bold], index) => {
    const estimate = model ? data.within_model_contrasts[model][contrast] : data.pooled_contrasts[contrast];
    const interval = model ? estimate.h1_ci : estimate.h1_bootstrap_95_ci;
    const difference = model ? estimate.h1_diff : estimate.h1_pass_rate_diff_pct_points;
    const y = 94 + index * 27;
    if ([4, 6, 8].includes(index)) line(lines, ax0, y - 14, ax0 + aw, y - 14, "#d0d7de");
    text(lines, ax0 - 8, y + 5, label, { anchor: "end", bold });
    lines.push(`<g data-model="${model || "pooled"}" data-contrast="${contrast}">`);
    line(lines, xOfDiff(interval[0]), y, xOfDiff(interval[1]), y, colour, bold ? 2.2 : 1.6);
    for (const value of interval) line(lines, xOfDiff(value), y - 4, xOfDiff(value), y + 4, colour, 1.4);
    lines.push(`<circle cx="${xOfDiff(difference)}" cy="${y}" r="${bold ? 3.5 : 2.8}" fill="${colour}"/></g>`);
  });
  text(lines, 230, 444, "Difference in P10 pass rate", { anchor: "middle" });
  text(lines, 230, 466, "(percentage points)", { anchor: "middle" });
  text(lines, 230, 488, "Right of 0 favors first arm; +10 is the target", { anchor: "middle" });
  text(lines, 230, 510, "CI includes 0: direction uncertain", { anchor: "middle" });

  const bx0 = 590, by0 = 54, bw = 340, bh = 340;
  const xOfCr = count => bx0 + count / 21 * bw;
  text(lines, 745, 25, "(b) CR1 adaptation outcomes (21/cell)",
    { size: 19, anchor: "middle", bold: true, colour: "#1f4e79" });
  panel(lines, bx0, by0, bw, bh);
  for (const tick of [0, 5, 10, 15, 21]) {
    const x = xOfCr(tick);
    line(lines, x, by0, x, by0 + bh);
    text(lines, x, 418, tick, { anchor: "middle" });
  }
  data.cells.forEach((cell, index) => {
    const y = 69 + index * 22.5;
    const model = cell.model.startsWith("claude") ? "Sonnet"
      : cell.model.startsWith("gemini") ? "Gemini" : "GPT 6.1";
    if ([5, 10].includes(index)) line(lines, bx0 - 85, y - 11, bx0 + bw, y - 11, "#c8d1d9");
    text(lines, bx0 - 8, y + 5, `${model} ${cell.arm}`, { anchor: "end" });
    lines.push(`<g data-model="${cell.model}" data-arm="${cell.arm}" data-metric="cr1">`);
    let start = 0;
    for (const [field, colour] of [
      ["cr1_pass", "#2e7d32"], ["cr1_fail", "#d9534f"], ["cr1_missing", "#7f8c8d"],
    ]) {
      if (cell[field]) {
        lines.push(`<rect data-outcome="${field}" x="${xOfCr(start)}" y="${y - 8.5}" width="${cell[field] / 21 * bw}" height="17" fill="${colour}"/>`);
      }
      start += cell[field];
    }
    text(lines, xOfCr(cell.cr1_pass / 2), y + 5, cell.cr1_pass,
      { anchor: "middle", bold: true, colour: "#ffffff" });
    lines.push("</g>");
  });
  for (const [x, label, colour] of [
    [590, "Pass", "#2e7d32"], [690, "Fail", "#d9534f"], [780, "Unknown", "#7f8c8d"],
  ]) {
    lines.push(`<rect x="${x}" y="432" width="17" height="17" fill="${colour}"/>`);
    text(lines, x + 24, 446, label);
  }
  text(lines, 745, 468, "More passes is better; grey is unknown", { anchor: "middle" });
  text(lines, 745, 490, "Read alongside P10 feature completeness", { anchor: "middle" });

  text(lines, WIDTH / 2, 540, "(c) P10 coverage vs settled delivery credits",
    { size: 19, anchor: "middle", bold: true, colour: "#1f4e79" });
  const offsets = {
    "claude-sonnet-5.5": { A: [-8, 32], B: [26, -17], C: [18, 30], D: [22, 54], E: [-20, -15] },
    "gemini-4-argon": { A: [-10, 32], B: [26, -15], C: [-12, -17], D: [24, 54], E: [-17, 40] },
    "gpt-6.1-sol": { A: [-8, 22], B: [-13, -13], C: [-12, 22], D: [14, -12], E: [15, 20] },
  };
  MODELS.forEach((model, index) => {
    const x0 = 85 + index * 300, y0 = 600, pw = 250, ph = 200;
    const xOfCost = value => x0 + (value - 35) / 290 * pw;
    const yOfPass = value => y0 + ph - (value - 90.5) / 9.9 * ph;
    text(lines, x0 + pw / 2, 570, MODEL_LABELS[model],
      { size: 19, anchor: "middle", bold: true, colour: "#1f4e79" });
    panel(lines, x0, y0, pw, ph);
    for (const tick of [50, 100, 150, 200, 250, 300]) {
      const x = xOfCost(tick);
      line(lines, x, y0, x, y0 + ph);
      text(lines, x, 824, tick, { anchor: "middle" });
    }
    for (const tick of [91, 93, 95, 97, 99, 100]) {
      const y = yOfPass(tick);
      line(lines, x0, y, x0 + pw, y);
      if (index === 0) text(lines, x0 - 8, y + 5, `${tick}%`, { anchor: "end" });
    }
    if (index === 0) {
      text(lines, 19, y0 + ph / 2, "P10 hidden pass rate (%)",
        { size: 17, anchor: "middle", bold: true, transform: `rotate(-90 19 ${y0 + ph / 2})` });
    }
    const cells = data.cells.filter(cell => cell.model === model);
    for (const cell of cells) {
      const x = xOfCost(cell.delivery_credits_mean), y = yOfPass(cell.p10_mean);
      const [dx, dy] = offsets[model][cell.arm];
      const lx = x + dx, ly = y + dy, colour = ARM_COLOURS[cell.arm];
      line(lines, x, y, lx + (dx < 0 ? 2 : -2), ly - 5, colour);
      lines.push(`<circle data-model="${model}" data-arm="${cell.arm}" data-metric="cost-coverage" cx="${x}" cy="${y}" r="4" fill="${colour}" stroke="#ffffff"/>`);
      text(lines, lx, ly, cell.arm, { size: 18, anchor: dx < 0 ? "end" : "start", bold: true, colour });
    }
    text(lines, x0, 882, `n: ${cells.map(cell => `${cell.arm}[${cell.delivery_credits_n}]`).join(" ")}`);
  });
  text(lines, WIDTH / 2, 852, "Mean settled delivery AI credits", { anchor: "middle" });
  text(lines, WIDTH / 2, 908, "Coverage uses all 21; brackets show completely billed n for delivery credits.",
    { anchor: "middle" });
  text(lines, WIDTH / 2, 934,
    "Up = more coverage; left = fewer credits. Prefer upper-left at comparable outcomes",
    { anchor: "middle" });
  text(lines, WIDTH / 2, 960, "Similar A/D means do not establish equivalence.", { anchor: "middle" });
  return [...lines, "</svg>"].join("\n");
}

const charts = [
  ["fig-study-trajectories", buildTrajectoriesSvg(), 800],
  ["fig-study-outcomes-costs", buildOutcomesCostsSvg(), 980],
];
await mkdir(output, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  channel: process.env.PAPER_BROWSER_CHANNEL || undefined,
  executablePath: process.env.PAPER_BROWSER_EXECUTABLE || undefined,
});
try {
  const context = await browser.newContext({ deviceScaleFactor: 3 });
  await context.route(/^https?:/, route => route.abort());
  const page = await context.newPage();
  for (const [stem, svg, height] of charts) {
    await page.setViewportSize({ width: WIDTH, height });
    await page.setContent(`<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:#fff;}</style>${svg}`);
    const issues = await page.locator("svg").evaluate((root) => {
      const width = root.viewBox.baseVal.width, height = root.viewBox.baseVal.height;
      const errors = [];
      const boxes = [...root.querySelectorAll("text")].map(node => {
        const bounds = node.getBoundingClientRect();
        const font = parseFloat(getComputedStyle(node).fontSize);
        if (font * (16 / 2.54 * 72) / width < 7) errors.push(`Small text: ${node.textContent}`);
        if (bounds.left < 0 || bounds.top < 0 || bounds.right > width || bounds.bottom > height) {
          errors.push(`Clipped text: ${node.textContent}`);
        }
        return { label: node.textContent, bounds };
      });
      for (let i = 0; i < boxes.length; i++) {
        for (const other of boxes.slice(i + 1)) {
          const a = boxes[i].bounds, b = other.bounds;
          if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 1
              && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 1) {
            errors.push(`Overlapping text: ${boxes[i].label} / ${other.label}`);
          }
        }
      }
      return errors;
    });
    if (issues.length) throw new Error(`${stem}:\n${issues.join("\n")}`);
    await writeFile(join(output, `${stem}.svg`), svg + "\n", "utf8");
    const png = await page.locator("svg").screenshot({ type: "png" });
    await writeFile(join(output, `${stem}.png`), png);
    console.log(`Exported ${stem}: ${WIDTH}x${height}; minimum ${(MIN_FONT * (16 / 2.54 * 72) / WIDTH).toFixed(2)} pt at 16 cm (3x PNG ${png.length} bytes); no clipped or overlapping text`);
  }
} finally {
  await browser.close();
}
