# Changes: issue 2008 deployed xlsx proof
Added: research note issue-2008-live-xlsx-deployed-2026-11-22.md, evidence dir demo-workbook/evidence-2026-11-22-live-xlsx/, index and log entries. No source change (focused tier). Hosted CI not observed locally; no push.

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1 Synthetic xlsx with generator, no real personal data | Proven | demo-workbook/demo-case-list.xlsx, earlier 2026-11-18 note |
| 2 Clean rows, mapping differences, conflicts in row preview | Proven | screenshot 02, raw JSON (6 ready, 4 to fix, duplicate DEMO-002) |
| 3 Deployed demo run with staff sign-in, source unchanged, evidence kept | Proven | live-import-check-raw-output.json (200, source_unchanged true), screenshots |
| 4 Walkthrough note | Proven | research note "How to use it" |
