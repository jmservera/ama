# Plan: #222 cohort ranking evaluation run

* Task: issue-222-cohort-ranking-run. Research: `.copilot-tracking/research/2026-11-01-issue-222-cohort-ranking-run-research.md`.
* Phase 1: add `src/agents/src/zava_forward/agents/cohort_ranking_eval.py` (manifest builder, ranker adapter, seeded defects, `main` with `--json`).
* Phase 2: add `src/agents/tests/test_cohort_ranking_eval.py` (clean run, seeded defects detected, per-cohort reconciliation, small sample stays insufficient, unapproved thresholds block, exceedance not averaged, synthetic never fairness evidence).
* Phase 3: document in `src/agents/README.md`; run unittest, ruff check, ruff format --check, mypy for `src/agents`.
* Critique (single pass, direct): the expected-rank oracle must be stated independently of the ranker, so ranks come from an explicit unit order with unique day counts, not from calling `rank`. Ranking and core stay unchanged. No approval is inferred; manifest approval is left empty by default.
* Out of scope: owner approval, live thresholds, real cohorts, AI task cohorts, API wiring.
