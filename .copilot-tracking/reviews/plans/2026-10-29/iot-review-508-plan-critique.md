---
title: PR 508 IoT review corrections final-candidate plan critique
description: Independent assessment of the focused cancellation and pacing correction plan
ms.date: 2026-10-29
---

## Metadata

* Task ID: pr-508-review-fixes-2026-10-29.
* Slug: iot-review-508.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/iot-review-508-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/iot-review-508-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: fix shared cleanup interruption ownership for both SDK
  runners, validate supplied Pacer rates and NaN deadlines before clients, and
  honor nearer active pacing targets while retaining bounded paused polling.
  Keep source under src/, use existing outside-package test files, remove no
  tests, add at most six methods, and introduce no generated targets.
* Supplied research: .copilot-tracking/research/2026-10-29/iot-review-508-research.md,
  including C1-C5 and its accepted cancellation-resistant SDK limitation.
* Source evidence: src/api/src/zava_forward/api/iot_stream.py and
  src/core/src/zava_forward/core/synthetic/sensor_stream.py.
* Test evidence: src/api/tests/test_iot_stream.py,
  src/api/tests/test_sensor_ingestion.py and src/core/tests/test_sensor_stream.py.
  The owning READMEs and both project pyproject.toml files were also read.
* Repository context: the original case study, addendum, reference index and
  memory were consulted. No regulatory, private-data or live Azure conclusion
  is needed for these local code corrections.
* Decisions and dependencies: G1-G3, FR1-FR4, AC1-AC5, the test ownership and
  validation lock, and P01-T01 through P03-T02 with their stated dependencies.
  The existing branch and untracked candidate inputs were inspected read-only.
* Boundary: assess implementation credibility, regression sensitivity, focused
  validation and local commit handoff. No production edits, test execution,
  external research, Git history changes, remote writes or additional agents.
  The requested existing /tmp/mv tools are distinguished from forbidden scratch
  writes. Publication and final exact-head gates remain coordinator work.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| G1, FR1-FR2, AC1, C1/C4, P01-T01/T02 | Covered | Shared synchronous finally, cancellation propagation, all-task observation, event-synchronized real-runner tests and cancellation-resistant shutdown coverage are explicitly planned. |
| G2, FR3, AC2, C2, P01-T01/T02 | Covered | Budget validation precedes supplied-control checks and SDK factories; rate type/finite/positive/budget cases, deadline nonfinite/budget cases and stricter valid controls are included. |
| G3, FR4, AC3, C3/C5, P01-T01/T02 | Covered | Fake-clock 25/50/100 per-second spacing, short model-time waits, elapsed paused targets and shortened deadline polls directly discriminate the faulty fixed 50 ms sleep. |
| Test ownership and validation lock | Covered | Existing two-file ownership, no removals, at most six added methods and no generated targets are compatible with parameterized coverage. |
| AC4, P02-T02 | Partial | Ruff, formatting, strict mypy and relevant unittest selectors are scoped appropriately, but fixture scratch storage is not constrained; PC-001. |
| P02-T01 | Covered | Owning guides explain changed contracts; authorized rubric restoration is restricted to the named main copy. |
| AC5, P03-T01 | Partial | One independent Review is planned, but blanket deferral of new findings can bypass current-candidate correctness gates; PC-002. |
| P03-T02 and handoff | Covered | Privacy-safe local identity, selective staging, Conventional Commit, Copilot trailer, persistence and no push are explicit. Complete publication evidence is not claimed. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0, High 0, Medium 2, Low 0.
* Rationale: the technical repair and focused regressions are credible. Two
  execution details need direct correction so tests respect the filesystem
  boundary and the independent Review can actually prevent an incorrect local
  candidate from being handed off as complete.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Constrain fixture scratch storage before focused tests

* Related IDs: AC4, test ownership and validation lock, P01-T01, P02-T02.
* Evidence: src/api/tests/test_iot_stream.py:63-66 constructs
  tempfile.TemporaryDirectory() without a directory argument. The candidate's
  test environment specifies PYTHONPATH but no scratch-directory override.
  P02-T02 requests the commands as locked in the plan. The execution
  instructions prohibit /tmp and /var/tmp file operations.
* Concern: the existing SQLite receiver fixtures can select the system temporary
  directory when TMPDIR is unset. Using the requested pre-existing /tmp/mv
  executables does not redirect fixture writes into the workspace.
* Impact: otherwise relevant red/green tests can violate the filesystem boundary
  or be blocked by it, leaving the validation promise unfulfilled.
