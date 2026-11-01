---
title: Issue 154 plan
ms.date: 2026-11-01
---

## Scope

* Add `src/core/tests/test_resident_journey_design.py` asserting J1-J7 coverage, a non-digital equivalent per journey, no-incapacity-inference and needs support, offered vs confirmed statuses, per-measure scoped choice, remedy separation, R1 task limits and expiry, no live contact and Not-run validation.
* No change to the design text, source, mvp/ or prototype/.

## Validation

ruff check, ruff format --check, mypy for the new test, and the unit test. CI is the evidence for the wider gate.

## Critique (single pass)

Risk: string-match tests can pass while design quality is poor. Disposition: accepted; the tests are stated as coverage regressions, not usability evidence. Risk: whitespace wrapping. Applied: normalise whitespace.

## Issue disposition

Use Refs #154. Unmet: usability-programme validation, accessibility acceptance, resident-view implementation of expiry.
