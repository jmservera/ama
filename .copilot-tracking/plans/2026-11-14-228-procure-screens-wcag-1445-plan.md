---
title: Issue 228 procurement and QA screens WCAG plan
ms.date: 2026-11-14
---

## Plan

* [x] Phase 1: add text-prefix helpers for capacity, expiry, defect and handover sign-off states in `role-screens.js`.
* [x] Phase 2: render a definition-list expiry panel on the package queue, a defect status and handover sign-off state on the quality queue; keep existing strings, table count and `aria-invalid` sites.
* [x] Phase 3: add `src/api/tests/test_procurement_qa_screen_wcag.py`; run focused tests, mypy and ruff with `/tmp` caches.

Critique: single pass, no conflicts; the expiry panel makes no validity claim.
