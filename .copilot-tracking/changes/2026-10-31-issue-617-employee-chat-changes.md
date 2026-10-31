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

## Correction cycle 3 (PR 620 CI)

* CI failure: ruff format --check in src-api flagged src/api/tests/test_chat_panel.py (one long assertEqual line). Reformatted with ruff format; no behaviour change.
* ruff check and ruff format --check pass in src/api and src/core; test_chat* tests pass (80); node --check passes for app.js, assistants.js and chat.js; mypy reports only pre-existing missing-stub errors in untouched files. Heavy gate not run.

## Correction cycle 4 (PR 620 Copilot review)

* Finding: a same-route refresh called employeeChat.install(), which unhid the launcher beneath a docked widget. install() now hides the launcher for unauthorised users and unhides it only when no widget exists (chat.js).
* Regression: test_reinstall_preserves_widget_toggle_and_launcher_state asserts a hidden (docked) launcher stays hidden after install(). test_chat_widget_focus passes; ruff check, ruff format --check and node --check pass; mypy shows only pre-existing missing-stub errors. Other test_chat* modules need the installed package, not available here. Heavy gate not run.

## Correction cycle 5 (PR 620 CI, Synthetic design-system browser checks)

* CI failure: case_journey_browser_check chat_cleanup timed out waiting for the stored-thread ask request. Reproduced locally with Chromium. Cause: the product change (kept) sends employee chat to /api/chat/unstored-ask while storage is not approved, and the check relied on the old always-stored behaviour.
* Fix (check only): chat_cleanup now routes /api/chat/status to add storage_approved true, so it still exercises the stored-thread lifecycle. Product behaviour unchanged.
* case_journey_browser_check passes in full; test_chat_panel and test_chat_widget_focus pass, plus the CI browser unit test; ruff check, ruff format --check and mypy pass. Heavy gate not run.
