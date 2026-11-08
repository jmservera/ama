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

test("the current source keeps 54 ordered pages and baseline protected-cost layouts", () => {
  assert.equal(manifest.slide_count, 54);
  assert.deepEqual(manifest.slides.map((slide) => slide.number), Array.from({ length: 54 }, (_, i) => i + 1));
  for (const number of [6, 11, 21, 32, 36, 52]) {
    assert.equal(manifest.slides[number - 1].layout, "baseline");
    assert.equal(manifest.slides[number - 1].images, undefined);
  }
});

test("reconciled appendix questions and index labels stay coupled", () => {
  const pairs = [
    [31, "Where do rules, decision models and generation fit?", "Where do rules, models and generation fit?"],
    [37, "How is the full application architecture organised?", "How is the application architecture organised?"],
    [46, "How do device readings support decisions safely?", "How do device readings support safe decisions?"],
    [47, "When would Fabric add value beyond SQL?", "When would Fabric add value beyond SQL?"],
  ];
  const index = manifest.slides[26].replacements.map((replacement) => replacement.to);
  for (const [number, question, label] of pairs) {
    const slide = manifest.slides[number - 1];
    assert.equal(slide.title, question);
    assert(slide.headers.some((header) => header.text === question));
    assert(index.includes(label));
    assert(slide.revised_notes[0].endsWith(question));
  }
});

test("main-route architecture and state-flow precede appendix depth", () => {
  assert.equal(manifest.slides[11].images[0].asset, "cxo-architecture");
  assert.equal(manifest.slides[36].images[0].asset, "azure-architecture");
  const help = manifest.slides[13];
  assert(help.elements.some((element) => element.text?.includes("Case facts -> coded gates -> next owner")));
  assert(help.revised_notes.some((note) => note.includes("not a claim that a deployed LangGraph")));
  assert(manifest.slides[15].elements.some((element) => element.text?.includes("L4 flags -> L2 concerns")));
});

test("native sources have unique editable elements and source-backed evidence", () => {
  for (const name of ["cxo-architecture", "azure-architecture"]) {
    const drawing = load(name);
    assert.equal(drawing.type, "excalidraw");
    assert.equal(new Set(drawing.elements.map((element) => element.id)).size, drawing.elements.length);
    for (const element of drawing.elements) {
      assert(["rectangle", "ellipse", "text", "arrow", "image", "frame"].includes(element.type));
      for (const reference of element.customData.evidence) {
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

test("the SVG and native derivatives match the explicit generator", () => {
  execFileSync(process.execPath, [resolve(directory, "build-architecture.mjs"), "--check"], { stdio: "pipe" });
});
