---
title: Account Switch Final-Candidate Plan Critique
description: One bounded assessment of the explicit account chooser repair and delivery evidence
ms.date: 2026-10-13
---

## Metadata

* Task ID: zava-account-switch-2026-10-13
* Critique date: 2026-10-13
* Plan: .copilot-tracking/plans/2026-10-13/zava-account-switch-plan.md
* Phase details: .copilot-tracking/details/2026-10-13/zava-account-switch-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique, including the owner's same-task documentation addition.

## Inputs and Criterion Boundary

* Caller requirements: repair Use another account, preserve normal logout and prior tenant bindings, provide useful no-identity flow events, respect existing successful allLogs routing, preserve deployment configuration, and keep real-browser account replacement owner-owned.
* Supplied research: .copilot-tracking/research/2026-10-13/zava-account-switch-research.md, including reported Microsoft documentation, HTTPS prompt forwarding, existing ContainerAppConsoleLogs ingestion, and the Copilot provider HTTP 403 followed by successful owner attempt 3.
* Read-only implementation evidence: mvp/zavaforward_mvp/auth.py; mvp/zavaforward_mvp/server.py; mvp/tests/test_auth.py; mvp/web/app.js, signOut segment.
* Context: docs/case_study_48_original.md; relevant opening and exercise-acceptance portions of docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md.
* Decisions: fixed /sign-in?switch=1 followed by Easy Auth prompt=select_account and fixed /app return; no provider-logout-first switching, global Microsoft logout, new consent, directory mutation, or authentication exemption.
* Dependencies: P01-T01 implementation precedes P01-T02 validation and image rollout; P01-T03 publishes supported results and preserves outstanding owner acceptance. Research already reports readiness; it is not a new research assignment.
* Test ownership: primary owns mvp/tests/test_auth.py; maximum three new methods using subcases; no removals; only the intentional existing switch expectation changes.
* Documentation addition: dated PRD review-learning dispositions, ADR 0002 identity/session mechanics, and addendum observed exercise evidence; supported earlier welcome/photo and role-initialization learning only. No unrelated BRD requirements, new ADR, or personal roster.
* Assessment boundary: credibility of this supplied candidate, not a vulnerability audit, live platform verification, directory inspection, full project-document review, or actual browser acceptance. No source, plan, research, configuration, or live resource was changed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P01-T01: fixed switch versus ordinary logout | Covered | auth.py currently sends switching through provider logout; app.js already follows the server redirect. The proposed server-owned split is appropriately narrow. |
| P01-T01: exact flag and fixed destinations | Covered | Plan rejects duplicate/untrusted flags and caller-supplied prompts/returns. Blank duplicate parsing needs explicit implementation care, noted below. |
| P01-T01: authorization, CSRF and password behavior | Covered | Existing POST checks and trusted-proxy tenant/role/oid gates remain; password mode stays local. Existing regressions remain owned by the primary. |
| P01-T01: required flow diagnostics | Partial | Phase details explicitly describe only switch request and app arrival, not all five plan-required transitions; PC-001. |
| P01-T02: targeted/full tests and image smoke checks | Covered | Existing tests plus at most three new methods, local non-root image checks, and live semantic prompt checks are proportionate. |
| P01-T02: Easy Auth and browser evidence | Covered with accepted limit | Research establishes prompt forwarding, not existing-cookie replacement. The plan explicitly leaves authenticated replacement to the owner. |
| P01-T02: configuration preservation and rollback | Partial | Image-only intent and old-image rollback exist, but preservation has no explicit before/after acceptance evidence; PC-002. |
| P01-T02: centralized logging | Covered | Existing allLogs and actual ContainerAppConsoleLogs are supplied evidence. No new resource or broad access logging is justified. |
| P01-T03: workflow cause and retry | Covered | Copilot provider HTTP 403 is distinct from workbench Entra; owner attempt 3 succeeded. No duplicate run or credential change is needed. |
| P01-T03: canonical learning and publication | Covered | Updated candidate places learning in PRD, ADR 0002, addendum and index/log, with historical evidence and acceptance limits preserved. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 0; Medium 2; Low 0.
* Rationale: The chosen repair and acceptance boundary are credible. Two direct phase-detail corrections are needed to make the promised diagnostic coverage and safe configuration-preserving rollout verifiable. Neither requires a new user decision, broader architecture, personal credentials, or another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Carry all five required flow events into implementation and proof

