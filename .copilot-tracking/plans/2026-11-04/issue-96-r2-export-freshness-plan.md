<!-- markdownlint-disable-file -->
# Plan: issue-96-r2-export-freshness

* [x] Phase 1: add `export_freshness` to `src/core/src/zava_forward/core/form_export.py`.
* [x] Phase 2: add behavioural tests in `src/core/tests/test_form_export.py` (JSON and SQL stores).
* [x] Phase 3: README note and knowledge-base log entry.
* [x] Phase 4: focused validation (ruff, mypy, unittest).

Details: [details](../../details/2026-11-04/issue-96-r2-export-freshness-details.md). Critique: [critique](../../reviews/plans/2026-11-04/issue-96-r2-export-freshness-critique.md).
Later slices: approved-rule validation and reviewed pack export (blocked on Finance/template authority); rule and approval stale propagation; API exposure.
