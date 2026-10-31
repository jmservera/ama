---
title: Employee identity correction plan critique
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 570-correction
* Task slug: employee-identity-check-570-correction
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/employee-identity-check-570-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/employee-identity-check-570-correction-phase-details.md
* Critique execution status: Complete
* Execution count: Exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller direction: RV-002 before RV-001; merge latest main into the existing branch without rewriting history, select main's rubric and retain both append-only log entries; API unittest/Ruff/tools/test_rpi_checks.py validation; complete clean current-base gate; requested commit trailer, non-force push and main PR.
* Locked boundary: Only runner, owning API test module, API guide and dated evidence are implementation targets. No Azure changes, secrets, sign-in machinery or credential-handling addition. Pip only. Maximum three added test methods in src/api/tests/test_employee_acceptance_check.py, no removals.
* Evidence: Supplied correction research, plan and details; relevant original Review and changes; current runner/test/guide; map renderer and producer; documented gate and extra-selector contract.
* User-resolved residual: Independent expected identity is unavailable. Truthful partial publication using Refs #570 and explicit unmet live employee chat/map/case verification is authorized. This is not whole-issue acceptance.
* Assessment boundary: Implementation readiness and meaningful correction/validation/publication contracts. No implementation, new research, validation execution, credential access, approval request, repeated critique or delegation occurred.
* Dependency boundary: Original adverse Review remains immutable. One correction Review, candidate/evidence commit, complete current-base receipt and separate independent exact-head assessment precede publication. Hosted checks and owner merge remain separate.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner correction order; C1/C2; RV-002; P01-T01 | Partial | Explicit callback and blocked admission-loss design is credible; action-denial regression obligations need closure, PC-003. |
| C3/C4; RV-001; P01-T02 | Partial | Selected response and rendered projection are required, but refresh settlement and exact payload invariants remain underspecified, PC-001/PC-002. |
| P01-T03; main integration | Covered | Fetch/non-rewriting merge, main rubric, both log entries and integrated reruns are explicit. |
| Immutable identity and privacy contracts | Covered | BINDING unchanged; no optional email/roster authority; no new login/credentials; fixed capture-free output. |
| Test ownership and addition/removal bounds | Partial | Owning module and three-method/no-removal ceiling are locked; named coverage and explicit third Chromium selection are missing, PC-003. |
| P02-T01; independent Review and commit | Covered | Exactly one correction Review, original outcome preservation, GitHub-derived local noreply author/committer identity and trailer are explicit. |
| C5; P02-T02; clean current-base gate | Covered | Clean detached exact HEAD, fresh external output, full-scope verification, invalidation and no fallback are explicit. Actual prerequisites and receipts remain execution obligations. |
| RV-003 original publication history | Covered with qualification | Original changes record actual ignored-input and stale-base preflight failures and the parent's rejected historical compatibility assertion. No successful gate is inferred. |
| W1; RV-004; live criterion | Covered as accepted residual | No independent identity or live verification; Refs #570 and unmet criterion naming required, not issue closure. |
| Hosted/human approval | Covered | Local success is not hosted approval or permission to merge. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 0; Medium 3; Low 0.
* Rationale: The scope, correction order and owner decisions are credible. Before implementation, directly lock the map refresh/payload oracle and executable regression matrix. These are substantive contracts that prevent another false positive or unexecuted negative regression, not formatting preferences.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Filter correlation does not define which refresh has completed

