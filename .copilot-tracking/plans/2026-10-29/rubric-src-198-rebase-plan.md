---
title: PR 507 conflict rebase plan
ms.date: 2026-10-29
---

Task ID: pr-507-rebase-2026-10-29. Slug: rubric-src-198-rebase.
Research: .copilot-tracking/research/2026-10-29/rubric-src-198-rebase-research.md.
Details: .copilot-tracking/details/2026-10-29/rubric-src-198-rebase-phase-details.md.

## Executive Summary

Replay the existing three PR commits on fetched main, manually combine the
conflicted index and log, and retain main's rubric and scenario manifest.
No application changes are expected. Verify core/API static contracts, focused
manifest/dependency tests, rubric regressions and content preservation; obtain
one independent Review and persist a local Conventional Commit. No push means
fresh hosted CI and remote mergeability remain coordinator-owned evidence.
Candidate status: implementation-ready; single critique Complete / Pass.
Implementation status: P01/P02 complete; current local checks passed except
the explicitly inherited authoritative-main rubric failures/runtime skips.
Production scoring decision reports no scored artifact changed, baseline 77.

## User Decisions and Requirements

* Full dated Research, Plan, Implement and Review loop for draft #507.
* Rebase feat/rubric-src-198 on origin/main; preserve both sides' intent.
* Keep upstream .github/rubric/* and scenario-manifest.json exactly.
* Source only under src; tests outside packages; no legacy application code.
* Use /tmp/mv; Ruff check/format, applicable core/API mypy and relevant unittest
  modules with local/sibling src/tests paths. Full API only with lock admission.
* No Azure changes, push or issue-closing keywords; Refs #198 only.
* Conventional Commit with required Copilot coauthor; record commands/results.

## Goals

Current-main ancestry with no lost independent documentation; truthful,
reproducible local validation and review evidence.

## Scope and Non-Goals

Scope: rebase/conflict resolution, authoritative-input restoration, dated RPI
evidence and exact preservation assertions. Existing source remains upstream.
Non-goals: rubric repairs, unrelated runtime changes, full API suite,
publication/hosted CI, approvals, historical acceptance repair.

## Functional Requirements

* Keep both appended log tails and independent index paragraphs, with no markers.
* Restore protected rubric/manifest from the recorded fetched base.
* Preserve original dated RPI evidence and original adverse outcomes.

## Non-Functional Requirements

Use privacy-safe local Git identity and preserve existing coauthor trailers on
replay. No shared venv mutation, private data, cloud fallback or weakened checks.
Do not install dependencies without a concrete missing-dependency failure.

## Acceptance Criteria

* Recorded origin/main is an ancestor; no rebase/unmerged paths remain.
* Rubric/manifest byte-identical to base; main log exact prefix; original
  branch-only entries and prior RPI artifacts retained.
* Required core/API Ruff/mypy and relevant unit commands execute with actual
  results recorded; inherited failures/skips stay explicit, not green claims.
* Single critique and Review have durable outcomes and routed findings.
* Local final commit has conventional subject, Refs #198 and required trailer;
  worktree clean; no push/Azure operations.

## Test Ownership and Targets

No test additions/removals (maximum additions zero); no generated targets.
Existing core owns test_scenario_manifest and test_dependency_rule; API owns
its test_dependency_rule. Existing rubric scripts own pytest regressions.
Semantic preservation assertions compare real Git blobs, not only exit codes.
Run full rubric scripts to reassess stale counts. Do not run full API discovery.
Scenario validator runs even if upstream pinned sources appear unchanged.
No full publication gate is claimed; coordinator owns it before push.

## Phase Checklist

<!-- phase: P01 -->
### P01: Integrate authoritative main

* [x] P01-T01 Rebase, combine documentation conflicts and restore protected inputs.
* [x] P01-T02 Verify ancestry, both histories and prior artifact preservation.

<!-- phase: P02 -->
### P02: Validate and reconcile

* [x] P02-T01 Run existing static/unit/rubric commands and record exact outcomes.
* [x] P02-T02 Reconcile plan/details/changes and freeze boundary for single Review.

## Critique Disposition

One final-candidate independent critique Complete / Pass, no findings, at
.copilot-tracking/reviews/plans/2026-10-29/rubric-src-198-rebase-plan-critique.md.
No plan changes or user decision required; no repeat critique.

## Follow-Up Items

Coordinator's authorized push and exact-head hosted/publication evidence;
separately owned inherited rubric failures and historical #198 acceptance
gaps only if still evidenced. Do not expand source scope to resolve them.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-29/rubric-src-198-rebase-changes.md.
After implementation reconcile every marker before the one independent Review.
Parent owns local commit and final state after Review, not a second Review.
All implementation markers now complete. No active source work remains.
Single Review assesses the recorded base and frozen document diff, with
inherited rubric failures and unperformed publication/hosted checks explicit.
