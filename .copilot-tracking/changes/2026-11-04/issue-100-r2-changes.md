# Changes: issue 100 r2

* Core unchanged: main already reports `by_capability` as a dict (after merging main, the duplicate list was dropped).
* src/core/tests/test_ai_consumption.py: breakdown test.
* src/api/src/zava_forward/api/web/role-screens.js: capability table on the asset and board view.
* src/api/tests/test_asset_board_screen.py: two screen tests.
* docs/reference/log.md: entry.

Run: core tests test_ai_consumption and test_ai_consumption_demo (39 OK); api test_asset_board_screen (15 OK); ruff check and format, mypy (core 253 files, api 178 files) clean.
Not run: rpi-checks gate, browser/axe, full suites, benchmarks, Azure.
