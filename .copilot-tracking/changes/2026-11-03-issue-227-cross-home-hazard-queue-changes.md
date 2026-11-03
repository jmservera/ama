# Changes: issue #227 cross-home hazard referral queue

* `src/api/src/zava_forward/api/web/role-screens.js`: shared `hazardQueue` summary for `safety-lead` and `hazard-triage`.
* `src/api/tests/test_safety_screens.py`: cross-home summary test.
* `src/api/README.md`: short description.
* `docs/reference/log.md`: entry.

Validation (focused): `tests.test_safety_screens` and `tests.test_role_screens` pass (15 tests) with `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests`; ruff check, ruff format --check and mypy on the test pass. Browser check, gate and full suites not run (coordinator runs the gate). No amendments or divergences.

Correction note (2026-11-03, after reviewer findings; the original review outcome is unchanged):

* A home whose case returns no hazard list now shows "Unknown. Hazard list not supplied"; a home flagged `hazard` in the list but returning no hazards shows a mismatch row. Neither reads as "no hazard".
* Released items without decision evidence show "Release decision evidence: open the home" in the Pause status cell.
* `roleScreensView` calls `screen.summarise` when no home is selected; a unit test now proves it.
* The cross-home table now has separate Sent, Received and Accepted columns; tests assert awareness time, destination, the three steps and pause status.
* State: critique recorded as executed inline in the plan; mode manual, session stopped.
* Validation (focused): tests.test_safety_screens and tests.test_role_screens, ruff check, ruff format --check, mypy.
