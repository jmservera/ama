---
title: Clarification, #74 original plan API-regression checkbox
description: Dated clarification; the original plan is preserved unchanged
ms.date: 2026-11-13
---

Applies to `.copilot-tracking/plans/2026-11-13-74-home-building-applicability-display-plan.md` (line 7, `[x] Phase 2: add regressions in test_home_case_api.py and one assertion in home_case_browser_check.py`), preserved unchanged in `f50c5c7fd`. Refs #74.

## Clarification

* No API test was added. `src/api/tests/test_home_case_api.py` is not changed by candidate `f50c5c7fd`. The checkbox over-ticked the plan's API-regression item.
* Six EXISTING API tests (`tests.test_home_case_api`) were run as regression checks and exited 0 in the retained validation (`8b98f72a3`, copied under the source-records folder).
* New browser behavior assertions were added in `src/api/checks/home_case_browser_check.py`. This is the only added test-like coverage.
* The author changes file and the static review addendum already record that no unit test was added (critique C1). This file makes the correction explicit and dated; it supersedes nothing in the original artifacts.
* The details file's planned "Affected homes" label and Phase 2 unit test differ from what was built ("Homes:" on the home view, no unit test). The changes file is the accurate record.
* Adverse history is unchanged: the first editable-install run resolved the wrong source, gave one unrelated 404, and a later red came from the check's own wording mismatch. Neither is a valid base-red. Old base-red claims stay author-reported and unverified.
