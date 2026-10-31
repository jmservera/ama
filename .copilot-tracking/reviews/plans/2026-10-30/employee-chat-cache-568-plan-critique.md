---
title: Employee chat and release cache final-candidate plan critique
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 568
* Task slug: employee-chat-cache-568
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-cache-568-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/employee-chat-cache-568-phase-details.md
* Research: .copilot-tracking/research/2026-10-30/employee-chat-cache-568-research.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: sequential research, plan, implementation and independent Review; shared employee/resident Return and Send regression; release-safe JS/CSS/library delivery on both sites; full local API discovery, Ruff, format, mypy and real Playwright; serialized heavy work; local commit with Refs #568 and the requested coauthor; no cloud, live sign-in, secrets, deployment or push.
* Supplied plan, phase details and research were read completely. Bounded supporting reads covered src/api/checks/chat_submit_browser_check.py, src/api/tests/test_workspace_scripts.py, the employee recovery loader and chat integration, the three static handlers, entry-point asset references, component validation guidance and development configuration. Repository case-study and reference context was also consulted.
* Decisions assessed: preserve the shared focus fix already reported in base d986c4c4; immutable-in-process packaged snapshots; deterministic filename/content release identity; versioned initial URLs and retries; no-store HTML/API/errors; byte-derived ETags and mandatory static revalidation; current bytes permitted at old-version URLs without an immutable promise.
* Acceptance boundary: AC1-AC5 and FR1-FR5, including ordinary launcher behavior, conditional GET/HEAD, old URLs, bounded recovery and a genuinely warm browser cache across a constructed release change.
* Test ownership/budget boundary: API-owned tests in src/api/tests and checks in src/api/checks; no removals; at most one new unit/HTTP module and one new browser harness; extend existing coverage preferentially.
* This is a credibility assessment, not implementation validation, a fresh web-guidelines review, live acceptance or a publication gate.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C3, C5-C7, FR1 | Covered | Research correctly distinguishes an existing shared source fix from unavailable historical deployed bytes; no duplicate widget is proposed. |
| FR2, AC1, P01-T02 | Partial | Ordinary-open/no-reset, focus, route/session refresh and deliberate dismissal are planned, but the employee success path can still use a fabricated browser reply; PC-003. |
| Q2, C4, C9, FR3, AC2, P01-T01 | Covered | Explicit packaged maps, filename/content identity, all three handlers and entry aliases include shared and vendored JS/CSS. |
| FR4-FR5, AC3, P01-T01 | Covered | Byte ETags, weak/list/star matching, empty HEAD/304, changed validators, old/unversioned URLs and admission/no-store separation are explicit. |
| C8, FR3, AC4, P01-T02 | Covered | Complete original script URLs, DOM-light source-test compatibility and retained retry/timeout/session guards cover the recovery contract. |
| AC2-AC4, P01-T03 warm-cache regression | Partial | Warm context and no routing are specified, but same-origin release turnover, demonstrated cache reuse and observable fresh execution/style are not acceptance assertions; PC-002. |
| AC5, P01-T03 validation environment | Partial | Requested checks and failure disclosure are explicit, but the named execution paths contradict the task environment's file-operation restriction; PC-001. |
| Test ownership and change budget | Covered | API ownership, addition ceilings, no removals, intentional header-only expectation changes and semantic rather than count-based coverage are locked. Findings can be resolved within this budget. |
| Full RPI, local commit, Review and publication boundaries | Covered | One independent implementation Review and original evidence/local commit are planned; no push is authorized and full-gate publication evidence is explicitly separate. |
| Local-only, no live identity/model/deployment | Covered | Synthetic browser/server fixtures and explicit live/human acceptance exclusions preserve the caller boundary. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: The delivery architecture and locked test budget are credible. Before implementation, the parent must reconcile prohibited execution paths and turn the two principal browser regressions into unambiguous measurable proofs. None of these corrections changes the selected architecture or requires a divergent product decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Named validation dependencies violate the execution path restriction

