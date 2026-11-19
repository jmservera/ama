---
title: Issue 153 live plan details
ms.date: 2026-11-18
---

* exposure_limits.py:258 reason becomes "No person-approved investment limit or tolerances are recorded."
* panels.js exposureNotice: `STATUS_WORDS = {Held: "Paused"}`; text replace of /envelope/ with "investment limit".
* app.js: the owner text is inlined (a shared constant broke the test slices of three handoff test modules; fixed in cycle 1).
* Tests: test_finance_exposure_screen.py (Held label), test_handoff_waiting_view.py (assertion at line 125 plus a case
  asserting no "Unassigned"), test_exposure_limits.py (reason has no "envelope").
