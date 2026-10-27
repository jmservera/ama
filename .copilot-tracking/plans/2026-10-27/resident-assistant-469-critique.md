---
title: Resident assistant 469 final-candidate plan critique
description: Independent bounded implementation-readiness assessment
ms.date: 2026-10-27
---

## Metadata

* Task ID: #469, parent #466.
* Critique date: 2026-10-27.
* Plan: .copilot-tracking/plans/2026-10-27/resident-assistant-469-plan.md.
* Phase details: .copilot-tracking/details/2026-10-27/resident-assistant-469-phase-details.md.
* Critique execution status: Complete.
* This is the single independent final-candidate critique. Sources remain unchanged.

## Inputs and Criterion Boundary

* Assessed the supplied research, plan and phase details against the owner's full ordered RPI direction, local rules prototype, configurable but disabled real provider, USD 5 additional ceiling through 2026-10-31, and prohibition on external model calls, Azure operations, private data, secrets, .env and verifier access.
* Assessed P01-T01, P02-T01/T02 and P03-T01/T02, including the independent panel, own-case authorization, advisory boundaries, budget activation caveats and acceptance coverage.
* Inspected supplied integration paths: src/api/src/zava_forward/api/resident_demo/app.py; src/api/src/zava_forward/api/resident_demo/web/demo.js and index.html; src/core/src/zava_forward/core/resident_showcase.py and resident_preview.py; src/api/tests/test_resident_demo_api.py; src/api/checks/resident_demo_browser_check.py; component pyproject.toml files; and src/README.md.
* Read the required case-study and knowledge-base context and the relevant content standard. These do not establish live resident-service approval.
* Branch inspection found feat/resident-assistant with existing untracked RPI artifacts. No source changes, branch changes, commits or remote writes were made. Stacking on feat/resident-interactive, Refs #469 only, sibling isolation and no merge/force push remain requirements, not verified remote lifecycle facts.
* Boundary: implementation readiness of this local prototype, not real-provider activation, regulatory acceptance, production identity, screen-reader acceptance or whole-issue completion. No open-ended research, external retrieval, tests or model calls were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI and independent critique | Covered | Research is supplied; this critique precedes implementation; P03-T02 requires independent post-implementation Review and preserved findings. |
| Local rules and separate panel, P01-T01/P02-T02 | Covered | Three explicit topics, native controls, scoped CSS and one integration call avoid a sibling-panel redesign. |
| Own-case access, C1/C3, P02-T01/P03-T01 | Covered | view_for verifies the session, fetches one current row and rechecks admission. Planned POST reuses origin, CSRF and body-size checks and excludes case selectors. |
| Grounding and advisory scope, C2, P01-T01 | Covered | Existing status mappings, explicit unknown documents, closed/unknown-state tests and generic form help avoid invented document requests or action authority. |
| Provider isolation, P01-T01/P02-T01 | Covered | Enum-only input/output, no resident view or free text in prompts, local rendering, generic errors, disabled default and no environment discovery are appropriate. |
| Provider cost boundary, P02-T01/P03-T01 | Partial | Budget reservation and expiry precede credentials, but model token ceilings and their reservation relationship need PC-002. |
| Targeted verification, P03-T01 | Covered | Core/API suites, changed Python lint/types, JS syntax and a new fake-reader browser check cover the bounded change without SQL or actual model transport. |
| Publication, P03-T02 | Partial | Targeted checks are valid development evidence but cannot replace the mandatory publication receipt; see PC-001. |
| Accessibility and manual routes, P02-T02/P03-T01 | Covered within boundary | Labels, native keyboard behavior, live feedback, focus, 320px reflow and manual help are planned. Chromium is explicitly not screen-reader/user acceptance. |
| USD 5 and activation decision | Covered with PC-002 caveat | USD 4 inference allocation plus USD 1 headroom, expiry at 2026-11-01 UTC, unverified tariffs and future durable shared accounting are appropriately distinguished from current USD 0 operation. |

## Verdict

