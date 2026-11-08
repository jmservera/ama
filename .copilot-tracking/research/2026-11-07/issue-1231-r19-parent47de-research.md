---
title: Issue 1231 r19 research, local alignment to parent79 47de325d
description: Prospective research for one normal merge of local parent79 47de325d into the child
ms.date: 2026-11-07
---

Disposition: executed (read-only), committed before the merge. r15 deviation and r16 to r18 records are preserved.

* Child start cfc78dbffb205743a5154d98440d4d884cec5fbb / tree de8bc0c7, ignored-clean, branch fix/ranking-archive-concurrent-writer-metadata. PR1242 OPEN, base feat/ranking-publication-runner-79.
* Local parent79 (issue-79-publisher) 47de325d80eda5665f3e3d3250fedce7a17c85d1 / tree 46f69e5e2af3538bc40725a9fc88b1a73684128b, ignored-clean. Prior parent 9b21a6a0 is the merge-base.
* Main a1d265340ba7d6f14b24e028362b2d5f4bb80126 is an ancestor of the parent; not fetched or moved here.
* Incoming 9b21a6a0..47de325d: commits 8d9caf976, 573c86fee, 47de325d8 plus main a1d26534 (#1252). Outside .copilot-tracking: docs/reference/log.md (append-only), tools/backlog-sync.py, tools/test_backlog_sync.py. No src change.
* Child owns ranking source, tests and README; no overlap. Dry run was clean (tree 3f97c0d9 before planning files).
* Selectors: core `tests.test_ranking_publication tests.test_ranking_publication_runner` (70), API `tests.test_ranking_publication_wiring` (18), `tools/test_backlog_sync.py` if it needs no service, Ruff, format, mypy.
* Another worktree holds the sole FULL; no heavy lock, service or main merge is touched.
