---
title: Issue 80 round 3 changes
description: Changes made
ms.date: 2026-11-05
---

Changed: `quality.checklist_rows`, the staff projection, the export route registry, the quality checklist form link, five test files and the API README. No divergences from the plan. No new dependency, no `.xlsx`, no audit write (matches existing exports).

## Validation (focused tier, before the full gate)

Run with `PYTHONPATH` pointing at this worktree's `src/*` trees, because the editable installs resolve to the main checkout.

* `test_list_export_api`, `test_role_endpoint_inventory`, `test_loading_feedback`, `test_role_matrix` (api): 50 OK. With the api source change removed, `test_list_export_api` fails 3 tests (registry, checklist rows, denial), so the new tests fail without the export.
* core `test_list_export` and `test_quality_procurement`: 114 OK.
* `ruff check` and `ruff format --check` on api and core: clean. `mypy` (tests included, as CI runs it) on api and core: clean.
* `node --check web/ops.js`: OK.
* Targeted real-server browser check (synthetic data, Chromium): link visible, `href=/api/checklists.csv`, keyboard focusable, download is the CSV with header `measure,version,step,check`, no horizontal overflow at 320 px, no page errors.
* Web review of `src/api/src/zava_forward/api/web/ops.js` against the fetched web-interface-guidelines source: `ops.js:114` pass (native link, visible label, no motion). The Title Case copy rule is not applied; the repository plain-language wording "Download for Excel" is kept as in the other export links.
* Existing `case_journey_browser_check` fails at "320x800 summary within one viewport scroll (1676.40625)" both with and without this change, so it is a pre-existing local result, not caused by this slice; it stays a full-gate item.

## Not run

FULL local gate: not admitted. The shared heavy lane is held by the #188 gate (pid 1148896); see the state file for the admission attempt. Hosted CI, independent exact-head review and coordinator publication are pending.
