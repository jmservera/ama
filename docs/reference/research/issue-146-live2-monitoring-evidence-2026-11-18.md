---
title: Issue 146 monitoring coverage, second live pass (demo, 2026-11-18)
description: Read-only Azure inventory of installed alerts, dashboards and runbooks for the demo with retained raw output and a per-criterion result for issue 146
ms.date: 2026-11-18
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login. Every Azure call in this pass was read-only. No drill, no rotation, no production change, no source change, and no resource was created. Subscription id and email addresses are redacted in the raw files. Earlier runs: [first run](./issue-146-live-monitoring-evidence-2026-11-18.md) and [re-run](./issue-146-live-monitoring-rerun-2026-11-18.md). This pass retains raw output those notes lacked.

Raw output is in [issue-146-live2-evidence-2026-11-18/](./issue-146-live2-evidence-2026-11-18/), captured about 12:35Z.

## What exists in the demo

| Item | Installed now | Raw output (retained) |
| --- | --- | --- |
| Metric alerts | Foundry throttle (Sev2), SQL CPU (Sev3), API 5xx (Sev2), API restarts (Sev3), all enabled | [metric-alerts.json](./issue-146-live2-evidence-2026-11-18/metric-alerts.json) |
| Scheduled-query alerts | Key Vault secret expiry (Sev2), Key Vault denied access (Sev3), ledger digest mismatch (Sev1), ledger verify missing (Sev1), all enabled | [scheduled-query-alerts.json](./issue-146-live2-evidence-2026-11-18/scheduled-query-alerts.json) |
| Action group | `ag-cutover-test-ops` | [action-groups.json](./issue-146-live2-evidence-2026-11-18/action-groups.json) |
| Workbooks | none | [workbooks.json](./issue-146-live2-evidence-2026-11-18/workbooks.json) |
| Resource list | full list; no `tmp146` names | [resources.json](./issue-146-live2-evidence-2026-11-18/resources.json), [tmp146-check.json](./issue-146-live2-evidence-2026-11-18/tmp146-check.json) |
| Fired alerts, 7 days | summary of Alerts Management records | [fired-alerts-7d.json](./issue-146-live2-evidence-2026-11-18/fired-alerts-7d.json) |
| Job `Executions` by state, 12 h | Failed 11, Running 6, Succeeded 6 | [job-executions-by-state-12h.json](./issue-146-live2-evidence-2026-11-18/job-executions-by-state-12h.json) |
| Query access | Log Analytics and Application Insights: public query Disabled | [workspace-query-access.txt](./issue-146-live2-evidence-2026-11-18/workspace-query-access.txt) |
| Offline tests | 28 alert tests and 24 runbook, workbook and privacy tests pass | [infra-offline-tests.txt](./issue-146-live2-evidence-2026-11-18/infra-offline-tests.txt) |

Source runbooks: `infra/monitoring-runbooks.md` holds 20 "Proposed owner" entries (counted with grep, not retained as a file). Source workbook: `infra/monitoring-workbook.json`.

Budgets: `az consumption budget list` returned `budget-forward-test` and `budget-cutover-test` at 300 (monthly) this pass; that output was viewed but not retained.

## Result per unticked criterion

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest, IoT ingestion | Partly proven | Digest alert installed, enabled and Sev1 fired 08:18Z then resolved (retained). A job-failure metric rule fired Sev3 at 10:17Z on the ledger-verify job; the fired record is retained, the throwaway rule `tmp146c-job-failed` was deleted by the earlier run, so only history remains. IoT Hub exposes `d2c.telemetry.ingress.sendThrottle` but no IoT alert is installed. Poison queue is unproven: the storage account has no queue log category and diagnostics cannot be enabled without an infrastructure change. Permanent job, IoT and poison alerts stay disabled in source pending named-human approval |
| Dashboard or workbook shows availability, errors, latency, cost against budget | Unproven | No workbook is installed, and query access is private-link only, so no render is possible from this host. Enabling public query would weaken a security control |
| Each alert has a runbook entry with an owner | Partly proven | Entries and offline tests exist; owners are proposed roles, and naming people is a human appointment |
| Tokenomics: AI usage by capability beside Azure cost, variance visible | Unproven | Panels exist in workbook source only; no render and no cost export table. Billing reconciliation is out of scope for the demo |

## Limits

* The ledger digest alert fire came from the forced-mismatch test in [digest-verification-alert-live-2026-11-18.md](./digest-verification-alert-live-2026-11-18.md), not a tamper.
* Email delivery was not observed.
* No Playwright or Portal screenshot was taken; no signed-in surface shows these resources to this session.
* No criterion is ticked. Independent review and hosted CI remain outstanding.
