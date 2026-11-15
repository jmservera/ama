# Details: issue 153 copy audit close

## Phase 1

* `progress.js:192`: "The file holds only" becomes "The file contains only".
* Test: `AUDITED_FILES` gains `aftercare.js`, `case-workspace.js`, `chat-widget.js`, `async-action.js`, `progress.js`, `workspace-shell.js`. New test globs `WEB/*.js` and `WEB/*.html` and asserts each is in AUDITED_FILES.

## Phase 2 message edits (keep existing prefixes)

* chat.js `unavailableNote`: add "Owner: ..." then "Next action: {manual}".
* chat.js "Chat could not load", two "Chat unavailable", "Proposal not requested", "Doubt route failed": add "Owner: application support. Next action: ...".
* aftercare.js `AC_UNCONFIRMED`, `AC_EARLIER`, 403 text and fallback: add Owner and Next action.
* async-action.js failure notice: add Owner and Next action.

## Phase 3 test

Regex-extract these literals from source and assert each contains "Owner:" before "Next action:" and no banned term.

## Phase 4 validation

`test_content_standard`, `test_programme_screen`, `test_aftercare_screen`, `test_chat_panel`, ruff, mypy in `/tmp/venv-153-1626`. `docs/reference/` is not touched, so `test_cutover_audit` is not required.
