---
title: PR 501 main rebase plan
description: Reconcile the resident content branch without losing upstream work
ms.date: 2026-10-29
---

Task ID and slug: `pr501-main-rebase`.

## Executive Summary

Rebase the existing draft onto fetched main, retaining both documentation
histories and applying the resident draft disclaimer to the refactored case
view. Restore upstream rubric and manifest bytes, run relevant engineering
checks, obtain one independent Review and commit dated evidence locally.
No push, Azure action, issue closure or human acceptance is part of this task.

## User Decisions and Requirements

* Execute all four RPI phases with dated artifacts.
* Rebase `docs/resident-ux-153` for draft PR #501 onto `origin/main`.
* Preserve both sides of index/log changes; take main's rubric and manifest.
* Source belongs in `src/`; tests stay outside packages; no legacy code.
* Validate Ruff check/format and core/API mypy plus relevant unittest modules
  in `/tmp/mv`, with local src/tests and sibling paths.
* Do not run full API discovery unless the nonblocking heavy lock succeeds.
* Do not modify Azure or push. Commit using Conventional Commits and the
  requested Copilot trailer. Use Refs #153, not issue-closing keywords.
* Record exact commands, failures and results in the changes artifact.

## Goals

Preserve behavior from both the resident copy increment and current main;
leave a clean, locally committed candidate with auditable integration checks.

## Scope and Non-Goals

Resolve rebase conflicts and tightly coupled test/copy issues only. Preserve
historical RPI outcomes. No redesign, dependencies, cloud, heavy full suite,
new business scope, PR publication or owner approvals.

## Functional Requirements

* Keep upstream refactored case sections/tabs/chat and branch no-send/review
  disclaimer, representative expiry label and proposal/time-capture copy.
* Preserve both index/log entries exactly once.
* Main's `.github/rubric/` and scenario manifest are canonical generated
  targets, not objects for manual regeneration.

## Non-Functional Requirements

Use `/tmp/mv`, explicit local imports, native semantics and current Fluent 2
content boundaries. No new exemptions, silent skips or broad catches.
Keep failures as evidence; hosted CI and human acceptance remain separate.

## Acceptance Criteria

* Latest fetched main is an ancestor; no unresolved Git conflicts.
* No branch delta in rubric or manifest; manifest test passes current pins.
* Ruff check/format and applicable core/API mypy pass.
* Focused content/design/accessibility/resident/assistant/UI tests pass,
  with skip counts explained, and changed JS parses.
* Independent critique dispositions and one Review are retained.
* Successful local candidate closeout requires a passing Review with no
  unresolved blocking findings. Record nonblocking findings with owner/reason.
  A blocker prevents a success claim; no second Review is scheduled.
* Local Conventional Commit has required trailer; nothing pushed.

## Test Ownership and Evidence Boundary

Core owns `test_scenario_manifest`, dependency checks and resident authority
tests; API owns `test_content_standard` and the relevant UI/HTTP modules.
No test removals. Maximum additions: two regression methods in the existing
content test if integration requires them; prefer preserving existing tests.
Canonical tests remain outside packages. Static lexical/syntax assertions are
regressions, not rendered usability, screen-reader or operational acceptance.
Run existing design-system browser check if locally available; report failures
instead of weakening it. Full API discovery is not planned.

## Phase Checklist

<!-- P01 -->
### P01: Rebase and reconcile

* [x] P01-T01 Rebase onto main and resolve documentation/UI conflicts.
* [x] P01-T02 Restore main rubric/manifest and verify intended branch delta.

<!-- P02 -->
### P02: Validate

* [x] P02-T01 Run Ruff, formatting, mypy, focused units and JS syntax checks.
* [x] P02-T02 Record commands/results and reconcile source/evidence.

<!-- P03 -->
### P03: Review and local delivery

* [x] P03-T01 Execute one independent Review and route residual findings.
* [x] P03-T02 Commit implementation and dated original evidence; do not push.

## Critique Disposition

One critique executed: Complete / Revise, one Medium PC-001.
Applied directly: P03 and acceptance now gate successful local closeout on a
passing Review without unresolved blockers. No user decision or second
critique required. Original critique preserved.

## Follow-Up Items

Coordinator publication, exact-head hosted CI and retained human wording/
resident usability/AT acceptance are outside this local integration.
Repository-wide complete publication gate remains required by repository
instructions, but no publication is authorized here. Do not equate targeted
validation with its receipt.

## Handoff

Research: `.copilot-tracking/research/2026-10-29/pr501-main-rebase-research.md`.
Details: `.copilot-tracking/details/2026-10-29/pr501-main-rebase-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-29/pr501-main-rebase-changes.md`.
Completion: all local plan items complete. Review execution Complete,
outcome Conformant with justified divergence, no findings or blockers. Source
fingerprint matches. Implementation/original evidence committed as `57ec5c95`;
tree clean and main ancestry verified. The final evidence-only closeout records
that result without changing reviewed source. No push is authorized or made.
