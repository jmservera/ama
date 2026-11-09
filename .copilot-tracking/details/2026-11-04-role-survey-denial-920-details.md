# Details: role survey browser test (Refs #920)

## Phase 1

* Add `survey_role()` using the existing owned server; append a Contractor staff record to the synthetic data.
* Use fixed 1.5 s settle per route, as the existing admin loop does; no network beyond loopback.
* Success: 8 roles pass with empty denied and error lists.

## Phase 2

* Run the check, `tests.test_expected_denials`, `tests.test_employee_live_responses`, ruff check and format, mypy `--cache-dir=/tmp/mypy-530`.
* Do not run the gate, benchmarks or full suites.
