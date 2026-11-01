---
title: Issue 222 cohort and missing-data evaluation plan
ms.date: 2026-11-01
---

## Plan

* [x] Phase 1: `cohort_eval.evaluate(manifest, observed, disposition)` returning a hashed record with per-cohort n, errors, exclusion, review burden, Wilson interval, per-dimension gaps, blockers and status.
* [x] Phase 2: constructed paired cohorts (source completeness, support need, appointment history) with seeded defects in `tests/cohort_eval_fixture.py`.
* [x] Phase 3: unit tests per acceptance criterion; ruff, format, mypy.

## Critique

Executed once. Verdict: acceptable. Applied directly: a human disposition may clear only exceedance and defect blockers, never unapproved thresholds, insufficient samples or reconciliation failures; synthetic input is never fairness evidence.

## Out of scope

Wiring into the ranking golden set (#108), the #174 fixtures, API or UI.
