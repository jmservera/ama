# Issue 193 plan: scenario consumer tests (2026-11-01)

* [x] Add `src/core/tests/test_retrofit_scenario_consumers.py` (5 tests) using `retrofit_exercise_scenarios`.
* [x] Validate: unittest, ruff check, ruff format --check, mypy on the touched test.
* [x] Critique (single pass): scope tight, no production code, no heavy gate; compatible. Applied: keep helpers explicitly labelled test oracles.
* PR uses `Refs #193`; criterion 3 not proven because real #111 and #133 consumers are absent.

* Correction cycle (2026-11-01): Copilot thread on text guard validated; test now asserts the exact approved descriptive note (blacklist retained as secondary guard). No scope change.
