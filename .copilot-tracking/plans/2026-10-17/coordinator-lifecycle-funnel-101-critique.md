---
title: Coordinator lifecycle funnel issue101 plan critique
description: Single final-candidate credibility assessment of the bounded read-only plan
ms.date: 2026-10-17
---

## Metadata

* Task ID: 101 / coordinator-lifecycle-funnel-101.
* Critique date: 2026-10-17.
* Plan: .copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-plan.md.
* Phase details: .copilot-tracking/details/2026-10-17/coordinator-lifecycle-funnel-101-phase-details.md.
* Critique execution status: Complete.
* Execution: exactly one final-candidate assessment; no delegated agents,
  implementation, original Review, or repeat critique.
* Worktree: current issue-101 worktree only; branch
  feat/coordinator-lifecycle-funnel-101.
* Supplied base: ebc8dab87ae9bd6a33380b85e86f38be5ed9f213.

## Inputs and Criterion Boundary

* Caller direction: ordered Research -> Plan with one critique -> Implement ->
  one original Review. Deliver only the critique artifact in this execution.
* Canonical research:
  .copilot-tracking/research/2026-10-17/coordinator-lifecycle-funnel-101-research.md,
  including C1-C10, W1-W4, dependency disposition and accepted evidence limits.
* Canonical plan and phase details are the exact paths in Metadata. Assessed
  FR1-FR7, all non-functional requirements, AC1-AC5, P01-P03 and their tasks,
  candidate/test ownership locks, exclusions, follow-ups and delivery gates.
* Supplied source pointers checked where needed: current case filtering and
  paging in src/core/src/zava_forward/core/store.py; snapshot and SQL paging in
  src/core/src/zava_forward/core/sqlstore.py; stage definitions and capped map
  clustering in src/core/src/zava_forward/core/insights.py; validated event and
  report outputs in src/core/src/zava_forward/core/progress.py; role and field
  controls in src/core/src/zava_forward/core/projection.py and
  src/core/src/zava_forward/core/export_fields.py; policy/stop semantics in
  src/core/src/zava_forward/core/taskqueues.py; existing mapPanel in
  src/api/src/zava_forward/api/web/app.js and GET dispatch in
  src/api/src/zava_forward/api/server.py.
* Requirements cross-check:
  docs/prds/zava-forward-retrofit-programme-demonstrator.md, FR-020, FR-021,
  PR-005, AC-023 and AC-024. Repository-mandated case-study, index and memory
  context was consulted; memory is not evidence.
* Merged dependencies event102/PR394, resident88/PR392 and sensor112/PR393 are
  accepted as supplied base context. No new remote dependency investigation
  was needed or performed.
* Criterion boundary: credibility of the read-only coordinator aggregate,
  heatmap, observed funnel and authorized drillthrough, retaining existing
  map/list behavior outside coordinator mode. This is not an implementation
  review, independent coordinator acceptance, human approval, accessibility
  conformance judgement or permission to alter operational controls.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| User scope; research C1-C10 and dependency decisions | Covered | Actual workbench/event reuse; supplied merged base; no issue117 writer dependency introduced |
| FR1; C2, C3, C5; P01-T01/T02 | Covered | Registered staff, server-first authority, current open own/all scope, shared lock, scalar query validation and direct-module denials |
| FR2; C6; AC1 | Covered | Current stops use active blocker or paused stage; draft priority does not become approved, and unavailable priority is null |
| FR3-FR4; AC2-AC3; P01-T01; P02-T01 | Partial | PC-001: current-stage cohort selection versus observed-stage drill selection needs an explicit invariant |
| FR4-FR5; C4; P01-T01/T02 | Covered | Inclusive UTC and precision validation; invalid/untrusted streams withheld; no fictional initial entry, final exit, exclusion, conversion or accepted whole-home completion |
| FR6; C7-C8; P01-T02; P02-T02 | Partial | PC-002: tiny-fixture validation does not explicitly exercise the changed coordinator cluster branch |
| FR7; C10; P02-T01/T02 | Covered | Native controls, keyboard paths, tables, URL state, stale-request protection, reflow, reduced motion and explicit unavailable states |
| Field minimization; no mutation; AC4 | Covered | Closed aggregate/record outputs and unchanged ledger/cases/sequence checks; no private narratives or source/actor leakage authorized |
| SQL/image/browser evidence; P03-T01/T02 | Covered | Actual local execution before push, loopback task-owned SQL, external refresh, hardened image and cleanup required, not merely CI promises |
| AC5; P03-T03/T04 | Partial | PC-003: adverse original Review disposition is not an explicit pre-push correctness gate |
| Test ownership and candidate lock | Covered | No removal, at most 18 new core and 12 API methods, same canonical modules and no new framework; fixes below fit existing bounds |
| Knowledge-base overlap and non-goals | Covered | Existing synthesis/index/log updates only; preserve prior entries; no memory, Store/writer, orchestrator or document-control expansion |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the bounded architecture and evidence posture are credible. Three
  planner-owned corrections are needed to fix an ambiguous membership contract,
  cover a changed map branch, and prevent unresolved blocking defects from
  passing automatically from the single original Review into delivery.
  None requires a new user decision or broadens the approved product scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Separate current-stage cohort filters from observed-stage drill selection

