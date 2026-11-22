# Changes, issue 2008 live

Tier: focused (no `src/` change). Refs #2008.

Changed: docs/reference/research/issue-2008-live-rerun-2026-11-22.md (new), docs/reference/research/demo-workbook/evidence-2026-11-22/ (preview output, live raw JSON, two screenshots, script), docs/reference/log.md, docs/reference/README.md.
Note: the evidence capture ran before this record was persisted; no source file was edited.
Validation: `python3 -m unittest tools/test_make_demo_case_list.py` OK (3 tests); live `/api/import-check` 200; source hashes unchanged; no `@` in raw output.

| Criterion | Result |
| --- | --- |
| Synthetic .xlsx in declared structure with generator | Proven |
| Clean rows, mapping differences and conflicts in row-level preview | Proven locally; deployed screen shows mapping and two rows to fix only |
| Deployed run with staff sign-in, source unchanged, screenshots and raw output | Partly proven: CSV only on the web; conflicts and .xlsx preview need the #80 web surface (src change, full tier) |
| Walkthrough note | Proven (2026-11-18 note, re-checked) |
