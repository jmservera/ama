import { readdir, readFile, stat, writeFile } from "node:fs/promises";
import path from "node:path";

const TEXT_EXTENSIONS = new Set([".md"]);
const PRESENTATION_EXTENSIONS = new Set([".pptx"]);
const VISUAL_EXTENSIONS = new Set([".svg", ".excalidraw"]);
const MAX_DOCUMENT_BYTES = 2 * 1024 * 1024;

const EDIT_POLICIES = [
  { test: (p) => p === "docs/case_study_48_original.md", reason: "The original case study is preserved as an immutable baseline." },
  { test: (p) => p === "docs/reference/memory.md", reason: "Project memory is owner-controlled and edited only on explicit request." },
  { test: (p) => p.startsWith("docs/reference/regulatory/"), reason: "Regulatory snapshots are immutable evidence records." },
];

function toPosix(value) {
  return value.split(path.sep).join("/");
}

function safeRelative(root, requestedPath) {
  const normalized = toPosix(path.normalize(String(requestedPath ?? "")).replace(/^([/\\])+/, ""));
  const absolute = path.resolve(root, normalized);
  const relative = toPosix(path.relative(root, absolute));
  if (!normalized || relative.startsWith("../") || path.isAbsolute(relative)) {
    throw new Error("Path is outside the repository workspace.");
  }
  return { absolute, relative };
}

function parseFrontmatter(content) {
  const result = {};
  if (!content.startsWith("---\n") && !content.startsWith("---\r\n")) return result;
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return result;
  for (const line of match[1].split(/\r?\n/)) {
    const separator = line.indexOf(":");
    if (separator < 1) continue;
    const key = line.slice(0, separator).trim();
    const value = line.slice(separator + 1).trim().replace(/^['"]|['"]$/g, "");
    result[key] = value;
  }
  return result;
}

function firstHeading(content) {
  return content.match(/^#{1,2}\s+(.+)$/m)?.[1]?.trim();
}

function cleanExcerpt(content) {
  return content
    .replace(/^---[\s\S]*?---\s*/m, "")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/[#>*_`|\[\]()!-]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 240);
}

function categoryFor(relative, extension) {
  if (PRESENTATION_EXTENSIONS.has(extension)) return "Presentations";
  if (VISUAL_EXTENSIONS.has(extension)) return "Visuals";
  if (relative.includes("/brds/")) return "BRDs";
  if (relative.includes("/prds/")) return "PRDs";
  if (relative.includes("/adrs/")) return "ADRs";
  if (relative.includes("/ideas/")) return "Ideas";
  if (relative.includes("/reference/research/")) return "Research";
  if (relative.includes("/reference/regulatory/")) return "Regulatory evidence";
  if (relative.includes("/reference/method/")) return "Methods";
  if (relative.includes("/reference/resources/")) return "Resources";
  if (relative.includes("/reference/")) return "Knowledge base";
  return "Project documents";
}

function evidenceLabel(relative) {
  if (relative === "docs/case_study_48_original.md") return "case-study fact";
  if (relative.includes("/regulatory/")) return "source snapshot";
  if (relative.includes("/research/")) return "research synthesis";
  if (relative.includes("/ideas/")) return "hypothesis";
  if (relative.includes("/brds/") || relative.includes("/prds/") || relative.includes("/adrs/")) return "proposal";
  return "project document";
}

export function editPolicy(relative, extension = path.extname(relative).toLowerCase()) {
  const policyPath = relative.toLowerCase();
  if (!TEXT_EXTENSIONS.has(extension)) return { editable: false, reason: "Only Markdown documents are editable in version one." };
  const policy = EDIT_POLICIES.find((entry) => entry.test(policyPath));
  return policy ? { editable: false, reason: policy.reason } : { editable: true, reason: "" };
}

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const results = [];
  for (const entry of entries) {
    if (entry.name.startsWith(".")) continue;
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) results.push(...await walk(target));
    else results.push(target);
  }
  return results;
}

export async function buildIndex(root) {
  const candidates = [path.join(root, "README.md")];
  for (const folder of ["docs"]) {
    try { candidates.push(...await walk(path.join(root, folder))); } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }

  const documents = [];
  for (const absolute of candidates) {
    const extension = path.extname(absolute).toLowerCase();
    if (![...TEXT_EXTENSIONS, ...PRESENTATION_EXTENSIONS, ...VISUAL_EXTENSIONS].includes(extension)) continue;
    const relative = toPosix(path.relative(root, absolute));
    const fileStat = await stat(absolute);
    let title = path.basename(relative, extension).replace(/[-_]/g, " ");
    let description = "";
    let date = fileStat.mtime.toISOString().slice(0, 10);
    let excerpt = "";
    if (TEXT_EXTENSIONS.has(extension) && fileStat.size <= MAX_DOCUMENT_BYTES) {
      const content = await readFile(absolute, "utf8");
      const frontmatter = parseFrontmatter(content);
      title = frontmatter.title || firstHeading(content) || title;
      description = frontmatter.description || "";
      date = frontmatter["ms.date"] || date;
      excerpt = cleanExcerpt(content);
    }
    const policy = editPolicy(relative, extension);
    documents.push({
      path: relative,
      title,
      description,
      excerpt,
      date,
      category: categoryFor(relative, extension),
      evidence: evidenceLabel(relative),
      kind: TEXT_EXTENSIONS.has(extension) ? "markdown" : PRESENTATION_EXTENSIONS.has(extension) ? "presentation" : "visual",
      editable: policy.editable,
      readOnlyReason: policy.reason,
      size: fileStat.size,
      modified: fileStat.mtime.toISOString(),
    });
  }
  return documents.sort((a, b) => a.category.localeCompare(b.category) || a.title.localeCompare(b.title));
}

function resolveMarkdownLinks(root, relative, content) {
  const links = [];
  const linkPattern = /\[[^\]]+\]\(([^)]+)\)/g;
  for (const match of content.matchAll(linkPattern)) {
    const href = match[1].split("#")[0].trim();
    if (!href || /^(https?:|mailto:)/i.test(href)) continue;
    const resolved = toPosix(path.normalize(path.join(path.dirname(relative), decodeURIComponent(href))));
    try {
      const safe = safeRelative(root, resolved);
      links.push(safe.relative);
    } catch { /* Ignore links outside the repository. */ }
  }
  return [...new Set(links)];
}

