export function splitFrontmatter(content) {
  const match = content.match(/^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/);
  return { metadata: match?.[0] || "", body: match ? content.slice(match[0].length) : content };
}

export function requiresSourceEditing(body) {
  return /^(?:>\s*\[![A-Z]+\]|```(?:mermaid|math)\b| {0,3}<\/?[A-Za-z][^>]*>|\[[^\]]+\]:)/m.test(body)
    || /^(?: {0,3})<[A-Za-z!/]/m.test(body)
    || /<\/?[A-Za-z][^>]*>/.test(body)
    || /!\[[^\]]*\]\(|\$\$|^\|.*\\\|/m.test(body);
}

export function createDocumentEditor(onChange) {
  const metadata = document.querySelector("#frontmatter-editor");
  const metadataWrap = document.querySelector("#frontmatter-wrap");
  const visual = document.querySelector("#visual-editor");
  const note = document.querySelector("#editor-note");
  let editor = null, original = "", draft = "", initialMarkdown = "", header = "", originalBody = "", loading = false, sourceOnly = false, switching = false, userEdited = false;

  visual.addEventListener("beforeinput", () => { userEdited = true; }, true);
  visual.addEventListener("keydown", (event) => {
    if (event.key.length === 1 || ["Backspace", "Delete", "Enter", "Tab"].includes(event.key)) userEdited = true;
  }, true);

  visual.addEventListener("click", (event) => {
    if (!editor) return;
    if (!event.target.closest(".toastui-editor-mode-switch")) {
      if (event.target.closest(".toastui-editor-toolbar, .toastui-editor-popup")) userEdited = true;
      return;
    }
    if (event.target.textContent === "WYSIWYG" && requiresSourceEditing(editor.getMarkdown())) {
      event.stopImmediatePropagation();
      note.classList.remove("hidden");
      note.textContent = "This Markdown uses extended syntax. Keep editing in Markdown mode to preserve it.";
      return;
    }
    switching = true;
    queueMicrotask(() => { switching = false; });
  }, true);

  function update() {
    if (loading || switching) return;
    const currentHeader = metadata.value === header.replace(/\r\n/g, "\n") ? header : metadata.value;
    let body = originalBody;
    if (userEdited && editor) {
      const newline = original.includes("\r\n") ? "\r\n" : "\n";
      body = editor.getMarkdown().replace(/\r?\n/g, newline);
      if (/^\r?\n/.test(originalBody) && !/^\r?\n/.test(body)) body = newline + body;
      if (/\r?\n$/.test(originalBody) && !/\r?\n$/.test(body)) body += newline;
    }
    draft = currentHeader + body;
    onChange(draft);
  }

  metadata.addEventListener("input", update);

  return {
    load(content) {
      loading = true;
      original = draft = content;
      userEdited = false;
      const parts = splitFrontmatter(content);
      header = parts.metadata;
      const body = parts.body;
      originalBody = body;
      metadata.value = header;
      sourceOnly = requiresSourceEditing(body);
      metadataWrap.classList.toggle("hidden", !header);
      note.classList.toggle("hidden", !sourceOnly);
      note.textContent = sourceOnly
        ? "TOAST Markdown mode protects this document's callouts, diagrams, images or extended syntax. WYSIWYG conversion is blocked while that syntax is present."
        : "";
      {
        if (!globalThis.toastui?.Editor) throw new Error("The local TOAST editor failed to load.");
        if (editor) {
          editor.changeMode("markdown", true);
          editor.setMarkdown(body, false);
        } else {
          editor = new toastui.Editor({
            el: visual,
            height: "100%",
            initialEditType: "markdown",
            previewStyle: "tab",
            initialValue: body,
            usageStatistics: false,
            customHTMLSanitizer: globalThis.workbenchSanitize,
            hideModeSwitch: false,
            autofocus: false,
            toolbarItems: [["heading", "bold", "italic", "strike"], ["hr", "quote"], ["ul", "ol", "task"], ["table", "link"], ["code", "codeblock"]],
          });
          editor.on("changeMode", () => {
            if (draft === original) initialMarkdown = editor.getMarkdown();
          });
          editor.on("change", () => {
            if (loading || switching) return;
            if (!userEdited) { update(); return; }
            // Opening or switching modes must not turn serializer normalization into an edit.
            if (editor.getMarkdown() === initialMarkdown && metadata.value === header) {
              draft = original; onChange(draft);
            } else update();
          });
        }
        initialMarkdown = editor.getMarkdown();
      }
      loading = false;
    },
    getContent() { return draft; },
    focus() { editor?.focus(); },
  };
}
