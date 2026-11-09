import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readFileSync, realpathSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const directory = dirname(fileURLToPath(import.meta.url));
const repository = resolve(directory, "../../../../..");
const paths = [
  "docs/architecture/zava-forward-executive-architecture.excalidraw",
  "docs/architecture/zava-forward-technical-architecture.excalidraw",
  "docs/capstone/source/diagrams/architecture/cxo-architecture.excalidraw",
  "docs/capstone/source/diagrams/architecture/azure-architecture.excalidraw",
];

function intersects(a, b, box) {
  let low = 0, high = 1;
  for (const [value, delta, minimum, maximum] of [
    [a[0], b[0] - a[0], box.x + 1, box.x + box.width - 1],
    [a[1], b[1] - a[1], box.y + 1, box.y + box.height - 1],
  ]) {
    if (delta === 0) { if (value < minimum || value > maximum) return false; }
    else {
      const limits = [(minimum - value) / delta, (maximum - value) / delta].sort((x, y) => x - y);
      low = Math.max(low, limits[0]); high = Math.min(high, limits[1]);
      if (low > high) return false;
    }
  }
  return true;
}

test("native diagram geometry has no clipping or newly introduced label/node crossings", () => {
  for (const path of paths) {
    const drawing = JSON.parse(readFileSync(resolve(repository, path)));
    const canvas = drawing.elements[0];
    const ids = new Map(drawing.elements.map((element) => [element.id, element]));
    const originalIds = new Set(drawing.customData?.originalElementIds ?? []);
    const failures = [];
    for (const element of drawing.elements) {
      const points = element.type === "arrow" ? element.points.map(([x, y]) => [element.x + x, element.y + y]) :
        [[element.x, element.y], [element.x + element.width, element.y + element.height]];
      assert(points.every(([x, y]) => x >= 0 && y >= 0 && x <= canvas.width + .1 && y <= canvas.height + .1),
        `Canvas overflow: ${path}/${element.id}`);
      if (element.type === "text") {
        const container = ids.get(element.customData?.container) ?? drawing.elements.find((node) =>
          node.customData?.role === "service" && node.groupIds.some((group) => element.groupIds.includes(group)));
        if (container) assert(element.x >= container.x && element.y >= container.y &&
          element.x + element.width <= container.x + container.width + .1 &&
          element.y + element.height <= container.y + container.height + .1, `Node overflow: ${path}/${element.id}`);
      }
      if (element.frameId) {
        const frame = ids.get(element.frameId);
        assert(frame && element.x >= frame.x && element.y >= frame.y &&
          element.x + element.width <= frame.x + frame.width + .1 &&
          element.y + element.height <= frame.y + frame.height + .1, `Frame overflow: ${element.id}`);
      }
      if (element.type !== "arrow" || originalIds.has(element.id)) continue;
      const bound = [element.startBinding.elementId, element.endBinding.elementId];
      const groups = bound.flatMap((id) => ids.get(id).groupIds);
      for (const other of drawing.elements) {
        if (other.id === element.id || bound.includes(other.id) || other.frameId !== element.frameId ||
          groups.some((group) => other.groupIds.includes(group)) || bound.includes(other.customData?.container)) continue;
        const protectedBox = other.type === "text" || other.type === "image" ||
          (other.type === "rectangle" && (other.customData?.role === "service" ||
            drawing.elements.some((child) => child.customData?.container === other.id)));
        if (!protectedBox) continue;
        if (points.slice(1).some((point, i) => intersects(points[i], point, other))) failures.push(`${element.id} -> ${other.id}`);
      }
    }
    assert.deepEqual(failures, [], `${path}: new wire crossings`);
  }
});

test("installed browser measures every native label within its authored width", async () => {
  const cli = realpathSync(execFileSync("which", ["excalidraw"], { encoding: "utf8" }).trim());
  const require = createRequire(cli);
  const { chromium } = require("playwright-core");
  assert(process.env.EXCALIDRAW_BROWSER_PATH, "Set EXCALIDRAW_BROWSER_PATH to the existing browser binary");
  const browser = await chromium.launch({ executablePath: process.env.EXCALIDRAW_BROWSER_PATH, headless: true });
  try {
    const page = await browser.newPage();
    const allFailures = [];
    for (const path of paths) {
      const drawing = JSON.parse(readFileSync(resolve(repository, path)));
      const failures = await page.evaluate((elements) => {
        const context = document.createElement("canvas").getContext("2d");
        return elements.filter((element) => element.type === "text").flatMap((element) => {
          context.font = `${element.fontSize}px Arial`;
          const width = Math.max(...element.text.split("\n").map((line) => context.measureText(line).width));
          return width > element.width + 1 ? [{ id: element.id, width, authored: element.width }] : [];
        });
      }, drawing.elements);
      allFailures.push(...failures.map((failure) => ({ path, ...failure })));
    }
    assert.deepEqual(allFailures, [], "Browser font overflow");
  } finally { await browser.close(); }
});

test("main-route diagrams retain a twelve-point service-text floor at approved contain sizes", () => {
  const cxo = JSON.parse(readFileSync(resolve(directory, "cxo-architecture.excalidraw")));
  assert(cxo.elements.filter((element) => element.type === "text").every((element) => element.fontSize >= 26));
  const azure = JSON.parse(readFileSync(resolve(directory, "azure-architecture.excalidraw")));
  assert(azure.elements.filter((element) => element.type === "text" && element.frameId === "deployment")
    .every((element) => element.fontSize >= 34));
  assert(26 * (5.45 * 1600 / 850) * 72 / 1600 >= 12);
  assert(34 * (5.8 * 2400 / 1170) * 72 / 2400 >= 12);
});
