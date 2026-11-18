# Review c1: review-fix cycle 1 (Refs #110)

Date: 2026-11-14. Execution: executed once. Outcome: conformant for the focused tier.

* Finding 1 (High): addressed; `decode` verifies live envelopes and `_live_shape` uses `reading_id_for`.
* Finding 2 (High): addressed; end-to-end redelivery and tamper tests pass.
* Finding 3 (Medium): addressed; type, seconds and grid enforced.
* Open: seeded-schema rows are not envelope-verified by design; hosted CI and independent exact-head review remain pending.
