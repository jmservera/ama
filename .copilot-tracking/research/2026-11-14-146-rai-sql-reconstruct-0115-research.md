---
title: "Research: #146 RAI metrics rebuilt from SQL after restart"
ms.date: 2026-11-14
task_slug: 146-rai-sql-reconstruct-0115
---

## Disposition

Research executed. Planning Readiness: Ready.

## Evidence

* PR #1590 added `reconcile_events(prior_event_ids=...)` in `src/core/src/zava_forward/core/monitoring_coverage.py` (offline helper; review left Criterion 5 unticked, no store consumer).
* The persisted audit evidence for RAI behaviour is `assistant_events` (SqlStore SQLite and MSSQL): append-only, unique id, epoch `at`, content-free JSON body with `kind`, `state`, `action`, `envelope.outcome`, `actual_tokens`, `fence` (`assistants.py` `event()`, `migrate()`). The hash-chained `audit` table has no event ids and records case actions, so it is not the metric source.
* The Orchestrator has no assistant or RAI monitoring code; it shares the core store. API reaches the service through `Assistants` in `server.py`.
* Editable installs resolve to the main checkout, so worktree validation sets PYTHONPATH to the worktree `src` trees.

## Findings

* Persisted ids of a window are exactly the `prior_event_ids` a restarted process needs; no extra checkpoint table is required.
* `MAX_CHECKPOINT` (10000) bounds a window; larger windows must block, not guess.