* Verdict: Revise.
* The deterministic prototype and isolation approach are credible. Two direct planner corrections are needed before implementation handoff: preserve the publication boundary while honoring the no-long-gate instruction, and specify a mock-testable cost envelope for the optional adapter.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Targeted checks are incorrectly authorized to replace the publication gate

* Related IDs: Executive Summary; P03-T02; targeted-check acceptance criterion.
* Evidence: The plan says targeted checks "replace the long gate"; P03-T02 says the owner's scope replaces the full gate and then directs push and stacked PR creation. src/README.md:48-109 explicitly distinguishes development checks from the complete pre-push gate and requires an external exact-candidate receipt, fresh-base verification and independent exact-head assessment.
* Concern: Disclosing that the full gate was not run does not satisfy the publication prerequisite. The owner's explicit no-long-gate instruction must be honored without converting targeted success into publication authorization.
* Impact: Following P03-T02 as written would publish a candidate that lacks required publication evidence, even if every targeted check passes.
* Smallest useful change: Keep implementation, targeted validation and the independent Review in scope. Replace the unconditional push/PR step with an explicit publication hold when the required gate/receipt is absent. Prepare the stacked PR description locally, retaining feat/resident-interactive, Refs #469 and the parent dependency. Do not execute the long gate in this scope and do not claim a waiver or substitute gate.
* Action owner: Planning parent.
* Exact resolving evidence: Revised plan and P03-T02 consistently separate targeted engineering checks from publication eligibility; their completion condition records "publication blocked: complete local gate and current exact-head receipt not run/available" rather than push/PR completion. Subsequent changes/Review evidence must preserve that status unless the actual prerequisite is later satisfied under an authorized scope.
* Decision route: Direct planner correction. No user response is required to stop before an unmet publication prerequisite. Any later expansion to run the gate is outside this critique's requested execution scope.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The optional provider lacks an explicit model-token and reservation contract

* Related IDs: Research Q4/design note; P02-T01; P03-T01 provider tests; budget acceptance criterion.
* Evidence: Research requires a conservative per-call reservation covering bounded tokens at verified rates. P02-T01 specifies a bounded reply read, timeout and no retries, but does not specify a model-side output-token ceiling, bounded serialized prompt, or how the reservation callback is tied to those limits.
* Concern: A response byte limit protects local parsing, not billed generation. A timeout likewise does not prove that the provider stopped processing. Without a fixed request token envelope, an implementation can call the reservation callback successfully while requesting generation outside the assumed reserved cost.
* Impact: The disabled prototype still spends USD 0, but its purported future budget boundary would not be a sufficiently specified, testable adapter contract.
* Smallest useful change: Define the fixed enum-only request envelope and an explicit provider-supported output-token limit in P02-T01. Define reservation success as reserving a conservative upper-bound cost for that exact bounded request under a separately reviewed tariff. Failed or ambiguous attempts must retain their reservation unless reconciled by the future durable accounting owner; no automatic refund/retry. Keep tariff verification and durable global USD 4 enforcement as activation prerequisites, not new live work.
* Action owner: Planning parent, then implementer of the adapter/provider tests.
* Exact resolving evidence: Revised P02-T01 and P03-T01 require fake-transport tests asserting the outbound output-token limit, bounded prompt and reserve-before-token/transport order; refused reservation causes zero token/transport calls; failed/timeout attempts do not release their reservation. The design note explicitly says no numeric affordability claim or activation is established without verified tariff/model support and durable aggregate accounting through expiry.
* Decision route: Direct planner correction. No model selection, live price lookup, durable service implementation or additional budget approval is required now.

## Strengths and Residual Risk

