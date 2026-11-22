---
title: Issue 2008 research, 2026-11-22
description: Research for the web .xlsx import preview (remaining gap of #2008)
ms.date: 2026-11-22
---

## Disposition

Research executed. Planning Readiness: Ready. Refs #2008, #80.

## Evidence

* Gap: `importView` in `src/api/src/zava_forward/api/web/app.js` accepts `.csv` and posts text to `/api/import-check` (`Store.import_check`, `src/core/.../store.py`), which does no stage or duplicate-reference checks. Prior notes: `docs/reference/research/issue-2008-demo-workbook-import-evidence-2026-11-18.md` (the 2026-11-22 rerun note lives only on `origin/docs/issue-2237-2008-evidence`, not on this base).
* Reusable code: `src/importer/.../xlsx.py` (stdlib only reader with size, entity, formula guards) and `mapping.py` (declared `case-list` structure, alias mapping, conflicts, row preview with lineage, `preview_bytes` scans and hashes bytes). Both depend on `core` and the standard library only.
* Boundary: `src/api/tests/test_dependency_rule.py` allows api to import only `api`, `core`, `agents`; the API image (`src/api/Dockerfile`) builds `core`, `agents`, `api` wheels only; importer README lists the web surface as not built until #144.
* No new dependency is needed: the reader is standard library. `src/api/pyproject.toml` already depends on core.
* Request limit: `_body` caps at 8,000,000 bytes, so base64 JSON of a workbook up to about 5.9 MB fits; importer's own cap is 10 MB (the lower limit applies, stated in plain words).

## Options

| Option | Effect | Verdict |
| --- | --- | --- |
| A. Make api import `importer` and ship it in the image | Breaks the dependency rule and changes the Dockerfile and wheels | Rejected: deployment/packaging change |
| B. Move `xlsx.py` and `mapping.py` into `core`; importer keeps same module paths as aliases; api calls core | Reuses code unchanged, keeps the rule and the image | Chosen |
| C. Copy the logic into the store | Duplicates guards | Rejected |

## Design

* `core/xlsx.py` and `core/import_preview.py` hold the moved code (git mv, imports adjusted). `importer/xlsx.py` and `importer/mapping.py` alias the core modules so every existing import and `mock.patch` target still works.
* `Store.import_check_workbook(name, data)` returns mapping, conflicts, matched-existing count and capped row preview; read only.
* `/api/import-check` accepts `{"name", "xlsx_base64"}` besides `{"text"}`; same role gating (unchanged route).
* `app.js` `importView` accepts `.xlsx`, shows mapping table, conflicts list and row preview table (captioned, headers, status words not colour-only).

## Tier

This changes `src/` code: full-tier classification. The coordinator owns the `rpi-checks.py --all` run; this worker runs targeted tests only. Not SQL or security-control change (read-only endpoint, same auth, same scan); no deployment.

## Live criteria

Criterion 3 of the issue needs the deployed demo. Deployment is forbidden for this task, so the live run on the new screen cannot be proven; it is proven locally with Playwright against a local server, and the live state is restated.
