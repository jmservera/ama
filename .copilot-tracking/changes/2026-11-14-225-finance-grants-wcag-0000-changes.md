---
title: Issue 225 finance and grants WCAG changes
ms.date: 2026-11-14
---

* Modified `src/api/src/zava_forward/api/web/role-screens.js`: State-prefixed eligibility and readiness; new Funding state summary table (grant eligibility, co-funding cap, claim pack readiness, cost variance).
* Modified `style.css`: inset focus-visible for scroll regions.
* Added `test_finance_grants_screen_wcag.py` (8 tests). 42 tests pass with the finance screens and accessibility baseline suites; mypy, ruff check and format clean.
* Divergence: co-funding cap and variance have no data source, so both show State: Unknown.
* Correction cycle 1 (independent-direct finding): `specialist_keyboard_browser_check.py` now expects the "Funding indicators and their state" region for `finance-funding` and drops it from `NO_REGION_GAPS`. `fundingEligibility` labels a grant "Verified:" only when `verified === true` or status is verified; a bare recorded outcome shows "(recorded, not verified)". No "Ready to claim" literal existed at f4e0fabee, so the guard covers the outcome label. Test added.
