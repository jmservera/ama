# Changes: role survey browser test (Refs #920)

* `src/api/checks/expected_denials_browser_check.py`: `survey_role()` runs for seven staff roles and Contractor (no 4xx, no console error).
* No app, auth or knowledge-base change; no log.md entry needed.

Validation run: Chromium expected_denials_browser_check all PASS (admin-only flow plus 8 role surveys); tests.test_expected_denials (3 OK) and tests.test_employee_live_responses (8 OK); ruff check and format clean; mypy --cache-dir=/tmp/mypy-530 run as src-ci (tests included): the touched file is clean. Two unused-ignore errors remain in untouched tests/test_ai_consumption_api.py lines 22-23 in this worktree, caused by the editable installs pointing at the primary checkout (stale agents package), not by this change.
Not run: rpi-checks gate, full suites, benchmarks, axe, keyboard or screen-reader checks, hosted CI, deployment. Not security, infrastructure, SQL or deployment work.
