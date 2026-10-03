import { copyFile, mkdir, readdir, readFile, stat, writeFile } from "node:fs/promises";
import { build } from "esbuild-wasm";
import { fileURLToPath } from "node:url";

const directory = new URL("../../.github/extensions/program-workbench/assets/vendor/", import.meta.url);
await mkdir(directory, { recursive: true });
await build({
  stdin: {
    contents: 'import Editor from "@toast-ui/editor"; import DOMPurify from "dompurify"; globalThis.toastui = { Editor }; globalThis.workbenchSanitize = html => DOMPurify.sanitize(html, { FORBID_TAGS: ["style"], FORBID_ATTR: ["style"] });',
    resolveDir: fileURLToPath(new URL(".", import.meta.url)),
    sourcefile: "workbench-editor-entry.js",
  },
  bundle: true,
  minify: true,
  format: "iife",
  outfile: fileURLToPath(new URL("toastui-editor.js", directory)),
  legalComments: "inline",
});
await copyFile(new URL("./node_modules/@toast-ui/editor/dist/toastui-editor.css", import.meta.url), new URL("toastui-editor.css", directory));

const lock = JSON.parse(await readFile(new URL("./package-lock.json", import.meta.url), "utf8"));
const notices = [await readFile(new URL("toastui-editor.LICENSE", directory), "utf8")];
for (const dependency of Object.keys(lock.packages).filter(Boolean)) {
  const folder = new URL(`./${dependency}/`, import.meta.url);
  const files = await readdir(folder);
  for (const name of files.filter((file) => /^(?:license|copying)(?:\..*)?$/i.test(file))) {
    notices.push(`\n${dependency}\n${await readFile(new URL(name, folder), "utf8")}`);
  }
}
await writeFile(new URL("THIRD-PARTY-NOTICES.txt", directory), notices.join("\n"));

async function directorySize(folder) {
  const entries = await readdir(folder, { withFileTypes: true });
  let bytes = 0;
  for (const entry of entries) {
    const file = new URL(entry.name + (entry.isDirectory() ? "/" : ""), folder);
    bytes += entry.isDirectory() ? await directorySize(file) : (await stat(file)).size;
  }
  return bytes;
}

const extension = new URL("../../.github/extensions/program-workbench/", import.meta.url);
const bytes = await directorySize(extension);
if (bytes >= 8388608) throw new Error(`Extension is ${bytes} bytes, exceeding the project trust limit. Keep build dependencies outside the extension.`);
console.error(`Program Workbench extension: ${bytes} bytes (limit: 8388608).`);
