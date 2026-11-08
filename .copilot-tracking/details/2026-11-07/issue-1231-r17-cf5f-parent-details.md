---
title: Issue 1231 r17 phase details
description: Prospective phase details for the r17 parent79 cf5f57a00 merge
ms.date: 2026-11-07
---

Companion to `.copilot-tracking/plans/2026-11-07/issue-1231-r17-cf5f-parent-plan.md`. Nothing here is executed yet.

## Phase 1

* `git rev-parse HEAD^{tree}` expected 6abbdc21 at 5f904c29 before the planning commit; afterwards the planning head differs only by the four r17 files (`git diff --stat 5f904c29 HEAD`).
* `git branch backup/issue-1231-5f904-pre-r17-merge 5f904c290e81948463b651135e7ac2d9d1ba4176`.

## Phase 2

* `git merge-tree --write-tree HEAD cf5f57a0084bb3ade9b53c7d2884e0db8367c20c` one line, exit 0.
* `git merge --no-ff -m "merge: align #1231 with parent79 cf5f57a00" cf5f57a0...` with Refs #1231 and the Copilot trailer.

## Phase 3

* `git log -1 --format=%P` equals planning head and cf5f57a0.
* `git diff --raw 87c027a30 cf5f57a00` versus `git diff --raw 5f904c29 HEAD` outside .copilot-tracking: identical paths, modes and blobs; the planning head and r17 records are separate.
* For ranking_publication.py, ranking_publication_runner.py, store.py, server.py and the three test files plus src/core/README.md, blobs equal 5f904c29.
* docs/reference/log.md: `git diff 5f904c29 HEAD` shows no deleted lines.
* Static grep: 0o600 stage, `_policy_problem`, `_future`, `stage_retained`, blocked exit.

## Phase 4

* Core from src/core: `-m unittest tests.test_ranking_publication tests.test_ranking_publication_runner`, expected 70.
* API from src/api: `-m unittest tests.test_ranking_publication_wiring`, expected 18.
* `python -m ruff check --no-cache src/core src/api`, `ruff format --check --no-cache`, mypy from src/core with an external cache.
* Interpreter `/tmp/zf79venv/bin/python` and Ruff from the preserved r7 venv; print module `__file__` for core, runner and api to confirm worktree origin. Run without masked pipelines, capturing the exit code of each command.
* Ensure no __pycache__ or other ignored files remain.
