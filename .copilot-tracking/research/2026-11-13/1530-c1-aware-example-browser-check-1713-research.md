---
title: Issue 1530 C1 fix research
description: Evidence for the aware-hint example and populated safety panel browser coverage
ms.date: 2026-11-13
---

Research disposition: reused. Planning Readiness: Ready.

## Evidence

* Review `1530-ux-independent-review-1652-review.md` Finding 1: `#hz-aware-hint` in `src/api/src/zava_forward/api/web/app.js` (about line 1771) has no example; `test_safety_panel_ux.py` asserts `Example:` only for `hz-note-hint` and `hz-source-hint` (lines 235-236).
* Coverage note 7: `src/api/checks/case_view_ux_browser_check.py` scans `ZF-1` with blockers fixture only; ZF-4 is visited only in fallback cases. No committed scan of a populated hazard panel at 1280/390/320 px or 200% zoom.
* `checks/case_journey_browser_check.py` provides `scan`, `journey_data`, `sign_in`; `design_system_browser_check.py` provides `check`, `main`.
* `scenario-manifest.json` hashes `workbench_browser_check.py` as the recipe; to be checked whether it binds `case_view_ux_browser_check.py` (grep found no reference).
* Tracking files are committed in this repository, so the final tree must be clean.
