<!-- markdownlint-disable-file -->
# Changes: #128 paired cohort comparability (2026-11-05)

Plan: [plan](../../plans/2026-11-05/issue-128-paired-cohort-comparability-plan.md).

## Files

* `src/core/src/zava_forward/core/paired_equity.py`: `CONTRASTS`, `_flatten`, `_same`, `_comparability`; `invalid_pairs` in the record; docstring updated.
* `src/core/tests/test_paired_equity.py`: regressions for confounded `days_in_stage`, no contrast, wrong dimension, unrelated nested change, partial support bundle, type-coerced and empty-mapping changes, and the supported support/adjustment bundle.
* `src/core/README.md`: existing paired_equity paragraph states fixture-local contrasts and `invalid_pairs`.

## Evidence

* Red (original source, new tests): 5 failures and 1 error. Original-source reproduction of the confound: pass, tested 3, failed 0, no blockers.
* Green after fix: `test_paired_equity.py` 15 tests OK.
* Divergence: the single Review found two Medium holes in the first implementation (type-insensitive equality, empty nested mapping dropped). Both were fixed in the same candidate with a regression test; the review was not repeated (one-pass rule), so those two fixes are verified by tests only, not re-reviewed.
* Stopped run: a full core `unittest discover` was started and stopped after more than 8 minutes with no result; it is not claimed. Affected tests were run instead.
* Environment: external venv `/tmp/rpi128-venv` (shared editable installs point at the primary checkout); external caches `/tmp/rpi128-ruff`, `/tmp/rpi128-mypy`.
