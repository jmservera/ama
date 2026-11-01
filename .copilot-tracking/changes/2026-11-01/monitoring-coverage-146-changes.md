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

## Amendment: PR #674 review fixes

* `evaluate_indicator`: `offline_only` initialised from `constructed` so blocked results keep provenance; the 0..1 range is checked before `math.isfinite`, so huge integer limits are blocked instead of raising `OverflowError`.
* `sanitize_diagnostic`: values validated per field (registered alert and owner role, enumerated status and severity, timestamps, bounded counts, identifier-shaped task and release); free text is dropped.
* Tests: `rai-harm` added to the explicit-gap assertion; new tests for provenance, huge limit and value schemas (12 tests).
