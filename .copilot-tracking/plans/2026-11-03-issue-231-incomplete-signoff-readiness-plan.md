# Plan: issue #231 slice 4, incomplete sign-off records block readiness

* [x] `signoffState` in `role-screens.js`: a "Signed off" record needs a named person and a design version, else not ok
* [x] Add `test_incomplete_signoff_record_cannot_show_readiness`
* [x] Run focused unit tests, ruff, mypy

## Critique (one pass, inline)

Verdict: proceed. Keep read-only, no new controls, no staleness threshold, keep older-version sign-offs valid. No finding conflicted with a confirmed decision. Validation tier: focused; no security, infrastructure, SQL or deployment change.

Details: the message reads "Signed off record is incomplete: no named person / no design version" and flows into the existing "Cannot confirm readiness" reasons.
