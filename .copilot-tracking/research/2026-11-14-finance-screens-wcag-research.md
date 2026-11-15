---
title: Finance and grants screens WCAG research (#225)
---

* Planning Readiness: Ready. Research disposition: executed.
* Existing: `test_finance_grants_screen_wcag.py` covers `State:` prefixes in the funding table, captions and scroll regions.
* Gap: no keyboard section jumps; invoice queue Status/pause cells and funding Status lacked text prefixes.
* Pattern: `exceptionJumpNav` (#229) uses native buttons with `data-jump-target` and `tabindex=-1` heading targets.
* Constraint: `test_content_standard.py` bans internal terms; `envelope-controls` contains "envelope", so the id `funding-summary` is used. Legacy finance tests forbid buttons, so they exempt the labelled jump `nav`.
* Screens are `finance-invoices` and `finance-funding` in `role-screens.js`; `finance-queue` and `grant-pack` are jump target ids.
