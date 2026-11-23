# Changes issue-223-live-r8 (2026-11-23)

Refs #223. Planned: src/core/src/zava_forward/core/ai_tasks.py (review_seconds), src/api/tests/test_ai_tasks.py (test), docs research note, index, log.

## Changes
* src/core/src/zava_forward/core/ai_tasks.py: `_elapsed_seconds`, `review_evidence.review_seconds`.
* src/api/tests/test_ai_tasks.py: `test_review_evidence_retains_elapsed_review_seconds`.
* docs/reference/research/issue-223-live-r8-2026-11-23.md, docs/reference/README.md, docs/reference/log.md.

## Validation (tier FULL by src change; targeted only, no rpi-checks --all)
api tests 94 OK; core 223 tests 6 OK; ruff clean; mypy 3 pre-existing errors, same without change. Hosted CI not observed.

## Per-criterion table
| Criterion | Status |
| --- | --- |
| Seeded critical defects detected and gate-blocked | Unproven beyond offline scripted panel (owner-only human panel) |
| Reviewer, source and reason retained | Proven (live r7; new time field unit-tested) |
| Detection, corrections, total effort reported on same scenarios | Unproven as measurement; capture added, aggregation not built |
| Default acceptance and citation validity cannot pass | Proven offline only |
| Automation-bias test; reviewer authority (OQ-017) | Test proven offline; authority unproven (owner-only) |
