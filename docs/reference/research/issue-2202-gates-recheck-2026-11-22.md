---
title: Issue 2202 recheck on API revision 0000054 and resident revision 0000026, with exact owner gates (2026-11-22)
description: Read-only Azure CLI and Playwright recheck of the demo deployment and the AI gating state, recording the two owner gates and a per-criterion table for 2202
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, owner decisions of 2026-11-18. Sign-in values were read at run time and never printed. Nothing was changed, deployed, created or pushed. Focused tier, documentation only. Probes and outputs: [issue-2202-gates-recheck-2026-11-22/](./issue-2202-gates-recheck-2026-11-22/). Refs #2202. Earlier proofs: [final proof](./issue-2202-finalproof-2026-11-22.md), [deploy proof](./issue-2202-deployproof-2026-11-22.md).

## Deployed state

[az-state.txt](./issue-2202-gates-recheck-2026-11-22/az-state.txt) and [az-state-2.txt](./issue-2202-gates-recheck-2026-11-22/az-state-2.txt):

* `ca-cutover-test-demo-api--0000054`: Running, Healthy, 100 percent traffic, created 2026-11-22 23:14 UTC, image digest prefix `3f2be6644fd4`, `ZF_CONTAINER_HARDENING=enforced`.
* `ca-resident-demo--0000026`: RunningAtMaxScale, Healthy, 100 percent, created 23:14 UTC, digest prefix `a71084bd2d42`, no hardening variable, `ZF_DEMO_EXPIRES_AT=2028-01-01T00:00:00Z`.
* `ca-cutover-test-demo-agents`: `ZF_CONTAINER_HARDENING=enforced`, so no api versus agents difference exists; the resident app is a separate image without the variable.
* Jobs: `job-live-simulator` (digest prefix `295164ca739d`) executions at 23:30 and 23:37 Succeeded, 23:45 Running; `job-live-receiver` (`541068a62d81`) 22:30 and 23:00 Succeeded, 23:30 Running. Their digests differ from the API digest, so they are not shown to be rebuilt from the same commit as 0054.
* A job `job-tmp-probe-2061` exists, was not created in this run and was left untouched; it uses the simulator digest.

## AI gating state and owner gates

| Gate | Observed state | Evidence | Owner action required |
| --- | --- | --- | --- |
| SUS-1, open suspension | `/api/continuity` HTTP 200 lists one suspension: scope `all` (kind `release`), status `Suspended`, reason "Demo probe: negative test", recorded 2026-11-18 11:51, containment "None; probe is refused". Employee chat status says AI answers are on hold. | [probe-continuity-result.json](./issue-2202-gates-recheck-2026-11-22/probe-continuity-result.json), [probe-staff-chat-result.json](./issue-2202-gates-recheck-2026-11-22/probe-staff-chat-result.json), [screen](./issue-2202-gates-recheck-2026-11-22/screens/employee-chat.png) | A named human lifts the suspension through the restart route in [issue 221 evidence](./issue-221-live-suspension-restart-evidence-2026-11-18.md), or approves another removal. The label SUS-1 is taken from the issue 2202 comment; the API output shows no identifier. |
| Resident ledger budget expiry | Resident reply label: "Summary by rules - AI unavailable: the AI usage limit was reached"; routing "Case progress helper". The older "exercise has ended" text does not appear. | [probe-resident-ai-a.json](./issue-2202-gates-recheck-2026-11-22/probe-resident-ai-a.json), [screen](./issue-2202-gates-recheck-2026-11-22/screens/resident-ai-a.png) | Extend `resident_ai.budget.expires_at` (default 2026-11-01 in [infra/sql/resident-assistant.sql](../../../infra/sql/resident-assistant.sql)) as an owner-reviewed data change per `infra/README.md`, then rerun `probe_resident_ai.py`. |

The budget expiry could not be read directly: the SQL server has public network access `Disabled` (checked with `az sql server show`). The expiry is the probable cause of the refusal, not a confirmed one; the other reasons (5 attempts per resident per hour, 2000 in total) cannot be excluded from the label alone. The resident app environment variable `ZF_DEMO_EXPIRES_AT` is set to 2028-01-01, so the deployment is not the blocker.

## Employee chat recheck

Of two asks, the funding question returned HTTP 200, kind `answer`, origin `decision_rule` ("Recorded case fields and fixed rules, not generative AI"), model `workflow-only`, routed to the Funding evidence agent. The first ask again timed out in the widget probe at 120 s (the known probe artefact recorded in the final proof; the dedicated UI probe answered in 7.2 s on 0053). Not re-diagnosed here. No generative answer exists.

## Per-criterion table for #2202

| Criterion | Result | Basis |
| --- | --- | --- |
| API, resident, simulator and receiver images rebuilt from main and rolled | Partly proven | API 0054 and resident 0026 are live (created 23:14 UTC) with digests above. Simulator and receiver run recent executions on their own digests; no source commit can be shown for any image from the CLI. |
| Revisions Running and Healthy; hardening enforced with rollback noted; agents app difference explained | Proven for state; rollback not exercised | Running and Healthy shown; api and agents `enforced`; resident has no variable by design (separate image). Rollback is re-deploying a prior digest or resetting the variable and was not exercised. |
| Owner demo checks: sensor charts, map gauges, consent checkbox, chat routing, half of homes with readings | Chat routing proven again; others unproven on 0054/0026 | Routing to the Funding evidence agent and the Case progress helper observed. Charts, map and coverage were proven on 0053/0025 in the [final proof](./issue-2202-finalproof-2026-11-22.md); consent checkbox on 0024 ([2192 r4](./issue-2192-live-r4-2026-11-22.md)); none re-run on the new revisions in this pass. |
| Live receipt and `docs/reference/log.md` entry | Proven | This note and its log entry, plus earlier receipts. |
| Generative AI answers (issue comment, not a checkbox) | Unproven; blocked by owner gates | SUS-1 open and resident ledger refusal as above. |

## Next owner actions

* Lift or accept the open suspension.
* Extend the ledger expiry through a private SQL path.
* Then rerun the employee ask and `probe_resident_ai.py`, and re-run chart, map, consent and coverage checks on the current revisions.
