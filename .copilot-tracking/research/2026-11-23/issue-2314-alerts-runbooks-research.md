---
title: Research for issue 2314 alert rules, runbooks and AI usage saved query
description: Audit of existing infra against the four acceptance criteria
ms.date: 2026-11-23
---

## Findings

* `infra/modules/operationalMonitoring.bicep` already holds job failure metric alerts (per job), IoT alerts, `agentTasksPoison` and `aiLimitBreach` scheduled query rules. Ledger digest mismatch and verify-missing rules live in `infra/modules/monitoring.bicep`/`main.bicep`.
* `infra/monitoring-runbooks.md` has an anchored entry with a proposed accountable role for each alert; tests `test_ai_alert_runbook_ownership.py` and `test_alert_runbook_signal_matrix.py` check this.
* AI usage by capability and period with unreconciled variance exists only as workbook panels (`ai-usage-by-capability`, `ai-variance-by-period`), not as a saved query resource.
* Baseline: `bicep build infra/main.bicep` succeeds; 34 existing monitoring tests pass.
* Read-only Azure inventory (resource group `ama`) lists scheduled query rules including poison, ledger and AI limits; nothing was changed.

## Gap

A Log Analytics saved search for the AI usage query (criterion 3) and a test and runbook entry for it.

## Planning Readiness

Ready. Research disposition: executed.
