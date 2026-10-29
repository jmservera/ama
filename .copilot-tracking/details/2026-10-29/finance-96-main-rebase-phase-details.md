<!-- markdownlint-disable-file -->
# RPI Phase Details: finance-96-main-rebase

Date: 2026-10-29. Task ID / slug: finance-96-main-rebase.
Plan: .copilot-tracking/plans/2026-10-29/finance-96-main-rebase-plan.md.

## P01: Rebase and preserve integration

### P01-T01

Initial branch clean at 373ab192, no active rebase. Main fetched at
356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7. Replay e114bc45 and 373ab192.
Workflow-created untracked artifacts belong to this task; do not stash/delete
other work. Use git rebase origin/main; inspect every unmerged stage.
In rebase terminology, ours is main plus replayed commits; theirs is the
finance commit. Do not select either globally. Preserve additions on both
sides of docs/reference/README.md and docs/reference/log.md.
For rubric/manifest paths restore exactly origin/main if a conflict appears.
Use noninteractive GIT_EDITOR=true git rebase --continue after staging
only resolved files. No push or history rewrite beyond requested local rebase.

### P01-T02

Compare range-diff and net main-to-candidate diff; examine endpoint dispatch,
Store private projection and combined mypy overrides. Verify main ancestor,
rubric directory and scenario manifest equality. Hash/compare seven original
2026-10-27 finance artifacts against pre-rebase commit 373ab192.

## P02: Validate and prepare local handoff

P01 complete: six actual conflicts resolved additively. Main ancestor,
protected-file equality, historical byte preservation and README/log retention
verified. P02-T01 complete: core/API lint, format, mypy and 237 selected tests
(54 existing optional SQL Server skips) succeeded. No test additions/removals.

### P02-T01

Use /tmp/mv/bin/python; /tmp/mv currently has other-worktree editables.
From src/core, use PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests.
From src/api, use PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests.
Assert zava_forward.core/api/agents module files resolve under this worktree.
Run python -m ruff check ., python -m ruff format --check ., python -m mypy
in both core and API; run the plan's combined focused unittest selectors.
Re-run test_scenario_manifest because upstream updated pinned sources.
If a concrete integration failure occurs, investigate/fix it and rerun affected
selectors. Do not repair unrelated main debt or weaken existing gates.
Do not run full API discovery unless the caller's lock probe succeeds;
if actually run, retain the lock throughout. Default is focused testing.

### P02-T02

Changes artifact records every meaningful command, result and limitation.
Preserve original critiques/Reviews and new one-pass evidence.
Finish implementation/reconciliation before independent Review. Commit with
Conventional Commit subject, Refs #96 and Copilot trailer, authenticated
8036360+jmservera@users.noreply.github.com author/committer.
No remote push: hosted CI/mergeability cannot be freshly asserted.
The repository publication receipt is not manufactured; complete local gate,
exact-head publication assessment and hosted approval remain separate.
Final read-only checks: clean worktree, ancestor check, branch, commit/trailer,
remote ref unchanged. If main moves, report the exact reviewed base honestly.

Pre-Review reconciliation: all implementation and validation complete;
P02-T02 local evidence commit is the remaining implementation bookkeeping
operation. Independent Review assesses that committed integration candidate.
Review findings route to follow-up work, not another fix/Review loop.
