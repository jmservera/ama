<!-- markdownlint-disable-file -->
# Review: Issue 1530 case safety usability

Execution: executed once after implementation (`code-review` and `code-review-accessibility`, independent agents).
Outcome: Conformant after one fix. No open material findings.

## Findings

* `code-review`: no significant issues. Restart eligibility, role and independence checks match the server. No banned words, non-ASCII, `aria-invalid` or `h("table"` additions.
* `code-review-accessibility`: one high-confidence finding. A stale `setCustomValidity` message could block resubmission after a whitespace-only entry (WCAG 3.3.1, 3.3.3, 4.1.2). Fixed by clearing the message on `input` in `textInput` and the raise `source` field, with test coverage. Re-run: 85 targeted tests, ruff, format and mypy pass.

## Routed later work

* Focus after a successful submit may return to the page body because `refresh()` re-renders the case view. Needs browser or screen reader confirmation. Not changed here.
* The `case_journey_browser_check` 320px summary height check (1636 against 1600) fails on unmodified HEAD and is outside this change.
