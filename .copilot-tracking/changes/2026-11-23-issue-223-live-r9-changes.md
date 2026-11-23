# Changes issue-223-live-r9 (2026-11-23)

Refs #223.

## Changes
* src/core/src/zava_forward/core/ai_tasks.py: `live_report()` returns `review_effort` per task.
* src/api/tests/test_ai_tasks.py: `test_live_report_aggregates_review_effort`.
* docs/reference/research/issue-223-live-r9-2026-11-23.md, docs/reference/README.md, docs/reference/log.md.

## Validation (tier FULL by src change; targeted only, no rpi-checks --all)
api tests.test_ai_tasks 87 OK; core 218/100/223 tests 14 OK; ruff clean; mypy 3 pre-existing errors. Hosted CI not observed.
Refs #223. Planned: src/core/src/zava_forward/core/ai_tasks.py (`review_effort` in `live_report`), src/api/tests/test_ai_tasks.py (regression test), docs research note, index, log.

## Changes
* `live_report` adds `review_effort` (per task: timed_reviews, total_seconds, mean_seconds).
* src/api/tests/test_ai_tasks.py: `test_live_report_totals_measured_review_effort` (JSON and SQL stores).
* Added the research note, index row and log entry.

## Validation (tier FULL by src change; targeted only, no rpi-checks --all)
api test_ai_tasks 87 OK; core 12 related tests OK; ruff check clean; mypy 3 pre-existing errors. Hosted CI not observed. Not deployed (no production change). The implement-start witness noted source edits landed concurrently with the call.

## Per-criterion table
| Criterion | Status |
| --- | --- |
| Seeded critical defects detected and gate-blocked | Unproven beyond offline scripted panel (owner-only human panel) |
| Reviewer, source and reason retained | Proven (live r7) |
| Detection, corrections, total effort reported on same scenarios | Unproven as a comparison; live effort aggregation added (unit-tested) |
| Reviewer, source and reason retained | Proven live (run 7) |
| Detection, corrections, total effort reported on same scenarios | Unproven as measurement; measured per-task total now in live report (unit-tested, not deployed) |
| Default acceptance and citation validity cannot pass | Proven offline only |
| Automation-bias test; reviewer authority (OQ-017) | Test proven offline; authority unproven (owner-only) |
