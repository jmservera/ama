---
title: Issue 153 exact button names research
ms.date: 2026-11-13
---

## Research disposition: reused

Evidence: review findings at 153-app-notices-review-1848-review.md (2 Medium) and direct reads of app.js.

* app.js:678 briefing notice names both "Try loading briefing again" and "Refresh briefing"; the load error path renders the retry button only when `content` is empty (line 679); otherwise the painted "Refresh briefing" button (line 647) remains.
* app.js:1967 startupFailed notice names both "Try again" and "Reload workspace"; only one renders, chosen by `error.reloadWorkspace`.
* Existing tests: src/api/tests/test_app_js_notices_content.py matches the notice pattern by regex only.

Planning Readiness: Ready