* Fixed-topic help is a reasonable local prototype, not a disguised conversational model. Exact topic equality and local response composition remove generated prose from the resident-facing trust boundary.
* Existing showcase_view is a positive allowlist but includes address and measures. The proposed narrower core contract must continue receiving only the approved status/next-step/closed information, not the whole view, reader or identifiers.
* Document requests remain unknown because the current projection has no requested-document facts. Do not convert that limitation into "no documents required".
* The new browser check correctly uses constructed rows rather than the existing SQL-backed browser runner, which requires SQL credentials. Mock-only provider testing must remain separate from any activation.
* Model/deployment availability, verified tariff, credential composition, processing/privacy evidence and durable shared accounting remain future owner-gated decisions. A configurable adapter is not permission to wire or enable it.
* The pending-response connectivity safeguard should be exercised with delayed replies across sign-out and a different resident's subsequent render. This is resolving verification of the already planned stale-response behavior, not an additional feature requirement.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents local implementation after the two direct corrections.
* The research's final repeated "Pending research" paragraph is inconsistent with its executed/Ready disposition. Treat it as stale wording, not evidence that any model or credential route is approved; the before-implementation design note must state the actual local-only decision unambiguously.

## Limitations

* Assessment is read-only except for this critique artifact. No implementation behavior, check results, remote branch ancestry, prices or live provider capability were verified.
* The attempted generic test-file lookup did not exist; assessment used the actual src/api/tests/test_resident_demo_api.py.
* No fresh web-guideline or accessibility conformance review was performed. This critique did not edit or review changed web implementation files.
* The mandatory publication gate was inspected as policy only and was not executed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Apply both direct corrections to the plan/details and record disposition of this original critique. Finalize without another critique, then continue the ordered local implementation and independent Review with publication held as necessary.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/resident-assistant-469-research.md](.copilot-tracking/research/2026-10-27/resident-assistant-469-research.md) | Supplied research and activation caveats |
| [.copilot-tracking/plans/2026-10-27/resident-assistant-469-plan.md](.copilot-tracking/plans/2026-10-27/resident-assistant-469-plan.md) | Final-candidate implementation plan |
| [.copilot-tracking/details/2026-10-27/resident-assistant-469-phase-details.md](.copilot-tracking/details/2026-10-27/resident-assistant-469-phase-details.md) | Task contracts and completion evidence |
| [.copilot-tracking/plans/2026-10-27/resident-assistant-469-critique.md](.copilot-tracking/plans/2026-10-27/resident-assistant-469-critique.md) | This single independent finding set |

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly, preserve this critique unchanged and finalize the plan without another critique pass. No user action is required. This critic stops here; it does not implement, run the long gate or publish.


## PR 474 P04 final-candidate critique addendum (2026-10-27, Refs #466)

* Execution: Complete. Verdict: Pass. Findings: none (Critical/High/Medium/Low: 0).
* Inputs/boundary: only the PR474 P04 addenda in
  .copilot-tracking/plans/2026-10-27/resident-assistant-469-plan.md,
  .copilot-tracking/details/2026-10-27/resident-assistant-469-phase-details.md,
  and .copilot-tracking/research/2026-10-27/resident-assistant-469-research.md,
  assessed once against the supplied owner requirements. This assesses planning
  credibility, not implementation or test results.
* Coverage: P04-T01 covers native Account closed/open visibility before Sign out;
  P04-T02 covers reserve OSError normalization inside the existing try, before
  token/transport, with callback isolation and generic HTTP 503; P04-T03 covers
  native focused submit through success and both failure types, duplicate busy
  guards, and no focus stealing after interaction/logout. Existing tests retain
  their assertions, with no new files and at most one added provider/API method.
* P04-T04 covers full API discovery, available Chromium checks with honest
  prerequisite reporting, independent Review, pull --no-rebase before commit/push,
  and existing-branch publication. Owner exclusions (full gate, Azure, secrets,
  force push) and Refs #466-only scope remain settled, not reopened. Original
  evidence and unrelated gate records remain untouched.
* Limitations/residual risk: no source review or tests performed; runtime focus,
  error normalization and browser availability remain implementation/Review
  evidence obligations. No actionable planning gaps or user decisions identified.

## Next Steps

Planning parent may proceed with the bounded correction and independent Review.
Highest-impact finding: none; disposition needs: none; user response: not required.
