# Research: issue 153 copy audit close (2026-11-13)

Disposition: executed. Planning Readiness: Ready.

## Criterion A (copy audit covers core flow, removes gate/hold/provenance/trace)

* `src/api/tests/test_content_standard.py` AUDITED_FILES omits served files: `aftercare.js`, `case-workspace.js`, `chat-widget.js`, `async-action.js`, `progress.js`, `workspace-shell.js`.
* Lexical scan of omitted files finds one visible violation: `progress.js:192` "The file holds only this page" (verb, but matches the banned lexical guard).
* Plan: reword to "contains", add all omitted files, add a completeness test requiring every served `*.js` and `*.html` in `web/` (excluding `vendor/`) to be audited.

## Criterion B (error and blocked messages state reason, owner, next action)

Existing coverage: `HELD_CHECK_ERRORS`, `HELD_CHECK_UNREADABLE`, `Store.gate_reasons`, `ranking_snapshot`, law.js.
Gaps outside `safetyPanel` (not touched):

* `chat.js`: `unavailableNote` (role-denied and generic), "Chat could not load", two "Chat unavailable" failures, "Proposal not requested", "Doubt route failed": no owner.
* `aftercare.js`: `AC_UNCONFIRMED`, `AC_EARLIER`, 403 refusal and fallback "Some details need fixing." lack explicit owner.
* `async-action.js` shared failure notice: "label: message. Try again." has no owner.

Constraints: keep existing asserted substrings ("Chat unavailable", "Chat could not load", "Saving could not be confirmed"), plan to keep `role-screens.js` unchanged (already compliant, tested).
