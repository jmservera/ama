<!-- markdownlint-disable-file -->
---
title: Issue 75 building SQL conformance research
description: Bounded real-engine conformance research
ms.date: 2026-10-18
---

## Research Brief

Status: Complete. Researcher: RPI Agent using rpi-research.
Output mode: convergence. Audience: parent coordinator and PR reviewers.
Research the existing building fixture, home gates, projections and disposable
MSSQL harness, not a new building implementation. Determine focused tests for
durability, independent visibility/conflicts, scoped holds, approval isolation
and role separation. All six caller acceptance points apply.

## Research Parameters

Focused posture selected from the explicit bounded caller direction.
Resolved evidence root: `.copilot-tracking/research/2026-10-18/`.
Initial internal candidates: `src/core/tests/building_fixture.py`,
`src/core/tests/test_buildings.py`, `src/api/tests/test_buildings.py`,
`src/api/tests/test_mssqlstore.py`, component READMEs and existing store.
External candidates: GitHub issue/PR metadata only; no web or legal claims.
Research permits evidence/state writes only. Exclude private support, .env,
configured data, sensors/ingestion owned by issue110, mvp implementation,
Azure/Graph/IAM, real AI, policy/editor/allocation/hold-release authority.

## Extension Registry and Provenance

Repository copilot instructions selected for all paths: src layout, pip-only
dependency restoration, topic branch and privacy-safe publication.
`rpi-research` selected for ordered Wider/Deeper/Contrarian evidence.
Python-specific implementation conventions will be applied at Implement.
Research specialist skipped: one tightly coupled local contract trace, no
independent uncertainty warranting delegation. Independent critique remains
required in Plan; one original Review remains required after implementation.

## User Participation and Research Decisions

Explicit parent-authorized automatic bounded task; no intake ambiguity and no
additional mode prompt. Stop after original Review and draft publication.

## Direction Controls

Frozen base and initial HEAD: `9d625a09e34491ecf9fd27ffc7d59e67c2373b29`.
Branch: `test/building-sql-conformance-75`, clean at intake, no existing PR.
PR398 merged at this exact base; preserve its governance continuity.
Issue75 remains open. Dependency290 is closed; parent74 is not execution order.
Production changes require observed attributable real-SQL failure and recorded
plan amendment; material intent/authority decisions return to coordinator.

## Research Questions

* Q1: What existing fixture/store API proves persistence without seed reread?
* Q2: What existing SQL infrastructure proves commit visibility and stale refusal?
* Q3: How do scoped hold gates and missing home approvals behave independently?
* Q4: Which existing projections distinguish Finance, staff and Contractor?
* Q5: Which exact local commands and resource cleanup prove the bounded result?

## Prior Knowledge Gate

Caller reports runtime delivered by PR310, not absent. Verify against exact
base, not pinned578631ac. Required original case study and memory read;
addendum/index opened at their current 2026-10-18 context. Their exercise
approval and synthetic evidence boundaries remain distinct from operational
acceptance.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline source inventory confirmed PR310's existing runtime and JSON/SQLite
tests. The MSSQL module already owns destructive wipe/factory and CI executes
the whole module. Reflection: add building-specific classes there, not a service.

#### Wave 2: Deeper

Inspected reusable fixture, package capacity setup, core gate tests, API loopback
fixture, SQL checked-document save and sync, and driver dialect. Q1-Q4 answered
by C2-C6. Reflection: reuse `building_fixture.open_store` with a scoped test-only
patch of its SQLite constructor to the existing MSSQL factory; it retains its
explicit contract/capacity setup. API fixture invokes that same helper.

#### Wave 3: Contrarian

Challenged the assumption that replay alone establishes persistence or authority.
Existing reopen uses an extant seed, so the new test must delete its constructed
seed before reopening. A refreshed reader alone is not stale-writer proof;
retain a stale document snapshot under its local lock while another independent
connection commits, then require ConflictError and independently read winner.
Clear building is not a positive home approval: separately remove resident,
funding and technical prerequisites; separately reject QA handover against
accepted/closed sibling. HTTP roles must also run on actual SQL, not pure views.
Reflection: these counterexamples sharpen tests without any runtime change.

#### Parent Synthesis and Disposition

Accept extending the existing module and shared fixture (C2-C6). Reject new model,
editor, DDL, service, sensor plumbing and allocation/release authority as duplicate
or out of bounds. Defer operational register rights and live/human acceptance.
No second cycle needed: remaining uncertainty is executable conformance, not a
missing source contract. Source and commands cover the bounded planning questions.

## Evidence Log

* W1: GitHub issue75 body/comment and dependency290 retrieved 2026-10-18 via gh:
  https://github.com/jmservera/ama/issues/75 and
  https://github.com/jmservera/ama/issues/290. Issue75 OPEN, dependency CLOSED.
* W2: https://github.com/jmservera/ama/pull/398 retrieved 2026-10-18:
  MERGED, merge commit equals frozen base.
* C1: `docs/case_study_48_addendum.md:112` separates per-home approvals,
  role rights and synthetic exercise decisions from live authority.
* C2: `src/core/tests/building_fixture.py:13` and `:126`: wholly constructed
  two-home fixture plus reusable store/capacity initialization.
* C3: `src/core/tests/test_buildings.py:50`, `:85`, `:234`, `:260`: missing
  approvals, scoped work orders, QA separation and SQLite stale document test.
* C4: `src/api/tests/test_buildings.py:22`, `:112`: real loopback server,
  Finance/staff/Contractor projections with server-enforced denial.
* C5: `src/api/tests/test_mssqlstore.py:28`, `:31`, `:39`: opt-in, wipe,
  reusable MSSQL factory; `src/core/src/zava_forward/core/sqlstore.py:554`
  and `:695` implement transactional checked-document persistence.
* C6: `.github/workflows/mvp-ci.yml:101` runs existing MSSQL module;
  `.github/workflows/src-ci.yml:73` configures project lint/type/tests.
* W3: https://github.com/jmservera/ama/pull/310 retrieved 2026-10-18:
  merged 2026-10-15 at d3c748f7bc107283af337a8ca47118c24eb98674.
* C7: Initial prerequisite probe of `test_mssqlstore.SharedSqlIsPortableTests`
  failed import before tests: system Python lacks installed zava_forward.
  Dependency restoration is therefore authorized, not a conformance failure.
  Docker is responsive (29.9.0), SQL2022 image cf8f0ab2ebe6 already local.

## Alternatives and Decision State

Selected: focused new building conformance tests and HTTP replay in existing
MSSQL module. Retain local core/API regressions. New generic harness rejected
because factory and wipe already exist. No production defect evidenced.

## Planning Readiness

Ready. Research disposition: executed. Q1-Q4 answered above; Q5 uses existing
src unittest commands, configured Ruff/mypy and migration regression. Unique
loopback container and unique database, explicit environment only, generated
ephemeral password withheld from artifacts, exact-ID cleanup in finally.
Image/nonroot rerun is redundant if production, Dockerfiles, manifests and image
inputs remain unchanged; document this applicability decision, not a Pass.

## Self-check and Continuation

Ordered Wider/Deeper/Contrarian cycle complete inline; no worker implied.
All material source findings have stable IDs/paths; external metadata dated.
No private datasets or support read, no source edits during Research.
Automatic parent may transition to Plan with phase details and one independent
critique before implementation.

## Risks and Residual Uncertainty

Actual local SQL execution not yet attempted. Opt-in skips are Not run, not Pass.
