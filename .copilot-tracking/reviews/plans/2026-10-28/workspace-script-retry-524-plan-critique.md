---
title: Workspace script retry final-candidate plan critique
description: Independent original critique of the issue 524 implementation candidate
ms.date: 2026-10-28
---

## Metadata

* Task ID: 524
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md
* Research: .copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md
* Critique execution status: Complete
* Original dated verdict: Revise, 2026-10-28
* Candidate HEAD: 413ccaf253fce4566e855bae9d0a924b2a82b506
* Observed branch: fix/workspace-script-retry-524
* Assessment count: Exactly one final-candidate critique.

## Inputs and Criterion Boundary

* Assess the supplied candidate for bounded missing-script recovery in
  requireWorkspaceScripts, including actual browser failed-first-load coverage,
  unchanged terminal wording, native controls and non-colour status.
* Preserve the ordered Research, Plan, Implement and independent Review workflow.
  No Azure access, secrets, .env, private datasets or deployment is authorized.
* Preserve the locked test ownership, no removals, two-file executable addition
  ceiling, canonical app.js target and semantic/regression coverage split.
* Research evidence C1-C7 and W1-W2 was considered. Source inspection covered
  app.js dependency predicates, route cancellation and sign-out; index.html;
  companion-script declarations; the Node VM test precedent; the synthetic
  browser server; API lint/type configuration; and src/README.md gate guidance.
* W1/W2 are supplied research claims, not independently refreshed remote evidence.
  This critique does not implement, execute tests, investigate live infrastructure,
  establish accessibility conformance or certify publication readiness.
* Initial status contained only four untracked supplied RPI artifacts: the plan,
  details, research and session-state JSON. No tracked modifications appeared.
  The earlier clean-start claim is research evidence, not a clean worktree
  observed at critique time. These existing artifacts were left untouched.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1 / Q2 / C1 / C3 | Covered | Startup order and static delivery evidence are identified; historical live cause remains explicitly unresolved. |
| AC2 / P01-T01 / C2 | Partial | Actual recovery is planned, but the timed script lifecycle needs PC-001 resolution. |
| AC3 / C2 | Covered | Exact existing message, semantic alert/status and native keyboard reload checks are specified. |
| AC4 / P01-T02 / C4 / C5 | Partial | Unit/browser ownership is clear; late script execution is not exercised. |
| AC5 / W1 | Covered | Live post-deploy verification remains owner-pending; Refs #524 avoids claiming closure. |
| Additional readiness / Q1 / Q3 | Partial | HTTP 200 without its expected global is named, but its retry/cache disposition is ambiguous: PC-002. |
| Route, role and session preservation / P01-T01 | Covered | Preserve current predicates and check obsolete-route cancellation before rendering or publishing errors; browser navigation/sign-out cases are assigned. |
| Attempt budgets and cleanup / P01-T01 | Partial | Two retries, delays, timeout and shared budgets are explicit; element removal alone does not establish execution cancellation: PC-001. |
| Test ownership and change budget | Covered | app.js, API README and exactly two allowed executable additions; no removals or new dependencies. |
| P02-T01 / validation prerequisites | Partial | Focused commands and API discovery exist, but prescribed filesystem paths conflict with this execution environment: PC-003. |
| P02-T02 / C7 / publication | Covered with blocker | Original Review, committed evidence and external exact-head receipt remain separate gates; PC-003 can block their execution, not justify bypassing them. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Implementation readiness: The scope and principal design are credible, but the
  planner should settle retry lifecycle/readiness semantics before P01. These are
  direct corrections within the accepted workstream, not new product choices.
* Publication readiness: Not established. Independent implementation Review,
  executed validation and the required complete exact-head receipt are future
  prerequisites. A missing tool, forbidden path or unavailable shared lock must
  be reported as a blocker rather than treated as a reason to skip a gate.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Timeout settlement does not establish that a classic script cannot execute later

