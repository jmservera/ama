# Changes: employee chat (#617)

* src/core/src/zava_forward/core/chat_panel.py: `ask_unstored`.
* src/api/src/zava_forward/api/server.py: `storage_approved` in chat status; `unstored-ask` route.
* src/api/src/zava_forward/api/web/chat.js: resizable layout (same as resident); unstored mode.
* Tests: core/tests/test_chat_panel.py (UnstoredAskTests); api/tests/test_chat_widget_focus.py (fake DOM extended, new unstored test).
* Validation: 86 api + core focused tests OK (2 skipped); ruff and mypy clean on touched files; node --check OK. Live local check: chat opens, stays open, reply returned (200), widget 448x560 at 1280x800, same widget code as resident. Heavy gate not run; CI is the evidence.
* Divergence: none. Not proven: live-site check with the test user.

## Correction cycle 1 (PR 620)

* Added HTTP regression tests in src/api/tests/test_chat_panel.py: storage_approved in both states, unstored-ask rules-only with no storage or model call, rejections (approved, 403, 401, invalid fields, unknown case).
* Widget test now asserts the chat-widget-resizable class and 35/70 default range controls; verified it fails without resizable: true.
* Focused tests, ruff and node --check pass; mypy reports only pre-existing import-not-found errors. Heavy gate not run.

## Correction cycle 2 (PR 620 CI)

* CI failure: test_both_chat_submissions_clear_only_successful_unchanged_raw_questions raised "root.insertBefore is not a function". The widget legitimately calls root.insertBefore (resize controls); the test's fake Node lacked it. Added Node.prototype.insertBefore to the fake in src/api/tests/test_case_journey.py; assertions unchanged.
* test_case_journey and test_chat_widget_focus pass (36 tests); ruff and node --check pass; mypy reports only pre-existing missing-stub errors. Heavy gate not run.
