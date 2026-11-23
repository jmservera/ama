---
title: Issue 2314 alert rules, runbooks and AI usage saved query evidence
description: Per-criterion proof that alerts, runbooks and tests exist, plus a new saved query for AI usage by capability and period
ms.date: 2026-11-23
ms.topic: reference
---

Refs #2314, #146, #136. Synthetic demo, desktop only. Read-only Azure inspection in resource group `ama`; nothing was deployed, changed or deleted.

## What was found

* Job failure, poison queue, AI limit and IoT alert rules, and the ledger digest mismatch and verify-missing rules, already exist in `infra/modules/operationalMonitoring.bicep` and `infra/main.bicep`, with anchored runbook entries naming a proposed accountable role in `infra/monitoring-runbooks.md`.
* The only gap was a saved query. AI usage by capability and period existed only as workbook panels. This change adds the workspace saved search `zava-ai-usage-by-capability-and-period`, a runbook section `ai-usage-saved-query`, a test, and the resource type in the `infra/README.md` inventory.

## Live read-only evidence (2026-11-23)

`az monitor metrics alert list -g ama` and `az monitor scheduled-query list -g ama` list the existing rules. Enabled: API 5xx and restarts, SQL CPU, Foundry throttle, Key Vault expiry and denied access, and the ledger digest mismatch and verify-missing rules (both prefixes). Disabled candidates: job failure rules for `orch`, `load` and `audit`, IoT rules, `alert-cutover-test-ai-limits` and `alert-cutover-test-agent-tasks-poison`. The new saved search is not deployed, so `az monitor log-analytics workspace saved-search list` shows only the built-in workspace searches.

## Validation

* `bicep build infra/main.bicep` and `bicep build infra/modules/operationalMonitoring.bicep` succeed.
* `python3 -m unittest` for the monitoring, policy, inventory, runbook ownership and signal matrix tests in `infra/tests` pass (91 tests, plus 34 baseline monitoring tests before the change); ruff check and format check pass on the edited test.
* Tier: focused (infra documentation and Bicep, no `src` code). Hosted CI and owner review are still required.

## Per-criterion result

| Criterion | Result | Evidence |
|---|---|---|
| Bicep alert rules compile and are covered by an infra test | Proven for compilation and tests | Build output above; `test_monitoring_alerts.py`, `test_alert_runbook_signal_matrix.py`, `test_monitoring_alert_coverage.py` |
| Each alert has a runbook entry with an owner | Proven for source: every rule links to an anchor with a proposed accountable role. Named human appointment is unproven | `test_ai_alert_runbook_ownership.py`, `infra/monitoring-runbooks.md`; the runbook states appointments are pending and not made by this change |
| Saved query shows AI usage by capability and period with unreconciled variance visible | Proven in source and compiled Bicep; not executed against live data and not deployed | New saved search, `test_saved_query_shows_usage_by_capability_period_and_variance`; billing reconciliation is out of scope for the demo |
| Deployment to Azure stays an owner-authorised action | Proven by observation: no deployment was run; candidate alerts stay behind `enableCandidateMonitoringAlerts` plus `monitoringApprovalReference` | `infra/main.bicep`, live inventory shows no new resources |
