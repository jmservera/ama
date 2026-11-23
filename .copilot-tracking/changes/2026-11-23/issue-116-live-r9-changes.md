# Changes 2026-11-23, issue 116 live r9

Tier: FULL (src change; basis: provider-boundary security control). `rpi-checks.py --all` not run; the coordinator runs gates. Witness note: the new test was written before `implement-start` was recorded (research proved the gap by a failing test), so the witness flagged pre-existing dirt.

## Files

* `src/core/src/zava_forward/core/ai.py`: `approved_payload` wraps a string `user` as one text part so strings share the type and size allowlist and are refused before the verifier and the protection hold.
* `src/core/tests/test_ai_input_bounds.py`: two tests (oversize string refused before the hold; system plus string share one budget).
* `docs/reference/research/issue-116-live-r9-evidence-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

core bounds, spy and dispatch-marker suites 36 OK; api inventories and assistant provider suites 25 OK; ruff clean; mypy 3 pre-existing errors identical at baseline. Hosted CI not observed (no push).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Allowlists at every provider boundary (unticked) | Proven offline, now including string input before the hold; live payloads unproven | New failing-then-passing test; r7 matrix; payload invisible from deployed apps |
| Every role against every endpoint | Ticked; not rerun live | Prior rounds; no credentialed sweep |
| Contractor view has no vulnerability reason | Ticked; not rerun live | Prior rounds |
| Free-text redaction decided | Ticked | Prior rounds |
| Roles allowed vulnerability reason (OD-14, OD-19) | Ticked | Prior rounds |
| Provider-spy tests zero canaries | Ticked; rerun green | Spy suite |
| Unknown task/field, excess input fail visibly | Ticked; rerun green, strengthened | Bounds suite |
| Output/citation/export recheck | Ticked; not rerun live | Prior rounds |
| Document AI derivative or exception | Ticked; rerun green | Spy suite |
| Source permissions, proposal-only, consent | Ticked; not rerun live | Prior rounds |
| Reuse current wrappers | Ticked | Same `approved_payload` |

Unproven: live payloads, independent review, hosted CI. The owner ticks the box after review.
