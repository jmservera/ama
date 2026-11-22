---
title: Issue 146 monitoring coverage, API 5xx, receiver job and SQL DTU (2026-11-22)
description: Read-only live inventory of the demo plus source additions for a SQL DTU alert and a receiver job failure alert, with a proven or unproven result per unticked criterion
ms.date: 2026-11-22
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-22 about 20:20 UTC. All Azure calls were read-only; no resource was created, so nothing needed deleting. No drill, no Key Vault rotation, no deployment. Earlier pass: [2026-11-19 re-check](./issue-146-live4-monitoring-2026-11-19.md).

## Live observations

| Command (all `-g ama`) | Result |
| --- | --- |
| `az monitor metrics alert list` | Enabled: Foundry throttle, SQL CPU (`cpu_percent` >85), API 5xx and API restarts for both `cutover-test` and `cutover-test-demo`. Disabled candidates: job failed for `demo-audit`, `demo-orch`, `demo-load`; four IoT rules |
| `az monitor scheduled-query list` | Enabled: Key Vault expiry and denied access, ledger digest mismatch and verify missing (both prefixes). Disabled: AI limits, agent tasks poison |
| `az resource list --resource-type microsoft.insights/workbooks` | One workbook installed (none on 2026-11-19) |
| `az sql db show` | Standard, capacity 100 (S3); metrics `dtu_consumption_percent`, `dtu_limit`, `dtu_used` exist; no DTU alert |
| `az monitor metrics list --metric dtu_consumption_percent`, hourly, 14:20 to 19:20 UTC | Average 15.7 to 20.9 percent; Maximum 82, 85, 85, 87, 89, 92 percent |
| `az containerapp job execution list job-live-receiver` | 61 Failed, 43 Succeeded, 2 Stopped, 1 Running; no alert covers this job |
| `az monitor metrics list` on the receiver job, `Executions` split by `state` | Failed 0 in the last three hourly buckets |
| `az monitor metrics alert show alert-job-cutover-test-demo-orch-failed` | `timeAggregation` Total (the 2026-11-19 aggregation concern is already fixed in source and deployed) |

## Source changes (not deployed)

* `infra/main.bicep`: `sqlDtu` alert, `dtu_consumption_percent` Average >80 over 15 minutes, severity 3, only when `sqlTier` is `dtu`.
* `infra/live-receiver-job.bicep`: optional `failureAlertActionGroupId`; when set, a failed-execution alert on the receiver job.
* `infra/monitoring-runbooks.md`: entries `sql-dtu`, `job-live-receiver` and API 5xx queries, each with proposed owner.
* `infra/tests/test_monitoring_alert_coverage.py`: both new rules must name an owner and a valid runbook anchor.

Validation: `bicep build` of both templates clean; `infra/tests` monitoring, outputs wiring, network posture, container hosting and demo wiring tests pass (31 and 54 tests); `src/core` monitoring tests pass (37). Tier: focused (no src, no security control change); hosted CI for the exact head is not observed here.

## Result per unticked criterion

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest and IoT Hub ingestion | Partly proven | Ledger digest alerts proven installed and enabled. Job, poison and IoT rules are installed but disabled; the receiver job and SQL DTU rules are source-only until a separately authorised deployment. No firing or notification drill was run. Unproven as a whole |
| Dashboard or workbook shows availability, errors, latency and cost against budget | Unproven | A workbook is installed, but workspace queries are private-link only, so a render cannot be observed from this host; opening public query would weaken a control |
| Each alert has a runbook entry with an owner | Partly proven | Every authored rule, including the two new ones, has a test-enforced entry naming a proposed role. Naming a person is a human decision, so unproven |
| Tokenomics: metered AI usage by capability beside the Azure cost record, variance visible | Proven for the demo on 2026-11-18 | See the [2026-11-19 note](./issue-146-live4-monitoring-2026-11-19.md); Azure billing reconciliation is excluded by owner decision. Not re-run today |

No box is ticked by this note.
