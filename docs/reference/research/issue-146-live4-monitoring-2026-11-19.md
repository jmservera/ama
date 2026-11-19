---
title: Issue 146 monitoring coverage re-check, live demo (2026-11-19)
description: Fresh read-only inventory of installed alerts and workbooks on the synthetic demo, with a proven or unproven result per unticked acceptance criterion of issue 146
ms.date: 2026-11-19
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-19 14:20 UTC. All calls were read-only; no resource was created, so nothing needed deleting. No drill, no Key Vault rotation, no production change. Earlier pass: [2026-11-18 closure note](./issue-146-live3-monitoring-closure-2026-11-18.md).

## Commands and results

| Command (all with `-g ama`) | Result |
| --- | --- |
| `az monitor metrics alert list` | Four enabled rules: Foundry throttle (Sev2), SQL CPU (Sev3), API 5xx (Sev2), API restarts (Sev3) |
| `az monitor scheduled-query list` | Four enabled rules: Key Vault secret expiry (Sev2), denied access (Sev3), ledger digest mismatch (Sev1), ledger verify missing (Sev1) |
| `az resource list --resource-type microsoft.insights/workbooks` | Empty: no workbook installed |

The inventory is identical to 2026-11-18 after the throwaway `tmp146` rules were deleted. No job-failure, poison-queue or IoT ingestion alert exists.

## Result per unticked criterion

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest verification and IoT Hub ingestion | Partly proven, not closable | Ledger digest alerts are installed and enabled. The other three are absent. The known job-failure fix (Total instead of Maximum aggregation in `infra/modules/operationalMonitoring.bicep`) is an infrastructure change needing a redeploy and the FULL tier, which this run excludes |
| A dashboard or workbook shows availability, errors, latency and cost against the budget | Unproven | No workbook is installed, and workspace query access is private-link only, so a render cannot be observed from this host. Opening public query would weaken a control |
| Each alert has a runbook entry with an owner | Unproven | Runbook entries and offline tests exist, but owners are proposed roles; naming people is a human decision |
| Tokenomics: dashboard of metered AI usage by capability beside the Azure cost record, unreconciled variance visible | Proven for the demo on 2026-11-18 | The deployed app report shows usage by capability, reconciliation "unreconciled" and Total Cost of AI Unknown. Azure billing reconciliation is excluded by owner decision |

No criterion is ticked by this note. Follow-up for the FULL tier: change the job-failure candidate aggregation to Total, redeploy and re-test on a fresh failure.
