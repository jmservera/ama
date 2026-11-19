---
title: Issue 2008 synthetic demo workbook for the import, walkthrough and live evidence, 2026-11-18
description: Synthetic case-list workbook with its generator, the local row-level preview, a run on the deployed demo with the staff test sign-in, and a per-criterion table
ms.date: 2026-11-18
---

## Status and limits

Refs #2008 and #80 (deferred). Synthetic demo only, desktop (1440 x 900), within the owner authority of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). The sign-in credentials were read at runtime by the script and never written to any output. No `src/` file changed, so the focused tier applies. No Azure resource was created or changed; the run used the existing demo app `ca-cutover-test-demo-api` (host redacted below as the demo API host).

One finding shapes everything else. The deployed demo cannot read an `.xlsx`. Its "Check a spreadsheet" screen accepts CSV only (`importView` in `src/api/src/zava_forward/api/web/app.js`) and posts the text to `/api/import-check` (`Store.import_check`), which maps name, address, postcode and phone columns and lists rows to fix. The `.xlsx` library with the declared `case-list` structure, alias mapping, duplicate-key conflicts and row-level preview (#80) is reachable only through the local command `python -m zava_forward.importer preview FILE`; the importer README lists the web surface as not built. The walkthrough therefore uses both.

## Files

| File | Purpose |
| --- | --- |
| [make-demo-case-list.py](../../../tools/make-demo-case-list.py) | Generator (standard library plus `zava_forward.importer.xlsx.write_workbook`) |
| [test_make_demo_case_list.py](../../../tools/test_make_demo_case_list.py) | Focused tests: preview content, source unchanged, invented values only, committed copy matches generator |
| [demo-case-list.xlsx](demo-workbook/demo-case-list.xlsx) | The synthetic workbook, sheets `Cases` and `About this demo` |
| [demo-case-list.csv](demo-workbook/demo-case-list.csv) | The `Cases` sheet saved as CSV, for the deployed screen |
| [local-cli-preview-raw-output.txt](demo-workbook/evidence-2026-11-18/local-cli-preview-raw-output.txt) | Raw output of the local row-level preview (the command exits 1 because the file has a blocking conflict) |
| [live-import-check-raw-output.json](demo-workbook/evidence-2026-11-18/live-import-check-raw-output.json) | Raw `/api/import-check` response captured from the deployed demo, with file hashes before and after |
| [01-import-page-before-upload.png](demo-workbook/evidence-2026-11-18/01-import-page-before-upload.png) | Deployed screen before a file is chosen |
| [02-import-result-mapping-and-rows-to-fix.png](demo-workbook/evidence-2026-11-18/02-import-result-mapping-and-rows-to-fix.png) | Deployed screen after choosing the CSV: mapping and rows to fix |
| [live_import_check.py](demo-workbook/evidence-2026-11-18/live_import_check.py) | The Playwright script used (reads credentials from the owner's home files at runtime) |

## What the workbook contains

All values are invented: fictional street names, `Demo Resident NN` labels, reserved-style `ZZ` postcodes, no phone numbers, no email addresses. The `Cases` headers differ from the declared names on purpose.

| Rows | Content | What the preview shows |
| --- | --- | --- |
| 2 to 7 | Complete rows | Ready |
| 8 | Empty address | Row to fix |
| 9 | Postcode `ZZ-18` | Row to fix |
| 10 | Empty stage | Row to fix |
| 11 | Repeats reference `DEMO-002` from row 3 | Row to fix and a blocking conflict |
| Headers | `Ref`, `Property address`, `Post code`, `Workflow stage`, `Case owner` | Alias mapping; `Status` maps exactly; `Resident name` and `Notes` are unmapped |

## Walkthrough: how to use it

1. Regenerate if wanted: `pip install -e src/core -e src/importer`, then `python3 tools/make-demo-case-list.py` from the repository root.
2. Local row-level preview: `python -m zava_forward.importer preview docs/reference/research/demo-workbook/demo-case-list.xlsx`. It prints the source hash, the column mapping, the conflict and each row with lineage-ready row numbers. The source is read once and never written.
3. Deployed demo: sign in with a staff account, choose "Check a spreadsheet" (`#/import`), choose `demo-case-list.csv`. The screen shows the column mapping and the rows to fix, and states that the file has not been changed.
4. Compare: the local preview shows ten rows classified with a named reason each and the duplicate-reference conflict; the deployed screen shows only the two rows its simpler check flags.

## Recorded results

Local preview (raw file linked above): six ready rows, four to fix (rows 8, 9, 10, 11), mapping with five alias matches and one exact match, and `CONFLICT: Duplicate reference DEMO-002 on rows 3 and 11`.

Deployed demo, same session as the screenshots: the endpoint answered 200 and the UI reported 8 rows ready, 0 matched to a home already on record, columns `name: Resident name`, `address: Property address`, `postcode: Post code`, `phone: not found`, and rows to fix `Row 8: Check address` and `Row 9: Check postcode looks wrong`. The SHA-256 of both the CSV and the `.xlsx` was identical before and after (`source_unchanged: true` in the raw file). Rows 10 and 11 are not flagged on the deployed screen because its check does not test stage or duplicate references; that difference is the gap between the web check and #80.

Not retained: the Entra sign-in pages (they carry the account name), the final landing page with the account initials beyond the cropped screenshots, and any run on a different account. The resident test account was not used; the import is an employee screen.

Credential handling: one earlier diagnostic shell command in this session displayed the content of the demo test password file in the terminal output before the live script was written (a mistaken `sed` on a file that had no key separator). No file or evidence copy holds it. The owner may wish to rotate that demo test password; rotation is outside this task's authority.

## Per-criterion table

| Criterion | Result | Evidence or reason |
| --- | --- | --- |
| Synthetic `.xlsx` in the declared structure, no real personal data, committed with generator | Proven | `demo-case-list.xlsx` read by `preview_file` as structure `case-list`, sheet `Cases`; generator and tests above; `test_only_invented_values` finds no `@` in any cell; values are invented |
| Clean rows, mapping differences and deliberate conflicts so the row-level preview shows each | Proven locally; partly proven on the deployed demo | Local preview shows all three. The deployed screen shows mapping and two row problems only, with no duplicate-reference conflict and no stage check, because the web check does not implement them |
| Import run on the deployed demo with the staff test sign-in shows mapping, conflicts and preview and never changes the source file; screenshots and raw output retained | Partly proven | Run done with the staff test sign-in; mapping and rows to fix shown; hashes unchanged; screenshots and raw output retained. Conflicts and the row-level preview are not shown on the deployed demo and an `.xlsx` cannot be uploaded there. Closing this needs the web import surface of #80, a `src/` change that takes the full tier and is out of scope here |
| Demo walkthrough note says how to use it | Proven | The walkthrough section above |
