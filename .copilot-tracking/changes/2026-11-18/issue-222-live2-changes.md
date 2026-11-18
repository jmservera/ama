# Issue 222 live2 changes (2026-11-18)

Tier: FOCUSED (documentation and retained evidence only; no `src/` change). Refs #222. Existing `issue-222-live-state.json` left untouched.

## Files

* `docs/reference/research/cohort-evaluation-live-2026-11-18.md` (new)
* `docs/reference/research/evaluation/cohort-eval-live-2026-11-18/` (raw outputs, probe script, shape JSON)
* `docs/reference/README.md`, `docs/reference/log.md`

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Paired cohorts against expected-outcome manifest | Proven (36 tests, raw retained); already ticked |
| Seeded defects detected | Proven (ranking 4 of 4, AI 3 of 3); already ticked |
| Counts, errors, review burden, uncertainty reconcile | Proven on fixture; already ticked |
| Small or missing samples insufficient | Proven (eight blockers); already ticked |
| Unapproved thresholds block activation | Proven (`activation allowed False`); already ticked |
| Owner approval of cohorts, fields, thresholds before live use (OQ-018) | UNPROVEN: needs named human approval and DPO/Legal (#1905, #1906), excluded for the demo; synthetic results are not fairness evidence |

## Validation

* 36 cohort tests from `src/agents`: OK. Live probe read-only; no Azure resource created; credentials not printed. mypy and web checks not applicable (no src or web change). Probe script is evidence under docs, not a src-ci target (isolated ruff strict rules would flag its style; format check passes).
* Prior note's seven-blocker count corrected to eight plus one.
