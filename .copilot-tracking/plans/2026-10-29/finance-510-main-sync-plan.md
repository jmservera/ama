<!-- markdownlint-disable-file -->
---
title: Finance PR 510 main synchronization plan
description: Bounded local integration plan and acceptance evidence
ms.date: 2026-10-29
---

## Task Metadata

* Task ID / slug: `finance-510-main-sync`.
* Date: 2026-10-29.
* Planning status: Ready; single critique Complete / Revise, both findings
  directly resolved without a second critique.
* Phase details: .copilot-tracking/details/2026-10-29/finance-510-main-sync-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-29/finance-510-main-sync-plan-critique.md.

## Executive Summary

Rebase the existing finance branch on fetched main, retaining the independent
monitoring and finance documentation and all later finance source fixes.
Use main's rubric/manifest copies, existing local package static checks and
focused regression modules, then commit dated evidence without pushing.

### What You May Not Know

GitHub currently marks the PR non-draft. The latest Source CI/rubric runs await
action and have no executed jobs. The PR body's original defects were fixed
by later commits with their own independent Conformant Review. Preserve both
historical outcomes; this task neither grants financial approval nor claims
hosted CI success. No local implementation blocker is known.

## Sources

* .copilot-tracking/research/2026-10-29/finance-510-main-sync-research.md, C1-C6.
* .github/workflows/src-ci.yml; src/core/pyproject.toml; src/api/pyproject.toml.
* Original finance and source-guard RPI evidence remains immutable.

## User Decisions and Requirements

* Execute the full dated RPI loop for PR #510 / branch `docs/finance-96`.
* Fetch/rebase on main; preserve both sides, especially log/index entries.
* Take main's `.github/rubric/*` and scenario manifest, checking pinned sources.
* Keep code in `src/`, tests outside packages, with no legacy implementation.
* Use `/tmp/mv`, explicit local/sibling source and test paths, Ruff lint/format,
  core/API mypy and relevant unittest modules.
* Do not run full API discovery without nonblocking heavy-lock admission.
* Do not create/modify Azure resources or push; coordinator publishes.
* Make a Conventional Commit with the required Copilot co-author trailer,
  references only, without issue-closing keywords.
* Record actual commands/results, failures and limitations in changes evidence.

## Goals

Retain source behavior and historical evidence while eliminating local merge
conflicts against the assessed main SHA. Establish the requested local check
results and provide an unpushed, reviewable candidate for coordinator handoff.

## Scope and Non-Goals

In scope: authorized local replay, additive conflict resolution, main-owned
generated files, targeted validation, dated evidence and one independent Review.
Out of scope: feature expansion, financial authority, issue/PR mutation,
Azure, remote CI dispatch, pushing, merging and publication-gate waiver.

## Functional Requirements

* FR1: main is an ancestor; no unfinished rebase/conflict markers remain.
* FR2: retain all main/finance index/log entries and finance code/test behavior.
* FR3: protected rubric tree and scenario manifest equal main exactly.
* FR4: original RPI evidence remains byte-identical.

## Non-Functional Requirements

* NFR1: no new production/test modules, test removals or exemptions are planned.
  Maximum new tests: zero. Existing canonical targets are package external
  `src/core/tests` and `src/api/tests`; generated target is main's score only.
* NFR2: local import assertions prove current worktree use despite shared
  editable installations. Do not reinstall/mutate `/tmp/mv` unnecessarily.
* NFR3: semantic preservation comes from range-diff and original-source
  comparison; regression evidence comes from existing finance/staging/role/
  provenance/manifest/dependency tests. No test creates approval authority.
* NFR4: keep validation light. Full API discovery is not selected, so no heavy
  admission is claimed. A required full publication gate remains coordinator
  work, not an excuse to push without evidence.
* NFR5: set absolute worktree-local `TMPDIR` and disable bytecode/static caches
  to keep synthetic fixture output bounded. Enforce the assessed main SHA
  before replay and use it for all preservation comparisons.

## Acceptance Criteria

* AC1: successful rebase, main ancestry and clean final worktree.
* AC2: main index lines retained plus finance block, both append-only log
  entries retained, protected files equal main, original evidence unchanged.
* AC3: core/API configured Ruff check, format check and mypy pass.
* AC4: selected core/API unittests and scenario-manifest test pass with actual
  totals/skips recorded. Imports resolve to this worktree.
* AC5: independent critique and single Review preserved; local Conventional
  Commit contains dated evidence/trailer, no push/Azure mutation.
* AC6: hosted CI/approval/publication limits are explicit, not marked passed.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase and preserve integration intent

Dependencies: finalized critique and clean pre-existing worktree (verified).

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Replay finance commits and resolve documented overlaps

Retain original start/base IDs. Rebase without autostash, dropping unrelated
work or changing branch. Resolve additive docs; restore main rubric/manifest.
See matching details section.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and deliver local candidate

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run scoped regression and static checks

Assert imports, preservation, ancestry and protected paths, then run current
package checks and selected modules. Record actual exits, totals and skips.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Complete one Review and local evidence commit

Reconcile plan/details/changes before Review. Review integration once, retain
all outcomes and route findings without same-task correction/re-review.
Resolve GitHub identity, configure repository-local privacy-safe attribution
and commit exact task changes with the Copilot trailer. No push.

## Dependencies

Existing tools and installed distributions in `/tmp/mv`; GitHub read access
for attribution/metadata; no cloud dependency for the selected local checks.

## Critique Disposition

Execution: Complete. Original verdict: Revise. No repeat critique.

| Finding | Owner and disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High | Planner; accepted as bounded fixture-output hygiene | NFR5 and details P02-T01 require absolute project-local TMPDIR and explicit bytecode/cache controls. The critique's claimed universal prohibition on `/tmp` is not a caller requirement; its operational suggestion is compatible and adopted without endorsing that broader premise. |
| PC-002 Medium | Planner; directly resolved | NFR5 and details P01-T01 require main-SHA equality, captured start/merge-base and immutable preservation comparisons; changed base requires reconciliation. |

Executive summary, current requirements and details are reconciled. No
significant or divergent user decision remains.

## Follow-Up Items

* Coordinator: publication gate, fresh hosted checks/required action and
  potentially stale PR body. Outside local no-push integration scope.
* Finance/template/Board owners: actual approved inputs remain unavailable.
  Outside source integration and not evidence for issue acceptance.

## Handoff

Changes artifact: .copilot-tracking/changes/2026-10-29/finance-510-main-sync-changes.md.
P01/P02-T01 complete: rebase and local preservation/static/focused tests pass.
Ready for one independent integration Review, then P02-T02 local commit.
No unresolved local design decision; hosted approval cannot be established
by this local task.
