---
title: Issue 225 Cycle 3 rebase research
---

* Task: rebase feat/ux-225-finance-screens-wcag-1745 onto origin/feat/demo-233-same-home-tensions-0825 (PR 1715, Refs #225).
* Research disposition: executed (git conflict inspection).
* Conflict: src/api/src/zava_forward/api/web/role-screens.js, financeQueueRows. Upstream (PR 1716 / #228 lineage) uses stateCue(invoiceCues, status); #225 adds text-prefixed Paused cells and finance jump-nav constants.
* app.py and test_ux_225_finance_wcag.py did not conflict; neither exists under that name in this tree. Equivalent tests are test_finance_screen_wcag, test_finance_grants_screen_wcag, test_procurement_screen_wcag and test_procurement_qa_screen_wcag.
* Planning Readiness: Ready.
