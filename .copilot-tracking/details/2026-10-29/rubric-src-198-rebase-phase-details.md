---
title: PR 507 conflict rebase phase details
ms.date: 2026-10-29
---

Task ID: pr-507-rebase-2026-10-29. Slug: rubric-src-198-rebase.
Plan: .copilot-tracking/plans/2026-10-29/rubric-src-198-rebase-plan.md.

<!-- phase: P01 -->
## P01: Integrate authoritative main

<!-- task: P01-T01 -->
### P01-T01: Rebase and resolve

Starting clean HEAD 6c85c6d7e662824b56e0db2d05e31ace301dade5; fetched
main 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7.
Only new task-owned tracking files may be untracked at rebase start.
Set repository-local authenticated privacy-safe email before continuation.
Run `GIT_EDITOR=true git rebase origin/main`. Inspect every conflict at each
replayed commit; manually combine README index entries and append-only log.
Retain updated upstream wording where it supersedes stale branch context.
Use `git restore --source=origin/main --staged --worktree -- .github/rubric
docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`
when the index can be updated safely, before final completion verification.
Completion: no rebase state/unmerged paths; upstream inputs exact.

<!-- task: P01-T02 -->
### P01-T02: Verify preservation

Compare main log as byte prefix and each branch-only original appended section.
Confirm upstream/branch index entries coexist and original prior artifacts
match starting HEAD, not just filenames. Use Git blobs and actual doc diffs.
Check no source/infra/legacy delta versus main, and `git diff --check`.
Completion: actual content and ancestry assertions pass.

<!-- phase: P02 -->
## P02: Validate and reconcile

<!-- task: P02-T01 -->
### P02-T01: Existing validation

From src/core, export
`PYTHONPATH=src:tests:../agents/src:../agents/tests`, then /tmp/mv/bin/python
`-m ruff check .`, `-m ruff format --check .`, `-m mypy`,
`-m unittest -q test_scenario_manifest test_dependency_rule`.
From src/api use
`PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests`
and the same static commands plus `-m unittest -q test_dependency_rule`.
Confirm imported namespace paths resolve this worktree before shared editable
roots. From root run `python3 -m pytest .github/rubric/scripts -q -ra` and the
existing `python3 tools/rename-zava-tests.py`. Preserve failing counts and
missing-runtime skips. No full API suite or heavy lock acquisition is needed.
Completion: each command has actual exit/result; no unsupported CI-green claim.

<!-- task: P02-T02 -->
### P02-T02: Reconcile evidence

Synchronize all plan markers/details and changes with implementation, validation
limits and follow-ups. Record source/document diff hash and reviewed base.
Single independent Review assesses frozen non-tracking delta and all evidence.
No source fixes or repeated Review after that Review; findings route later.
Parent persists final local commit with required identity and trailer.

## Validation Boundary

Tests added/removed: none. Source/generated code edits: none planned.
Main rubric/scenario inputs are immutable for this task. Existing CI names,
protections and issue state remain unchanged. No Azure resource operation.

## Completion Evidence

P01-T01/P01-T02 complete: all three commits replayed, two conflicts combined,
main ancestry and protected-input identity passed. Actual preservation
assertions retain main's entire log prefix, original branch log tail, all
upstream index body lines and fourteen original tracking artifacts byte-exact.
P02-T01 complete: core/API lint, format, mypy and 12 focused tests passed;
scenario source pins validated unchanged. Migration runner passed 25 tests
using /tmp/mv after system Python lacked presentation dependencies.
Full rubric scripts: 18 failed / 355 passed / 7 missing-runtime skips;
rubric and workflow failure inputs match upstream exactly.
P02-T02 complete: plan markers/details/changes reconciled, preservation and
three added local links/anchors rechecked, production rubric decision confirmed
no scored artifact changed (baseline 77). Complete validation counts are
execution evidence, not a conformant suite or hosted CI claim.
Frozen document diff SHA-256:
1def559c27d81d2f652c6b3437eedf0642e6057745660650352e75ef29d52247.
Base remains 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7.
