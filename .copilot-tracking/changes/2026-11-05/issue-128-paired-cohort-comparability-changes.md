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

## Correction 2 (2026-11-05, appended; original above unchanged)

* Research: the coordinator reproduced two further bypasses on head c837e6bc (both pass, tested 3, invalid_pairs empty, blockers empty): (1) resident.extra [1] vs [True], because `_same` compared only the outer list type; (2) resident `{"extra": {"x": 1}, "extra.x": 1}` vs `{"extra": {"x": 2}, "extra.x": 1}`, because dotted-string flattening let a literal key shadow a nested leaf.
* Plan: tuple-path flattening for unambiguous identities; type-aware deep `_same` for mappings and sequences; contrast paths split into tuples. No change to supported contrasts, ranker, accounting or gates.
* Implement: `_flatten`, `_same`, `_comparability` in `paired_equity.py`; two regressions in `test_paired_equity.py` for the exact probes.
* Evidence: red on the old source gave 2 failures (the new tests); green gave 17 paired_equity tests OK; journey_register 7, rai_release 6, rai_release_invalidation 6, ranking_publication 13 and cohort_eval 25 OK; Ruff check, format and mypy (266 files) clean. Loaded module: `/home/azureuser/source/ama-wt/issue-128-comparability/src/core/src/zava_forward/core/paired_equity.py` via external venv `/tmp/rpi128-venv`. No full core discovery; the earlier stopped broad run remains not claimed.
