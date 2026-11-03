# Changes: issue #227 cross-home hazard referral queue

* `src/api/src/zava_forward/api/web/role-screens.js`: shared `hazardQueue` summary for `safety-lead` and `hazard-triage`.
* `src/api/tests/test_safety_screens.py`: cross-home summary test.
* `src/api/README.md`: short description.
* `docs/reference/log.md`: entry.

Validation (focused): `tests.test_safety_screens` and `tests.test_role_screens` pass (15 tests) with `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests`; ruff check, ruff format --check and mypy on the test pass. Browser check, gate and full suites not run (coordinator runs the gate). No amendments or divergences.
