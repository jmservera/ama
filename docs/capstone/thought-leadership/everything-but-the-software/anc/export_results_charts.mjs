import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const here = dirname(fileURLToPath(import.meta.url));
const paper = resolve(here, "..");
const output = process.argv[2] ? resolve(process.argv[2]) : paper;
const dataPath = join(here, "study-results-2026-11-15.json");
const data = JSON.parse(await readFile(dataPath, "utf8"));
const dataHash = createHash("sha256").update(await readFile(dataPath)).digest("hex");

const ARM_COLOURS = {
  A: "#b8332a",
  B: "#1b5e20",
  C: "#5c2d91",
  D: "#b26a00",
  E: "#00695c",
};

const ARM_DASH = {
  A: "",
  B: "",
  C: "5,3",
  D: "2,2",
  E: "7,3,2,3",
};

const MODEL_LABELS = {
  "claude-sonnet-5.5": "Claude Sonnet 5.5",
  "gemini-4-argon": "Gemini 4 Argon",
  "gpt-6.1-sol": "GPT 6.1 Sol",
};

function esc(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function buildTrajectoriesSvg() {
  const width = 1080;
  const height = 560;
  const models = ["claude-sonnet-5.5", "gemini-4-argon", "gpt-6.1-sol"];
  const arms = ["A", "B", "C", "D", "E"];
  const panelW = 290;
  const panelH = 175;
  const left0 = 72;
  const gapX = 48;
  const topRowY = 74;
  const botRowY = 308;
  const complexityMaximum = Math.ceil(Math.max(1, ...models.flatMap((model) =>
    arms.flatMap((arm) => data.series_means[model][arm].map((point) => point.share_ccn_over_10_pct))
  )));

  const lines = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" data-source-sha256="${dataHash}" style="font-family: Georgia, 'Times New Roman', serif; background: #ffffff;">`,
    `<rect width="${width}" height="${height}" fill="#ffffff"/>`,
    `<text x="${width / 2}" y="26" text-anchor="middle" font-size="15" font-weight="bold" fill="#111111">Mean Hidden-Test Pass Rate and Complexity Hotspots Across 315 Completed Trajectories (k = 1..10)</text>`,
  ];

  // Legend at top
  const legendItems = [
    ["A", "Arm A: Feature only (30m)"],
    ["B", "Arm B: Consolidation + ./tcr (30+15m)"],
    ["C", "Arm C: Read-only review (30+15m)"],
    ["D", "Arm D: Longer session (45m)"],
    ["E", "Arm E: Visible-spec repair (30+15m)"],
  ];
  let lx = 68;
  for (const [arm, label] of legendItems) {
    const col = ARM_COLOURS[arm];
    const dash = ARM_DASH[arm] ? ` stroke-dasharray="${ARM_DASH[arm]}"` : "";
    lines.push(`<line x1="${lx}" y1="46" x2="${lx + 24}" y2="46" stroke="${col}" stroke-width="2.4"${dash}/>`);
    lines.push(`<circle cx="${lx + 12}" cy="46" r="3.2" fill="${col}"/>`);
    lines.push(`<text x="${lx + 30}" y="50" font-size="11" fill="#222222">${esc(label)}</text>`);
    lx += arm === "B" ? 228 : arm === "C" ? 198 : arm === "E" ? 210 : 168;
  }

  models.forEach((model, mIdx) => {
    const x0 = left0 + mIdx * (panelW + gapX);

    // Top row: Pass rate (88% to 100.5%)
    const y0 = topRowY;
    const yMin = 88;
    const yMax = 100.5;
    const xOfK = (k) => x0 + ((k - 1) / 9) * panelW;
    const yOfPass = (v) => y0 + panelH - ((v - yMin) / (yMax - yMin)) * panelH;

    lines.push(`<text x="${x0 + panelW / 2}" y="${y0 - 10}" text-anchor="middle" font-size="13" font-weight="bold" fill="#1f4e79">${esc(MODEL_LABELS[model])} (n = 21/arm)</text>`);
    lines.push(`<rect x="${x0}" y="${y0}" width="${panelW}" height="${panelH}" fill="#fafafa" stroke="#d0d7de" stroke-width="1"/>`);

    for (const tick of [88, 90, 92, 94, 96, 98, 100]) {
      const ty = yOfPass(tick);
      lines.push(`<line x1="${x0}" y1="${ty.toFixed(1)}" x2="${x0 + panelW}" y2="${ty.toFixed(1)}" stroke="#e6ebf1" stroke-width="0.8"/>`);
      if (mIdx === 0) {
        lines.push(`<text x="${x0 - 7}" y="${(ty + 3.5).toFixed(1)}" text-anchor="end" font-size="10" fill="#444444">${tick}%</text>`);
      }
    }
    for (let k = 1; k <= 10; k++) {
      const kx = xOfK(k);
      lines.push(`<line x1="${kx.toFixed(1)}" y1="${y0}" x2="${kx.toFixed(1)}" y2="${y0 + panelH}" stroke="#f0f3f6" stroke-width="0.7"/>`);
      lines.push(`<text x="${kx.toFixed(1)}" y="${y0 + panelH + 15}" text-anchor="middle" font-size="10" fill="#444444">F${k}</text>`);
    }
    if (mIdx === 0) {
      lines.push(`<text x="${x0 - 46}" y="${y0 + panelH / 2}" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#222222" transform="rotate(-90 ${x0 - 46} ${y0 + panelH / 2})">Hidden pass rate (%)</text>`);
    }

    for (const arm of arms) {
      const pts = data.series_means[model][arm];
      const col = ARM_COLOURS[arm];
      const dash = ARM_DASH[arm] ? ` stroke-dasharray="${ARM_DASH[arm]}"` : "";
      const d = pts
        .map((pt, idx) => `${idx === 0 ? "M" : "L"}${xOfK(pt.k).toFixed(1)},${yOfPass(pt.pass_rate).toFixed(1)}`)
        .join(" ");
      lines.push(`<path d="${d}" fill="none" stroke="${col}" stroke-width="${arm === "B" ? 2.5 : 1.8}"${dash}/>`);
      for (const pt of pts) {
        lines.push(`<circle cx="${xOfK(pt.k).toFixed(1)}" cy="${yOfPass(pt.pass_rate).toFixed(1)}" r="${arm === "B" ? 3.0 : 2.3}" fill="${col}"/>`);
      }
    }

    if (model === "gpt-6.1-sol") {
      lines.push(`<rect x="${x0 + 8}" y="${y0 + panelH - 56}" width="188" height="48" rx="3" fill="#ffffff" fill-opacity="0.92" stroke="#d0d7de" stroke-width="0.8"/>`);
      lines.push(`<text x="${x0 + 14}" y="${y0 + panelH - 41}" font-size="9.2" font-weight="bold" fill="#222222">F9 ranking allowlist lock (k = 9..10):</text>`);
      lines.push(`<text x="${x0 + 14}" y="${y0 + panelH - 27}" font-size="9.0" fill="#1b5e20">B &amp; E: 95.28% (12/21 runs at 100%)</text>`);
      lines.push(`<text x="${x0 + 14}" y="${y0 + panelH - 14}" font-size="9.0" fill="#b8332a">C: 93.18% (8/21) · D: 92.13% · A: 91.60%</text>`);
    }

    lines.push(`<text x="${x0 + panelW / 2}" y="${y0 + panelH + 35}" text-anchor="middle" font-size="10" fill="#222222">Higher pass rate is better; lines are 21-run means</text>`);
    const by0 = botRowY;
    const cMax = complexityMaximum;
    const yOfCcn = (v) => by0 + panelH - (v / cMax) * panelH;

    lines.push(`<text x="${x0 + panelW / 2}" y="${by0 - 10}" text-anchor="middle" font-size="12" font-weight="bold" fill="#333333">${esc(MODEL_LABELS[model])}: Functions &gt; CCN 10</text>`);
    lines.push(`<rect x="${x0}" y="${by0}" width="${panelW}" height="${panelH}" fill="#fafafa" stroke="#d0d7de" stroke-width="1"/>`);

    for (let tick = 0; tick <= cMax; tick++) {
      const ty = yOfCcn(tick);
      lines.push(`<line x1="${x0}" y1="${ty.toFixed(1)}" x2="${x0 + panelW}" y2="${ty.toFixed(1)}" stroke="#e6ebf1" stroke-width="0.8"/>`);
      if (mIdx === 0) {
        lines.push(`<text x="${x0 - 7}" y="${(ty + 3.5).toFixed(1)}" text-anchor="end" font-size="10" fill="#444444">${tick}%</text>`);
      }
    }
    for (let k = 1; k <= 10; k++) {
      const kx = xOfK(k);
      lines.push(`<line x1="${kx.toFixed(1)}" y1="${by0}" x2="${kx.toFixed(1)}" y2="${by0 + panelH}" stroke="#f0f3f6" stroke-width="0.7"/>`);
      lines.push(`<text x="${kx.toFixed(1)}" y="${by0 + panelH + 15}" text-anchor="middle" font-size="10" fill="#444444">F${k}</text>`);
    }
    if (mIdx === 0) {
      lines.push(`<text x="${x0 - 46}" y="${by0 + panelH / 2}" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#222222" transform="rotate(-90 ${x0 - 46} ${by0 + panelH / 2})">Functions &gt; CCN 10 (%)</text>`);
    }

    for (const arm of arms) {
      const pts = data.series_means[model][arm];
      const col = ARM_COLOURS[arm];
      const dash = ARM_DASH[arm] ? ` stroke-dasharray="${ARM_DASH[arm]}"` : "";
      const d = pts
        .map((pt, idx) => `${idx === 0 ? "M" : "L"}${xOfK(pt.k).toFixed(1)},${yOfCcn(pt.share_ccn_over_10_pct).toFixed(1)}`)
        .join(" ");
      lines.push(`<path d="${d}" fill="none" stroke="${col}" stroke-width="${arm === "B" ? 2.5 : 1.8}"${dash}/>`);
      for (const pt of pts) {
        lines.push(`<circle cx="${xOfK(pt.k).toFixed(1)}" cy="${yOfCcn(pt.share_ccn_over_10_pct).toFixed(1)}" r="${arm === "B" ? 3.0 : 2.3}" fill="${col}"/>`);
      }
    }
    lines.push(`<text x="${x0 + panelW / 2}" y="${by0 + panelH + 37}" text-anchor="middle" font-size="10" fill="#1b5e20" font-weight="bold">Lower is better: B at P10 = 0% (21 runs)</text>`);
  });

  lines.push(`<text x="${width / 2}" y="${height - 14}" text-anchor="middle" font-size="10.5" fill="#444444">P1..P10: 3,150 end-of-cycle states; 315 completed trajectories, owner-attested unassisted. P10 open regressions: 0/252 trajectories in Arms A-D; 1/21 in Gemini E.</text>`);
  lines.push(`</svg>`);
  return lines.join("\n");
}

