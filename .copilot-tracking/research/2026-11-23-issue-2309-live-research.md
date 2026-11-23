# Research: issue #2309 seeded critical-defect gate harness

Disposition: executed. Planning Readiness: Ready.

## Finding

The harness the issue asks for already exists from #223 work:
`src/core/src/zava_forward/core/human_review_effectiveness.py` (gate
`human_review_gate`, `evaluate_panel`, `run_automation_bias_harness`) and
`src/core/tests/test_human_review_effectiveness_223.py` (6 tests). Four defect
classes (wrong, stale, unsupported, incomplete) plus a control are seeded in 8
workflow-only synthetic scenarios, each with resolving citations.

## Evidence (run 2026-11-23, `src/core`, `PYTHONPATH=src:tests python3 -m unittest -v tests.test_human_review_effectiveness_223`)

Ran 6 tests, OK. Panel summary from `run_automation_bias_harness()`
(panel, detection rate, gate passed, gate leakage):

* competent 1.0, 8, 0
* default_accept 0.0, 0, 0
* automation_bias 0.1667, 2, 0
* citation_only 0.0, 0, 0
* unauthorised_competent 1.0, 0, 0

## Criteria

See the per-criterion table in the changes record. All five are proven by
existing tests; none needs a live Azure call (core library, synthetic data only).

## Decision

No source change is needed. Deliver research, plan, critique, changes and review
artifacts plus a research note under `docs/reference/research/`.
