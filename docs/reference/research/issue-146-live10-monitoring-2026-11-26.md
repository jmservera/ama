---
title: Issue 146 monitoring criteria, live10 pass (2026-11-26)
description: Read-only live inventory of alerts, workbook query execution and per-criterion proven or unproven result for the synthetic demo
ms.date: 2026-11-26
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-26 about 11:07 UTC. Every Azure call was read-only; no resource was created or changed, so nothing needed deleting. No drill, rotation, deployment or credential read. Earlier passes: [live7](./issue-146-live7-monitoring-2026-11-23.md), [live9](./issue-146-live9-monitoring-2026-11-25.md).

## Observations

| Check | Result |
| --- | --- |
| `monitoring_live_inventory.py` on `az monitor metrics alert list`, `scheduled-query list` and `containerapp job list` | job_failure partial (enabled for `job-cutover-test-demo-audit`, `-load`, `-orch` and `job-live-receiver`; none for `job-184-bodyscan`, `job-live-simulator`); poison_queue enabled; ledger_digest enabled (4 rules); iot_ingestion enabled (4 rules); firing never observed. Live9 recorded poison, IoT and jobs disabled, so the estate changed since |
| Notification route | all 22 rules have one action group `ag-cutover-test-ops`, which has one email receiver (address not printed) |
| Owner and runbook in rule description | 18 of 22 carry both; `alert-cutover-test-api-5xx`, `-api-restarts`, `-ledger-digest-mismatch` and `-ledger-verify-missing` do not, and the api pair targets `ca-cutover-test-api`, which no longer exists |
| Deployed workbook (`az rest` with `canFetchContent`) | every source tile name present, modified 2026-11-26 09:09 UTC |
| Workbook queries over 7 days, workspace `log-cutover-test` | all eight execute, exit code 0: ingress 170529 requests, 1449 server errors, p95 4509 ms; AppRequests and AppAvailabilityResults 0 rows (Insufficient); cost Unknown and Unreconciled; AI usage 75 attributed calls; 3 AI limit breach rows with owner and runbook |
| Poison alert query | `StorageQueueLogs` has 13 `PutMessage` rows in 7 days, none on `agent-tasks-poison`, so the query is valid and does not match |

Not done: Portal rendering (the Portal needs an interactive Azure sign-in; the test-user credentials are application sign-ins and were not used for it), notification delivery and any firing drill (not authorised).

## Change

Documentation only: `infra/monitoring-runbooks.md` described the job, IoT, poison and AI rules as disabled candidates; it now states that they are enabled in the demo estate and links this note. No src, Bicep or workflow file changed (focused tier).

## Result per unticked criterion

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest and IoT ingestion | Partly proven, unproven as a whole | Installed and enabled for all four classes, each with an action group. Two of six jobs have no failure rule, so job coverage is partial. No firing or delivered notification observed; drills are not authorised |
| Dashboard or workbook shows availability, errors, latency and cost against budget | Partly proven, unproven as a whole | Deployed workbook matches source and every query executes. Errors and latency return real ingress data. Availability has 0 rows (no availability tests). Cost shows Unknown by design (billing reconciliation excluded). No Portal render |
| Each alert has a runbook entry with an owner | Unproven | 18 of 22 descriptions name a proposed role and runbook anchor; four legacy rules lack both. No person is named (human decision) |
| Tokenomics: metered AI usage beside the Azure cost record, variance visible | Proven for the demo | Executed live today: 75 attributed calls by capability, cost record Unknown, variance shown as unreconciled, not zero |

Follow-ups for the owner: add failure alerts for `job-184-bodyscan` and `job-live-simulator` or record them as exempt; delete or redeploy the four legacy rules (a production change, not made). No box is ticked by this note.
