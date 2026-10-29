<!-- markdownlint-disable-file -->
# RPI Plan Critique: PR #508 nominal replay pacing

## Metadata

* Task ID: pr-508-nominal-pacing
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/iot-nominal-pacing-508-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/iot-nominal-pacing-508-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: fix only fault-independent observation replay pacing on
  continuing PR #508; retain reordered payload timestamps; use required
  nominal_at metadata through every Frame constructor and publisher scheduling.
* Research: .copilot-tracking/research/2026-10-29/iot-nominal-pacing-508-research.md,
  including C1-C5 and the supplied reproduction.
* Source evidence: src/core/src/zava_forward/core/synthetic/sensor_stream.py,
  src/api/src/zava_forward/api/iot_stream.py,
  src/core/tests/test_sensor_stream.py and src/api/tests/test_iot_stream.py.
* Locked test ownership, zero removals, at most two new methods, existing
  canonical targets, and separate semantic/regression coverage are accepted,
  not reopened.
* Supplied pull/rebase and OPEN PR status are accepted context. Read-only
  inspection confirms branch feat/iot-consumer-110; existing untracked planning
  artifacts were left untouched.
* Required scoped validation, origin/main rubric replacement, commit and no-push
  boundaries are assessed as planned obligations, not executed results.
* General repository context documents were consulted for standing instructions,
  not used to expand the source-evidence or acceptance boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Nominal metadata; C1/C4; P01-T01 | Covered | Required datetime is derived from configured origin and nominal slot cadence, copied through original, duplicate and publisher snapshot constructors. |
| Fault-independent spacing; C2/C3; P01-T01 | Covered | Publisher replaces only the scheduling source; original payload row, wire serialization and reference remain independent. |
| Exact suffix regression; C3/C5; P01-T01 | Covered | Actual Pacer, virtual clock, speed 1000, 60-second budget, two sends separated by 28.8 seconds and exact clean-row 2/5 bodies distinguish the reported defect. |
| Semantic coverage; P01-T01 | Covered | Default/custom origin and cadence, explicit faults, duplicates and suffix equivalence are assigned to existing core tests within the locked additions limit. |
| Safety compatibility; P01-T01 | Covered | Burst exception, actual-send admission and existing deadline/cleanup paths remain unchanged; selected API/core modules retain their existing control tests. |
| Validation and documentation; P02-T01 | Covered | Component README updates and exact requested static/module checks are planned without API discovery or cloud activation. |
| Independent Review disposition; P02-T01 | Partial | PC-001: unconditional deferral of any open finding does not distinguish an unresolved defect in this fix from unrelated follow-up. |
| Rubric, commit, publication boundary; P02-T01 | Covered | origin/main rubric copy, privacy-safe identity and trailer, original evidence retention, no push and coordinator-owned publication are explicit. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: the technical approach and regression design are credible. One
  review-disposition instruction permits the task to be closed with an
  unresolved in-scope defect and needs a bounded planner correction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Distinguish blocking in-scope Review findings from deferred follow-up

* Related IDs: P02-T01; acceptance criteria for scoped checks, independent Review
  and completion of the requested timing fix.
* Evidence:
  .copilot-tracking/details/2026-10-29/iot-nominal-pacing-508-phase-details.md:75-78
  requires one Review and then says to "route any open finding to later work"
  before committing. The plan's P02-T01 requires reconciliation and a commit
  without qualifying that blanket deferral.
* Concern: the instruction also covers a Review finding that nominal pacing is
  still wrong, reordered bodies changed, a constructor omitted nominal_at, or
  a requested check failed. Those findings would invalidate this task's own
  acceptance criteria, not merely identify later publication work.
* Impact: implementation could record completion and hand off a known-broken
  timing fix despite correctly withholding publication approval.
* Smallest useful change: qualify P02-T01 in the plan/details so unrelated
  findings may be recorded for later work, but in-scope material findings require
  correction and relevant scoped revalidation before completion. If unresolved,
  preserve a blocked/incomplete handoff even if a checkpoint commit is made.
  Preserve the original Review outcome and the one-Review limit; do not imply
  corrections received a fresh independent Review.
* Action owner: planning parent; implementation parent executes the disposition.
* Exact resolving evidence: revised P02-T01 text in both supplied planning
  artifacts explicitly separates in-scope blocking findings from unrelated
  follow-up. Subsequent changes evidence maps any actual in-scope Review finding
  to its correction and relevant requested check result, or records the remaining
  blocker without marking the task complete.
* Decision route: direct planner correction. No significant or divergent user
  decision is needed; no broader suite, repeated critique/Review, push or change
  to locked test allocation is requested.

## Strengths and Residual Risk

* The defect is correctly traced: nominal slots 3/4 select faulted payload rows
  2/5. Their 24-hour observation delta must not replace the nominal 8-hour delta.
* Initializing virtual time from real monotonic time satisfies the publisher's
  supplied-deadline check without production clock changes. The actual Pacer
  exercises speed scaling; old scheduling reaches its virtual deadline before
  the second send, while nominal scheduling permits it at 28.8 seconds.
* Existing burst, per-device client, rate, cancellation and cleanup tests remain
  available in the selected modules. No source redesign is justified.
* Full publication validation is explicitly outside the caller's scoped checks.
  A successful local result is not full-gate, live-Azure or hosted/human approval.

## Questions or Blocking Evidence Gaps

* None requiring user input. PC-001 is a planner-owned correction.

## Limitations

* No implementation changes, tests, static checks, commit, remote lifecycle
  queries or publication gate were performed during this critique.
* Constructor completeness is assessed within the four permitted source files
  and supplied C4 research, not a fresh repository-wide search.
* README content, tool installation/configuration and rubric bytes were not
  independently inspected within the supplied source boundary.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: qualify Review-finding disposition in P02-T01, record
  this original critique and continue the authorized loop without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/iot-nominal-pacing-508-plan.md](.copilot-tracking/plans/2026-10-29/iot-nominal-pacing-508-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/iot-nominal-pacing-508-phase-details.md](.copilot-tracking/details/2026-10-29/iot-nominal-pacing-508-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-29/iot-nominal-pacing-508-research.md](.copilot-tracking/research/2026-10-29/iot-nominal-pacing-508-research.md) | Supplied bounded research |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-nominal-pacing-508-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-nominal-pacing-508-plan-critique.md) | Original independent critique |

## Next Steps

The active planning parent resolves PC-001 directly, preserves this critique,
then continues implementation and the single independent Review under the
requested scoped validation and commit-only boundary. No user action or repeat
critique is required. Publication remains coordinator-owned.
