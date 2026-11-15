---
title: Alert signal to runbook matrix research (Refs #146)
ms.date: 2026-11-14
---

## Disposition

Research executed. Planning Readiness: Ready.

## Findings

* `infra/modules/monitoring.bicep` declares only the action group and workspace; it declares no alert rules.
* Alert rules live in `infra/main.bicep` (foundry-throttle, sql-cpu, api-5xx, api-restarts, ledger-digest-mismatch, ledger-verify-missing, budget), `infra/modules/operationalMonitoring.bicep` (job failures, IoT failures, agent-tasks poison, ai-limits), `infra/modules/keyvault.bicep` (secret-expiry, denied-access) and `infra/modules/iothub.bicep` (budget).
* `infra/monitoring-runbooks.md` has a heading per signal with "Proposed owner" or "Accountable role" text. AI limits have four anchors (calls, tokens, budget, expiry) marked "appointment pending".
* `test_ai_alert_runbook_ownership.py` and `test_monitoring_alerts.py` check parts; none enumerate every declared alert across `infra/`.
* Known gap: `import-jobs-poison` is a missing-signal procedure, not a declared rule.

## Constraint

Add only `infra/tests/test_alert_runbook_signal_matrix.py`; do not edit the bicep, runbook or workbook. Focused validation tier.
