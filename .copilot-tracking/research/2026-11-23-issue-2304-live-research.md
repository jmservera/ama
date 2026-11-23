---
title: Issue 2304 forecast research
ms.date: 2026-11-23
---

# Research: GET /api/assistants/forecast does not answer on live data (#2304)

Research disposition: executed. Planning Readiness: Ready.

## Scope and tier

Synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (read-only probe here). Tier FULL for the `src/` change, but `rpi-checks.py --all` is not run by this worker.

## Evidence

* `Assistants.forecast` in `src/core/src/zava_forward/core/assistants.py` runs, for each allowed assistant and each open case in scope, `snapshot` then `_due`. Per case these read the procurement meta row, the schedule slot, the task by id, release and continuity records (through `_task_id`, `_scope`, `_adopt`), and for Quality the per-home sensor readings and consent index.
* Profile on an equivalent SQLite-backed store with a counting connection (same data, identical output):

| Open cases | Statements before | Statements after |
| --- | --- | --- |
| seed set | 422 | 16 |
| seed set plus 40 clones | 3622 | 16 |

  The cost before is about 80 statements per additional open case across the five assistants. On Azure SQL each statement is a network round trip on one connection, so 443 cases give tens of thousands of round trips. Time goes to round-trip latency, not compute.
* Live baseline (revision 0000055) is recorded in the evidence folder.

## Decision

Serve the forecast from a read-through view of the connection (`forecast_reads.py`): repeated global statements are answered once, per-case schedule, task, adoption and sensor-home lookups come from a fixed number of bulk reads, and a 10 second budget turns an overrun into a named 503 state with `Retry-After` instead of a silent hang. Output equality with the old path was checked on both data sets.
