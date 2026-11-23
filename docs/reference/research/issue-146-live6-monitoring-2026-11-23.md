---
title: Issue 146 monitoring coverage, live workbook query execution (2026-11-23)
description: Live execution of the operations workbook queries now that workspace query access is open, one real workbook query defect fixed, and a proven or unproven result per unticked criterion
ms.date: 2026-11-23
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-23 about 14:50 to 15:00 UTC. Azure calls were read-only except one throwaway storage account (tag `purpose=tmp146-delete`) with a queue diagnostic setting, created and deleted in this run; `az resource list` then showed no `tmp146` name. No drill, no Key Vault rotation, no deployment, no production change. No credential was read. Earlier pass: [2026-11-22](./issue-146-live5-monitoring-2026-11-22.md).

## Observations

| Observation | Result |
| --- | --- |
| Inventory | Unchanged from 2026-11-22: six enabled metric alerts (Foundry throttle, SQL CPU, API 5xx, API restarts for both prefixes), six enabled scheduled-query alerts for ledger digest mismatch and verify missing plus Key Vault expiry and denied access; job-failure, IoT, AI-limit and poison candidates disabled; one workbook installed; action group with one email receiver; budgets `budget-cutover-test` and `budget-forward-test` 300 and `budget-iot-cutover-test-rzsrg` 25 (monthly) |
| Workspace query access | `log-cutover-test` now reports query access Enabled (ingestion Disabled). Earlier notes found it private only, so workbook queries can be executed from the CLI for the first time. This is a new observation, not a change made here |
| Workbook KQL executed (7-day window, budget 300) | `cost-vs-budget`: returns AzureActualCost Unknown and the unreconciled basis, not zero. `ai-usage-by-capability`: returns 16 attributed calls, Azure cost record "Unknown (billing record not connected)". `ai-limit-breaches`: 30 holds, reason liability-unknown, owner "appointment pending", runbook `infra/monitoring-runbooks.md#ai-limits`. `requests` and `availability`: execute and return Status Insufficient with 0 rows. `operation-errors-latency`: 0 rows |
| Defect: `ai-variance-by-period` | Failed with SEM0100 "Failed to resolve column ... AzureCostRows". A probe (`print A=1 \| extend C=2, B=C+1`) fails the same way on this workspace, so Log Analytics does not allow an extend to use a column defined in the same extend. Fixed in source by splitting the extend; the fixed query returns Period 2026-11, AttributedCalls 16, UnattributedUsageRows 0, UnreconciledVariance "Unreconciled, not zero", Variance and BilledCost null |
| Application Insights | `appi-cutover-test` has no workspace link (not workspace-based) and query access Disabled, so `AppRequests` and `AppAvailabilityResults` hold no rows in the workspace and the availability, error and latency tiles can only show Insufficient |
| Storage queue signal | `StorageQueueLogs` (7 days) holds only GetQueueMetadata (42061), CreateQueue (12), GetQueueServiceProperties (6) and ListQueues (4); zero `PutMessage`, so the poison candidate query returns 0 and cannot be shown to work. A throwaway account was meant to check the `ObjectKey` shape; its public network access could not be enabled (policy kept it Disabled), the put was rejected with AuthorizationFailure, and the account was deleted |

## Result per unticked criterion

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest and IoT Hub ingestion | Partly proven, unproven as a whole | Ledger digest installed, enabled and previously fired Sev1. Job, poison and IoT rules exist but are disabled pending named-human approval; no firing or notification was observed; poison `PutMessage` shape unverified (no such logs exist) |
| Dashboard or workbook shows availability, errors, latency and cost against budget | Partly proven, unproven as a whole | Workbook installed and its cost, AI usage, AI variance (after fix) and limit tiles execute with real results. Availability, errors and latency have no data because Application Insights is not workspace-based. No Portal render was captured; the fixed workbook is not redeployed (production change excluded) |
| Each alert has a runbook entry with an owner | Unproven | Test-enforced runbook entries name proposed roles; appointing named people is a human decision |
| Tokenomics: metered AI usage by capability beside the Azure cost record, variance visible | Proven for the demo (app, 2026-11-18) and now by query | The workbook tiles show usage by capability with the Azure cost record Unknown and variance "Unreconciled, not zero". A real Azure cost record is excluded by owner decision, so the "beside the Azure cost record" half shows Unknown only |

No box is ticked by this note.

## Source change

* `infra/monitoring-workbook.json`: the `ai-variance-by-period` extend is split into two so it runs on Log Analytics.
* `infra/tests/test_ai_observability_workbook_budget.py`: new test that fails on the old query; 20 workbook tests pass.

Tier: focused (infra JSON and tests; no `src`, permission, secret or control change). Hosted CI for the exact head is not observed here.
