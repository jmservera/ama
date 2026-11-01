---
title: Issue 531 briefing feedback guidance changes
ms.date: 2026-11-01
---

* `src/api/src/zava_forward/api/web/app.js`: briefing paragraph (`data-briefing-feedback`) explaining how to correct, give feedback and refresh.
* `src/api/tests/test_loading_feedback.py`: `BriefingFeedbackGuidance` test.
* `src/api/README.md`: G15 row now names the visible feedback paragraph.
* `docs/reference/log.md`: appended entry.
* Validation: ruff check and format passed; mypy reports the same 12 pre-existing missing-stub errors as unchanged main; 34 focused unit tests passed; `loading_briefing_browser_check` passed with axe-core 4.10.3 (SHA-256 matches the pin).
* Divergences: none.
* PR #628 thread amendment: guidance now applies only when review controls are shown and tells users to choose Refresh briefing for a fresh briefing when Edit this draft is unavailable (stale or unverified) or the review is already recorded. Test updated to match.
* PR #628 second thread amendment: refresh advice now says Refresh briefing may reuse the cached draft for an unverified briefing with unchanged records, and points to the rules and templates option or ordinary case work. Test updated.
