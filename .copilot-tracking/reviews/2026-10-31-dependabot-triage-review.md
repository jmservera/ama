---
title: Dependabot alert triage review
ms.date: 2026-10-31
---

Execution: executed once after implementation. Outcome: conformant for the assessed boundary (manifests and lock files only).

* All 10 open alerts map to patched versions in the changed files; none left unfixed.
* Diff touches no product runtime code. Vendored bundles were rebuilt via the supported build step; mermaid.js and the workbench sanitizer embed DOMPurify 3.4.17, but toastui-editor.js still embeds the editor's own prebuilt DOMPurify 2.3.3.
* Follow-up: replace or patch @toast-ui/editor (or route its sanitizer through DOMPurify 3.4.17) to remove the embedded 2.3.3.
* Residual risk (follow-up): the katex 0.16 to 0.18 and nanoid 4 to 5 overrides are outside upstream's declared ranges; run the full diagram export in a browser-enabled environment. Alert closure is confirmed by GitHub only after merge.
