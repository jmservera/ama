<!-- markdownlint-disable-file -->
# Plan: issue-96-r1-held-export

* [x] Phase 1: add `src/core/src/zava_forward/core/form_export.py` (read-only, reuses `form_review._report`).
* [x] Phase 2: add `src/core/tests/test_form_export.py` (JSON and SQL stores).
* [x] Phase 3: README boundary note and log entry.
* [x] Phase 4: focused validation (ruff, mypy, unittest).

Details: [details](../../details/2026-11-03/issue-96-r1-held-export-details.md). Critique: [critique](../../reviews/plans/2026-11-03/issue-96-r1-held-export-critique.md).
Later slices: S2 approved-rule validation and S3 reviewed pack export (blocked on Finance/template authority), S4 rule/calculation/approval stale propagation.
