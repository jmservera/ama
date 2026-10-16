---
title: Issue 211 implementation plan
ms.date: 2026-10-16
---

Task: 211 / issue-211-rule-cards. Status: implementation-ready.

## Executive Summary

Extend the migrated core rule-card and law stores, then expose the lifecycle
through the authenticated API. Keep all cards visibly exercise-only and retain
every version and approval event. Dedicated Entra rule capabilities, independent
from workbench roles, replace caller-supplied authority at the HTTP boundary.
No live approval, tenant assignment or legal correctness is claimed.

## Sources

Research: .copilot-tracking/research/2026-10-16/issue-211-rule-cards-research.md.
Details: .copilot-tracking/details/2026-10-16/issue-211-rule-cards-phase-details.md.
Issue #211 body and owner comments; ADR 0006; existing core/API tests.

## User Decisions and Requirements

* Full ordered RPI loop with dated committed artifacts, same PR, Refs #211.
* Reuse core rulecards.py and lawstore.py; all implementation in src/.
* Draft/approved/active/held/retired, retained versions/dates, independent
  author/owner and owner hold; two unapproved exercise fixture cards.
* Source changes never overwrite approved cards; server-side authorization.
* No private data or fabricated approvals; owner nomination is not approval.
* Local-first unit suites, mypy, ruff check/format and local HTTP app run.
* Push feat/src-rule-cards-211 and open an honest PR to main; no merge.

## Goals

Preserve the existing domain lifecycle while enforcing authenticated authority
and durable atomic version/source-change evidence.

## Scope and Non-Goals

Core, API, tests and directly related documentation. No new UI, deterministic
rule engine, legal assessment, tenant provisioning, live data or Azure deployment.

## Functional Requirements

* Immutable draft versions, append-only lifecycle/approval/review history.
* Approved-only activation, named-owner-only actions, no identity self-approval.
* Server-derived actor, role and event date; no shared-password approval authority.
* Read routes for history/reviews; explicit draft and lifecycle POST routes.
* Law ingestion automatically records source-change review items.

## Non-Functional Requirements

Reuse law SQL adapters, portable SQL and driver-agnostic integrity handling.
Whole-mutation transactions serialize versions and supersession. Validate field
types, canonical dates and intervals before writes. Existing behavior survives.

## Acceptance Criteria

1. Local positive and negative lifecycle tests cover all six issue criteria.
2. HTTP tests prove signed/provisioned staff capability binding, rejected
   spoofing, contractor/unknown/agent/password denial and no self-approval.
3. Source re-ingestion preserves card contents and approval history.
4. All requested local validation is recorded with honest platform limits.
5. Artifacts, docs index/log and code are committed and pushed in one PR.

## Phase Checklist

<!-- P01 -->
### P01: Core reuse and persistence

* [x] P01-T01: Adapt RuleCardStore to law SQL adapters and atomic portable writes.
* [x] P01-T02: Validate drafts/dates/holds and wire source review creation.

<!-- P02 -->
### P02: Authenticated API

* [x] P02-T01: Preserve existing staff auth and add separate trusted rule claims.
* [x] P02-T02: Expose history, draft and owner transition routes with server checks.

<!-- P03 -->
### P03: Evidence and delivery

* [x] P03-T01: Extend existing core/law/auth/inventory tests and add bounded HTTP tests.
* [x] P03-T02: Run local suites/tooling/app, update docs and record results.
* [ ] P03-T03: One post-implementation review, commit, push, open PR to main.

## Test Ownership and Validation Lock

Canonical targets: src/core/tests/test_rulecards.py and
src/api/tests/test_lawstore.py, test_auth.py, test_role_endpoint_inventory.py.
At most one additional API test file for the HTTP lifecycle. No removals or
generated test targets. Semantic coverage: trusted identity and deny cases,
atomic rollback, invalid values, source-change immutability. Regression coverage:
full core/API unit suites and per-project mypy/ruff/format. Local app uses only
synthetic fixture data in a temporary directory; no Azure/Docker needed.

## Critique Disposition

One independent critique executed: Revise, with the following final dispositions.

* PC-001 accepted: one shared reentrant adapter lock; outer source transaction
  owns commit/rollback and calls a non-committing review helper. Acquire database
  write lock before state/version reads. Source/review rows atomic; immutable
  blobs may remain orphaned after failure. Index is derived, rebuilt on retry.
* PC-002 accepted: capabilities require one unique provisioned oid binding;
  fallback-only workbench login receives none. Reserved rule claims never map
  to workbench roles. Test ambiguity and spoofed fields.
* PC-003 accepted: retain legacy history and test initialization/reopen, adapter
  SQL contract and opt-in SQL Server cleanup. No identity rewriting.
* PC-004 rejected: the purported /tmp prohibition is not an applicable user or
  parent constraint. The user explicitly requires /tmp/zf164; retain it.
* PC-005 partially accepted: distinguish defects from residual acceptance limits.
  Reject advice to return to implementation after Review: the governing one-pass
  protocol routes review findings to later work. A material open finding means
  a blocked/draft PR, not conformant completion.

## Follow-Up Items

Human card approval, real tenant capability assignments and platform verification
remain owner/deployment work. UI and rule engine are outside this bounded slice.

## Handoff

After critique disposition, proceed under explicit full-loop user direction.
Changes: .copilot-tracking/changes/2026-10-16/issue-211-rule-cards-changes.md.
