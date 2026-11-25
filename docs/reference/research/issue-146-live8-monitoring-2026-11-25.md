---
title: Issue 146 monitoring criteria, live pass (2026-11-25)
description: Live observation of installed alerts, the deployed workbook, workspace queries and a poison-queue provocation attempt for the unticked acceptance criteria of issue 146, with a proven or unproven result per criterion
ms.date: 2026-11-25
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-25 14:19 to 14:35 UTC. No drill, no Key Vault rotation, no credential read, no production change. Earlier pass: [2026-11-23 ingress pass](./issue-146-live7-monitoring-2026-11-23.md). No source change was needed or made.

## Observations

| Check | Result |
| --- | --- |
| Metric alerts (`az monitor metrics alert list -g ama`) | Enabled: Foundry throttle, SQL CPU, API 5xx and restarts for the legacy and the demo API (six rules). Installed but disabled: job failure for `demo-audit`, `demo-orch`, `demo-load`; IoT ingress throttle, routing dropped, invalid, orphaned. Job rules use `Executions`, dimension `state=Failed`, aggregation Total, window PT15M |
| Scheduled-query alerts | Enabled: Key Vault expiry and denied access, ledger digest mismatch and verify missing (legacy and demo, four rules). Disabled: `alert-cutover-test-ai-limits`, `alert-cutover-test-agent-tasks-poison` |
| Workbook | One shared workbook installed (modified 2026-11-21) with 12 items; source `infra/monitoring-workbook.json` has 14. The deployed copy lacks `edge-caveat` and `edge-requests` |
| Workbook from current source | A throwaway workbook built from the source JSON (placeholders substituted) saved with 14 items and was deleted |
| Workspace `log-cutover-test` | Query access Enabled; `AppRequests`, `AppAvailabilityResults`, `AppTraces` hold 0 rows over 30 days |
| Source workbook queries executed live (30-day window) | All eight tiles return rows. `edge-requests`: 226412 ingress rows, 223674 with a response, 2408 status 500 or above (1.08 percent), 2738 client-aborted, p95 2726 ms, 2 apps. `cost-vs-budget`: configured 300 USD, Azure actual and forecast "Unknown", variance "Unreconciled". `ai-usage-by-capability`: `chat-case-conversation`, 40 metered calls, 37575 tokens, cost record "Unknown (billing record not connected)". `ai-variance-by-period`: 2026-11, 0 Azure cost rows, "Unreconciled, not zero". `ai-limit-breaches`: 79 `call-budget-limit` and 30 `liability-unknown` holds, each row naming an owner role and runbook anchor |
| `StorageQueueLogs` | 174904 rows in 30 days, so queue diagnostics now flow. Operations seen: `GetQueueMetadata`, `CreateQueue`, `PutMessage` (only `AuthorizationFailure`), `ListQueues`. The disabled poison rule query executes without error and returns 0 matching `PutMessage` successes on `/agent-tasks-poison/` |
| Job failures in the last 24 hours | `job-live-receiver` 8 Failed of 2742 executions; demo jobs 0 Failed. No failure alert is installed for `job-live-receiver` (its Bicep creates one only when `failureAlertActionGroupId` is set at deployment) |
| Runbook links in alert descriptions | 17 of 21 alerts carry a runbook anchor and an owner statement, including every demo-environment alert. The four legacy-environment alerts (`alert-cutover-test-api-5xx`, `-api-restarts`, `-ledger-digest-mismatch`, `-ledger-verify-missing`) have no description, a deployment drift from the source template that the demo alerts do not show |
| Subscription budget | `az consumption budget list` now succeeds: `FDPOAzureBudget` 750 USD monthly, current spend 449.21 USD, notifications at 80 percent actual and 125 percent. It is the owner's subscription budget, not the `budget-cutover-test` the workbook references |

## Poison-queue provocation attempt

A throwaway scheduled-query rule `tmp146p-poison` (the poison rule, enabled, 5-minute frequency, same action group) and a throwaway storage account `sttmp146poison` with queue diagnostics were created. Writing a probe message failed on this host: the policy-controlled account kept public network access Disabled and shared-key authentication refused, and the existing storage account denies data-plane writes to this login (no Queue Data role). Weakening either control to force the test would breach the "no production change" boundary, so the poison firing path was not exercised. All three throwaway resources (rule, diagnostic setting, account with its scoped role) were deleted; `az resource list -g ama` and the scheduled-query list show no `tmp146` name.

## Per-criterion result

| Criterion | Result | Evidence and reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest and IoT ingestion | Unproven as a whole | Ledger digest: proven installed and enabled, and fired in the [2026-11-18 test](./digest-verification-alert-live-2026-11-18.md). Job failures: rules installed with the Total shape that fired on a throwaway on 2026-11-18, but disabled; `job-live-receiver` has real failures and no installed rule. IoT: installed, disabled, never fired. Poison: query now valid on live queue logs, rule disabled, firing not provoked. Enabling the disabled rules needs named-human approval recorded in `approvalReference` |
| Dashboard or workbook shows availability, errors, latency and cost against the budget | Partly proven | Errors and latency: source tile returns real ingress data, executed live; it is not in the deployed workbook (12 of 14 items). Availability: no availability tests exist (0 rows), so the tile reports Insufficient. Cost against budget: renders Unknown and Unreconciled, because no Azure cost export is ingested. No Portal render was captured: Portal sign-in is outside the CLI login and the tiles were verified by executing their queries |
| Each alert has a runbook entry with an owner | Unproven | Test-enforced entries and the demo alerts name a runbook and a proposed owner role; four legacy alerts have no description; no person is named, which is a human decision |
| Tokenomics: metered AI usage by capability and period beside the Azure cost record, unreconciled variance visible | Proven for the demo | Live query output above shows usage by capability and period, the cost record as Unknown and variance as "Unreconciled, not zero". A real billing record is excluded by owner decision |

No box is ticked by this note.

## Follow-ups outside this run

* Redeploy the workbook from source so the deployed copy carries the ingress tile (monitoring deployment, not run here).
* Decide whether to install a failure alert for `job-live-receiver` (set `failureAlertActionGroupId`) and enable the candidate rules once owners approve.
* Refresh the four legacy alert descriptions or retire that environment's alerts.
