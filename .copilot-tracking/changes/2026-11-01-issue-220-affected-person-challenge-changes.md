# Changes: affected-person challenge route (issue 220), 2026-11-01

* Added `src/core/src/zava_forward/core/challenges.py` (digital and staff-recorded routes, permitted explanations, owner, next update, resolution evidence, dependent-only staleness).
* Added `src/core/tests/test_challenges.py` (9 tests).
* Updated `src/core/README.md` with a section for #220.
* Validation (src/core): unittest `test_challenges` 9 passed; ruff check, ruff format --check and mypy clean on touched files. No heavy local gate by owner direction; CI is the evidence.
* Divergences: none. Store, API and UI wiring deferred (see plan scope).
* PR #641 review fixes: dependency parents materialised at construction (generator-safe); `review` and `resolve` validate date and evidence before mutating the record; added 3 `Robustness` tests.
