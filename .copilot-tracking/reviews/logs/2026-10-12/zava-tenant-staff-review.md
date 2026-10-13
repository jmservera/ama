---
title: Tenant Staff Initialization Review
description: Single post-implementation review of app-scoped onboarding and preservation
ms.date: 2026-10-12
---

## Scope and Evidence

* Task: zava-tenant-staff-2026-10-12.
* Scope: full P01 tenant staff initialization, published source 3073285 on #65.
* Plan: .copilot-tracking/plans/2026-10-12/zava-tenant-staff-plan.md
* Details: .copilot-tracking/details/2026-10-12/zava-tenant-staff-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-12/zava-tenant-staff-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-12/zava-tenant-staff-changes.md
* Research: .copilot-tracking/research/2026-10-12/zava-tenant-staff-research.md
* Source: infra/scripts/initialize-workbench-staff.py
* Synthetic coverage: infra/tests/test_initialize_workbench_staff.py
* Existing runtime authorization, shared SQL adapter/ledger and recorded live
  Graph/SQL/private preservation/restart/public-boundary evidence.

## Opening Review State

* Goal: compare approved onboarding and preservation with implementation and
  live convergence, without converting operator checks into browser acceptance.
* Scope: P01 and all three completed task markers; no parent Review repetition.
* Readiness: current plan/details/changes, single critique and dispositions,
  source/tests, private exact comparison summaries and live ready replicas.
* Acceptance basis: eight role kinds across eleven distinct tenant people,
  protected admin/Coordinator, stable codes/history, scoped Contractor,
  repeatable private initialization, unchanged fail-closed runtime and #65.
* First comparison: role/private-input validation and protected SQL identity
  boundary, then exact preservation, recovery and documentation/publication.
* Authority: evidence reads and this review record only; parent owns state.
* Initial blockers: none; user browser acceptance explicitly unavailable.

## Execution Status

Complete. One post-implementation comparison of the full supplied boundary.
No second critique, repeated parent Review, source edits or invented browser
session.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Operator initializer and twelve synthetic methods; 27 infra tests | Reconciled; existing tests untouched |
| P01-T02 | Eleven live profiles, app grants, exact snapshots, no-op recovery and fresh replicas | Reconciled; no weakened auth or stock regeneration |
| P01-T03 | Generic guides, routing/log, private listing and published 3073285 | Reconciled; privacy scan/link checks passed |
| Follow-Up Items | Real-browser acceptance and retained tenant branding | Outside P01; routed distinctly below |

All P01 markers and handoff statements are current. No remaining active plan
work or implementation blockers.

## Completed Work Assessment

* Private input validates enabled members, resource-account exclusions, full
  code coverage, distinct UUIDs/UPNs and protected existing bindings. New
  positions require Contractor and a currently existing supplier.
* Runtime role evaluation merges DEFAULT_ROLE_MAP with the deployed overlay,
  counts distinct mapped internal roles, reads complete fixed-host pages,
  rejects conflicting direct/direct-group roles, preserves Default Access and
  adds missing grants for this application only. Post-write reads precede SQL.
* Live checks show eleven matching unique profiles across eight role kinds and
  twelve direct assignments: eleven business-role grants plus preserved Default
  Access. No assigned groups, directory-role changes or group-membership writes.
* SQL uses the API adapter's transaction-owned exclusive zavaforward_write lock,
  fresh protected-state reads, collision-safe roster key replacement, expected
  case versions/row counts, one sequence advance and one generic chained audit.
* Private exact comparison verifies all 980 cases/owner codes/supplier scopes/
  non-owner fields, ten original codes/admin binding, six recommendations and
  all nineteen historical audit rows. Exactly 980 current owner labels changed
  once; prior embedded history remains identical; the one appended entry and
  audit head/chain validate.
* First apply committed SQL but a CLI operation interrupted restart proof.
  The no-op recovery returned zero changes/grants and confirmed replacement
  ready replicas for every serving revision. Repeated preservation checks
  demonstrate no additional audit/sequence/version mutation.
* Public welcome/health remain 200; anonymous me/cases are 401. Runtime tenant,
  exact mapped-role and oid gates are unchanged; email fallback was not enabled.
* Guidance explains app role versus staff binding, isolated management profile,
  private input, repeat/restart semantics and historical boundaries. Complete
  directory/people allocation reports remain outside Git.

## Implementation-Time Update Assessment