* Related IDs: P01-T01, P01-T02, AC2, AC4, additional hanging-attempt coverage,
  non-functional cleanup and no-unnecessary-reload requirements.
* Evidence: .copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md:41-50
  prescribes dynamic classic script tags, a five-second timeout and removal on
  settlement. Its browser scenarios at lines 55-62 do not include a response
  arriving after that timeout.
  src/api/src/zava_forward/api/web/panels.js:3-5 and
  src/api/src/zava_forward/api/web/role-screens.js:3-5 contain top-level lexical
  declarations; research C6 already identifies duplicate execution as unsafe.
* Concern: Clearing handlers and removing an inserted script element is not an
  established cancellation barrier for an already-started external script.
  The first timed-out request may still evaluate while or after the second
  attempt succeeds. The plan does not specify how it prevents or safely handles
  this overlap. Rechecking globals only after the recovery sequence does not
  settle the case where two outstanding deliveries evaluate the same source.
* Impact: Recovery can create a lexical redeclaration error or duplicate
  initialization, even while the promise/request-count tests pass. A mocked
  timer test proves bounded waiting, not real browser execution isolation.
* Smallest useful change: Define the late-delivery policy and an implementation
  mechanism that makes timeout/retry overlap safe. Recheck readiness before
  inserting any subsequent attempt, but do not claim that alone cancels an
  already-started request. Add a focused real-browser delayed-companion scenario
  within the existing allowed browser file; adjust the loading mechanism within
  app.js if plain tag removal cannot meet the policy.
* Action owner: Planning parent, with implementation and evidence owned by
  P01-T01 and the existing P01-T02 browser-check owner.
* Exact resolving evidence: Revised phase details specify the execution-safety
  mechanism and late-result disposition. The planned Chromium check withholds
  a lexical companion response beyond 5000ms, permits the next attempt to
  progress, then releases the old response and checks the intended view,
  bounded attempts, absence of duplicate-evaluation errors and absence of stale
  terminal/progress updates. Include the no-recovery late-settlement outcome
  where relevant to the chosen mechanism. Execution evidence belongs to P02,
  not to this planning critique.
* Decision route: Direct planner correction. No significant or divergent user
  decision is needed; do not broaden source targets or the executable-file cap.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Successful transport has no explicit per-attempt readiness/cache transition

* Related IDs: P01-T01, P01-T02, functional readiness requirement, additional
  missing-global-despite-HTTP-200 coverage.
* Evidence: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md:62-65
  separates fixed-path shared attempts from the readiness check.
  .copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md:41-50
  says to recheck readiness after recovery but does not state whether a load
  event without the expected global consumes a failed attempt and continues.
  src/api/src/zava_forward/api/web/app.js:148-156 supplies the authoritative
  expected-global predicates.
* Concern: An implementation could resolve and cache the path promise on the
  first load event, discover the missing global only in the route recheck, and
  permanently fail with an unused retry. Merely asserting that HTTP 200 is not
  readiness would not distinguish that behavior from the intended recovery.
* Impact: A transient empty/wrong script response can leave the workspace
  unrecoverable despite a remaining automatic attempt. The page-lifetime cache
  makes this disposition persist across navigation.
* Smallest useful change: Specify that each attempt validates the expected
  predicate before being considered successful; a transport success without
  readiness consumes an unsuccessful attempt and uses the remaining budget.
  Cache the bounded recovery result, not an unvalidated load event. Preserve
  the final route-specific missing-path recheck and existing terminal wording.
* Action owner: Planning parent; P01-T01 implementer and P01-T02 unit-test owner.
* Exact resolving evidence: Phase details explicitly define these transitions.
  Unit cases cover first retry load-without-global followed by second retry
  readiness, and both retries load-without-global followed by unchanged terminal
  failure; revisit the failed route and prove no new requests. Keep these cases
  in tests/test_workspace_scripts.py under the locked ownership split.
