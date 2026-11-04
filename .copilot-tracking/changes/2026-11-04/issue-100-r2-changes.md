# Changes: issue 100 r2

* src/core/src/zava_forward/core/ai_consumption.py: `by_capability` in the report.
* src/core/tests/test_ai_consumption.py: breakdown test.
* src/api/src/zava_forward/api/web/role-screens.js: capability table on the asset and board view.
* src/api/tests/test_asset_board_screen.py: two screen tests.
* docs/reference/log.md: entry.

Run: core tests test_ai_consumption and test_ai_consumption_demo (39 OK); api test_asset_board_screen (15 OK); ruff check and format, mypy (core 253 files, api 178 files) clean.
Not run: rpi-checks gate, browser/axe, full suites, benchmarks, Azure.
