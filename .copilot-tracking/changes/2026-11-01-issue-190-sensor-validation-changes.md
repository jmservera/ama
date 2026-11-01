# Changes: sensor validation consumer contract (issue 190), 2026-11-01

* Added `src/core/tests/test_sensor_retrofit_consumer_contract.py` (2 tests, per-profile subTests; exercise tolerances 0.5 C / 2.0 RH points labelled as such).
* Updated `src/core/README.md` with a pointer to the contract as the fixture for #111/#133.
* Validation: `unittest` for the new, scenario and plausibility modules (25 tests OK); ruff check, ruff format --check and mypy clean on the new file. No heavy local gate; CI is the evidence.
* No divergences from plan. Plan items 1-3 done; 4 follows in the PR.
