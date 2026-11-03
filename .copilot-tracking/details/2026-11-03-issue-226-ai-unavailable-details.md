<!-- markdownlint-disable-file -->
# Asset and board AI-unavailable state: details (2026-11-03)

## Phase 1

`assetCost(report)` adds an "AI report" row (Loaded or Unavailable text) and a "Without AI" row (manual path to Programme manager or Finance owner records) before the cost rows. Plain language per the content standard; textual state, no colour signal.

## Phase 2

`tests/test_asset_board_screen.py`: `run(None)` shows Unavailable and the manual path with the stock conflict table still present; a loaded report shows Loaded and no unavailable text.

## Phase 3

Docs: `src/api/README.md` #226 paragraph, `docs/reference/research/ux/atlas-screen-trace.md` row, `docs/reference/log.md` entry.

## Phase 4

Commands: unittest for asset and finance screen tests, ruff check and format check, mypy with `--cache-dir=/tmp/mypy-226`.
