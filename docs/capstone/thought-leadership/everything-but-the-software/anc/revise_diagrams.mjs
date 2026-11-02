import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const paper = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const elements = [];
let serial = 1;

function text(id, value, x, y, width, height, fontSize = 24, containerId = null) {
  const element = {
    id, type: "text", x, y, width, height, text: value, originalText: value,
    fontSize, fontFamily: 2, lineHeight: 1.25, strokeColor: "#000000",
    textAlign: containerId ? "center" : "left", verticalAlign: "middle",
    containerId, seed: serial++, angle: 0, opacity: 100, isDeleted: false,
  };
  elements.push(element);
  return element;
}

function box(id, value, x, y, width, background) {
  const shape = {
    id, type: "rectangle", x, y, width, height: 105, angle: 0,
    strokeColor: "#495057", backgroundColor: background, fillStyle: "solid",
    strokeWidth: 2, strokeStyle: "solid", roughness: 0, opacity: 100,
    seed: serial++, isDeleted: false, boundElements: [],
  };
  elements.push(shape);
  const label = text(`${id}-label`, value, x + 8, y + 7, width - 16, 90, 24, id);
  shape.boundElements.push({ type: "text", id: label.id });
  return shape;
}

function connect(id, source, target) {
  const x = source.x + source.width + 5;
  const y = source.y + source.height / 2;
  const dx = target.x - 5 - x;
  elements.push({
    id, type: "arrow", x, y, width: dx, height: 0, angle: 0,
    points: [[0, 0], [dx, 0]], strokeColor: "#495057",
    backgroundColor: "transparent", fillStyle: "solid", strokeWidth: 2,
    strokeStyle: "solid", roughness: 0, opacity: 100, seed: serial++,
    isDeleted: false, startArrowhead: null, endArrowhead: "arrow",
    startBinding: { elementId: source.id, focus: 0, gap: 5 },
    endBinding: { elementId: target.id, focus: 0, gap: 5 },
  });
  source.boundElements.push({ type: "arrow", id });
  target.boundElements.push({ type: "arrow", id });
}

text("title", "PROSPECTIVE STUDY DESIGN\n495 trajectories across five arms",
  0, 0, 1120, 95, 36);
text("scope", "Each model runs every arm: GPT 6.1 Sol, Sonnet 5.5, Gemini 4 Argon.\n"
  + "33 trajectories per arm/model; seed 2027; fresh sessions inherit repository state.",
  0, 110, 1120, 70);

const arms = [
  ["A", "Feature 30 min\n300 nominal credits", "No post session\nP_t = F_t", "#CFE4FA"],
  ["B", "Feature 30 min\n300 nominal credits", "Consolidate 15 min\n300 credits\nDESIGN.md", "#DFF6DD"],
  ["C", "Feature 30 min\n300 nominal credits", "Review-only 15 min\n300 credits\nREVIEW.md", "#E8DEFA"],
  ["D (A+)", "Feature 45 min\n600 nominal credits", "No post session\nP_t = F_t", "#CFE4FA"],
  ["E", "Feature 30 min\n300 nominal credits", "Visible repair 15 min\n300 credits\nNo hidden feedback", "#FFF4CE"],
];
for (const [index, [arm, feature, post, colour]] of arms.entries()) {
  const y = 200 + index * 125;
  const first = box(`arm-${index}-feature`, `${arm}\n${feature}`, 0, y, 230, colour);
  const f = box(`arm-${index}-f`, "External F_t\nHidden tests\nwithheld", 275, y, 190, "#F3F2F1");
  const middle = box(`arm-${index}-post`, post, 510, y, 260, colour);
  const p = box(`arm-${index}-p`, "External P_t\nNext feature;\nCR1 after P_10", 815, y, 240, "#F3F2F1");
  connect(`arm-${index}-to-f`, first, f);
  connect(`arm-${index}-to-post`, f, middle);
  connect(`arm-${index}-to-p`, middle, p);
}
text("footer", "CR1: withheld change request, 45 min / 300 nominal credits.\n"
  + "Primary B-D: matched time/credit ceilings; session structure, tests and handovers differ.\n"
  + "15 excluded calibration trajectories. New freeze, OSF amendment and launch approval pending.",
  0, 850, 1120, 105);
