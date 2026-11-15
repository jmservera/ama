---
title: Issue 153 criterion 3 remaining unowned notices research
description: Evidence for adding Owner and Next action to ops, assistants, simulator-control, staff-intake and panels notices
ms.date: 2026-11-13
---

## Research disposition

Disposition: `reused` (independent review `153-close-independent-review-1652-review.md` names the gap; local grep confirmed).

## Evidence

* Existing test `test_content_standard.py` checks Owner and Next action only in `chat.js`, `aftercare.js`, `async-action.js`, `progress.js`, `role-screens.js`, plus selected literals.
* Unowned notices found by grep in the five target files: `ops.js` (lines 49, 59, 91, 141, 150, 184, 257, 375-376, 387), `assistants.js` (95-96, 111, 164, 225, 234, 248, 298), `simulator-control.js` (8, 11, 22, 54, 67), `staff-intake.js` (27, 125, 156), `panels.js` (199, 205, 490, 497, 503-505, 569).
* Substrings relied on by existing tests and browser checks that must be kept: `Use the manual route`, `could not be saved`, `Your review was recorded`, `Refresh and check the history`, `Assistance unavailable: Assistance request timed out`, `Nothing was changed`.
* Server-supplied `e.message` may already contain `Owner:` (for example `Store.gate_reasons`), so dynamic sinks append owner and next action only when absent.
* Scripts are classic globals loaded before `app.js`, so each file gets a uniquely named local helper rather than a shared one. `safetyPanel` in `app.js` is out of scope.

## Planning Readiness

Ready.
