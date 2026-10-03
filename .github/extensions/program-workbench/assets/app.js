import { createDocumentEditor } from "./markdown-editor.js";

const token = document.querySelector('meta[name="canvas-token"]').content;
const initialPath = decodeURIComponent(document.querySelector('meta[name="initial-path"]').content || "");
const state = { documents: [], current: null, dirty: false, mode: "preview", view: "overview" };
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const documentEditor = createDocumentEditor((content) => setDirty(content !== state.current?.content));
const api = async (path, options = {}) => {
  const response = await fetch(path, { ...options, headers: { "Content-Type": "application/json", "X-Canvas-Token": token, ...(options.headers || {}) } });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "The workspace request failed.");
  return data;
};

function escapeHtml(value = "") {
  return value.replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function inlineMarkdown(value) {
  return escapeHtml(value)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => {
      const linked = resolveLinkedPath(href.split("#")[0]);
      return linked ? `<a href="#" data-doc-path="${escapeHtml(linked)}">${label}</a>` : `<span>${label}</span>`;
    });
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, "").split(/\r?\n/);
  let html = "", inList = false, inCode = false, code = [], table = [];
  const flushList = () => { if (inList) { html += "</ul>"; inList = false; } };
  const flushTable = () => {
    if (!table.length) return;
    const rows = table.map((line) => line.replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim()));
    if (rows.length > 1 && rows[1].every((cell) => /^:?-{3,}:?$/.test(cell))) {
      html += `<table><thead><tr>${rows[0].map((cell) => `<th>${inlineMarkdown(cell)}</th>`).join("")}</tr></thead><tbody>${rows.slice(2).map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
    } else html += table.map((line) => `<p>${inlineMarkdown(line)}</p>`).join("");
    table = [];
  };
  for (const line of lines) {
    if (line.startsWith("```")) {
      flushList(); flushTable();
      if (inCode) { html += `<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`; code = []; }
      inCode = !inCode; continue;
    }
    if (inCode) { code.push(line); continue; }
    if (line.includes("|") && /^\s*\|?.+\|.+\|?\s*$/.test(line)) { flushList(); table.push(line); continue; }
    flushTable();
    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) { flushList(); const level = heading[1].length; html += `<h${level}>${inlineMarkdown(heading[2])}</h${level}>`; continue; }
    const list = line.match(/^\s*[*-]\s+(.+)$/);
    if (list) { if (!inList) { html += "<ul>"; inList = true; } html += `<li>${inlineMarkdown(list[1])}</li>`; continue; }
    flushList();
    if (/^>\s?/.test(line)) html += `<blockquote>${inlineMarkdown(line.replace(/^>\s?/, ""))}</blockquote>`;
    else if (line.trim()) html += `<p>${inlineMarkdown(line)}</p>`;
  }
  flushList(); flushTable();
  if (inCode) html += `<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`;
  return html;
}

