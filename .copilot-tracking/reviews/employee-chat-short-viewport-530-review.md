<!-- markdownlint-disable-file -->
# Employee chat short viewport Send: review (2026-11-04)

Review executed once, inline, over [the changes](../../changes/2026-11-04/employee-chat-short-viewport-530-changes.md). Independent exact-head review and hosted CI remain required.

Outcome: conformant for scope. The sticky row is CSS only; focus order, labels and the AI-suggestion and sources text are unchanged. The sticky rule is in shared widget CSS so it also applies to the resident chat; the resident leg's pre-existing 320px failure was not made to pass or fail differently at its assertion.

Routed, open:

* Resident chat 320px composer and shared check green status (#520).
* Criterion 8: live employee verification, owner confirmation of the agent names, SQL selectors of the gate.
* Check file formatting (`ruff format`) predates this change.
