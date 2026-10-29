---
title: Capacity delayed sibling 401 original plan critique
description: Independent final-candidate critique for issue 523 and PR 528
ms.date: 2026-10-28
---

## Metadata

* Task ID: 523-delayed-401
* Slug: capacity-page-523-delayed-401
* Critique date: 2026-10-28 UTC
* Original verdict: Revise
* Critique execution status: Complete
* Plan: .copilot-tracking/plans/2026-10-28/capacity-page-523-delayed-401-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/capacity-page-523-delayed-401-phase-details.md
* Candidate source HEAD: 2d207b6284930d926324cdfea9282d3e78ce6203
* Branch and PR: fix/capacity-page-523, open PR #528 targeting main
* Assessment count: exactly one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Caller requirements: smallest post-read lifecycle guard; deterministic browser
  completion after an older failed-refresh sibling returns 401 and newer retry
  reads succeed; preserve existing scenarios and once-only real mutation.
* Research: .copilot-tracking/research/2026-10-28/capacity-page-523-delayed-401-research.md,
  C1-C4, including accepted alternatives and residual uncertainty.
* Named source evidence: src/api/src/zava_forward/api/web/ops.js,
  src/api/src/zava_forward/api/web/app.js,
  src/api/checks/capacity_browser_check.py and src/api/README.md.
* Repository context: original case study, relevant addendum context,
  reference index, owner memory and housing-association primer. No new customer
  or regulatory conclusion is needed.
* All plan requirements, acceptance criteria, locked test ownership,
  P01-T01/P01-T02/P02-T01/P02-T02, dependencies and publication decisions were
  assessed. User authorization already permits scoped validation, normal push
  and subsequent exact-thread reply/resolution. No additional authorization is
  requested for those actions.
* This is plan credibility assessment, not implementation acceptance, browser
  execution, full web-guidelines review or independent implementation Review.
  No az, heavy tests, secrets, environment files, private datasets or nested
  agents were used. The complete local gate is barred and is not recommended.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C2; smallest lifecycle guard | Covered | ops.js:176 awaits both reads; app.js:28-37 parses and processes 401 without aborting the route. Checking the captured signal and current session before synchronous rendering addresses this boundary. |
| C3; real mutation and old-sibling/new-retry ordering; P01-T01 | Partial | Planned sequence and fixture are appropriate; completion observable is unspecified, PC-001. |
| Both endpoint orderings reproduce red; P01-T01 | Partial | Plan requires both; details make the second red result conditional, PC-003. |
| Once-only mutation and no replay | Covered | Both POST count and persisted configuration count are required, beyond a mocked mutation response. |
| Existing navigation, draft, recovery, cancellation, expiry and empty scenarios | Covered | Existing harness scenarios are retained; a full focused capacity browser run remains required for green. |
| C4; nonblocking admission and bounded busy retry; P01-T02 | Partial | Admission sequencing is sound, but selected filesystem paths are prohibited in this execution environment, PC-002. |
| Focused units, syntax, Ruff/format and mypy; P01-T02 | Covered | Named checks and shared fixture paths are identified; execution remains prospective. |
| Independent original Review; P02-T01 | Covered | Fresh Review includes synchronization and red/green evidence; no repeat Review is proposed. |
| Publication and exact thread; P02-T02 | Covered with dependency | Normal push, privacy-safe identity, preserved historical evidence and verified thread resolution are explicit; scoped evidence must actually exist first. |
| Full gate and live acceptance | Covered | Explicitly unavailable, not represented by historical receipts or scoped checks. |

## Verdict

* Verdict: Revise.
* Severity summary: 2 High, 1 Medium; no Critical or Low findings.
* The production design is credible. The plan needs a named completion barrier,
  executable validation prerequisites consistent with filesystem restrictions,
  and mandatory red evidence for both promised orderings.
* These are direct planning-parent corrections. No significant or divergent
  user decision is identified by the supplied boundary.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Name a completion barrier tied to the retry continuation

* Related IDs: C1-C3, P01-T01, deterministic completion requirement,
  plan lines 56-58 and 75-78.
* Evidence: phase-details lines 20-24 say to wait for the handler to settle but
  do not identify how. In ops.js:148-164, go awaits capacityView and clears the
  clicked button's disabled/aria-busy state in finally. app.js:28-37 awaits body
  parsing after fetch. The current harness uses response waits in other
  scenarios, but those are not this continuation's completion evidence.
* Concern: The sign-in assertions are already true before retry reads finish.
  Response headers, route.fulfill returning, or immediate successful assertions
  can therefore pass while the stale-render continuation is still pending.
  The plan states the right invariant but leaves its decisive proof unspecified.
* Impact: A regression can falsely pass without exercising the guard's effect.
* Smallest useful change: Specify a retained ElementHandle for the exact
  clicked retry button. While both retry GETs are held, verify that this element
  is disabled and aria-busy is true. After observing the old sibling's sign-in
  transition and releasing both successful retry bodies, wait on that same
  retained element until disabled is false and aria-busy is absent, even though
  login detached it. Only then assert sign-in heading/alert, focus, no capacity
  heading or retry controls, POST count and persisted count. This observes the
  existing go finally after its awaited capacityView, without a production hook.
  An equivalently demonstrated continuation-specific barrier is acceptable.
