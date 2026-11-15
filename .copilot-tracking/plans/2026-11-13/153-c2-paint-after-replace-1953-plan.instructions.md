---
applyTo: ".copilot-tracking/changes/2026-11-13/153-c2-paint-after-replace-1953-changes.md"
---

# Plan 153 c2

* [ ] Move `painted = true` to the end of `paint()` in `app.js`, after `content.replaceChildren(...)`.
* [ ] Add test: node model of `paint` throwing on first load renders "Try loading briefing again" and the notice names it; static check that `painted = true` follows `replaceChildren`.
* [ ] Run test_app_js_notices_content, test_content_standard, test_case_journey, ruff, mypy in `/tmp/venv-153bc2-1953`.

Details: `.copilot-tracking/details/2026-11-13/153-c2-paint-after-replace-1953-details.md`
