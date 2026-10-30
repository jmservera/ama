---
title: Resident chat launcher 520 final-candidate plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: 520
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/resident-chat-launcher-520-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/resident-chat-launcher-520-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and research, including C1-C7
  source pointers, and issue #520's body and owner comments retrieved read-only.
* Read the original case study, addendum, knowledge-base index and owner memory
  for context; memory is not evidence.
* Examined resident chat routing, HTTP dispatch, bounded AzureAdvisor selection,
  host-owned document facts, assistant UI, API tests, browser check and component
  validation guides.
* Covered all seven acceptance criteria and P01-T01, P01-T02 and P02-T01,
  preserving the specified test ownership, no removals, maximum two new methods,
  canonical test file and no generated targets.
* Applied the caller's finite RPI, local-commit-only, Refs #520, no push, no uv,
  synthetic-only and no Azure/deploy/live-sign-in/secrets boundaries.
* This assesses implementation-plan credibility, not implemented correctness,
  current regulatory completeness, operational calendars, live inference or
  human/assistive-technology acceptance. No implementation or validation gate
  was executed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1, C5, C7: launcher and interaction | Covered | Existing browser harness exercises signed-out, signed-in, loading/error, touch, keyboard, focus and narrow-screen states; proposed UI change is discoverability text only. |
| AC2, C2-C4: own-record isolation | Covered | HTTP handler resolves the session-owned case and reauthorizes before response; planned tests cover payload isolation, permission precedence and late revocation. |
| AC3, C1, C5: regulatory limits | Covered | Existing source and tests retain dated local provision references, bounded currentness and refusal of legal conclusions. No new legal rule is proposed. |
| AC4, C5: appointment proposals and confirmation | Covered | Existing real local SQLite and browser search/book/cancel/manual flows are retained; no calendar or booking-authority expansion is needed. |
| AC5, C3: AI/off/failure labels | Covered | Fixed-topic selection appends approved guidance to mandatory facts and retains sources; plan explicitly requires the typed-document disabled label and truthful fallback. |
| AC6, P02-T01: automated/local evidence | Partial | Planned gates and browser checks are appropriate, but their filesystem/lock execution contract conflicts with the active environment constraint; PC-001. |
| AC7, C1-C4, P01-T01: document answers | Covered | Bounded complete questions, existing document facts and fixed-topic advisor dispatch address the demonstrated admission and generated-prose gaps without adding upload or approval authority. |
| P01-T02: test reconciliation | Covered | The locked semantic/regression contract covers facts, source references, unknowns, no approval/upload, malformed selector output, complete-message refusals and unchanged other generation. Both existing generated-record test methods need reconciliation under that contract. |
| C5, P01-T02: browser integration | Covered | Existing ask_chat helper returns the newly added reply; plan requires ordinary document questions and newest-reply facts/source assertions while retaining agenda, session, focus, axe and reflow checks. |
| Handoff and user boundaries | Covered | Original evidence, one independent Review, local commit and attempted complete gate are planned; publication/live prerequisites remain blockers rather than inferred permission. |

## Verdict

* Verdict: Revise
* Rationale: The functional approach is credible and appropriately bounded.
  One execution-contract correction is needed before validation can follow
  this plan without violating the session's filesystem restriction. No design
  expansion, live action or additional critique is required.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Resolve the prohibited filesystem path before heavy validation

* Related IDs: AC6, P02-T01, Dependencies, Handoff.
* Evidence: The plan's User Decisions and Requirements and phase-details
  P02-T01 require flock -w 600 /tmp/ama-rpi-heavy.lock. The active execution
  instructions prohibit file operations under /tmp and temporary system paths.
  src/api/tests/test_resident_chat_api.py uses tempfile.TemporaryDirectory,
  and src/api/checks/resident_assistant_browser_check.py also uses default
  temporary directories for fixtures and fallback output. Merely specifying
  an allowed browser --out does not redirect those internal fixture paths.
* Concern: The plan neither resolves the lock-path conflict nor specifies
  compliant scratch-path configuration for the existing validation processes.
  Its fallback provision for missing prerequisites does not explicitly address
  this known conflict.
