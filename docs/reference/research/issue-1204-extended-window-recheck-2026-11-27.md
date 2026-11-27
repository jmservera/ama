---
title: Issue 1204 extended-window re-check and flaky guard test, 2026-11-27
description: Re-scan of local tick_log windows for the extended columns, the one real defect found (wall-clock bounds in the handoff guard tests) and the per-criterion proven or unproven table
ms.date: 2026-11-27
---

Refs #1204. Synthetic demo, desktop only. Tier FOCUSED: one `tools/` test file changed, no `src/` change, no Azure resource used or created, no browser proof applicable (the issue is a prompt and tooling contract). Credentials were not read.

## Evidence

* Scan of 332 local session databases: three `tick_log` tables (216, 17 and 4 rows). None has the extended columns (`closure_batch`, `approvals_granted`, `approvals_expired`, `reclassified`, `global_stop`). The 17 and 4 row tables use other schemas and the checker exits 2 ("no such column").
* Read-only copy of the 216-tick window (session `74bd1fe9`): `tools/check-tick-log.py` default mode 216 ticks, 0 violations (exit 0); `--require-extended` 216 violations (exit 1). Copies deleted.
* The coordinator agent contract (`.github/agents/ama-backlog-delivery-coordinator.agent.md`, lines 147-151) already names every extended field, so no contract gap.

## Defect found and fixed

`tools/test_check_coordinator_handoff.py` asserted wall-clock bounds of 0.1 to 0.5 s on regex-scaling guards. At host load average 8 they failed intermittently (2 of 4 reruns: 0.172 s against 0.15 s, 0.263 s against 0.25 s) with no code defect, so a green run could not be relied on as handoff evidence (criterion 5). All six bounds now use one `LINEAR_TIME_BUDGET_S = 2.0`; backtracking regressions on the 4000-element inputs exceed that by orders of magnitude, and the correctness assertions are unchanged. After the fix: 25 tests, OK in 5 of 5 consecutive runs at the same load; `ruff check` and `ruff format --isolated --line-length 100 --check` clean.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Fresh classification before idle or stop | Proven (ticked) | Not re-audited |
| 2 Next action, bounded closure progress, approvals, no global stop | Rules proven, runtime unproven, stays unticked | Checker rules, strict mode and agent contract cover every sub-claim; next-action holds on 216 real ticks; no real window has the extended fields, so closure progress, approval reconciliation and global-stop absence cannot be shown on real ticks. Future-tick behaviour is not provable from a snapshot |
| 3 One question, approved actions routed | Proven (ticked) | Not re-audited |
| 4 Prompts active, obsolete schedules stopped | Proven (ticked) | Not re-audited |
| 5 Handoffs and cleanup | Proven (ticked) | Handoff guard tests now deterministic under load |
| 6 Dated RPI artifacts and checks | Proven (ticked) | Dated 2026-11-27 artifacts accompany this change |

## Follow-up

When the coordinator writes the extended columns, run `python3 tools/check-tick-log.py --require-extended <session.db>` on that window; a pass is the runtime evidence for criterion 2. Independent exact-head review and hosted CI remain required before any ticking.
