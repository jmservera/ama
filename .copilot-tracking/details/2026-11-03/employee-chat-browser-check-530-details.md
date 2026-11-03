<!-- markdownlint-disable-file -->
# Employee chat browser check repair: details (2026-11-03)

Task: `employee-chat-browser-check-530`. Plan: [../../plans/2026-11-03/employee-chat-browser-check-530-plan.md](../../plans/2026-11-03/employee-chat-browser-check-530-plan.md).

## Phase 1

* `src/api/src/zava_forward/api/web/chat-widget.css`: `.chat-widget-log{min-height:max(3rem,40%)}`. Success: with the Sources summary focused and the log at the bottom, the control stays inside the log at 1280x720.

## Phase 2

* `checks/chat_widget_browser_check.py`: employee tab-out keeps the panel open (resident still closes); `current_reply_focus` takes `closes`; the synthetic external note is in flow for the stay-open chat; the Escape step focuses the panel first; script attempts expected are four.
* `checks/chat_submit_browser_check.py`: `render_focus` dismissal covers Escape and Close only.

## Phase 3

* From `src/api` with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH=tests:src:../core/src:../agents/src:../core/tests:../agents/tests:.`: `python3 -m unittest test_chat_widget_focus test_chat_panel test_browser_asset_urls test_case_journey`, `ruff check --no-cache checks tests`, `mypy --cache-dir=/tmp/mypy-530` on the two edited checks, and `python3 -m checks.chat_widget_browser_check --axe <pinned axe> --out <external dir>`.
