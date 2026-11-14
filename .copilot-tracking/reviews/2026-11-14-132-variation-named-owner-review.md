# Review: #132 named-owner variation and escalation routing (2026-11-14)

Execution: one self-review, executed. Outcome: conformant for the bounded slice, with qualifications. Independent exact-head review and hosted CI are still required and not done.

* Placeholder owners rejected, role allow-list preserved: verified by tests.
* `contract_instruction` enforced as exactly False and surfaced in API and UI: verified by tests; the UI rows are not browser-tested.
* No write endpoint, contractor access, permission or consent change was added.
* Open item: the delivery/identity decision (ADR #1150 acceptance) stays an owner matter; `Closes #132` is therefore a claim only for the AC listed, and the PR should use `Refs #132` unless the owner accepts that gate. Routed follow-up: browser/AT check of the new rows; full core suite run in CI.

## Cycle 1 correction review (1 of 5)

Execution: one self-review, executed. Outcome: findings 1, 2, 3 and 4 addressed for the API and core boundary; independent exact-head re-review and hosted CI still required.

* Finding 1: `field-escalate` is wired end to end (staff-only 403, work-order lookup 404, named owner required, advisory only) and persists on the case and audit log across a JSON store restart (tested). The SQL path reuses the same case body and audit mechanism but its test class is opt-in and was skipped.
* Finding 2: placeholder, hyphen, underscore, slash, email and role-only owners and placeholder contacts are rejected (tested). `governance._looks_placeholder` does not exist in this checkout.
* Finding 3: HTTP fail-closed and restart tests added; no state or audit mutation on rejection.
* Finding 4: counts corrected (see changes).
* Routed, not done: `staff-intake.js` still shows a static advisory line and has no escalation form or readback (review finding 3), so `Closes #132` is not claimed; the commit uses `Refs #132`.

## Cycle 2 correction (2 of 5)

Fixed independent cycle 1 findings: escalation summary held for roles without a recorded need (advisory note kept), staff-intake.js escalation form, readback and computed contract-instruction text, non-string and dotted-initial owner rejection, README and AC5 numbering. Focused core/api tests, ruff and mypy pass. Browser, SQL Server, human AT and hosted CI not run. Refs #132.
