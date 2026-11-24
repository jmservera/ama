---
title: Issue 1204 strict tick-log window check, 2026-11-24
description: Adds a --require-extended mode to the tick-log checker so legacy windows cannot be read as proof of the closure and approval sub-claims
ms.date: 2026-11-24
---

Refs #1204. Synthetic demo, desktop only. Tier FOCUSED: `tools/` change only, no `src/` change, no Azure resource used or created, no browser proof applicable.

## Gap and change

The checker passed any window lacking the extended columns, so the 216-tick legacy window reads as "0 violations" although it carries no `closure_batch`, approval, `reclassified` or `global_stop` data. `tools/check-tick-log.py --require-extended` now reports a `schema` violation for every row missing one of those fields; the default mode is unchanged.

## Evidence

* `python3 -m unittest test_check_tick_log test_check_coordinator_handoff` in `tools/`: 25 tests, OK (1 new).
* `ruff check` and `ruff format --isolated --line-length 100 --check`: clean.
* Read-only copy of the real 216-tick coordinator `tick_log` (session `74bd1fe9`): default mode 0 violations (exit 0); `--require-extended` 216 violations (exit 1). Temporary copy deleted.
* Fresh scan of local session databases: three `tick_log` tables (216, 17 and 4 rows), none with extended columns.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Fresh classification before idle or stop | Proven (ticked) | Not re-audited |
| 2 Next action, bounded closure progress, approvals, no global stop | Rules proven, runtime unproven, stays unticked | Checker rules and tests cover every sub-claim; next-action proven on 216 real ticks; no real window has the extended fields, and a strict run now fails visibly instead of passing silently. Future-tick liveness is not provable for the demo |
| 3 One question, approved actions routed | Proven (ticked) | Not re-audited |
| 4 Prompts active, obsolete schedules stopped | Proven (ticked) | Not re-audited |
| 5 Handoffs and cleanup | Proven (ticked) | Not re-audited |
| 6 Dated RPI artifacts and checks | Proven (ticked) | Not re-audited |

## Follow-up

Once the coordinator records the extended columns, run `python3 tools/check-tick-log.py --require-extended <session.db>` on that window; a pass is the runtime evidence for criterion 2.
