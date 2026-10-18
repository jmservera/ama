<!-- markdownlint-disable-file -->
---
title: Issue 75 original building SQL Review
description: Single post-implementation Review of bounded conformance evidence
ms.date: 2026-10-18
---

## Scope and Evidence

Task 75 / issue-75-building-sql, 2026-10-18. One original Review, no repeat.
Scope: complete bounded test-only implementation P01/P02 and P03 readiness;
publication follows Review and is not a pre-existing validation result.
Base: 9d625a09e34491ecf9fd27ffc7d59e67c2373b29.
Assessed executable blob: src/api/tests/test_mssqlstore.py
351c81ab24c09811a4e3195b9d88482456482b01.
Assessed documentation blob: src/api/README.md
3c8b48ae6c6a37d38100a9c860768727fa162073.

Compared artifact set:

* .copilot-tracking/research/2026-10-18/issue-75-building-sql-research.md
* .copilot-tracking/plans/2026-10-18/issue-75-building-sql-plan.md
* .copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-18/issue-75-building-sql-plan-critique.md
* .copilot-tracking/changes/2026-10-18/issue-75-building-sql-changes.md
* All issue-75 execution text records in changes/2026-10-18, adverse originals
  included, plus exact two-file git diff and unchanged building/HTTP fixtures.

## Opening Review State

Goal: assess all six bounded criteria and critique dispositions against actual
tests/evidence, not declare full issue or operational acceptance.
Evidence ready: P01/P02 checked, phase details current, original critique Revise
and PC-001-PC-004 dispositions retained. Single successful actual SQL selection
and lifecycle probes available; first failed runs remain preserved.
Acceptance basis: caller bounds and plan A1-A6. First comparison: source diff,
test assertions, state/cleanup and validation coverage.
Read-only authority: only this Review record may change in Review.
Initial blockers: none. No independent lens dispatched: the complete coupled
diff/evidence fits direct assessment; independent Plan critique is distinct.

## Execution Status

Complete. One direct post-implementation Review, no second Review and no
post-Review source correction. Completion does not mean human approval.

## Plan-to-Change Reconciliation

| Scope | Evidence and assessment | Reconciliation |
| --- | --- | --- |
| P01/P01-T01 | Two classes, five semantics plus three inherited HTTP tests; fixture and existing factory reused, no table additions | Complete |
| P02/P02-T01 | 117 core pass, 47 API/portable pass plus eight explicit opt-in skips; eight actual SQL pass separately; final static/migration pass | Complete |
| P03/P03-T01 | One original Review executing now; draft publication remains parent-owned next action | Correctly unchecked at assessment |
| Follow-Up Items | Operational rights/policy/human/accessibility/live evidence not implemented or claimed | Distinct coordinator work |

## Completed Work Assessment

| Criterion | Actual assertion/evidence | Assessment |
| --- | --- | --- |
| A1 | Save full record with explicit dependency, close original session, unlink seed, reopen with nonexistent seed; full buildings/cases equality, separate home costs and no evidence/allocation in shared view | Covered on actual SQL |
| A2 | Distinct raw connections, synchronized hold read, locally retained stale snapshot, competing committed version/name, ConflictError on attempted hold erasure, third connection reads exact winner | Covered; controlled interleaving, not a parallel load/throughput claim |
| A3 | Correct building reason with valid resident bindings for advance/issue/reissue; unchanged cases/orders; ZF-2/OTHER and ZF-3/SHARED positive controls, supplied commitment/appointment, sibling booked and retained hold/audit | Covered on actual SQL |
| A4 | Three independent missing resident/funding/technical reasons, clear building, unchanged reopened home state; explicit Submitted-to-Handed-over refusal against accepted/closed sibling, full reopened state equality | Covered; no invented approvals |
| A5 | Existing real loopback HTTP suite inherited unchanged, scoped constructor patch selects MSSQL, existing Finance/staff/Contractor/unknown/unauthenticated denial and evidence/cost separation | Covered; static asset serving is not human/browser acceptance |
| A6 | Unique task databases/containers, loopback ports, known explicit local configuration, eight actual tests without skips; four attempts cleaned by exact ID; three actual failure-cleanup probes | Covered for local constructed-engine slice |

Inventory: executable test module and directly related API README only.
No package source, allocation model, release authority, sensor ingestion,
workflow, Dockerfile, dependency manifest or web change. PR398 source is retained
byte-for-byte from frozen base. Wipe's sole change closes its existing temporary
connection in finally; no DDL/table-list widening. Existing migrated harness
exemptions remain, no new lint/type exemption.

## Implementation-Time Update Assessment

| Update | Trigger and disposition | Assessment |
| --- | --- | --- |
| Actual environment selector names | Source verified local scanner/password auth before execution, details corrected | Local factual refinement, approved intent preserved |
| Registry actor instead of staff-list index | First SQL run had two fixture errors; exact adverse log retained; registry identity fixes test selection only | Within locked test scope, not a runtime defect or authority change |
| Restore missing dependencies | Observed loader/tool failures before pip installation; isolated task venv | Allowed dependency restoration, no manifest change |
| Runtime-path/cache cleanup for mypy | First invocation included runtime PYTHONPATH, cache persisted; archived base and fresh current analysis pass, final standard command passes | Invocation correction with adverse originals retained |
| Fault-probe import path | External script needed explicit cwd path unlike unittest; original loader failure and cleanup retained | Probe-only invocation correction |

