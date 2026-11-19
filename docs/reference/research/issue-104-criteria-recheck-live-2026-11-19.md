---
title: Epic 104 first unmet demo criterion recheck, 2026-11-19 (Refs #104)
description: Per-criterion proven or unproven table for epic 104 on the synthetic demo, with the finding that the first unmet criterion is not a code deliverable
ms.date: 2026-11-19
---

Refs #104. Scope is the synthetic demo, desktop only, under the owner decisions of 2026-11-18. No source code changed, no Azure resource was created and nothing was ticked on any issue. It builds on [the 2026-11-18 audit](./issue-104-epic-audit-live-2026-11-18.md).

## Finding

The first unticked criterion of #104 is the #440 stabilization checkpoint. Its text requires reconciliation, regression checks, bug disposition, and "owner-approved pivot/defer" records, and says merged children alone do not satisfy it. #440 itself still has two unticked criteria (triage into scoped issues with owner approval for pivots and deferrals; the PR artifacts and HVE Builder validation of the coordinator change). Neither is source code. Every child gap left by the audit is either an owner decision, person evidence, production-only, or a run needing new AI authorisation. So no code and test deliverable exists for this criterion on the demo.

The MSSQL old-image gap named in the 2026-11-18 audit as the one engineering item is already closed on main: `MssqlRevocationAndSuspension` in `src/api/tests/test_assistant_restart_non_replenishment.py` subclasses the revocation tests on a disposable SQL Server, and #107 now has zero unticked criteria.

## Evidence recorded (folder `.copilot-tracking/evidence/2026-11-19/issue-104-live-r4/`)

* `azure_cli_outputs.json`: read-only `az containerapp show -g ama -n ca-cutover-test-demo-api`, filtered to revision, image digest prefix and non-secret `AI_*`, `ZF_STORE`, `ZF_DEPLOYMENT_PROFILE`. Revision `ca-cutover-test-demo-api--0000033` (was 0000031 on 2026-11-18), `ZF_STORE` `mssql`, profile `demo`, model `gpt-4.1-nano-2025-04-14`.
* `unticked_criteria.txt`: unticked checkbox lines read with `gh issue view` for #440, #108, #164 and #216 on 2026-11-19.
* `invariants_test.txt`: `src/agents`, `PYTHONPATH=src:tests:../core/src:../core/tests:../api/tests`, `python -m unittest test_epic104_bounded_ai_invariants -q` under a throwaway venv holding the pinned `opentelemetry-*==1.45.2` packages: 27 tests, OK.
* No browser proof was taken: no UI or API behaviour changed and the owner decisions need no new screenshot; the 2026-11-18 probe of the six GET endpoints stands as the latest live read.

## Per-criterion table

| # | Criterion | Proven for the demo? | Basis |
| --- | --- | --- | --- |
| 1 | #440 stabilization checkpoint | Unproven | #440 OPEN with two unticked criteria; owner pivot and deferral decisions are not recorded; the criterion excludes merged children as proof. Cannot be proven by engineering. |
| 2 | All child features closed or deferred | Unproven | Closed: #105, #106, #107 (0 unticked), #432. Open: #108 (2 unticked), #164 (1), #216 (1). No owner deferral recorded. |
| 3 | AI never approves, executes, ranks or mutates controlled records | Proven (already ticked) | 27-test invariant suite passes on this head; 2026-11-18 live probe showed all assistants denied. |
| 4 | #432 complete or gap recorded | Proven (already ticked) | #432 CLOSED 2026-11-18; cost shown as Unknown with inputs named. |
| 5 | No capability enabled beyond the exercise without finite limits and alert | Proven (already ticked) | Unchanged from the 2026-11-18 live read; no new enablement was made. |

## Residual gaps and class

| Open item | Remaining gap | Class |
| --- | --- | --- |
| #108 model quotas | Regional quota route returned an empty list | Run, not code |
| #108 one-lever routing or caching | No live lever measured | Needs a finite AI authorisation |
| #164 thresholds approved | Accountable reviewer and thresholds | Owner decision |
| #216 gates on graded set | Re-run of 30 prompts via the model | Needs a later meter window and a regulatory-chat account |

## Limits

* Azure facts are operator-observed and filtered; full output was not kept.
* Issue states are as read on 2026-11-19 and may change.
* Independent exact-head review and hosted CI are outstanding.
