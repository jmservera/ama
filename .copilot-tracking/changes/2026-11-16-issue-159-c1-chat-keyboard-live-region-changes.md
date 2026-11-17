# Issue 159 c1 changes

* Modified src/api/tests/test_home_chat_regulatory_keyboard_provenance.py line 165: exact aria-describedby assertion now includes `employee-chat-keys`.
* No other test asserted the old string (the a11y_159 test already expects the new value).
* Validation: pending, see below.

## Validation results

* test_home_chat_regulatory_keyboard_provenance, test_assistant_panel_a11y_159, test_accessibility_baseline, test_chat_widget_focus: pass.
* test_chat_panel: 4 failures (three test_b_*_budget_holds_before_live_dispatch and test_post_dispatch_provider_failure_settles_the_meter_as_ineligible), identical on parent 5e0c7f744 in a clean worktree, so pre-existing and unrelated to chat.js; not fixed here.
* ruff check and mypy on the touched test file: clean.