function buildOutcomesCostsSvg() {
  const width = 1120;
  const height = 470;
  const lines = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" data-source-sha256="${dataHash}" style="font-family: Georgia, 'Times New Roman', serif; background: #ffffff;">`,
    `<rect width="${width}" height="${height}" fill="#ffffff"/>`,
    `<text x="${width / 2}" y="25" text-anchor="middle" font-size="14.5" font-weight="bold" fill="#111111">Complete 315/315 Benchmark Outcomes: (a) P10 Coverage Contrasts, (b) CR1 Adaptation, and (c) Delivery Credits vs Coverage</text>`,
  ];

  // Panel (a): Forest plot of H1 P10 coverage contrasts (x: -4 to +10.5 pp)
  const ax0 = 135;
  const ay0 = 64;
  const aw = 215;
  const ah = 305;
  const cMin = -3.8;
  const cMax = 10.6;
  const xOfDiff = (v) => ax0 + ((v - cMin) / (cMax - cMin)) * aw;

  lines.push(`<text x="${ax0 + aw / 2}" y="${ay0 - 12}" text-anchor="middle" font-size="12" font-weight="bold" fill="#1f4e79">(a) P10 Coverage Contrasts (95% CI)</text>`);
  lines.push(`<rect x="${ax0}" y="${ay0}" width="${aw}" height="${ah}" fill="#fafafa" stroke="#d0d7de" stroke-width="1"/>`);

  for (const tick of [-3, 0, 3, 6, 10]) {
    const tx = xOfDiff(tick);
    const isZero = tick === 0;
    const isThresh = tick === 10;
    lines.push(`<line x1="${tx.toFixed(1)}" y1="${ay0}" x2="${tx.toFixed(1)}" y2="${ay0 + ah}" stroke="${isThresh ? "#b8332a" : isZero ? "#333333" : "#e6ebf1"}" stroke-width="${isZero || isThresh ? 1.2 : 0.8}"${isThresh || isZero ? ' stroke-dasharray="3,2"' : ""}/>`);
    lines.push(`<text x="${tx.toFixed(1)}" y="${ay0 + ah + 14}" text-anchor="middle" font-size="9.5" fill="${isThresh ? "#b8332a" : "#444444"}">${tick > 0 ? `+${tick}` : tick}</text>`);
  }
  lines.push(`<text x="${xOfDiff(10) - 3}" y="${ay0 + 13}" text-anchor="end" font-size="8.5" fill="#b8332a" font-weight="bold">Target +10 pp</text>`);
  lines.push(`<text x="${ax0 + aw / 2}" y="${ay0 + ah + 30}" text-anchor="middle" font-size="10.5" fill="#222222">Difference in P10 pass rate (percentage points)</text>`);
  lines.push(`<text x="${ax0 + aw / 2}" y="${ay0 + ah + 46}" text-anchor="middle" font-size="9.5" fill="#222222">Right of 0 favors first arm; +10 is the target</text>`);
  lines.push(`<text x="${ax0 + aw / 2}" y="${ay0 + ah + 61}" text-anchor="middle" font-size="9" fill="#444444">CI includes 0: direction uncertain</text>`);

  const forestRows = [
    { label: "Pooled B - D (primary)", diff: 1.19, lo: 0.10, hi: 2.22, col: "#1b5e20", bold: true },
    { label: "Pooled B - A", diff: 1.41, lo: 0.33, hi: 2.45, col: "#1b5e20", bold: false },
    { label: "Pooled B - C", diff: 0.66, lo: -0.45, hi: 1.75, col: "#5c2d91", bold: false },
    { label: "Pooled E - B", diff: 0.04, lo: -1.07, hi: 1.14, col: "#00695c", bold: false },
    { label: "Sonnet B - D", diff: 0.26, lo: -0.15, hi: 0.75, col: "#1f4e79", bold: false },
    { label: "Sonnet B - A", diff: 0.22, lo: -0.19, hi: 0.71, col: "#1f4e79", bold: false },
    { label: "Gemini B - D", diff: 0.15, lo: -0.15, hi: 0.52, col: "#8a5a00", bold: false },
    { label: "Gemini B - A", diff: 0.34, lo: -0.07, hi: 0.82, col: "#8a5a00", bold: false },
    { label: "GPT 6.1 B - D", diff: 3.15, lo: 0.00, hi: 6.30, col: "#b8332a", bold: true },
    { label: "GPT 6.1 B - A", diff: 3.67, lo: 0.52, hi: 6.82, col: "#b8332a", bold: true },
    { label: "GPT 6.1 B - C", diff: 2.10, lo: -1.05, hi: 5.25, col: "#b8332a", bold: false },
  ];

  forestRows.forEach((row, idx) => {
    const contrast = row.label.match(/([A-E]) - ([A-E])/).slice(1).join("-");
    const model = row.label.startsWith("Sonnet") ? "claude-sonnet-5.5"
      : row.label.startsWith("Gemini") ? "gemini-4-argon"
      : row.label.startsWith("GPT") ? "gpt-6.1-sol" : null;
    const estimate = model ? data.within_model_contrasts[model][contrast] : data.pooled_contrasts[contrast];
    const interval = model ? estimate.h1_ci : estimate.h1_bootstrap_95_ci;
    row = { ...row, diff: model ? estimate.h1_diff : estimate.h1_pass_rate_diff_pct_points,
      lo: interval[0], hi: interval[1] };
    const ry = ay0 + 20 + idx * 26.2;
    if (idx === 4 || idx === 6 || idx === 8) {
      lines.push(`<line x1="${ax0}" y1="${(ry - 13).toFixed(1)}" x2="${ax0 + aw}" y2="${(ry - 13).toFixed(1)}" stroke="#d0d7de" stroke-width="0.8"/>`);
    }
    lines.push(`<text x="${ax0 - 6}" y="${(ry + 3.5).toFixed(1)}" text-anchor="end" font-size="9.5" font-weight="${row.bold ? "bold" : "normal"}" fill="#222222">${esc(row.label)}</text>`);
    const xLo = xOfDiff(row.lo);
    const xHi = xOfDiff(row.hi);
    const xPt = xOfDiff(row.diff);
    lines.push(`<line x1="${xLo.toFixed(1)}" y1="${ry.toFixed(1)}" x2="${xHi.toFixed(1)}" y2="${ry.toFixed(1)}" stroke="${row.col}" stroke-width="${row.bold ? 2.2 : 1.6}"/>`);
    lines.push(`<line x1="${xLo.toFixed(1)}" y1="${(ry - 3.5).toFixed(1)}" x2="${xLo.toFixed(1)}" y2="${(ry + 3.5).toFixed(1)}" stroke="${row.col}" stroke-width="1.4"/>`);
    lines.push(`<line x1="${xHi.toFixed(1)}" y1="${(ry - 3.5).toFixed(1)}" x2="${xHi.toFixed(1)}" y2="${(ry + 3.5).toFixed(1)}" stroke="${row.col}" stroke-width="1.4"/>`);
    lines.push(`<circle cx="${xPt.toFixed(1)}" cy="${ry.toFixed(1)}" r="${row.bold ? 3.5 : 2.8}" fill="${row.col}"/>`);
  });

  // Panel (b): CR1 Outcomes across 15 cells (out of 21 allocated runs per cell)
  const bx0 = 445;
  const by0 = 64;
  const bw = 240;
  const bh = 305;
  const xOfCr = (cnt) => bx0 + (cnt / 21) * bw;

  lines.push(`<text x="${bx0 + bw / 2}" y="${by0 - 12}" text-anchor="middle" font-size="12" font-weight="bold" fill="#1f4e79">(b) CR1 Adaptation Outcomes (21/cell)</text>`);
  lines.push(`<rect x="${bx0}" y="${by0}" width="${bw}" height="${bh}" fill="#fafafa" stroke="#d0d7de" stroke-width="1"/>`);

  for (const tick of [0, 5, 10, 15, 21]) {
    const tx = xOfCr(tick);
    lines.push(`<line x1="${tx.toFixed(1)}" y1="${by0}" x2="${tx.toFixed(1)}" y2="${by0 + bh}" stroke="#e6ebf1" stroke-width="0.8"/>`);
    lines.push(`<text x="${tx.toFixed(1)}" y="${by0 + bh + 14}" text-anchor="middle" font-size="9.5" fill="#444444">${tick}</text>`);
  }
  lines.push(`<text x="${bx0 + bw / 2}" y="${by0 + bh + 30}" text-anchor="middle" font-size="10.5" fill="#222222">Trajectories: Pass (green) / Fail (red) / Unknown (grey)</text>`);
  lines.push(`<text x="${bx0 + bw / 2}" y="${by0 + bh + 46}" text-anchor="middle" font-size="9.5" fill="#222222">More passes is better; grey is unknown</text>`);
  lines.push(`<text x="${bx0 + bw / 2}" y="${by0 + bh + 61}" text-anchor="middle" font-size="9" fill="#444444">Read alongside P10 feature completeness</text>`);

  data.cells.forEach((cell, idx) => {
    const ry = by0 + 13 + idx * 19.6;
    if (idx === 5 || idx === 10) {
      lines.push(`<line x1="${bx0 - 65}" y1="${(ry - 9.5).toFixed(1)}" x2="${bx0 + bw}" y2="${(ry - 9.5).toFixed(1)}" stroke="#c8d1d9" stroke-width="0.9"/>`);
    }
    const shortMod = cell.model.startsWith("claude") ? "Sonnet" : cell.model.startsWith("gemini") ? "Gemini" : "GPT 6.1";
    lines.push(`<text x="${bx0 - 5}" y="${(ry + 3.5).toFixed(1)}" text-anchor="end" font-size="9.2" fill="#222222">${shortMod} ${cell.arm}</text>`);

    const wPass = (cell.cr1_pass / 21) * bw;
    const wFail = (cell.cr1_fail / 21) * bw;
    const wMiss = (cell.cr1_missing / 21) * bw;
    const barH = 11.5;
    lines.push(`<rect x="${bx0.toFixed(1)}" y="${(ry - barH / 2).toFixed(1)}" width="${wPass.toFixed(1)}" height="${barH}" fill="#2e7d32"/>`);
    if (cell.cr1_fail > 0) {
      lines.push(`<rect x="${(bx0 + wPass).toFixed(1)}" y="${(ry - barH / 2).toFixed(1)}" width="${wFail.toFixed(1)}" height="${barH}" fill="#d9534f" opacity="0.82"/>`);
    }
    if (cell.cr1_missing > 0) {
      lines.push(`<rect x="${(bx0 + wPass + wFail).toFixed(1)}" y="${(ry - barH / 2).toFixed(1)}" width="${wMiss.toFixed(1)}" height="${barH}" fill="#7f8c8d"/>`);
    }
    lines.push(`<text x="${(bx0 + wPass / 2).toFixed(1)}" y="${(ry + 3.2).toFixed(1)}" text-anchor="middle" font-size="8.5" fill="#ffffff" font-weight="bold">${cell.cr1_pass}</text>`);
  });

  // Panel (c): Scatter of P10 Mean Pass Rate (%) vs Mean Settled Delivery Credits
  const cx0 = 760;
  const cy0 = 64;
  const cw = 330;
  const ch = 305;
  const xMinCost = 35;
  const xMaxCost = 325;
  const yMinPass = 90.5;
  const yMaxPass = 100.4;
  const xOfCost = (c) => cx0 + ((c - xMinCost) / (xMaxCost - xMinCost)) * cw;
  const yOfP10 = (p) => cy0 + ch - ((p - yMinPass) / (yMaxPass - yMinPass)) * ch;

  lines.push(`<text x="${cx0 + cw / 2}" y="${cy0 - 12}" text-anchor="middle" font-size="12" font-weight="bold" fill="#1f4e79">(c) P10 Coverage vs Settled Delivery Credits</text>`);
  lines.push(`<rect x="${cx0}" y="${cy0}" width="${cw}" height="${ch}" fill="#fafafa" stroke="#d0d7de" stroke-width="1"/>`);

  for (const tick of [50, 100, 150, 200, 250, 300]) {
    const tx = xOfCost(tick);
    lines.push(`<line x1="${tx.toFixed(1)}" y1="${cy0}" x2="${tx.toFixed(1)}" y2="${cy0 + ch}" stroke="#e6ebf1" stroke-width="0.8"/>`);
    lines.push(`<text x="${tx.toFixed(1)}" y="${cy0 + ch + 14}" text-anchor="middle" font-size="9.5" fill="#444444">${tick}</text>`);
  }
  for (const tick of [91, 93, 95, 97, 99, 100]) {
    const ty = yOfP10(tick);
    lines.push(`<line x1="${cx0}" y1="${ty.toFixed(1)}" x2="${cx0 + cw}" y2="${ty.toFixed(1)}" stroke="#e6ebf1" stroke-width="0.8"/>`);
    lines.push(`<text x="${cx0 - 6}" y="${(ty + 3.5).toFixed(1)}" text-anchor="end" font-size="9.5" fill="#444444">${tick}%</text>`);
  }
  lines.push(`<text x="${cx0 + cw / 2}" y="${cy0 + ch + 30}" text-anchor="middle" font-size="10.5" fill="#222222">Mean settled delivery AI credits (completely billed n in brackets)</text>`);
  lines.push(`<text x="${cx0 + cw / 2}" y="${cy0 + ch + 46}" text-anchor="middle" font-size="9.5" fill="#222222">Up = more coverage; left = fewer credits</text>`);
  lines.push(`<text x="${cx0 + cw / 2}" y="${cy0 + ch + 61}" text-anchor="middle" font-size="9" fill="#444444">Prefer upper-left at comparable outcomes</text>`);

  const labelOffsets = {
    "claude-sonnet-5.5:A": [10, 22],
    "claude-sonnet-5.5:D": [10, 36],
    "claude-sonnet-5.5:E": [-14, -7],
    "claude-sonnet-5.5:C": [28, 15],
    "claude-sonnet-5.5:B": [12, -8],
    "gemini-4-argon:A": [16, 44],
    "gemini-4-argon:D": [22, 28],
    "gemini-4-argon:E": [-14, 24],
    "gemini-4-argon:C": [-14, -7],
    "gemini-4-argon:B": [14, 10],
    "gpt-6.1-sol:A": [-12, 14],
    "gpt-6.1-sol:D": [12, -6],
    "gpt-6.1-sol:C": [-12, 14],
    "gpt-6.1-sol:B": [-14, -10],
    "gpt-6.1-sol:E": [6, -10],
  };

  for (const cell of data.cells) {
    const px = xOfCost(cell.delivery_credits_mean);
    const py = yOfP10(cell.p10_mean);
    const col = ARM_COLOURS[cell.arm];
    const shortMod = cell.model.startsWith("claude") ? "S" : cell.model.startsWith("gemini") ? "G" : "GPT";
    const [dx, dy] = labelOffsets[`${cell.model}:${cell.arm}`] || [6, -4];
    const anchor = dx < 0 ? "end" : "start";
    const lx = px + dx;
    const ly = py + dy;
    lines.push(`<line x1="${px.toFixed(1)}" y1="${py.toFixed(1)}" x2="${(lx + (dx < 0 ? 2 : -2)).toFixed(1)}" y2="${(ly - 3).toFixed(1)}" stroke="${col}" stroke-width="0.75" opacity="0.65"/>`);
    lines.push(`<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="4.0" fill="${col}" stroke="#ffffff" stroke-width="1"/>`);
    lines.push(`<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="${anchor}" font-size="8.4" fill="${col}" font-weight="bold">${shortMod}-${cell.arm}[${cell.delivery_credits_n}]</text>`);
  }

  lines.push(`<rect x="${cx0 + 8}" y="${cy0 + 118}" width="215" height="46" rx="3" fill="#ffffff" fill-opacity="0.92" stroke="#d0d7de" stroke-width="0.8"/>`);
  lines.push(`<text x="${cx0 + 13}" y="${cy0 + 131}" font-size="8.8" fill="#333333" font-weight="bold">S = Sonnet 5.5 · G = Gemini 4 Argon · GPT = GPT 6.1</text>`);
  lines.push(`<text x="${cx0 + 13}" y="${cy0 + 144}" font-size="8.6" fill="#333333">Similar A/D means do not establish equivalence.</text>`);
  lines.push(`<text x="${cx0 + 13}" y="${cy0 + 157}" font-size="8.6" fill="#333333">Coverage uses all 21; credit n is shown in labels.</text>`);

  lines.push(`<text x="${width / 2}" y="${height - 10}" text-anchor="middle" font-size="10" fill="#444444">All 315/315 trajectories completed and owner-attested unassisted. Settled ledger: 5,317/5,372 attempts (62,299.76 credits); 55 holds retain 19,200 reserved credits (783.16 lower bound).</text>`);
  lines.push(`</svg>`);
  return lines.join("\n");
}

const charts = [
  ["fig-study-trajectories", buildTrajectoriesSvg(), 1080, 560],
  ["fig-study-outcomes-costs", buildOutcomesCostsSvg(), 1120, 470],
];

await mkdir(output, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  channel: process.env.PAPER_BROWSER_CHANNEL || undefined,
});

try {
  const context = await browser.newContext({ deviceScaleFactor: 3 });
  const page = await context.newPage();
  for (const [stem, svg, width, height] of charts) {
    const svgPath = join(output, `${stem}.svg`);
    const pngPath = join(output, `${stem}.png`);
    await writeFile(svgPath, svg + "\n", "utf8");
    await page.setViewportSize({ width, height });
    await page.setContent(`<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:#fff;}</style>${svg}`);
    const png = await page.locator("svg").screenshot({ type: "png" });
    await writeFile(pngPath, png);
    console.log(`Exported ${stem}: ${width}x${height} (3x PNG ${png.length} bytes)`);
  }
} finally {
  await browser.close();
}
