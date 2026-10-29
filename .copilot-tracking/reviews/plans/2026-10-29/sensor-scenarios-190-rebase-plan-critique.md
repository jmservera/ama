---
title: Sensor scenarios PR 505 rebase final-candidate plan critique
description: Independent bounded assessment of the rebase plan and execution boundaries
ms.date: 2026-10-29
---

## Metadata

* Task ID: 505 / sensor-scenarios-190-rebase.
* Parent task: 190 / sensor-scenarios-190.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/sensor-scenarios-190-rebase-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/sensor-scenarios-190-rebase-phase-details.md.
* Critique execution status: Complete.
* Assessment count: Exactly one independent final-candidate critique.
* Source writes: None. This critique is the only written artifact.

## Inputs and Criterion Boundary

* Caller requirements: Continue the explicitly selected automatic Follow-up
  through the ordered RPI loop; rebase draft PR 505's existing branch onto
  current fetched main; preserve both intentions; commit locally without push
  or any remote writes.
* Candidate identity observed by read-only Git inspection:
  feat/sensor-scenarios-190 at
  2fdf08bba5f3c30969645191aafee8bf8e087036; origin/main at
  b0364e4b326936715d69ab1d75040c4528282af7. The two branch-only commits
  match the research. Intake status contains only the new untracked dated
  research, plan, details and state directories.
* Supplied evidence: The plan, details,
  .copilot-tracking/research/2026-10-29/sensor-scenarios-190-rebase-research.md
  and .copilot-tracking/rpi-sessions/2026-10-29/sensor-scenarios-190-rebase-state.json.
* Scoped supporting evidence: src/README.md; core/API pyproject files;
  src/core/src/zava_forward/core/synthetic/scenario_manifest.py;
  src/core/tests/test_sensor_scenarios.py; core/API dependency-rule tests;
  src/api/tests/test_sensor_ingestion.py; tools/rpi-checks.py, including its
  incoming origin/main version; Git differences for the relevant incoming
  model, manifest and rubric paths; original parent state.
* Repository context: docs/case_study_48_original.md, the opening project
  framing in docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory was treated as context, not evidence.
* Decision boundary: Assess whether the proposed rebase, setup, bounded
  checks, evidence retention and local handoff are credible. Do not demand
  new live features, consumer adoption, parent closure, hosted execution,
  another critique, or another original-task Review.
* Budget: No removals; no new test modules; at most two regression methods,
  only after reproducing a rebase-coupled defect.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Explicit automatic Follow-up; research Q1-Q3 | Covered | Current and original state distinguish the selected continuation from the original completed task. |
| P01-T01 ancestry and conflict policy | Covered | Exact base and HEAD match inspection; details correctly explain rebase side inversion and explicit origin/main ownership. |
| P01-T01 preservation of both intentions | Covered | Independent documentation entries are retained; upstream indoor/backfill behavior is preserved rather than restored to branch-era behavior. |
| Main-owned rubric and scenario manifest | Covered | Plan permits only necessary stale source-hash refresh, requires all four exact-byte bindings and test_scenario_manifest. |
| P02-T01 setup and project checks | Partial | Missing import is recorded and editable installs/project-config checks are planned, but the specified write destinations are not executable within the current boundary; PC-001. |
| P02-T01 actual regression scope | Covered | Listed modules exist. Existing scenario tests already assert eleven cases, fifteen passing checks, truth independence and fixed-truth sensitivity. No speculative new regression work is required. |
| Source/test ownership and budget | Covered | Canonical module remains under src/core/src; tests remain outside packages; no legacy application path or new-module allowance is introduced. |
| API sibling fixtures and selector isolation | Covered | test_sensor_ingestion imports core test_sensor_consumer and its fixture; project/sibling source and test paths are explicitly required. Core/API dependency modules need their respective project invocation, not one ambiguous combined import. |
| Shared-resource safeguards | Covered, execution constrained | Full API discovery is excluded; a probe is not treated as a reservation and the full runner holds its own lock. That lock's temporary path participates in PC-001. |
| P03-T01 evidence and commit boundary | Covered | Original evidence remains byte-preserved; new Review precedes candidate/evidence commit; gate follows commit. Privacy-safe identity, Conventional Commit, required trailer and Refs-only references are explicit. |
| Local gate versus hosted/human acceptance | Covered | Failed prerequisites stay blockers; coordinator owns later exact-head publication work; no push, cloud fallback, fabricated receipt or protection change is authorized. |
| Original 2026-10-27 outcomes | Covered | Original adverse critique/Review and RV-001 through RV-004 remain unchanged; downstream/live acceptance is not silently satisfied. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 0 Medium, 0 Low.
* Rationale: The rebase and regression design are proportionate and otherwise
  credible. One actionable execution-boundary conflict must be represented
  honestly before implementation can claim the proposed validation is
  runnable. This finding does not regrade or resolve historical RV-001.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Separate permitted work from currently blocked temporary-path validation

* Related IDs: P02-T01, P03-T01, research Q3, Non-Functional Requirements,
  Acceptance Criteria, Unresolved Decisions or Blockers.
