---
title: Issue 83 implementation plan
ms.date: 2026-10-15
---

Task: #83 / src-handoffs-83.

## Executive Summary

Extend the migrated workflow rather than rebuild it. Add return/reopen
provenance, receipt/escalation/completion and explicit ownership projections.
Preserve old labels as aliases; close the immediate-handover bypass. Deliver
API/UI and synthetic JSON/SQLite regression evidence. Approved operational
escalation timing and live Azure/SQL/model acceptance remain unclaimed.

## User Decisions and Requirements

* Full RPI loop, committed artifacts, `Refs #83`, PR to main, no merge.
* Only assigned worktree/branch; no new mvp code, private data or excluded files.
* ADR 0006 and merged moves are authoritative; pip only and portable SQL.
* AI stays available with human gates; workflow never manufactures consent.
* Record every validation command/result; leave unavailable criteria unticked.

## Goals

Named human accountability and reconstructable return/handoff transitions.

## Scope and Non-Goals

Core mixin/store, API routes/projection, existing web panels, component READMEs,
reference index/log and tests. No deployment, new model task, scheduled worker,
operational SLA approval or broad FR-043 invalidation redesign.

## Functional Requirements

* Versioned return/reopen record: reason, prior/current stages, source,
  initiating authority, receiving owner, next action.
* Distinct sent/received/accepted/rejected/escalated/completed states.
* Receipt/escalation never transfers ownership; sender chases until acceptance.
* Legacy immediate handover becomes an offer; no acceptance bypass.
* Pending queue visible to sender, recipient and managers; role-redacted text.
* Human-selected due date and manual escalation; no invented approved SLA.

## Non-Functional Requirements

Use current persistence/locking/audit, no schema/dependency changes. Core imports
no workload. Existing AI proposal paths remain intact. Preserve safety/consent.

## Acceptance Criteria

* [x] New API and core return/reopen confirmations require source and next action and
  preserve authenticated initiator, receiving owner and history.
* [x] All six handoff statuses distinguish current owner/receiver/chase owner.
* [x] Negative transitions, unauthorized actors and bypass are refused.
* [x] Synthetic persistence, role, UI and local app evidence recorded.
* [ ] Approved-time operational escalation (blocked: OD-09; not this slice).

## Phase Checklist

<!-- P01 -->
### P01 Core workflow
* [x] P01-T01 Add provenance and role-checked handoff transitions/history/queue.
* [x] P01-T02 Route hand_over through offer; preserve legacy read compatibility.

<!-- P02 -->
### P02 API, UI and evidence
* [x] P02-T01 Wire endpoints, projection and panels for states/provenance.
* [x] P02-T02 Add core semantics and API/role tests; update docs/index/log.

<!-- P03 -->
### P03 Validation and delivery
* [x] P03-T01 Run all project suites, ruff/format/mypy, local app synthetic run,
  migration checks and attempted Docker; record commands/results.
* [x] P03-T02 One post-implementation review; commit, push and open PR.

## Test Ownership and Change Budget

Core semantic tests in `src/core/tests/test_handoff_lifecycle.py`; API integration
in `src/api/tests/test_handoff_api.py`, reused by the existing guarded SQL Server
suite. Existing workflow tests retained; adjust immediate-handover
expectations where behavior intentionally changes. No test removals. At most two
new test modules, no generated checked-in data. Existing suites are regression
coverage, new tests assert exact metadata/state/ownership/persistence shapes.

## Critique Disposition

One independent critique executed, verdict Revise. All findings disposed directly:

* PC-001: simplify return/reopen to record the existing accountable owner only.
  No recipient selection or reassignment is allowed through dispositions.
  Distinct destinations use the ordinary offer/accept path.
* PC-002: explicit state/actor table added to details; exercise all edges and
  refusal immutability in semantic/API tests.
* PC-003: include independent urgency, next action and resident-update owner/date.
  Preserve resident-update commitments across rejection and replacement offers.
* PC-004: in-scope correctness failures block passing acceptance/ready publication.
  The one-review contract prohibits another implementation/review loop here:
  route such failures and publish draft/blocked, never claim passing acceptance.
  Owner timing and unavailable live evidence remain accepted exclusions.

Planning Readiness: Ready. No owner decision needed for these corrections.

## Follow-Up Items

OD-09 approved escalation periods and human operating authority; SQL Server,
image and live AI/Azure acceptance evidence. These do not block this bounded PR.
Published as #311, Refs #83. All implementation tasks complete; Review execution
Complete, outcome Residual work. No full issue acceptance or merge claimed.

## Handoff

Research: `.copilot-tracking/research/2026-10-15/src-handoffs-83-research.md`.
Details: `.copilot-tracking/details/2026-10-15/src-handoffs-83-phase-details.md`.
Changes target: `.copilot-tracking/changes/2026-10-15/src-handoffs-83-changes.md`.
