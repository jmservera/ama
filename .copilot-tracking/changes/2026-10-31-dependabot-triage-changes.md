---
title: Dependabot alert triage changes
ms.date: 2026-10-31
---

* tools/program-workbench-assets/package.json, package-lock.json: dompurify 3.4.16 to 3.4.17.
* .github/extensions/program-workbench/assets/vendor/mermaid.js, toastui-editor.js: rebuilt with `npm run build`; the embedded workbenchSanitize DOMPurify and mermaid now report 3.4.17.
* Remaining gap: @toast-ui/editor 3.2.2 ships a prebuilt dist with DOMPurify 2.3.3 inline, so toastui-editor.js still embeds 2.3.3 in the editor's own sanitizer. No dependency bump can change this.
* docs/capstone/.../anc/package.json, package-lock.json: overrides lodash-es 4.18.1, katex 0.18.2, nanoid 3.3.18 (excalidraw) and 5.1.16 (mermaid-to-excalidraw).
* src/build-requirements.in, build-requirements.txt: setuptools 84.1.0 to 84.2.1 (pip-compile, hashes regenerated).

## Validation

* `npm ci --ignore-scripts` and `npm audit` in both folders: 0 vulnerabilities.
* `node --check vendor-editor.mjs` and `node --check export_diagrams.mjs`: pass.
* `node --test .github/extensions/program-workbench/tests/*.mjs`: 6 pass, 0 fail.
* nanoid 5 import under node: pass. Full diagram export (needs a browser) not run.
