<!-- markdownlint-disable-file -->
# Asset and board AI-unavailable state: changes (2026-11-03)

Refs #226.

## Changed

* `src/api/src/zava_forward/api/web/role-screens.js`: AI report and Without AI rows.
* `src/api/tests/test_asset_board_screen.py`: new test; `run` accepts a null report.
* `src/api/README.md`, `docs/reference/research/ux/atlas-screen-trace.md`, `docs/reference/log.md`.

## Validation

* Run: unittest for `test_asset_board_screen` and `test_finance_grants_screens` (PYTHONPATH core and agents tests): 24 tests, asset tests pass; one finance test errors with `ModuleNotFoundError: zava_forward` (package not pip-installed in this worktree, unrelated to this change). ruff check and format check clean; mypy on the test file clean.
* Not run: browser and axe check, gate, benchmarks, full suites, assistive-technology testing.

## Divergences

None.
