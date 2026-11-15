# Changes: 157 C4 status depth and memory caps (1953)

Tier: Focused (report-only fields, tests; no gate, permission, dependency or security-control change).

* `chat_panel.py`: `AGENT_DEPTH`, `MEMORY_CAPS`, `CALLS_PER_REQUEST_BASIS`.
* `server.py`: `/api/chat/status` limits add `agent_depth`, `memory_caps`, `calls_per_request_basis`.
* `chat.js`: limits note shows request call cap, assistant depth, saved-note caps.
* Tests: api `test_chat_panel.py` (3 new), `test_chat_widget_focus.py` (render assertions).

Validation (venv /tmp/venv-157c4c-1953): core test_chat_panel 53 OK; api test_chat_panel + widget_focus + content_standard 95 OK (1 skipped opt-in Chromium); ruff check and format, mypy clean for core and api. Not run: hosted CI, browser test, live model.
Deviation: memory-item-absent-from-prompt test not added (existing memory_used flag assertion kept).
