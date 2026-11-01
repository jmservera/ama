# Changes: affected-person challenge route (issue 220), 2026-11-01

* Added `src/core/src/zava_forward/core/challenges.py` (digital and staff-recorded routes, permitted explanations, owner, next update, resolution evidence, dependent-only staleness).
* Added `src/core/tests/test_challenges.py` (9 tests).
* Updated `src/core/README.md` with a section for #220.
* Validation (src/core): unittest `test_challenges` 9 passed; ruff check, ruff format --check and mypy clean on touched files. No heavy local gate by owner direction; CI is the evidence.
* Divergences: none. Store, API and UI wiring deferred (see plan scope).
* PR #641 review fixes: dependency parents materialised at construction (generator-safe); `review` and `resolve` validate date and evidence before mutating the record; added 3 `Robustness` tests.
* PR #641 second Copilot review (3 threads): challenge IDs skip existing entries so a prepopulated register is never overwritten; dependency graph nodes are now `(kind, id, version)` tuples so only dependents of the corrected version go stale; `unittest.main()` guard moved to the end of `test_challenges.py`. Tests now 12 passed; ruff and mypy clean.

## Correction cycle 2 (2026-11-01)

Copilot thread on challenges.py: resolving a challenge dropped a pending hazard referral from the listing. Fix: `hazard_referrals()` lists referrals with status `referred_on_receipt` regardless of challenge status; new `confirm_hazard_handoff()` (named owner, non-empty evidence) marks `handed_off`. Test and README contract updated. Validation: ruff check, ruff format --check, mypy clean; tests.test_challenges 14 pass. Human review remains required.
