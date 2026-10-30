---
title: Sensor ingestion consistency issue 188 final-candidate plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: 188.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/sensor-ingestion-consistency-188-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/sensor-ingestion-consistency-188-phase-details.md.
* Critique execution status: Complete.
* Critique count: one final-candidate assessment; no additional agents or critique passes.

## Inputs and Criterion Boundary

* Caller direction: Research, Plan, Implement, Review; local commit only;
  Refs #188 only; no Azure, deployment, sign-in, credential files, secrets or
  push. This critique writes only its specified output.
* Candidate sources: the plan and phase details above, plus
  .copilot-tracking/research/2026-10-30/sensor-ingestion-consistency-188-research.md,
  C1-C5 and W1-W3. The supplied W1 issue body was checked read-only through
  gh issue view 188.
* Relevant implementation evidence: src/core/src/zava_forward/core/synthetic/sensor_stream.py,
  sensor_backfill.py and climate_history.py in that same synthetic directory;
  src/core/src/zava_forward/core/sensor_consumer.py;
  src/core/tests/test_sensor_stream.py;
  src/core/tests/sensor_consumer_fixture.py;
  src/core/tests/test_sensor_consumer.py;
  src/api/tests/test_iot_stream.py; src/api/tests/test_sensor_ingestion.py;
  src/core/pyproject.toml; tools/rpi-checks.py.
* Context and validation policy: docs/case_study_48_original.md;
  docs/case_study_48_addendum.md, opening context;
  docs/reference/README.md; docs/reference/memory.md;
  docs/reference/research/iot-sensor-analytics-research-plan.md, bounded
  streaming and issue-evidence sections; src/README.md, local RPI gate and
  stabilization validation ladder.
* Criterion boundary: jointly query live/backfill series per home, demonstrate
  statistical handover within a declared tolerance, and replay a window
  idempotently. The candidate can establish constructed local evidence, not
  actual Hub transport or Azure SQL acceptance. #110 remains a live dependency;
  #183/#186 delivery is recorded by the supplied research, not re-audited here.
* Fixed implementation constraints: core owns model/report semantics; API owns
  admission, fake receiver and actual task-owned SQL Server tests; remove no
  tests; add at most two test files and ten test methods. Corrections below
  must fit those limits, using existing tests and subtests where appropriate.
* Workspace observed: feat/sensor-ingestion-consistency-188 at
  a31048f15fa3120c58bacd22a375d86ae5ab7431. Existing untracked research,
  plan, phase details and lifecycle state were preserved.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| User scope and W1-W3 | Covered | Local commit, Refs #188, no cloud execution and outstanding live acceptance are explicit. |
| C1/C2, P01-T01 | Covered | Full-origin composed generation, optional inputs, legacy compatibility and descriptor provenance reuse existing model contracts. |
| AC1, C3-C5, P02-T01 | Partial | Two-home CSV/admission/SDK/SQL proof is specified, but its actual SQL Server execution is not wired to a concrete owned invocation; PC-001. |
| AC2, P01-T01, P02-T01 | Partial | Reference-adjusted mean-step, population standard deviations, point error and strict metadata/coverage checks are credible; tolerance-boundary proof is missing; PC-003. |
| AC3, P02-T01 | Partial | Reopen, overlap/full replay, accepted receipts and invariant durable tables are specified; actual SQL execution inherits PC-001. |
| P02-T01 test constraints | Covered | Ownership, no removals and two-file/ten-method limits are fixed and need no expansion. |
| P02-T02 validation and evidence | Partial | Original Review, local commit and full gate sequencing are explicit, but lock/path admission conflicts must be resolved as blocked validation where necessary; PC-002. |
| Dependencies and residual risks | Covered | Local synthetic work is independent of unavailable live authority; no whole-issue closure or physical calibration is inferred. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 1 Medium, 0 Low.
* Rationale: the implementation direction is credible, but the candidate
  cannot yet substantiate its promised actual SQL Server coverage or execute
  the written validation procedure within current constraints. The declared
  tolerance contract also needs a small, bounded verification addition.
  These are direct planner corrections, not significant or divergent choices.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The standard full gate does not execute the promised sensor proof on SQL Server

