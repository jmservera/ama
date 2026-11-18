---
title: Issue 1288 UI and snapshot correlation plan (0900)
ms.date: 2026-11-14
---

## Plan

* [x] Add `src/api/tests/test_quality_sensors_correlation.py` for criteria 1-7 and 9 locally: UI values and IDs equal the model request, missing retrofit context, provenance labels, role denial, bounded read with no generation, burst plus restart dedupe, H0 release/epoch status, non-approval, stale, missing/unavailable, model failure.
* [x] Run impacted tests, ruff check and format, mypy; commit locally, do not push.

Validation tier: Focused (test-only; no workflow, dependency or deployment impact; no web file touched, so the accessibility baseline test is not applicable).

## Critique (single pass)

Risk: tests use a MOCK provider; they are labelled local engineering evidence. Compatible, no plan change required.
