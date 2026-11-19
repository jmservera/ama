# Issue 222 live demo research (opened 2026-11-18)

Refs #222. Scope: synthetic desktop demo; owner decisions of 2026-11-18 apply. Production-only criteria stay deferred (#1905-#1908).

## Research disposition

Disposition: reused plus local re-run. Five of six criteria are already ticked in the issue. One is unticked: owner approval of cohorts, lawful analysis fields and thresholds before live use (OQ-018). Baseline evidence: `src/agents/tests/test_cohort_ranking_eval.py`, `test_cohort_ai_eval.py`, `test_cohort_manifest_draft.py`, and the review pack `docs/reference/research/evaluation/cohort-evaluation-review-pack.md`.

## Questions

1. Do the cohort tests still pass at this head (regression evidence for ticked criteria)?
2. Can the unticked criterion be proven for the demo? It requires named owner, DPO and competent-task-owner approval, which the owner decisions of 2026-11-18 explicitly do not supply, and the criterion itself states synthetic results are not fairness evidence.

## Planning readiness

Ready: no source edits, no Azure action needed (the evaluation is offline and deterministic; the live app adds no cohort surface). Evidence plan: run the three cohort test modules, record output, write research note under `docs/reference/research/`.