* Related IDs: AC1, AC3, C5, P02-T01, P02-T02.
* Evidence: phase details lines 43-50 require actual local SQL Server through
  ZF_SENSOR_MSSQL. src/core/tests/sensor_consumer_fixture.py:67-80 chooses
  MssqlStore only when ZF_SENSOR_MSSQL=1. In tools/rpi-checks.py:31-40,
  SQL_SELECTORS omits test_sensor_ingestion and test_iot_stream; its sql()
  environment at lines 1721-1732 sets ZF_TEST_MSSQL, not ZF_SENSOR_MSSQL.
* Concern: API discovery plus the existing full SQL gate does not establish
  that the new joint-query and reopened-window assertions execute against
  SQL Server. Merely naming the fixture mode does not specify their execution.
  That fixture also has destructive reset behavior, so ambient configured
  database credentials cannot safely fill the gap.
* Impact: a passing full receipt could coexist with SQLite-only issue-specific
  coverage while the final evidence claims actual SQL Server proof.
* Smallest useful change: name the API-owned selector(s) and a separate,
  explicit issue-local invocation that enables ZF_SENSOR_MSSQL=1 only against
  a verified task-owned loopback SQL Server, with bounded ownership, readiness,
  cleanup and command/result evidence. State that ordinary discovery and the
  unmodified full gate do not cover this assertion on SQL Server. If compliant
  ownership or execution is unavailable, mark this proof blocked rather than
  inferred. Do not expand tests or modify the gate simply to add selectors.
* Action owner: planning parent, then implementation parent for execution.
* Exact resolving evidence: revised P02 details identify actual test IDs,
  fixture switch, owned database admission and failure/cleanup conditions.
  Implementation evidence must subsequently record the selected tests,
  non-skipped execution, confirmed MssqlStore backend and results for joint
  queries and reopened full-window replay, or explicitly record them blocked.
* Decision route: direct planner correction; no user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Heavy-validation instructions conflict with current path and admission constraints

* Related IDs: caller constraints, P02-T02.
* Evidence: plan lines 99-101 prescribe flock -w 600 against
  /tmp/ama-rpi-heavy.lock. Phase details lines 59-62 require the full gate and
  outside-repository logs. Current execution instructions prohibit temporary
  directory file operations and require created files relative to the working
  directory. tools/rpi-checks.py:2272-2286 itself opens the fixed /tmp lock;
  src/README.md's stabilization ladder requires nonqueued admission, actual
  holder inspection and a blocked result when another owner holds the lock.
* Concern: avoiding a nested lock does not make the fixed lock path permitted.
  Waiting 600 seconds also contradicts the documented nonqueued coordination
  policy. Relocating only the shell lock would neither fix the runner's path
  nor preserve serialization with other owners.
* Impact: the written sequence cannot be executed as promised under current
  constraints, and attempting it risks prohibited writes or foreign-owner
  interference. Required full-gate evidence cannot be silently waived.
* Smallest useful change: reconcile validation paths and admission explicitly.
  Require nonqueued heavy admission and record busy ownership as blocked.
  Do not execute a gate whose fixed writes violate the current prohibition;
  mark that gate blocked with the exact source and resume condition. Preserve
  the mandatory external-receipt requirement rather than substituting an
  in-repository receipt, a second lock or a claimed pass. Do not change the
  shared runner, weaken the gate or seek an unnecessary user scope expansion.
  Continue independent permitted implementation and local-commit work, with
  incomplete validation stated accurately and publication still prohibited.
* Action owner: planning parent.
* Exact resolving evidence: P02-T02 no longer directs forbidden path writes
  or queued lock acquisition; it names compatible validation where available,
  lists the fixed-path full gate as blocked when incompatible, and states
  that resumption requires a compliant execution context and free ownership.
  Final evidence must retain that blocked status unless a genuinely compliant
  complete run and external receipt exist.
* Decision route: direct planner correction and truthful blocker recording;
  no user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Zero-tolerance drift tests do not verify the declared tolerance contract

