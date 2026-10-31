# Changes: employee chat (#617)

* src/core/src/zava_forward/core/chat_panel.py: `ask_unstored`.
* src/api/src/zava_forward/api/server.py: `storage_approved` in chat status; `unstored-ask` route.
* src/api/src/zava_forward/api/web/chat.js: resizable layout (same as resident); unstored mode.
* Tests: core/tests/test_chat_panel.py (UnstoredAskTests); api/tests/test_chat_widget_focus.py (fake DOM extended, new unstored test).
* Validation: 86 api + core focused tests OK (2 skipped); ruff and mypy clean on touched files; node --check OK. Live local check: chat opens, stays open, reply returned (200), widget 448x560 at 1280x800, same widget code as resident. Heavy gate not run; CI is the evidence.
* Divergence: none. Not proven: live-site check with the test user.
