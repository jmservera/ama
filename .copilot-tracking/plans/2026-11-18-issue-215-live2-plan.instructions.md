# Plan: issue 215 live2 (2026-11-18)
* [x] P1 Edit `src/api/src/zava_forward/api/web/chat-widget.css` (composer, sticky tools, log min-height media query). Details: .copilot-tracking/details/2026-11-18-issue-215-live2-details.md
* [x] P2 Add `src/api/tests/test_chat_widget_helper_line_visible.py`: Playwright, skipped when chromium is unavailable; asserts helper line hit-tested and tools inside panel at 1366x700, 1280x720, 1366x900 with status and error shown.
* [x] P3 Run the new test, test_accessibility_baseline.py, test_content_standard.py, test_regulatory_chat_live_region_semantics.py, mypy, ruff check/format. Tier FULL not required for CSS-only focused change? Web UI file change in src/api: focused tier with the two web-UI tests; no SQL/security/infra.
* [x] P4 Research note with per-criterion table, log, index; commit.
