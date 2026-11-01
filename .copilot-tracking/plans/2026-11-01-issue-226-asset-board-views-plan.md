# Plan: issue 226 asset executive and board views (2026-11-01)

1. Add `assetBoardScreen` registration to `role-screens.js` (load: portfolio count and `/api/ai/report` consumption; render: panels above).
2. Add node-vm tests in `src/api/tests/test_asset_board_screen.py`: unknown handling, owner naming, source age, no approval/form/button controls, portfolio separate, AI cost Unknown without token-only figure, textual states, no GET other than reads.
3. Validate: unittest for new and role_screens tests, ruff check, ruff format --check, mypy for src/api.
4. Commit, push, PR (Refs #226 unless all criteria proven).

Critique (single pass, self): keep read-only; do not infer eligibility; cost shows Unknown unless server supplies ratio with evidence label and quality Pass. Accepted. Reject adding a new role (not required).

## Correction cycle 2 (PR 710)

Parse dates in `queue_rows` only, normalise output, add cross-home mixed-format regression. Critique (single pass, self): compatible, applied directly.

## Correction cycle 3 (PR 710)

Add the route to the role inventory so every role is exercised against it. Critique (single pass, self): compatible, applied directly.