* Related IDs: AC5, P01-T03, Dependencies, User Decisions and Requirements.
* Evidence: The plan requires the lock file /tmp/ama-rpi-heavy.lock and pip environment /tmp/mv. Phase details instruct validation with that environment under the heavy lock. The supplied execution instructions prohibit file operations in /tmp or other temporary directories and require created files to remain relative to the working directory. P01-T03 also calls for temporary constructed asset roots without constraining their location.
* Concern: The candidate says there are no implementation blockers but its prescribed validation path is not executable under the current restriction. Opening a prohibited lock file or using a prohibited environment is not made permissible by the plan. Unilaterally substituting a worktree-specific lock would also fail to serialize with other workers using the shared lock.
* Impact: Implementation could violate the environment boundary, run heavy checks without effective shared exclusion, or incorrectly report AC5 as complete.
* Smallest useful change: Revise validation prerequisites to use permitted paths, including constructed asset roots and browser output. Establish a permitted shared lock honored by all relevant heavy workers before running those checks; do not silently substitute an unshared lock. Select a permitted installed environment, or record the actual missing-dependency failure before permitted pip setup. If coordinated serialization cannot be established, explicitly block heavy validation and report AC5 as unproven rather than bypassing either constraint.
* Action owner: Planning parent; shared-lock coordination belongs to the parent/coordinator.
* Exact resolving evidence: Plan/details identify permitted environment, fixture/output and shared-lock locations, the bounded flock wait and the coordination prerequisite. Implementation evidence subsequently records the actual lock admission and check exits, or an explicit blocked outcome without executing prohibited-path operations.
* Decision route: Direct planner correction and prerequisite coordination. No user response can waive the hard execution restriction; none is requested.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The warm-cache release test lacks observable pass/fail conditions

* Related IDs: FR3-FR5, AC2-AC4, P01-T03, Test Ownership and Change Budget.
* Evidence: Phase details require constructed release A/B asset roots, a warm context, normal navigation, no cache-disabling Playwright routing and fresh JS/CSS. They do not require preserving the origin across release turnover, proving that A populated/reused the browser cache, or asserting executed JavaScript and applied CSS from B. Research explicitly identifies previously fresh old-URL cache entries as the reason headers alone are insufficient.
* Concern: The stated exercise could pass with a fresh origin or unpopulated cache, or by checking only changed URL strings. Because packaged bytes are snapshotted at handler creation, editing the fixture root alone cannot simulate release B. A test of newly introduced no-cache responses also does not by itself exercise the legacy fresh unversioned-entry risk.
* Impact: The principal release-freshness regression can remain unproved even when AC2 URL and AC3 socket assertions pass.
* Smallest useful change: Add an explicit browser acceptance sequence within the existing harness budget: serve A on a fixed loopback origin, populate and demonstrate browser cache reuse/revalidation, recreate the handler/snapshot for B on the same origin, then perform ordinary navigation in the same context. Assert B entry URLs, an executed JS marker and an applied CSS value, including observable vendored/shared asset identity. Include a bounded legacy case that primes an old unversioned asset with a fresh cache lifetime before navigating to versioned B. Keep browser cache enabled and avoid page/context routing in this exercise; inject failures server-side. Tie recovery assertions to the exact initial versioned URL and bounded request attempts.
* Action owner: Planning parent, with implementation owned by P01-T03.
* Exact resolving evidence: Revised details enumerate the fixed-origin A/B turnover and assertions. Browser output records A cache evidence, unchanged origin/context, B JS/CSS observations, dependency identities and retry URLs/counts. The legacy cached URL does not supply B's executed code or style. Actual run failures remain failures.
* Decision route: Direct planner correction; no new dependency, additional test module or user decision is necessary.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Ordinary employee opening is not explicitly paired with a real server reply

