---
title: Case journey round five correction plan
description: Complete three-thread correction and sibling-path audit for PR 529
ms.date: 2026-10-28
---

## Task Metadata

Task `526-pr529-round5-20261028`, automatic full loop; branch
`feat/case-journey-ux-526`, intake `1d36e8b3`.

## Executive Summary

Clear only successfully submitted chat text, prevent restored proposal editors
from offering unavailable acceptance, and announce AI count changes from the
always-visible summary without repeatedly announcing unchanged content.
Audit sibling dirty, readiness and status paths before one independent Review.

### What You May Not Know

Both chat handlers are in chat.js, not the dirty-listener location in the
thread. Publication remains blocked by the required full gate's az dependency;
commit validated local work and original evidence for the coordinator.

## Sources

Research: .copilot-tracking/research/2026-10-28/case-journey-526-round5-research.md.
Details: .copilot-tracking/details/2026-10-28/case-journey-526-round5-phase-details.md.

## User Decisions and Requirements

* Full RPI loop for the three open Copilot threads and sibling instances.
* Existing branch/worktree, fast-forward bot changes first; done at intake.
* Focused journey/workspace units and both browser checks with axe.
* Nonblocking shared heavy lock, retries bounded to 40 minutes; no Azure/secrets.
* Ruff 100 columns; Conventional Commit with required Copilot trailer.
* Retain Refs #526. Coordinator owns push/replies/resolution if az blocks gate.

## Goals

Correct all three failures without losing newer drafts or weakening review gates.

## Scope and Non-Goals

Production targets: chat.js, assistants.js, case-workspace.js. Related app.js,
ops.js, panels.js and existing HTML/CSS are audit-only unless a tightly coupled
sibling defect requires correction. No framework/style overhaul or server changes.
Canonical tests: src/api/tests/test_case_journey.py and existing browser checks.
No generated source targets. Removals: none. Maximum new unit methods: three,
one executable lifecycle regression per defect; extend existing browser checks.
Semantic coverage tests actual shipped functions; browser regressions use real DOM
and controlled network timing. No duplicate test harness or gate scan-count change.

## Functional Requirements

* Snapshot both raw question values before dispatch. Clear matching text and dirty
  marker after success only; preserve newer text, failures and unrelated dirtiness.
  Retain the complete chat panel in the case session so same-case redraws retain
  pending controls, handler state, thread identity, text and completion cleanup.
* Save edited proposal uses the same ready and own-verification condition as
  Accept/Edit; restored text stays visible, selectable and copyable.
* Summary count text has one atomic polite live region, separate from navigation
  and panel availability status. Equal count text causes no DOM mutation.

## Non-Functional Requirements

Preserve Fluent/native semantics, tab focus, revision binding, manual paths and
approval/consent boundaries. No new dependencies. Preserve 38 journey axe scans.
Distinguish local evidence from full gate, hosted or manual acceptance.

## Acceptance Criteria

* Both chats: unchanged success clean; later raw/whitespace text remains dirty;
  failed thread or answer retains question; pending keyboard resubmit blocked.
  Repeat unchanged/later/failure paths across unrelated case-save redraws.
* Restored same-revision editor: save disabled for stale, nonready, nonactionable,
  denied, old epoch or another verifier; ready own verification enables all three.
* Summary: loading/count/unavailable transitions visible on Overview with AI
  panel hidden; one polite count text region; repeated counts do not reannounce.
* Focused units, both browser checks with pinned axe, JS parse and owning
  Python Ruff/format/type checks pass. No unresolved in-scope defect at handoff.
* One independent critique disposed and one independent post-implementation Review
  preserved; no claim that automated checks establish screen-reader conformance.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and regress the state paths

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement chat cleanup and both timing regressions

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Align editor readiness and regress restored states

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Deduplicate polite summary updates and audit siblings

<!-- rpi:phase id=P02 -->
### [x] P02: Validate, independently review and commit

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused units, lint/types and locked browser checks

Depends on P01-T01/T02/T03. Use flock -n with absolute 2400-second deadline,
short retries and owned short TMPDIR; retain original failures and final logs.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence, execute one Review, commit local handoff

Depends on P02-T01. Authenticate author via gh api user and configure local
privacy-safe identity. No push/full gate invocation while az is prohibited.

## Critique Disposition

One independent critique executed, original verdict Revise preserved at
.copilot-tracking/reviews/plans/2026-10-28/case-journey-526-round5-plan-critique.md.
PC-001 applied directly: retain the complete chat panel per case session, and
exercise both pending handlers across a same-case redraw with unchanged/newer/
failure and duplicate-submit subcases. No user decision needed. Plan Ready.

## Follow-Up Items

* RV-001 later bounded test correction completed and validated separately:
  final journey 207 assertions/38 scans; original Review Defects found preserved.
* Coordinator complete exact-head gate, publication and thread resolution.
* Human screen-reader/staff acceptance remains separate; no new claim made.

## Handoff

P01 and P02 complete; 17 focused units, 43 related contracts, owning lint/
format/types/JS parse, final journey 207 assertions/38 axe scans and assistants 58
checks/10 axe scans pass. Sole Review Complete / Defects found retained, and
RV-001 later bounded correction validated without another Review. Source and
original dated evidence committed as 6f836a68459dbafee5a6c3382b1d62366c8fcd67
with verified safe identity/trailer and clean worktree. This final documentation
reconciliation accompanies the coordinator handoff. Full publication gate remains
blocked; no remote action or acceptance is implied by task completion.
Changes: .copilot-tracking/changes/2026-10-28/case-journey-526-round5-changes.md.
