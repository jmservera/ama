<!-- markdownlint-disable-file -->
# Employee chat short viewport Send: details (2026-11-04)

## Phase 1

File `src/api/src/zava_forward/api/web/chat-widget.css`: add `.chat-widget-composer .chat-widget-tools{position:sticky;bottom:0;background:var(--surface);padding-top:var(--spacingHorizontalS)}`. Success: Send is inside the panel box at 320x480 and 640x360.

## Phase 2

File `src/api/checks/chat_widget_browser_check.py`, `employee_reserved_and_short`: loop over 320x480 and 640x360, expect Send in viewport and within the panel bounding box; remove the "open, not asserted" comment.

## Phase 3

Run from `src/api` with source PYTHONPATH: `test_chat_panel`, `test_chat_isolation`, `test_resident_chat_api`; `ruff check`; `mypy --cache-dir=/tmp/mypy-530`; `checks.chat_widget_browser_check` with pinned axe 4.10.3. Add a README note.
