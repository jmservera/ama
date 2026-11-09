<!-- markdownlint-disable-file -->
# Details: paired-equity anchor ID collision correction, 2026-11-08

Plan: [plan](../../plans/2026-11-08/paired-equity-id-collision-123-plan.md).

## Tests (test_paired_equity.py)

* Finding example: `ANCHORS + [case("p1")]` with `penalise_missing` and no seeded defects; expected after fix: status `blocked`, blocker `s1:invalid_comparison:anchor_id_collision`, `s1` in `invalid_pairs`, tested count for sensor dimension 0. Before the fix the expectation fails because the record passes the sensor pair.
* Same collision with the default `ranking.rank` is blocked.
* Missing case ID (both sides lack `id`) is a structured `missing_case_id` block, not a `KeyError`.
* Distinct-ID positive control: unchanged `pairs()` with `ANCHORS` still passes (existing test) and an extra distinct anchor `case("z4")` still passes.

## Source

* `_identity_problem(pair, anchors)` in `paired_equity.py`; called in `evaluate` after `_comparability` and before counting; shares the existing invalid-comparison reporting. Anchor IDs read with `.get("id")` so a malformed anchor cannot raise here.

## Checks

* Env: `PYTHONDONTWRITEBYTECODE=1`, external `XDG_CACHE_HOME` and `MYPY_CACHE_DIR` under `/tmp/c0811b`, `/tmp/ci764b-venv` (Ruff 0.17.1, mypy 2.4.0), explicit current-source `PYTHONPATH`, import-file assertion. Coupled selection as before (paired equity, journey, cohort, RAI release and invalidation, ranking publication and runner).
