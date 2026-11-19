---
title: Research for issue 1258 (live demo run)
ms.date: 2026-11-18
---

Opening note. Prior worktree `issue-1258-20261118T0629Z` concluded main already holds the fix (PR #1328).
This run re-verifies against `origin/main` baf24bf5b by reading source and running tests.

## Finding

Main already contains the fix (PR #1328). 110 tests in `test_ranking_publication` and the runner pass; the
module fails against `cd687abad^`; mypy clean. Evidence note: `docs/reference/research/issue-1258-archive-ancestor-durability-2026-11-18.md`.
Planning readiness: Ready, disposition `satisfied-and-skipped` for source implementation. Tier: FOCUSED (no src change).
