# Plan: frontline screens WCAG 1.4.1 state text (Issue #232)

* [x] Add `stateCue` helper and cue tables in `role-screens.js` (`Object.hasOwn`, no new CSS classes).
* [x] Apply to choice answers, paused/withdrawn table, update commitment status, service status and contact needs, queue rows.
* [x] Add `src/api/tests/test_frontline_screen_wcag.py`.
* [x] Run design-system, role-screen, connected-home, keyboard check, full suite, ruff, mypy.
* [x] Commit with `Refs #232`; do not push.

Critique: single pass in-line; advice applied: preserve existing substrings so existing assertions stay valid; do not claim appointment coverage.
Mapping: Confirmed = resident answer recorded or closed; Waiting for resident = no answer or no contact needs yet; Action needed = staff step remains or value unrecognised.