* Action owner: Planning parent; implementer supplies the promised evidence.
* Exact resolving evidence: P01-T01 names the observable and its busy-to-settled
  transition; the eventual red/green record shows the barrier completes before
  final assertions for both orderings. Network response arrival alone is
  explicitly insufficient.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Validation paths conflict with the execution restrictions

* Related IDs: C4, P01-T02, P02-T02, scoped browser validation prerequisite.
* Evidence: phase-details lines 34-37 prescribe an interpreter under a
  prohibited temporary root and a shared lock there. The execution instructions
  prohibit file operations under temporary directories and require created
  files to remain project-relative. src/api/checks/capacity_browser_check.py:662
  opens that hardcoded shared lock, and line 673 uses TemporaryDirectory without
  a project-relative directory. Chromium also needs its generated runtime
  files accounted for.
* Concern: The planned validation command cannot be executed as written under
  the current restrictions. Setting TMPDIR alone does not change the hardcoded
  lock. Replacing it with an unrelated per-worktree lock would also lose shared
  heavy-work exclusion.
* Impact: Required browser evidence is blocked; scoped push/thread resolution
  cannot truthfully claim the planned passing validation without correction.
* Smallest useful change: Reconcile P01-T02 with project-relative tooling and
  runtime storage, including fixture/browser generated files, while preserving
  one shared nonblocking admission mechanism and the existing 60-second,
  40-minute busy-only retry contract. Make any necessary harness-support change
  an explicit narrow exception to the one-scenario-only boundary. If no
  compliant shared-admission/runtime arrangement is available, mark browser
  validation and its dependent publication step Blocked rather than executing
  prohibited paths, silently bypassing the lock or claiming green.
* Action owner: Planning parent.
* Exact resolving evidence: Revised details identify compliant interpreter,
  generated-file and shared-admission paths, or explicitly record the blocked
  dependency. Any executable route must explain how all participating heavy
  runs retain the same exclusion boundary; merely changing the lock name or
  setting TMPDIR is not resolving evidence.
* Decision route: Direct planner correction or explicit execution blocker;
  no new user decision is needed to honor an existing prohibition.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Make both unguarded red orderings mandatory

* Related IDs: P01-T01; plan acceptance criterion at lines 62-63.
* Evidence: plan requires both packages-first and workorders-first failures to
  reproduce stale rendering without the fix. Phase-details lines 25-26 instead
  say to record both stale-render failures "if practical."
* Concern: A fail-fast first red run could leave the second ordering unproved
  while the phase is treated as complete.
* Impact: Reported acceptance would exceed the available unguarded evidence.
* Smallest useful change: Remove the conditional wording. Require two separately
  recorded unguarded runs or a red-only evidence collector that records each
  expected stale-render assertion and continues to the other ordering. Keep the
  committed green assertions strict and preserve unexpected-error detection.
  Do not auto-retry actual failures under the heavy-lock busy retry policy.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 unconditionally requires both red outcomes;
  eventual original evidence identifies the failed endpoint, completed retry
  barrier and stale-render assertion for each, followed by both green outcomes.
* Decision route: Direct planner correction; no user response required.

## Strengths and Residual Risk

* The two-line guard is correctly located before constructing capacity content.
  Checking both captured abort state and current session preserves navigation
  cancellation and handles the distinct non-aborting 401 path.
* Real persisted mutation, two endpoint permutations, actual successful read
  payloads and preserved error collectors make the proposed regression valuable.
* No auth redesign, request-generation framework or production test hook is
  justified by this trace.
* Scoped test results cannot establish the complete gate, hosted approval,
  deployed acceptance or issue closure. Those limits are already explicit.

## Questions or Blocking Evidence Gaps

* No user question is required. PC-002 is an execution-prerequisite conflict,
  not missing evidence about the production race.
* Browser and scoped-check results are prospective. This critique does not
  invent outcomes or change historical RV-004/005/006 dispositions.

## Limitations

* Assessment used the supplied plan, sibling evidence and named source trace.
  No open-ended research, test execution or source changes were performed.
* The plan, details and research were already untracked inputs at critique
  start; they were not altered, staged or committed by this critique.
* This dated original verdict must remain preserved after direct corrections;
  another critique is neither required nor requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Name the retry-button finally barrier in P01-T01,
  require both red orderings, and reconcile or block P01-T02's filesystem
  prerequisites before execution.
* User response required: No.

## Artifacts

| Path | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-28/capacity-page-523-delayed-401-plan.md | Assessed plan; unchanged |
| .copilot-tracking/details/2026-10-28/capacity-page-523-delayed-401-phase-details.md | Assessed phase details; unchanged |
| .copilot-tracking/research/2026-10-28/capacity-page-523-delayed-401-research.md | Supplied C1-C4 research; unchanged |
| .copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-delayed-401-plan-critique.md | This dated original critique |

## Next Steps

The active planning parent corrects PC-001 through PC-003 directly and records
their resolving evidence without another critique. Continue the authorized RPI
only when scoped validation prerequisites are executable; retain a blocked
publication dependency otherwise. Do not invoke the complete local gate.
No user action is required.
