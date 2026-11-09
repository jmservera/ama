# Details: harden role survey (Refs #1189)

* Edit survey_role in src/api/checks/expected_denials_browser_check.py only.
* Success: 8 roles pass with the new asserts; mypy with tests, ruff and unit tests clean.
* Do not run the gate, benchmarks or full suites.
