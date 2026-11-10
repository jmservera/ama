---
title: Plan - numeric boundary D1 for the constructed paired report (Refs #216, #208)
description: Reject negative and non-finite-derived constructed observations explicitly
ms.date: 2026-11-10
---

## Phases

* [x] Phase 1: red tests for both defects (negative seconds, subnormal-derived ratio, exact upper bound, next greater value) for both seconds fields
* [x] Phase 2: implement negative bound and strict pre-report section validation in `src/agents/evals/run_regulatory_gates.py`
* [x] Phase 3: README sentence, targeted validation (new tests, affected paired/regulatory tests, configured mypy, Ruff check and format, supplementary strict script typing)
* [x] Phase 4: changes record and single post-implementation review

Details: `.copilot-tracking/details/2026-11-10/numeric-d1-216-details.md`. Critique: `.copilot-tracking/reviews/plans/2026-11-10/numeric-d1-216-plan-critique.md`.

## Boundaries

* `paired_trial.py`, schema, thresholds, cost, approvals, default output and `--record` semantics unchanged. No new parser, no broad catch, no silent replacement.
