---
title: Issue 188 research, ingestion into the store and consistency with the backfill
ms.date: 2026-11-02
---

## Disposition

Research disposition: reused. Planning Readiness: Ready (for a local re-validation scope only).

## Evidence

* Issue 188 closure audit comment (2026-10-31) lists all three criteria as unmet for the live Azure SQL scope.
* PR 587 (local constructed union, handover statistical checks) and PR 645 (read-only operator verifier `zava_forward.api.sensor_handover_verify`, `SensorConsumer.observed_series`) are merged on main.
* `docs/reference/research/iot-sensor-analytics-research-plan.md` lines 147-168 separate the local SQL contract from the actual Hub to Azure SQL run.
* Dependencies: 183 and 186 closed; 110 open (live Hub to Azure SQL ingestion, owner-gated: tier, sizing, cost, network exposure, device credential owner).

## Gap

All three criteria require a live-streamed run through Azure SQL. No Azure SQL, Hub or SQL Server prerequisite is available in this worktree (no sqlcmd, no running SQL container, no test URL), and no cloud fallback is permitted. No new source behaviour is justified.
