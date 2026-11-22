---
title: Issue 2008 web .xlsx import preview, 2026-11-22
description: The Check a spreadsheet screen now previews the synthetic .xlsx with mapping, conflicts and a row preview; local proof, limits and a per-criterion table
ms.date: 2026-11-22
---

## Status and limits

Refs #2008 and #80 (deferred). Synthetic demo only, desktop 1440 x 900. This change was built and proven locally. It was not deployed (deployment was outside this task), so the deployed demo still shows the earlier CSV-only screen recorded in [the 2026-11-18 evidence](./issue-2008-demo-workbook-import-evidence-2026-11-18.md). No Azure resource was created or changed and no sign-in credential file was read.

Tier: this changes `src/` code, so the full tier applies. Only targeted checks were run here; the complete gate and hosted CI are for the coordinator and the pull request.

## What changed

* `xlsx.py` and `mapping.py` moved from `src/importer` to `src/core` as `zava_forward.core.xlsx` and `zava_forward.core.import_preview`, unchanged except imports. The importer, its tests and `tools/make-demo-case-list.py` import them from core. This keeps the api dependency rule (api may import only api, core and agents) and the API image (core, agents, api wheels) as they were, and adds no dependency (the reader is standard library).
* `Store.import_check_workbook` returns mapping, conflicts, matched-home count and up to 200 rows. `POST /api/import-check` accepts `{"name", "xlsx_base64"}` next to `{"text"}`; bad base64 or an unreadable workbook returns 400 with a plain sentence.
* `importView` in `app.js` accepts `.csv` and `.xlsx`, and shows a column-mapping table, a conflicts list and a row-by-row table with a "Ready" or "To fix: reason" word per row (not colour alone). Both tables have captions and column headers.

## Evidence

| File | Content |
| --- | --- |
| [local_xlsx_import_proof.py](demo-workbook/evidence-2026-11-22-local/local_xlsx_import_proof.py) | Playwright script: local server on the synthetic test dataset, synthetic staff sign-in, choose the workbook |
| [raw-import-check-response.json](demo-workbook/evidence-2026-11-22-local/raw-import-check-response.json) | Raw response, `accept` attribute and SHA-256 of the workbook before and after (`source_unchanged: true`) |
| [rendered-text.txt](demo-workbook/evidence-2026-11-22-local/rendered-text.txt) | Text the screen shows: 6 ready, 4 to fix, `Duplicate reference DEMO-002 on rows 3 and 11`, mapping with `Resident name` and `Notes` unused |
| [01-before-choosing-a-file.png](demo-workbook/evidence-2026-11-22-local/01-before-choosing-a-file.png), [02-xlsx-mapping-conflicts-rows.png](demo-workbook/evidence-2026-11-22-local/02-xlsx-mapping-conflicts-rows.png) | Screenshots |

Checks run (targeted): importer suite 125 tests OK; core suite run once (4159 tests): the only failure touching this change was a Fabric note link to the moved `xlsx.py`, fixed and rechecked with `test_live_doc_links`; the other 57 failures and errors are Azure IoT SDK-missing and installed-package-path cases in this environment, in files this change does not touch (not rerun on `main` here); api `test_mvp`, `test_accessibility_baseline`, `test_content_standard`, `test_polish_ux`, `test_epic149_role_workbench_heading_hierarchy`, `test_dependency_rule`, `test_list_export_inventory`, `test_role_matrix` and `test_role_endpoint_inventory` OK; `tools/test_make_demo_case_list.py` 3 tests OK; mypy clean in api and importer, core unchanged at its 3 existing errors; ruff clean. The table-count check in `test_accessibility_baseline.py` rose from 15 to 17 for the two new captioned tables.

## How to use it

1. Sign in with a staff account and choose "Check a spreadsheet" (`#/import`).
2. Choose [demo-case-list.xlsx](demo-workbook/demo-case-list.xlsx) (or the CSV copy, which keeps the simpler check).
3. Read the mapping table, the conflicts list and the row-by-row table. Your file is not changed.

## Per-criterion table

| Criterion | Result | Evidence or reason |
| --- | --- | --- |
| Synthetic `.xlsx` in the declared structure, no real personal data, with generator | Proven | Unchanged workbook, generator and passing test; read as `case-list` |
| Clean rows, mapping differences and conflicts shown by the row-level preview | Proven, now on the web screen locally | Screenshot 02 and rendered text: clean, mapped by alias, duplicate-reference conflict |
| Run on the deployed demo with the staff sign-in shows mapping, conflicts and preview, source unchanged; screenshots and raw output kept | Proven locally; not proven on the deployed demo | The screen and source-unchanged hash are proven on a local server. The deployed app still runs the older build; deploying was not authorised here. Needs a deploy of the commit, then a rerun of the Playwright script against the demo with the staff sign-in |
| Demo walkthrough note says how to use it | Proven | Section above and the 2026-11-18 walkthrough |
