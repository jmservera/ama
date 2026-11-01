---
title: Issue 222 cohort and missing-data evaluation research
ms.date: 2026-11-01
---

## Disposition

Research executed. Planning Readiness: Ready.

## Findings

* PRD FR-054 and AC-073 require a versioned evaluation record; OQ-018 leaves cohorts, lawful fields, sample sufficiency and thresholds to owner approval, and states synthetic scenarios do not prove fairness.
* `src/core/src/zava_forward/core/ranking.py` ranks deterministically but reports no cohorts. `rai_release.py` is a pure typed module with `digest` and `named` helpers, reusable here.
* No existing cohort evaluation code (searched `src/`). Core imports only core (dependency rule test).
* `src/core` gates: ruff check, ruff format --check, strict mypy, unittest with `PYTHONPATH=src:tests`.

## Decision

Add a pure `cohort_eval.py` in `src/core` with constructed fixtures in `tests/`; no store, API or UI wiring in this slice.
