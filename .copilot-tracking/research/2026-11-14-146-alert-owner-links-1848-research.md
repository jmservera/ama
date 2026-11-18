---
title: "Research: #146 alert owner and runbook links on existing rules"
ms.date: 2026-11-14
task_slug: 146-alert-owner-links-1848
---

## Disposition

Research executed (source inspection). Planning Readiness: Ready.

## Findings

* `infra/modules/operationalMonitoring.bicep` already holds disabled candidates for job failures, IoT transport, agent-tasks poison and AI limits (calls, tokens, budget, expiry), each naming an owner role and a runbook anchor in its description.
* `infra/monitoring-runbooks.md` has an owned section for every alert and budget notice; `infra/tests/test_alert_runbook_signal_matrix.py` maps each declared rule to an anchor.
* `infra/monitoring-workbook.json` covers availability, errors, latency and cost versus budget (existing tests).
* Gap: the eight existing rules (`main.bicep` four metric alerts and two ledger rules, `keyvault.bicep` two rules) carried no owner or runbook link in the resource itself, and the four metric alerts had no description. An operator opening the fired alert could not find its owner or runbook.
* Pre-existing environment failure: `test_ledger_alert_queries_match_the_verifier_markers` needs the uninstalled `zava_forward.orchestrator` package; unrelated.

## Boundaries

Owners are proposed roles, not appointments. No activation, no threshold change, no Azure access.
