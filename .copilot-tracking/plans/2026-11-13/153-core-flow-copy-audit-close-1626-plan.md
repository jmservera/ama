# Plan: issue 153 copy audit close

Research: [research](../../research/2026-11-13/153-core-flow-copy-audit-close-1626-research.md)
Details: [details](../../details/2026-11-13/153-core-flow-copy-audit-close-1626-details.md)

* [x] Phase 1: reword `progress.js` "holds"; extend AUDITED_FILES; add completeness test over served web files.
* [x] Phase 2: add Owner and Next action to chat.js, aftercare.js, async-action.js error messages; keep `safetyPanel` and `role-screens.js` untouched.
* [x] Phase 3: add `test_content_standard` test asserting reason, owner, next action for those messages.
* [x] Phase 4: run targeted tests, ruff, mypy; independent review; commit.
