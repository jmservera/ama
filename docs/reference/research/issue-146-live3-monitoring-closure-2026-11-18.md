---
title: Issue 146 monitoring closure re-verification, live demo (2026-11-18)
description: Fresh live check of the open acceptance criteria of issue 146 on the synthetic demo, with retained raw output, Playwright screenshots and a proven or unproven result per criterion
ms.date: 2026-11-18
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-18 16:57 to 17:10 UTC. Azure calls were read-only except for observing and then deleting three throwaway alert rules and one throwaway job left by an earlier stalled worker. No drill, no Key Vault rotation, no production change, no source change. Credentials were read at run time and never printed; a literal scan of the retained text and JSON files for both credential values found no match. Subscription id and email addresses are not retained.

Raw output and scripts: [issue-146-live3-evidence-2026-11-18/](./issue-146-live3-evidence-2026-11-18/). Earlier passes: [first](./issue-146-live-monitoring-evidence-2026-11-18.md), [re-run](./issue-146-live-monitoring-rerun-2026-11-18.md), [second](./issue-146-live2-monitoring-evidence-2026-11-18.md), [coverage check](./monitoring-coverage-live-146-2026-11-18.md).

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Installed metric alerts | Foundry throttle (Sev2), SQL CPU (Sev3), API 5xx (Sev2), API restarts (Sev3), enabled; three `tmp146` throwaways from the earlier worker also present | [metric-alerts.json](./issue-146-live3-evidence-2026-11-18/metric-alerts.json) |
| Installed scheduled-query alerts | Key Vault secret expiry (Sev2), Key Vault denied access (Sev3), ledger digest mismatch (Sev1), ledger verify missing (Sev1), all enabled | [scheduled-query-alerts.json](./issue-146-live3-evidence-2026-11-18/scheduled-query-alerts.json) |
| Action group, activity-log alerts, workbooks | `ag-cutover-test-ops` with 1 email receiver and no webhook; no activity-log alert; no workbook | [action-groups.json](./issue-146-live3-evidence-2026-11-18/action-groups.json), [activity-log-alerts.json](./issue-146-live3-evidence-2026-11-18/activity-log-alerts.json), [workbooks.json](./issue-146-live3-evidence-2026-11-18/workbooks.json) |
| Fired alerts, 1 day | Ledger digest mismatch Sev1 fired 08:18Z then resolved; `tmp146c` (Total shape) fired 10:17Z; `tmp146e` (Total shape) fired 16:50Z; no other source-shape job alert fired | [fired-1d.json](./issue-146-live3-evidence-2026-11-18/fired-1d.json) |
| Job-failure rule shapes on fresh failures | A throwaway job running `/bin/false` failed at 16:35Z and 16:48Z. Rule `tmp146d` (Maximum, PT15M, PT5M, `state=Failed`, the shape in `infra/modules/operationalMonitoring.bicep`) did not fire, and `tmp146f` (Maximum, PT1H) had not fired after 16 minutes. `tmp146e` (Total, PT15M) fired within about 2 minutes. The metric itself showed the Failed series at 16:36 to 16:38 and 16:49 to 16:52 | [throwaway-rule-shapes.json](./issue-146-live3-evidence-2026-11-18/throwaway-rule-shapes.json), [failjob-executions-metric.txt](./issue-146-live3-evidence-2026-11-18/failjob-executions-metric.txt) |
| Throwaway cleanup | Three rules and the job deleted at about 17:05Z; `az resource list` shows no `tmp146` name | [post-cleanup-tmp146.json](./issue-146-live3-evidence-2026-11-18/post-cleanup-tmp146.json), [cleanup-at.txt](./issue-146-live3-evidence-2026-11-18/cleanup-at.txt) |
| Storage queue diagnostics | The queue service now has a `to-log-analytics` setting with the `audit` category group enabled. This differs from the earlier note, which found none | [storage-queue-diagnostics.json](./issue-146-live3-evidence-2026-11-18/storage-queue-diagnostics.json) |
| IoT Hub ingestion signal | `d2c.telemetry.ingress.success` totals by hour: 21 (12Z), 15 (13Z), then 0 for 14Z to 16Z. The signal exists; no IoT alert is installed | [iot-ingress-success.json](./issue-146-live3-evidence-2026-11-18/iot-ingress-success.json) |
| AI usage by capability in the app (Playwright, employee test account, role Retrofit Programme Manager, 1366 by 900) | `/api/ai/report` returned 200 with `coverage` incomplete, `reconciliation` unreconciled, `total_cost_of_ai` Unknown, 16 calls, 1 failure, one capability (`chat-case-conversation`, 17833 tokens). The Asset and board view with a selected home shows "Metered usage by AI capability", "Reconciliation with the bill: Action needed: unreconciled" and "Total Cost of AI: State: Unknown", plus 30 owned held-call alerts | [ai-usage-proof.json](./issue-146-live3-evidence-2026-11-18/ai-usage-proof.json), `asset-usage-by-capability.png` (removed in review because it showed names), `asset-usage-reconciliation.png` (removed in review because it showed names), [ai_usage_proof.py](./issue-146-live3-evidence-2026-11-18/ai_usage_proof.py) |
| Offline monitoring tests | 61 tests across the ten monitoring, runbook, workbook and privacy test modules pass | [infra-offline-tests.txt](./issue-146-live3-evidence-2026-11-18/infra-offline-tests.txt) |

The first Playwright run showed only the landing page and a second run found no usage text; the panel appears only for the Asset and board view with a selected home (`#/screens?screen=asset-board&case=<id>`). The scripted attempts are the retained history of that discovery.

## Result per unticked criterion

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest verification and IoT Hub ingestion | Partly proven; not closable on the demo | Ledger digest: installed, enabled, Sev1 fired and resolved. Job failures: no permanent rule is installed; the Total shape fires on a real failure, and the source Maximum shape did not fire on two fresh failures, so the disabled source candidate is likely wrong and needs a Bicep fix under the FULL tier. Poison queue: no alert installed, and with KQL query access private only the `StorageQueueLogs` signal cannot be read, so it stays unproven. IoT: signal exists and carried traffic, no alert installed. Installing permanent rules is an infrastructure change outside this run, and the candidates stay disabled in source pending named-human approval |
| A dashboard or workbook shows availability, errors, latency and cost against the budget | Unproven | No workbook is installed on the demo. Workspace and Application Insights query access is private-link only, so a render cannot be observed from this host. Enabling public query would weaken a security control |
| Each alert has a runbook entry with an owner | Unproven as written | Runbook entries exist in source and offline tests pass, but the owners are proposed roles; appointing named people is a human decision outside the demo |
| Tokenomics: dashboard of metered AI usage by capability beside the Azure cost record, with unreconciled variance visible | Proven for the demo, with one limit | The deployed app shows metered usage by capability and the reconciliation state "unreconciled" with Total Cost of AI Unknown (observed in the app; screenshots deleted because they showed staff and resident names). It does not show an Azure cost record beside it; Azure billing reconciliation is out of scope for the demo by owner decision, so the Azure cost half is not proven |

Ticked criteria (diagnostic log privacy, RAI harm monitoring, AI limit alert ownership, budget notification wording) were not re-opened. No criterion is ticked by this note.

## Limits and follow-ups

* Email delivery of any fired alert was not observed.
* The three `tmp146` rules and the job existed when this run began; they belonged to the earlier stalled worker and were deleted here after their state was recorded.
* Follow-up for the FULL tier: change the source job-failure candidate aggregation from Maximum to Total and re-test on a fresh failure; verify `StorageQueueLogs` content for the poison candidate.
* Independent review and hosted CI remain outstanding.
