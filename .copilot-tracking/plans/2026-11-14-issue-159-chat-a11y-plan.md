# Issue #159 criterion 6 plan

* Add `aria-atomic="false"` to the chat log in `chat-widget.js`.
* Add a widget-scoped `:focus-visible` rule using `--focus-w`, `--focus-ink`, `--focus-off` and `--focus` tokens in `chat-widget.css`.
* Add `src/api/tests/test_chat_panel_accessibility.py` covering live-region attributes, focus rules, Enter/Escape and focus preservation on message arrival.
* Validate with the fast formula (targeted unittest modules, ruff, mypy).
* Critique: executed once; compatible finding applied (keep dialog role to preserve existing tests). No push or PR.
