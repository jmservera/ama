# Issue 159 c1 research: src-api CI failure on PR 1819

* Research disposition: executed. Planning Readiness: Ready.
* Failure: `test_chat_says_in_plain_words_it_cannot_approve_or_change_records` asserts the exact string `"employee-chat-entry-warning employee-chat-error"` in chat.js.
* Cause: commit 473259a90 appended `employee-chat-keys` to aria-describedby, so the closing quote no longer follows `employee-chat-error`.
* Location: src/api/tests/test_home_chat_regulatory_keyboard_provenance.py line 165; the only test asserting the old string (grep of src/api/tests).
* Intent of the assertion: the warning and error ids stay in the entry description. The keyboard hint id is an intended addition.