await writeFile(resolve(paper, "fig-pilot-design.excalidraw"), JSON.stringify({
  type: "excalidraw", version: 2, source: "https://excalidraw.com", elements,
  appState: { viewBackgroundColor: "#ffffff", exportBackground: true },
  files: {},
}, null, 2) + "\n");

async function replaceLabels(stem, replacements) {
  const path = resolve(paper, `${stem}.excalidraw`);
  const scene = JSON.parse(await readFile(path, "utf8"));
  const used = new Set();
  for (const element of scene.elements) {
    if (element.type === "text") {
      const match = Object.entries(replacements).find(
        ([original, value]) => element.text === original || element.text === value,
      );
      if (match) {
        used.add(match[0]);
        element.text = match[1];
        element.originalText = match[1];
      }
    }
  }
  const missing = Object.keys(replacements).filter(key => !used.has(key));
  if (missing.length) throw new Error(`${stem}: expected labels absent: ${missing.join(", ")}`);
  await writeFile(path, JSON.stringify(scene, null, 2) + "\n");
}

await replaceLabels("fig-experiment-measures", {
  "Combines acquisition,\nretention and repair\nNot a pure decay rate":
    "Combines acquisition,\nretention and repair\nFinal behavioural coverage",
  "Zero risk set = undefined\nUnknown evaluation != failure\nNever-passed != loss":
    "Empty observed risk: undefined\nMissing stays unobserved\nPrior pass required for loss",
  "Tokens & seconds distinct\nMissing billing = unknown (!= 0)\nCheap failure != efficiency":
    "Separate tokens, time, credits\nMissing billing stays unknown\nReport cost alongside success",
  "MEASUREMENT | Pilot endpoints, cost counterbalance & interpretation":
    "MEASUREMENT | Coverage, retention, adaptation and cost",
  "Primary B-A and B-C contrasts reported separately per model (2 runs/arm/model)\nExploratory uncertainty only; no pass/fail hypothesis verdicts":
    "Primary: equal-model-weight B-D coverage; 33 trajectories per arm/model\n"
    + "Other outcomes and per-model contrasts are secondary; no family-wide coverage claim",
  "H1: Final coverage\nCheckpoint P_10\nAll 127 feature tests":
    "Final coverage\nCheckpoint P_10\n127 feature contracts",
  "H2: Contract retention\nEvery F_t and P_t\nPrior-P passing risk set":
    "Contract retention\nEvery F_t and P_t\nPrior-P passing risk set",
  "Open losses & density\non unchanged prior-P passes\nRecovery keeps episode":
    "Losses / observed risk\nFull risk + missing counts\nRecovery keeps episode",
  "H6: Changeability\nWithheld CR1 after P_10\n2 runs/arm/model denom.":
    "CR1 adaptation\nWithheld after P_10\n33 runs/arm/model",
  "All 15 CR1 tests pass\nAND all P_10 passing\nfeature contracts retained":
    "Strict: CR1 + retention\nGraded: passes / 15; losses\nF9/F10 acquisition strata",
  "Single regional scope probe\nUnobserved stays missing\nwith explicit bounds":
    "One withheld change probe\nUnobserved stays missing\nwith explicit bounds",
  "Structural proxies\nSecondary checkpoints\nFrozen tool settings":
    "Treatment fidelity\nExternal measurements\nFixed tool settings",
  "Targets of B's budget\nNot independent efficacy\nor comprehension":
    "Structural budget targets\nTreatment fidelity\nComprehension unmeasured",
});

await replaceLabels("fig-contract-states", {
  "CONCEPTUAL | Acquisition is not retention":
    "CONCEPTUAL | Contract acquisition, loss and recovery",
  "Unobserved results stay missing. No frequencies or effects are implied.":
    "Unobserved results stay missing. Retain the onset, recovery and recurrence of losses.",
});

