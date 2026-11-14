# Research: #128 AC2 and AC3 (missing data review, aggregate-only usability)

Planning Readiness: Ready. Disposition: executed.

* `src/core/src/zava_forward/core/journey_register.py` already routed missing source, sensor, support and incomplete appointments to `human_review` with `rank_effect: none`, covered by `tests/test_journey_register.py`.
* Gaps: no named human reviewer on the route; `appointment_history` of `None` or a non-string, and `missed`, were not treated as incomplete; no aggregate-only usability reporting existed (no staff-surveillance rejection).
* `paired_equity.py` consumes `human_review_route(subject)["rank_effect"]`; the signature stays backward compatible.
* Constraints: no invented thresholds (minimum cell size is owner-approved, absent means blocked); `role-screens.js` untouched; not usability evidence (AC3 user research protocol remains a human decision).
