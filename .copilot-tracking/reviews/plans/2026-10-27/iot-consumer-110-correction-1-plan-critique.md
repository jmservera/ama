---
title: IoT consumer correction 1 final-candidate plan critique
description: One independent bounded assessment of correction phases P04-P07
ms.date: 2026-10-27
---

## Metadata

* Task ID: 110-correction-1; parent: 110.
* Critique date: 2026-10-27.
* Repository: jmservera/ama; branch: feat/iot-consumer-110.
* Plan: .copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md, correction section only.
* Phase details: .copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md, correction section only.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Caller requirements: correct RV-001, RV-003 and RV-002 in that order; focused
  local regressions, existing component suites, configured lint/format and mypy;
  same-branch publication to existing draft PR #508. No network, Azure, secrets,
  private data, uv, optional heavy gate or full --all gate.
* Research considered: correction C7-C10/W6 and its directly related correction
  rationale in .copilot-tracking/research/2026-10-27/iot-consumer-110-research.md.
* Original adverse evidence: RV-001/RV-002/RV-003 and their supporting scope in
  .copilot-tracking/reviews/logs/2026-10-27/iot-consumer-110-review.md.
* Exact source considered: src/core/src/zava_forward/core/synthetic/sensor_stream.py,
  src/core/src/zava_forward/core/synthetic/sensor_stock.py and
  src/api/src/zava_forward/api/iot_stream.py.
* Existing regression ownership considered: src/core/tests/test_sensor_stream.py
  and src/api/tests/test_iot_stream.py.
* Decisions and dependencies: P04 precedes P05, which precedes P06; P07 depends
  on all three. Two existing test modules, zero test removals and no more than
  12 additional methods are locked. Source, direct documentation and required
  RPI evidence are in scope; dependency, lock and generated targets are not.
* Assessment boundary: credibility of the supplied correction plan, not
  implementation acceptance, live operational readiness, hosted approval or
  merge. Explicit current publication directions are settled inputs, not an
  unresolved decision or a reason to revive historical publication refusal.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-001 / C7 / P04-T01 | Covered | Separates model pacing from actual admission; one global limiter, reservation inside the send coroutine after connect/message/truth and immediately adjacent to the SDK await |
| RV-001 control preservation | Covered | Burst/speed, pause/stop, cancellation and cleanup-reserved absolute deadline remain explicit; fake SDK timestamps, delayed connect/truth and multiple devices prevent a Pacer-return-only proof |
| RV-003 / C8 / P05-T01 | Covered | Optional ownership initialized before construction; constructors and receive/wait task creation share one error/cleanup scope; only successfully created resources/tasks are closed or observed |
| RV-003 error contract | Covered | Preserves cancellation and StreamError, fixes unexpected setup/receive failures to IOT_RECEIVE_FAILED, and requires explicit IOT_CLEANUP_FAILED; constructor, synchronous startup and close failures have regressions |
| RV-002 / C9 / P06-T01 | Covered | Shared canonical-validation helper reuses select normalization and selected-copy digest, retains original register digest separately, and records selected IDs/count and granted count |
| RV-002 frame consistency | Covered | Generation uses the exact validated local copy; Frame carries selected provenance outside telemetry and publisher copies it; subset, fabric/consent mutation, old/new frames, invalid input and normalization/order tests are specified |
| C10 / bounded test ownership | Covered | The two existing modules already own replay/pacing and publisher/receiver lifecycle contracts; subtests can cover the named variants within 12 new methods without removals or another module |
| P07-T01 local validation | Covered | Core sensor/backfill selectors, full API discovery with existing test-helper paths, both configured Ruff/format and mypy are explicit; declared tools use pip only after the reported missing-dependency probe |
| P07-T01 evidence and Review | Covered | Existing dated evidence is updated, original adverse Review preserved, correction addendum receives one independent Review and findings route forward without a second Review |
| W6 / same-branch publication | Covered | Existing draft PR #508 is reused with non-force push, required commit trailer and Refs; no issue closure, merge or live acceptance claim |
| Dependencies and exclusions | Covered | Ordered phases preserve owner priority; credential lifecycle, actual Hub/SQL/model seam, operational headroom and OD-43 remain deferred |

## Verdict

* Verdict: Pass.
* Rationale: the correction plan directly addresses all three reproduced causes,
  including the scheduling boundary that would invalidate an outside-coroutine
  rate reservation and the mutable-input boundary that would invalidate a
  descriptor-only provenance fix. Lifecycle ownership extends through partial
  construction and startup. Acceptance evidence is appropriately local and
  bounded, and the implementation order and publication destination match
  current user direction.

## Findings

No actionable PC-xxx findings. Severity counts: Critical 0, High 0, Medium 0,
Low 0. No direct planner correction or significant/divergent user decision is
required.

## Strengths and Residual Risk

* Assertions target actual fake SDK send entry rather than elapsed reservation
  time. Merely moving a wait before the existing _bounded call would not satisfy
  the same-coroutine adjacency requirement already stated in P04.
* P05 explicitly includes synchronous receive startup, not only failures after
  the receive task starts. Cleanup must cover only returned resources and
  created tasks while meeting the stated fixed-error and cancellation contract.
* P06 binds frames to the snapshot actually used for generation rather than
  recomputing provenance from subsequently mutated selection rows. The digest
  remains separate from observation bytes and historical reading identities.
* These are implementation acceptance obligations, not additional findings.
  Their presence in the plan does not establish that the forthcoming code
  satisfies them.
* Accepted residual boundaries remain actual SDK/cloud behavior, live SQL and
  restart evidence, credential operations, cost/headroom verification and human
  governance. Local tests do not discharge those deferred criteria.

## Questions or Blocking Evidence Gaps

None for this bounded plan assessment. W6 is treated as supplied research
evidence; no remote PR state was independently queried.

## Limitations

* No tests, lint, type checks, network calls or live probes were executed.
* Only correction plan/details sections, supplied correction research, original
  findings and directly relevant source/tests were assessed. Historical plan
  sections were not reassessed or silently reapproved.
* Existing dirty plan/details/research inputs and the untracked correction
  state were left unchanged. This critique is the sole written artifact.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent, then parent-owned implementer.
* Smallest next action: record this Pass in the correction disposition, finalize
  planning and implement P04 before P05 and P06, retaining the locked scope.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md](.copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md) | Correction requirements, scope and ordered phases |
| [.copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md](.copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md) | Correction implementation and validation obligations |
| [.copilot-tracking/research/2026-10-27/iot-consumer-110-research.md](.copilot-tracking/research/2026-10-27/iot-consumer-110-research.md) | Correction C7-C10/W6 evidence |
| [.copilot-tracking/reviews/logs/2026-10-27/iot-consumer-110-review.md](.copilot-tracking/reviews/logs/2026-10-27/iot-consumer-110-review.md) | Preserved original adverse findings |
| [.copilot-tracking/reviews/plans/2026-10-27/iot-consumer-110-correction-1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/iot-consumer-110-correction-1-plan-critique.md) | This single independent final-candidate critique |

## Next Steps

The active planning parent may finalize and continue the authorized ordered RPI
loop without another plan critique or user response. This assessment stops here;
it does not implement, run validation or publish.
