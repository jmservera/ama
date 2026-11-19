---
title: Simulator run controls, cost and quota live evidence, second pass (issue 189, demo, 2026-11-18)
description: Live read-only Azure checks, a signed-in probe of the deployed admin control endpoint and an offline exercise of start, stop and rate limits for issue 189
ms.date: 2026-11-18
---

Scope: synthetic demo only, desktop, resource group `ama`, cap USD 700. This pass extends the
[first pass](./issue-189-simulator-run-controls-live-evidence-2026-11-18.md). No source file changed, no Azure
resource was created or changed, no role was granted, and no simulator run was started. No secrets are recorded;
the owner name and email in raw output are replaced with `<owner-name>` and `<email>`. Raw output is retained in
[the evidence folder](./simulator-run-controls-live-189-2026-11-18/).

## Live observations

| Check | Result | Retention |
| --- | --- | --- |
| IoT budget `budget-iot-cutover-test-rzsrg` | USD 25 monthly, current spend USD 5.16 (20.6 percent of budget, 0.7 percent of the USD 700 cap); notifications `actual80` (over 80 percent actual) and `forecast100` (over 100 percent forecast), both enabled with one contact email | Retained: [azure-readonly-raw.txt](./simulator-run-controls-live-189-2026-11-18/azure-readonly-raw.txt) |
| IoT hub `iot-cutover-test-rzsrg` | Basic B1, capacity 1, Active, tag `owner` set (the run owner of record) | Retained, same file |
| Hub metrics, last 24 h | `d2c.telemetry.ingress.success` total 135; `dailyMessageQuotaUsed` maximum 96 per hour sample, summed 34411 across hourly samples (a cumulative gauge, so the sum is not a message count) | Retained, same file |
| Simulator job and control file | No `job-live-simulator` among the eight cutover jobs; `ZF_SIM_CONTROL_FILE` is not set on `ca-cutover-test-demo-api` (observed; raw output not retained, the `simcontrol env` section of the raw file is empty), so nothing can send | Job list retained, same file |
| Deployed admin endpoint, staff sign-in (Playwright, read at runtime) | `GET /api/admin/simulator-control` 403 `ADMIN_REQUIRED`; `/start` and `/stop` 403; unknown sub-path 403 | Retained: [probe-output-raw.txt](./simulator-run-controls-live-189-2026-11-18/probe-output-raw.txt), script `probe.py` |

The staff test user holds a staff role, not `ZavaForward.ApplicationAdmin`. Assigning that role is an identity
change on the shared tenant, outside the owner's authorisation (no production changes), so the live admin start
and stop could not be exercised. The denial is itself live proof that the deployed image carries the endpoint and
refuses non-administrators with no detail.

## Start, stop and rate controls (offline, real code)

[local_exercise.py](./simulator-run-controls-live-189-2026-11-18/local_exercise.py) drives
`simulator_admin.handle` against a throwaway control file with an administrator principal. Raw output:
[local-exercise-raw.txt](./simulator-run-controls-live-189-2026-11-18/local-exercise-raw.txt).

| Action | Result |
| --- | --- |
| Start without confirmation | 400 `CONFIRMATION_REQUIRED` |
| Start with blank owner | 400 `CONTROL_INVALID` |
| Start with expiry 15 days out | 400 `CONTROL_WINDOW_INVALID` (limit 14 days) |
| Start, 5 homes, expiry two hours out | 200, audit entry `sim_control_start` written |
| Second start while permitted | 409 `ALREADY_RUNNING` |
| Stop | 200, audit entry `sim_control_stop`; control disabled |
| Rate limits | `Limits`: 10 messages per second maximum, batch 50, 4 attempts |
| Capacity N=1, 60, 1000 | accepted; N=5000 refused `B1_QUOTA_HEADROOM` |

The 2000-home start case in the script was refused for home-identifier format, not rate, so it is not evidence
for a rate refusal; the capacity rows are. Cost estimate: B1 with one unit is a flat monthly charge allocated at
USD 60 per month (cited from the [research plan](./iot-sensor-analytics-research-plan.md), not measured here); observed spend on the budget
scope is USD 5.16 month to date. The quota is 400000 messages per day on B1 (observed; raw output not retained; demo budget in the control status:
360000), and observed use is far below it.

## Per-criterion result

| Criterion | State | Evidence |
| --- | --- | --- |
| Cost estimate for the declared N homes recorded before any run (ticked) | Consistent | Allocation and capacity rows above; observed spend USD 5.16 |
| Message quota headroom against the #140 tier (ticked) | Consistent | B1 capacity 1 live; 135 messages in 24 h; N=5000 refused |
| Run has an owner | Proven for the demo | Hub `owner` tag live; start refuses blank owners and records the owner in the control (offline) |
| Run has a time limit | Proven in control code, not by a live run | Expiry required and capped at 14 days; stop disables. No simulator job exists, and none was created |
| Run has a budget alert | Proven as configuration, not as a firing | USD 25 budget with two enabled notifications. The control has no alert field and says so in its status. Firing would need spend to the threshold |

The criterion stays unticked unless the owner accepts this table for the demo; the control-to-alert link is
configuration, not code, and no live run exists to observe it.
