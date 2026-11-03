<!-- markdownlint-disable-file -->
# Asset and board evidence class: changes (2026-11-03)

Refs #226.

## Changed

* `src/api/src/zava_forward/api/web/role-screens.js`: evidence class no longer falls back to coverage; cost component needs an evidence label.
* `src/api/tests/test_asset_board_screen.py`: new test.
* `src/api/README.md`, `docs/reference/log.md`.

## Validation

* Run: `test_asset_board_screen` and `test_role_screens_conformance` (18 tests, pass); screen test discovery (106 tests) has 2 errors that also occur without my change (`zava_forward` not pip-installed here). ruff check and format check, mypy `--cache-dir=/tmp/mypy-226` on the test file: clean.
* Not run: browser and axe check, gate, benchmarks, full suites, assistive-technology testing.

## Divergences

None.
