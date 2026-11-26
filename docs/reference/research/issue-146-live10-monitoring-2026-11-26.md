---
title: Issue 146 monitoring criteria, live10 simulator failure rule (2026-11-26)
description: Fresh read-only live inventory for issue 146, a new opt-in failure rule and runbook entry for the live simulator job, and a proven or unproven result per criterion
ms.date: 2026-11-26
ms.topic: reference
---

Refs #146. Synthetic demo, resource group `ama`, desktop only, existing Azure CLI login. Read-only calls (names, enabled flags, aggregation); nothing deployed, created or changed, no credential read. Builds on the [live8](./issue-146-live8-monitoring-2026-11-25.md) and [live9](./issue-146-live9-monitoring-2026-11-25.md) notes.

## Live inventory (2026-11-26 08:22 UTC)

* Metric alerts enabled: Foundry throttle, SQL CPU, API 5xx and restarts (legacy and demo). Disabled: demo audit, orch and load job failure (`Executions`, Total) and four IoT rules.
* Scheduled-query alerts enabled: Key Vault expiry and denied access, ledger digest mismatch and verify missing (legacy and demo). Disabled: AI limits, agent-tasks poison.
* Jobs: `job-cutover-test-demo-load`, `-audit`, `-orch`, `job-live-simulator`, `job-live-receiver`, `job-184-bodyscan`. The last three have no failure rule installed.
* No `tmp146` resource. Workbook last modified 2026-11-21 (stale against source per live8).

## Source change

`infra/live-simulator-job.bicep` gains `failureAlertActionGroupId` (empty by default, so no rule and no estate change) and `alert-job-live-simulator-failed`, mirroring the receiver rule: `Microsoft.App/jobs` `Executions`, `state=Failed`, Total >0, 15 minutes, every five minutes, severity 2. Its description names the proposed owner role, "appointment pending" and the new `Job live simulator` runbook anchor in `infra/monitoring-runbooks.md`.

Validation: `az bicep build` of the module succeeds; `infra` tests `test_monitoring*` (44), `test_alert_runbook_signal_matrix`, `test_bicep_policy` and `test_ai_alert_runbook_ownership` (77) pass; `ruff check` clean. Not run: deployment of the rule, hosted CI, `rpi-checks.py --all`.

## Per-criterion result

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest, IoT ingestion | Unproven as a whole | Ledger digest installed, enabled and fired on 2026-11-18. Job, poison and IoT rules are installed but disabled, or (simulator, receiver) not installed; enabling needs a named-human `approvalReference`. The simulator rule is source only |
| Workbook shows availability, errors, latency and cost against budget | Unproven | Source tiles executed live in live8; deployed copy is stale and a redeploy was not authorised here; no Portal render |
| Each alert has a runbook entry with an owner | Partly proven | Source entry exists for every authored rule, test-enforced, with proposed owner roles; no person is named (human decision) |
| Metered AI usage beside the Azure cost record, variance visible | Proven for the demo (live8, not re-run) | Cost record shows Unknown and variance Unreconciled; billing reconciliation is out of demo scope |

No box is ticked by this note.
