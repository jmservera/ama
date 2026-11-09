import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const directory = dirname(fileURLToPath(import.meta.url));
const repository = resolve(directory, "../../../../..");
const manifest = JSON.parse(readFileSync(resolve(directory, "../../slides.json"), "utf8"));
const load = (name) => JSON.parse(readFileSync(resolve(directory, `${name}.excalidraw`), "utf8"));
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const slide = (code) => {
  const selected = manifest.slides.find((entry) => entry.code === code);
  assert(selected, `Missing slide code: ${code}`);
  return selected;
};
const drawings = () => [
  ...["cxo-architecture", "azure-architecture"].map((name) => ({ name, drawing: load(name) })),
  ...["executive", "technical"].map((name) => ({ name, drawing: JSON.parse(readFileSync(
    resolve(repository, `docs/architecture/zava-forward-${name}-architecture.excalidraw`), "utf8")) })),
];

test("the current source adds one deployment page without repinning original cost layouts", () => {
  assert.equal(manifest.slide_count, 55);
  assert.deepEqual(manifest.slides.map((slide) => slide.number), Array.from({ length: 55 }, (_, i) => i + 1));
  assert.equal(slide("S11A").number, slide("S11").number + 1);
  assert.equal(slide("S11A").part_number, 55);
  for (const number of [6, 11, 21, 32, 36, 52]) {
    const original = manifest.slides.find((entry) => entry.part_number === number);
    assert.equal(original.layout, "baseline");
    assert.equal(original.images, undefined);
  }
});

test("reconciled appendix questions and index labels stay coupled", () => {
  const pairs = [
    ["B04", "Where do rules, decision models and generation fit?", "Where do rules, models and generation fit?"],
    ["B10", "How is the full application architecture organised?", "How is the application architecture organised?"],
    ["B19", "How do device readings support decisions safely?", "How do device readings support safe decisions?"],
    ["B20", "When would Fabric add value beyond SQL?", "When would Fabric add value beyond SQL?"],
  ];
  const index = slide("QX").replacements.map((replacement) => replacement.to);
  for (const [code, question, label] of pairs) {
    const selected = slide(code);
    assert.equal(selected.title, question);
    assert(selected.headers.some((header) => header.text === question));
    assert(index.includes(label));
    assert(selected.revised_notes[0].endsWith(question));
  }
});

test("main-route architecture and state-flow precede appendix depth", () => {
  assert.equal(slide("S11").images[0].asset, "cxo-architecture");
  assert.equal(slide("S11A").images[0].asset, "architecture-azure-deployment");
  assert.equal(slide("B10").images[0].asset, "azure-architecture");
  const help = slide("S13");
  assert(help.elements.some((element) => element.text?.includes("Case facts -> coded gates -> next owner")));
  assert(help.revised_notes.some((note) => note.includes("not a claim that a deployed LangGraph")));
  assert(slide("S15").elements.some((element) => element.text?.includes("L4 flags -> L2 concerns")));
});

test("native sources have unique editable elements and source-backed evidence", () => {
  for (const { name, drawing } of drawings()) {
    assert.equal(drawing.type, "excalidraw");
    assert.equal(new Set(drawing.elements.map((element) => element.id)).size, drawing.elements.length);
    for (const element of drawing.elements) {
      assert(["rectangle", "ellipse", "text", "arrow", "image", "frame", "line"].includes(element.type));
      if (element.type === "line") {
        assert.equal(element.id, "application-boundary");
        assert.deepEqual(element.points[0], element.points.at(-1));
        assert.equal(element.polygon, true);
      }
      for (const reference of element.customData?.evidence ?? []) {
        const bytes = readFileSync(resolve(repository, reference.path));
        assert.equal(sha(bytes), reference.sha256);
        assert(reference.line > 0 && reference.line <= bytes.toString("utf8").split(/\r?\n/).length);
      }
    }
  }
});

test("embedded icons preserve their source bytes and aspect ratios", () => {
  const drawing = load("azure-architecture");
  for (const image of drawing.elements.filter((element) => element.type === "image")) {
    const metadata = image.customData.icon_source;
    const original = readFileSync(resolve(repository, metadata.path));
    assert.equal(sha(original), metadata.sha256);
    assert.deepEqual(Buffer.from(drawing.files[image.fileId].dataURL.split(",")[1], "base64"), original);
    assert(Math.abs(image.width / image.height - metadata.aspect_ratio) < 1e-9);
    assert.deepEqual(image.scale, [1, 1]);
    assert.equal(image.crop, null);
  }
});

test("conditional device arrows cannot appear as half-paths in the core projection", () => {
  const drawing = load("azure-architecture");
  const frame = drawing.elements.find((element) => element.id === "core");
  for (const arrow of drawing.elements.filter((element) => element.type === "arrow" && element.frameId !== "core")) {
    assert(arrow.y >= frame.y + frame.height, `Unexpected cropped conditional arrow: ${arrow.id}`);
  }
});

