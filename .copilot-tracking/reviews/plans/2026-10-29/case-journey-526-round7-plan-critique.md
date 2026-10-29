---
title: Case journey round seven final-candidate plan critique
description: One bounded assessment of mutation outcome preservation and recovery
ms.date: 2026-10-29
---

## Metadata

* Task ID: 526-round7
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/case-journey-526-round7-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/case-journey-526-round7-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: Seventh correction for PR #529, Refs #526, on the
  existing topic; preserve committed/uncertain API outcomes and prevent
  resubmission before authoritative recovery; audit the named sibling paths.
* Research: .copilot-tracking/research/2026-10-29/case-journey-526-round7-research.md,
  including C1-C9, W1-W2 and its stated decisions.
* Supplied source inspected: Relevant handlers in
  src/api/src/zava_forward/api/web/app.js, assistants.js, ops.js and panels.js;
  src/api/tests/test_case_journey.py and test_workspace_scripts.py; existing
  matrix/function locations in src/api/checks/case_journey_browser_check.py
  and assistants_browser_check.py; src/README.md local-gate requirements.
* Project context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory is context, not correctness evidence.
* Decisions and dependencies: Outcome takes precedence over status; explicit
  refusals remain correctable; preserve drafts, approval boundaries, stale
  session isolation and original review evidence. Implementation precedes
  targeted validation and independent Review.
* Acceptance boundary: Both requested unit modules and journey/assistants
  browser checks with pinned axe; no test removals, at most four added unit
  methods and two added browser helpers. Existing matrices are preferred.
* Execution boundary: This critique writes only its designated artifact. No
  implementation, tests, nested agents, Azure/az, secrets/.env access, push,
  PR changes or thread mutations were performed. Publication remains blocked
  on the separate complete gate; scoped checks cannot substitute for it.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C4; P01-T01 outcome precedence | Covered | Shared classifier, preserved status/reasons/outcome, and explicit refusal exception are specified. |
| C2; P01-T01 recovery barrier | Partial | Session and fieldless guards are included, but recovery-read ordering is unspecified; PC-001. |
| C3-C4/C7; P01-T01 sibling recovery | Partial | Guard intent is stated, but resource-specific recovery evidence is not defined; PC-001. |
| C5; P01-T01 upload dispatch | Partial | Moving dispatch inside refresh is necessary, but local preparation failures need different treatment; PC-002. |
| C6; P01-T01 raw resident/challenge forms | Covered | Structured uncertain parity and existing transport handling are expressly retained. Regression assignment remains incomplete under PC-003. |
| Research synthesis; invocation and case-workspace.js audit | Covered | Invocation barrier is required; non-mutating workspace module is audit-only. |
| C9/Q3; P01-T02 regression evidence | Partial | Quality/proposal matrices are concrete; remaining named mutation handlers lack explicit execution coverage; PC-003. |
| P02-T01 requested checks and locked limits | Covered | Named suites, browser checks, pinned axe, Ruff limit, shared environment and bounded heavy-check admission are specified. |
| P02-T02 independent Review and local commit | Covered | One independent Review, preserved outcomes, privacy-safe identity and required trailer; no publication is authorized. |
| User approval and accessibility boundaries | Covered | Existing human/consent controls remain unchanged; axe is not treated as conformance acceptance. |

## Verdict

* Verdict: Revise
* Rationale: The central diagnosis and correction scope are credible, but the
  plan leaves an unsafe recovery-read ordering unspecified, risks treating
  upload preparation errors as ambiguous server outcomes, and does not
  establish execution-level regression coverage for every named sibling.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Define causally fresh, resource-specific recovery reads

* Related IDs: C2-C4/C7, Q2-Q3, P01-T01, P01-T02; acceptance criterion
  "Successful authoritative reload unlocks only current evidence/action state."
* Evidence: The plan requires a successful authoritative case GET; phase
  details say to clear barriers after successful authoritative reads.
  src/api/src/zava_forward/api/web/app.js caseView clears check-history
  entries immediately after its GET. assistants.js assistantProposal clears
  uncertain state when a card is constructed. app.js priorityPanel has a
  separate recommendation GET, and retained session.draftBox can preserve
  draft-review objects across case reloads. ops.js capacityView loads packages
  and work orders together.
* Concern: Success alone does not establish that a read observed the mutation.
  A GET started before the uncertain/committed response can complete afterward
  with an older snapshot. The plan does not require the recovery read to start
  after that outcome or define which reads reconcile each sibling's state.
  A case GET, cached proposal-card construction or retained draft object is
  not automatically authoritative evidence of a separate review's outcome.
* Impact: An older response can unlock a stale action and permit another
  mutation, or a retained review can remain permanently blocked despite an
  unrelated successful case reload.
* Smallest useful change: Specify a per-resource recovery contract: affected
  identity/revision, barrier generation, read endpoint(s), and the reset event.
  Only a successful relevant read initiated after the barrier was established,
  still belonging to the current session/generation, may reconcile it. Keep
  retained drafts copyable without inventing approval. If a review has no
  authoritative rehydration path, retain its block and specify a safe explicit
  reload/history path instead of treating a case rerender as confirmation.
* Action owner: Planning parent; implementation owner executes the contract.
* Exact resolving evidence: Revised P01 details identify recovery evidence for
  case submissions, proposal/draft/priority reviews, invocation and procurement.
  A deferred-read regression holds a pre-outcome GET, establishes the barrier,
  then resolves that older GET and proves another action dispatches no POST.
  A later relevant successful GET reconciles only current state; failed and
  obsolete-session reads cannot unlock it.
