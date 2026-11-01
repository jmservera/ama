---
title: Monitoring coverage 146 plan (2026-11-01 slice)
ms.date: 2026-11-01
---

## Phases

* [x] P1 Module `src/core/src/zava_forward/core/monitoring_coverage.py`: `ALERTS` register, `coverage_gaps`, `evaluate_indicator`, `sanitize_diagnostic`.
* [x] P2 Tests `src/core/tests/test_monitoring_coverage.py` including register vs `infra/monitoring-runbooks.md` anchors and Bicep alert names.
* [x] P3 Runbook doc: add a short "Executable coverage check" section and ms.date in `infra/monitoring-runbooks.md`.
* [x] P4 Focused validation: unittest, ruff check, ruff format --check, mypy in `src/core`.
* [x] P5 Review, commit, push, PR (`Refs #146`).

## Critique (single pass, self-critique)

Execution: done once. Verdict: proceed. Dispositions: keep thresholds constructed-only unless a named approver is given; never emit green wording; no AI authority transfer; no new platform. No conflicts with confirmed decisions.
