---
title: Resident chat logout follow-up final-candidate plan critique
ms.date: 2026-10-28
---

## Metadata

* Task ID: 520-logout-followup.
* Critique date: 2026-10-28.
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-logout-followup-plan.md.
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-520-logout-followup-phase-details.md.
* Critique execution status: Complete.
* Execution: exactly one independent final-candidate assessment. No tests,
  browser, heavy checks, agents, remote mutations or implementation edits.

## Inputs and Criterion Boundary

* Caller requirements: fix RV-002 first; establish actual corrected all-five
  Chromium/pinned-axe evidence; use bounded nonblocking shared-lock admission
  every 60 seconds for at most 60 minutes; run owning units, Ruff100, mypy and
  permitted gate operations. Preserve the existing-method budget, original
  adverse evidence, normal publication and five verified-thread boundaries.
* Supplied evidence: the named plan, phase details and research, plus
  .copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md.
* Source considered: src/api/src/zava_forward/api/resident_demo/app.py;
  src/api/src/zava_forward/api/resident_demo/web/demo.js;
  src/api/checks/resident_assistant_browser_check.py;
  src/api/tests/test_resident_demo_api.py;
  src/core/src/zava_forward/core/resident_showcase.py;
  tools/rpi-checks.py; src/README.md. Required case-study and reference
  orientation was read; no regulatory or whole-product audit was undertaken.
* Decisions and dependencies: response-side-effect removal rather than a new
  cookie scheme; P01 before browser validation; validation before the child's
  original Review; commit before exact-head publication checks. No az,
  deployment, merge, secret, .env or private-data access is authorized.
* Assessment boundary: planning credibility and necessary unchanged source,
  not fresh implementation acceptance. Future passing results, remote bot
  ancestry and thread verification are not assumed. No lock-path operation
  was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-002; C1/C2/C4; P01-T01 | Covered | Remove both logout cookie writes; retain request admission and revoke the bound token. Existing logout method owns header/replay/session assertions. |
| Revoked-cookie lifetime and ordinary sign-out | Covered | Codec denies revoked sid through the token's remaining life. demo.js rechecks /session and retains ordinary confirmation/focus coverage. |
| Same/different resident replacement; P01-T02 | Partial | Both identities, fresh sid/permission and protected state are specified, but the upstream-fetch cookie-isolation premise is unsupported, PC-001. |
| RV-001; C3; P02-T01 | Covered | All five named scenarios, retained times=1 synchronization, real Chromium, hash-checked axe and bounded lock admission are required. No historical pass substitutes. |
| Units, Ruff100, mypy, JS; P02-T02 | Covered | Actual results and explicit failures/skips are required; no new tests or removed methods are authorized. |
| Non-az gate boundary; C5; P02/P03 | Covered | Mandatory az preflight prevents a canonical full receipt. Partial command evidence cannot authorize publication. |
| Original Review and immutable evidence; P03-T01 | Covered | One distinct child Review, no repetition or rewriting of the parent's Not accepted result. |
| Commit, ancestry and publication; P03-T02/T03 | Partial | Identity, trailer and conditional bot rebase are bounded, but exact-head assessment is ordered after push and the final current-main verification sequence is incomplete, PC-002. |
| Five verified replies/resolutions; P03-T03 | Covered | Only actually fixed/verified threads may be resolved after publication prerequisites; no closing keyword or hosted/human approval claim. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 0 High, 2 Medium, 0 Low.
* Rationale: the root-cause solution is credible and narrowly scoped. Two
  direct planning corrections are needed: establish the browser-cookie hold
  boundary rather than asserting route.fetch isolation, and place exact-head
  publication assessment before remote publication. The separately acknowledged
  no-az/full-receipt blocker is not a request to weaken or bypass the gate.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: The delayed-cookie regression assumes an unproven isolation boundary

* Related IDs: RV-002, C3, P01-T02, P02-T01; delayed replacement-login acceptance.
* Evidence:
  .copilot-tracking/details/2026-10-28/resident-chat-520-logout-followup-phase-details.md,
  P01-T02 explicitly says "Playwright route.fetch does not automatically apply
  Set-Cookie." Existing
  src/api/checks/resident_assistant_browser_check.py:45-47 uses route.fetch
  before route.fulfill, but contains no assertion about cookie-store state at
  that boundary. Existing held session/view checks establish response/UI
  scheduling, not upstream-fetch cookie isolation. The supplied research does
  not establish the installed Playwright transport's cookie behavior.
* Concern: holding route fulfillment alone is not evidence that the upstream
  fetch cannot mutate the shared browser cookie store. route.fetch is not an
  explicitly isolated request context. If deletion headers take effect during
  upstream fetching, the planned ordering does not hold the defect's side
  effect until after replacement login. A no-Set-Cookie assertion can still
  detect the old server implementation, but does not independently establish
  the required actual-browser response-application ordering.
* Impact: the required browser regression could claim the delayed-cookie
  race is reproduced without establishing its defining acceptance boundary.
* Smallest useful change: replace the unconditional transport claim with an
  explicit cookie-isolation and verification contract inside the existing
  shared_session_checks method. Obtain the accepted old logout through an
  upstream transport whose response cannot update the shared browser store,
  forwarding the original bound request cookies/headers. Preserve the actual
  response headers/body when releasing to Chromium. Assert cookie state at
  upstream acceptance, immediately before release after replacement login,
  and after release/recovery. Establish that destructive Set-Cookie headers
  would reach Chromium on release, using supported runtime-source evidence
  or a bounded control within the existing method, not a separate harness.
* Action owner: planning parent; implementation/validation owner executes the
  amended contract in the existing browser method.
