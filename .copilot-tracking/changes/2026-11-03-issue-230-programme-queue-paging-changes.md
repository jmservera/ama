# Changes: issue 230 programme queue paging

* `src/api/src/zava_forward/api/web/role-screens.js`: paged queue (Previous page, Next page), page status, failure message.
* `src/api/tests/test_programme_screen.py`: two paging tests.
* `docs/reference/research/ux/atlas-screen-trace.md`, `docs/reference/log.md`: trace row and log entry.

Divergences: none. Web-design-guidelines source fetched 2026-11-03 and applied (labelled native buttons, role=status live region, no outline or transition changes).

Validation run: unittest test_programme_screen, test_role_screens, test_role_screens_conformance, test_design_system, test_content_standard (53 OK, run with PYTHONPATH to src dirs); ruff check and format check; mypy --strict --cache-dir=/tmp/mypy-230 on the test file.
Not run: gate, browser/axe check (story 230 does not cover paging), full suites, benchmarks, assistive technology.
