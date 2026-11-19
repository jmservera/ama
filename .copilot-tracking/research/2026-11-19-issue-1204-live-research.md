# Research: issue 1204, run 2026-11-19

Task: issue-1204-live. Disposition: executed (builds on the 2026-11-18 note
`docs/reference/research/coordinator-contract-criteria-1204-live-2026-11-18.md`).

## Unmet criterion

Only one box is unticked: "Every tick has an actual next action and bounded closure-review
progress ... expired approvals and freshly granted approvals are reconciled without treating one
blocked lane as a global stop."

The 2026-11-18 note proved the instruction text and left runtime liveness unproven: nothing reads
the `tick_log` rows that the agent file (lines 147-150) says each tick must record, and no
executable check turns the contract into pass/fail.

## Proposed implementation

A new offline tool `tools/check-tick-log.py` that validates an exported `tick_log` (JSON list or
JSON lines) against the contract: each tick has an action and evidence or is flagged no-progress;
two consecutive no-progress ticks while ready or unassessed work remains need a recovery action in
the second tick; closure-review batches are at most five and never repeat an item; expired
approvals return only their scope to human-blocked; no tick may stop globally while ready work
exists. Synthetic fixtures only; no network, no Azure.

## Planning readiness

Ready. Tier: FOCUSED (tools only, no src, no SQL, no security, no infrastructure).
