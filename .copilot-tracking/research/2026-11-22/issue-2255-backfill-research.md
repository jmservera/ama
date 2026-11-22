---
title: Issue 2255 research, demo hazards without aware_at
date: 2026-11-22
---

# Research

Research disposition: executed. Planning Readiness: Ready.

## Findings

* The note named in the brief (docs/reference/research/issue-2255-live-2026-11-22.md) does not exist in this worktree; the issue body and the 2202 mapwalk probe (22 unknown, 0 known, 22 named owners) are the evidence.
* `hazard_clock` and `clock_fields` (src/core taskqueues.py) read `hazard.aware_at`. With it, the queue derives the deadline from the existing reference window by priority (Emergency 24 h, Significant 7 d, or 14 d once accepted, Routine 14 d; clock_basis `operational_reference_from_awareness`). Without it the clock fails closed to "unknown". No `response_due_at` is needed, so the hazard service stays the timing authority.
* Hazards are inside `cases.body` JSON. `SqlStore.merge_seed` is insert-only and cannot update; the normal path for a case edit is `store._case`, mutate, `store.audit`, `store.save`.
* The SQL server `sql-cutover-test-rzsrg` has public access Disabled. The existing private routes are the replica `az containerapp exec` into `ca-cutover-test-demo-api` (used in earlier live notes) and one-off in-VNet jobs (`resident_sensor_seed.py`). The exec route reached the store with the app's own settings.
* Live read-only inspection (exec into the demo replica, counts only): 980 cases; 23 open hazards in 23 cases lack `aware_at`; 53 released skipped. All 23 are 14 days or older (Emergency 2, Significant 9, Routine 12), so a pure record-based backfill makes all 23 overdue and none running.

## Decision input

Record-based awareness (from `recorded_at`, else `noticed` at 09:00 UTC) is the honest default. To show a running clock, a small, marked, evenly spread subset (N) is re-dated to 40 percent of its reference window before run time; the original `noticed` is kept in a `demo_clock_seed` marker. Projected with N=6: 6 running, 17 overdue.
