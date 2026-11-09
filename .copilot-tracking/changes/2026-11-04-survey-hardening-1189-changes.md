# Changes: harden role survey (Refs #1189)

* src/api/checks/expected_denials_browser_check.py: assert me.user.role equals the mapped role and navigation is non-empty; wait for networkidle and 500 ms after the last route before asserting.

Validation run: Chromium check exit 0 (44 PASS); tests.test_expected_denials (3 OK); ruff check and format clean; mypy --cache-dir=/tmp/mypy-1189 from src/api as src-ci (tests included): no issues in 186 files.
Not run: rpi-checks gate, full suites, benchmarks, hosted CI. Not security, infrastructure, SQL or deployment work.
Acceptance: all three items met (both asserts, final settle, check green); the issue's wording says me.role, the field is me.user.role.