* Decision route: Direct planner correction. Existing user direction already
  requires authoritative recovery; no divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Separate upload preparation failures from dispatched uncertainty

* Related IDs: C1/C2/C5, P01-T01, P01-T02; correctable refusal and upload goals.
* Evidence: src/api/src/zava_forward/api/web/app.js documentsPanel.upload throws
  a plain Error when no file is available and rejects FileReader errors before
  calling api(). The current refresh implementation interprets an error
  without status as uncertainty. The plan moves upload dispatch inside guarded
  refresh and retains transport-without-status classification, but does not
  distinguish these pre-dispatch failures.
* Concern: Wrapping the existing upload routine wholesale in refresh makes a
  local file-selection/read failure indistinguishable from a lost POST
  confirmation. A broad case barrier would then incorrectly require history
  recovery for a request that never reached the server.
* Impact: A correctable local failure can freeze case submissions and mislead
  the person into believing a document may have been recorded.
* Smallest useful change: Explicitly separate local preparation from mutation
  outcome classification, using a dispatch marker or bounded preparation stage.
  Preserve duplicate protection during asynchronous file reading, but classify
  a failure before POST as retryable and retain the selected draft/file recovery.
* Action owner: Planning parent; implementation owner applies the distinction.
* Exact resolving evidence: P01 details specify the dispatch boundary. Extend
  an existing upload/shared-refresh matrix to show zero POSTs and no history
  barrier after file preparation failure, a subsequent valid submission works,
  concurrent attempts issue at most one POST, and lost/committed/uncertain POST
  responses still establish the history barrier.
* Decision route: Direct planner correction; no user response is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Assign shipped-handler regression coverage to all named siblings

* Related IDs: C3-C7/C9, Q3, P01-T02, P02-T01; locked test boundary.
* Evidence: Existing test_case_journey.py matrices execute proposal review,
  quality/manual actions, shared refresh and aiNotes draft review. Its current
  test_workspace_scripts.py companion covers loader and route behavior.
  case_journey_browser_check.py quality_pending_cleanup and
  assistants_browser_check.py review_pending_cleanup exercise quality/proposal
  refusal and reload failure. The supplied plan promises broad matrices but
  does not assign priority review, assistant invocation, procurement, raw
  resident/challenge submissions or upload to specific executable coverage.
* Concern: Extending the existing quality/proposal matrices alone can satisfy
  the stated aggregate check commands while leaving the other changed handlers
  untested. Their lifecycle differs: priority repaints on failure, invocation
  lacks a pending guard, procurement reenables in finally, and raw forms bypass
  api()/shared refresh. A shared predicate test cannot prove those handlers use
  it correctly or retain their own blocked state.
* Impact: The requested sibling correction can regress or remain incomplete
  while both browser checks and both unit modules still pass.
* Smallest useful change: Assign each named handler family to an existing
  matrix extension or one of the permitted new methods/helpers. Test the shared
  classifier's complete 409/503 by committed/uncertain/refusal matrix once;
  execute every changed handler with representative ambiguous and explicit
  refusal outcomes, counting actual dispatches and checking its recovery path.
  Keep the existing success/later-edit cases and locked addition limits.
* Action owner: Planning parent; test implementation owner supplies evidence.
* Exact resolving evidence: Revised P01-T02 lists the concrete test method or
  browser matrix owning each named family, including both raw-form variants.
  Result artifacts show one initial POST, zero repeat POSTs before relevant
  recovery, retained values/status feedback, and retryable explicit refusal
  for those handlers. Test diff confirms no removals and additions within the
  four-unit/two-helper limits.
* Decision route: Direct planner correction; no scope expansion or user
  decision is necessary.

## Strengths and Residual Risk

* Outcome-before-status correctly covers committed 409 as well as 503 and
  preserves ordinary explicit refusals.
* Session-wide, fieldless and measure/tab recovery requirements address
  bypasses that a form-key-only guard would miss.
* The plan preserves drafts and distinguishes recorded mutation from approval.
* The separate publication blocker is candid. No local browser pass, axe
  result or scoped unit result establishes complete-gate or human acceptance.
* Backend idempotency is explicitly outside this correction. This critique
  does not reopen that decision or require unrequested backend changes.

## Questions or Blocking Evidence Gaps

* None requiring user input. The supplied evidence supports a revision
  decision. The planning parent can resolve all findings directly.

## Limitations

* This is a plan credibility assessment, not an implementation Review or a
  test execution. No current source fix or runtime success is claimed.
* External thread/guideline content was considered through the supplied
  research record, not independently refetched. A fresh guidelines review
  remains an implementation/Review obligation.
* Source inspection was bounded to the supplied mutation trace and owning
  test/check locations; this is not a repository-wide audit.
* Existing dirty inputs are the supplied untracked round-seven planning
  artifacts. They were not changed, moved, staged or committed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define causal and resource-specific recovery evidence
  in P01, then incorporate PC-002/PC-003 directly before implementation.
* User response required: No.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/case-journey-526-round7-plan.md](.copilot-tracking/plans/2026-10-29/case-journey-526-round7-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/case-journey-526-round7-phase-details.md](.copilot-tracking/details/2026-10-29/case-journey-526-round7-phase-details.md) | Assessed phase contracts |
| [.copilot-tracking/research/2026-10-29/case-journey-526-round7-research.md](.copilot-tracking/research/2026-10-29/case-journey-526-round7-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/reviews/plans/2026-10-29/case-journey-526-round7-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/case-journey-526-round7-plan-critique.md) | Complete critique; Revise |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly and
finalize the plan without another critique pass. No user action is required.
This critic stops here; implementation and all validation remain with the
parent workflow.
