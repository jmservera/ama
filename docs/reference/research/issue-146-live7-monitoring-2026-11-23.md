---
title: Issue 146 ingress availability, errors and latency tile (2026-11-23)
description: Live read-only observation that Application Insights tables hold no rows, a new workbook tile on Container Apps ingress logs that does return data, and a proven or unproven result per unticked criterion
ms.date: 2026-11-23
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-23 about 21:50 UTC. Every Azure call was read-only; nothing was created, so nothing needed deleting. No drill, Key Vault rotation, deployment or credential read. Earlier pass: [2026-11-23 query execution](./issue-146-live6-monitoring-2026-11-23.md).

## Observations

| Check | Result |
| --- | --- |
| `monitoring_live_inventory.py` on live `az monitor metrics alert list` and `scheduled-query list` | ledger_digest enabled; job_failure, poison_queue, iot_ingestion installed but disabled; coverage partial |
| Workspace `log-cutover-test` | Query access Enabled, ingestion Disabled; all eight workbook queries execute (exit code 0) |
| `appi-cutover-test` | Now Log Analytics mode and linked to the workspace (earlier passes found it unlinked), query access Disabled |
| `AppRequests`, `AppAvailabilityResults`, `AppTraces` (workspace) | 0 rows each, so the existing availability, errors and latency tiles can only return Insufficient |
| `ContainerAppHTTPLogs` (7 days) | 134784 rows; 133536 with a response; 1036 with status 500 or above; 1248 status 0 (`downstream_remote_disconnect`, `http2.remote_reset`, `too_many_premature_resets`); p95 about 1.9 s; 2 apps |

## Defect and change

The workbook claimed availability, errors and latency coverage but read only Application Insights tables that hold no data in this estate, while the Container Apps ingress table held real signal. New tile `edge-requests` (with the `edge-caveat` text) in `infra/monitoring-workbook.json` summarises ingress requests, server errors, client-aborted connections and p95 duration. It projects only time, app name, status and duration. Live execution found two typing faults before the final form: `RequestDuration` is `long`, and `percentile` over a long returns long, so it is converted with `todouble`. Live results on the 7-day window: Status "Observed ingress rows; not SLO acceptance", Requests 133536, ServerErrors 1036, ServerErrorPercent 0.78, NonServerErrorPercent 99.22, ClientAborted 1248, InvalidRows 0. An empty window returns Status Insufficient with null percentages (verified live). Not redeployed: the workbook change is source only, since a production change is excluded.

Tests: `infra/tests/test_monitoring_workbook.py` gains one case (stub shape, columns, no path, user agent or address, Insufficient). 41 monitoring tests and 5 AI observability tests and 7 diagnostic privacy tests pass; `ruff check` and `ruff format --isolated --line-length 100` clean on the changed test; `az bicep build` of `operationalMonitoring.bicep` succeeds. Focused tier: infra JSON and test only, no `src`, permission, secret, control or gate change. Hosted CI for the exact head is not observed.

## Result per unticked criterion

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest and IoT ingestion | Unproven (partial) | Ledger digest proven installed and enabled. Job, poison and IoT rules are installed but disabled; enabling is a production change outside the authorisation. No firing or notification drill is permitted; poison has no `PutMessage` log rows to prove the query |
| Dashboard or workbook shows availability, errors, latency and cost against budget | Partly proven, unproven as a whole | Errors and latency now have a tile whose query returns real ingress data (executed live). Availability tests do not exist (0 rows). Cost against budget shows Unknown/unreconciled by design; billing reconciliation is excluded. No Portal render captured and the new tile is not deployed |
| Each alert has a runbook entry with an owner | Unproven | Test-enforced entries name proposed roles; naming a person is a human decision |
| Tokenomics: metered AI usage beside the Azure cost record, variance visible | Proven for the demo | Workbook queries executed live today: 16 metered calls, cost record Unknown, variance "Unreconciled, not zero". Real billing record excluded by owner decision |

No box is ticked by this note.