* Smallest useful change: add a workspace-relative scratch setup and export an
  absolute, project-contained TMPDIR before every red/green unittest process;
  assert Python tempfile.gettempdir() resolves there before running tests.
  Retain the requested tool executables and selectors. Keep scratch untracked
  and clean up only newly created, task-owned scratch inputs after use.
* Action owner: planning parent, implemented by the validation owner.
* Exact resolving evidence: the plan validation lock and phase details include
  the workspace-local scratch environment for P01-T01 and P02-T02; subsequent
  changes evidence records the resolved tempfile directory and successful
  relevant test commands, with no scratch inputs staged.
* Decision route: direct planner correction. No divergent user decision and no
  request to replace /tmp/mv tooling.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Do not defer blocking findings about the current fixes

* Related IDs: AC1-AC5, P03-T01, P03-T02.
* Evidence: .copilot-tracking/details/2026-10-29/iot-review-508-phase-details.md,
  P03-T01 says, "Preserve original findings and route any new ones to later
  work, not repeated Review." P03-T02 then commits after recording disposition;
  neither task distinguishes unrelated follow-up from a blocking defect in
  this candidate.
* Concern: as written, even a Review finding that cleanup still leaks tasks,
  invalid supplied controls reach a factory, or paused pacing spins can be
  deferred while this task is declared complete. Exactly one Review does not
  require accepting its blocking findings.
* Impact: the only independent post-implementation assessment can lose its
  gating effect on the requested fixes.
* Smallest useful change: restrict deferral to unrelated or explicitly
  nonblocking residual work. Require in-scope blocking findings to be resolved
  with recorded evidence and relevant checks rerun before successful handoff,
  or record the task as blocked/not accepted. Preserve the original Review
  and do not schedule a second Review or critique. Leave publication and
  independent exact-head assessment with the coordinator.
* Action owner: planning parent, with implementation and Review disposition
  recorded by the local delivery owner.
* Exact resolving evidence: P03-T01/T02 and AC5 state this acceptance condition;
  the eventual unchanged original Review plus changes/disposition evidence
  maps every blocking in-scope finding to its correction and relevant passing
  validation, or explicitly records a blocked/not-accepted handoff.
* Decision route: direct planner correction. The confirmed request already
  requires working fixes; no significant or divergent user decision is needed.

## Strengths and Residual Risk

* The fix stays shared rather than duplicating runner cleanup logic. Observing
  every owned task, including completed failures, is explicitly required.
* Regression synchronization uses shutdown-entry events rather than guessed
  sleeps, and the plan requires releasing test-owned tasks on assertion failure.
* The plan rejects awaiting cancellation-resistant shutdown completion and
  correctly limits its guarantee to bounded runner return, cancellation request
  and eventual exception observation. This is an explicitly accepted residual
  SDK limitation, not an unowned finding.
* Supplied-control validation remains at the publisher entry boundary rather
  than expanding Pacer-wide validation or changing global send admission.
* Existing pause/stop/deadline and SQL/consent behavior remain protected by the
  focused module selection. High-rate claims are local deterministic timing
  evidence, not live transport throughput or SLA acceptance.

## Questions or Blocking Evidence Gaps

* None requiring user input. Supplied source and tests support the decision.

## Limitations

* This is a plan critique, not an implementation review or validation receipt.
  No tests or static checks were executed, and no new runtime behavior is
  claimed verified.
* The research's local probes were assessed as supplied evidence, not rerun.
* No full API suite, Azure action, dependency change, push or publication gate
  was performed. Unrelated repository conditions were not audited.
* Plan, phase details, research and other existing records remain unchanged;
  this critique is the only written artifact.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: planning parent.
* Smallest next action: directly revise the Review acceptance rule and the
  focused-test scratch environment, then record both finding dispositions
  before implementation.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/iot-review-508-plan.md](.copilot-tracking/plans/2026-10-29/iot-review-508-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/iot-review-508-phase-details.md](.copilot-tracking/details/2026-10-29/iot-review-508-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-29/iot-review-508-research.md](.copilot-tracking/research/2026-10-29/iot-review-508-research.md) | Supplied focused research |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-review-508-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-review-508-plan-critique.md) | This single independent critique |

## Next Steps

The active planning parent should dispose PC-001 and PC-002 directly, finalize
the plan without another critique, and continue the authorized local RPI loop.
No user action is required. Publication and final exact-head gates remain the
coordinator's responsibility.