* Evidence: The plan states that there are no implementation blockers and
  proposes editable setup and checks in /tmp/mv. The details prescribe
  "/tmp external logs". The full runner in tools/rpi-checks.py, including
  incoming main, opens /tmp/ama-rpi-heavy.lock with create/read-write flags.
  Selected tests also use tempfile.TemporaryDirectory, for example
  src/core/tests/test_dependency_rule.py and
  src/api/tests/test_dependency_rule.py. The current execution boundary does
  not permit temporary-directory file operations. No such operation was
  attempted during this critique.
* Concern: The plan treats the caller-selected validation locations as
  unconditionally executable. Recording only a missing package or tool as
  the possible blocker omits the already known write-location constraint.
  Executable location alone also does not isolate pip, cache and test scratch
  writes.
* Impact: Implementation could violate the current execution boundary or
  report validation readiness that it cannot establish. A successful lock
  probe would not resolve that separate constraint.
* Smallest useful change: Mark the affected setup/check/gate operations
  blocked under the current execution boundary. Use permitted
  workspace-relative destinations for any logs, caches or scratch that can
  legitimately be configured, without substituting another environment for
  the requested /tmp/mv checks or substituting another shared lock. Keep
  required checks outstanding when their exact requested execution cannot
  be performed. Record this limitation in the dated changes and handoff;
  do not change source or runner behavior merely to evade it. Continue
  independently permitted rebase/reconciliation work only with an honest
  partial-validation status.
* Action owner: Planning parent, with implementation recording actual
  commands and blocked outcomes.
* Exact resolving evidence: Revised plan/details explicitly classify the
  affected validation as blocked rather than declaring unconditional
  readiness; dated changes identify any permitted scratch configuration,
  commands actually run, and checks not run. If a later permitted execution
  context performs the exact requested checks, retain its command/exit-code
  evidence separately. A full-gate success still requires its genuine
  exact-candidate receipt and verification; a blocker record is not a pass.
* Decision route: Direct planner correction. The user already selected the
  requested environment and no-push scope; do not ask for a different product
  acceptance criterion or imply that user confirmation can override the
  execution boundary. Preserve the original RV-001 and its disposition.

## Strengths and Residual Risk

* Conflict resolution is explicit about upstream ownership and rebase side
  semantics, reducing the risk of accidentally choosing the old rubric,
  manifest or model.
* Existing scenario assertions provide substantive regression coverage.
  The plan correctly avoids adding tests merely to consume the two-method
  allowance or weakening expected results without a reproduced defect.
* Source-hash validation is correctly distinct from application, resident,
  consumer and human acceptance.
* No full API discovery is required by this bounded task. Retaining the
  existing full runner's internal serialization avoids the probe/reservation
  race; no wrapper that holds the same lock while invoking the runner is
  needed.
* Review, commit and complete-gate sequencing is credible for a local
  candidate. Later publication still needs current-base receipt verification
  and independent exact-head assessment; the plan assigns that handoff to
  the coordinator rather than claiming the precommit Review proves it.
* Hosted checks cannot assess an unpushed rebased HEAD. This limitation,
  original adverse outcomes and unmet consumer/live/parent acceptance are
  explicitly retained, not new acceptance work for this rebase.

## Questions or Blocking Evidence Gaps

* No unresolved user product or conflict-policy choice was identified.
* PC-001 is a known execution blocker, not a request for open-ended research.
  The planning parent can correct readiness and handoff claims directly.

## Limitations

* This is a plan critique, not an implementation Review or a test execution.
  No rebase, pip installation, linter, type checker, unittest, lock probe or
  complete gate was run.
* Read-only Git checks establish the supplied local branch/base identity;
  no new fetch or remote metadata refresh was performed.
* Incoming source/configuration and scoped test evidence support the
  planning assessment but do not prove the future merged candidate passes.
* Historical critique and Review records were not edited or re-adjudicated.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Dispose PC-001 directly in the plan/details and
  retain blocked validation explicitly while continuing eligible work.
* User response required: No.
* Stop: This completes the single requested final-candidate critique. Do
  not commission another critique for this boundary.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/sensor-scenarios-190-rebase-plan.md](.copilot-tracking/plans/2026-10-29/sensor-scenarios-190-rebase-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-29/sensor-scenarios-190-rebase-phase-details.md](.copilot-tracking/details/2026-10-29/sensor-scenarios-190-rebase-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-29/sensor-scenarios-190-rebase-research.md](.copilot-tracking/research/2026-10-29/sensor-scenarios-190-rebase-research.md) | Supplied focused evidence |
| [.copilot-tracking/rpi-sessions/2026-10-29/sensor-scenarios-190-rebase-state.json](.copilot-tracking/rpi-sessions/2026-10-29/sensor-scenarios-190-rebase-state.json) | Active automatic parent state |
| [.copilot-tracking/reviews/plans/2026-10-29/sensor-scenarios-190-rebase-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/sensor-scenarios-190-rebase-plan-critique.md) | This single independent critique |

## Next Steps

The active planning parent disposes the complete finding set once, records the
direct correction and continues only eligible ordered RPI work. No user action
or second critique is required. This reviewer stops here.
