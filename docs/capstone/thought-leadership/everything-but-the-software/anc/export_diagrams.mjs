import { createHash } from "node:crypto";
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { build } from "esbuild";
import { chromium } from "playwright";

const here = dirname(fileURLToPath(import.meta.url));
const paper = resolve(here, "..");
const output = process.argv[2] ? resolve(process.argv[2]) : paper;
const stems = ["fig-state-inheritance", "fig-pilot-design", "fig-contract-states"];
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const temporary = await mkdtemp(join(tmpdir(), "paper-excalidraw-"));
let browser;

try {
  await build({
    stdin: {
      resolveDir: here,
      loader: "js",
      contents: `
        import { restore, exportToSvg, exportToBlob } from "@excalidraw/excalidraw";
        window.exportScene = async (input, sourceHash) => {
          const scene = restore(input, null, null, { refreshDimensions: true, repairBindings: true });
          const options = {
            ...scene,
            appState: { ...scene.appState, exportBackground: true, exportWithDarkMode: false, exportEmbedScene: false },
            exportPadding: 20,
          };
          const canvas = document.createElement("canvas");
          const context = canvas.getContext("2d");
          const overflow = [];
          for (const element of scene.elements.filter(e => e.type === "text")) {
            context.font = element.fontSize + "px Arial";
            const lines = element.text.split("\\n");
            const container = scene.elements.find(e => e.id === element.containerId);
            const width = container ? container.width - 10 : element.width;
            if (lines.some(line => context.measureText(line).width > width + 1)) {
              overflow.push(element.id + ": line width");
            }
            if (container && lines.length * element.fontSize * element.lineHeight > container.height - 10) {
              overflow.push(element.id + ": container height");
            }
            if (container && (element.x < container.x || element.y < container.y
                || element.x + element.width > container.x + container.width
                || element.y + element.height > container.y + container.height)) {
              overflow.push(element.id + ": label outside container");
            }
          }
          if (overflow.length) throw new Error("Text overflow: " + overflow.join(", "));
          const svg = await exportToSvg({ ...options, skipInliningFonts: true });
          svg.setAttribute("data-source-sha256", sourceHash);
          const blob = await exportToBlob({
            ...options, mimeType: "image/png",
            getDimensions: (width, height) => ({ width: width * 3, height: height * 3, scale: 3 }),
          });
          const bytes = new Uint8Array(await blob.arrayBuffer());
          let binary = "";
          for (let start = 0; start < bytes.length; start += 32768) {
            binary += String.fromCharCode(...bytes.subarray(start, start + 32768));
          }
          return {
            svg: svg.outerHTML, png: btoa(binary),
            width: Number(svg.getAttribute("width")),
            height: Number(svg.getAttribute("height")),
            elements: scene.elements.length,
          };
        };
      `,
    },
    bundle: true,
    format: "iife",
    outfile: join(temporary, "render.js"),
    define: { "process.env.NODE_ENV": '"production"' },
    loader: { ".woff2": "file", ".woff": "file", ".ttf": "file" },
    logLevel: "warning",
  });
  await writeFile(join(temporary, "index.html"),
    '<!doctype html><meta charset="utf-8"><script src="render.js"></script>');
  browser = await chromium.launch({
    headless: true,
    channel: process.env.PAPER_BROWSER_CHANNEL || undefined,
  });
  const context = await browser.newContext();
  await context.route(/^https?:/, route => route.abort());
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", error => errors.push(error.message));
  await page.goto(pathToFileURL(join(temporary, "index.html")).href);
  await page.waitForFunction(() => typeof window.exportScene === "function");
  await mkdir(output, { recursive: true });
  const receipt = {
    renderer: "@excalidraw/excalidraw 0.18.1",
    browser: browser.version(),
    export: "Native offline SVG and 3x PNG; source files are never overwritten.",
    png_scale: 3,
    diagrams: [],
  };
  for (const stem of stems) {
    const source = await readFile(join(paper, `${stem}.excalidraw`));
    const sourceHash = sha256(source);
    const rendered = await page.evaluate(
      async ({ scene, hash }) => window.exportScene(scene, hash),
      { scene: JSON.parse(source), hash: sourceHash },
    );
    if (errors.length) throw new Error(errors.join("\n"));
    const png = Buffer.from(rendered.png, "base64");
    if (Math.abs(png.readUInt32BE(16) - rendered.width * 3) > 1
        || Math.abs(png.readUInt32BE(20) - rendered.height * 3) > 1) {
      throw new Error(`Unexpected raster dimensions for ${stem}`);
    }
    await writeFile(join(output, `${stem}.svg`), rendered.svg);
    await writeFile(join(output, `${stem}.png`), png);
    receipt.diagrams.push({
      stem, source_sha256: sourceHash,
      svg_sha256: sha256(rendered.svg), png_sha256: sha256(png),
      width: rendered.width, height: rendered.height, elements: rendered.elements,
    });
    console.log(`Exported ${stem}: ${rendered.width}x${rendered.height}, ${rendered.elements} native elements`);
  }
  await writeFile(join(output, "diagram-exports.json"), JSON.stringify(receipt, null, 2) + "\n");
} finally {
  if (browser) await browser.close();
  await rm(temporary, { recursive: true, force: true });
}