* Related IDs: FR1-FR2, AC1, P01-T02, C7.
* Evidence: src/api/checks/chat_submit_browser_check.py:26 resets/reinstalls employee chat before opening. Its employee send matrix intercepts the ask request and fulfills a constructed reply at lines 53-101. The resident exercise already receives an actual local rules answer. P01-T02 removes the reset shortcut and requires socket-delivered source, but does not require the added employee success case to let thread creation and ask responses reach the actual local server.
* Concern: A no-reset launcher test can still reuse the fabricated reply path and satisfy the current completion wording. Loading source over sockets is not evidence that the employee's ordinary launcher-to-answer integration works through its server endpoint.
* Impact: The revised browser evidence could prove focus behavior but still miss an employee-only endpoint/session integration failure affecting visible answers.
* Smallest useful change: Require at least one ordinary authenticated synthetic employee session, with no reset/install override, to submit both Enter and mouse Send through the real loopback thread/ask endpoints and display successful server-produced replies. Use the existing synthetic rules/fake-model fixture, not live inference or sign-in. Retain the controlled-delay matrix for pending route/session refresh and dismissal races; do not replace its coverage.
* Action owner: Planning parent, with implementation owned by P01-T02.
* Exact resolving evidence: Plan/details separate real-endpoint happy-path assertions from controlled race tests. Browser results record successful local thread/ask responses, the added assistant message, visible panel/reply, expanded launcher and retained composer focus for both activations without employeeChat.reset/install or ask-route fulfillment in that happy path. Existing route/session and deliberate-dismissal cases remain covered.
* Decision route: Direct planner correction within the existing harness and test budget; no user decision or live service is required.

## Strengths and Residual Risk

* Conditional HTTP semantics are unusually concrete: body-derived quoted ETags; weak, list and wildcard validators; empty 304/HEAD; changed release contents; and distinct static versus HTML/API/error policy.
* Serving current bytes at an old query URL is an explicit, bounded choice, not an accidental immutable-cache claim. Historical deployment acceptance remains unknown.
* The snapshot design avoids per-request file reads and identity derived from git, secrets, user content or runtime credentials.
* Shared-widget identity, initial/recovered versions and Leaflet are in scope. Recovery preserves existing timeout behavior rather than blindly retrying timed-out lexical scripts.
* Existing auth, host checks, allowlists, CSP, MIME types, consent and manual dismissal are preserved. No visual redesign is authorized.
* API test ownership and addition limits need no relaxation to resolve these findings.
* Local engineering success cannot establish deployed employee-site behavior, actual model behavior, human accessibility acceptance, hosted approval or publication eligibility.

## Questions or Blocking Evidence Gaps

* No unresolved user product or architecture decision.
* PC-001 is an execution prerequisite, not permission to bypass the shared lock or the path restriction. If coordination is unavailable, the parent must preserve a blocked validation outcome.
* Historical deployed assets remain unavailable by design; no additional external research is requested.

## Limitations

* No source edits, dependency installation, heavy checks, browser execution, credential access, cloud calls, deployment, commit or push were performed.
* Supporting reads were restricted to the supplied evidence chain. The reported base and historical evidence are not independently reproduced validation results.
* This critique did not refetch web rules or assess changed web files; implementation and the subsequent independent Review retain those obligations.
* No second critique is required or authorized. The parent should dispose of this complete finding set directly and preserve this original outcome.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Reconcile permitted validation paths/shared-lock admission, then add the PC-002 and PC-003 browser acceptance assertions to the existing plan/details without expanding the test budget.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/employee-chat-cache-568-plan.md](.copilot-tracking/plans/2026-10-30/employee-chat-cache-568-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/employee-chat-cache-568-phase-details.md](.copilot-tracking/details/2026-10-30/employee-chat-cache-568-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-30/employee-chat-cache-568-research.md](.copilot-tracking/research/2026-10-30/employee-chat-cache-568-research.md) | Supplied bounded research evidence |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-chat-cache-568-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-chat-cache-568-plan-critique.md) | This original critique |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly,
record their dispositions and finalize without another critique. Proceed to
implementation only after planning corrections, respecting any remaining
validation blocker. No user action is required.