No material intent, architecture or authority divergence required coordinator
decision. No production failure was inferred from fixture mistakes. Source was
not changed after successful SQL conformance. No significant dependent work
resumed without a required decision.

## Critique and Material Revision Assessment

Original independent critique remains Revise, unchanged. PC-001 exact causes and
bindings, PC-002 orthogonal sibling/package control, PC-003 sanitized local
execution and PC-004 immediate/partial setup cleanup are each disposed in plan
and realized in tests/execution. Cleanup is substantiated by three probes on
actual SQL, not only code inspection. One critique only; no new material scope.

## Findings and Defects

No substantive implementation defect or unresolved bounded acceptance gap found.
No RV defect invented to represent intentionally excluded operational work.
This is an agent engineering Review, not named human acceptance or the
coordinator's adjudication of full issue75 criteria.

## Validation Evidence

All logs below are under `.copilot-tracking/changes/2026-10-18/`.

| Command / evidence | Status | Result and limits |
| --- | --- | --- |
| src/core: python -m unittest test_buildings test_quality_procurement -q | Passed | 117 tests |
| src/api: python -m unittest test_buildings test_procurement_api test_role_matrix test_mssqlstore.SharedSqlIsPortableTests test_mssqlstore.MssqlBuildings test_mssqlstore.MssqlBuildingHttp -q | Passed with explicit Not run | 55 total; 47 passed, eight opt-in SQL skips |
| src/api, owned SQL: python -m unittest test_mssqlstore.MssqlBuildings test_mssqlstore.MssqlBuildingHttp -v | First run failed, later passed | First six pass/two actor-fixture errors retained in issue-75-sql-execution.txt; final eight pass/zero skips in issue-75-sql-rerun-execution.txt |
| Actual SQL failure-cleanup probes | First invocation unavailable, later passed | Original loader failure retained; final three probes pass in issue-75-sql-fault-final-execution.txt |
| python tools/rename-zava-tests.py | First failed missing tools, final Passed | 25 tests, issue-75-static-final-execution.txt |
| src/api: ruff check .; ruff format --check . | Passed | Existing configured harness exemptions unchanged |
| src/api: mypy | Initial failed tools/cache, final Passed | Standard final command succeeds on 58 files; archived base/fresh current analysis retained |
| git diff --check | Passed | Exact assessed two-file diff |
| Application image/nonroot/browser/human accessibility checks | Not run, redundant/outside scope | No app image/source/web input changed; no fresh acceptance claim |
| Full all-engine suite, Azure, real AI, live application | Not run | Outside bounded constructed test slice |

Actual SQL: Microsoft SQL Server 2022 RTM-CU27-GDR 16.0.4305.5, Linux Developer
edition, image sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718.
Successful test container e36e9fb1059966ed892268f96f0e33921c90e2b32910809ca18180914e2ab98d
and database issue75_1d6c6df9eb6f41a883fedb507799707c removed. All attempt logs
record exact-ID removal exit0 and empty remaining lookup; subsequent task-prefix
listing empty. Fixture law store remains explicitly unavailable/Unknown on
HTTP side effects, not a claimed regulatory check.

## Plan Follow-Up Assessment and Routing

| Item | Why distinct | Owner / route |
| --- | --- | --- |
| Full issue criteria proof and remaining acceptance | This is a bounded follow-up, not closure of parent hierarchy or all requirements | Coordinator reviews draft/evidence; issue stays open |
| Operational register/update rights and allocation policy | No actual company authority/policy supplied; building screen stays read-only | Coordinator-owned requirements/authority follow-up |
| Named human/accessibility and live application evidence | Constructed loopback/SQL tests cannot substitute for people or live operations | Coordinator-owned acceptance follow-up |

## Blockers and Remaining Work

No bounded implementation blocker. Parent must commit all issue artifacts/tests,
publish draft to main with Refs #75 and preserve exact base. P03 publication was
not completed at assessment and is not retrospectively claimed here.
No source correction or second Review authorized.

## Outcome

Outcome: Conformant **within the bounded test-only local SQL conformance scope**.
Rationale: A1-A6 have source-grounded assertions and actual engine evidence,
critique concerns are realized without runtime expansion, adverse originals
and all skip/unknown boundaries are retained. This does not approve operational
FR-002 delivery, register writes, allocation policy, human/a11y acceptance,
Azure/AI/live application or whole-issue completion.

## Closeout Routing Record

| Finding class | Destination | Next action |
| --- | --- | --- |
| Implementation defect | None | No source corrections |
| Decision gap / invalid assumption | None in bounded task | Preserve external authority gates |
| Material research gap | None in bounded task | No new research loop |
| Distinct residual work | Coordinator | Review draft against full issue and remaining operational/human/live gates |

Execution: Complete. Outcome: Conformant for bounded scope.
Parent continuation: publication only, then stop as explicitly authorized.
