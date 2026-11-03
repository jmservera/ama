<!-- markdownlint-disable-file -->
# Employee chat browser check repair: changes (2026-11-03)

Task: `employee-chat-browser-check-530`. Refs #530. Plan: [../../plans/2026-11-03/employee-chat-browser-check-530-plan.md](../../plans/2026-11-03/employee-chat-browser-check-530-plan.md).

## Files changed

* `src/api/src/zava_forward/api/web/chat-widget.css`: log minimum height `max(3rem,40%)`.
* `src/api/checks/chat_widget_browser_check.py`: stay-open employee expectations, in-flow external note, four-attempt budget.
* `src/api/checks/chat_submit_browser_check.py`: no external-focus dismissal case for the employee chat.
* `src/api/README.md`: note on stay-open behaviour and the open resident 320px finding.
* `.copilot-tracking/*/2026-11-03/`: this RPI evidence.

## Validation (focused tier; the complete gate was not run)

Run, from `src/api`, with `PYTHONDONTWRITEBYTECODE=1` and Chromium via Playwright 1.64.1 plus pinned axe-core 4.10.3 (sha256 matched):

* `unittest test_chat_widget_focus test_chat_panel test_browser_asset_urls test_case_journey`: 88 tests OK, 1 skipped.
* `ruff check --no-cache checks tests`: passed.
* `mypy --cache-dir=/tmp/mypy-530` on the two edited checks: no issues.
* `checks.chat_widget_browser_check`: the employee legs (shared UI, focus, stale, Enter/Send, recovery, axe, reflow at 320/390/1280) and the `chat_submit_browser_check` employee legs PASS. The resident leg FAILS (Send not in viewport at 320px; also fails on unchanged main), so the command exits non-zero and is not claimed green.

Not run: full suites, benchmarks, the complete local gate, actual SQL Server selectors, live model, live employee-site verification, screen-reader or voice-control testing.

## Divergences

* Planned a fully green shared check; the resident leg is outside this slice (#520) and is routed instead.
