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

## Correction 2026-11-03 (after independent review, Pass with fixes)

Original text above is preserved. Changes:

* `chat-widget.css`: the `max(3rem,40%)` log minimum applied to the resident chat too. Now `@media (min-height:700px){#employee-chat .chat-widget-log{min-height:max(3rem,40%)}}`; the shared rule is back to `min-height:3rem`.
* `chat_widget_browser_check.py`: new `employee_reserved_and_short` asserts the open employee panel's bounding box does not overlap an in-flow note (the stay-open chat reserves page space) and that Send stays in the viewport at 1280x480.
* `chat_submit_browser_check.py`: comment records that external focus leaving the panel open with focus intact is asserted by `current_reply_focus` and `employee_current_focus` in the widget check.
* State record: critique pointer set to the plan, `session_status` set to `stopped` (task completed).

### Measurements (Chromium, synthetic data, Send bottom edge in px; lower is better)

Resident chat, consent composer, 320px wide (viewport height 900 / 800 / 480):

| CSS | 900 | 800 | 480 |
| --- | --- | --- | --- |
| origin/main (329824c44) | 1047 | 986 | 784 |
| original PR head (e5af5ba1b) | 1143 | 1080 | 863 |
| corrected | 1047 | 986 | 784 |

The original rule made the resident worse (about 96px further out at 900); the corrected rule is identical to main for the resident. Send is outside the viewport in every case, so the resident finding (#520) remains open.

Employee chat, Send bottom edge (viewport height): 1280x720: main 575, corrected 597 (log 164 to 220px, in viewport). 1280x480: 383 on both (in viewport, asserted). 320x480, 320x568 and 640x360: identical on main and corrected, Send scrolls inside the composer (intersection ratio 0, 0.42, 0); this is pre-existing, not asserted and unverified as fixed.

### Validation (focused tier; complete gate and benchmarks not run)

Run from `src/api` with `PYTHONDONTWRITEBYTECODE=1`: 93 focused unit tests OK (1 skipped; adds `test_static_assets`); `ruff check --no-cache checks tests` passed; `mypy --cache-dir=/tmp/mypy-814` on the two checks: no issues. Chromium (Playwright 1.64.1) with pinned axe-core 4.10.3: all employee legs of `chat_widget_browser_check`, including the new assertions, and the employee and resident legs of `chat_submit_browser_check` PASS. The resident leg of `chat_widget_browser_check` still FAILS at 320px (focus/Send outside the viewport; the resident CSS equals main), so the shared command exits non-zero. Pre-existing ignored `__pycache__` removed; `git status --short --ignored` is empty after commit.
