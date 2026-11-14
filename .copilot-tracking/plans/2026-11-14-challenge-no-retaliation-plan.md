# Plan: issue #220 assurance flags

* Add `challenges.assurance()` and `stamp_assurance()` (verify protected state, then stamp the record).
* Stamp on challenge open, resolve and nomination correction; add to `view()` and `detail` as `challenge_assurance` (permitted readers only).
* Render `#challenge-assurance` note in `panels.js`.
* Tests in `src/api/tests/test_challenge_non_retaliation_hazard_guard.py`.
* Critique: executed once, self-review; compatible, no conflicts. Validation tier: focused (targeted tests, ruff, mypy).