test("all four editable views include the complete sensor chain and honest resident/averages targets", () => {
  for (const { name, drawing } of drawings()) {
    const text = drawing.elements.filter((element) => element.type === "text").map((element) => element.text).join("\n");
    for (const required of [/Home sensors/i, /IoT Hub/i, /Event Hubs/i, /telemetry/i, /history/i,
      /averages/i, /resident website/i, /TARGET/i, /gated/i, /on read/i]) assert.match(text, required, name);
    for (const key of ["deviceTransport", "intake", "consumer", "analysis", "averages", "residentDeployment", "qualityHelper"]) {
      const reference = drawing.customData.sources[key];
      assert.equal(sha(readFileSync(resolve(repository, reference.path))), reference.sha256);
    }
    for (const arrow of drawing.elements.filter((element) => element.type === "arrow")) {
      for (const end of ["start", "end"]) {
        const node = drawing.elements.find((element) => element.id === arrow[`${end}Binding`]?.elementId);
        assert(node, `Missing ${end} binding: ${name}/${arrow.id}`);
        assert(node.boundElements.some((bound) => bound.id === arrow.id && bound.type === "arrow"));
      }
    }
  }
});

test("the wide deployment frame is a complete same-model projection, not a reduced tall map", () => {
  const drawing = load("azure-architecture");
  const frame = drawing.elements.find((element) => element.id === "deployment");
  assert.deepEqual([frame.width, frame.height], [2400, 1170]);
  const elements = drawing.elements.filter((element) => element.frameId === "deployment");
  const text = elements.filter((element) => element.type === "text").map((element) => element.text).join("\n");
  for (const service of ["Entra", "ACA", "Azure SQL", "Blob", "Foundry", "IoT Hub", "Event Hubs",
    "telemetry", "averages", "Managed identities", "Vault", "ACR", "Private DNS", "NSGs", "PEs",
    "Log Analytics", "App Insights", "AMPLS", "Alerts", "budgets", "Resident website", "Sweden Central",
    "Front Door", "WAF", "internal ACA", "poison queues", "Worker", "importer", "orchestrator",
    "Digest", "token", "renewal", "simulator"]) assert(text.includes(service), `Missing deployment service: ${service}`);
  const linked = new Set(elements.filter((element) => element.type === "arrow")
    .flatMap((element) => [element.startBinding.elementId, element.endBinding.elementId]));
  for (const node of elements.filter((element) => element.type === "rectangle" && element.id !== "deployment-vnet"))
    assert(linked.has(node.id), `Orphan deployment node: ${node.id}`);
});

test("the continuing tagged views preserve every original icon and existing arrow binding", () => {
  for (const name of ["executive", "technical"]) {
    const path = `docs/architecture/zava-forward-${name}-architecture.excalidraw`;
    const drawing = JSON.parse(readFileSync(resolve(repository, path)));
    const original = JSON.parse(execFileSync("git", ["show", `${drawing.customData.originalArtifactHead}:${path}`],
      { cwd: repository, maxBuffer: 4 * 1024 * 1024 }));
    assert.deepEqual(drawing.customData.originalElementIds, original.elements.map((element) => element.id));
    for (const old of original.elements) {
      const current = drawing.elements.find((element) => element.id === old.id);
      assert(current, old.id);
      if (old.type === "image") assert.deepEqual(current, {
        ...old, customData: { ...old.customData, sources: [], evidence: [] },
      });
      if (old.type === "arrow") for (const end of ["start", "end"])
        assert.deepEqual(current[`${end}Binding`], old[`${end}Binding`]);
    }
    for (const [id, bytes] of Object.entries(original.files)) assert.deepEqual(drawing.files[id], bytes);
  }
});

test("vector previews retain accessible text and tagged native-source provenance", () => {
  for (const { name } of drawings()) {
    const path = ["executive", "technical"].includes(name) ?
      resolve(repository, `docs/architecture/zava-forward-${name}-architecture.svg`) : resolve(directory, `${name}.svg`);
    const svg = readFileSync(path, "utf8");
    assert.match(svg, /<svg\b[^>]*\brole="img"/);
    assert.match(svg, /aria-labelledby=/);
    assert.match(svg, /<title[ >]/);
    assert.match(svg, /<desc[ >]/);
    if (["executive", "technical"].includes(name)) {
      const native = readFileSync(resolve(repository, `docs/architecture/zava-forward-${name}-architecture.excalidraw`));
      assert(svg.includes(`data-native-sha256="${sha(native)}"`));
    }
  }
});

test("the SVG and native derivatives match the explicit generator", () => {
  execFileSync(process.execPath, [resolve(directory, "build-architecture.mjs"), "--check"], { stdio: "pipe" });
  execFileSync(process.execPath, [resolve(repository, "docs/architecture/update-architecture.mjs"), "--check"], { stdio: "pipe" });
});
