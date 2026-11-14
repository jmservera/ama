---
title: Issue 225 finance and grants WCAG plan
ms.date: 2026-11-14
---

* Add `fundingStateRows` table (row headers, State prefixes) to the funding screen; prefix eligibility and claim pack readiness values.
* Add `.table-scroll:focus-visible` inset two-tone outline in `style.css`.
* Add `src/api/tests/test_finance_grants_screen_wcag.py`; run it with `test_finance_grants_screens` and `test_accessibility_baseline`.
* Validation tier: focused (mypy, ruff check and format with /tmp caches in src/api). Critique: single pass, no conflicting findings; no push or PR.
* Review checkboxes for human approval stay unchecked.

* Correction cycle 1: update the region contract and gap list, harden the verified label, add a test, rerun mypy, ruff and the focused suites. Critique executed once; compatible findings applied directly.
