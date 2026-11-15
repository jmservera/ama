---
title: Finance and grants screens WCAG changes (#225)
---

* `src/api/src/zava_forward/api/web/role-screens.js`: jump helpers, jump nav, anchors, text prefixes.
* `src/api/tests/test_finance_screen_wcag.py`: new.
* `src/api/tests/test_finance_grants_screens.py`, `test_finance_grants_screen_wcag.py`: exempt jump nav and `-1` jump targets.
* Divergence: id `funding-summary` replaces `envelope-controls` because the content standard bans "envelope".
* Validation: 88 targeted tests OK, ruff and mypy clean. `unittest discover` not run, by instruction. Focused tier.
