---
title: Issue 228 procurement and QA screens WCAG changes
ms.date: 2026-11-14
---

## Changes

* `src/api/src/zava_forward/api/web/role-screens.js`: capacity states (Offered capacity remaining, Fully committed, Over-committed, Unknown), expiry states (Expired, Expires within 30 days, In date until, Unknown), defect status and handover sign-off state, and a "Ready on record." prefix on the quality ready message.
* `src/api/tests/test_procurement_qa_screen_wcag.py`: new focused conformance tests.

## Validation

* Passed: the new tests, `test_accessibility_baseline`, `test_procurement_screens`, `test_technical_quality_screens`, `test_role_screens_conformance` and the `*screen*` suites with `../core/src` on the path.
* `mypy` and `ruff check` and `ruff format --check` in `src/api` passed with `/tmp` caches.
* Not run: the full gate, browser checks and Docker, by instruction (focused tier). Hosted CI is unobserved.
