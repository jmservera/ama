---
title: SQL roster chat revocation plan
description: Minimal authoritative actor correction for PR 503
ms.date: 2026-10-29
---

## Task Metadata

Task: `157-chat-sql-roster`; slug: `chat-sql-roster-157`.
Branch: `feat/agent-chat-157`; PR #503, Refs #157.

## Executive Summary

Make the shared chat actor resolver read SQL directly for roster-backed users.
The existing panel dispatch and completion checks then observe revoked access
instead of stale cached staff. Add SQLite regressions and update the core guide.

### What You May Not Know

The panel already rechecks actor and projected sources on completion. No panel
control-flow change is necessary. A SQL history fixture currently changes only
cache on its last role switch and needs to persist that switch. This work does
not prove live/SQL Server acceptance or authorize publication.

## Sources

Research: `.copilot-tracking/research/2026-10-29/chat-sql-roster-157-research.md`,
C1-C8. Details:
`.copilot-tracking/details/2026-10-29/chat-sql-roster-157-phase-details.md`.

## User Decisions and Requirements

* Full dated Research, Plan, Implement and Review for #157 / PR #503.
* Resolve authoritative SQL actor at dispatch and completion; fail closed when
  SQL access is revoked and test SQL row changes without touching cache.
* Minimal source changes, in `src/` only, plus requested RPI evidence.
* Pull with rebase first, reuse current branch, commit locally with Conventional
  Commit and supplied Copilot trailer; no push, no az, no manual rubric changes.
* Use `/tmp/mv`, core focused chat tests with sibling paths, Ruff check/format check.

## Goals

Prevent cached roster authorization from releasing answers after SQL revocation.

## Scope and Non-Goals

Shared roster resolver, focused chat tests and related core README only.
No Entra redesign, global SQL cache changes, schema changes, new dependencies,
provider calls, Azure use, issue closure or remote publication.

## Functional Requirements

* FR1: Query staff by authenticated normalized email under the SQL database lock
  on every roster-backed resolver call; no cached fallback for missing SQL rows.
* FR2: Deny missing, disabled, inactive or non-chat roles via `ChatForbidden`.
* FR3: Keep verified Entra and non-SQL identity behavior; retain panel projection,
  history, audit and role/source-change withholding behavior.

## Non-Functional Requirements

Use the existing parameterized SQL/dblock pattern. Do not retain a database lock
over inference. SQL read errors propagate, never become an allowed cached actor.
Keep changes limited and use existing lint/format policies.

## Acceptance Criteria

* AC1: SQL-only deletion/demotion before dispatch raises `ChatForbidden`, with no
  model call or assistant message despite unchanged staff caches.
* AC2: SQL-only deletion/demotion during inference raises `ChatForbidden`, with
  no assistant message/released answer; completion audit records access rejection.
* AC3: A still-chat-permitted SQL role change during inference withholds the
  answer, while unchanged SQL users still receive cited answers.
* AC4: Focused chat tests and Ruff checks pass; original evidence and independent
  critique/Review are recorded. No human/live/publication approval is inferred.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct resolver and regression contract

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add authoritative SQL actor lookup

Keep both existing `ChatPanel.ask` reauthorization sites. Change only the
roster-backed branch of `ChatIsolation.current_user`, using direct SQL when the
store has a database, and retaining the existing cache path only for non-SQL.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Cover stale-cache revocation and document behavior

Add a SQLite test class in `src/core/tests/test_chat_panel.py`: commit staff
updates/deletes through a separate SQLite connection, never mutate either
cached staff collection, and assert dispatch/completion rejection, audit and
absence of persisted answer. Cover unknown/contractor/disabled/inactive,
permitted-role change and unchanged actor. Persist the existing history test's
last role switch to SQL. Update `src/core/README.md`.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and independently review

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Demonstrate red/green and run focused checks

From `src/core`, use `/tmp/mv/bin/python`, with
`PYTHONPATH=src:tests:../agents/src:../agents/tests:../api/src:../api/tests`.
Run the new regression against old code first, then chat panel, chat threads,
privacy, memory, isolation, regulatory chat and API panel focused tests.
Run `/tmp/mv/bin/ruff check` and `ruff format --check --force-exclude` on changed
Python files; the latter honors the existing migrated-isolation exclusion.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Record one independent Review and commit locally

One fresh reviewer assesses only this fix, no repeated Review. Route new
findings to later work, retain original outcomes. Commit implementation and
dated evidence using GitHub-resolved privacy-safe author/committer email and
the requested trailer. Do not push. Full publication gate remains unrun and
publication blocked; scoped local checks are not a full-gate receipt.

## Test Ownership and Change Budget

Implementation parent owns tests. Canonical target:
`src/core/tests/test_chat_panel.py`; generated targets: none. Removals: none.
Maximum additions: one fixture class with up to five test methods and helpers.
Semantic checks: denied actor cannot dispatch/release/persist an answer;
regression checks: independent SQLite row mutation leaves cached staff intact.
Existing history regression amended, not removed.

## Critique Disposition

One independent final-candidate critique executed: Pass, no actionable findings.
Original:
`.copilot-tracking/reviews/plans/2026-10-29/chat-sql-roster-157-plan-critique.md`.
No corrections, repeat critique, caller decision or implementation blocker.

## Follow-Up Items

* Full local publication gate and independent exact-head/hosted acceptance remain
  later work if publication is requested; this task explicitly forbids push.

## Handoff

Critique passed; source implementation and validation complete, ready for one
independent Review, now executed Complete / Conformant with no findings.
P02-T02 remains pending only for the local commit; there is no remaining source
task. Original red/command failures and corrected
passing results are preserved in changes evidence. No implementation blockers.
Changes record:
`.copilot-tracking/changes/2026-10-29/chat-sql-roster-157-changes.md`.
