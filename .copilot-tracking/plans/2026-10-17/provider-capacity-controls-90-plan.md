<!-- markdownlint-disable-file -->
# RPI Plan: Provider capacity and controlled orders

## Task Metadata

* Task ID: 90
* Task slug: provider-capacity-controls-90
* Date: 2026-10-17
* Status: P01/P02 complete; one independent Review Complete/Conformant; P03 publication pending
* Phase details: .copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/provider-capacity-controls-90-plan-critique.md

## Executive Summary

Close proven gaps in the existing procurement workflow, not replace delivered screens or storage. Bind confirmed capacity to current source versions, dates, home-order units, covered homes, package scope and named contract delegation. Version every order mutation and stop the alternate case-booking bypass. Keep provider reads own-only and all system output non-instructional.

### What You May Not Know

The current 21 tests pass despite missing these exact controls. Existing SQL checked-document CAS already prevents concurrent over-allocation; it must be reused. Actual contract delegations do not exist in supplied evidence: trusted staff configuration may supply them, never a self-granting API or AI. Legacy records remain readable but cannot authorize new confirmed work.

## User Decisions and Requirements

* Execute full dated, committed Research -> Plan -> Implement -> Review, manager review during research, one critique and one implementation Review.
* Satisfy all four exact #90 criteria and PRD FR-016/BRD RULE-007/008; #89 is hierarchy, no explicit issue dependencies.
* Preserve named human instruction authority, resident/safety controls, contractor read-only own orders, #78 provenance and #97 forms.
* No private/real data, live orders, finances, cloud or paid AI; own venv; local SQL Server via existing standard container harness if available.
* Publish topic branch to main PR using Refs #90, no closing, merge, rebase or force push; stop after final push.

## Goals

* Make committed capacity and order chronology enforceable and testable on both existing stores and HTTP surfaces.
* Surface unknown evidence and missing real permission honestly without blocking fictional engineering delivery.

## Scope and Non-Goals

* In scope: procurement mixin, case advance, narrow SQL transaction validation, existing API and capacity screen inputs, coupled test fixtures, component guides and existing KB synthesis/index/log.
* Non-goals: new service/framework/schema, MVP edits, live company approval, award/payment, new AI route, broader UI redesign or full PRD FR-016 acceptance.

## Functional Requirements

* Registered named current manager plus explicit trusted contract delegation reference/version/effective dates for consequential package/capacity/order changes; no delegation granted by package creation.
* Capacity source ref/version/date/review date, committed status, valid interval, exact case set, fixed home-order unit and package scope-version binding. Known zero/reduction can be recorded; deficit blocks new work.
* Issue/reissue/booking/correction and case advance recheck quota/evidence; booking date must be inside both intervals. Offered/legacy/unknown evidence cannot authorize.
* Every successful order change appends sequential issuer/time/state/appointment/scope/authority/capacity snapshots. Returned records are copies.
* Drafts state not an instruction; reviewing drafts never issues. Contractors cannot mutate and cannot see another supplier's orders/packages through direct or HTTP surfaces.

## Non-Functional Requirements

* Reuse existing single-process JSON lock, SQL checked-document CAS, case-rowversion and writer/application locks.
* Revalidate named staff and read-only procurement dependency inside SQL commit; failed writes restore cache and do not append success audit.
* Keep existing Fluent 2 native styling and keyboard/label/error semantics; narrow UI fields only.

## Acceptance Criteria

1. Exactly one committed home allocation permits one active/completed order, never two despite larger offer, bad evidence, interval mismatch, rescope or concurrent writers; alternate advance cannot bypass.
2. Issue plus each appointment, reissue, completion, correction and withdrawal has immutable sequential versions and stable issuer identity.
3. Template/AI proposals and review never become instructions or alter procurement.
4. Two fixture contractors read only own orders; every write route rejects them.

## Sources

