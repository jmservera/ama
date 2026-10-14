import { createServer } from "node:http";
import { readFile, realpath, stat } from "node:fs/promises";
import { dirname, extname, join, resolve, relative, isAbsolute } from "node:path";
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

export async function startProgramWorkbenchServer({ initialPath = "", repositoryRoot = defaultRepositoryRoot, port = 0, requestConversation } = {}) {
  const token = randomBytes(24).toString("hex");
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, "http://127.0.0.1");
      if (url.pathname === "/media") {
        if (url.searchParams.get("token") !== token) return sendJson(res, 403, { error: "Canvas token is missing or invalid." });
        if (req.method !== "GET") return sendJson(res, 405, { error: "Images are read-only." });
        const types = { ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp" };
        const requested = url.searchParams.get("path") || "";
        const docs = await realpath(join(repositoryRoot, "docs"));
        const candidate = resolve(repositoryRoot, requested);
        const insideDocs = (file) => {
          const location = relative(docs, file);
          return location && location !== ".." && !location.startsWith(`..${process.platform === "win32" ? "\\" : "/"}`) && !isAbsolute(location);
        };
        if (!insideDocs(candidate) || !types[extname(candidate).toLowerCase()]) return sendJson(res, 400, { error: "Only repository documentation images can be displayed." });
        const absolute = await realpath(candidate);
        if (!insideDocs(absolute)) return sendJson(res, 400, { error: "Image is outside the documentation workspace." });
        const info = await stat(absolute);
        if (!info.isFile() || info.size > 20 * 1024 * 1024) return sendJson(res, 400, { error: "Image exceeds the 20 MB viewer limit." });
        const content = await readFile(absolute);
        res.writeHead(200, {
          "Content-Type": types[extname(candidate).toLowerCase()],
          "Cache-Control": "no-store",
          "X-Content-Type-Options": "nosniff",
          "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox",
        });
        return res.end(content);
      }
      if (url.pathname.startsWith("/api/")) {
        if (req.headers["x-canvas-token"] !== token) return sendJson(res, 403, { error: "Canvas token is missing or invalid." });
        if (req.method === "GET" && url.pathname === "/api/index") return sendJson(res, 200, { documents: await getIndex(repositoryRoot) });
        if (req.method === "POST" && url.pathname === "/api/refresh") return sendJson(res, 200, { documents: await getIndex(repositoryRoot, true) });
        if (req.method === "POST" && url.pathname === "/api/start-conversation") {
          const body = await readBody(req);
          const target = body.target ?? "current";
          if (!["current", "new"].includes(target)) return sendJson(res, 400, { error: "Select current or new conversation." });
          const documents = await getIndex(repositoryRoot, true);
          const document = documents.find((item) => item.path === body.path && item.kind === "markdown");
          if (!document) return sendJson(res, 400, { error: "Select an indexed Markdown document." });
          if (!requestConversation) return sendJson(res, 503, { error: "The conversation handoff is unavailable." });
          return sendJson(res, 202, {
            path: document.path,
            ...await requestConversation(document.path, { target, absolutePath: join(repositoryRoot, document.path) }),
          });
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

      const assetMap = {
        "/": "index.html", "/app.js": "app.js", "/styles.css": "styles.css",
        "/zava-logo.png": "zava-logo.png",
        "/markdown-editor.js": "markdown-editor.js",
        "/diagram.html": "diagram.html", "/diagram.js": "diagram.js",
        "/vendor/toastui-editor.js": "vendor/toastui-editor.js",
        "/vendor/mermaid.js": "vendor/mermaid.js",
        "/vendor/toastui-editor.css": "vendor/toastui-editor.css",
      };
      const asset = assetMap[url.pathname];
      if (!asset) { res.writeHead(404); return res.end("Not found"); }
      let content = await readFile(join(assetsDirectory, asset));
      if (asset === "index.html") {
        content = content.toString("utf8").replace("__CANVAS_TOKEN__", token).replace("__INITIAL_PATH__", encodeURIComponent(initialPath));
        res.setHeader("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'");
      }
      if (asset === "diagram.html") {
        res.setHeader("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; img-src data:; sandbox allow-scripts; base-uri 'none'");
      }
      const type = extname(asset) === ".png" ? "image/png" : extname(asset) === ".js" ? "text/javascript" : extname(asset) === ".css" ? "text/css" : "text/html";
      res.writeHead(200, { "Content-Type": type === "image/png" ? type : `${type}; charset=utf-8`, "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" });
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
