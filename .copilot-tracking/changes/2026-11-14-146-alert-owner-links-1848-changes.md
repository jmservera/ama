---
title: "Changes: #146 alert owner and runbook links on existing rules"
ms.date: 2026-11-14
task_slug: 146-alert-owner-links-1848
---

## Changes

* `infra/main.bicep`: `runbookBase` var; descriptions with proposed owner and runbook anchor on foundry-throttle, sql-cpu, api-5xx, api-restarts, ledger-digest-mismatch and ledger-verify-missing. The digest description no longer claims job failure, matching the query.
* `infra/modules/keyvault.bicep`: same for secret-expiry and denied-access.
* `infra/tests/test_alert_runbook_signal_matrix.py`: new test tying each existing rule description to its matrix anchor and an existing runbook section.
* `infra/monitoring-runbooks.md`: B3 evidence row updated.

## Validation

* `az bicep build` main.bicep: pass.
* `pytest infra/tests -k "alert or monitoring or runbook or workbook or policy"`: 99 passed, 1 pre-existing environment failure (missing `zava_forward.orchestrator`).
* ruff check and format (line length 100): see commit.

## Not done

Hosted CI, appointments, signal drills, activation.
