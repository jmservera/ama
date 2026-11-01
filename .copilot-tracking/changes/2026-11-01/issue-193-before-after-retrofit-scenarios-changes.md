# Issue 193 changes

* Added `retrofit_exercise_scenarios()` and `EXERCISE_LABEL` to `src/core/src/zava_forward/core/synthetic/sensor_scenarios.py`.
* Added `test_retrofit_exercise_scenarios_cover_outcomes_and_label_values` to `src/core/tests/test_sensor_scenarios.py`.
* Added a pointer paragraph to `src/core/README.md` (scenario pack section).
* Validation: `unittest tests.test_sensor_scenarios` (16 OK), ruff check, ruff format --check, mypy src/core: all pass. No heavy gate run; CI is the evidence.
* Divergence: none. AC3 remains unmet (no #111/#133 consumer tests exist).
