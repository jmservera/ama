# Details: 432 chat failure meter forwarding

## Phase 1
Provider stub returns envelopes with `meter_id`/`meter_root` for: timeout, disabled, empty returned text, completion-check failure, revocation. Assert `exc.meter_id`/`exc.meter_root` equal; `calls==1`. Pre-dispatch denial: ids None, calls 0. Non-string ids are dropped to None.

## Phase 2
Helper `_failure(outcome, calls, usage, envelope)` builds `ModelUnavailable(outcome, calls=, usage=)` and sets `meter_id`/`meter_root` attributes (str only, else None). Works with the base signature and with the sibling kwargs. `src/core` and `dispatch.py` unchanged: Ai.evidence already keeps ids in failure envelopes.

## Phase 3
Run `python3 -m unittest discover -s tests -q` in src/agents, core test_ai_consumption, ruff check/format, mypy.

## Critique dispositions (rubber-duck, REVISE, applied directly)
* PC-001: all admission exits also go through the helper so both attributes are always present (None pre-dispatch).
* PC-002: ids follow the envelope, not the call count; add a real `Ai.evidence` test where a reservation exists but transport fails (calls may be 0 or 1) and a test where the reserve itself is held (no ids).