* Related IDs: FR1, FR3, FR4, FR6, AC2, AC3, P01-T01/T02, P02-T01.
* Evidence: the plan requires existing source filters and metric/stage sets,
  exact observed-stage drillthrough and shared filters. Phase details require
  count links to preserve those filters, but do not distinguish the existing
  current `stage` filter from the stage named by an entry/exit/return metric.
  src/core/src/zava_forward/core/insights.py, matches, interprets `stage` as
  the current case stage. src/core/src/zava_forward/core/progress.py, history,
  exposes distinct event from_stage/to_stage boundaries.
* Concern: the selection contract does not explicitly prevent an observed exit
  link for stage A from applying current `stage=A`. A case now in B can
  legitimately contribute an exit from A. Reusing the current-stage parameter
  for that link would remove the very case counted. This is a planning
  ambiguity, not a claim that unimplemented code already has this defect.
* Impact: aggregate counts and record/map membership can disagree on the
  central observed-stage drillthrough path even while current occupancy tests
  pass.
* Smallest useful change: define current cohort/source-stage selection and
  observed metric-stage selection independently in P01/P02. State that metric
  membership is computed from the authorized source-filtered current cohort,
  then used for both the drillthrough record total and its map population;
  selecting an event stage must not silently replace a current-stage source
  filter. Label the contextual cohort denominator separately from the selected
  metric-member total.
* Action owner: planning parent.
* Exact resolving evidence: revised P01-T01/P02-T01 membership and URL contract,
  plus an assigned assertion within the existing test-method bounds: a case
  currently in B with a valid A-to-B event appears in exit-A records and the
  corresponding map population, with matching total; a separately supplied
  current-stage filter still intersects correctly. Include preservation of
  this distinction in the existing browser drillthrough journey.
* Decision route: direct planner correction. The user's exact-membership
  requirement resolves the intended behavior; no user response is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Exercise clustering through the coordinator population adapter

* Related IDs: FR6, C1, C7, PR-005, AC2, P01-T02, P02-T01/T02.
* Evidence: src/core/src/zava_forward/core/insights.py, map_view, switches
  between points and clusters at MAP_CAP, currently 500; cluster rows carry
  counts rather than case IDs. The existing mapPanel renders these modes
  differently. The plan reuses and parameterizes that panel, but the locked
  fixtures are dataset.DATA with tiny explicit mutations and the stated
  coordinator validations do not explicitly force cluster mode.
* Concern: a small-population point-mode reconciliation can pass without
  exercising clustered counts, cluster navigation or the coordinator query
  retained across map movement. Existing legacy map regressions do not alone
  prove the new coordinator adapter shares the correct metric/group population
  in its cluster branch.
* Impact: the main map reuse can fail or lose selected membership when the
  mapped population exceeds the point cap, despite all newly planned
  small-fixture count checks passing.
* Smallest useful change: assign a forced-cluster assertion to the existing
  canonical tests and browser journey. Use a supported test-only lower cap
  or a small explicit fixture that reaches the branch, without changing the
  production cap, generating stock, adding a framework or increasing method
  limits. Exercise zoom/navigation with the coordinator selection retained.
* Action owner: planning parent.
* Exact resolving evidence: revised P01-T02/P02-T02 requiring a coordinator
  cluster response whose cluster-count sum equals mapped in-viewport records,
  while the full selected total still includes missing-geocode/out-of-viewport
  records; actual browser journey checks the cluster-to-zoom path and unchanged
  record selection. Production scale/performance acceptance is not implied.
* Decision route: direct planner correction within existing validation scope;
  no user response is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Make adverse original Review findings a delivery gate

* Related IDs: AC4, AC5, P03-T03, P03-T04, ordered RPI requirement.
* Evidence: P03-T03 in the plan says to retain the complete original findings
  and route them separately; phase details say, "Route findings as later work;
  do not run another Review." P03-T04 then prescribes commit/push/PR without
  an explicit unresolved-blocker condition.
