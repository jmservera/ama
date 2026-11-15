---
title: "Plan: #146 RAI SQL restart reconstruction"
ms.date: 2026-11-14
task_slug: 146-rai-sql-reconstruct-0115
---

## Objective

Every RAI metric is reconstructable from SQL audit records after an API or Orchestrator restart without double counting.

## Phases

1. Failing-first test `src/api/tests/test_rai_restart_sql_reconstruction.py` (two store lifecycles on one SQLite file).
2. `core/rai_metrics.py`: pure `classify` and `reconstruct` using `reconcile_events` with persisted ids as `prior_event_ids`.
3. `Assistants.rai_metrics` reads `assistant_events` by window; staff-only; `GET /api/assistants/rai-metrics`.
4. Validate (Focused tier), commit, no push.

## Decisions

* No new tables; the unique persisted ids are the checkpoint.
* Orchestrator untouched: it has no RAI consumer and shares the core reader.
* Metric mapping: invocation, refusal, withheld, validation_failure, fallback, human_review, override, consumption, latency_samples, tokens.

## Critique

Executed once before implementation (see critique file). Verdict: proceed.
