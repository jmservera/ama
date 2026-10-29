---
title: Chat receipt audit locking plan
description: Bounded correction for issue 157 and PR 503
ms.date: 2026-10-29
---

Task ID: `157-pr503-audit-locking-2026-10-29`.
Status: complete in the enclosing local commit; Review Complete / Conformant.

## Executive Summary

Serialize the panel's receipt and message-event writes with the shared reentrant
store lock, never inference. Prove rejected and completed concurrent turns retain
the real shared hash chain; preserve SQL behavior and nested callers.

## Sources

* `.copilot-tracking/research/2026-10-29/chat-audit-locking-157-research.md`, C1-C9.
* User request 2026-10-29; issue 157; open PR 503.

## User Decisions and Requirements

* First pull with rebase to absorb the bot commit; completed at feccc77d.
* Fix the rejected-turn audit race and sibling patterns in chat_panel.py.
* Lock append operations, not inference, and avoid nested-lock deadlocks.
* Add concurrent rejected-turn chain regression; run focused chat tests from
  src/core with /tmp/mv and explicit source/test sibling paths, Ruff lint/format.
* Record the full dated RPI loop and commit locally with Conventional Commit
  subject and required Copilot coauthor; do not push, use az or edit rubric JSON.

## Goals

Preserve shared audit predecessor integrity across this panel's concurrent paths.

## Scope and Non-Goals

Source: chat_panel.py. Tests: existing core test_chat_panel.py. Documentation:
src/core/README.md. Dated RPI artifacts only otherwise. No global store change,
schema migration, UI work, real model invocation or activation/epic acceptance.

## Functional Requirements

* Final chat.turn receipt always uses store.lock, including rejected requests.
* finish writes its assistant message and chat.answer while holding store.lock.
* Question persistence also holds store.lock through its indirect message audit.
* Existing reply shapes, exceptions, receipt metadata and privacy remain intact.

## Non-Functional Requirements

Use the existing reentrant JSON/SQL locks; no additional lock hierarchy. Model
execution stays outside the newly acquired sections. Tests use synthetic data.

## Acceptance Criteria

* AC1: Concurrent rejected turns produce all expected receipts with an intact
  full ledger, including a subsequent ordinary locked append.
* AC2: Completed/refused turns and message events serialize with shared writes.
* AC3: A competing locked write completes during inference.
* AC4: JSON and SQLite nested-lock callers complete and retain valid ledgers.
* AC5: Focused chat tests, Ruff check and Ruff format --check pass.
* AC6: Independent critique and one post-implementation Review are preserved;
  final local commit includes evidence and required trailer, without push.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Regression, implementation and validation

* [x] P01-T01: Add concurrency, nested-call and inference-lock regressions.
* [x] P01-T02: Reproduce rejected-chain failure before applying the source fix.
* [x] P01-T03: Lock the three small persistence sections and document behavior.
* [x] P01-T04: Run focused core/API/agent chat tests and Ruff checks.

<!-- rpi:phase id=P02 -->
### [x] P02: Independent Review and local closeout

* [x] P02-T01: Execute one independent post-implementation Review.
* [x] P02-T02: Reconcile all phase evidence and commit locally.

## Test Ownership and Coverage Lock

Canonical test owner: src/core/tests/test_chat_panel.py. Removals: none.
Maximum additions: five test methods and one small concurrency helper; no
generated fixtures. Keep existing API/agents tests unchanged. Chain verification
must use real ledger entries, not only mocked audit counts. Bounded barriers
may widen the original race while allowing serialized entry builders to proceed.
Use /tmp/mv; no new dependencies. Record commands and counts in changes evidence.

## Dependencies and Risks

RLock and _SyncLock are reentrant (C3/C4); MemoryRepo also acquires store.lock
(C5). SqlRepo owns dblock with no new opposite-order acquisition (C8).
SQL _SyncLock stages audit on outer exit, so verify real SQLite persistence,
not only mocks. Cross-process JSON writers and other modules' unlocked writes
remain outside this correction. No complete publication receipt is claimed:
this task is local-only, and the repository's full publication gate remains
required before any later push.

## Critique Disposition

Exactly one final-candidate independent critique executed:
`.copilot-tracking/plans/2026-10-29/chat-audit-locking-157-critique.md`.
Verdict Pass, no PC findings, no significant/divergent user decision required.
Accepted as implementation-ready without another critique.

## Follow-Up Items

None selected. Wider issue 157 acceptance and publication approvals are not
delivered by this narrowly scoped correction.

## Handoff

Details: `.copilot-tracking/details/2026-10-29/chat-audit-locking-157-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-29/chat-audit-locking-157-changes.md`.
Review: `.copilot-tracking/reviews/logs/2026-10-29/chat-audit-locking-157-review.md`.
Original Review: execution Complete, outcome Conformant, zero findings. Reviewed
source/test/README diff unchanged afterward; parent closeout only reconciles
artifact metadata and prepares the authorized local commit. Publication remains
blocked until its separate complete gate and approvals; no push is authorized.