export async function readDocument(root, requestedPath, index) {
  const { absolute, relative } = safeRelative(root, requestedPath);
  if (path.extname(relative).toLowerCase() !== ".md") throw new Error("Only Markdown documents can be opened in the editor.");
  const fileStat = await stat(absolute);
  if (fileStat.size > MAX_DOCUMENT_BYTES) throw new Error("This document is too large for the canvas editor.");
  const content = await readFile(absolute, "utf8");
  const outgoing = resolveMarkdownLinks(root, relative, content).filter((p) => index.some((item) => item.path === p));
  const backlinks = [];
  for (const candidate of index.filter((item) => item.kind === "markdown" && item.size <= MAX_DOCUMENT_BYTES && item.path !== relative)) {
    const source = await readFile(path.join(root, candidate.path), "utf8");
    if (resolveMarkdownLinks(root, candidate.path, source).includes(relative)) backlinks.push(candidate.path);
  }
  return { content, outgoing, backlinks, ...index.find((item) => item.path === relative) };
}

export async function saveDocument(root, requestedPath, content) {
  const { absolute, relative } = safeRelative(root, requestedPath);
  const extension = path.extname(relative).toLowerCase();
  const policy = editPolicy(relative, extension);
  if (!policy.editable) throw new Error(policy.reason);
  if (typeof content !== "string") throw new Error("Document content must be text.");
  if (Buffer.byteLength(content, "utf8") > MAX_DOCUMENT_BYTES) throw new Error("Document exceeds the 2 MB editor limit.");
  await writeFile(absolute, content, "utf8");
  return { path: relative, savedAt: new Date().toISOString() };
}

export async function searchDocuments(root, query, index) {
  const terms = String(query ?? "").toLowerCase().trim().split(/\s+/).filter(Boolean);
  if (!terms.length) return index.slice(0, 50);
  const scored = [];
  for (const item of index) {
    let haystack = `${item.title} ${item.description} ${item.excerpt} ${item.path} ${item.category}`.toLowerCase();
    if (item.kind === "markdown" && item.size <= MAX_DOCUMENT_BYTES) {
      haystack += ` ${(await readFile(path.join(root, item.path), "utf8")).toLowerCase()}`;
    }
    if (!terms.every((term) => haystack.includes(term))) continue;
    const titleHits = terms.filter((term) => item.title.toLowerCase().includes(term)).length;
    const pathHits = terms.filter((term) => item.path.toLowerCase().includes(term)).length;
    scored.push({ ...item, score: titleHits * 5 + pathHits * 2 + 1 });
  }
  return scored.sort((a, b) => b.score - a.score || a.title.localeCompare(b.title)).slice(0, 100);
}