* .copilot-tracking/research/2026-10-17/provider-capacity-controls-90-research.md: C1-C7, completed three waves and Ready.
* .copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md: research instrument, no approval.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reproduce and enforce controls

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add failing-first JSON/SQLite and controller regressions

Exact root gaps, quota thresholds, identity/authority, source fields/dates/units, all-change snapshots, failed-write restoration and advance bypass.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement bounded domain and transaction controls

Depends on P01-T01. Add trusted staff contract-authority checks and structured committed evidence; preserve unknown/legacy reads, resident controls and current checked documents.

<!-- rpi:phase id=P02 -->
### [x] P02: Wire and validate existing surfaces

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Complete API/screen evidence inputs and coupled fixtures

Depends on P01-T02. No redesign or permission grant. Fresh guidelines and local browser required for changed screen.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Run focused parity, quality gates and document evidence

Depends on P02-T01. Existing local SQL Server 2022 harness only. Record exact Pass/Fail/Not run; preserve #78 and #97 regression suites.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and publish

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: One independent Review and main-targeting Refs #90 PR

Depends on P02-T02. Review findings route later, no review loop. Commit dated artifacts with phase execution, privacy-safe identity/trailer, push without merge/closing.

## Test Ownership and Validation Lock

Parent owns new regressions in existing `test_quality_procurement.py` and new `test_procurement_api.py`; reuse existing opt-in SQL Server test factory with procurement behavior inheritance. Existing safety/resident/building fixture owners retain assertions; update only supplied capacity/delegation prerequisites and changed version expectations. Removals: none. Maximum additions: 35 test methods, no dependencies beyond existing component extras. Canonical targets are migrated Python/JS sources; no generated assets. Semantic exact-criterion tests are separate from regressions of preserved controls. Validation: focused unittest, lint/format/type commands per component, JS syntax, local browser and standard local SQL Server parity if available.

## Dependencies

* P01-T01 -> P01-T02 -> P02-T01 -> P02-T02 -> P03-T01.
* No issue dependency or actual operational permission inferred.

## Critique Disposition

| Finding | Disposition |
| --- | --- |
| PC-001 | Applied: exact trusted action/contract-version/supplier/scope and unrevoked dated delegation predicate below |
| PC-002 | Applied: original uploaded source bytes/hash/version resolved, manager acceptance recorded; explicit source/review/delivery boundaries |
| PC-003 | Applied: advance requires one current Appointed order with latest Booked date; existing allocations use <= quota; withdrawal explicitly releases with version/reason |
| PC-004 | Applied: deterministic two-store pre-save races and injected save failure with cache/audit/reopen oracles |
| PC-005 | Applied: executable target/selector/budget manifest in details; no test removals or second critique |

No significant/divergent decision remains. These define bounded fictional engineering contracts, not company delegations.

## Follow-Up Items

* Actual contract evidence/delegations and operational approval: named human contract authority owner must provision and validate these before any live use. No live authority was supplied, and no test fixture grants it.
* Hosted AI/Azure and human/screen-reader/WCAG acceptance: deployment and UX owners must commission separate approved validation. These are not required for the four local engineering criteria and were not exercised.

## Implementation-Time Reconciliation

P01/P02 used existing transaction helpers, not new services. JSON save/audit
failure compensation was extended to the alternate advance path after tracing
the same boundary; SQL retains transactional rollback. Coupled core and API
building positives now supply an authorized fictional booked order instead of
asserting the removed advance bypass. No original assertion was deleted.
The final API-inclusive regression set is 278 tests (one existing opt-in
skip); actual local SQL Server parity is 29 tests. Exact semantic tests are
63 tests. Browser and quality evidence is in the changes record. No scope,
human approval or architecture divergence required a new decision/critique.

## Handoff

Changes record: .copilot-tracking/changes/2026-10-17/provider-capacity-controls-90-changes.md. P01/P02 complete; one independent Review Complete/Conformant with no substantive findings; parent publication remains. No additional implementation/review loop or routine approval prompt.
