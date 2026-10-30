---
title: Employee expanded-map filters final-candidate plan critique
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 551
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-map-filters-551-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/employee-map-filters-551-phase-details.md
* Critique execution status: Complete
* Assessment: exactly one independent final-candidate critique; Refs #551 only.

## Inputs and Criterion Boundary

* Caller requirements: research, plan, implement, review in order; local only;
  no push, Azure operations, deployment, live sign-in, credential files or
  secrets. The execution instructions also prohibit all /tmp and /var/tmp
  file operations and require newly created files to be workspace-relative.
* Inputs: the named plan, phase details and
  .copilot-tracking/research/2026-10-30/employee-map-filters-551-research.md,
  including C1-C6/W1 and the four issue acceptance criteria as supplied.
* Source checks: src/api/checks/map_fullscreen_browser_check.py,
  src/api/src/zava_forward/api/web/app.js, src/api/checks/design_system_browser_check.py,
  src/README.md and tools/rpi-checks.py, limited to the planned assertion
  strategy and safe validation/gate behavior.
* Baseline: HEAD is 721ba973; read-only ancestry inspection confirms
  4a9d5cce is its ancestor. Existing compact controls are not missing work.
* Decisions: preserve runtime, existing tests and all inherited browser
  checks; add no test module and only one bounded assertion block inside
  check_expanded_filters' per-flag loop plus one result-row extension.
* Boundary: assess implementation credibility, locked test scope, acceptance
  traceability and safe validation. Do not execute tests, implement changes,
  refresh external research, establish human accessibility acceptance or
  authorize publication. Existing parent-owned untracked artifacts remain
  untouched.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1, C1-C3, C6 | Covered | Delivered baseline and existing original-node, compact-font and geometry assertions justify preserving runtime. |
| AC2, C2, C4, P01-T01 | Covered | Exact API item IDs, native marker summary/link identity and each flag's header/expanded round trip address the identified count-only weakness. |
| AC3, C3-C5, W1 | Covered | Plan preserves Enter/Space, pressed/text state, focus, reflow, enlarged text, reduced motion and axe checks without claiming whole-app conformance. |
| AC4, C4-C5, P01-T01 | Covered | Existing actual-app browser function is the canonical target; source-contract tests remain unchanged. |
| Locked change budget | Covered | One assertion block and result-row extension suffice; marker iteration and header round trips can stay within the existing flag loop. |
| P01-T01 regression dependencies | Covered | Details explicitly preserve support/zero as the final loop state and retain subsequent pending/race tests. |
| P01-T02, safety and full gate | Partial | PC-001: planned tool, lock and output paths conflict with execution constraints; full runner has a hard-coded forbidden lock path. |
| RPI sequence, review and publication boundary | Covered | Research precedes this critique; implementation then independent Review and a post-commit gate are specified. No push or approval bypass is authorized. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 1; Medium 0; Low 0.
* Rationale: the browser-hardening proposal is credible, proportionate and
  within its locked budget. Validation instructions require one direct
  safety correction before execution. This does not justify runtime changes,
  new tooling or weakening the complete-gate requirement.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation paths require forbidden file operations

* Related IDs: P01-T02; Non-Functional Requirements; Dependencies; local-only
  safety boundary and post-commit publication gate.
* Evidence: the plan's P01-T02 specifies existing /tmp/mv tools and
  flock -w 600 /tmp/ama-rpi-heavy.lock. Phase details prepend /tmp/mv/bin,
  request fresh external session output, then instruct an attempt of the
  full runner. tools/rpi-checks.py:2272-2275 hard-codes
  /tmp/ama-rpi-heavy.lock and opens it with O_CREAT and O_RDWR.
  src/README.md:114-116 requires this same shared lock. Current execution
  instructions prohibit /tmp file operations and non-workspace file creation.
* Concern: the targeted heavy command and full runner cannot be executed as
  written within the active safety constraints. Changing TMPDIR or --out
  does not relocate the runner's literal lock. The generic instruction to
  report a blocker after attempting the gate does not prevent the forbidden
  operation itself. A separate workspace lock would not coordinate with
  other users of the required shared lock.
