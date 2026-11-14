---
title: Issue 225 Cycle 3 rebase changes
---

* role-screens.js: conflict resolved in financeQueueRows (stateCue status, State: Paused prefixes, finance jump constants kept).
* tests/test_finance_screen_wcag.py: status assertion now expects Action needed: Exception, with Finance.
* Validation: ruff check, ruff format --check, mypy pass; 28 finance and procurement WCAG tests pass (run with tests on PYTHONPATH). The named test_ux_225/228 files do not exist in this tree.
* Note: an intermediate rebased commit briefly tracked __pycache__; a later branch commit untracks it, so the net diff is clean.