* Related IDs: P01-T01, P01-T02; functional requirement for fixed flow events; acceptance criterion for console and centralized event visibility.
* Evidence: .copilot-tracking/plans/2026-10-13/zava-account-switch-plan.md requires explicit switch request, chooser start, ordinary sign-in, ordinary sign-out, and authorized workbench arrival. .copilot-tracking/details/2026-10-13/zava-account-switch-phase-details.md P01-T01 explicitly instructs fixed prints for request and arrival only; P01-T02 generically says to collect constant events.
* Concern: The executable detail and proof do not enumerate the other three transitions. Two markers alone cannot distinguish ordinary SSO login, attempted selection, and ordinary logout in the next reported failure.
* Impact: Delivery could pass generic event checks while omitting diagnostics the owner explicitly requested.
* Smallest useful change: Add a five-event trigger checklist to P01-T01 and its validation matrix to P01-T02. Emit authenticated POST switch/sign-out events after existing user/CSRF checks; emit normal-sign-in versus chooser-start events at their respective fixed redirects; emit workbench arrival only after successful authorization. Keep each message constant and do not label chooser-start or arrival as proof of a selected different account.
* Action owner: Planning parent; primary implementer executes the revised checklist.
* Exact resolving evidence: Revised details enumerate all five triggers; the constant-event test method uses subcases to assert exact complete messages and absence of new success-flow messages on denied arrivals/POSTs. Exercise ordinary sign-in and chooser-start through unauthenticated live GETs and show their fixed messages in console and ContainerAppConsoleLogs. Use synthetic valid-principal POST/arrival captures for events that require authentication, recording live equivalents as owner-pending if unavailable rather than demanding a browser session. No fourth new test method is needed.
* Decision route: Direct planner correction; no significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make image-only configuration preservation an explicit rollout gate

* Related IDs: P01-T02; non-functional requirement preserving SQL staff, AI, scopes, secrets and token store.
* Evidence: .copilot-tracking/details/2026-10-13/zava-account-switch-phase-details.md says to update only the image, wait ready and preserve the current image for rollback. .copilot-tracking/plans/2026-10-13/zava-account-switch-plan.md names preservation invariants but its acceptance criteria do not require comparing them. The owner confirms the prior tenant bindings and expects them retained.
* Concern: Readiness and a working /sign-in redirect do not establish that app configuration, authentication settings, serving revision/image, or preserved runtime dependencies survived the rollout.
* Impact: A seemingly successful chooser deployment could mask lost SQL/AI settings, scoped own-photo access, token-store behavior, or unintended revision traffic.
* Smallest useful change: Require a private pre-rollout configuration baseline and post-rollout comparison, an unambiguous tested image tag/digest and serving-revision check, and explicit rollback on unexpected configuration drift or failed readiness/live route validation. Use the existing image-only update path; do not replace the full app/auth configuration or reprovision SQL/staff.
* Action owner: Planning parent; primary deployment owner performs and records checks.
* Exact resolving evidence: Revised P01-T02 names the preservation gate. Delivery evidence records tested and deployed image identity, ready serving revision/traffic, and a redacted pass/fail comparison of environment settings and secret references, identities, ingress, registry settings, and Easy Auth scopes/token-store settings. Preserve the prior image reference and record the rollback trigger. Do not fetch secret values or copy raw sensitive configuration into Git; do not add SQL writes to prove a no-write invariant.
* Decision route: Direct planner correction; no significant or divergent user decision.

## Strengths and Residual Risk

