---
title: Ranking archive ancestor durability evidence
description: Demo evidence for issue 1258 acceptance criteria
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only. Source reviewed: `src/core/src/zava_forward/core/ranking_publication.py` at the worktree head (main 42546c9221).

`_confirmed` syncs the archive folder and every parent folder opened by `_walk` after the link, on each confirmation including a retry. An `OSError` becomes `DurabilityUnconfirmedError` and the record is kept. Tests in `src/core/tests/test_ranking_publication.py` (nested ancestors, post-link failure, retries, partial ancestors, read-only and denied ancestors) and the runner suite passed: 110 tests, OK, on 2026-11-22.

These are mocked syscall-order tests; they do not show real crash or live filesystem behaviour. The FULL receipt, independent exact-head review and hosted checks remain unproven because no source changed, the full gate was not run and nothing was pushed. Per-criterion table: `.copilot-tracking/changes/2026-11-22-issue-1258-live-changes.md`.
