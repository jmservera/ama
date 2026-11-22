---
title: Issue 1204 tick-criterion re-check, 2026-11-22
description: Re-run of the tick contract checker against every local coordinator tick_log and its test suite, with the per-criterion verdict
ms.date: 2026-11-22
---

Scope: synthetic desktop demo, FOCUSED tier, no source change, no Azure resource used, no credentials read. Refs #1204. The prompt contract itself already requires the `closure_batch`, `approvals_granted`, `approvals_expired`, `reclassified` and `global_stop` fields (`.github/agents/ama-backlog-delivery-coordinator.agent.md`, tick_log bullet).

## Evidence

* Local coordinator session databases with a `tick_log` table (read-only scan of `~/.copilot/session-state/*/session.db`): three, unchanged since 2026-11-19. Their last rows are dated 2026-11-17 (216 ticks, 17 ticks) and 2026-11-05 (4 ticks). No window recorded after the fields were added exists.
* `python3 tools/check-tick-log.py <db>` on the 216-tick database: `216 ticks, 0 violations`. On the other two: `cannot read tick_log: no such column`, because they use a single `classifications` text column. Raw rows are operational text and are not committed.
* `python3 -m unittest test_check_tick_log -v` (run in `tools/`): `Ran 11 tests ... OK`. The synthetic cases cover the clean log, missing action with ready work, third tick after two no-progress ticks, closure batch bound and repeat, granted approval becoming ready the same tick, expired approval needing scoped reclassification, an unrelated task not blocked by expiry, global stop with remaining work, idle with full capacity or no work, SQLite input and CLI exit codes.

## Per-criterion table

| Sub-claim of the unticked criterion | Status | Basis |
| --- | --- | --- |
| Every tick has an actual next action | Proven for the 216-tick real window (2026-11-16 to 2026-11-17); contract enforced by synthetic tests | Checker: 0 violations; tests for no-progress and recovery |
| Bounded closure-review progress when capacity is free | Checker rule proven on synthetic rows only | No real row carries `closure_batch` |
| Expired and fresh approvals reconciled without a global stop | Checker rule proven on synthetic rows only | No real row carries approval or reclassification fields |
| One blocked lane is not a global stop | Synthetic rule proven; no real tick shows a stop | Test `global_stop` flagged with remaining work |
| Holds for every future tick | Cannot be proven for the demo | Needs an unbounded run; a new real window is the only evidence that can be added |

## Verdict

The box stays unticked. Real coordinator ticks recorded after the schema extension do not exist yet, so the closure-batch and approval sub-claims have only synthetic evidence. Re-run the checker on the first coordinator database that records the new fields.
