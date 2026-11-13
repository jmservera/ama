---
title: Issue 153 C4 async-action owner/next-action dedup research
description: Research for review findings F1 and F2 in async-action.js
ms.date: 2026-11-13
---

## Scope

Review findings F1 and F2 (`.copilot-tracking/reviews/2026-11-13/153-srv-closure-review-1921-review.md` in the review worktree) on `src/api/src/zava_forward/api/web/async-action.js:35`.

## Evidence

* `async-action.js` `finish(error)` always appends `Owner: application support. Next action: check the recorded history before repeating a change...` to `error.message`. A server 500 message that already carries `Owner:` and `Next action:` renders a duplicate pair.
* `ops.js` `opsOwned` already returns messages unchanged when `Owner:` precedes `Next action:`, but only for that order and not for `Next step:`.
* The same wording is shown for read-only loads and searches, where "repeating a change" is misleading.
* Asserted strings: `test_loading_feedback` expects `/Synthetic failure.*Try again/`; `test_content_standard` asserts the "recorded history before repeating a change" phrase against `app.js` only (GENERIC_CHANGE_ERROR), not `async-action.js`; `test_timecapture_copy` asserts `Owner: application support. Next action:` on rendered banners.

## Decision

* F1: in `finish`, return the message unchanged when it contains `Owner:` and `Next action:` or `Next step:`.
* F2: neutral default `Next action: check what the screen or recorded history now shows. Try again if nothing changed; ...`. `app.js` GENERIC_CHANGE_ERROR (mutation specific) is untouched.
* Add a node-driven unit test in `test_loading_feedback.py`.

Planning Readiness: Ready. Research disposition: executed.
