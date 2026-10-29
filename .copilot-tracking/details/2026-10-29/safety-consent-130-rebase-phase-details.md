---
title: Safety consent PR 509 rebase phase details
ms.date: 2026-10-29
---

Task ID: pr-509-rebase-2026-10-29. Candidate implementation details.

## Execution Reconciliation

P01-T01/T02 complete: two README conflicts resolved by retaining both full
sections; range-diff shows only insertion context changes. Main's controlled
files and log/index are unchanged; both topic commits replayed successfully.
P02-T01/T02 complete: project-wide Ruff/format/mypy all pass; core 383 tests
(87 skips), API 120 (one skip), migration 25 (no skips). No source/test repair,
addition, removal or generated-output update was necessary. Exact commands
and qualified integration boundaries are in the dated changes artifact.
P03-T01 complete; independent Review and final commit/handoff remain.

## P01: Rebase integration

### P01-T01

Initial branch is clean and matches open draft #509. Starting head `fa665644`;
fetched main `356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7`.
Run `git rebase origin/main`. Observe conflict hunks, not assumptions. In a
rebase, ours is the rebased main side and theirs the replayed topic commit.
Preserve referral/tenure privacy and hold logic plus newer store behavior.
Keep both README additions and any append-only log/index entries.
Continue with noninteractive editor; do not skip a topic commit to hide conflict.

### P01-T02

Compare rubric directory and scenario manifest directly against main, verify
ancestor relationship and `git diff --check`. Inspect retained two-commit patch
with range-diff. Historical RPI evidence is not to be rewritten.

## P02: Validation and bounded repair

### P02-T01

Use `/tmp/mv/bin/{ruff,mypy,python}` from each component. `ruff check .`,
`ruff format --check .`, `mypy` use existing project-wide policy.
Set `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests`
as applicable. Run relevant existing modules rather than full API discovery:
core resident decisions, hazard referral, consultation, quality/procurement;
API resident and hazard plus consultation/procurement modules if present.
Also run API `test_ai_tasks` (owner `src/api/tests/test_ai_tasks.py`) to preserve
main's briefing authorization, programme versus assigned selection, projected
status minimisation and entitlement-sensitive cache behavior (PC-001).
Opt-in SQL skips must be recorded, not claimed as integration acceptance.
Restore dependencies only following an actual missing-dependency failure.

### P02-T02

Locate the existing `test_scenario_manifest` owner and run it using current
main's pins; tests must establish source integrity rather than refreshing
digests blindly. Run owning dependency-rule tests and migration regression.
Repair only a demonstrably rebase-related failure. Lock maximum additions and
ownership are defined in the plan; no deletions or generated fixture writes.

## P03: Review and local handoff

### P03-T01

Changes artifact records literal commands, outcomes, test counts/skips,
conflict decisions, amendments and any divergence. Reconcile all task markers
and known blockers before dispatching Review.

### P03-T02

Fresh independent worker activates `rpi-review`, reads exact current candidate
against fetched main and canonical RPI evidence, and writes only the designated
Review artifact. One Review; residual findings route to follow-up, not a second
implementation/Review loop. No human acceptance is marked complete.
Excluded operational/human residuals do not block this local integration.
Material in-scope source defects or failed mandatory checks do block readiness:
preserve the adverse Review and return the blocker to the coordinator (PC-002).

### P03-T03

Use authenticated GitHub noreply address for author and committer. Preserve
rebased authorship; new Conventional Commit includes `Refs #130` and Copilot
trailer, no closing keywords. Commit dated evidence with the candidate.
Check clean worktree, ancestor and controlled-file equality. Do not push.
Full publication receipt and hosted exact-head checks remain explicitly unrun.
If Review is blocking, label any evidence commit blocked/not ready and do not
present it as accepted. Do not silently repeat Review or repair after that gate.
