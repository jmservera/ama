---
title: Issue 2008 demo workbook import re-verification, 2026-11-22
description: Fresh local preview, generator test and deployed demo run for the synthetic case-list workbook, with a per-criterion table
ms.date: 2026-11-22
---

## Status and limits

Refs #2008 and #80 (deferred). Synthetic demo only, desktop 1440 x 900, within the owner authority of 2026-11-18. No `src/` file changed, so the focused tier applies. No Azure resource was created or changed. Credentials were read at runtime by the script and never printed; the raw output holds no identity string (checked for `@`). It repeats and extends the [2026-11-18 evidence](./issue-2008-demo-workbook-import-evidence-2026-11-18.md), which holds the walkthrough and the workbook description.

## Evidence

| File | Content |
| --- | --- |
| [local-cli-preview-raw-output.txt](demo-workbook/evidence-2026-11-22/local-cli-preview-raw-output.txt) | Row-level preview of [demo-case-list.xlsx](demo-workbook/demo-case-list.xlsx): six ready rows, four to fix, one duplicate-reference conflict |
| [live-import-check-raw-output.json](demo-workbook/evidence-2026-11-22/live-import-check-raw-output.json) | `/api/import-check` on `ca-cutover-test-demo-api` returned 200; SHA-256 of the CSV and `.xlsx` identical before and after |
| [01-import-page-before-upload.png](demo-workbook/evidence-2026-11-22/01-import-page-before-upload.png), [02-import-result-mapping-and-rows-to-fix.png](demo-workbook/evidence-2026-11-22/02-import-result-mapping-and-rows-to-fix.png) | Deployed screen before and after choosing the CSV |
| [live_import_check.py](demo-workbook/evidence-2026-11-22/live_import_check.py) | Playwright script |

The generator test `python3 -m unittest tools/test_make_demo_case_list.py` passed (3 tests): preview content, source unchanged, invented values only, committed copy equals generator output.

## Findings

* The deployed "Check a spreadsheet" screen still accepts CSV only (`accept=".csv,text/csv"` in `app.js`). It reported 8 rows ready, columns name, address, postcode matched and phone not found, and rows to fix 8 and 9. It does not test stage or duplicate references.
* The `.xlsx` row-level preview with conflicts exists only in the local command `python -m zava_forward.importer preview`.

## Per-criterion table

| Criterion | Result | Evidence or reason |
| --- | --- | --- |
| Synthetic `.xlsx` in the declared structure, no real personal data, with generator | Proven | Workbook read as `case-list`; generator and passing test; no `@` in any cell |
| Clean rows, mapping differences and conflicts shown by the row-level preview | Proven locally | Local preview output above. Not shown by the deployed screen |
| Run on the deployed demo with the staff sign-in shows mapping, conflicts and preview, source unchanged; screenshots and raw output kept | Partly proven | Run with the staff sign-in; mapping and two rows to fix shown; hashes unchanged; screenshots and raw output kept. Conflicts and the `.xlsx` row-level preview cannot be shown because the web surface accepts CSV only; a web `.xlsx` import is a `src/` change under #80 and takes the full tier |
| Demo walkthrough note says how to use it | Proven | Walkthrough section of the 2026-11-18 note, still accurate against the output above |
