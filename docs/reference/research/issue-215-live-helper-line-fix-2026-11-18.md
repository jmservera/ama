---
title: Employee Chat Helper Line Fix and Per-criterion Status (Issue 215, run 4)
description: Reproduces and fixes the clipped helper line in the employee chat panel on short desktop windows, with a Playwright regression test and a per-criterion proven or unproven table
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

Refs #215. Follows [run 3](./issue-215-live-rerun3-evidence-2026-11-18.md), which recorded the clipped helper line as an open visual finding.

## Defect and fix

* Reproduced locally (real `chat-widget.js` and `chat-widget.css`, desktop Chromium, status and error lines shown): at 1366x700 and 1280x720 the sticky tools row covered the helper line "Press Enter to send..." (hit test landed on the skill select). At 1366x900 and 1920x1080 it was visible.
* Cause: the composer was a scrolling grid with a sticky tools row, and the log reserved 40% of the panel from 700px window height, leaving the composer too little room.
* Fix in `src/api`: the composer is a column with a scrolling entry region (helper lines, text area) and a non-overlapping tools row that is always visible; the 40% log reservation starts at 900px window height. The Send-in-panel guarantee for short windows is kept.
* Regression test: `src/api/tests/test_chat_widget_helper_line_visible.py` fails on the old CSS (2 sub-test failures) and passes on the fix.

## Validation (focused tier, web UI change in src/api, no SQL, security, infrastructure or deployment)

| Check | Result |
| --- | --- |
| New helper-line test | Pass; fails without the fix |
| test_chat_widget_layout, test_accessibility_baseline, test_content_standard, test_regulatory_chat_live_region_semantics | 57 tests pass |
| test_alert_chat_input_label_pii_notice_a11y (reading-order source assertion) | Failed on the DOM change; assertion updated to the new `entry`/`tools` structure; 211 tests across the chat widget and accessibility modules then pass (reviewer rerun) |
| `chat_widget_browser_check.py --employee-layout` | Pass: Send inside panel at 1280x480, 320x480, 640x360 |
| Full `chat_widget_browser_check.py` | Fails in `reply_scroll` (focused control obscured); recorded as identical on the unchanged baseline, raw output not retained; pre-existing, not caused by this change, not fixed here |
| mypy (src/api), ruff check and format | Pass |
| Live deployed app | Not re-probed: the fix is not deployed and no deployment was authorised |

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Alert and chat patterns per role | Proven earlier (ticked) | Earlier runs |
| Alert states what, source and status, safe action, owner, clock | Proven earlier (ticked) | Earlier runs |
| WCAG 2.2 AA: no colour-only status, keyboard, plain-language mode | Partly proven; the helper-line defect is fixed in code and tested locally, but a deployed re-check and the axe contrast-overlap item remain; person-run assistive-technology testing is waived for the demo, so no conformance claim | Runs 1 to 3 plus this note |
| Doubt route and no-source states | Proven earlier (ticked) | Earlier runs |
| Comprehension tested with staff | Unproven; person-run staff testing is not available for the demo | Owner decision 2026-11-18 |