* Related IDs: C3/C4, RV-001, P01-T02.
* Evidence: Phase details require correlation with selected filter query/origin and matching actual rendering. src/api/src/zava_forward/api/web/app.js, mapPanel.draw, increments seq, discards superseded draws and, after a fit response with bounds, calls draw(false) again. overviewView paints selection synchronously before draw(true). The original runner waits for the first matching /api/map response.
* Concern: Matching only the selected filter can capture an already pending response or the fit response rather than the subsequently rendered viewport refresh. A transient matching DOM snapshot is not necessarily the settled result; a later same-filter refresh can fail or replace it. The plan does not specify request initiation, zoom/bbox follow-up handling or when the page-error observation interval may safely end.
* Impact: Implementation can reject valid maps because the wrong response is compared, or accept a temporary render before a superseding response fails. This undermines the stated stale/error refusal contract.
* Smallest useful change: Define a bounded post-activation observation protocol: exclude pre-activation requests; match owned origin and actual selected flag/area; track relevant fit/viewport follow-ups; compare the payload that produced the settled current render. Define completion/error-event settlement without using cleared busy, selection paint or a fixed sleep as the oracle. Do not change app rendering.
* Action owner: Planning parent; implementer realizes the accepted protocol.
* Exact resolving evidence: Revised P01-T02 identifies the response-generation and completion rule, and requires actual Chromium subtests with a delayed pre-activation response and a same-filter bounds-triggered follow-up, covering valid replacement and failed/mismatched replacement. Tests assert fixed failed/passed outcomes and listener cleanup, without raw response/error output.
* Decision route: Direct planner correction. No divergent user decision or approval is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Strict payload and rendered matching lack mode-specific invariants

* Related IDs: C3/C4, RV-001, P01-T02.
* Evidence: Plan names total/mode/shown/items and renderer-required fields but gives no accepted types or relationships. src/core/src/zava_forward/core/insights.py, map_view, returns points/clusters with shown=len(items), mode-specific counts and bounds. src/api/src/zava_forward/api/web/app.js, renderList/draw, uses MAP_SIGNALS[p.kind], point IDs/names, cluster counts/hazards, coordinates and bounds for fitting.
* Concern: There is no exact schema/projection oracle for points, clusters or empty output. Missing or malformed bounds can fail after labels/markers have been built; unknown kind or invalid coordinates can throw; internally inconsistent shown/counts can still look plausible. Conversely, a generic total==shown requirement would incorrectly reject clusters.
* Impact: The advertised strict validation can preserve false acceptance or introduce false failures on supported modes. The existing ordinary rosterless fixture does not guarantee cluster or empty coverage.
* Smallest useful change: Specify supported mode and exact numeric/string/list types, rejecting booleans as numeric values and non-finite coordinates. Define shown/items equality, point total/items equality, cluster positive counts and aggregate total/hazard consistency, allowed signal kinds, usable point IDs/names, and renderer-used bounds shape/order. Define actual list labels/links, marker labels/counts and status per mode; valid empty points require zero list entries/markers and the successful zero-home status. Validate required fields without unnecessarily rejecting producer metadata.
* Action owner: Planning parent, with implementation in the existing runner/test module.
* Exact resolving evidence: Revised P01-T02 contains the mode-specific invariants derived from the cited producer/renderer and assigns actual Chromium subtests for valid points, forced synthetic clusters and empty points, plus missing items, unknown kind, invalid coordinates/bounds and inconsistent counts. Assertions compare the rendered projection, not just HTTP 200 or selected/focused state.
* Decision route: Direct planner correction. Public synthetic routing is already authorized; no dataset, renderer or policy expansion is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Regression matrix and complete-gate selectors are not executable yet

* Related IDs: RV-002, RV-001, P01-T01/P01-T02/P01-T03, P02-T02, Test Ownership and Locked Boundaries.
* Evidence: Details specify navigation-denial subtests for map/case, while Functional Requirements also guard offered controls including chat sending. src/api/checks/employee_acceptance_check.py, chat, waits for skill availability and fills/sends before its outer post-probe; verify_employee currently catches browser/value failures as failed. The owning module has six methods and two Chromium methods. Plan requires all three Chromium selectors without naming the third. tools/rpi-checks.py, extra_selector/--extra-test, requires explicit reviewed PROJECT:test_module[.Class.method] selectors.
* Concern: No regression is assigned to admission loss during chat readiness before draft/send, or to the dedicated admission-loss exception's blocked/capture-free reducer behavior. Updating the callback signature also affects existing patched observers. The plan's test ceiling is feasible, but without a concrete allocation and selector list an implementer can omit meaningful coverage or keep the existing two-test CLI/gate and never explicitly execute the new browser negatives.
* Impact: Navigation fixes may pass while a later offered-control action still runs after denied admission. A passing gate may not supply explicit executed evidence for the correction's actual Chromium negatives.
* Smallest useful change: Allocate at most three added methods with composed subtests: navigation/action admission refusal, actual Chromium map render contract, and any remaining reducer/privacy contracts. Within that allocation require origin/identity loss at overview, all-list and second case-link boundaries; chat admission loss after readiness and before fill/send; zero next actions; blocked current/later stages; no exception/canary output. Update existing mock observer signatures in place without removing tests. Name the new browser method and the exact CLI/gate selectors.
* Action owner: Planning parent; implementer maintains existing test ownership.
* Exact resolving evidence: Revised details enumerate method allocation and outcomes; CLI/full gate explicitly execute api:test_employee_acceptance_check.AcceptanceTests.test_chromium_rosterless, api:test_employee_acceptance_check.AcceptanceTests.test_chromium_wrong_account and the named new Chromium contract method using --extra-test. Integrated logs and final receipt later prove execution with zero unexpected skips. Final diff proves no methods removed and at most three added.
* Decision route: Direct planner correction. The user already selected the owning module, ceiling and full gate.

