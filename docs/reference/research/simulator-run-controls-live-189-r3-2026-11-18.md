---
title: Simulator run controls live audit, third pass (issue 189, demo, 2026-11-18)
description: Per-criterion audit of issue 189 against the repository and the live demo, with a wall-clock time-limit exercise and an adverse finding on budget alert delivery
ms.date: 2026-11-18
---

Refs #189. Scope is the synthetic desktop demo (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). No source file changed, no Azure resource was created or modified and no sign-in was needed, so nothing needs deleting. This pass re-reads the live state after the [first](./issue-189-simulator-run-controls-live-evidence-2026-11-18.md) and [second](./simulator-run-controls-live-189-2026-11-18.md) passes and adds a real wall-clock exercise of the run meter. Raw output is in [the evidence folder](./simulator-run-controls-live-189-r3-2026-11-18/). No secrets are recorded; email addresses are redacted to `<email>`.

## Live observations (2026-11-18 16:00 UTC)

| Check | Result |
| --- | --- |
| Hub `iot-cutover-test-rzsrg` | B1, capacity 1, Active; tags `owner` (a named person) and `purpose` non-production-demonstrator |
| Budget `budget-iot-cutover-test-rzsrg` | USD 25 monthly, spend USD 5.48 (0.8 percent of the USD 700 cap); `actual80` and `forecast100` enabled, one contact each |
| Budgets `budget-cutover-test`, `budget-forward-test` | USD 300 monthly, spend USD 90.61, same two notifications |
| Simulator job and control | No simulator job among the eight cutover jobs; no `ZF_SIM`, control or live setting on `ca-cutover-test-demo-api`, so no run can start live |
| Action group `ag-cutover-test-ops` | Enabled; email receiver domain is the GitHub noreply domain |

Adverse finding: the IoT budget contacts and the ops action group both use a GitHub noreply domain, and `budget-forward-test` uses `example.invalid`. A budget threshold would be evaluated by Azure, but delivery to a monitored human mailbox is not shown and cannot be shown without sending mail. Raw: [azure-readonly-raw.txt](./simulator-run-controls-live-189-r3-2026-11-18/azure-readonly-raw.txt).

## Repository checks

* `src/core` tests `test_simulator_run_controls_189` and `test_simulator_run_budget_controls`: 32 run, OK (observed; raw output not retained).
* `src/api` test `test_simulator_admin`: 30 run, OK (observed; raw output not retained).
* Wall-clock exercise of the repository `RunMeter` with `time.monotonic`, owner `demo-owner`, a 6 second limit and a 0.5 alert and 1 cap: spend of 0.6 raised `budget_alert`; the loop then halted with `RUN_DEADLINE` and event `time_limit_halt`; a blank owner was refused with `RUN_OWNER_REQUIRED`. Raw: [runmeter-wallclock-raw.txt](./simulator-run-controls-live-189-r3-2026-11-18/runmeter-wallclock-raw.txt). This is real repository code on a real clock, not a deployed run.
* The deployed admin endpoint refused staff with 403 in the second pass; the administrator role was not granted (identity change on the shared tenant, outside the authorisation).

## Per-criterion result

| Criterion | State | Basis |
| --- | --- | --- |
| Cost estimate for the declared N homes recorded before any run (ticked) | Consistent, no change | Allocation USD 60 per month for B1 (research plan); observed spend USD 5.48; N=5000 refused by the headroom check in tests |
| Message quota headroom against the #140 tier (ticked) | Consistent, no change | Live hub B1 capacity 1; 400000 per day quota; headroom validator tested |
| Run has an owner | Proven for the demo | Live hub `owner` tag; start refuses a blank owner (tests and wall-clock exercise) |
| Run has a time limit | Proven in code on a real clock; no deployed run | Wall-clock `RUN_DEADLINE` halt; control expiry capped at 14 days; no live job or control file exists and none may be added under the demo decision |
| Run has a budget alert | Configuration proven live; firing and human delivery unproven | Three budgets with enabled 80 percent actual and 100 percent forecast notifications; recipients are noreply or invalid addresses; spend is 22 percent of the IoT budget, so no alert has fired |
| Whole criterion 3 as a conjunction on one live run | Unproven | Needs a deployed simulator run with the control enabled, an administrator role and a monitored recipient |

## Separate production-only items

* A deployed run with the control file and an administrator role: needs a deployment and identity change.
* A real alert recipient and a firing test: needs a named mailbox and spend at the threshold.
* Billing reconciliation, DPO or Legal approval and person-run assistive-technology testing are outside the demo.

The owner ticks; this note does not tick criterion 3. Independent review and hosted CI are outstanding.
