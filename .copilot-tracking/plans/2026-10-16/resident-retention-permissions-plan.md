---
title: Resident retention and permissions plan
description: Implementation candidate for issue 86 follow-up
ms.date: 2026-10-16
---

Task: issue-86-resident-retention-permissions.

## Executive Summary

Apply the confirmed five-year first-contact schedule and server-side matrix,
then prove synthetic local and Azure SQL persistence and remove Azure costs.
Reuse existing role and manager-reviewed retention boundaries. Unknown contact
history is explicit, never silently dated from a decision.

## User Decisions and Requirements

* Refs #86, never Closes. Five calendar years from first recorded resident contact,
  including withdrawal and expired authority; configurable constant.
* Liaison (Neighbourhood/Resident Engagement) and Coordinator record/view;
  manager/support view; contractor per-measure Proceed/Hold only for resident data.
* Agents receive only allow-listed task inputs, no decision record/evidence.
* Source implementation only src; requested docs/log and RPI artifacts excepted.
* Local unit/ruff/mypy/app before Azure SQL in ama, uksouth, then cost cleanup.
* No private data/properwarm, uv, protected configuration paths, SQLite-only new SQL,
  force-push or issue closure. Use requested privacy-safe email and coauthor trailer.
* Commit, push, PR; no merge.

## Goals

Correct time origin and field rights without widening agent or contractor access.

## Scope and Non-Goals

Core/API/web/tests, relevant READMEs, reference index/log, RPI artifacts.
Not operational human acceptance, legal certification, real-resident tests,
complaints platform integration or cross-case resident identity invention.

## Functional Requirements

* Persist earliest first-contact marker from actual contact evidence.
* Return first-contact retention schedule, block overdue decision reliance,
  list and approve deletion through existing manager retention APIs, respect legal hold.
* Enforce named registered-human recording on resident and legacy decision paths.
* View permission independent from configurable vulnerability-reason permission.
* Contractor flag derived using the same per-measure gate, never private reasons.

## Non-Functional Requirements

Portable persistence; no schema change required for JSON case payload fields.
No sensitive text in retention audit. No private existing SQL reads.

## Acceptance Criteria

Deterministic tests distinguish contact from decision, exact anniversary,
leap-day, configuration, withdrawn/expired authority and missing history.
Permission tests exercise allow and deny roles and forged identities, contractor
flags and AI input canaries. JSON/SQLite restart and synthetic Azure SQL restart.
Existing relevant suites, ruff/mypy and loopback HTTP pass before Azure.

## Phase Checklist

<!-- P01 -->
### P01: Implement and prove locally

Phase status: Completed.

* [x] P01-T01: Retention metadata, first contact, gates and retention deletion.
* [x] P01-T02: Separate field roles, actor binding, contractor flags and matching UI.
* [x] P01-T03: Regression tests, local suites, ruff, mypy, loopback app.

<!-- P02 -->
### P02: Azure, evidence and delivery

* [x] P02-T01: Isolated synthetic Azure SQL exercise, restart and ledger checks.
* [ ] P02-T02: Remove ama resource group, verify deletion, record limitations.
* [ ] P02-T03: Documentation/log, one Review, commit/push/PR.

## Test Ownership and Locked Scope

Existing core resident tests own semantics for JSON/SQLite; API resident tests
own HTTP permissions. Update old expectations that incorrectly hide coordinator
data or allow manager writes. Exact removals: none. Maximum new files:
one synthetic Azure verification script under src/core/tests, plus RPI artifacts.
Canonical code only src; no generated production assets. Capture failing new
tests against pre-change code or equivalent isolated reverse patch, then green.
Use component unit runners, ruff check and mypy; fix coupled failures only.

## Critique Disposition

Single critique executed, verdict Revise; finalized with these dispositions:

* PC-001 accepted: purge exact resident fields (scopes, measure decisions,
  authorities, safe route/history, reviews, legacy decision); scrub representative
  refs in service requests but preserve complaint outcomes and general contacts.
  Keep first-contact marker and metadata tombstone. Stop copying new legacy notes
  into immutable audit; inherited ledger text remains a declared limitation.
* PC-002 accepted: include historical safe-contact confirmations and persist
  their contact marker. Malformed/future contact evidence is unusable, not a
  fallback to a decision date; later contact never resets earliest evidence.
* PC-003 accepted: restore authorized resident subtrees after unrelated recursive
  note redaction, leaving vulnerability/contact notes protected.
* PC-004 accepted: shared expiry check applies to authority_for as well as gates,
  even when legal hold prevents purge.
* PC-005 accepted: Azure evidence states ledger mode and current-row deletion
  only, never claims removal from backups/history.
* PC-006 rejected as a required constraint: no supplied runtime instruction
  forbids tempfile directories. Project-local isolated scratch remains a harmless
  execution choice, not a reason to change fixtures.

Implementation readiness: Ready. No owner decision needed; no second critique.

## Follow-Up Items

Named role-holder/human acceptance and formal complaints integration remain #86
work, not this slice. Historical contact evidence and universal resident identity
need reconciliation before real operational use.
Current-payload deletion is not backup/history erasure; schedule and approve
operational erasure design separately. No automatic purge service is configured.

## Current Execution State

P01 complete. P02 SQL verification complete, authorized teardown running.
Documentation and log updated. Review and git delivery await cleanup evidence.
Service-action preservation is an ordinary coupled compatibility correction,
not a grant to managers to record resident decisions. No material divergence
from owner choices; no additional critique required.

## Handoff

Research: .copilot-tracking/research/2026-10-16/resident-retention-permissions-research.md.
Details: .copilot-tracking/details/2026-10-16/resident-retention-permissions-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-16/resident-retention-permissions-changes.md.
