# Research: #215 citation and source-origin attribution (2026-11-14)

Disposition: executed. Planning Readiness: Ready. Refs #215. Tier: focused (test-only, `src/api/tests/`).

## Evidence

* `chat.js` `attribution()` yields five origins: decision rules (deterministic, 0 generative calls), decision rules with withheld generative draft, generative-grounded, withheld generative draft, and workflow-only or unverified help. Each has its own visible label and `Source:` sentence; only a real answer can claim a rule or generative origin.
* `sourceLine()` tags citations `[Workflow rule]`, `[Decision rule]` or `[Case record]`. `chat-widget.js` `message()` renders `Sources (N)` in a native `details`/`summary`; an empty list shows a check-with-a-person note.
* The entry warning (`employee-chat-entry-warning`) is appended to the form `beforeInput`, outside the message log, so it persists across answers and withheld replies. `statusFor()` and the attribution text repeat the no-record-changed statement.
* Alert cards state 0 model calls and list sources through `regulatorySources()` with status, effective and retrieved dates.

## Gaps and limits

* Per-message source lists use native `details` semantics. `aria-expanded` and `aria-controls` exist only on the panel launcher, so the requested explicit attributes on the source list are not present; the test records this rather than asserting them. Adding them would duplicate native state and is routed to a later task if owners want it.
* Static source checks only: no rendered, screen reader or conformance evidence.
