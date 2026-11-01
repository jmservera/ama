---
title: Monitoring coverage 146 changes (2026-11-01)
ms.date: 2026-11-01
---

## Added

* `src/core/src/zava_forward/core/monitoring_coverage.py`: alert register, `coverage_gaps`, `evaluate_indicator`, `sanitize_diagnostic`.
* `src/core/tests/test_monitoring_coverage.py`: 10 tests (register vs runbook/Bicep, indicator states, sanitiser).

## Modified

* `infra/monitoring-runbooks.md`: "Executable Coverage Check" section, ms.date.

## Validation

* src/core: unittest for the new module OK; `ruff check`, `ruff format --check`, `mypy` clean.
* No Azure access, no deployment, no new alert resources. Divergence: none from plan.

## Amendment

Ledger alert markers point at `main.bicep` (defined there, not containerapps).