* Related IDs: AC2, P01-T01, P02-T01.
* Evidence: plan lines 44-45 allow finite nonnegative tolerances for point
  error and distribution change; lines 60-61 require only zero-tolerance
  clean/drift controls. Phase details lines 29-35 add explicit per-channel
  tolerances and three metric families, but name only shifted values, dates
  and missing data as completion tests.
* Concern: an implementation that ignores every nonzero tolerance and uses
  equality could satisfy the stated acceptance tests. Likewise, a single
  point-error failure could mask broken mean-step or standard-deviation
  decisions. Neither case demonstrates the promised tolerance semantics.
* Impact: the report could give incorrect within/outside-tolerance results
  despite the positive and negative zero-tolerance evidence passing.
* Smallest useful change: add bounded core subtests specifying inclusive
  tolerance-boundary behavior, values just within/at/above a nonzero declared
  limit, independent temperature/humidity channels, and rejection of negative
  or nonfinite tolerances. Exercise mean-step and standard-deviation failures
  with point-error tolerance deliberately permissive, plus point-only failure,
  so each promised metric's decision is observable. Keep all existing tests
  and stay within the locked two-file/ten-method budget.
* Action owner: planning parent, then core implementation/test owner.
* Exact resolving evidence: the revised P01/P02 test contract declares the
  comparison rule and these cases; core test results subsequently demonstrate
  boundary acceptance/rejection and independently observable metric failures.
  No physical accuracy or live sensor calibration claim accompanies them.
* Decision route: direct planner correction; no user decision required.

## Strengths and Residual Risk

* Full-origin projection before slicing correctly avoids restarted RNG and
  household-history discontinuities. The existing legacy replay tests provide
  a concrete compatibility baseline.
* Continuous same-input reference adjustment avoids misclassifying changing
  weather or dated works as an ingestion seam. Exact identity, units, schema,
  UTC grid and complete coverage supplement, rather than replace, statistics.
* Two canonical homes, including a long stock ID, persisted CSV inputs and
  independently configured units make the proposed local proof materially
  stronger than the existing two-point legacy seam.
* Reopened persistence and unchanged reading/delivery/DQ outcomes are explicit.
  The plan preserves original adverse Review evidence and separates hosted,
  human and live approval from engineering checks.
* Actual authenticated Hub transport, Azure SQL query/restart, physical model
  validity and whole #188 acceptance remain unproven under current authority.
  This critique does not request their execution or issue closure.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents planner correction or independent local
  implementation.
* The mandatory full gate is execution-blocked while its fixed path operations
  conflict with current constraints. Actual SQL evidence is also blocked unless
  a compliant owned execution route is specified and run. Neither is a reason
  to invent an acceptance result or use Azure.

## Limitations

* This is one source-grounded plan assessment, not an implementation Review,
  test run, receipt verification or live-system audit.
* No application tests, Docker containers, heavy locks, gate runs, Azure calls,
  credential-file reads, source edits, commits or pushes were performed.
* Supplied dependency dispositions were considered within their recorded
  boundary; no open-ended dependency or external research was undertaken.
* Plan, phase details, research and lifecycle state remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: specify the actual owned SQL execution route, reconcile
  heavy-validation blockers and add tolerance subtests to the existing bounded
  test contract; then finalize the corrected plan without another critique.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/sensor-ingestion-consistency-188-plan.md](.copilot-tracking/plans/2026-10-30/sensor-ingestion-consistency-188-plan.md) | Assessed final-candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-30/sensor-ingestion-consistency-188-phase-details.md](.copilot-tracking/details/2026-10-30/sensor-ingestion-consistency-188-phase-details.md) | Assessed task contracts, unchanged. |
| [.copilot-tracking/research/2026-10-30/sensor-ingestion-consistency-188-research.md](.copilot-tracking/research/2026-10-30/sensor-ingestion-consistency-188-research.md) | Supplied focused research, unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-30/sensor-ingestion-consistency-188-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/sensor-ingestion-consistency-188-plan-critique.md) | Complete critique and full actionable finding set. |

## Next Steps

Active planning parent: resolve PC-001 through PC-003 directly, finalize without
another critique, and continue the authorized local RPI loop with blocked
validation retained where necessary. No user action is required.
