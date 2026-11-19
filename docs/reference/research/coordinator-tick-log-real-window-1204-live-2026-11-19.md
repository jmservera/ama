---
title: Coordinator tick liveness on a real tick_log window (issue 1204), 2026-11-19
description: Result of running tools/check-tick-log.py on 216 real coordinator ticks, with what the window can and cannot prove
ms.date: 2026-11-19
---

Scope: synthetic desktop demo, FOCUSED tier, no source change, no Azure resource used. Refs #1204. This note corrects the 2026-11-19 r2 claim that no local `tick_log` exists: a read-only scan of `~/.copilot/session-state/*/session.db` finds three coordinator databases with `tick_log` (216, 17 and 4 rows).

## Method

* Source: coordinator session database `74bd1fe9`, table `tick_log`, 216 ticks from 2026-11-16 08:29:52 to 2026-11-17 11:34:37.
* Export: read-only, mapped `ready_count`, `running_count`, `unknown_count` (as `unassessed`), `human_blocked_count`, `dep_blocked_count`, `action_taken` and `evidence` to the checker row schema, written to a temporary file and deleted afterwards.
* Command: `python3 tools/check-tick-log.py <export>`.

## Result

| Measure | Value |
| --- | --- |
| Ticks checked | 216 |
| Violations | 0 (exit 0) |
| Ticks with empty action or evidence | 0 |
| Ticks with ready or unassessed work | 175 |
| Ticks with no pending work | 37 |
| Action texts mentioning closure review | 36 |
| Action texts mentioning approvals | 3 |

## Per-criterion table

| Sub-claim of the unticked criterion | Status | Basis |
| --- | --- | --- |
| Every tick has an actual next action with evidence | Proven for this 216-tick window | Checker: no no-progress or recovery violation |
| Bounded closure-review progress (at most five, no repeats) | Unproven | The export has no `closure_batch` column; only text mentions in 36 ticks |
| Expired and granted approvals reconciled | Unproven | No approval or reclassification columns; 3 text mentions only |
| A blocked lane is never a global stop | Partly proven | No tick in the window carries a stop signal; the schema has no `global_stop` field, and counts show 35 to 57 blocked items beside launched work |
| Holds for every future tick | Not provable for the demo | Needs unbounded runtime |

## Verdict

The criterion stays unticked. The window gives real evidence for the next-action sub-claim and none of the closure-batch and approval sub-claims, because the coordinator's `tick_log` schema does not record them. The other two databases (17 and 4 rows) store classifications in one text column and were not mapped.

## Follow-up

* Extend the coordinator's `tick_log` instruction to record `closure_batch`, approval events, reclassifications and a stop flag, then re-run the checker on a new window. That is a prompt change owned by the coordinator, outside this demo run.
