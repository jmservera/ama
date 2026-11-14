---
title: Finance and grants screens WCAG plan (#225)
---

* [x] Add `screenJumpPanel` and `screenJumpNav` helpers in `role-screens.js`.
* [x] Add jump nav and target ids (`finance-queue`, `finance-lines`, `finance-economics`, `grant-pack`, `funding-summary`).
* [x] Add `Status:` and `State:` text prefixes to queue, invoice pause and funding status cells.
* [x] Add `src/api/tests/test_finance_screen_wcag.py`; adjust legacy finance tests to exempt the jump nav.
* [x] Run targeted tests, ruff and mypy.
* Critique: executed once; compatible findings applied (no `gate` or `envelope` terms).
