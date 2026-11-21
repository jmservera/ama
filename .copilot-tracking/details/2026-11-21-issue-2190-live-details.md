# Details: issue 2190

* tools/rpi-checks.py: `_region_passed` accepts `ok` on any region line; `_test_header_indexes` requires `name (dotted.id) ... `; exact and required-test parsers merge docstring headers.
* src/api/checks/employee_chat_browser_check.py: `wait_for_load_state("networkidle")` before the `before` snapshot.
* src/api/tests/test_rai_release_readiness_api_218.py: `REQUEST_TIMEOUT_S = 120` plus a budget test.
* tools/test_rpi_checks.py: accepting and rejecting regression tests.
