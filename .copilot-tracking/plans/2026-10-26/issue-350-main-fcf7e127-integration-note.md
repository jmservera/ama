<!-- markdownlint-disable-file -->
---
title: Issue 350 main fcf7e127 integration note
description: Prospective integration note, written before the merge
ms.date: 2026-10-26
---

Written 2026-10-26 before the merge. Topic head `ea6aaceb4b881486be88158cf138e4fa41be4fe9`, clean; remote `a9bdae31` is an ancestor. Fresh `origin/main` after a GitHub fetch: `fcf7e12735c9e4e69f83df9d643ec8e28a981409` (merge base `acafc6ee`; shared runner fix from PR 437 merged). Earlier artifacts and reviews are unchanged.

Scope overlap: main changes 76 paths, including `tools/rpi-checks.py`, `tools/test_rpi_checks.py` and `.github/rubric/scores/latest.json`. The topic changed none of these, so path overlap is empty. `git merge-tree --write-tree HEAD origin/main` is conflict-free. Main's rubric score and any log entries are taken verbatim, with no score synthesis and no log rewrite. The checker and its tests are not touched by main.

Plan: normal `git merge --no-ff origin/main`; then cheap checks only (88 focused tests in the topic-bound venv, ruff check line-length 100 and format check on the test file, confirm the checker, tests and earlier artifacts are unchanged); commit; freeze a clean candidate and an external future gate plan under /mnt. No full gate, Docker, browser, push or PR edit; the 444 gate holds the lock and 462 is next. Scope is bounded integration, not acceptance; the original 350 acceptance criteria stay unmet where unproved.
