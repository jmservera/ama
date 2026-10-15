---
title: Issue 84 implementation plan
description: Src stock comparisons, human technical decisions and unknown support
ms.date: 2026-10-15
---

Task ID: 84. Slug: stock-reconciliation-84. Status: Ready.

## Executive Summary

Add owned, unresolved stock comparisons with both source assertions in the
staff case view/API. Reuse separate human sign-offs, strengthen provenance and
validation, preserve affected-only reapproval, and make missing support data
explicitly Unknown without changing known-input ranking policy. No live
source authority, operational approval or AI benefit is asserted.

## User Decisions and Requirements

* Full automatic RPI loop, evidence committed in the PR, branch
  feat/src-stock-reconciliation-84, work only in the supplied worktree.
* ADR 0006 Accepted; all code/tests in src, existing code reused.
* Issue #84 four criteria; nomination #130 and tenure #131 excluded.
* Named professional sign-offs are human decisions, never agent inference.
* Preserve consent, safety, proposal-only AI, portable SQL and Azure-only deployment.
* pip only; do not touch .env, .vscode or tracking/github-issues.
* Local suites, ruff, mypy and synthetic app first; record commands and gaps.
* Commit/push PR to main with Refs #84 unless all acceptance is evidenced.

## Goals

Expose unresolved stock evidence and accountable ownership; protect technical
decisions and represent unknown support without silently excluding homes.

## Scope and Non-Goals

Core comparison/tri-state helpers and workflow wiring, API endpoint and
readable staff panel, sign-off hardening, focused tests and related docs.
No source-resolution policy, vulnerability inference, nomination workflow,
new SQL dialect, cloud deployment or operational competence certification.

## Functional Requirements

* Compare non-resident stock fields only, with two source IDs, dates, versions,
  validation states and differing values; bind query owner to existing staff.
* Retain previous comparisons and keep authority/resolution/eligibility Unknown.
  An unresolved comparison blocks technical approval/progression, not hazard intake.
* Separate assessment/design/building/coordination decisions remain versioned,
  authenticated, different-person and human-only. Validate before mutation.
* Reuse hazard and building gates; no transfer of home consent or sibling approval.
* Missing support flags remain Unknown in detail/ranking. Existing safety,
  waiting, stage and stable ID factors continue unchanged.

## Non-Functional Requirements

No private data or new dependencies in application code. Default-deny
contractor projection; strict validation and actionable error responses.
New helper/test files pass existing ruff/mypy rules without broad exemptions.
JSON and SQL persistence use existing Store contracts, no new SQL.

## Acceptance Criteria

* [x] AC1: API/view shows both compared values and named query owner.
* [x] AC2: all four human decisions remain separate/versioned (synthetic roles).
* [x] AC3: only explicitly affected sign-offs return on a design change.
* [x] AC4: absent support is Unknown; ranking retains independent factors.
* [ ] Live Azure SQL/model evidence and named professional competence acceptance
  (not producible locally; do not check this item).

## Phase Checklist

<!-- P01 -->
### P01: Core controls

* [x] P01-T01: Add validated immutable stock-comparison records and owned holds.
* [x] P01-T02: Harden sign-off provenance/atomicity and reuse safety/building checks.
* [x] P01-T03: Share tri-state support handling across relevant views and ranking.

<!-- P02 -->
### P02: API and staff experience

* [x] P02-T01: Wire reconciliation POST and readable staff evidence panel.
* [x] P02-T02: Add core semantic/persistence tests and synthetic HTTP app tests.

<!-- P03 -->
### P03: Evidence and delivery

* [x] P03-T01: Run src suites, ruff/mypy, JS checks and synthetic local HTTP run.
* [x] P03-T02: Update core/API guides, reference routing and append-only log.
* [x] P03-T03: One post-implementation Review, commit, push and open PR #318.

## Locked Test Ownership and Validation

Core owns pure comparison/support and JSON/SQL workflow semantics. API owns
HTTP/auth/projection and running synthetic app tests. Exact removals: none.
Maximum additions: two Python test modules, up to 24 test methods total.
Existing finance sign-off, ranking, building, hazard and handoff suites remain
regression coverage. Canonical code: src/core and src/api. Generated targets:
none. Existing tooling only; install missing dev tools with pip in a local
ignored virtual environment. Full src suites and checks follow targeted tests.
Docker attempted explicitly; SQL Server/Azure/real model gaps stated honestly.

## Sources and Handoff

Research: .copilot-tracking/research/2026-10-15/stock-reconciliation-84-research.md.
Details: .copilot-tracking/details/2026-10-15/stock-reconciliation-84-phase-details.md.
Changes target: .copilot-tracking/changes/2026-10-15/stock-reconciliation-84-changes.md.

## Critique Disposition

Exactly one independent final-candidate critique completed; verdict Revise.
PC-001 accepted directly: details now define the tri-state truth table,
coverage and compatibility Boolean consumers including AI facts.
PC-002 accepted directly: versioned portable derived-data refresh and
legacy-current-policy/reopen idempotence regression added.
PC-003 accepted directly: conflict hold precedes no-design early return;
no-design and signed-case/hazard-independent scenarios added.
PC-004 accepted directly: actual rendered browser exercise required if
available, otherwise explicitly unmet. No user decision or repeat critique.
The plan is Ready for this bounded slice, not full operational acceptance.

## Follow-Up Items

## Owner-directed PR #318 correction scope

The 2026-10-15 owner request authorizes this bounded implementation follow-up,
not a repeated critique or Review. Merge origin/main first, retaining both
documentation entries. Source/test edits stay in src/core and src/api.

* [x] Add append-only Withdrawn/Reconciled events, authenticated human
  provenance, raiser/manager withdrawal and case-owner/manager query opening.
* [x] Require manager human attestation plus evidence for reconciliation;
  do not choose a winning source or change home/eligibility/technical decisions.
  Operational rules remain Unknown/owner-approval-needed.
* [x] Prove regression tests fail before implementation, then pass JSON/SQL
  and HTTP tests and required absolute-PYTHONPATH suites and quality checks.
* [ ] Update changes/review evidence, source guides, index/log and non-closing
  PR body; commit with requested identity/trailer and push named topic.

Source authority/resolution policy, operational competence/delegation, live
Azure SQL/model and direct human acceptance remain outside this local slice.
