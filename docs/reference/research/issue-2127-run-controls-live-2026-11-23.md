---
title: Simulator run owner, time limit and budget alert, main versus live (#2127)
description: Per-criterion record for the single remaining criterion of issue 2127 on the synthetic demo, with repository and live Azure evidence
ms.date: 2026-11-23
---

Scope: issue #2127 (split from #189), one unticked criterion: "Run has an owner, a time limit and a budget alert". Synthetic demo, desktop only, resource group `ama`. Owner decision of 2026-11-18 removes billing reconciliation, DPO/Legal approval and person-run assistive-technology testing from the demo scope. No Azure resource was created, changed or deleted, and no credential was read.

## Evidence

Repository (main, worktree head):

* `src/core/src/zava_forward/core/synthetic/run_plan.py` and `run_governance.py` refuse a run without a governed owner (`RUN_OWNER_COST_ALERT_REQUIRED`), bound the time limit to at most 3600 seconds (`MAX_TIME_LIMIT_SECONDS`), and require a budget alert contract (`BudgetAlertContract`, `INVALID_BUDGET`).
* `infra/live-simulator-job.bicep` sets `replicaTimeout: 240`, a single scheduled run, no retries, and mounts the admin-written `control.json` (cohort, owner, expiry, stop). `infra/modules/iothub.bicep` and `infra/main.bicep` define `actual80` and `forecast100` budget notifications.
* Command run from `src/core`: `PYTHONPATH=src:tests python3 -m unittest tests.test_simulator_run_controls_189 -q` gave `Ran 11 tests ... OK`, including `test_live_infra_bicep_matches_actual80_and_forecast100_run_controls` and the tamper and drift tests.

Live Azure (read-only `az` queries, 2026-11-23):

| Control | Live observation |
| --- | --- |
| Budget alert | `budget-iot-cutover-test-rzsrg`, USD 25 monthly, scoped to the IoT Hub; current spend about USD 13.35. Notifications `actual80` (GreaterThan 80, enabled) and `forecast100` (GreaterThan 100, enabled). Subscription-level resource-group budgets `budget-forward-test` and `budget-cutover-test` (USD 300, spend about USD 142) carry the same two rules. |
| Owner | IoT Hub `iot-cutover-test-rzsrg` tagged `owner: Juan Manuel Servera`; the demo jobs carry the same owner tag. The live simulator job itself carries no `owner` tag; its run owner is held in the mounted `control.json`, which was not read. |
| Time limit | `job-live-simulator` has `replicaTimeout` 270 seconds, trigger `Schedule`, `--once`, 108 executions listed, latest runs `Succeeded` or `Running`; 6 executions `Failed` (not analysed here). 270 is below the 3600 second cap. |
| Run expiry and stop | `ZF_SIM_CONTROL_FILE` and `ZF_SIM_APPROVAL` are set on the job; `live_simulator.py` logs `run control: stopped or expired; nothing sent` and ends the run. |

## Findings

* Drift: live `replicaTimeout` is 270 seconds while `infra/live-simulator-job.bicep` declares 240. Both satisfy the cap, so the criterion holds, but the source and the live job differ. No deployment was made (no production or estate change authorised for this task); recorded for the owner.
* No code gap was found, so no source change was made.

## Per-criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| Run has an owner | Proven in code and tests; live owner tag proven on the hub; the per-run owner in the mounted `control.json` is unproven live (file not read) | Tests above, `az` tags |
| Run has a time limit | Proven live (270 s replica timeout, one-shot schedule) and in code (cap 3600 s) | `az containerapp job show` |
| Run has a budget alert | Proven live (`actual80` and `forecast100` on a hub-scoped budget) | `az consumption budget list` |

The issue's own wording covers production-only, DPO and legal items that the demo decision excludes; none of them is claimed here.
