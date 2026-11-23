---
title: Issue 146 live alert inventory classifier (2026-11-23)
description: Read-only live inventory of the demo alerts, a repeatable offline classifier for criterion 1, and a proven or unproven result per unticked criterion
ms.date: 2026-11-23
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, desktop only, existing Azure CLI login, 2026-11-23 about 17:45 UTC. All Azure calls were read-only; nothing was created, so nothing needed deleting. No drill, no Key Vault rotation, no deployment. Earlier pass: [2026-11-22 note](./issue-146-live5-monitoring-2026-11-22.md).

## Live observations

| Command (all `-g ama`) | Result |
| --- | --- |
| `az monitor metrics alert list` | 13 rules. Enabled: Foundry throttle, SQL CPU, API 5xx and restarts for both prefixes. Disabled: job failed for `demo-audit`, `demo-orch`, `demo-load`; IoT ingress throttle, routing dropped, invalid and orphaned |
| `az monitor scheduled-query list` | 8 rules. Enabled: Key Vault expiry and denied, ledger digest mismatch and verify-missing for both prefixes (severity 1). Disabled: `ai-limits`, `agent-tasks-poison` |
| `az resource list --resource-type microsoft.insights/workbooks` | One workbook resource exists |

## Tooling added

`infra/scripts/monitoring_live_inventory.py` reads the two CLI JSON lists and classifies rules into job failure, poison queue, ledger digest and IoT ingestion, reporting `enabled`, `disabled` or `missing` per class. It reports only rule name and enabled flag, and always sets `firing_observed` to false. Run on this day's live JSON:

| Class | Status |
| --- | --- |
| job_failure | disabled |
| poison_queue | disabled |
| ledger_digest | enabled |
| iot_ingestion | disabled |

Overall coverage: `partial`. Regression tests: `infra/tests/test_monitoring_live_inventory.py` (7 cases, including a check that the name patterns match names the Bicep declares and that a string `"true"` is not treated as enabled). Focused tier: 38 monitoring tests in `infra/tests` pass; `ruff check` and `ruff format --isolated --line-length 100` clean. No `src` change.

## Result per unticked criterion

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest and IoT ingestion | Unproven (partial) | Ledger digest proven installed and enabled. Job, poison and IoT rules are installed but disabled; enabling needs an approval reference, and poison needs a verified `StorageQueueLogs` signal. No firing or notification drill is allowed for the demo |
| Dashboard or workbook shows availability, errors, latency and cost against budget | Unproven | Workbook resource exists; its queries run over a private-link workspace that this host cannot reach, and opening public query would weaken a control |
| Each alert has a runbook entry with an owner | Unproven | Test-enforced entries name proposed roles; naming a person is a human decision |
| Tokenomics: metered AI usage beside the Azure cost record | Proven for the demo on 2026-11-18 | See the [2026-11-19 note](./issue-146-live4-monitoring-2026-11-19.md); billing reconciliation excluded by owner decision; not re-run |

No box is ticked by this note.
