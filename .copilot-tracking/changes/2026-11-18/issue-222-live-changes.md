# Issue 222 live demo changes (2026-11-18)

Tier: FOCUSED (documentation only; no `src/` change, so no FULL tier). Refs #222.

## Files

* `docs/reference/research/cohort-evaluation-demo-2026-11-18.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)

## Validation

* `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests.test_cohort_ranking_eval tests.test_cohort_ai_eval tests.test_cohort_manifest_draft` from `src/agents`: 36 tests OK; seven blockers printed as expected.
* mypy, ruff, web and browser checks: not applicable (no source or web change). No Azure action taken; no throwaway resource; credentials files not read.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Paired cohorts against expected-outcome manifest | Proven (regression re-run); already ticked |
| Seeded defects detected | Proven (regression re-run); already ticked |
| Counts, errors, review burden, uncertainty reconcile | Proven (regression re-run); already ticked |
| Small or missing samples insufficient | Proven (six blockers observed); already ticked |
| Unapproved thresholds block activation | Proven (blocker observed); already ticked |
| Owner approval of cohorts, fields, thresholds before live use (OQ-018) | UNPROVEN, deferred to #1905 and #1906; requires named human approval the demo excludes |
