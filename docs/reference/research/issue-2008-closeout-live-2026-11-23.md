---
title: Issue 2008 close-out on the latest live revision, 2026-11-23
description: Per-criterion close-out of the synthetic Excel import demo, re-proved on API revision 0000054
ms.date: 2026-11-23
---

## Status and limits

Refs #2008 and #80 (deferred). Synthetic demo only, desktop 1440 x 900. No source change, so the focused tier applies. No Azure resource was created or changed. Sign-in credentials were read at runtime by the script; the raw output has no `@`, `password` or identity strings.

Revisions checked with the Azure CLI on 2026-11-23: `ca-cutover-test-demo-api--0000054` (100% traffic, Healthy) and `ca-resident-demo--0000026` (100% traffic). The earlier [deployed proof](./issue-2008-live-xlsx-deployed-2026-11-22.md) ran on 0000053. The code on main needed no change: the workbook, generator, `.xlsx` preview and walkthrough were already merged.

## Evidence

| File | Content |
| --- | --- |
| [live_xlsx_import_check.py](demo-workbook/evidence-2026-11-23-live/live_xlsx_import_check.py) | Playwright script: staff sign-in, open `#/import`, choose the workbook |
| [live-import-check-raw-output.json](demo-workbook/evidence-2026-11-23-live/live-import-check-raw-output.json) | Raw API response (200), screen text, file hashes before and after (`source_unchanged: true`) |
| [01-import-page-before-upload.png](demo-workbook/evidence-2026-11-23-live/01-import-page-before-upload.png), [02-xlsx-mapping-conflicts-rows.png](demo-workbook/evidence-2026-11-23-live/02-xlsx-mapping-conflicts-rows.png) | Screenshots |

On revision 0000054 the screen showed sheet "Cases" with 6 rows ready and 4 to fix, six matched columns (Reference, Address, Postcode, Stage, Status, Owner), `Resident name` and `Notes` unused, the conflict `Duplicate reference DEMO-002 on rows 3 and 11`, and a row table with a Ready or To fix verdict for every row. `POST /api/import-check` returned 200 and the SHA-256 of the CSV and `.xlsx` was identical before and after.

## How to use it

1. Sign in to the demo with a staff account and open "Check a spreadsheet" (`#/import`).
2. Choose [demo-case-list.xlsx](demo-workbook/demo-case-list.xlsx) (or the CSV beside it).
3. Read the mapping table, the conflicts list and the row table. The file is not changed.

The generator and the full walkthrough are in the [2026-11-18 note](./issue-2008-demo-workbook-import-evidence-2026-11-18.md).

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| Synthetic `.xlsx` in the declared structure, no real personal data, committed with generator | Proven | Committed workbook and generator; fictional addresses and `ZZ1` postcodes |
| Clean rows, mapping differences and deliberate conflicts shown by the row preview | Proven | Screenshot 02 and raw response on 0000054 |
| Run on the deployed demo with staff sign-in shows mapping, conflicts and preview; source unchanged; screenshots and raw output kept | Proven | This note's evidence; `source_unchanged: true` |
| Walkthrough note says how to use it | Proven | Section above and the 2026-11-18 note |

Owner-gated: none for the demo. Unproven: none.
