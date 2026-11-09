import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const directory = dirname(fileURLToPath(import.meta.url));
const previews = resolve(process.argv[2] ?? directory);
const escape = (value) => value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
for (const name of ["executive", "technical"]) {
  const filename = `zava-forward-${name}-architecture`;
  const native = readFileSync(resolve(directory, `${filename}.excalidraw`));
  const hash = createHash("sha256").update(native).digest("hex");
  const path = resolve(previews, `${filename}.svg`);
  const original = readFileSync(path, "utf8");
  const title = `Zava Forward ${name} architecture: 8 November source continuation`;
  const description = "Retained core layout and icons; home sensors feed Basic B1 IoT Hub, Event Hubs and shared-API validated SQL telemetry/history. Read-only averages are computed on read; persisted per-home averages and quality-helper linkage are gated targets. A separate resident website has independently supplied SQL and optional public Sweden Central AI outside the core boundary. No new infrastructure adoption, live acceptance, diagnosis, consent or safety release is implied.";
  const header = `<title id="zava-title">${escape(title)}</title><desc id="zava-description">${escape(description)}</desc><metadata id="zava-native-source">${escape(JSON.stringify({ path: `docs/architecture/${filename}.excalidraw`, sha256: hash }))}</metadata>`;
  const svg = original.replace(/\srole="img"|\saria-labelledby="zava-title zava-description"|\sdata-native-sha256="[a-f0-9]+"/g, "")
    .replace(/<(title|desc|metadata) id="zava-(?:title|description|native-source)">[\s\S]*?<\/\1>/g, "")
    .replace(/<svg\b[^>]*>/, (root) => `${root.slice(0, -1)} role="img" aria-labelledby="zava-title zava-description" data-native-sha256="${hash}">${header}`);
  assert(svg.includes(header), `Missing SVG root: ${path}`);
  writeFileSync(path, svg);
  console.log(`${filename}: accessible text and exact native-source hash attached; rendering geometry unchanged.`);
}
