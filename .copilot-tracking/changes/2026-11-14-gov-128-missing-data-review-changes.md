# Changes: #128 AC2 and AC3

* `src/core/src/zava_forward/core/journey_register.py`: reviewer assignment, `unassigned` and `dropped` counts, stricter incomplete-appointment detection, `aggregate_usability`.
* `src/core/tests/test_journey_register.py`: two new tests.
* Validation: `python3 -m ruff check` pass; `ruff format --line-length 100 --check` pass; 49 focused unittest cases pass (journey_register, paired_equity, journey_acceptance, journey_trace).
* Not run: full local RPI gate, hosted CI. Not pushed. `role-screens.js` unchanged.
