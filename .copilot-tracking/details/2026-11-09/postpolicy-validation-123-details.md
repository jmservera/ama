<!-- markdownlint-disable-file -->
# Phase details: post-policy validation of recovered #123, 2026-11-09

Plan: [plan](../../plans/2026-11-09/postpolicy-validation-123-plan.md).

Critique amendments (PC-001 to PC-004) are applied below.

## Phase 1

* Pre-merge guard (PC-003): require HEAD `572fc4729b59e6d41c831536e3841251b860f263`, `origin/main` `9814cf6b236be1f2e86c4401973b8e834be927bc` and a clean tracked tree; stop on mismatch.
* From the worktree root: `git merge --no-ff -m "<Conventional Commit message with trailer>" origin/main`. Use repository-local `user.email` `8036360+jmservera@users.noreply.github.com` (resolved via `gh api user`, already configured) for author and committer.
* Expected: clean merge, only main's seven non-tracking docs paths and its tracking files added; `docs/reference/log.md` auto-merges.

## Phase 2

* `git merge-base --is-ancestor` for `b46a9ad9a`, `572fc4729`, `cfd1bca`.
* `git rev-parse HEAD^1 HEAD^2` equals frozen candidate and `9814cf6b2`.
* `git diff --name-only 572fc4729 HEAD -- 'src/**/*.py' 'src/**/*.sql' 'src/**/tests'` must be empty (PC-001); `src/README.md` changes are documentation and reviewed in Phase 4.
* `git diff --check 572fc4729 HEAD -- . ':!.copilot-tracking'` must be clean; record any inherited trailing-whitespace findings under `.copilot-tracking/` without editing them (PC-002).
* Record the tested merge SHA and tree; the later evidence commit must add only `.copilot-tracking/` files (PC-004).

## Phase 3

Run from `src/core` with the pinned venv first on PATH:

* `ruff check .` and `ruff format --check .` (expect 216 files formatted).
* `mypy` (expect 269 source files).
* `PYTHONPATH=src:tests python -m unittest test_paired_equity test_cohort_eval test_household_conditions test_retrofit_effects test_monitoring_coverage test_rule_engine test_chat_privacy -q` (expect 146 tests, 0 skips); print `zava_forward.core.paired_equity.__file__` to prove worktree import provenance.

## Phase 4

Check relative links in the merged `src/README.md`, `docs/reference/log.md` new entries and `docs/reference/README.md` resolve to existing files; review the merged diff of log.md for append-only integrity (no earlier entry changed).

## Phase 5

Write changes and review records, update state JSON, commit evidence files only (no logs or receipts), report HEAD/tree.
