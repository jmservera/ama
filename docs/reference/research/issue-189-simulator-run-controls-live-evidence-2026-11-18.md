---
title: Issue 189 simulator run controls live evidence (demo, 2026-11-18)
description: Per-criterion evidence for issue 189 on the synthetic demo; the run owner, time limit and budget alert criterion is proven in part live and in part by the deterministic control code
ms.date: 2026-11-18
---

Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, read-only Azure calls. Owner decisions of 2026-11-18 apply (no drills, no Key Vault rotation, no production change). No source files were changed and no resource was created, so nothing needed deleting. No secrets recorded.

## Live observations (read-only)

| Check | Command | Result |
| --- | --- | --- |
| Budgets | `az consumption budget list -g ama` | `budget-iot-cutover-test-rzsrg` USD 25 monthly; `budget-cutover-test` and `budget-forward-test` USD 300 monthly. Each has `actual80` (greater than 80 percent) and `forecast100` (greater than 100 percent) notifications, enabled. |
| Hub tier | `az iot hub show -n iot-cutover-test-rzsrg` | Basic B1, capacity 1, state Active; `owner` tag set. |
| Simulator job | `az containerapp job list -g ama` | No `job-live-simulator`; only manual cutover jobs exist, so nothing can run unattended. |

## Code-path observations (local, deterministic)

* `src/core` tests `test_simulator_run_controls_189` and `test_simulator_run_budget_controls`: Ran 32 tests, OK.
* A `RunGovernance`/`RunMeter` run (owner set, 30 minute limit, GBP 4 alert, GBP 5 cap): accumulated GBP 4.5 emitted one `budget_alert` event naming the owner; a further GBP 1 halted with `RUN_BUDGET_HALT`; a clock beyond 1800 seconds halted with `RUN_DEADLINE`; blank and `TBD` owners were refused with `RUN_OWNER_REQUIRED`.

## Per-criterion result

| Criterion | State | Evidence or reason |
| --- | --- | --- |
| Cost estimate for the declared N homes recorded before any run (ticked) | Previously ticked; consistent | The estimate helper reports tier B1, 1 unit, 30 messages for the declared sample against 400000 messages per day. |
| Message quota headroom checked against the tier decided in #140 (ticked) | Previously ticked; consistent | Hub is B1 with capacity 1, matching the decision; headroom above. |
| Run has an owner | Proven | Hub `owner` tag live; `RUN_OWNER_REQUIRED` refusal in code. The per-run owner in the admin-written `control.json` was not observed because no job is deployed. |
| Run has a time limit | Proven in code only | `RUN_DEADLINE` halt; template `replicaTimeout: 240`. Not provable live: no simulator job is deployed, and deploying one (device registration, certificates, image push) is a production-affecting owner step outside this task. |
| Run has a budget alert | Proven (configuration); firing not demonstrated | The USD 25 IoT budget alerts at 80 percent actual and 100 percent forecast. Firing it would require spending to the threshold, which the cap and the no-drills rule forbid. |

Recommendation: leave the criterion unticked until a simulator job is deployed and a run is observed with its time limit; then tick it. The owner may instead accept the table above as sufficient for the demo.
