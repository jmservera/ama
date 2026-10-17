---
title: Issue 97 implementation plan
description: Bounded immutable form schema registry and source-linked candidate staging
ms.date: 2026-10-17
---

## Task Metadata

* Task ID: 97
* Task slug: form-schema-staging-97
* Planning status: Ready after one critique and direct dispositions
* Phase details: .copilot-tracking/details/2026-10-17/form-schema-staging-97-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/form-schema-staging-97-plan-critique.md

## Executive Summary

Add a small core registry and candidate-staging API using the existing case documents, JSON store, SQL checked shared documents, row versions and audit ledger. Store exact schema versions, field policy and provenance without approving a template or accepting a field. Verify text spans and CSV cells against uploaded bytes; imported OCR candidates retain supplied provenance and explicit unverified route state. Unsupported inputs return owned manual recovery.

### What You May Not Know

The AI registry prerequisite exists (#105); live form selection would still need its own registered/approved task, but this implementation never calls AI. The owner accepted PRD v0.12.0 for exercise implementation planning on 2026-10-10; current in-review frontmatter is a separate status fact, not a new prerequisite. No actual approved form schema or authority evidence exists in the inspected baseline. All registered schemas remain Unapproved; this intentionally cannot open a reviewed/approved form or submit a pack.

## User Decisions and Requirements

* Run one full ordered Research -> Plan -> Implement -> Review loop with dated committed phase artifacts and persistent phase log; stop after pushed main-target PR, without merge/rebase/force-push or a child loop.
* Implement only #97 / FR-038 and FR-039. Parent #96 is hierarchy; preserve actual missing prerequisites, not invented ordering.
* Preserve types, units/options, required/conditional rules, source authority and evidence, exact raw values, source hash/version/locator and parser/model lineage.
* Do not forge authority, fixture approval, live extraction, field acceptance, funding eligibility or submission. #98 owns review/validation/pack/staleness.
* Use migrated src packages, external tests, existing stores/helpers and own pip venv. No private datasets, live paid AI/Azure/SQL, Docker escalation, new services or UI.
* Run fail-before tests, fixture HTTP exercise, relevant suites and existing lint/format/type checks; push a Refs #97 PR with exact unmet criteria.

## Goals

* Make schema definitions immutable and candidates auditable without increasing source or model authority.
* Preserve conflicts and enable later #98 integration without implementing it.

## Scope and Non-Goals

In scope: schema registration/read, candidate import/read, text/CSV locator verification, supplied OCR lineage, safe manual recovery, store parity, docs and artifacts.

Non-goals: actual parser/OCR/model invocation, semantic choice, schema approval workflow, approved draft preparation/binding, human review, validation reports, calculations, exports, stale propagation, UI or infrastructure.

## Functional Requirements

* Versioned schemas identify type/template, reviewer function/person, field/section IDs, types, units/options, conditions, source-kind precedence/evidence requirements and versioned calculation/rule references.
* Server assigns Unapproved and creator/time/hash; caller cannot set approval, source authority or audit identity.
* Append candidate batches to the current case only. Copy actual document ID/hash/version and parser/model metadata; verify actual bytes against stored hash, scan and role checks.
* Verify supplied text offsets / CSV cells against actual bytes; retain all alternatives, no value normalization or winner.
* OCR imports retain supplied route/version/error evidence and label it unverified; never run/approve OCR. Unsupported/unreadable input records an owned manual-recovery event with no candidates.
* Human-only field categories reject prefill. All registry/staging reads and writes conservatively require the intersection of existing reason, resident-record and Finance-view rights, checked against the current registered actor on every request. Schema policy can narrow, never widen rights. Unknown/malformed inputs are explicit errors with no partial writes.

## Non-Functional Requirements

* No provider/network calls in new domain code. Existing local JSON/SQLite/MssqlStore paths remain shared; no new tables, service or dependency.
* Shared registry uses existing checked meta documents; candidate history uses row-versioned case bodies. Audit contains IDs/counts/hashes, never raw values.
* Input bounds: at most 200 fields / batch candidates; text within existing 5 MB upload limit, field raw value at most 16,000 characters; strict keys and finite scalar values.

## Acceptance Criteria

* Focused tests fail before behavior exists, then pass for schema structure/version immutability, lineage integrity, conflict retention, role/cross-case denial, invalid-input atomicity, unsupported/manual recovery, source byte/hash mismatch and no automatic controlled-state mutation.
* JSON and SQLite reopen retain exact schema/candidate history. Cross-process SQL writer conflicts do not leak uncommitted registry or candidates.
* Real loopback authenticated HTTP exercise proves health, registration, staging, read-back and denial; no outbound AI.
* Component suites and existing lint/format/mypy run in own pip venv; actual results and skips recorded.
* Actual approved-template/authority and full AC-046/047/053 remain explicitly unmet where not implemented; never use closing keywords.

## Sources

* .copilot-tracking/research/2026-10-17/form-schema-staging-97-research.md: W1-W4, C1-C7.
* Existing `ai_registry.digest` is the canonical structured digest helper; ledger provides audit, not a nonexistent canonical/hash API.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Prove the contract fails before implementation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add focused external synthetic tests

Own `src/core/tests/test_form_staging.py` and `src/api/tests/test_form_staging_api.py`. Record actual baseline failures. No existing tests removed or weakened.

<!-- rpi:phase id=P02 -->
### [x] P02: Implement the bounded contract

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Registry, provenance and persistence

Add `src/core/src/zava_forward/core/forms.py`; add `form_schemas` to SqlStore checked documents and seed list if required. Use protocol-typed Store boundary and existing digest/scan/document/audit helpers.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Authenticated API and documentation

Wire registry and per-case staging endpoints in existing server/projection policy. Update component guides plus additive index/log entries only.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and reconcile

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Exercise and validate

Run focused core/API behavior tests, relevant full core/API suites and existing lint/format/mypy. Reconcile changes, plan and details before Review. Existing SQL Server harness may skip without server; no live claim.

## Test Ownership and Change Budget

* Canonical tests: two new external test files above; maximum two additions, removals none. Extend existing `test_role_endpoint_inventory.py` route lists/dynamic-action assertion for the new endpoints; no existing coverage removed.
* Production additions: one core module; no generated runtime artifacts or dependency-manifest additions.
* Semantic coverage: independent expected schema/candidate keys and literal source spans; regression coverage: unchanged funding/stage/source snapshots, existing component suites.
* Evidence: actual fail-before and subsequent command outcomes in changes record; HTTP harness starts/stops ephemeral loopback service over temporary synthetic data.

## Dependencies

* Existing AI registry is delivered (#105); unregistered form AI selection remains disabled/out of scope.
* Actual approved template/source authority is unavailable: unmet positive preparation acceptance, not a blocker to unapproved candidate collection.
* No ordering dependency on #96, #98, #360, #358 or #182.

## Critique Disposition

One independent critique executed; verdict Revise. All compatible planner-owned findings applied directly; no significant/divergent decision or second critique.

| Finding | Disposition | Resolving contract |
| --- | --- | --- |
| PC-001 | Applied | Conservative intersection of existing reason/resident/Finance rights for arbitrary raw content; current identity and rights rechecked on reads/writes; no generic-detail/audit leakage |
| PC-002 | Applied | Exact schema keys, funding Unknown/not-applicable distinction, immutable versions and server-enforced human-only categories in details |
| PC-003 | Applied | UTF-8 code-point half-open spans, 1-based CSV cells including header, supplied processing assertion separated from observed verifier |
| PC-004 | Applied | Inject non-conflict body/audit/save failures for both registry and candidates; no local/durable leakage or replay |
| PC-005 | Applied | Dated v0.12.0 PRD planning acceptance separate from current frontmatter, form approval and operational release |

## Follow-Up Items

* Actual form/template approval and recorded delegation are required before approved preparation can be claimed; owner-supplied evidence, not fixtures.
* #98 owns field decisions, deterministic validation, packs and exact stale propagation.
* Any future AI selector needs a registered task and release authority; do not extend the registry here.

## Handoff

Changes record: .copilot-tracking/changes/2026-10-17/form-schema-staging-97-changes.md. P01-P03 complete with actual fail-before evidence, 15 focused core/two HTTP tests, complete core/API suites and static checks. Ready for one Review; all critique findings dispositioned. Actual approved-template/full PRD acceptance remains unmet, not an implementation blocker to this bounded slice.