function resolveLinkedPath(href) {
  if (!state.current || !href || /^(https?:|mailto:|#)/i.test(href)) return null;
  const parts = state.current.path.split("/"); parts.pop();
  for (const segment of decodeURIComponent(href).split("/")) {
    if (segment === "..") parts.pop(); else if (segment !== ".") parts.push(segment);
  }
  const path = parts.join("/");
  return state.documents.some((doc) => doc.path === path) ? path : null;
}

function showToast(message) {
  const toast = $("#toast"); toast.textContent = message; toast.classList.add("visible");
  clearTimeout(showToast.timeout); showToast.timeout = setTimeout(() => toast.classList.remove("visible"), 3200);
}

function setDirty(dirty) {
  state.dirty = dirty;
  $("#save-status").textContent = dirty ? "Unsaved changes" : "All changes saved";
  $("#save-button").disabled = !dirty || !state.current?.editable;
}

function switchView(view) {
  state.view = view;
  $$(".view").forEach((node) => node.classList.add("hidden"));
  $(`#${view}-view`)?.classList.remove("hidden");
  $$(".rail-button").forEach((button) => button.classList.toggle("active", button.dataset.view === view));
  $("#main").scrollTop = 0;
}

function categoryOrder(category) {
  return ["Project documents", "BRDs", "PRDs", "ADRs", "Ideas", "Research", "Regulatory evidence", "Knowledge base", "Methods", "Resources", "Presentations", "Visuals"].indexOf(category);
}

function renderLibrary() {
  const groups = Map.groupBy ? Map.groupBy(state.documents, (doc) => doc.category) : state.documents.reduce((map, doc) => map.set(doc.category, [...(map.get(doc.category) || []), doc]), new Map());
  $("#category-list").innerHTML = [...groups.entries()].sort((a, b) => categoryOrder(a[0]) - categoryOrder(b[0])).map(([category, docs], groupIndex) => `
    <section class="category">
      <button class="category-toggle" type="button" aria-expanded="${groupIndex < 4}" data-category="${escapeHtml(category)}"><span>${escapeHtml(category)}</span><span class="category-count">${docs.length}</span></button>
      <div class="category-documents ${groupIndex < 4 ? "" : "hidden"}">${docs.map((doc) => `<button class="library-document" type="button" data-path="${escapeHtml(doc.path)}" title="${escapeHtml(doc.path)}">${escapeHtml(doc.title)}</button>`).join("")}</div>
    </section>`).join("");
  $("#document-count").textContent = `${state.documents.length} connected records`;
  $$(".category-toggle").forEach((button) => button.addEventListener("click", () => {
    const list = button.nextElementSibling; list.classList.toggle("hidden"); button.setAttribute("aria-expanded", String(!list.classList.contains("hidden")));
  }));
  $$(".library-document").forEach((button) => button.addEventListener("click", () => openDocument(button.dataset.path)));
  $$(".library-document").forEach((button) => button.classList.toggle("active", button.dataset.path === state.current?.path));
}

function renderOverview() {
  const count = (category) => state.documents.filter((doc) => doc.category === category).length;
  const metrics = [
    [count("BRDs") + count("PRDs"), "Requirements"],
    [count("ADRs") + count("Ideas"), "Decisions & ideas"],
    [count("Research") + count("Regulatory evidence"), "Evidence records"],
    [count("Presentations"), "Presentations"],
  ];
  $("#pulse-number").textContent = state.documents.length;
  $("#metric-grid").innerHTML = metrics.map(([value, label], index) => `<div class="metric metric-${index + 1}"><strong>${value}</strong><span>${label}</span></div>`).join("");
  const preferred = ["docs/case_study_48_original.md", "docs/case_study_48_addendum.md", "docs/brds/agentic-retrofit-programme-brd.md", "docs/reference/README.md"];
  $("#spine-list").innerHTML = preferred.map((path, index) => state.documents.find((doc) => doc.path === path)).filter(Boolean).map((doc, index) => `<button class="spine-item" type="button" data-path="${escapeHtml(doc.path)}"><span class="spine-number">0${index + 1}</span><span><strong>${escapeHtml(doc.title)}</strong><small>${escapeHtml(doc.description || doc.category)}</small></span><span class="spine-arrow">&rarr;</span></button>`).join("");
  $("#recent-list").innerHTML = [...state.documents].sort((a, b) => b.modified.localeCompare(a.modified)).slice(0, 5).map((doc) => `<button class="recent-item" type="button" data-path="${escapeHtml(doc.path)}"><span><strong>${escapeHtml(doc.title)}</strong><small>${escapeHtml(doc.category)}</small></span><time>${escapeHtml(doc.date)}</time></button>`).join("");
  $$(".spine-item, .recent-item").forEach((button) => button.addEventListener("click", () => openDocument(button.dataset.path)));
}

function renderContextLinks(selector, paths) {
  const container = $(selector);
  container.innerHTML = paths.length ? paths.map((path) => {
    const doc = state.documents.find((item) => item.path === path);
    return `<button class="context-link" type="button" data-path="${escapeHtml(path)}">${escapeHtml(doc?.title || path)}</button>`;
  }).join("") : `<p class="context-empty">No linked records found.</p>`;
  container.querySelectorAll("button").forEach((button) => button.addEventListener("click", () => openDocument(button.dataset.path)));
}

let documentRequest = 0;
async function openDocument(path, refreshOnly = false) {
  const summary = state.documents.find((doc) => doc.path === path);
  if (!summary) return;
  if (summary.kind !== "markdown") { showToast("Presentations and visual files are read-only in version one."); return; }
  if (state.dirty && !confirm("Discard unsaved changes and open another document?")) return;
  const request = ++documentRequest;
  try {
    const doc = await api(`/api/document?path=${encodeURIComponent(path)}`);
    if (request !== documentRequest) return;
    if (refreshOnly && (state.dirty || state.current?.path !== path || state.current.content === doc.content)) return;
    state.current = doc; setDirty(false); switchView("documents");
    $("#document-title").textContent = doc.title;
    $("#document-description").textContent = doc.description || doc.excerpt;
    $("#evidence-badge").textContent = doc.evidence;
    $("#breadcrumbs").textContent = doc.path.split("/").slice(0, -1).join("  /  ");
    documentEditor.load(doc.content);
    $("#markdown-preview").innerHTML = renderMarkdown(doc.content);
    $("#meta-updated").textContent = doc.date;
    $("#meta-path").textContent = doc.path;
    $("#readonly-note").textContent = doc.readOnlyReason || "";
    $("#readonly-note").classList.toggle("hidden", doc.editable);
    const editButton = $('.mode-button[data-mode="edit"]');
    editButton.disabled = !doc.editable;
    editButton.title = doc.editable ? "Edit this Markdown document" : doc.readOnlyReason;
    $("#agent-editor-button").disabled = !doc.editable;
    renderContextLinks("#outgoing-links", doc.outgoing || []);
    renderContextLinks("#backlinks", doc.backlinks || []);
    $$(".library-document").forEach((button) => button.classList.toggle("active", button.dataset.path === path));
    setMode("preview");
  } catch (error) { showToast(error.message); }
}

function setMode(mode) {
  if (mode === "edit" && !state.current?.editable) return;
  state.mode = mode;
  $$(".mode-button").forEach((button) => button.classList.toggle("active", button.dataset.mode === mode));
  $("#markdown-preview").classList.toggle("hidden", mode !== "preview");
  $("#editor-wrap").classList.toggle("hidden", mode !== "edit");
  if (mode === "preview" && state.current) {
    $("#markdown-preview").innerHTML = renderMarkdown(documentEditor.getContent());
    $("#markdown-preview").querySelectorAll("[data-doc-path]").forEach((link) => link.addEventListener("click", (event) => { event.preventDefault(); openDocument(link.dataset.docPath); }));
  }
  if (mode === "edit") documentEditor.focus();
}

async function saveCurrent() {
  if (!state.current?.editable || !state.dirty) return;
  try {
    const doc = state.current;
    const content = documentEditor.getContent();
    const result = await api("/api/document", { method: "PUT", body: JSON.stringify({ path: doc.path, content }) });
    if (state.current === doc) {
      doc.content = content; doc.modified = result.savedAt;
      setDirty(documentEditor.getContent() !== content);
    }
    showToast("Markdown saved to the repository.");
  } catch (error) { showToast(`Save failed: ${error.message}`); }
}

async function openEditorViaAgent() {
  if (!state.current?.editable) return;
  if (state.dirty) { showToast("Save or discard canvas edits before opening the app editor."); return; }
  const button = $("#agent-editor-button");
  button.disabled = true;
  try {
    await api("/api/open-editor", { method: "POST", body: JSON.stringify({ path: state.current.path }) });
    showToast("Editor request sent to the agent. Opening may take an agent turn.");
  } catch (error) { showToast(`Editor request failed: ${error.message}`); }
  finally { button.disabled = !state.current?.editable; }
}

let searchTimer;
async function runSearch(query) {
  clearTimeout(searchTimer);
  if (!query.trim()) { switchView(state.current ? "documents" : "overview"); return; }
  searchTimer = setTimeout(async () => {
    try {
      const { documents } = await api(`/api/search?q=${encodeURIComponent(query)}`);
      $("#search-title").textContent = `${documents.length} result${documents.length === 1 ? "" : "s"} for "${query}"`;
      $("#search-results").innerHTML = documents.length ? documents.map((doc) => `<button class="search-result" type="button" data-path="${escapeHtml(doc.path)}"><strong>${escapeHtml(doc.title)}</strong><small>${escapeHtml(doc.category)} | ${escapeHtml(doc.evidence)}</small><p>${escapeHtml(doc.description || doc.excerpt || doc.path)}</p></button>`).join("") : `<p class="muted">No matching programme records.</p>`;
      $$(".search-result").forEach((button) => button.addEventListener("click", () => openDocument(button.dataset.path)));
      switchView("search");
    } catch (error) { showToast(error.message); }
  }, 220);
}

let refreshing = false;
async function refresh(notify = true) {
  if (refreshing) return;
  refreshing = true;
  const path = state.current?.path;
  const view = state.view;
  const mode = state.mode;
  const scrollTop = $("#main").scrollTop;
  try {
    const data = await api("/api/refresh", { method: "POST", body: "{}" });
    state.documents = data.documents; renderLibrary(); renderOverview();
    if (path && !state.dirty && state.current?.path === path) {
      await openDocument(path, true);
      switchView(view);
      setMode(mode);
      $("#main").scrollTop = scrollTop;
    }
    if (notify) showToast("Document index refreshed.");
  }
  catch (error) { showToast(error.message); }
  finally { refreshing = false; }
}

async function initialize() {
  try {
    const data = await api("/api/index"); state.documents = data.documents; renderLibrary(); renderOverview();
    if (initialPath) await openDocument(initialPath);
  } catch (error) { showToast(`Workspace failed to load: ${error.message}`); }
}

$$('.rail-button').forEach((button) => button.addEventListener("click", () => switchView(button.dataset.view)));
$$('.mode-button').forEach((button) => button.addEventListener("click", () => setMode(button.dataset.mode)));
$("#save-button").addEventListener("click", saveCurrent);
$("#agent-editor-button").addEventListener("click", openEditorViaAgent);
$("#refresh-button").addEventListener("click", () => refresh());
$("#global-search").addEventListener("input", (event) => runSearch(event.target.value));
$("#connections-open-docs").addEventListener("click", () => switchView("overview"));
window.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") { event.preventDefault(); saveCurrent(); }
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") { event.preventDefault(); $("#global-search").focus(); }
});
window.addEventListener("beforeunload", (event) => { if (state.dirty) { event.preventDefault(); event.returnValue = ""; } });
window.addEventListener("focus", () => refresh(false));
document.addEventListener("visibilitychange", () => { if (!document.hidden) refresh(false); });
initialize();
