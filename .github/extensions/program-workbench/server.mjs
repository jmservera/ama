import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { dirname, extname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { randomBytes } from "node:crypto";
import { buildIndex, readDocument, saveDocument, searchDocuments } from "./document-store.mjs";

const extensionDirectory = dirname(fileURLToPath(import.meta.url));
const defaultRepositoryRoot = join(extensionDirectory, "..", "..", "..");
const assetsDirectory = join(extensionDirectory, "assets");
let cachedIndex = null;
let cachedRoot = null;

function sendJson(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" });
  res.end(JSON.stringify(body));
}

async function readBody(req) {
  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > 2 * 1024 * 1024) throw new Error("Request body exceeds 2 MB.");
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
}

async function getIndex(root, refresh = false) {
  if (!cachedIndex || cachedRoot !== root || refresh) {
    cachedIndex = await buildIndex(root);
    cachedRoot = root;
  }
  return cachedIndex;
}

export async function refreshDocumentIndex(repositoryRoot = defaultRepositoryRoot) {
  return getIndex(repositoryRoot, true);
}

export async function getIndexedDocument(requestedPath, repositoryRoot = defaultRepositoryRoot) {
  return readDocument(repositoryRoot, requestedPath, await getIndex(repositoryRoot));
}

export async function startProgramWorkbenchServer({ initialPath = "", repositoryRoot = defaultRepositoryRoot, port = 0, requestEditor } = {}) {
  const token = randomBytes(24).toString("hex");
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, "http://127.0.0.1");
      if (url.pathname.startsWith("/api/")) {
        if (req.headers["x-canvas-token"] !== token) return sendJson(res, 403, { error: "Canvas token is missing or invalid." });
        if (req.method === "GET" && url.pathname === "/api/index") return sendJson(res, 200, { documents: await getIndex(repositoryRoot) });
        if (req.method === "POST" && url.pathname === "/api/refresh") return sendJson(res, 200, { documents: await getIndex(repositoryRoot, true) });
        if (req.method === "POST" && url.pathname === "/api/open-editor") {
          const body = await readBody(req);
          const documents = await getIndex(repositoryRoot, true);
          const document = documents.find((item) => item.path === body.path && item.kind === "markdown");
          if (!document) return sendJson(res, 400, { error: "Select an indexed Markdown document." });
          if (!document.editable) return sendJson(res, 403, { error: document.readOnlyReason });
          if (!requestEditor) return sendJson(res, 503, { error: "The agent editor handoff is unavailable." });
          return sendJson(res, 202, { path: document.path, ...await requestEditor(document.path) });
        }
        if (req.method === "GET" && url.pathname === "/api/document") {
          return sendJson(res, 200, await getIndexedDocument(url.searchParams.get("path"), repositoryRoot));
        }
        if (req.method === "PUT" && url.pathname === "/api/document") {
          const body = await readBody(req);
          const result = await saveDocument(repositoryRoot, body.path, body.content);
          await getIndex(repositoryRoot, true);
          return sendJson(res, 200, result);
        }
        if (req.method === "GET" && url.pathname === "/api/search") {
          return sendJson(res, 200, { documents: await searchDocuments(repositoryRoot, url.searchParams.get("q"), await getIndex(repositoryRoot)) });
        }
        return sendJson(res, 404, { error: "Canvas endpoint not found." });
      }

      const assetMap = { "/": "index.html", "/app.js": "app.js", "/styles.css": "styles.css" };
      const asset = assetMap[url.pathname];
      if (!asset) { res.writeHead(404); return res.end("Not found"); }
      let content = await readFile(join(assetsDirectory, asset), "utf8");
      if (asset === "index.html") {
        content = content.replace("__CANVAS_TOKEN__", token).replace("__INITIAL_PATH__", encodeURIComponent(initialPath));
        res.setHeader("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'");
      }
      const type = extname(asset) === ".js" ? "text/javascript" : extname(asset) === ".css" ? "text/css" : "text/html";
      res.writeHead(200, { "Content-Type": `${type}; charset=utf-8`, "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" });
      res.end(content);
    } catch (error) {
      sendJson(res, 400, { error: error instanceof Error ? error.message : "Unexpected canvas error." });
    }
  });
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(port, "127.0.0.1", resolve);
  });
  const address = server.address();
  return { server, token, url: `http://127.0.0.1:${address.port}/` };
}
