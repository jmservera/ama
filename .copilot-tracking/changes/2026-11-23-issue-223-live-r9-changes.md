# Changes issue-223-live-r9 (2026-11-23)

Refs #223.

## Changes
* src/core/src/zava_forward/core/ai_tasks.py: `live_report()` returns `review_effort` per task.
* src/api/tests/test_ai_tasks.py: `test_live_report_aggregates_review_effort`.
* docs/reference/research/issue-223-live-r9-2026-11-23.md, docs/reference/README.md, docs/reference/log.md.

## Validation (tier FULL by src change; targeted only, no rpi-checks --all)
api tests.test_ai_tasks 87 OK; core 218/100/223 tests 14 OK; ruff clean; mypy 3 pre-existing errors. Hosted CI not observed.

## Per-criterion table
| Criterion | Status |
| --- | --- |
| Seeded critical defects detected and gate-blocked | Unproven beyond offline scripted panel (owner-only human panel) |
| Reviewer, source and reason retained | Proven (live r7) |
| Detection, corrections, total effort reported on same scenarios | Unproven as a comparison; live effort aggregation added (unit-tested) |
| Default acceptance and citation validity cannot pass | Proven offline only |
| Automation-bias test; reviewer authority (OQ-017) | Test proven offline; authority unproven (owner-only) |