| Update | Trigger and disposition | Assessment |
| --- | --- | --- |
| Sanitized CLI operation and post-SQL recovery message | Live partial-convergence failure; retained safe retry/no-op | Local in-scope correction, no user decision needed |
| Direct memberOf instead of transitive groups | Official Entra documentation says nested groups do not inherit app assignment | Preserves runtime-equivalent intent; plan/details/research/guidance reconciled before Review |
| prepare_roster/nested-group test subcases | Exact validation needed within twelve-method ceiling | No extra methods or weakened existing assertions |
| Named test import path | Existing test_mvp fixture is a top-level test module | Corrected PYTHONPATH; successful actual regression execution |

## Critique and Material Revision Assessment

PC-001 through PC-004 were directly disposed after the single candidate
critique. Current source/evidence demonstrate effective-role completeness,
shared locking, failed-restart/no-op recovery and exact private preservation.
The direct-group clarification is supported by official evidence and does not
change the owner's allocation or authority. No divergent user decision,
unresolved planning assumption or unjustified dependency bypass was found.

## Plan Follow-Up Assessment

| Follow-up | Why outside P01 | Owner and route |
| --- | --- | --- |
| Fresh-browser role/account acceptance | Operator Graph/SQL checks are not actual interactive sessions | Owner; distinct acceptance follow-up, RV-001 |
| Retained tenant registration/role naming | Deliberately retained compatibility bridge, unrelated to SQL onboarding | Later naming research/plan, RV-002 |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Real-user acceptance remains unobserved

* Class: non-blocking residual follow-up, not an implementation defect.
* Evidence: changes and plan expressly exclude invented browser sessions.
* Impact: successful interactive access, coordinator My work, photo, logout
  and account switching cannot be claimed from operator convergence.
* Destination: distinct owner acceptance follow-up.
* Next action: fresh sign-in using assigned tenant people; confirm intended
  role/workload/supplier boundaries and account UI. Never request passwords.
* Required human acceptance: [ ] Actual role/account browser checks.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Retained tenant naming is a separate migration

* Class: non-blocking residual follow-up, not an onboarding defect.
* Evidence: approved non-goal and deployed role-map compatibility bridge.
* Impact: old application role values remain intentionally compatible; this
  initialization does not certify complete tenant-side branding replacement.
* Destination: distinct naming work, beginning with rpi-research.
* Next action: inventory actual registration/service-principal names, claims
  and dependants before proposing changes. Do not rename operational claims
  opportunistically or treat this as permission to mutate directory roles.

## Defects

None identified within the assessed P01 boundary.

## Validation Evidence

| Validation | Status | Result |
| --- | --- | --- |
| Infra unittest discover | Passed | 27 tests, including exactly twelve new methods |
| Existing auth/role_matrix/sqlreads/quality_procurement | Passed | 63 tests; includes real projection/privacy and supplier boundaries |
| First named-test invocation | Failed, resolved before Review | Fixture import path corrected, not an application defect |
| Live read-only initializer after final direct-group refinement | Passed | Eleven positions; all differences zero |
| First apply restart proof | Failed, resolved before Review | Explicit incomplete result; safe no-op recovery succeeded |
| Idempotent apply/restart | Passed | Zero added grants/staff/labels; fresh ready serving replicas |
| Exact private before/after SQL comparison | Passed | Permitted deltas only; valid preserved audit/history and admin binding |
| Live public/anonymous boundaries | Passed | Root/health 200; me/cases 401 |
| Private-data scan, relative links and diff checks | Passed | No selected identities in twelve changed files |
| Published 3073285 MVP workflow 38319331882 | Passed | test, image and mssql jobs succeeded |
| Published 3073285 validation 38319331881/38319331894 | Passed | Both validation workflows succeeded |
| Actual user browser acceptance | Unavailable | Owner must perform separate real-session checks |
| Capstone scoring | Outside boundary | Publication rubric is not role-onboarding or capstone acceptance |

## Blockers and Remaining Work

No P01 blockers or remaining active markers. RV-001/RV-002 are separate
follow-ups; no source changes or repeat Review are authorized by this record.

## Outcome

Conformant for the approved operator initialization/preservation boundary.
Execution Complete is separate from this outcome. No production approval,
professional competence, new user sign-in or account-photo acceptance is
inferred. The historic parent Review outcome remains unchanged.

## Closeout Routing Record

| Class | Destination | Next owner/action |
| --- | --- | --- |
| Implementation defects | None | No later correction required by this record |
| Decision gaps | None | Confirmed user allocation preserved |
| Material in-scope evidence gaps | None | Required operator evidence is present |
| Non-blocking residual work | Distinct follow-ups | RV-001 owner acceptance; RV-002 naming research |

Return to the automatic parent for Follow-up selection. The task can complete
without stopping the automatic session or silently beginning either child.