* Exact resolving evidence: amended P01-T02 identifies the isolated upstream
  transport and intermediate cookie assertions; actual same-resident and
  different-resident Chromium results show accepted old-token revocation,
  fresh replacement sid and renewed permission, preserved replacement
  authentication/CSRF values and required attributes, own protected view and
  transcript after release, and old-token replay denial. Distinguish auth
  cookie expiry preservation from permitted CSRF expiry refresh during
  /session recovery. Retain the successful-response no-Set-Cookie assertion.
* Decision route: direct planner correction. No new runtime design, dependency,
  test method, removed coverage or user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Conditional publication orders exact-head assessment after push

* Related IDs: P03-T02/P03-T03; current-main exact-head publication evidence.
* Evidence:
  .copilot-tracking/plans/2026-10-28/resident-chat-520-logout-followup-plan.md
  P03-T03 says "normal push; independently assess exact head"; matching phase
  details say "normal push and one exact-head assessment." src/README.md,
  Local RPI gate, requires fetching main again and verifying the external
  receipt immediately before independent exact-head review and push.
  The parent original Review's RV-001 also places exact-head assessment before
  normal push. P03-T02 says fetch remote but does not explicitly restore this
  final current-origin/main verification sequence.
* Concern: the conditional success path permits publication before independent
  assessment of its committed head, and leaves the final main refresh/receipt
  verification implicit. The earlier uncommitted original Review cannot
  substitute for assessment after a bot rebase or other candidate change.
* Impact: if publication later becomes eligible, a changed head/base could be
  pushed without the required current exact-head evidence.
* Smallest useful change: make the conditional sequence explicit: commit
  implementation/original evidence, fetch and perform only an authorized
  necessary bot rebase, establish eligible exact-head evidence, fetch main
  again, verify the external full receipt against current origin/main, obtain
  independent exact-head assessment, then normal push and verified replies/
  resolutions. Any head/base/input change invalidates prior gate evidence.
* Action owner: planning parent, then publication owner.
* Exact resolving evidence: P03-T02/T03 and dependencies consistently place
  current-base receipt verification and independent exact-head assessment
  before push. Under the present no-az direction, they explicitly stop at
  blocked publication because tools/rpi-checks.py:1322-1334 always invokes
  az bicep version in preflight. Non-az command logs remain partial evidence;
  no fabricated receipt, preflight suppression, runner modification or
  protection change is an eligible resolution.
* Decision route: direct planner correction to sequencing. No user response
  is needed to preserve the existing no-az prohibition and blocked outcome.

## Strengths and Residual Risk

* Removing logout's Set-Cookie tuple eliminates the shared response-side
  effect, rather than trying to fence cookie processing with JavaScript.
  Same-origin, CSRF, strict sid admission and old-token revocation remain.
* Retaining a revoked HttpOnly token is consistent with the codec:
  src/core/src/zava_forward/core/resident_showcase.py:423-455 rejects its sid
  until after the token's maximum remaining lifetime. Retaining cookie bytes
  does not retain authenticated access. No session lifetime extension or new
  cookie scheme is needed.
* Existing demo.js:350-369,405-422 clears local personal state and rechecks the
  actual shared session after successful logout. Ordinary sign-out remains
  distinct from recovery into another tab's valid replacement login.
* The existing HTTP logout method currently expects cookie removal; the plan
  intentionally replaces that expectation with no response cookie writes and
  denial of the retained/replayed token. Existing expiry, CSRF and binding
  regressions remain, without new methods or removals.
* The all-five browser requirement and bounded admission timeout are honest
  evidence gates, not permission to bypass contention. Human/resident, actual
  assistive-technology/native zoom, real-model and hosted approval remain
  separate.
* Full publication is currently blocked by the explicit no-az direction and
  mandatory canonical preflight. This accepted execution limitation is not a
  reason to redesign logout or manufacture a complete-gate success.

## Questions or Blocking Evidence Gaps

* No unresolved user decision is needed for either correction.
* Actual browser/check outcomes remain implementation-time evidence gaps.
  The full-receipt publication prerequisite is unavailable under the present
  prohibition; stop publication rather than silently downgrade it.

## Limitations

* Read-only source assessment apart from this critique artifact. No tests,
  runtime cookie experiment, dependency-source inspection, lock admission,
  gate execution, network research or remote thread inspection was performed.
* PC-001 identifies the unsupported transport premise and missing cookie
  boundary proof; it does not claim a fresh Playwright reproduction.
* This is one complete finding set for the supplied boundary. No cosmetic
  findings, broad redesign or second critique is prescribed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly revise the existing browser regression's
  upstream cookie-isolation contract and the conditional publication ordering,
  then continue the authorized child implementation without another critique.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/resident-chat-520-logout-followup-plan.md](.copilot-tracking/plans/2026-10-28/resident-chat-520-logout-followup-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-28/resident-chat-520-logout-followup-phase-details.md](.copilot-tracking/details/2026-10-28/resident-chat-520-logout-followup-phase-details.md) | Assessed execution contracts |
| [.copilot-tracking/research/2026-10-28/resident-chat-520-logout-followup-research.md](.copilot-tracking/research/2026-10-28/resident-chat-520-logout-followup-research.md) | Supplied focused research |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review-correction-review.md) | Preserved original adverse parent Review |
| [.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-logout-followup-critique.md](.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-logout-followup-critique.md) | This single independent critique |

## Next Steps

Active planning parent: resolve PC-001 and PC-002 directly, preserve the
original assessment outcomes and finalize without another critique. Continue
bounded implementation/validation only; publication and thread resolutions
remain blocked without an eligible full receipt. No user action is required.
