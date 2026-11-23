# Changes 2026-11-23, issue 116 live r11

Tier: FULL (src change; basis: provider-boundary security control). `rpi-checks.py --all` not run; the coordinator runs gates.

## Files

* `src/core/src/zava_forward/core/ai.py`: `_utf8_size` refuses unencodable text as `input-type-not-approved`.
* `src/core/tests/test_ai_input_bounds.py`: `test_shared_boundary_refuses_unencodable_text_visibly` (3 errors without the fix).
* `docs/reference/research/issue-116-live-r11-evidence-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

core 38 OK (three boundary suites); api 57 OK; ruff check clean; mypy 3 pre-existing errors. Hosted CI not observed (no push). No Azure change, no credential read.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Allowlists at every provider boundary (unticked) | Proven offline, now including unencodable text; live payloads unproven | New failing-then-passing test; earlier matrices; payload invisible from deployed apps |
| Every role against every endpoint | Ticked; not rerun live | Prior rounds |
| Contractor view has no vulnerability reason | Ticked; not rerun live | Prior rounds |
| Free-text redaction decided | Ticked | Prior rounds |
| Roles allowed vulnerability reason (OD-14, OD-19) | Ticked | Prior rounds |
| Provider-spy zero canaries | Ticked; rerun green | Spy suite |
| Unknown task/field, excess input fail visibly | Ticked; rerun green, strengthened | Bounds suite |
| Output/citation/export recheck | Ticked; not rerun live | Prior rounds |
| Document AI derivative or exception | Ticked; rerun green | Spy suite |
| Source permissions, proposal-only, consent | Ticked; not rerun live | Prior rounds |
| Reuse current wrappers | Ticked | Same `approved_payload` |

Unproven: live payloads, independent review, hosted CI.
