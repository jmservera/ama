---
title: "Research: #146 RAI window reconciliation across restart and disabled-task owner exposure"
ms.date: 2026-11-14
task_slug: demo-146-rai-window-reconcile-0003
---

## Scope

Issue #146 RAI-2 / RAI-5 offline coverage. Out of scope: `infra/modules/operationalMonitoring.bicep` and `infra/workbooks/monitoring-workbook.json` (open PR #1579).

## Findings

* `src/core/src/zava_forward/core/monitoring_coverage.py` `reconcile_events` deduped repeat event IDs only within one in-memory call. A process restart loses `seen`, so a replay of earlier events in a second pass could not be recognised (gap).
* Disabled tasks appear in `assistants.registry()` `registered_tasks` (`assistants.py`, `enabled is False` branch) with `accountable_function`, `accountable_individual` (Unknown) and `activation` only inside the raw spec; no explicit owner/reason status row and no owner-gap flag (gap, RAI-4/RAI-6).
* Runtime suspensions are covered by `continuity.py` (`continuity_view`, role gated, free-text reason limited to authorised roles); not changed.
* `rai_release.named` is the shared "named" test; Unknown individuals never count as named.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready.

## Decisions

* Extend `reconcile_events` with an opaque `prior_event_ids` checkpoint and a returned `checkpoint` (ids only, bounded to 10000).
* Add pure `disabled_task_status` and surface it as `status` on disabled registry rows.
