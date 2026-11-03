# Details: redress access under holds test (Refs #86, R1)

Phase 1: `test_complaint_and_independent_review_stay_open_under_every_hold` in src/core/tests/test_resident_decisions.py (runs for JSON and SQLite stores). Asserts the gates hold (disclosure and works release) while both routes open and the Withdrawn decision is unchanged.
Phase 2: unittest of the file, ruff check and format, mypy with --cache-dir=/tmp/mypy-86.
