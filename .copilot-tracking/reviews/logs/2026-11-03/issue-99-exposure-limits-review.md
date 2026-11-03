<!-- markdownlint-disable-file -->

# Review: issue-99-exposure-limits

Execution: once, by the implementing agent against the diff. Independent exact-head review and human approval remain required. Outcome: Conformant for the slice, with open acceptance criteria.

## Criteria

* AC1 envelope and tolerances recorded as human-approved inputs, not invented: UNMET. The mechanism rejects inputs without an approval record, but no actual Board-approved figures exist, and nothing persists them.
* AC2 a breach produces a pause signal for a human decision: PARTIAL. Logic proven by unit tests on synthetic values; not wired into any store, API or screen, so no live breach can occur yet.

## Findings routed to later work

1. Persist approved limits with change provenance and expose a read route (stacked slice 2).
2. Resident-staff UI panel with manual path and AI-independent behaviour (slice 3).
3. Board supplies OD-12 and OD-15 inputs; owner decision.

No AI feature is added. Resident consent and human approval boundaries unchanged.