await replaceLabels("fig-refactoring-economics", {
  "ASSUMED SCENARIOS / NOT RESULTS | Payback depends on k / delta":
    "ASSUMED COST SCENARIOS | Payback depends on k / delta",
  "Consolidated B investment\nAverage k credits / cycle\nTotal outlay (AI credits):\nk * N  (assumed k = 5)":
    "Consolidation investment\nAverage k credits / cycle\nTotal outlay: k * N\nk awaits calibration",
  "Null slope: delta = 0\nNo break-even (k > 0)\nPure overhead every cycle\nN = 10: -50 credits\nN = 20: -100 | N = 40: -200":
    "No premium: delta = 0\nNo break-even for k > 0\nPure overhead\nCaps do not reveal delta\nComparable quality needed",
  "Ratio k / delta = 5\nBreak-even at 11 cycles\nN >= 1 + 2k / delta\nExample: k = 5, delta = 1\nNot a measured estimate":
    "Ratio k / delta = 5\nBreak-even at 11 cycles\nN >= 1 + 2k / delta\nExample: k = 5, delta = 1\nIllustrative parameters",
  "Ratio k / delta = 100\nBreak-even at 201 cycles\nN >= 1 + 2k / delta\nExample: k = 100, delta = 1\nNot a measured estimate":
    "Ratio k / delta = 100\nBreak-even at 201 cycles\nN >= 1 + 2k / delta\nExample: k = 100, delta = 1\nIllustrative parameters",
  "All values are algebraic AI credit differences (A minus B) for assumed k = 5 credits/cycle.\nAt pilot horizon N = 10, all three assumed slopes remain negative (-50, -27.5, -5 credits): no payback.":
    "Break-even depends on the ratio k / delta, not the units or a preferred k.\n"
    + "k awaits measured consolidation spend; delta is an uncapped, quality-matched counterfactual.",
});

const economicsPath = resolve(paper, "fig-refactoring-economics.excalidraw");
const economics = JSON.parse(await readFile(economicsPath, "utf8"));
economics.elements = economics.elements.filter(element => !element.id.startsWith("ratio-plot-"));
const line = (id, x, y, points, colour = "#495057") => ({
  id, type: "line", x, y, width: Math.max(...points.map(point => point[0])),
  height: Math.max(...points.map(point => Math.abs(point[1]))), points,
  strokeColor: colour, backgroundColor: "transparent", strokeWidth: 2,
  strokeStyle: "solid", roughness: 0, opacity: 100, angle: 0, seed: 2027,
  isDeleted: false, startArrowhead: null, endArrowhead: null,
});
const label = (id, value, x, y, width = 500) => ({
  id, type: "text", x, y, width, height: 60, text: value, originalText: value,
  fontSize: 24, fontFamily: 2, lineHeight: 1.25, strokeColor: "#000000",
  textAlign: "left", verticalAlign: "middle", angle: 0, opacity: 100,
  seed: 2027, isDeleted: false, containerId: null,
});
economics.elements.push(
  label("ratio-plot-title", "Break-even sensitivity: N >= 1 + 2 * (k / delta)\nIllustrative boundary; integer cycles round up", 90, 660, 1050),
  line("ratio-plot-x", 110, 990, [[0, 0], [900, 0]]),
  line("ratio-plot-y", 110, 990, [[0, 0], [0, -220]]),
  line("ratio-plot-function", 110, 990, [[0, 0], [900, -220]], "#0078D4"),
  label("ratio-plot-x-label", "k / delta (0 to 100; delta > 0)", 380, 1010, 730),
  label("ratio-plot-low", "5: 11 cycles\n10: 21 cycles", 155, 880, 400),
  label("ratio-plot-high", "100: 201 cycles", 775, 730, 400),
  label("ratio-plot-y-label", "Cycles\n1 to 201", 0, 800, 150),
);
await writeFile(economicsPath, JSON.stringify(economics, null, 2) + "\n");
