# Issue 444 focus, loading and error-announcement follow-up details

Date: 2026-10-26. Plan: ../../plans/2026-10-26/issue444-focus-followup-plan.md.

## Files

* `index.html`: empty `#status`; remove `role="alert"` from `#error`; add `aria-describedby="error-text"` to `#error-title`.
* `src/api/src/zava_forward/api/resident_preview/web/resident.js`: `load(fromRetry)`; focus `#main` on retry; status text on success after retry; keep `fail()` focus on `#error-title`; set loading text from script.
* `src/api/src/zava_forward/api/resident_preview/web/resident.css`: delete `main:focus{outline:none}`.
* `src/api/checks/resident_preview_browser_check.py`: new `check_retry_focus_and_announcements`, plus the revoked step clicks the real retry control and the alert assertion becomes a focus and single-announcement assertion.
* `src/api/tests/test_resident_preview_api.py`: HTML contract test through the real HTTP server (empty status, no alert role, tabindex on main and heading, noscript present).
* `src/api/README.md`: one short note on the retry focus behaviour only if the section already lists the resident browser check.

## Browser assertions (real Chromium, real server, real grant file changes)

1. Revoke grant, load: error heading focused; `[role=alert]` count 0; status empty; exactly one visible error panel.
2. Delay `/resident/view` by 500 ms through route interception, Tab to Try again, Enter: during loading `document.activeElement.id == "main"`, status text "Loading your progress...", error hidden.
3. Still revoked: after failure `activeElement.id == "error-title"`.
4. Restore grant, Tab, Enter: after success `activeElement.id == "main"`, status "Your progress has loaded.", content visible, never `BODY`.
5. Poll `document.activeElement` immediately after Enter and across the delayed pending request; it must be `#main` each time (critique C3).
6. JavaScript disabled context: `#status` text is empty and noscript text is visible.
7. Skip link Enter: `#main` focused and computed outline width >= 3px.
8. 320px reflow after recovery: no horizontal scroll.

## Validation commands (from src/api, venv in /mnt/ama-rpi-gates/issue444-focus-followup)

* `python -m unittest tests.test_resident_preview_api tests.test_resident_api -q` with the repository's established test paths.
* `PLAYWRIGHT_BROWSERS_PATH=<gate>/browsers python -m checks.resident_preview_browser_check`.
* `ruff check` and `ruff format --check` where installed for touched Python; `mypy` only if available without heavy installs.
* Failing-before run: new tests against unchanged web files; record the failing assertion names.
