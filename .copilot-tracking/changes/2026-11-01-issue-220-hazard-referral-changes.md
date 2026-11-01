# Changes: issue 220 hazard referral follow-up, 2026-11-01

* `src/core/src/zava_forward/core/challenges.py`: `hazard_concern` flag, `hazard_referral` record, `hazard_referrals()`.
* `src/core/tests/test_challenges.py`: `HazardConcern` (2 tests); 14 pass.
* `src/core/README.md`: documented behaviour.
* Validation: ruff check, ruff format --check, mypy clean on touched files. Divergences: none.

## Correction cycle (PR 693)

* Merged `origin/main` cleanly (no conflicts).
* `challenges.py`: `confirm_hazard_handoff` validates evidence before mutation.
* `test_challenges.py`: rejected blank evidence leaves referral listed and `referred_on_receipt`.
* Validation: ruff check, ruff format --check, mypy clean in `src/core`.
