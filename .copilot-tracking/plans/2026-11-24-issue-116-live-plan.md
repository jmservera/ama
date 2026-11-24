# Issue 116 live plan (2026-11-24)

* [ ] Add `MAX_PARTS = 8` to `approved_payload`; refuse more as `input-too-many-parts` before verifier, hold and meter.
* [ ] Add one test in src/core/tests/test_ai_input_bounds.py (9 empty text parts refused; 2 accepted).
* [ ] Run core targeted tests, api consumers, ruff. Write research note r13, index/log, changes, review. Local commit.

## Critique (executed once)

Verdict: accept. Risk: a cap could break a real caller; `look_at` sends 2 parts and the only list callers are tested. Alternative of rejecting empty images was dropped because the part cap already bounds them and existing tests send small payloads. Tier: FULL (src change), `rpi-checks.py --all` not run by the worker.
