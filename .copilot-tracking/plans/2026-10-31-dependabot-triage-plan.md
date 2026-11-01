---
title: Dependabot alert triage plan
ms.date: 2026-10-31
---

* Workbench: bump the dompurify override to 3.4.17, drop the stale nested lock entry, regenerate the lock with npm.
* anc: add npm `overrides` (lodash-es, katex, nanoid per parent) because upstream pins are exact; regenerate the lock.
* setuptools: bump `build-requirements.in` and recompile `build-requirements.txt` with pip-compile (pip only, hashes kept).
* No product runtime code or vendored assets are changed; `npm run build` is not run because it rewrites vendored runtime assets.
* Validation (focused): npm ci, npm audit, node --check, program-workbench node tests.

Critique: single pass, compatible, no findings that change scope. The nanoid 5.x override on mermaid-to-excalidraw is a major-version jump, so the export tool needs a smoke check.
