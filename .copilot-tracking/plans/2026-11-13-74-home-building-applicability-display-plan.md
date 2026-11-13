---
title: Plan for #74 home view building applicability display
ms.date: 2026-11-13
---

* [x] Phase 1: render existing `case_ids` and `package_ids` in the home-case building region (details: ../details/2026-11-13-74-home-building-applicability-display-details.md).
* [x] Phase 2: add regressions in `test_home_case_api.py` and one assertion in `home_case_browser_check.py`.
* [x] Phase 3: focused checks (unit test file, ruff, mypy per guide, node check), one synthetic browser observation under the heavy-lock nonqueued rule.
* Critique: one independent pass required before Phase 1 (result recorded in `../changes/` and state).
* Review: one original post-implementation Review; adverse results frozen, not iterated.