* Concern: preserving one original Review is correct, but unconditional
  deferral leaves no stated gate if it identifies unauthorized disclosure,
  invented transitions or broken aggregate/drillthrough reconciliation.
  The plan does not distinguish deferrable residual risk from defects that
  violate the user's mandatory boundaries.
* Impact: the automatic loop could report durable delivery and push a known
  incorrect candidate merely because the required Review ran once.
* Smallest useful change: retain exactly one original Review and its complete
  verdict. Require explicit disposition of each finding before P03-T04:
  directly correct in-scope blocking defects with focused validation and a
  separate resolution record, without rewriting or rerunning the original
  Review; defer only non-blocking findings with rationale. If correction
  requires forbidden paths or a significant new decision, stop the delivery
  gate and report the blocker instead of treating it as completed.
* Action owner: planning parent.
* Exact resolving evidence: P03-T03/T04 and AC5 explicitly condition push and
  completion on no unresolved mandatory-boundary/correctness blocker. The
  planned changes/disposition record must retain original finding IDs,
  remediation or deferral rationale, focused command evidence and any
  remaining limits. No second Review or self-awarded coordinator acceptance
  is authorized by this correction.
* Decision route: direct planner correction. Existing user scope already
  determines what must not ship as a completed solution; no user response
  is required to add the gate.

## Strengths and Residual Risk

* Source selection, SQL refresh and aggregation are explicitly placed inside
  the existing snapshot lock; authorized membership precedes aggregation.
* Draft policy remains draft. Neither staff-wide visibility nor a proposed
  coordinator mode creates a new approval or case-access authority.
* The plan correctly treats timestamp evidence as partial, distinguishes
  distinct-case counts from event occurrences, and rejects additive conversion
  interpretations. Current membership is not an as-of reconstruction.
* Existing event readers return exception and coverage evidence; the candidate
  explicitly requires withholding untrusted transitions rather than treating
  every returned event as a valid count. Last-exit uncertainty is not a reason
  to invent a completion or discard an otherwise valid recorded transition.
* Missing or invalid geocodes remain in records and denominators. Existing
  closed map-field guards remain intact for mapped records.
* Local browser, SQL and image evidence are planned as actual pre-push
  execution. These checks remain unexecuted in this critique.
* Unsupported lifecycle exclusions/closure capture, full historical coverage,
  independent human understanding and WCAG/coordinator acceptance remain
  explicit limits. They are not new blockers requiring prohibited writers.

## Questions or Blocking Evidence Gaps

* No unresolved significant or divergent user choice is needed for this
  critique's findings.
* No decision-critical research gap prevents assessment of the supplied
  candidate. Revise is due to planner-owned contract, coverage and gating gaps,
  not missing authority to expand scope.

## Limitations

* This assessment inspected supplied artifacts and relevant source contracts,
  not an implementation diff. Findings identify readiness gaps, not reproduced
  runtime defects.
* No tests, local browser journey, SQL instance or image validation were run;
  they belong to implementation. No private datasets, external services,
  tiles, paid AI or other worktrees were accessed.
* Web rules were not refreshed and no web/UI conformance review was performed:
  this is plan critique, not the later original Review or a web edit.
* The supplied base/dependency status is context, not an independent remote-head
  attestation.
* Plan, phase details, research and workflow state were not edited. Existing
  untracked planning artifacts were left untouched.

## Recommended Next Action

* Highest-impact finding: PC-003, the original Review delivery gate.
* Action owner: planning parent.
* Smallest next action: incorporate PC-001 through PC-003 directly into the
  existing plan/details and disposition this single complete finding set.
* User response required: No.
* After compatible corrections, the active parent may continue the already
  requested ordered implementation loop; do not commission a second critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/coordinator-lifecycle-funnel-101-research.md](.copilot-tracking/research/2026-10-17/coordinator-lifecycle-funnel-101-research.md) | Canonical research and evidence boundary |
| [.copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-plan.md](.copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-plan.md) | Assessed final-candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-17/coordinator-lifecycle-funnel-101-phase-details.md](.copilot-tracking/details/2026-10-17/coordinator-lifecycle-funnel-101-phase-details.md) | Assessed phase details, unchanged |
| [.copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-critique.md](.copilot-tracking/plans/2026-10-17/coordinator-lifecycle-funnel-101-critique.md) | Single complete critique and actionable finding set |

## Next Steps

The active planning parent corrects and dispositions PC-001 through PC-003,
finalizes planning without another critique, then continues the authorized RPI
loop when its gates permit. No user action is required. This worker stops here;
no implementation, original Review or independent coordinator acceptance is
performed.
