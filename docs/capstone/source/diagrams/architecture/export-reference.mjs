import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Export selection only: keep the authoritative scene, hide editor frame chrome.
const directory = dirname(fileURLToPath(import.meta.url));
const drawing = JSON.parse(readFileSync(resolve(directory, "azure-architecture.excalidraw"), "utf8"));
drawing.elements = drawing.elements.filter((element) =>
  element.frameId !== "deployment" && element.id !== "deployment" && element.type !== "frame");
for (const element of drawing.elements) element.frameId = null;
drawing.elements[0].height = 2060;
process.stdout.write(JSON.stringify(drawing));
