---
title: Issue 1231 r16 phase details
description: Prospective phase details for the r16 parent79 alignment
ms.date: 2026-11-07
---

Date: 2026-11-07. Companion to `.copilot-tracking/plans/2026-11-07/issue-1231-r16-87-parent-plan.md`. Prospective; nothing here has been executed.

## Phase 1 details: preconditions

* `git rev-parse HEAD HEAD^{tree}` must be a4ada1e91841143239a0aec33024e4b9788b05e5 and 472f82b23c3d236bad3ca64e110bdf830174f88e, unless the planning commit that follows this record is the only difference. In that case the planning HEAD must differ from a4ada1e9 only by the four r16 prospective files (`git diff --stat a4ada1e9 HEAD`).
* `git rev-parse 87c027a30ba5a1dd5e4f16b01052e7c32a09138c^{tree}` must be f391682d93bac1ce9ec256c6d02dfebf9bda4dc4.
* `git merge-base --is-ancestor 357e842d... 87c027a3...` and the same for HEAD.
* `git status --short --ignored` empty. Parent worktree status is read only, never edited.
* `git branch backup/issue-1231-a4ada-pre-r16-align a4ada1e9` (the plan commit is on top; use the planning HEAD name in the final report as the true pre-merge head and keep a4ada1e9 as the source baseline).

## Phase 2 details: merge

* Dry run: `git merge-tree --write-tree --merge-base=357e842d064296d4764f087f7a39006cc702f4ee HEAD 87c027a30ba5a1dd5e4f16b01052e7c32a09138c`; exit 0 and one line.
* Because the planning commit only adds new record paths, the expected merged tree equals a00c8d19 plus those four files. Compare with `git diff --stat` rather than assuming.
* Commit message: `merge: align #1231 with parent79 87c027a30` with `Refs #1231` and the Copilot trailer; identity `8036360+jmservera@users.noreply.github.com`.
* Conflict policy: stop on any conflict, abort with `git merge --abort`, report files; do not hand-pick sides.

## Phase 3 details: static proof

* `git diff a4ada1e9 HEAD --stat -- src` must list only ranking_publication_runner.py, test_ranking_publication_runner.py and src/core/README.md.
* `git diff 87c027a3 HEAD --stat -- src` must list only child-side files (helper, store, API wiring test, helper test, runner hunk, README hunk).
* `git show HEAD:src/core/src/zava_forward/core/ranking_publication.py | grep -n 0o6` must show only 0o600 for the stage open.
* Runner file must contain `_policy_problem`, `_future`, `stage_retained` and the `("refused", "blocked")` exit.

## Phase 4 details: focused checks

* Interpreter and Ruff come from the previously used external environments (`/tmp/zf79venv/bin/python`; Ruff 0.17.1 via the preserved g1231-r7 venv). Install nothing unless a command fails for a missing dependency; then pip into an owned external environment, never uv, never PYTHONPATH=mvp.
* Core run from src/core, API run from src/api, with PYTHONDONTWRITEBYTECODE=1. mypy cache external. Final ignored-inclusive status must be empty.
* Expected baselines at the child: core publication/runner 66 tests, API wiring 18 tests; parent adds runner tests, so counts rise. Record actual counts.

## Phase 5 details: optional regressions

* Future-date versus winner: seed an archive holding a record dated after the run date and assert `verify` and non-exercise `publish` follow the parent behaviour; separately assert a helper-level concurrent loser still returns the winner's recorded date.
* Double-failure: runner refusal with a failing link and failing unlink keeps `stage_retained`, no path, and the parent's refusal shape.
* Do not touch the parent's tests; add only to existing files if a gap exists.

## Phase 6 details: records

* New files only, named `issue-1231-r16-87-parent-*` for changes, review and state. Do not edit this research, plan, details or critique after the planning commit; amendments go to changes.
* Review is author-written and not independent; it separates execution status from outcome and routes residuals.