* Impact: following the plan can violate the execution boundary before
  producing useful validation. Conversely, silently substituting a lock,
  dropping the lock, using forbidden output paths or treating targeted
  checks as a complete gate would undermine safety or evidence credibility.
* Smallest useful change: revise P01-T02 and the matching details to perform
  read-only admission checks before any validation command. Remove /tmp/mv
  execution assumptions; identify an already available allowed toolchain or
  record its absence. Use only permitted workspace-relative locations for
  admissible targeted outputs. Explicitly record heavy browser/full-gate
  execution as blocked while the required lock conflicts with the active
  path prohibition; do not invoke those commands to rediscover the known
  conflict. Keep full-gate receipts external as required by repository
  policy, but acknowledge that creating such evidence is not authorized
  here. Preserve the required gate as an unmet publication prerequisite.
  Do not broaden this issue into a runner/lock rewrite or an alternative gate.
* Action owner: planning parent; implementation executor owns recording
  actual admitted checks and blocked checks in the subsequent changes record.
* Exact resolving evidence: both
  .copilot-tracking/plans/2026-10-30/employee-map-filters-551-plan.md and
  .copilot-tracking/details/2026-10-30/employee-map-filters-551-phase-details.md
  explicitly prohibit invoking the known-conflicting heavy commands, contain
  no executable /tmp tool/lock/output instructions, and distinguish permitted
  focused validation from blocked browser/full-gate evidence. Their completion
  conditions must require an honest blocked status rather than a passing
  receipt or AC claim. Later implementation evidence must enumerate commands
  actually run and retain browser-dependent criteria as unverified unless
  admissible execution becomes possible under authorized constraints.
* Decision route: direct planner correction; no new user decision is needed
  to obey the existing prohibition. Removing a validation blocker would need
  separate authorized resolution, not an inferred permission or second critique.

## Strengths and Residual Risk

* The baseline-aware approach avoids duplicating delivered controls and
  introduces no unnecessary runtime synchronization risk.
* Comparing sorted exact home identities defeats equal-count/wrong-home
  regressions. Native marker activation checks rendered behavior rather
  than merely comparing two API-derived arrays.
* Keeping focus assertions before marker interaction and restoring the loop
  flag after header changes protects existing downstream race assumptions.
* The budget is compatible with the intended change; no additional helper,
  test module or test deletion is necessary.
* Automated browser/axe evidence is explicitly not employee usability,
  assistive-technology, live-site or operational acceptance. The plan
  already accepts that limitation. Blocked execution must not be relabeled
  as this accepted residual limitation or as a passing gate.

## Questions or Blocking Evidence Gaps

* No unresolved product decision. Known validation admission conflict is
  captured completely in PC-001; it does not prevent this plan assessment.
* Successful local browser and full-gate evidence remains to be produced by
  subsequent authorized execution, not assumed from the delivered baseline.

## Limitations

* This is one read-only assessment of the supplied final candidate, not an
  implementation Review or a second research pass.
* No application, test suite, browser, gate, Azure command, sign-in or
  credential operation was executed. External W1 retrieval was not refreshed;
  its supplied research record was used only for the existing planning boundary.
* Issue acceptance criteria were assessed from the supplied plan/research,
  not a new remote issue retrieval. No hosted or human acceptance is inferred.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: reconcile plan/details validation instructions with
  the active path restrictions and record known gate blockers before
  handing the unchanged bounded assertion scope to implementation.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/employee-map-filters-551-plan.md](.copilot-tracking/plans/2026-10-30/employee-map-filters-551-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-30/employee-map-filters-551-phase-details.md](.copilot-tracking/details/2026-10-30/employee-map-filters-551-phase-details.md) | Assessed implementation and validation details. |
| [.copilot-tracking/research/2026-10-30/employee-map-filters-551-research.md](.copilot-tracking/research/2026-10-30/employee-map-filters-551-research.md) | Supplied baseline and regression evidence. |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-map-filters-551-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-map-filters-551-plan-critique.md) | This single independent critique. |

## Next Steps

The active planning parent corrects PC-001 directly and finalizes without
another critique. Continue only with safely admitted implementation/checks;
preserve known browser/full-gate blockers and do not publish. No user action
is required and no peer stage is invoked by this critique.