* Impact: Following the written command attempts a forbidden lock-file
  operation; default tempfile placement can independently violate the same
  restriction. Using a different private lock without coordination would not
  preserve shared heavy-run serialization. This can block the required fresh
  evidence even when all packages are available.
* Smallest useful change: Add a validation preflight that explicitly reconciles
  allowed scratch/output paths and existing tempfile behavior, and determines
  whether a compliant, genuinely shared lock is available. Do not unilaterally
  substitute a private lock, alter shared infrastructure, change the heavy-gate
  tooling or weaken serialization. If the required shared lock or complete gate
  cannot operate within the active filesystem constraint, record the affected
  validation as Blocked and retain that limitation in local delivery evidence.
* Action owner: Planning parent.
* Exact resolving evidence: Plan/details explicitly state the compliant
  scratch-path configuration, shared-lock preflight and fail-closed outcome;
  subsequent changes/Review evidence records the paths and lock actually used,
  or the exact blocked commands, without claiming their execution or success.
  Required evidence must remain outside candidate inputs where the complete
  gate requires it. This critique does not require running those commands.
* Decision route: Direct planner correction. No user response is required:
  inability to satisfy the existing constraints is a reported blocker, not
  permission to change scope or request prohibited live actions.

## Strengths and Residual Risk

* Reusing AzureAdvisor.answer for typed documents retains document_answer's
  mandatory answer and source tuple; selector success adds only known guidance
  sentences, and failure preserves deterministic facts. Other typed topics
  can remain on answer_question without redesigning model behavior.
* The existing handler's permission and session checks surround either advisor
  path. The planned late-revocation and payload-isolation regressions correctly
  protect this integration boundary.
* Finite full-message alternatives preserve refusal precedence and avoid
  keyword-routing arbitrary composite requests into record/model access.
* Reconcile both test_typed_record_questions_generate_but_explicit_topic_stays_legacy
  and test_complete_record_questions_still_generate in the existing canonical
  test file. This is execution detail within the already required reconciliation,
  not an additional test suite, finding or scope change.
* The existing browser harness exercises real loopback requests and local agenda
  mutations, and already handles long document answers and source disclosure at
  320px with 200% root text resizing. The plan does not misrepresent that as
  native zoom, human acceptance or full WCAG conformance.
* Large valid document payloads can exceed the existing model request cap and
  truthfully fall back to rules; retaining the cap is appropriate.
* The owner's authenticated resident check, actual model/content evaluation,
  operational consents/calendar history and human/AT acceptance remain outside
  authorized local work. No closing keyword or whole-issue closure is justified.

## Questions or Blocking Evidence Gaps

* No unresolved functional design decision requires the user.
* Heavy validation feasibility remains subject to PC-001 and actual prerequisite
  checks; unavailable evidence must be recorded, not replaced with cloud runs
  or fabricated success.

## Limitations

* Source inspection only: no tests, browser sessions, heavy gates, deployment,
  sign-in or model calls were performed.
* No fresh external regulatory-currentness assessment or independent web-design
  guideline refresh was performed. Existing routing/citation behavior and the
  supplied research's recorded guideline retrieval were assessed only for this
  bounded plan.
* Existing untracked parent-owned plan, details, research and session-state
  artifacts were observed and left unchanged. Only this critique was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Disposition PC-001 directly in plan/details, then
  finalize the plan and continue the authorized implementation and one Review.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/resident-chat-launcher-520-plan.md](.copilot-tracking/plans/2026-10-30/resident-chat-launcher-520-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/resident-chat-launcher-520-phase-details.md](.copilot-tracking/details/2026-10-30/resident-chat-launcher-520-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-30/resident-chat-launcher-520-research.md](.copilot-tracking/research/2026-10-30/resident-chat-launcher-520-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-chat-launcher-520-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-chat-launcher-520-plan-critique.md) | This single independent critique |

## Next Steps

Planning parent: resolve PC-001 directly, preserve this original critique and
finalize without another critique. No user action is required. This reviewer
stops here; implementation and validation remain with the parent.
