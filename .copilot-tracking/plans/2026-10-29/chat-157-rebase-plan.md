---
title: Chat 157 rebase plan
ms.date: 2026-10-29
---

## Task Metadata

Task ID: 503-chat-157-rebase-2026-10-29. Branch: feat/agent-chat-157.

## Executive Summary

Rebase onto fetched main and surgically preserve chat accounting/provenance
alongside #506 conflict routing, offline usage and bounded audit snapshots.
Deliver a locally committed candidate with focused CI evidence, not a push
or claim of fresh hosted/human acceptance.

## Sources

.copilot-tracking/research/2026-10-29/chat-157-rebase-research.md;
origin/main 3e742ef1; current branch 2931b7f1.

## User Decisions and Requirements

* Full dated Research, Plan, Implement and Review; rebase this existing branch.
* Keep both append-only/index contributions; main owns rubric and manifest.
* Preserve bounded audit read and chat accounting; no mvp source.
* Use /tmp/mv, focused chat/regulatory tests, Ruff and core/API mypy.
* Full API tests only after nonblocking shared-lock admission.
* Commit Conventional Commit plus requested coauthor trailer; no push or Azure.
* Refs #157 only, no issue-closing keywords.

## Goals

Make current main an ancestor while retaining both behaviors and passing
applicable local CI selectors.

## Scope and Non-Goals

Conflict resolution, coupled regression tests, local static checks and evidence.
No new feature, UI redesign, resource provisioning or historical evidence edits.

## Functional Requirements

All direct regulatory writers persist actor_role, preserving copied roles or
unknown legacy roles; main's conflict referral and bounded reads remain.

## Non-Functional Requirements

No private dataset reads; source under src only, tests outside packages.
Keep main rubric/manifest exact, preserve locks and unrelated work.

## Acceptance Criteria

No pending rebase/conflicts; fetched main ancestor; main-owned paths identical.
Focused chat/regulatory/manifest and affected package static checks pass.
Record exact commands, exits/skips and validation boundaries in changes.
One independent critique and one independent post-implementation Review.
No push. Hosted green/remote mergeability remains coordinator-dependent.

## Test Ownership and Locked Boundary

Core owns chat/accounting/audit regressions, agents owns model/eval, API owns
HTTP/role isolation. Exact test removals: none. Maximum new tests: two focused
regressions if existing tests miss composed behavior. Canonical code is src;
no generated source targets. Preserve main's manifest bytes, do not regenerate
hashes unless approved scope demands it. Validate pinned sources with existing
test_scenario_manifest. Semantic checks cover role provenance, conflict
referral/offline usage and bounded reads; regression selectors preserve chat.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase and compose
<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Rebase on origin/main; retain both docs and main-owned files.
<!-- rpi:task id=P01-T02 -->
* [x] P01-T02: Resolve regulatory writer refactor and role/accounting composition.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate
<!-- rpi:task id=P02-T01 -->
* [x] P02-T01: Restore /tmp/mv existing dependencies after observed missing import.
<!-- rpi:task id=P02-T02 -->
* [x] P02-T02: Ruff/check-format/mypy; focused core/agents/API and manifest tests.

<!-- rpi:phase id=P03 -->
### [x] P03: Review and persist
<!-- rpi:task id=P03-T01 -->
* [x] P03-T01: Independent single Review; reconcile artifacts and commit locally.

## Critique Disposition

One independent critique Complete / Revise; original preserved at
.copilot-tracking/reviews/plans/2026-10-29/chat-157-rebase-plan-critique.md.
PC-001 accepted: acceptance-invalidating Review findings block ready handoff,
not silently deferred. PC-002 accepted: exact selectors and behavior mapping
added to details. Caller-required source/test PYTHONPATH retained, supplemented
by installed-import provenance checked without PYTHONPATH.
PC-003 accepted: shared setup/full discovery require held nonblocking lock.
PC-004 rejected: no temporary-directory prohibition applies to this parent
execution; caller explicitly requests /tmp/mv and the lock, both accessible.
The critic's differing environment limitation is not evidence of a parent
blocker. PC-005 accepted: full fetched base/old head pin and comparisons in
changes. No second critique. Implementation ready after direct dispositions.

## Follow-Up Items

* Coordinator push and fresh hosted checks; actual human/SQL/live acceptance
  and complete publication receipt remain separate from this focused rebase.

## Handoff

Details: .copilot-tracking/details/2026-10-29/chat-157-rebase-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-29/chat-157-rebase-changes.md.
P01-P03 complete locally. Reviewed implementation/evidence commit
5faa132970904d15ef159b328efdad802eb5fd67 verified. Single Review Complete /
Residual work, implementation Conformant; original outcome unchanged.
RV-001 persistence fulfilled; RV-002/003 remain coordinator-owned follow-ups.
No push, no Azure, no hosted-green or full publication-readiness claim.
