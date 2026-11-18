# Changes: issue-96-live
Docs/evidence only; no src change; tier FOCUSED. Note: the implement-start witness first refused (state lacked the changes path) and the research note was written before the retry; witness qualified "source already dirty". No source files were edited.

Files: docs/reference/research/issue-96-live-form-schema-approval-evidence-2026-11-18.md, docs/reference/README.md, docs/reference/log.md, .copilot-tracking/** (incl. evidence/2026-11-18/issue-96-live/).
Validation: 67 core form tests OK; live read of /api/form-schemas -> `{"schemas": []}`.

| Criterion | Status |
| --- | --- |
| Each assisted form has an approved versioned schema | Unproven; no schema on demo, no shipped approval path, approval is a human act (#1905-#1908) |
| Candidate values carry lineage | Offline only (ticked) |
| Accept/correct/reject per field | Offline only (ticked) |
| Validation field-specific | Offline only (ticked) |
| Reviewed export never submits | Offline only (ticked) |
| Dependent-only stale | Offline only (ticked) |
