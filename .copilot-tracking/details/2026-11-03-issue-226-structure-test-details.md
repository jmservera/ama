<!-- markdownlint-disable-file -->
# Asset and board structure test: details (2026-11-03)

## Phase 1

Test 1 renders with report absent, empty and failing quality. Asserts every section uses `card screen-record` with an h2 first, no h1 or h3, every table has a caption and column-scoped headers, every blocked block carries the text "Cannot confirm readiness", and no click handlers. Test 2 scans the asset-board source for simulator or role-switch terms.

## Phase 2

`docs/reference/log.md` entry.

## Phase 3

unittest for `tests.test_asset_board_screen`, `tests.test_design_system`, `tests.test_accessibility_baseline`; ruff check and format; mypy strict with `--cache-dir=/tmp/mypy-226`.
