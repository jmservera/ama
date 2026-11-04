# Changes: admin-only landing (Refs #920)

* Files: server.py, app.js, test_expected_denials.py, expected_denials_browser_check.py.
* Run: `tests.test_expected_denials` (3 OK); `checks/expected_denials_browser_check.py` Chromium (all PASS, no console errors for staff and admin-only); related unit tests content_standard, role_endpoint_inventory, workbench, accessibility_baseline (48 OK); ruff check clean; mypy --cache-dir=/tmp/mypy-920 clean on src and the check.
* Pre-existing: `ruff format --check` flags the browser check file before and after this change.
* Not run: rpi-checks gate, full suites, benchmarks, axe, keyboard or screen-reader evidence, deployment, live re-check.