* Decision route: Direct planner correction; current user direction already
  requires bounded recovery and global-based readiness. No user response needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Validation instructions require filesystem operations forbidden in this execution environment

* Related IDs: P02-T01, P02-T02, dependency setup, shared heavy-gate lock,
  complete publication gate.
* Evidence: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md:153-155
  records a task venv under a forbidden temporary root.
  .copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md:75-90
  directs using that environment and a shared lock under that root.
  src/README.md also documents the full runner's shared-lock requirement.
  Active execution instructions prohibit file operations in temporary directories
  and require newly created files to be workspace-relative.
* Concern: The validation recipe cannot be followed verbatim in this environment.
  This is an execution-policy mismatch, not evidence that the implementation is
  defective or that the publication gate is optional.
* Impact: Focused heavy validation or final publication can block even after
  source implementation is otherwise ready. Silently using a different lock
  would lose shared serialization; using the forbidden locations would violate
  the active execution boundary.
* Smallest useful change: Preserve the historical dependency-setup record,
  specify a permitted workspace-relative task environment for future operations,
  and record the mandated shared-lock/full-gate path conflict explicitly.
  If the mandated gate cannot run in an authorized execution context, stop at
  a local candidate with validation/publication blocked. Do not invent a
  replacement lock, modify the gate or publish without its required receipt.
* Action owner: Planning parent for the executable instructions and blocker
  record; an authorized execution-context provider for any later gate run.
* Exact resolving evidence: Revised P02 details distinguish runnable local work
  from blocked heavy/full-gate work, retain the original path/setup history,
  and identify a permitted execution context before claiming those checks ran.
  Publication still requires the actual complete exact-head receipt and fresh
  verification against current origin/main; a planning acknowledgement alone
  is not gate evidence.
* Decision route: Direct planner correction and explicit prerequisite blocker.
  No product/user-scope decision is needed, and no policy bypass is proposed.

## Strengths and Residual Risk

* Fixed same-origin targets, page-lifetime budgets, explicit timing and retained
  predicates constrain the repair appropriately.
* The exact terminal message and native status/alert/button semantics remain
  protected without redesign or a new dependency.
* Actual script bytes, an actual map, document-navigation count and permanent
  failure give the browser check meaningful semantic responsibilities.
* Original critique/Review evidence, unresolved historical cause and owner-pending
  live verification are preserved. Source headers do not prove historical live
  delivery, and local success must not be presented as deployment acceptance.
* The supplied no-Azure boundary is compatible with investigating this local
  behavior; missing live telemetry is not an implementation-readiness blocker.

## Questions or Blocking Evidence Gaps

* No unresolved significant user choice was found within this candidate.
* The late-execution policy needs planner resolution, not open-ended research.
* Publication prerequisites are not yet executed, and the filesystem/shared-lock
  conflict must remain visible until a permitted execution context exists.

## Limitations

* No tests or browser sessions were run; this is a plan critique, not an
  implementation Review or a reproduction of browser-specific cancellation.
* No network, Azure, credential, .env or private-dataset inspection occurred.
* Only the supplied candidate and directly relevant cited evidence were assessed.
  Upstream PR lifecycle and the historical clean-start claim were not refreshed.
* Only this critique artifact was created. Plan, details, research, session
  tracking and production/test sources remain unchanged by this assessment.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Resolve the timed-out classic-script execution policy,
  specify per-attempt readiness transitions and correct/qualify the validation
  execution recipe. Finalize the candidate directly, without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md](.copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md) | Assessed canonical candidate |
| [.copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md](.copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md) | Task and validation details |
| [.copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md](.copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md) | Supplied evidence and uncertainty |
| [.copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-plan-critique.md) | Original dated critique |

## Next Steps

The active planning parent should disposition PC-001 through PC-003 directly,
then continue the authorized ordered RPI loop only through satisfied gates.
No user action or second critique is required. This independent assessment stops
here; publication prerequisites remain separate from implementation readiness.
