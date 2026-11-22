---
title: Issue 2008 changes, 2026-11-22
ms.date: 2026-11-22
---

## Changes

* Moved `xlsx.py` and `mapping.py` from `src/importer` to `src/core` (`xlsx.py`, `import_preview.py`); importer, its tests and `tools/make-demo-case-list.py` import from core.
* `Store.import_check_workbook` and the `xlsx_base64` branch of `POST /api/import-check` (`src/api/.../server.py`).
* `importView` in `app.js` accepts `.xlsx` and renders mapping, conflicts and row preview; accessibility baseline table count 15 to 17.
* Tests in `src/api/tests/test_mvp.py`; docs in the api and importer READMEs, the research note, KB index and log.
* Evidence: `docs/reference/research/demo-workbook/evidence-2026-11-22-local/`.

## Tier

Full classification (src change). Targeted checks only; no `rpi-checks.py --all`. Not SQL, not a security-control change, not deployed.

## Validation

Importer 125 tests OK; api focused suites OK (mvp, accessibility baseline, content standard, polish, heading hierarchy, dependency rule, list export, role matrix and inventory); tools test OK; mypy api and importer clean, core at its 3 existing errors; ruff clean; core suite: link fix in `microsoft-fabric-fit-assessment.md`; 57 other failures are environment related (see review). Playwright local proof recorded.

## Per-criterion table

| Criterion | Result | Evidence or reason |
| --- | --- | --- |
| Synthetic `.xlsx`, declared structure, no real data, generator committed | Proven | Existing workbook, generator, test |
| Clean rows, mapping differences and conflicts shown by row-level preview | Proven locally on the web screen | `rendered-text.txt`, screenshot 02 |
| Run on the deployed demo with staff sign-in; source unchanged; screenshots and raw output | Unproven on the deployed demo; proven locally | Deploy not authorised; local hash unchanged. Needs deploy then rerun of the script |
| Walkthrough note | Proven | `issue-2008-web-xlsx-import-2026-11-22.md` |
