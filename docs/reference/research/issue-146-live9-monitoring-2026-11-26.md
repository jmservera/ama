---
title: Issue 146 monitoring criteria, live pass (2026-11-26)
description: Live activation of the demo monitoring candidates, a new receiver failure alert, the redeployed operations workbook and a per-criterion result for the unticked acceptance criteria of issue 146
ms.date: 2026-11-26
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-26 09:05 to 09:15 UTC, under the owner decisions of 2026-11-18 (demo needs no billing reconciliation, DPO/Legal approval or person-run assistive-technology testing). No drill, no Key Vault rotation, no credential read. Earlier pass: [2026-11-25](./issue-146-live8-monitoring-2026-11-25.md). This note is the dated activation reference named by `monitoringApprovalReference` in `infra/main.test.bicepparam`; it is a demo activation record, not a production approval or a named appointment of owners.

## Live changes made

| Change | Command shape | Result |
| --- | --- | --- |
| Enable job failure rules for `demo-audit`, `demo-orch`, `demo-load` | `az monitor metrics alert update --enabled true` | `enabled` True for all three |
| Enable IoT ingress throttle, routing dropped, invalid, orphaned rules | same | all four True |
| Enable poison-queue and AI-limit rules | `az monitor scheduled-query update --disabled false` | both True |
| Create `alert-job-live-receiver-failed` (Executions, state Failed, Total above 0, PT15M window, PT5M frequency, severity 2, action group `ag-cutover-test-ops`, owner and runbook anchor `job-live-receiver` in the description) | `az monitor metrics alert create` | created, enabled; same shape as the source in `infra/live-receiver-job.bicep` |
| Redeploy the shared workbook from `infra/monitoring-workbook.json` with placeholders substituted | `az rest --method put` on the existing workbook | read back 14 items including `edge-caveat`, `edge-requests`, `cost-vs-budget`, `ai-usage-by-capability` (was 12) |

Final listing after the changes: 14 metric alerts all enabled (including the receiver rule) and 8 scheduled-query rules enabled (ledger digest mismatch and verify-missing for both environments, Key Vault expiry and denied access, poison, AI limits).

## Source change

`infra/main.test.bicepparam` now sets the three candidate gates to true with this note as the approval reference, so a redeploy from source reproduces the live state. A test in `infra/tests/test_monitoring_alert_coverage.py` pins it.

## Per-criterion result

| Criterion | Result | Evidence and reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest and IoT ingestion | Proven installed and enabled for the demo | Listing above. Ledger digest firing proven on 2026-11-18. Job rule shape fired on a throwaway on 2026-11-18. Poison firing is not provoked: policy blocks the queue write (see the 2026-11-25 note). IoT rules fire only on transport failures, which were not provoked |
| Dashboard or workbook shows availability, errors, latency and cost against the budget | Proven for the demo, with caveats | Deployed workbook now has all 14 source items. Errors and latency return ingress data; availability reports Insufficient because no availability test exists; cost shows Unknown and Unreconciled because billing reconciliation is excluded for the demo. Portal render was not captured |
| Each alert has a runbook entry with an owner | Partly proven | Every installed demo and receiver alert names a runbook anchor and a proposed owner role. Four legacy alerts have no description. No person is named; appointment is a human decision |
| Tokenomics: metered AI usage beside the cost record with variance visible | Proven for the demo | Workbook item `ai-usage-by-capability` is now deployed; values as in the 2026-11-25 note |
