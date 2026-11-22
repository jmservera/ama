---
title: Issue 2008 deployed .xlsx import proof, 2026-11-22
description: The synthetic demo workbook chosen on the deployed demo with the staff test sign-in, showing mapping, conflicts and a row preview with the source unchanged
ms.date: 2026-11-22
---

## Status and limits

Refs #2008 and #80 (deferred). Synthetic demo only, desktop 1440 x 900. No source change, so the focused validation tier applies. No Azure resource was created or changed; the sign-in credentials were read at runtime by the script and are not printed or stored (the raw output was searched for `@` and `password`: no matches).

The earlier [local proof](./issue-2008-web-xlsx-import-2026-11-22.md) left one gap: the deployed demo ran an older build. Revision `ca-cutover-test-demo-api--0000053` of `ca-cutover-test-demo-api` now accepts `.xlsx` (the file input's `accept` attribute lists it) and `POST /api/import-check` returned 200.

## Evidence

| File | Content |
| --- | --- |
| [live_xlsx_import_check.py](demo-workbook/evidence-2026-11-22-live-xlsx/live_xlsx_import_check.py) | Playwright script: staff sign-in on the demo, open `#/import`, choose the workbook |
| [live-import-check-raw-output.json](demo-workbook/evidence-2026-11-22-live-xlsx/live-import-check-raw-output.json) | Raw API response (200), screen text, SHA-256 of the files before and after (`source_unchanged: true`) |
| [01-import-page-before-upload.png](demo-workbook/evidence-2026-11-22-live-xlsx/01-import-page-before-upload.png), [02-xlsx-mapping-conflicts-rows.png](demo-workbook/evidence-2026-11-22-live-xlsx/02-xlsx-mapping-conflicts-rows.png) | Screenshots |

What the deployed screen showed: sheet "Cases", 6 rows ready and 4 to fix; six columns matched (Ref, Property address, Post code, Workflow stage, Case owner by similar name, Status by name); `Resident name` and `Notes` unused; conflict `Duplicate reference DEMO-002 on rows 3 and 11`; 10 rows each with a "Ready" or "To fix: reason" word (address empty, postcode looks wrong, stage empty, duplicate reference).

## How to use it

1. Sign in to the demo with a staff account and choose "Check a spreadsheet" (`#/import`).
2. Choose [demo-case-list.xlsx](demo-workbook/demo-case-list.xlsx).
3. Read the mapping table, the conflicts list and the row table. The file is not changed.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| Synthetic `.xlsx` in the declared structure, no real personal data, with generator | Proven | Workbook and generator committed earlier (see the 2026-11-18 note); fictional addresses, `ZZ1` postcodes |
| Clean rows, mapping differences and conflicts shown by the row-level preview | Proven | Screenshot 02 and raw response |
| Run on the deployed demo with the staff sign-in shows mapping, conflicts and preview, source unchanged; screenshots and raw output kept | Proven | This note's evidence; `source_unchanged: true` |
| Demo walkthrough note says how to use it | Proven | Section above and the 2026-11-18 walkthrough |
