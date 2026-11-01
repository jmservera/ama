# Plan: #222 cohort ranking evaluation run

* Task: issue-222-cohort-ranking-run. Research: `.copilot-tracking/research/2026-11-01-issue-222-cohort-ranking-run-research.md`.
* Phase 1: add `src/agents/src/zava_forward/agents/cohort_ranking_eval.py` (manifest builder, ranker adapter, seeded defects, `main` with `--json`).
* Phase 2: add `src/agents/tests/test_cohort_ranking_eval.py` (clean run, seeded defects detected, per-cohort reconciliation, small sample stays insufficient, unapproved thresholds block, exceedance not averaged, synthetic never fairness evidence).
* Phase 3: document in `src/agents/README.md`; run unittest, ruff check, ruff format --check, mypy for `src/agents`.
* Critique (single pass, direct): the expected-rank oracle must be stated independently of the ranker, so ranks come from an explicit unit order with unique day counts, not from calling `rank`. Ranking and core stay unchanged. No approval is inferred; manifest approval is left empty by default.
* Out of scope: owner approval, live thresholds, real cohorts, AI task cohorts, API wiring.
* Correction plan (PR #697 threads): (1) record the approval-before-implementation deviation as a merge blocker; (2) carry sensor_data, source_record and appointment_history into ranked cases with field-sensitive negative controls; (3) pair accessibility cases on equal waiting days and add an ignore-support control; (4) compare precedence among retained cases so exclusions cannot hide demotions, with a combined-defect regression; (5) remove the public approval path so exported records stay blocked, keeping mock approval test-only.
* Correction cycle 2: review thread on observe precedence rule resolved; no scope change.
* Correction cycle 3 (PR #697): merged origin/main (restored a syntax-broken role-screens.js); fixed two threads: observe now emits unknown-ID and duplicate-ID ranker rows so the evaluator blocks, and a review_required observation flag keeps review burden accurate when a partial-source case is also demoted. New tests added; ruff, format, mypy and cohort tests pass.
