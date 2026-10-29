---
title: Chat widget 550 rebase plan
description: Local-only main integration and validation
ms.date: 2026-10-29
---

Task: 550-rebase. Slug: chat-widget-550-rebase. Parent: 550.

## Executive Summary

Rebase the two existing chat commits onto fetched main ecbb5a80, retaining
main's case journey/map work and both README sections. Run fresh project
static checks, related units and actual chat/browser integration. Independently
review once, then commit dated evidence locally. No push or Azure actions.

## User Decisions and Requirements

* Rebase feat/chat-widget-550 onto origin/main; preserve both conflict intents.
* Keep append-only log/index entries; main owns rubric and scenario manifest.
* Source remains under src/, tests outside packages; no legacy application code.
* Use /tmp/mv, explicit project/sibling source and test paths.
* Full API discovery requires successful nonblocking heavy-lock admission.
* Run chat unit and browser checks; Conventional Commit with required coauthor.
* Reference issue 550 without issue-closing keywords. No push or PR creation.

## Goals

Produce a conflict-free, locally validated integration for coordinator handoff.

## Scope and Non-Goals

Resolve integration conflicts and tightly coupled test failures only. Do not
redesign the application, alter protected scoring/pins, change dependencies
without a demonstrated missing prerequisite, access private data or provision.

## Functional Requirements

Both shared chat audiences and main's compact journey/map behavior survive.
README retains chat, case journey and map guidance. Main is an ancestor.

## Non-Functional Requirements

Clean diff, no conflict markers, preserved historical evidence, explicit
validation commands/results and honest distinction from hosted acceptance.
The complete publication gate remains required before later publication;
this task does not publish and cannot claim that gate or hosted success.

## Acceptance Criteria

* Rebase completes; main ancestry and protected-file byte equality pass.
* Core/API Ruff check, format check and configured mypy pass.
* Relevant chat/core manifest tests and shared chat browser pass.
* Main's impacted case journey browser passes or any actual failure is recorded
  and corrected within the bounded integration scope before Review.
* One critique and one independent Review retained; local commit, no push.

## Test Ownership and Change Budget

Existing API/core tests and checks own coverage. Removals: none. Maximum new
test files: zero; change existing assertions only for evidenced integration
behavior, never to hide a failure. No generated targets. Ruff/mypy are static;
unit/browser checks provide semantic regressions. Use synthetic loopback data.

## Phase Checklist

<!-- P01 -->
### P01: Integrate

* [x] P01-T01 Rebase and resolve conflicts; verify protected inputs and ancestry.

<!-- P02 -->
### P02: Validate

* [x] P02-T01 Run static checks, relevant units, manifest and browser regressions.

Core checks and all specified browsers pass. Full API discovery admitted with
heavy lock held: 1,332 tests, 318 skips; separately enabled chat panel: 38 pass.
Existing case-journey Node test adapted to actual shared popup after its stale
inline selector failed. All original semantic assertions retained; no new tests
or production changes. This is a compatible integration amendment, not scope
expansion. P03 remains independent Review and local persistence.

<!-- P03 -->
### P03: Review and persist

* [x] P03-T01 Reconcile evidence, run one independent Review and commit locally.

Single independent Review Complete / Conformant, zero findings. The local
commit containing this completed checklist is the persistence receipt. No
post-Review source changes. Main re-fetched before commit remains ecbb5a80.

## Critique Disposition

Exactly one independent critique executed by rebase-plan-critique: Complete /
Pass, no findings. Evidence:
.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-rebase-plan-critique.md.
Plan Ready for full implementation; no significant unresolved decisions.

## Follow-Up Items

Coordinator publication gate, hosted CI and human acceptance are not performed.
Issue 550 remains reference-only; this refresh does not establish full acceptance.

## Handoff

Research: .copilot-tracking/research/2026-10-29/chat-widget-550-rebase-research.md.
Details: .copilot-tracking/details/2026-10-29/chat-widget-550-rebase-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-29/chat-widget-550-rebase-changes.md.
