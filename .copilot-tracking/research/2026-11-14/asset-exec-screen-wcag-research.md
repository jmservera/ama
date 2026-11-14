---
title: Asset executive and board view WCAG research (#226)
ms.date: 2026-11-14
---

## Scope

Issue #226 criterion: Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation. Stacked on PR #1639, base c9d4204029692886e26fdf56011c25d2fd180e1a. Refs #226.

## Evidence

* The view is the `asset-board` role screen in `src/api/src/zava_forward/api/web/role-screens.js`, with tests in `src/api/tests/test_asset_board_screen.py`.
* Tables already use captions, column headers and focusable named scroll regions.
* Gaps: no summary equivalent for portfolio KPIs, risk band, milestones and AI cohort; state cells said only "Unknown"; no keyboard jump path between the eight long sections.
* The view has no visual badges and no risk band; the summary states that explicitly rather than inventing one.
* Constraints: no `aria-invalid` outside the audited baseline; no extra `[role="status"]` or `#regulatory-alerts` content; in-page hash anchors would trigger the hash router.

## Planning readiness

Ready. Research is desk-based, not observed behaviour; validation remains in #155.

## Cycle 1 correction (independent-direct-226-exec-068fc41c7)

* `test_connected_home_check.py` locates panels by the literal `screenPanel("Title"` in `role-screens.js`, so a renamed helper hides panels from the dependency manifest.
* `connected_home_browser_check.py` `EXCLUDED["asset-board"]` and `specialist_keyboard_browser_check.py` `EXPECTED_REGIONS["asset-board"]` must name the new "Summary in words" panel.
