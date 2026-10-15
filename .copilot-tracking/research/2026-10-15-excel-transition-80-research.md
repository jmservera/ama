---
title: Research for issue 80 Excel transition
description: Evidence for importing, exporting and comparing Excel in src/importer
ms.date: 2026-10-15
---

## Task

Issue #80: import declared workbook structures with preview and lineage without changing the source, export every list, retain history independent of the AI provider, agree staged thresholds. Research disposition: executed. Planning Readiness: Ready (for the library slice).

## Evidence

* Issue #80 comment (2026-10-15): the import workload is `zava_forward.importer` (ADR 0001 quarantine design), calls `doc_controls` in `core`, owns its image and limited SQL role.
* `docs/adrs/0006-src-layout-and-cutover.md` (Accepted): all new code in `src/`, `mvp/` receives none; core imports no workload; api imports agents only until #144; Azure only for deployment.
* `src/importer` held a version module, fixtures and dependency-rule test; depends on `zava-forward-core[blob]` only.
* `src/core/.../store.py` `import_check` and `export_csv` are the prior art (CSV only, regex column guess, no lineage, no history); left unchanged.
* `src/core/.../doc_controls.py` `LocalSignatureScanner` checks magic bytes and the synthetic malware marker; reused.
* Environment: Python 3.12, pip only, no openpyxl, Docker permission denied.

## Decisions

* Standard library only for .xlsx (no new pinned dependency, smaller attack surface); reader rejects entities, oversize parts and returns values only.
* SQL portable: qmark parameters, VARCHAR/INT/NVARCHAR(4000), explicit insert then update.
* Cannot be done here: owner thresholds, web surface and per-list export buttons (api cannot import importer), AI-assisted mapping, image and SQL role evidence.
