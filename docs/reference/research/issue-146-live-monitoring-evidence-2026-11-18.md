---
title: Issue 146 live monitoring evidence (demo, 2026-11-18)
description: Per-criterion live Azure evidence for the unticked monitoring criteria of issue 146 on the synthetic demo resource group ama
ms.date: 2026-11-18
---

Scope: synthetic demo, resource group `ama`, existing Azure CLI login. Owner decisions of 2026-11-18 apply (no drills, no Key Vault rotation, no production change, billing reconciliation, DPO/Legal approval and person-run assistive-technology testing out of scope). No secrets recorded. Source files were not changed; throwaway resources were named `tmp146-*` and deleted.

## Starting live inventory (read-only)

* Metric alerts: Foundry throttle, SQL CPU, API 5xx, API restarts.
* Scheduled-query alerts: ledger digest mismatch, ledger verify missing, Key Vault secret expiry and denied access.
* Action group `ag-cutover-test-ops` with one enabled email receiver (address not recorded).
* Budgets `budget-forward-test` and `budget-cutover-test` (300, current spend 84.47 at query time) and `budget-iot-cutover-test-rzsrg` (25, spend 5.16).
* No job-failure, poison-queue or IoT alert and no workbook existed. Storage account diagnostic setting `to-log-analytics` has no enabled log category, so `StorageQueueLogs` is not collected.

## Criterion 1: alerts cover job failures, poison queue, ledger digest, IoT ingestion

* Ledger digest: proven installed. `alert-cutover-test-ledger-digest-mismatch` is enabled and, per Alerts Management, fired Sev1 at 2026-11-18T08:18:52Z (state New). This is a live signal that the demo ledger digest check currently reports a mismatch; it was not investigated here and is recorded as an adverse finding for the owner.
* Job failures: signal proven, rule proven creatable. Metric `Executions` on `job-cutover-test-ledger-verify` has dimension `state` and showed Failed 11, Running 6, Succeeded 6 over three days. Rule `tmp146-job-ledger-verify-failed` (Max Executions > 0, state Failed, PT15M window, PT5M frequency, action group attached) was created enabled and deleted. It did not fire during the window because no failure occurred in it.
* IoT ingestion: rule creatable. `d2c.telemetry.ingress.sendThrottle` is listed by the IoT Hub metric definitions; the rule `tmp146-iot-ingress-throttle` was created through REST (the CLI rejected the dotted metric name) and deleted. No firing was provoked.
* Poison queue: UNPROVEN. The storage account has no queue log category enabled and its network rules block this client, so no poison message can be created or observed; enabling storage diagnostics is an infrastructure change outside the demo remit.
* Result: partly proven (digest installed and firing; job-failure and IoT rules creatable with a real signal); the permanent installation of job, IoT and poison alerts is not done because source defaults them disabled pending named-human approval.

## Criterion 2: dashboard or workbook shows availability, errors, latency, cost against budget

* Workbook `infra/monitoring-workbook.json` (placeholders replaced for the demo workspace, Application Insights and `budget-cutover-test`) was deployed as shared workbook `tmp146 operations workbook` and deleted. The ARM write succeeded and the serialized data parsed to 12 items including requests, availability, cost-vs-budget, errors and latency panels.
* Rendering UNPROVEN. Workspace and Application Insights have `publicNetworkAccessForQuery` Disabled (private link scope), so all seven workbook queries run from this host returned `InsufficientAccessError`. Enabling public query is a security-control change and was not made. Portal rendering from the private network is not available to this session.
* Cost panel remains Unknown/unreconciled by design; billing reconciliation is out of scope for the demo.

## Criterion 3: each alert has a runbook entry with an owner

* `infra/monitoring-runbooks.md` has 20 "Proposed owner" entries covering existing, job, IoT, poison and AI alerts; `infra/tests` coverage and ownership tests pass (21 tests OK).
* Owners are proposed roles ("Digital service owner" and others, appointment pending), not named humans. Naming actual people is a human appointment; not proven.

## Criterion 4 (Tokenomics): dashboard shows metered AI usage by capability beside Azure cost with unreconciled variance

* Panels `ai-usage-by-capability`, `ai-variance-by-period` and `cost-vs-budget` exist in the deployed workbook. Same rendering limit as criterion 2; UNPROVEN live. No Azure cost export table was provisioned, so variance would display unreconciled.

## Test alert

Throwaway scheduled-query rule `tmp146-test-fire` (always-true `print x=1`, severity 4, existing action group) was created and fired at 2026-11-18T08:28:37Z (Alerts Management: Sev4, Fired, New). Email delivery was not independently observed.

## Cleanup

All four `tmp146` resources deleted; `az resource list -g ama` shows no `tmp146` names and the workbook list is empty. Query-and-IoT alert states of pre-existing alerts were not modified.
