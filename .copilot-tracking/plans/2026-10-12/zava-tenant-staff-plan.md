---
title: Initialize Tenant Workbench Staff
description: Approved app-scoped role and staff initialization
ms.date: 2026-10-12
---

## Task Metadata

Task zava-tenant-staff-2026-10-12. Automatic continuation of
zava-workbench-entry-2026-10-12 on existing PR #65.

## Executive Summary

Populate eleven workbench positions with distinct enabled tenant people,
using existing title/group hints only for demo coherence. Preserve the main
admin and existing Coordinator assignment. Add an idempotent initialization
script: validate private roster, add only missing application roles, update
SQL staff/current case owner labels atomically, restart API and verify.
No runtime authorization relaxation or stock regeneration.

## User Decisions and Requirements

* Fix the assigned Coordinator account's authorization failure.
* Replace generated staff names with tenant people.
* Retain the main admin as Programme Manager and Default Access.
* Use current roles/groups for illustrative coherence, or ordinary demo
  allocation when no relevant hint exists.
* No further persona-choice approval is needed after this explicit direction.

## Goals

Make enterprise-app assignments usable through the existing staff boundary,
with repeatable initialization and consistent current staff/workload labels.

## Scope and Non-Goals

infra/scripts/initialize-workbench-staff.py, its infra unit tests,
infra/README.md, mvp/README.md, knowledge-base routing/log, private operator
roster, this application's role assignments, SQL staff/current owner labels,
and API replica restart. No directory-role/group modifications, runtime auth
changes, tenant-name migration, generated stock changes or historical identity
rewrite. Directory data stays outside Git.

## Functional Requirements

* Ten existing staff codes remain stable; add one contractor code with an
  explicit existing supplier scope.
* Validate distinct enabled member people, UUIDs, roles and full roster coverage.
* Preserve existing bindings and matching roles; reject conflicting mapped
  roles, including group-inherited application roles.
* Read-only check mode; retry-safe addition of missing app roles.
* Atomic SQL roster/current owner-label replacement under the shared write lock.
* Restart existing API after success because staff is startup-cached.

## Non-Functional Requirements

No passwords/tokens or directory personal data in Git/log summaries. Retain
fail-closed tenant, exact-role and staff checks. Preserve case IDs, owner codes,
workload counts, supplier restrictions, append-only audit and previous approvals.
Record one new generic initialization audit event, not forged historical actors.
Use existing Azure CLI profiles and SQL driver; no new dependencies.

## Acceptance Criteria

* Synthetic tests cover validation, role conflicts/idempotency, SQL atomicity,
  owner-label-only changes, immutable history and repeat execution.
* Real Graph/SQL check confirms eleven unique bindings and one effective mapped
  app role per selected account; main-admin binding remains.
* All eight role kinds represented; resource accounts excluded.
* API restarted/ready; public root remains 200 and anonymous API remains blocked.
* Existing auth/projection regressions pass and changes published on #65.
* Actual interactive sign-in is explicitly unavailable unless owner verifies;
  operator checks are not claimed as personal browser acceptance.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Initialize, validate and publish
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement initializer and synthetic regressions
<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile private roster, roles and SQL; restart/verify
<!-- rpi:task id=P01-T03 -->
#### [ ] P01-T03: Update initialization guidance and publish

## Test Ownership and Candidate Lock

Primary owns infra/tests/test_initialize_workbench_staff.py; maximum twelve
new test methods, no removals or changes to existing auth/projection assertions.
Semantic: identities, roles, roster consistency and owner-label migration.
Regression: existing initializer/auth/projection tests and live boundaries.
Generated/private directory evidence stays outside Git.

## Critique Disposition

One critique executed, verdict Revise; all four findings disposed directly.
PC-001: use runtime DEFAULT_ROLE_MAP plus deployed overlay, complete paginated
direct/direct-group reads, distinct mapped internal roles, matching position role and
post-grant recheck. Default Access remains untouched.
PC-002: use MssqlStore._Conn `BEGIN IMMEDIATE`, which takes database-scoped
`zavaforward_write` until commit/rollback. Re-read/revalidate inside it; replace
email keys collision-safely and check rowversions/row counts.
PC-003: separate SQL no-op from runtime convergence; apply always restarts all
traffic-serving revisions and checks replacement replica readiness.
Implementation clarified PC-001 using Microsoft's explicit nested-group
limitation: use direct memberOf for effective app assignments, not transitive
membership. Existing directory allocations use direct user grants and are
unaffected. No new user choice or second critique is required.
PC-004: private consistent baseline, exact permitted deltas and prior audit
prefix preservation; twelve methods maximum with subcases. Planning Ready.

## Follow-Up Items

Owner fresh-browser sign-in/photo/account acceptance remains separate.
Existing retained Entra registration naming remains outside this initialization.

## Handoff

Research reused, Planning Readiness Ready; one critique completed/disposed.
P01-T01/P01-T02 complete. Live Graph/SQL reconciliation matches all eleven
positions, idempotent recovery confirmed fresh ready replicas, and exact
private preservation/anonymous-boundary checks passed. Guidance and targeted
regressions are complete; publish P01-T03 before the single Review.
