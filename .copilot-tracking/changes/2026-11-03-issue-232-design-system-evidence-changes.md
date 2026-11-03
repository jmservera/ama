# Changes: issue #232 design-system and no-simulator evidence

* src/api/tests/test_role_screens.py: inventory-class and no-simulator unit test.
* src/api/checks/role_screens_browser_check.py: `check_design_system_use` for stories 232 and 232s.
* src/api/README.md: describes the new checks and their limits.

## Validation (focused tier)

* Run: unittest tests.test_role_screens and tests.test_accessibility_baseline (15 OK); `checks.role_screens_browser_check 232` and `232s` (local Chromium 156, all PASS); ruff check and format; mypy with --cache-dir=/tmp/mypy-232.
* Not run: axe scan (pinned axe 4.10.3 file unavailable here, so skipped, not passed), local gate, rpi-checks, benchmarks, full suites, other stories. No assistive-technology or human testing.