## Strengths and Residual Risk

* Explicit RV-002 then RV-001 order, callback admission capability and dedicated blocked exception target the actual original defects without changing identity authority.
* Correlated data/render observation and page-error refusal are stronger than the original HTTP/pressed/not-busy predicate; the findings complete that direction rather than replace it.
* Non-rewriting main integration, main rubric selection and append-only log preservation follow confirmed owner direction.
* Original Review/failed gate attempts remain historical evidence. No passing correction Review, receipt or hosted result exists yet.
* Caller-owned watchdog/lifecycle and non-atomic session probing are accepted boundaries, not reasons to add credential/sign-in machinery.
* Live employee verification remains an explicitly accepted unmet criterion. Independent identity administrator provenance is a future live-lane prerequisite, not a blocker to the permitted partial publication after all correction/publication gates pass.

## Questions or Blocking Evidence Gaps

* No decision-critical user question remains. All three findings are compatible with the selected scope and can be resolved directly by the planning parent.
* Actual full-gate prerequisite availability, current main at execution time, passing correction Review and exact-head receipt/assessment are intentionally not established by this critique. Failure of any required publication gate blocks push/PR; it does not authorize weakening the gate.

## Limitations

* Only supplied artifacts and necessary original Review/source were read. Research W1 was treated as a supplied issue-evidence pointer; no new issue/web/directory research occurred.
* No tests, browser, merge, gate, commit or push were performed. Readiness findings describe planned contracts, not observed correction defects.
* Historical host-compatibility assertions and their parent's rejection remain preserved. This critique does not establish a compatible execution environment or permission to bypass applicable file-operation restrictions.
* Only this critique artifact was written; research, plan, details, state, originals and source remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001, settled map refresh correlation.
* Action owner: Planning parent.
* Smallest next action: Amend P01-T02 with the response-generation/settlement contract, mode-specific oracle and bounded test allocation, then reconcile P01-T01 and P02-T02 with PC-003.
* User response required: No.
* Handoff: Apply all compatible dispositions directly once and continue the active parent's implementation sequence; do not repeat this critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/employee-identity-check-570-correction-research.md](../../../research/2026-10-31/employee-identity-check-570-correction-research.md) | Supplied bounded correction research. |
| [.copilot-tracking/plans/2026-10-31/employee-identity-check-570-correction-plan.md](../../../plans/2026-10-31/employee-identity-check-570-correction-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-31/employee-identity-check-570-correction-phase-details.md](../../../details/2026-10-31/employee-identity-check-570-correction-phase-details.md) | Assessed phase contracts. |
| [.copilot-tracking/reviews/logs/2026-10-31/employee-identity-check-570-review.md](../../logs/2026-10-31/employee-identity-check-570-review.md) | Immutable original adverse Review. |
| [.copilot-tracking/changes/2026-10-31/employee-identity-check-570-changes.md](../../../changes/2026-10-31/employee-identity-check-570-changes.md) | Original dispositions and actual failed gate evidence. |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-identity-check-570-correction-plan-critique.md](employee-identity-check-570-correction-plan-critique.md) | This complete independent critique. |

## Next Steps

Active planning parent resolves PC-001 through PC-003 directly and finalizes the plan without another critique, then continues RV-002 before RV-001 implementation and the already selected validation/publication gates. No user action is required.
