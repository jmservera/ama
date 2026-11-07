---
title: Issue 1231 details r6 (retained-stage wording accuracy)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 about 14:15Z, after the r6 Plan file was completed and before any edit or check. Plan: `.copilot-tracking/plans/2026-11-06/issue-1231-r6-stage-wording-plan.md`.

## P01 Edit the two wording sites

* P01-T01 Helper docstring. In `ranking_publication.py` replace "(stage_retained, a hard-link alias of the record that an operator removes)" with conditional wording: the retained stage may share the archived record's bytes and inode when this call committed it, but a stage of a call that lost the race is a separate file whose content can differ, so an operator checks it before removing. Wrap lines within the existing docstring style.
* P01-T02 Runner warning. In `ranking_publication_runner.py` replace "It is a hard-link alias of the record and must not be edited." with "It may share the archived record's bytes, so do not edit it." Keep code, stage name and next action.
* Use apply_patch for edits. No change to logic, keys, outcomes, README, store, server or tests.
* Done when: grep for `hard-link alias` in `src/` returns nothing, and `git diff --stat` shows only these two source files.

## P02 Focused checks (once, after both edits are finished)

* Interpreter: read-only `/tmp/zf79venv/bin/python` (shared, not isolated, unpinned tools), with `PYTHONPATH` set to this worktree's `src/core/src`, `src/core/tests`, `src/api/src`, `src/api/tests`, `src/agents/tests`. Print `__file__` of `ranking_publication` and `ranking_publication_runner` as import proof. `PYTHONDONTWRITEBYTECODE=1`; caches and logs under `/mnt/ama-gates/e1231-r6-r68-1106/`.
* One combined unittest selection: `test_ranking_publication`, `test_ranking_publication_runner` (their cleanup and concurrent-loser classes are covered by running the modules; the module runs are small) and `test_ranking_publication_wiring` for the API storage-error route.
* Ruff check, Ruff format --check and mypy on the edited ranking files, using the same config the repository uses (as in R5).
* Compare tracking blob hashes of all files under `.copilot-tracking` present at HEAD `e5486018` with the working tree after the run; all must match.
* Keep raw outputs unmodified; a failure is reported, not rerun into a pass.

## P03 Records and freeze

* Changes record after checks; separate author Review after the Changes; final state; commit with fresh `gh api user` noreply identity for author and committer, Conventional message, Copilot trailer, no amend.
