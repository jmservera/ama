# Changes: issue #232 resident-staff browser evidence

* `src/api/checks/role_screens_browser_check.py`: new story 232s; 232 and 232s join STORY_ACCESSIBLE; resident-staff branch of the accessibility check; 232s queue region check.
* `src/api/README.md`: documents stories 232 and 232s.

## Validation run (2026-11-03, focused)

* `python3 -m checks.role_screens_browser_check 232` and `232s` with pinned axe 4.10.3 (sha256 verified): all PASS, axe 0 violations, 0 incomplete, Tab reached every table region, reflow at 320, 390, 1280 px, no POSTs, local Chromium 156, synthetic loopback.
* ruff check and format check on `checks`: pass. mypy (`--cache-dir=/tmp/mypy-232`) on the changed file: pass.
* unittest test_resident_choice_screen, test_resident_service_screen, test_role_screens, test_role_screens_conformance: 26 OK.

## Not run

The local gate, `rpi-checks.py`, benchmarks, full suites and other browser stories were not run. No assistive-technology or human testing.
