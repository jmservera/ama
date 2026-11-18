# Changes: chat origin badge accessibility tests

Date: 2026-11-14. Plan: `.copilot-tracking/plans/2026-11-14-chat-origin-badge-a11y-plan.md`.

* Added `src/api/tests/test_chat_origin_badge_a11y.py` (10 tests, static source checks).
* No production, `checks/*` or documentation edits.
* Divergence: dropped "grounded" from the jargon list because the existing generative detail text uses it; recorded as follow-up.
* Validation: unittest `test_chat_origin_badge_a11y`, `test_accessibility_baseline`, `test_content_standard` OK (52 tests); `ruff check` and `ruff format --check` pass.
