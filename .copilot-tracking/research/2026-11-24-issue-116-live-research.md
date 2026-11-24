# Issue 116 live research (2026-11-24)

Disposition: executed (rereading r1-r12 notes and `approved_payload` in src/core ai.py).

* Four of five boxes plus six of seven RAI boxes are ticked; only "allowlists at every provider boundary" is open.
* Caller inventory test (src/api/tests/test_ai_boundary_caller_inventory.py) classifies every Ai.run/evidence/look_at/_chat caller; all funnel through `Ai._request_body` -> `approved_payload`.
* Gap found: `approved_payload` bounds text bytes and decoded image bytes but not the number of parts. A list of millions of empty text parts or empty images passes every size allowlist and reaches the provider body unbounded. Real callers send at most 2 parts (`look_at`).
* Live payload contents are not observable from the deployed apps (no provider capture), so live proof of the box is not possible.

Planning Readiness: Ready.
