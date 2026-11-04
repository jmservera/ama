---
title: Issue 130 nomination human review changes
ms.date: 2026-11-04
---

## Changes

* `src/core/src/zava_forward/core/resident_decisions.py`: `nomination_review` action, stale marking on correction, `review_current` in the follow-up view.
* `src/core/tests/test_resident_decisions.py`: `test_nomination_review_retains_reviewer_and_correction_stales_it`.
* `src/core/README.md`, `src/api/README.md`: action documented.

## Validation run

* `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions.JsonResidentDecisions` (67 tests, OK).
* `ruff check .` and `ruff format --check .` in `src/core`: clean.
* `mypy --cache-dir=/tmp/mypy-130` in `src/core` as CI runs it (tests included): no issues in 253 files.

## Not run

* Local gate, full suites, benchmarks, SQL-backed variants (no SQL prerequisites run), API and browser tests.
* No API or UI route test was added; the generic API action path is unchanged.

## Acceptance criteria

* Newly advanced, not fully proven: C3 (reviewer and outcome retained; no actual resident/representative challenge participation), C4 and C11 (nomination review staleness only; no wider dependent-decision graph).
* Unmet: C2 (delivery unverified), C5 (no automatic hazard routing), C8, C9, C10 (no UI/keyboard route), C14.
* Uses Refs #130.
