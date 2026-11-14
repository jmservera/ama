---
title: Epic 149 form error summary associations plan
ms.date: 2026-11-14
---

## Plan

* [x] Phase 1: add `src/api/tests/test_epic149_form_error_summary_associations.py` (details: `.copilot-tracking/details/2026-11-14-demo-149-form-error-summary-associations-0502-details.md`).
* [x] Phase 2: run baseline, epic149 and accessibility tests, ruff check, ruff format --check, mypy.

## Critique (one pass, inline)

Compatible. Keep the counted baseline untouched: the test reads it but never edits it. Record focus gaps as shrink-only sets rather than fixing web code (out of scope). Verdict: proceed, no user decision needed.

## Validation tier

Focused (tests only, no workflow, dependency, Dockerfile or security-control change).
