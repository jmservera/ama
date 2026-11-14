# Plan: #228 procurement screens WCAG 2.2

1. Add `procurementJumpNav` and `stateCue` tables (work order, invoice, evidence) in `role-screens.js`. Done.
2. Anchor panels on `procurement-packages`, `contractor-job-pack` and `finance-invoices` and add jump links. Done.
3. Add `tests/test_procurement_screen_wcag.py`; drop `a` from the no-controls list in `test_procurement_screens.py` because in-page jump links are intended. Done.
4. Run targeted tests, ruff and mypy; commit without caches; do not push. Done.

Critique: single pass, no conflicting advice; risk was the literal `screenPanel` matching, handled by keeping the title first.
