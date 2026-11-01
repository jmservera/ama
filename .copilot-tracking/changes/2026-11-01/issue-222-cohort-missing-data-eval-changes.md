---
title: Issue 222 cohort and missing-data evaluation changes
ms.date: 2026-11-01
---

## Changes

* Added `src/core/src/zava_forward/core/cohort_eval.py`.
* Added `src/core/tests/cohort_eval_fixture.py` and `src/core/tests/test_cohort_eval.py` (19 tests after review corrections).

## Validation (focused tier, from `src/core`)

* `PYTHONPATH=src:tests python3 -m unittest test_cohort_eval test_dependency_rule`: OK.
* `ruff check`, `ruff format --check`, `mypy`: clean.
* Heavy local gate not run; CI is the evidence.

## Divergences

None.

## Review-thread corrections (PR 636)

* Thresholds now require a positive non-boolean integer `min_sample` and finite rate/gap limits in [0, 1].
* Missing observations are tracked per cohort (`missing`) and excluded from `n`, sufficiency and the Wilson interval.
* Duplicate IDs in manifest or observations, and missing or unsupported outcomes, raise non-disposable `invalid_input` blockers.
* Empty cohort declarations, labels or cases raise a non-disposable `insufficient_sample` blocker.
* Error-rate and gap threshold comparisons use unrounded rates; rounding applies only to reported values.
* A valid human `reject` adds a non-disposable `rejected` blocker.
* The hashed record includes `input_digests` for the manifest and observations.
* Second round: expected outcomes are validated against `OUTCOMES`, and missing `task_id` or `subject_version` raises non-disposable `invalid_input` blockers.
* `fairness_evidence` is false when invalid-input, reconciliation or insufficient-sample blockers exist, so an unmeasured non-synthetic run is not fairness evidence.
* Duplicate-ID detection uses a single `Counter` pass instead of `list.count` (linear, not quadratic).
* Tests: 21 in `test_cohort_eval.py` (10 added); `ruff check` and `ruff format --check` clean.
* CI `rubric/score` failed with "Scoring failed" in the hosted scorer; to be re-run, not a code failure.
* Third round: case IDs in the manifest and observations must be non-empty strings (malformed IDs raise non-disposable `invalid_input` and never join), `missing_data_treatment` is required, and only a literal `synthetic: false` is non-synthetic.
* Tests: 23 in `test_cohort_eval.py`; `ruff check` and `ruff format --check` clean. `gh pr checks 636` showed only `rubric/score`, passing.
