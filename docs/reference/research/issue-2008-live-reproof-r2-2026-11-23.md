---
title: Issue 2008 live re-proof on API revision 0000054, run r2, 2026-11-23
description: Fresh Playwright proof of the synthetic Excel import demo and per-criterion table
ms.date: 2026-11-23
---

## Status and limits

Refs #2008 and #80 (deferred). Synthetic demo only, desktop 1440 x 900. No source change, so the focused tier applies. No Azure resource was created or changed. Credentials were read at runtime; the raw output has no `@` characters.

The Azure CLI on 2026-11-23 showed `ca-cutover-test-demo-api--0000054` (100% traffic, Healthy) and `ca-resident-demo--0000026` (100% traffic), the same revisions as the [earlier close-out](./issue-2008-closeout-live-2026-11-23.md). No code or data gap was found, so none was fixed.

## Evidence

| File | Content |
| --- | --- |
| [live-import-check-raw-output.json](demo-workbook/evidence-2026-11-23-live-r2/live-import-check-raw-output.json) | `POST /api/import-check` 200, screen text, file hashes before and after (`source_unchanged: true`) |
| [01-import-page-before-upload.png](demo-workbook/evidence-2026-11-23-live-r2/01-import-page-before-upload.png), [02-xlsx-mapping-conflicts-rows.png](demo-workbook/evidence-2026-11-23-live-r2/02-xlsx-mapping-conflicts-rows.png) | Screenshots |

The script is the one in [evidence-2026-11-23-live](demo-workbook/evidence-2026-11-23-live/live_xlsx_import_check.py), run with the worktree and output paths changed. The screen showed the conflict `Duplicate reference DEMO-002 on rows 3 and 11`. The workbook's SHA-256 was identical before and after.

## How to use it

Sign in with a staff account, open "Check a spreadsheet" (`#/import`), choose [demo-case-list.xlsx](demo-workbook/demo-case-list.xlsx), and read the mapping, conflicts and row table. The file is not changed. The generator and full walkthrough are in the [2026-11-18 note](./issue-2008-demo-workbook-import-evidence-2026-11-18.md).

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| Synthetic `.xlsx` in declared structure, no real personal data, committed with generator | Proven | Committed workbook and generator (2026-11-18 note) |
| Clean rows, mapping differences and deliberate conflicts shown by the row preview | Proven | Screenshot 02 and raw response, revision 0000054 |
| Run on the deployed demo with staff sign-in; source unchanged; screenshots and raw output kept | Proven | This note's evidence, `source_unchanged: true` |
| Walkthrough note says how to use it | Proven | Section above and the 2026-11-18 note |

Owner-gated: none for the demo. Unproven: none.
