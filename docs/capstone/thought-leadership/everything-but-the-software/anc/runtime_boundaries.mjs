import { createHash } from "node:crypto";
import { readFile, rm, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { build } from "esbuild";
import { chromium } from "playwright";

// --write-source explicitly resets the editable source to this original layout.
// Without it, render the current source and preserve any subsequent edits.
const here = dirname(fileURLToPath(import.meta.url));
const paper = resolve(here, "..");
const stem = "fig-runtime-boundaries";
const sourcePath = join(paper, `${stem}.excalidraw`);
const manifestPath = join(paper, "diagram-exports.json");
const sourceCommit = "b7973e200a6edbb1d19355badae3b7e03a066b09";
const sha256 = bytes => createHash("sha256").update(bytes).digest("hex");
if (process.argv.slice(2).some(argument => argument !== "--write-source")) {
  throw new Error("Usage: node anc/runtime_boundaries.mjs [--write-source]");
}

function originalScene() {
  const elements = [];
  let serial = 1;
  const common = (id, type, x, y, width, height) => ({
    id, type, x, y, width, height, angle: 0,
    strokeColor: "#495057", backgroundColor: "transparent",
    fillStyle: "solid", strokeWidth: 2, strokeStyle: "solid",
    roughness: 0, opacity: 100, seed: serial++, version: 1,
    versionNonce: serial++, isDeleted: false, groupIds: [],
    frameId: null, roundness: null, boundElements: [],
    updated: 1, link: null, locked: false,
  });
  function text(id, value, x, y, width, fontSize = 24, parent = null) {
    const height = value.split("\n").length * fontSize * 1.25;
    const element = {
      ...common(id, "text", x, y, width, height),
      strokeColor: "#000000", text: value, originalText: value,
      fontSize, fontFamily: 2, lineHeight: 1.25,
      textAlign: parent ? "center" : "left", verticalAlign: "middle",
      containerId: parent?.id || null, autoResize: true,
    };
    elements.push(element);
    if (parent) parent.boundElements.push({ type: "text", id });
    return element;
  }
  function rectangle(id, x, y, width, height, background = "transparent", dashed = false) {
    const element = {
      ...common(id, "rectangle", x, y, width, height),
      backgroundColor: background, strokeStyle: dashed ? "dashed" : "solid",
    };
    elements.push(element);
    return element;
  }
  function box(id, value, x, y, width, height, background = "#F3F2F1") {
    const parent = rectangle(id, x, y, width, height, background);
    const textHeight = value.split("\n").length * 30;
    text(`${id}-label`, value, x + 12, y + (height - textHeight) / 2,
      width - 24, 24, parent);
    return parent;
  }
  function arrow(id, source, target, points, bidirectional = false) {
    const x = Math.min(...points.map(point => point[0]));
    const y = Math.min(...points.map(point => point[1]));
    const width = Math.max(...points.map(point => point[0])) - x;
    const height = Math.max(...points.map(point => point[1])) - y;
    elements.push({
      ...common(id, "arrow", x, y, width, height),
      points: points.map(point => [point[0] - x, point[1] - y]),
      startArrowhead: bidirectional ? "arrow" : null, endArrowhead: "arrow",
      startBinding: { elementId: source.id, focus: 0, gap: 7 },
      endBinding: { elementId: target.id, focus: 0, gap: 7 },
      elbowed: false,
    });
    source.boundElements.push({ type: "arrow", id });
    target.boundElements.push({ type: "arrow", id });
  }

  rectangle("development-panel", 0, 0, 1480, 690, "#ffffff");
  rectangle("evaluation-panel", 0, 720, 1480, 790, "#ffffff");
  text("development-title", "A   Development: tools, with host-side AI transport",
    30, 25, 1420, 32);
  text("evaluation-title", "B   Post-run evaluation: replay, then tool-free judging",
    30, 745, 1420, 32);

  rectangle("development-host-boundary", 35, 95, 1020, 480, "transparent", true);
  rectangle("development-provider-boundary", 1080, 95, 370, 480, "transparent", true);
  text("development-host-title", "HOST CONTROL + VALIDATED STATE REPLAY", 55, 112, 960, 22);
  text("development-provider-title", "REMOTE PROVIDER", 1100, 112, 330, 22);

  const controller = box("experiment-controller",
    "Python experiment controller\nSchedule steps; prepare prompt\nand state-replay workspace",
    70, 170, 435, 105);
  const transport = box("copilot-transport",
    "Host JavaScript\nCopilot transport",
    575, 170, 440, 105);
  const model = box("copilot-model",
    "Remote Copilot model\nRequests tools\nOutside candidate sandbox",
    1100, 170, 330, 105, "#E8DEFA");
  const candidate = box("fresh-candidate-container",
    "FRESH candidate container\nWritable state-replay workspace\nEdit, test, commit",
    70, 355, 435, 110, "#CFE4FA");
  const broker = box("execution-broker",
    "Host Python broker\nEnforce isolated_exec\nBound stdout / stderr / exit code",
    575, 355, 440, 110);
  box("hidden-measurement-container",
    "Hidden-measurement container\nSeparate scheduled evaluation",
    70, 490, 435, 75, "#DFF6DD");
  text("workspace-persistence",
    "Validated files/Git: state replay\nProcesses/memory reset per call\nHost/model conversation continues",
    585, 480, 430);
  text("development-ai-location",
    "Model and host transport\nstay outside the candidate\nsandbox.",
    1100, 355, 330);

  arrow("controller-to-transport", controller, transport,
    [[512, 222.5], [568, 222.5]]);
  arrow("transport-model-exchange", transport, model,
    [[1022, 222.5], [1093, 222.5]], true);
  arrow("transport-broker-exchange", transport, broker,
    [[795, 282], [795, 348]], true);
  text("tool-request-result", "isolated_exec\n/ bounded result", 820, 288, 225, 22);
  arrow("broker-candidate-exchange", broker, candidate,
    [[568, 410], [512, 410]], true);
  text("development-result-note",
    "Only validated committed regular contents cross feature/CR checkpoints; host history is canonicalized.",
    35, 590, 1410, 22);
  text("test-execution-note",
    "Tool calls may request tests; scheduled visible validation and hidden measurement remain separate.",
    35, 622, 1410, 22);
  text("failure-semantics",
    "Collection/isolation failure: unavailable. Observed candidate failure: failure evidence.",
    35, 654, 1410, 22);

  rectangle("evaluation-host-boundary", 35, 815, 1020, 595, "transparent", true);
  rectangle("evaluation-provider-boundary", 1080, 815, 370, 595, "transparent", true);
  text("evaluation-host-title", "HOST: ARCHIVED INPUTS, REPLAY AND VALIDATION", 55, 832, 965, 22);
  text("evaluation-provider-title", "REMOTE PROVIDER", 1100, 832, 330, 22);

  const archive = box("stopped-study-archive",
    "Stopped local study\narchive: recorded HEADs\nand step records",
    70, 885, 305, 110);
  const prepare = box("judging-prepare-broker",
    "Host Python judging\nprepare + broker",
    430, 885, 280, 110);
  const evaluator = box("isolated-evaluator-container",
    "Isolated evaluator\nRead-only snapshot\nFixed API workflows",
    765, 885, 260, 110, "#DFF6DD");
  const packet = box("anonymized-evidence-packet",
    "Anonymized evidence packet\nRequirements + evidence + rubric\nHistorical witness/retention context",
    70, 1070, 465, 150, "#FFF4CE");
  const adapter = box("host-judging-adapter",
    "Host Python / JavaScript\nJudging adapter",
    600, 1070, 415, 150);
  const judge = box("no-tool-blind-judge",
    "Remote no-tool blind judge\nNo tools or repo access\nCitations + separate\nordinal scores",
    1100, 1070, 330, 150, "#E8DEFA");
  const report = box("host-validation-report",
    "Host validation / report\nValidate citations and scores",
    600, 1270, 415, 90);

  arrow("archive-to-prepare", archive, prepare, [[382, 940], [423, 940]]);
  arrow("prepare-to-replay", prepare, evaluator, [[717, 940], [758, 940]]);
  arrow("replay-to-evidence", evaluator, packet,
    [[895, 1002], [895, 1040], [302.5, 1040], [302.5, 1063]]);
  text("bounded-replay-results", "Bounded outcomes / failures / errors",
    375, 1005, 475, 22);
  arrow("evidence-to-adapter", packet, adapter, [[542, 1145], [593, 1145]]);
  arrow("adapter-judge-exchange", adapter, judge,
    [[1022, 1145], [1093, 1145]], true);
  arrow("adapter-to-validation", adapter, report,
    [[807.5, 1227], [807.5, 1263]]);
  text("judge-location-note",
    "Judge is not inside\nthe evaluator container.",
    1100, 1270, 330);
  text("container-controls",
    "Both execution containers: no network/credentials; read-only root filesystem; bounded resources.\n"
    + "Candidate child: unprivileged, capability-free, no-new-privileges; supervisor constrained. Replay: conceptual.",
    35, 1430, 1410, 22);

  return {
    type: "excalidraw", version: 2, source: "https://excalidraw.com",
    elements,
    appState: {
      viewBackgroundColor: "#ffffff", exportBackground: true,
      exportWithDarkMode: false, exportEmbedScene: false,
    },
    files: {},
  };
}

function verifyScene(scene) {
  const elements = new Map(scene.elements.map(element => [element.id, element]));
  if (scene.type !== "excalidraw" || elements.size !== scene.elements.length) {
    throw new Error("Invalid scene or duplicate element IDs");
  }
  for (const element of elements.values()) {
    if (!["rectangle", "text", "arrow"].includes(element.type) || element.isDeleted) {
      throw new Error(`Non-editable or deleted element: ${element.id}`);
    }
    if (element.width < 0 || element.height < 0) throw new Error(`Negative size: ${element.id}`);
    if (element.type === "text") {
      if (element.text !== element.originalText || element.fontFamily !== 2 || element.fontSize < 22) {
        throw new Error(`Unexpected text styling: ${element.id}`);
      }
      if (element.containerId && !elements.get(element.containerId)?.boundElements.some(
        binding => binding.type === "text" && binding.id === element.id,
      )) throw new Error(`Unbound label: ${element.id}`);
    }
    if (element.type === "arrow") {
      for (const end of ["startBinding", "endBinding"]) {
        if (!elements.get(element[end]?.elementId)?.boundElements.some(
          binding => binding.type === "arrow" && binding.id === element.id,
        )) throw new Error(`Unbound arrow: ${element.id}`);
      }
    }
  }
}

const resetSource = process.argv.includes("--write-source");
const source = resetSource
  ? Buffer.from(JSON.stringify(originalScene(), null, 2) + "\n")
  : await readFile(sourcePath);
const input = JSON.parse(source);
verifyScene(input);
const sourceHash = sha256(source);
const manifestBytes = await readFile(manifestPath);
const manifest = JSON.parse(manifestBytes);
const legacyBindings = JSON.stringify(manifest.diagrams);
const renderScript = join(here, ".runtime-boundaries-render.js");
const renderPage = join(here, ".runtime-boundaries-render.html");
const created = [];
let browser;

try {
  browser = await chromium.launch({
    headless: true, channel: process.env.PAPER_BROWSER_CHANNEL || undefined,
  });
  const bundle = await build({
    stdin: {
      resolveDir: here, loader: "js",
      contents: `
        import { restore, exportToSvg, exportToBlob } from "@excalidraw/excalidraw";
        window.renderRuntimeBoundaries = async (input, hash) => {
          const scene = restore(input, null, null, { refreshDimensions: true, repairBindings: true });
          const context = document.createElement("canvas").getContext("2d");
          const byId = new Map(scene.elements.map(element => [element.id, element]));
          for (const original of input.elements.filter(element => element.type === "text")) {
            const element = byId.get(original.id);
            if (element.text !== original.text) throw new Error("Unexpected wrapping: " + element.id);
            const parent = byId.get(element.containerId);
            context.font = element.fontSize + "px Arial";
            const lines = element.text.split("\\n");
            const available = parent ? parent.width - 24 : original.width;
            if (lines.some(line => context.measureText(line).width > available + 1)) {
              throw new Error("Text line overflow: " + element.id);
            }
            if (parent && (element.x < parent.x || element.y < parent.y
                || element.x + element.width > parent.x + parent.width
                || element.y + element.height > parent.y + parent.height)) {
              throw new Error("Label outside container: " + element.id);
            }
          }
          const options = {
            ...scene, exportPadding: 10,
            appState: { ...scene.appState, exportBackground: true,
              exportWithDarkMode: false, exportEmbedScene: false },
          };
          const svg = await exportToSvg({ ...options, skipInliningFonts: true });
          svg.setAttribute("data-source-sha256", hash);
          const blob = await exportToBlob({
            ...options, mimeType: "image/png",
            getDimensions: (width, height) => ({ width: width * 3, height: height * 3, scale: 3 }),
          });
          const bytes = new Uint8Array(await blob.arrayBuffer());
          let binary = "";
          for (let start = 0; start < bytes.length; start += 32768) {
            binary += String.fromCharCode(...bytes.subarray(start, start + 32768));
          }
          return { svg: svg.outerHTML, png: btoa(binary),
            width: Number(svg.getAttribute("width")), height: Number(svg.getAttribute("height")),
            elements: scene.elements.length };
        };
      `,
    },
    bundle: true, format: "iife", write: false,
    define: { "process.env.NODE_ENV": '"production"' },
    loader: { ".woff2": "dataurl", ".woff": "dataurl", ".ttf": "dataurl" },
    logLevel: "warning",
  });
  await writeFile(renderScript, bundle.outputFiles[0].contents, { flag: "wx" });
  created.push(renderScript);
  await writeFile(renderPage,
    '<!doctype html><meta charset="utf-8"><script src=".runtime-boundaries-render.js"></script>',
    { flag: "wx" });
  created.push(renderPage);
  const context = await browser.newContext();
  await context.route(/^https?:/, route => route.abort());
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", error => errors.push(error.message));
  await page.goto(pathToFileURL(renderPage).href);
  await page.waitForFunction(() => typeof window.renderRuntimeBoundaries === "function");
  const rendered = await page.evaluate(
    async ({ scene, hash }) => window.renderRuntimeBoundaries(scene, hash),
    { scene: input, hash: sourceHash },
  );
  if (errors.length) throw new Error(errors.join("\n"));
  const png = Buffer.from(rendered.png, "base64");
  if (Math.abs(png.readUInt32BE(16) - rendered.width * 3) > 1
      || Math.abs(png.readUInt32BE(20) - rendered.height * 3) > 1
      || !rendered.svg.includes(`data-source-sha256="${sourceHash}"`)) {
    throw new Error("Source binding or native PNG dimensions mismatch");
  }
  const entry = {
    stem, source_sha256: sourceHash,
    svg_sha256: sha256(rendered.svg), png_sha256: sha256(png),
    width: rendered.width, height: rendered.height, elements: rendered.elements,
    renderer: manifest.renderer, browser: browser.version(), png_scale: 3,
    export: "Native offline SVG and 3x PNG; Arial text and arrows remain editable in the source.",
    generator: "anc/runtime_boundaries.mjs",
    source_qualification: {
      repository: "jmservera/ama-thought-mve", commit: sourceCommit,
      basis: "Owner-provided conceptual flow at this pin; source verification delegated separately.",
      observed_execution: false, private_data_accessed: false,
    },
    caption: "Conceptual, source-described development and post-run evaluation boundaries. "
      + "Host-side AI transport remains outside isolated execution; development uses writable state-replay workspaces, "
      + "while replay uses a read-only snapshot and the remote blind judge has no tools or repository access. "
      + "Replay paths are not observed experiment execution.",
  };
  const index = manifest.diagrams.findIndex(item => item.stem === stem);
  if (index < 0) manifest.diagrams.push(entry);
  else manifest.diagrams[index] = entry;
  if (JSON.stringify(manifest.diagrams.filter(item => item.stem !== stem))
      !== JSON.stringify(JSON.parse(legacyBindings).filter(item => item.stem !== stem))) {
    throw new Error("Historical figure bindings changed");
  }
  if (!(await readFile(manifestPath)).equals(manifestBytes)) {
    throw new Error("Provenance changed concurrently; retry against the updated manifest");
  }
  if (resetSource) await writeFile(sourcePath, source);
  await writeFile(join(paper, `${stem}.svg`), rendered.svg);
  await writeFile(join(paper, `${stem}.png`), png);
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + "\n");
  console.log(`Exported ${stem}: ${rendered.width}x${rendered.height}; `
    + `${png.readUInt32BE(16)}x${png.readUInt32BE(20)} PNG; ${rendered.elements} editable elements`);
  console.log(`SHA-256 source ${sourceHash}\nSVG ${entry.svg_sha256}\nPNG ${entry.png_sha256}`);
} finally {
  if (browser) await browser.close();
  await Promise.all(created.map(path => rm(path)));
}
