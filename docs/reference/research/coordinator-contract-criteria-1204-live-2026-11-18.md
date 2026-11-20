---
title: Coordinator contract criteria audit (issue 1204), live demo run 2026-11-18
description: Per-criterion proven or unproven record for the one unticked acceptance criterion of #1204
ms.date: 2026-11-18
---

Scope: synthetic desktop demo, FOCUSED tier, documentation and evidence only. Owner decisions of 2026-11-18 apply. Live Azure is authorised but this issue repairs a prompt contract and has no cloud surface, so no Azure resource, sign-in or browser proof was used and nothing was created or deleted. Candidate head `b285d6039b263929c343590ee98f2bc471306ca8` (equal to `origin/main` at fetch); agent blob `e745c4a68540bc4190f1dee0fa410a8a4a19393f`.

## Unticked criterion

> Every tick has an actual next action and bounded closure-review progress when capacity is free; expired approvals and freshly granted approvals are reconciled without treating one blocked lane as a global stop.

### Sub-claims and evidence

| Sub-claim | Evidence | Status |
| --- | --- | --- |
| Each tick advances at least one real action when capacity allows, no invented work | `.github/agents/ama-backlog-delivery-coordinator.agent.md` line 94 | Proven as instruction text on main |
| Bounded closure review (up to five unassessed items, rotating cursor, no repeats, continues when slots are full) | same file, line 135 | Proven as instruction text |
| A tick without a concrete action is recorded as no-progress; bounded recovery after two such ticks | lines 148 and 150 | Proven as instruction text |
| Expired approvals return only the affected scope to human-blocked; granted approvals become ready the same tick | line 263 (`approved_actions` reconciliation) | Proven as instruction text |
| A blocked lane is never a global stop | line 70, and the recurring prompt text near line 340 | Proven as instruction text |
| Instruction text is on main, not only a parent topic | `git log` shows `20f0b166f` (#1903, 2026-11-18) ported the contract; the corrected 2026-11-16 note named #1641, which is now `MERGED` into `main` (checked with `gh pr view 1641`) | Proven |
| Guard and tests pass for the current file | `python3 tools/check-coordinator-handoff.py` reports 1 target, 0 violations; `python3 -m unittest discover -s tools -p test_check_coordinator_handoff.py -q` ran 11 tests, OK | Proven |
| Contained behaviour scenarios | 2026-11-13 report (14 variants Pass, frozen blob `f453ffc15...`) covers refill, permissions and counting. It predates the 2026-11-18 port and did not target rotating closure batches or approval expiry | Partly proven, stale blob |
| Every actual scheduled tick, now and in future, satisfies the rule | Needs an unbounded run of real ticks with a `tick_log`; the 2026-11-16 closure correction recorded a tick with incomplete priority classification | Not provable for the demo |

## Verdict

| Criterion | Result |
| --- | --- |
| Every tick has an actual next action and bounded closure-review progress; approvals reconciled; no global stop | Unproven. Static instruction coverage is proven; runtime liveness over all ticks cannot be proven by a finite demo, and no behaviour scenario covers the current blob. The box stays unticked. |

The five ticked criteria are unchanged and were not re-audited here.

## Follow-ups

* If the owner wants the box ticked, run a contained hve-builder scenario for closure-batch rotation and approval expiry against blob `e745c4a68...` and read a bounded window of real `tick_log` rows. No agent-file change is required by this audit.
* The retired owner-approval gates (billing, DPO/Legal, assistive-technology testing) are irrelevant to this issue.

## Pass 2 (2026-11-19)

Base `origin/main` ec63bfc7c. The static sub-claims above were re-read against the current agent file and still hold. The guard `tools/check-coordinator-handoff.py` did not assert the liveness clauses, so deleting them would have passed. It now reports `missing-tick-liveness-rule` when the file lacks the bounded closure batch (up to five), `closure_review`, `tick_log`, `approved_actions`, the expired-approval reconciliation or the no-global-stop clause. Six mutation cases in `tools/test_check_coordinator_handoff.py` cover each clause; the live file passes (1 target, 0 violations; 11 tests OK).

Runtime liveness over real ticks stays unproven: the coordinator's session SQL (`tick_log`) is not available to this worker and a finite demo cannot cover future ticks. Live Azure was not used and nothing was created. Criterion 2 remains unticked.
