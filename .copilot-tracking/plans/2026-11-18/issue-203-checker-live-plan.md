# Plan: issue-203-checker-live

Research: ../../research/2026-11-18/issue-203-checker-live-research.md. Details: ../../details/2026-11-18/issue-203-checker-live-details.md. Tier: FOCUSED.

* [x] Phase 1: add the three regression-test files to `GUARD_FILES` and a `RECORD_PATTERNS` regex for dated live-evidence research notes in `tools/check-legacy-references.py`; `is_exempt` honours both.
* [x] Phase 2: add unit tests for the regex (dated note and evidence folder exempt; undated research note and docs page still flagged).
* [x] Phase 3: run the checker, unit tests, ruff; record the per-criterion table, a research note, index row and log entry.
