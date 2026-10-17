<!-- markdownlint-disable-file -->
# RPI Plan: consultation-record-controls-92

## Task Metadata

Task ID: 92. Date: 2026-10-17. Status: Implemented, ready for independent Review.
Details: .copilot-tracking/details/2026-10-17/consultation-record-controls-92-phase-details.md
Critique: .copilot-tracking/reviews/plans/2026-10-17/consultation-record-controls-92-plan-critique.md

## Executive Summary

Add a consultation record to the existing provider contract package, defaulting to
unknown. Record supplied human decisions, evidence and version history without
certifying Legal authority. Guard existing binding order confirmations.

### What You May Not Know

There is no dedicated let/renew command and no verified Legal consultation
capability. Therefore no supplied positive status can release the guard in this
delivery. This is partial issue acceptance, not a substitute let/renew API.
Existing success-flow tests will explicitly isolate the new guard when exercising
other domain controls; separate unmocked tests prove that no status bypasses it.

## User Decisions and Requirements

* Execute ordered Research, Plan/critique, Implement and independent Review.
* Preserve #90 source/capacity/delegation and existing safety/resident/financial controls.
* No invented Legal role, mapping, grants, approved consultation or operational activation.
* Unknown blocks binding work; applies alone cannot imply completion.
* Document absent let/renew acceptance. Publish a normal PR with Refs #92.

## Goals

Capture reviewable consultation evidence and stop unverified binding confirmation.

## Scope and Non-Goals

Existing procurement.py, authenticated server package route, procurement-domain
tests and directly related documentation. No UI, SQL schema/Store changes,
new capability, real order, legal interpretation or immutable snapshot changes.
Shared overlap: server.py one route. Legacy procurement/building/hazard/resident
test setups and one API role-matrix test explicitly isolate only the consultation
guard. No corresponding other-domain source or dataset helper was edited.
No generated fixtures, Store/SQL or UI edits.

## Functional Requirements

* New and legacy packages expose effective `consultation_status="unknown"`.
* A manager can record a supplied named human Legal decision with exact enum,
  reason, source case/document/version/hash and expected record version. The
  server records the current registered recorder, UTC time and monotonic version.
* Supplied status is separate from effective status. Mark Legal authority
  unverified; no manager/rule-owner becomes Legal and no source becomes law.
* Deny issue, reissue, correction/reopening, positive booking and final ordering.
  Drafts, capacity, negative appointment, withdrawal and factual completion retain
  existing checks and do not need consultation clearance.
* Existing SQL procurement validation checks the source rowversion and original
  procurement snapshot; rollback leaves no decision or success audit on conflict.

## Non-Functional Requirements

JSON, SQLite and task-owned loopback SQL Server persistence/reload parity.
Strict bounded text and exact payload fields; source bytes clean, non-generated,
version/hash checked. No private data or credential output. Preserve audit chain.
Configured component Ruff/format/mypy plus relevant core/API regressions.

## Acceptance Criteria

* Four statuses are recordable as supplied decisions, always visibly unverified.
* Unknown/missing/invalid/stale decisions cannot issue or confirm work.
* Untrusted claims cannot mint authority; version conflict leaves state/audit intact.
* All existing binding seams deny without editing unrelated domains.
* Exact issue criterion 1 remains partial (no verified Legal recorder); criterion 2
  remains partial (actual order holds proven, dedicated letting/renewal absent).

## Sources

.copilot-tracking/research/2026-10-17/consultation-record-controls-92-research.md,
C1-C10; BRD RULE-023/CON-004; PRD FR-007/CON-002; ADR 0005 owner scope.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Record and gate consultation
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add record-only procurement mechanics and authenticated route
<!-- rpi:phase id=P02 -->
### [x] P02: Validate and document
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add exact semantic, mutation and transaction tests
<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Run component checks, local SQL parity and document partial criteria

## Test Ownership Lock

No removals. Add at most 18 focused semantic test methods in a new consultation
test module plus at most 4 API methods. Existing procurement test setups may
explicitly patch only the consultation guard to retain independent #90 regression
coverage; tests that claim #92 behavior must never patch that guard.
Canonical targets: src/core/tests/test_consultation_controls.py and
src/api/tests/test_procurement_api.py; no generated targets or fixture hash changes.
Other existing tests that issue orders may need scoped setup patches, not synthetic
approval backfills. Run new tests unmocked, existing procurement/stock/hazard/
finance/grant/API regressions, format/lint/type checks and real local SQL parity.
PC-001 resolution: new #92 tests seed explicit historical Issued/Appointed/Completed
order snapshots with valid independent #90 prerequisites, never patching the guard
even during setup. Assert consultation-specific messages and unchanged state/audit.
Use a separate API class for unpatched #92 tests. Only legacy regression classes
isolate the new guard. Remove each individual call in memory during focused mutation
validation to prove all five consequential seams are actually reached.
PC-002 resolution: the new core test module exposes JSON, SQLite and opt-in MSSQL
variants of the same behavior mixin. MSSQL variant uses the existing test_mssqlstore
wipe/factory via a local import and the same temporary seed. Selector:
`python -m unittest test_consultation_controls.MssqlConsultation -q` with
ZF_TEST_MSSQL=1 and task-owned loopback ZF_SQL_* settings. Shared MSSQL file stays
unchanged. Authored test counts exclude inherited backend executions.

## Dependencies

#90 merged in #384; #290 historical skeleton only; #89 hierarchy only.
Actual Legal consultation authority and real let/renew workflow remain external gaps.

## Critique Disposition

Original independent verdict: Revise. One critique, no repeat.

| Finding | Owner | Disposition | Resolving evidence |
| --- | --- | --- | --- |
| PC-001 | Parent | Applied directly | Test Ownership Lock and P02-T01 historical snapshots, separate API class and individual guard mutation |
| PC-002 | Parent | Applied directly | Test Ownership Lock and P02-T02 opt-in MssqlConsultation using existing wipe/factory |

## Follow-Up Items

* Named owner must approve the future exact Legal consultation authority contract.
* Procurement integration must expose a genuine letting/renewal seam before exact acceptance.
* Coordinator-bounded engineering proposal: separately plan the existing
  package-linked genuine let/renew transition or authoritative integration,
  bind it to exact contract/scope/source and current authorized human consultation
  evidence, and test unknown/stale/unauthorized denials with fictional stores.
  Missing human approval does not prohibit isolated fail-closed mechanics;
  actual authorized Legal decision and missing workflow software are distinct
  prerequisites. No financial purchase API, operational activation or portal.

## Handoff

Changes: .copilot-tracking/changes/2026-10-17/consultation-record-controls-92-changes.md.
Full P01/P02 implemented and reconciled. 321 targeted executions, 47 explicit skips,
70 actual SQL Server passes, 25 migration passes, configured core/API static checks
and five individually killed guard mutations. Independent Review is next.
No full issue closure claim.

Coordinator continuation: authorized own-topic rebase onto main 1a05dfb8,
docs-only manual log conflict, exact own src added/removed byte parity and
upstream hazard/shared persistence unchanged. Fresh combined 348 executions:
300 passes/48 explicit skips; configured core/API lint/format/types pass.
Original Review retained, not repeated; coordinator final-head review pending.
Original 70 MSSQL passes remain historical, not new integration validation.
