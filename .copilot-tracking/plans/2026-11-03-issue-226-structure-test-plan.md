<!-- markdownlint-disable-file -->
# Asset and board structure test: plan (2026-11-03)

Task: `issue-226-structure-test`. Refs #226. Research: [../research/2026-11-03-issue-226-structure-test-research.md](../research/2026-11-03-issue-226-structure-test-research.md). Details: [../details/2026-11-03-issue-226-structure-test-details.md](../details/2026-11-03-issue-226-structure-test-details.md).

* [x] Phase 1: add structure and no-role-simulator tests to `src/api/tests/test_asset_board_screen.py`.
* [x] Phase 2: knowledge-base log entry.
* [x] Phase 3: focused tests, ruff, mypy; record changes and review.

Critique: executed once inline; verdict accepted. Risk: tests couple to the shared helper markup. Mitigation: they assert only semantic structure. No user decision needed.
