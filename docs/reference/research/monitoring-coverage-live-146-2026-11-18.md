---
title: Live monitoring coverage check on the demo (issue 146)
description: Read-only Azure Monitor evidence for each unticked acceptance criterion of issue 146, with proven and unproven status
ms.date: 2026-11-18
ms.topic: reference
---

Refs #146. Scope is the synthetic demo in resource group `ama`, desktop only, run on 2026-11-18 under the owner decisions of that date. Every Azure command was a read (`list`, `show`, `metrics list`); no resource was created, changed or deleted, and no drill ran. Subscription ids are omitted. No credentials were read or printed.

## Result

| Criterion | Status | Evidence |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest verification and IoT Hub ingestion | Partly observed. Ledger digest observed installed; raw output not retained. Job failure, poison queue and IoT not installed | Sections 1 to 3 |
| A dashboard or workbook shows availability, errors, latency and cost against the budget | Unproven: no workbook or dashboard exists on the demo | Section 4 |
| Each alert has a runbook entry with an owner | Observed in source for the 8 installed alerts, 4 budget notifications and the disabled candidates; the owner is a proposed role, not an appointed person | Section 5 |
| Tokenomics: dashboard of metered AI usage by capability beside the Azure cost record | Unproven: no dashboard installed; cost variance cannot be read | Section 4 |

The four ticked criteria (diagnostic logs exclude personal data, the RAI harm monitoring set, AI limit alerts naming an owner, budget notification documented as not a hard cap) were not re-opened.

## 1. Installed alerts (az monitor)

| Rule | Type | Severity | Enabled | Action group |
| --- | --- | --- | --- | --- |
| alert-cutover-test-foundry-throttle | metric | 2 | yes | ag-cutover-test-ops |
| alert-cutover-test-sql-cpu | metric | 3 | yes | ag-cutover-test-ops |
| alert-cutover-test-api-5xx | metric | 2 | yes | ag-cutover-test-ops |
| alert-cutover-test-api-restarts | metric | 3 | yes | ag-cutover-test-ops |
| alert-cutover-test-ledger-digest-mismatch | scheduled query, hourly, 1 hour window | 1 | yes | ag-cutover-test-ops |
| alert-cutover-test-ledger-verify-missing | scheduled query, hourly, 1 day window | 1 | yes | ag-cutover-test-ops |
| alert-kv-cutovertest-rzsrg-secret-expiry | scheduled query | 2 | yes | not read |
| alert-kv-cutovertest-rzsrg-denied-access | scheduled query | 3 | yes | not read |

Activity log alerts: none. The action group `ag-cutover-test-ops` has one email receiver (`operations`) and no webhook, so no Teams route is installed. Mail delivery is not observable from this run (see the digest note, `digest-verification-alert-live-2026-11-18.md`).

## 2. Per criterion 1 findings

* Ledger digest verification: both the mismatch and the missing-run rules are installed and enabled. A forced mismatch fired the mismatch rule on 2026-11-18 (see the digest note). Observed; raw output not retained.
* Job failures: no rule on `Microsoft.App/jobs` `Executions` with state `Failed`. The metric exists on the ledger-verify job and carries a `Failed` series, and the job list shows failed executions earlier today (08:00 and 08:02 UTC), so the signal is real but nothing alerts on it. The repository defines disabled candidates in `infra/modules/operationalMonitoring.bicep` (`alert-<job>-failed`, gated by `candidateAlertsEnabled`); none is deployed. Observed; raw output not retained. Not installed.
* Poison queue: the candidate `alert-<prefix>-agent-tasks-poison` is a scheduled query on `StorageQueueLogs`. It is not deployed. The queue service of `stcutovertestrzsrg` has no diagnostic setting, so that table receives nothing and the rule could not fire if installed. The storage account denies public access, so the queue list could not be read from this host. Observed; raw output not retained.
* IoT Hub ingestion: `iot-cutover-test-rzsrg` exposes `d2c.telemetry.ingress.success` (totals 12, 18 and 6 in the last three hourly buckets), `ingress.sendThrottle`, `egress.dropped`, `egress.invalid` and `egress.orphaned`, so the signals exist and traffic flows. No IoT alert is deployed; the four candidates stay disabled in source. Observed; raw output not retained.

Installing the missing rules needs a Bicep deployment under the infrastructure FULL tier, an approval reference and named owners (the candidates stay off without them). That is a production-style change outside this run's authority, so the gap is reported, not closed.

## 3. Log access limit

The Log Analytics workspace `log-cutover-test` has query access disabled for the public network, and a query from this host returned `InsufficientAccessError` (`NspValidationFailedError`). Application Insights also disables public query and ingestion. KQL results and portal rendering were therefore not observed; the findings above come from the control plane and metrics APIs only. The Container Apps environment sends logs to `azure-monitor`.

## 4. Workbook, dashboard and cost

* `az resource list --resource-type microsoft.insights/workbooks` returned nothing; `az portal dashboard list` returned nothing. The source workbook `infra/monitoring-workbook.json` and its offline checks exist but are not installed on the demo. Browser proof is not applicable: there is nothing to open, and the portal sits behind a sign-in outside the test users.
* Budget `budget-forward-test`: monthly, USD 300, start 2026-10-01, notifications `actual80` (80 percent actual) and `forecast100` (greater than 100 percent), contact `<alert-address>`. Current spend read as USD 90.61. The recipient is a placeholder address, so notification delivery is not proven; it is a notification, not a hard cap (matching the runbook text).
* Billing reconciliation is out of scope by owner decision, so the "unreconciled variance visible" part cannot be shown.

## 5. Runbook entries and owners

`infra/monitoring-runbooks.md` has a section for every installed alert (Foundry, SQL CPU, API errors, API restarts, ledger mismatch, ledger missing, vault expiry, vault denied), the four budget notifications, five disabled job candidates and the IoT candidates. Each names a proposed owner (Digital service owner, Finance budget owner, with Compliance/Legal for the digest). The file states these are proposed roles and that actual primary and backup appointments are still to be recorded. So the entry exists; a named human owner does not, and this run cannot appoint one.

## Unmet criteria

All three unticked infrastructure criteria and the Tokenomics dashboard criterion stay unticked. Missing for the demo: deployed job-failure, poison queue and IoT alerts; queue diagnostic setting; an installed workbook; named owners.