* The fixed local route avoids provider end-session dependence without weakening normal logout. It does not automatically select a different person. No global logout, prompt=consent, new registration, or authentication exemption is warranted.
* Platform evidence is appropriately limited: the reported HTTPS trace proves select_account forwarding, not that an already-valid Easy Auth cookie cannot short-circuit reauthentication or that the callback replaces that cookie. Easy Auth must retain ownership of state, nonce and session issuance.
* Existing-session acceptance remains explicitly owner-owned, not an implementation blocker invented by this critique. The eventual owner checklist should start in an already-authenticated browser, activate Use another account, observe the chooser, optionally select another already-authorized account, and verify the returned workbench/current-account view. Record only pass/fail observations, never names or a roster.
* Choosing the same account, cancelling, returning through browser Back, or selecting an unprovisioned account are not evidence of a successful different-account replacement. Cancellation need not log out the old session. A denied selected account must not be described as an authentication bypass or remedied by weakening role/oid gates.
* If the owner later observes old-cookie short-circuiting or stale account/photo state after a completed selection, report that narrower evidence before proposing a platform session-reset change. This candidate must not silently expand into global Microsoft logout.
* A direct, file-free Python 3 parsing check showed that parse_qs defaults discard blank values: switch=1&switch= and switch=&switch=1 become ["1"]. Preserve blank values when enforcing the single-value requirement and include these strings in the existing hostile-flag subcases. This implements an already-present requirement, not an additional finding or user decision.
* New success-flow markers can be strictly no-identity. Existing auth.py _deny prints identity-related detail, so do not claim that all historical/application/platform logs are identity-free. Changing unrelated denial diagnostics or enabling general request logging is outside this repair.
* The existing test's normal logout/CSRF assertions can stay intact while changing only its switch destination expectation. Input, event and password coverage fits three new methods with subcases; do not replace or generate a new test corpus.
* Dated PRD/ADR/addendum updates should distinguish owner-reported role access, observed synthetic/platform evidence and pending real-user acceptance. Prior learning is integrated only from supported published evidence; rubric retry success does not prove browser acceptance or full product acceptance.

## Questions or Blocking Evidence Gaps

* None requiring a user response before implementation. The owner has already resolved the switch mechanism, consent boundary and separate real-browser acceptance responsibility.
* Actual existing-session replacement remains unverified by design. CLI authentication, synthetic principal headers, a new browser context, and an unauthenticated chooser screenshot cannot close that owner gate.

## Limitations

* Official documentation, live Azure observations and workflow outcomes were assessed as supplied research evidence; no new web research, Azure calls or live mutation occurred.
* No tests, Docker build, deployment or browser login were run. The only executable check was the standard-library query-parsing demonstration, which created no files.
* The broader PRD, ADR and addendum were not independently audited; the owner's requested integration was assessed against the updated P01-T03 scope only.
* Existing untracked planning artifacts were not moved, committed or modified. This critique writes only its caller-specified review artifact.

## Recommended Next Action

* Highest-impact finding: PC-002, because readiness alone does not prove preservation of the already-working runtime and authentication configuration.
* Action owner: Planning parent.
* Smallest next action: Add the private before/after preservation gate to P01-T02 and the five-event checklist/proof to P01-T01/P01-T02, then reconcile critique disposition and proceed through the active parent's implementation gate.
* User response required: No. Actual browser replacement remains a separately recorded owner acceptance step, not a request for credentials.
* Stop: This is the complete actionable finding set for one final-candidate critique; do not launch another critique or agent.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-13/zava-account-switch-plan.md](.copilot-tracking/plans/2026-10-13/zava-account-switch-plan.md) | Updated final candidate and acceptance boundary |
| [.copilot-tracking/details/2026-10-13/zava-account-switch-phase-details.md](.copilot-tracking/details/2026-10-13/zava-account-switch-phase-details.md) | Implementation, deployment and learning tasks |
| [.copilot-tracking/research/2026-10-13/zava-account-switch-research.md](.copilot-tracking/research/2026-10-13/zava-account-switch-research.md) | Supplied platform, logs and workflow evidence |
| [.copilot-tracking/reviews/plans/2026-10-13/zava-account-switch-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-13/zava-account-switch-plan-critique.md) | Complete one-pass critique and resolving evidence |

## Next Steps

The active planning parent resolves PC-001 and PC-002 directly, finalizes without another critique, and continues its approved lifecycle. No new user decision or credential request is required; retain owner authenticated-browser acceptance as pending until actually observed.
