# Changes: admin-only case-data routes (Refs #920)

* app.js: plain-language page for admin-only accounts on all case-data routes (minimal web edit).
* Browser check and unit test extended.
* log.md entry appended.

Validation run: tests.test_expected_denials (3 OK); content_standard, role_endpoint_inventory, workbench, accessibility_baseline, workspace_scripts (56 OK); Chromium expected_denials_browser_check 12 PASS; ruff check and format; mypy (--cache-dir=/tmp/mypy-920, as src-ci, tests included) clean; node --check.
Not run: rpi-checks gate, full suites, benchmarks, axe, keyboard or screen-reader checks, deployment. Not security/infra/SQL work.
