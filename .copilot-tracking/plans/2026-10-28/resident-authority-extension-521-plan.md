---
title: Resident demo authority extension plan
description: Source-only issue 521 implementation candidate
ms.date: 2026-10-28
---

Task ID: 521. Slug: resident-authority-extension-521.

## Executive Summary

Use the existing packaged policy as the single authority for the exclusive
2027-02-01T00:00:00Z end. Render and migrate the SQL constraint from it without
renewing rows or changing grants. Document conditional rotation and cost.
No live change is authorized by this source-only loop.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review in order with dated artifacts.
* Use the named branch/worktree, pip only, no Azure, az, secrets or .env.
* Extend through January 31 UTC; retain all guards and USD700 all-in cap.
* Document credential/SQL rotation and cost; live apply pending owner confirmation.
* Commit Conventional Commits with GitHub noreply identity and Copilot trailer.
* Push once and open a PR with Refs #521 only, subject to repository gates.
* Hold /tmp/ama-rpi-heavy.lock nonblocking for every heavy run.

## Goals

Consistent inclusive configuration maximum / exclusive serving instant across
Python, Bicep, SQL and helpers, with explicit boundary regression coverage.

## Scope and Non-Goals

Change packaged policy, SQL rendering/migration, existing tests and relevant
guides/index/log. No UI, model tariff extension, Azure invocation, secret reads,
new resources, roles, routes, minimum replicas or automatic row renewal.

## Functional Requirements

Python, Bicep and secret/deploy helpers continue to share resident-demo.json.
SQL renders AUTHORITY_END and replaces the named existing constraint inside a
transaction with WITH CHECK, preserving rows and rollback on invalid data.
Serving, sessions and admission deny at/after the new instant.

## Non-Functional Requirements

Preserve synthetic provenance, revocation, per-row windows, own-case isolation,
30-minute sessions, strict helper what-if and private SQL access gates.
Document credential rotation without broadening the new-secret-only helper.
No unsupported claim of fresh Azure headroom or zero ongoing cost.

## Acceptance Criteria

* Old November/December cutoffs no longer cap newly approved January config.
* Exact new maximum is accepted for configuration; later instants refused.
* January 31 final instant serves, exact February 1 instant denies.
* SQL renderer has no unresolved tokens; fresh and existing constraints use cap.
* Rotation, conditional added-cost model and USD700 headroom check documented.
* Relevant core/API/infra/tools tests run with actual exits and skips recorded.
* Original independent Review and complete exact-head gate remain prerequisites
  for push; report blocked publication honestly if no permitted gate exists.

## Phase Checklist

<!-- phase: P01 -->
### P01 Policy, SQL and regression coverage

* [x] P01-T01 Change packaged cap and render transactional checked SQL migration.
* [x] P01-T02 Update existing boundary tests; add HTTP and migration regressions.

<!-- phase: P02 -->
### P02 Operations guidance and validation

* [x] P02-T01 Update API/infra guides, knowledge index/log and rotation/cost plan.
* [ ] P02-T02 Run focused then relevant existing suites under nonblocking lock.

<!-- phase: P03 -->
### P03 Review and publication

* [x] P03-T01 Complete one independent Review and preserve original outcome.
* [ ] P03-T02 Commit candidate/evidence; run full gate only if compatible with
  no-az instruction, verify current-base receipt, push once and create PR.

## Locked Test Ownership and Targets

No test removals. Modify existing core showcase/SQL tests, infra secret/deploy
tests and API showcase tests. Maximum additions: eight test methods total.
Canonical target: resident-demo.json. Generated target: rendered SQL (not
checked-in generated files). Semantic coverage: real HTTP boundary and optional
real disposable SQL migration. Regression coverage: exact dates and shared
cap rendering; helper refusal checks retain all guards.
Validation: relevant core/API/infra suites, tools tests, migration checks,
changed-file Ruff and core/API mypy; full final gate only under allowed tools.

## Critique Disposition

One final-candidate critique executed: original verdict Revise, preserved at
.copilot-tracking/plans/2026-10-28/resident-authority-extension-521-critique.md.
PC-001 applied: explicit safe test selection and both az-dependent exclusions
are recorded in details. PC-002 applied: trusted/idempotent migration, row/rights
preservation and failed-replacement rollback assertions are required.
PC-003 applied: final refetch, receipt verification and independent exact-head
assessment are explicit publication prerequisites. All are compatible direct
planner corrections; no new user decision or repeat critique. Source-only
implementation readiness: Ready. Publication remains Blocked.

## Follow-Up Items

1. Owner-confirmed exact live apply including new image, bounded secret
   rotation and SQL row renewal, after all-in cost evidence.
2. Resolve no-az/full-gate incompatibility without weakening publication rules.
3. RV-001: complete existing runtime/SQL/lint validation after an explicit
   coordination event permits nonblocking heavy admission. Eight lightweight
   tool passes are not acceptance evidence for the changed runtime.

Original Review: Complete / Residual work, acceptance withheld, RV-001 High,
RV-002 High, RV-003 Medium. Source task loop is assessed; P02-T02 and
P03-T02 validation/publication remain incomplete. No repeated Review or
post-Review source correction is performed.

## Handoff

Research: .copilot-tracking/research/2026-10-28/resident-authority-extension-521-research.md.
Details: .copilot-tracking/details/2026-10-28/resident-authority-extension-521-phase-details.md.
Changes (implementation-owned):
.copilot-tracking/changes/2026-10-28/resident-authority-extension-521-changes.md.
