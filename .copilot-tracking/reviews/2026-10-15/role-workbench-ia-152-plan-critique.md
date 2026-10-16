---
title: Role workbench IA 152 final-candidate plan critique
description: Independent implementation-readiness assessment of the bounded API shared-IA plan
ms.date: 2026-10-15
---

## Metadata

* Task ID: 152; slug: role-workbench-ia-152.
* Critique date: 2026-10-15.
* Branch inspected: feat/src-role-workbench-ia-152.
* Plan: .copilot-tracking/plans/2026-10-15/role-workbench-ia-152-plan.md.
* Phase details: .copilot-tracking/details/2026-10-15/role-workbench-ia-152-phase-details.md.
* Critique execution status: Complete.
* Execution boundary: exactly one independent final-candidate critique, not post-implementation Review. Only this critique artifact was written. Existing untracked planning/research/session artifacts were left untouched.

## Inputs and Criterion Boundary

* Caller direction controls: shared role-workbench IA/responsive layout only in src/api; no new client role gating, dependency-boundary changes, private data, owner-device decisions or fabricated evidence. Full RPI once and a PR with artifacts are delivery requirements, not authority to claim unavailable acceptance.
* Supplied research: .copilot-tracking/research/2026-10-15/role-workbench-ia-152-research.md, especially C1 to C10 and the accepted/deferred decision state.
* Requirements inspected: issue #152 body/comments retrieved read-only on 2026-10-15; docs/prds/zava-forward-retrofit-programme-demonstrator.md, SA-001/002/003/007, AC-034/043 and the Profile Journey/reset and read-only slice contracts.
* Named evidence inspected: docs/adrs/0006-src-layout-and-cutover.md; docs/architecture/mvp-to-src-parity-matrix.md; docs/reference/research/ux/zava-forward-prototype-profile-review.md; src/api/README.md; src/api/src/zava_forward/api/web/app.js, index.html and style.css; src/api/src/zava_forward/api/server.py; src/core/src/zava_forward/core/projection.py; src/core/tests/dataset.py; src/api/tests/test_role_matrix.py; src/api/checks/design_system_browser_check.py; src/api/pyproject.toml; .github/workflows/src-ci.yml.
* Repository context read: docs/case_study_48_original.md, relevant opening exercise-baseline sections of docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and the housing-association primer. Memory was context, not acceptance evidence.
* Dependencies and decisions considered: migrated src package placement; reuse of the existing Fluent/browser foundation; server-only authorization; preservation of permitted cross-team views; engineering widths distinct from supported devices; eight implemented roles distinct from eleven research perspectives; deferred workflow/device/human/live-platform acceptance.
* Assessment covers implementation readiness, concrete changed-flow edge cases, test credibility and delivery gates. It does not independently validate historical merged-PR results, run application tests, approve devices, expand role screens or establish live-service/human acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller API-only/dependency/privacy boundaries; C1/C5/C6 | Covered | API metadata using existing core policy is coherent; no new client permission map or store/schema change is needed. |
| SA-001/002; P01-T01 | Partial | Eight-role endpoint coverage is specified, but executable browser identities and observable expected navigation are not established by the named fixture; PC-002. |
| AC-034; C7/C8; P01-T02 | Partial | Defaults, debounce cancellation and reset focus are explicit; cross-render request lifetime, pending search and full originating-context behavior remain underspecified; PC-003. |
| SA-003/007; P01-T02/P02-T01 | Partial | Expanded early safety detail is appropriate. Presence checks alone do not prove unchanged control access/order or usable reflow; PC-005. |
| AC-043; C4/C9; P02-T01 | Partial | All eleven perspectives/nine workflows and explicit deferral are correct. The runnable role fixture and independent expected-result/applicability contract need definition; PC-002. |
| C3; P02-T01/P02-T02; test ownership | Partial | Typed reuse avoids a duplicate launcher, but its current scratch default conflicts with the task execution constraint; PC-004. |
| Widths, text enlargement, keyboard/current-page/status; P02-T01 | Partial | Width list is concrete; enlargement level, navigation checks and functional pass/fail oracles are incomplete; PC-005. |
| Src suites, lint/types, browser regressions; P02-T02 | Covered | Existing project tools, no widened exemptions and baseline/introduced-failure separation are appropriate. Execution is future work, not critique evidence. |
| Evidence boundaries and CI; P02-T03 | Partial | Offline/live distinction is sound elsewhere, but the CI SQL statement and new-check persistence are not supported by the named workflow; PC-006. |
| One Review and publication; P02-T03 | Partial | A single Review is authorized; unconditional future-work routing omits a delivery-blocking outcome for introduced failures; PC-001. |
| Owner-supported devices and complete issue acceptance | Covered as deferred | Current direction resolves scope: do not decide devices or claim full #152/PRD acceptance. No additional user decision is needed for this slice. |

## Verdict

* Verdict: Revise.
* Severity counts: 0 Critical, 3 High, 3 Medium, 0 Low.
* Rationale: The architecture and bounded scope are credible, but the candidate leaves material gaps in asynchronous recovery, runnable independent role/result oracles and the final delivery gate. These are direct planner corrections, not reasons to restart research, request owner-device choices or perform another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Single Review has no blocking disposition for introduced failures

* Related IDs: P02-T02, P02-T03; full RPI once; verified working delivery.
* Evidence: .copilot-tracking/details/2026-10-15/role-workbench-ia-152-phase-details.md, P02-T03 says "Review findings route to future work, not another implementation/review loop" and then instructs commit/push/PR. The plan does not distinguish known deferred acceptance from a newly introduced broken permission, reset, safety or layout invariant.
* Concern: Taken literally, the delivery sequence routes every discovered defect to future work and proceeds even when the bounded slice fails its own acceptance checks. One Review does not imply a passing outcome.
* Impact: An introduced defect can be published as implementation-ready merely to preserve stage count.
* Smallest useful change: Define final dispositions before implementation: pre-existing/out-of-scope limitations may remain explicit follow-up; introduced acceptance failures or unresolved High/Critical findings block readiness. Within the one-pass constraint, either finish the authorized implementation corrections and targeted validation before Review, or record a blocked/not-ready outcome after Review rather than claiming success. Do not mandate another critique or Review.
* Action owner: Planning parent; implementer and final reviewer apply the gate.
* Exact resolving evidence: Revised P02-T03 and matching plan acceptance language distinguish accepted deferrals from introduced blockers and specify the blocked/not-ready PR disposition. Eventual changes/Review/PR records must report actual checks and outstanding blockers without a false completed-slice claim.
* Decision route: Direct planner correction. No user decision is required; do not reinterpret the one-pass instruction as permission to waive failures.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The role/manifest checks lack an executable, independent fixture oracle

* Related IDs: P01-T01, P02-T01; AC-034/043; C3/C4/C9.
* Evidence: src/core/tests/dataset.py defines only Resident Liaison Officer and Retrofit Programme Manager identities. src/api/checks/design_system_browser_check.py synthetic_data preserves those two identities and makes its 505 cases from normal/waiting/hazard copies owned by the same officer. By contrast, src/api/tests/test_role_matrix.py build constructs all eight roles and a second contractor. Phase details require eight implemented role checks but say only to use the existing dataset and freeze expected own/default IDs/order before reset.
* Concern: The named browser fixture cannot by itself log in as all eight roles or distinguish own/all membership. A baseline copied from the UI or the same queried endpoint can freeze an already incorrect default. The JSON's eleven/nine declarations also need a check-to-fixture/expected-endpoint mapping to make applicability executable, rather than a count of labels.
* Impact: Role navigation, contractor projection, all-to-own reset and ordering can pass vacuously. A manifest may claim checked paths that no browser scenario exercises.
* Smallest useful change: Specify an API-check-owned constructed extension of the shared fixture, without modifying core or adding dependencies. Include the eight existing role identities, at least two different staff owners, assigned and unassigned/other-contractor cases, and an empty-own identity or equivalent separate scenario. Declare exact expected navigation routes and default IDs/count/order independently of the rendered result. Map each represented manifest check to its identity, fixture IDs and expected route/endpoint; explicitly mark non-applicable/deferred perspective/workflow/selection semantics without calling this the complete historical Slice A.
* Action owner: Planning parent; implementer authors the fixture and manifest within the existing API file budget.
* Exact resolving evidence: P02-T01 names the synthetic identities/ownership distinctions and independent expectation source. The versioned JSON and browser checks consume fixed expectations and fail on missing/extra/reordered cases, a forbidden/missing navigation item, and own/all leakage. Existing projection/endpoint denial tests remain unchanged; unknown-role denial is tested at the server boundary.
* Decision route: Direct planner correction. The caller already rejects invented auth roles and full cross-profile acceptance; no owner approval of synthetic identities is implied.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Recovery covers stored filters but not pending work or cross-render races

* Related IDs: P01-T02, P02-T01; AC-034; C7/C8.
* Evidence: src/api/src/zava_forward/api/web/app.js listView owns a local timer and seq; listState.q is updated only after the 250 ms timer. Each listView first awaits facets, show focuses main, and route dispatches asynchronous views without a shared lifetime guard. The candidate clears debounce on reset and tracks last queue scope, but does not define cancellation/invalidating outstanding loads when replacing a view or returning to it.
* Concern: Resetting or changing routes while facets/case data is delayed can allow an older render to replace the current screen or steal reset focus. Opening a case before search debounce fires can lose or later resurrect the visible query. "Last queue scope" alone does not define behavior for direct case entry, history Back/Forward, a case opened from Overview/Closed, or return from a paged queue.
* Impact: Users can see stale scope/counts, lose their origin, return to the wrong queue or lose the promised logical focus despite happy-path tests passing.
* Smallest useful change: Define a view-lifetime/request-generation or cancellation contract covering reset and route replacement, including stale success/error/401 behavior. Define when typed query becomes retained context and invalidate obsolete debounce callbacks. Specify originating queue scope plus filter/sort state, safe fallback for no queue origin, and explicit pagination/focus-return behavior; retaining loaded pages is optional, but dropping the originating row must not be silently described as full context restoration.
* Action owner: Planning parent; implementer owns the API web state changes.
* Exact resolving evidence: Revised P01-T02 states these behaviors. Deterministic browser tests hold and release existing API responses to check reset during outstanding load, type-then-open before debounce, delayed old view after navigation, mine/all return, direct case fallback and history navigation. A >50-result scenario proves the declared paging/return choice; final URL, heading, filters, count/order, focused element and status agree after old requests settle.
* Decision route: Direct planner correction. No new client authorization predicate or persistent/private context storage is needed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Launcher reuse needs an explicit worktree-local scratch location

* Related IDs: P02-T01, P02-T02; C3; task execution constraints.
* Evidence: src/api/checks/design_system_browser_check.py main uses tempfile.TemporaryDirectory(prefix="zf-design-system-") without dir. Phase details require reuse through typed callables but only explicitly locate the venv in the worktree.
* Concern: The default launcher normally writes synthetic JSON, state and server logs under the system temporary directory, which is forbidden for this execution. Calling the baseline unchanged is not compliant simply because its data is synthetic.
* Impact: Required browser validation is blocked or violates the task's file-operation boundary.
* Smallest useful change: During the already planned launcher refactor, make scratch allocation explicitly worktree-local and ignored, with owned cleanup on success/failure. Supply that location for both the existing baseline and the new callback. Keep the sanitized environment, health check and owned-process shutdown; do not duplicate server lifecycle code.
* Action owner: Planning parent; implementer edits only the existing API check and planned new API check.
* Exact resolving evidence: Details name the worktree-relative ignored scratch parent and cleanup behavior; the shared launcher passes an explicit permitted directory or receives it through a documented invocation setting. Changes evidence records both check commands, successful cleanup and no generated fixture/log files in the commit.
* Decision route: Direct planner correction. No owner or device decision is required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Responsive/accessibility checks need functional oracles beyond width and presence

* Related IDs: P01-T01/P01-T02, P02-T01; SA-001/002/003/007; NFR reflow/focus/status.
* Evidence: The candidate lists five widths, "enlarged text," safety markers/panel, focus and live status. It does not set a text enlargement factor/method or specify whether checks cover the new navigation, actual keyboard activation, current-route state, long content and safety control order. src/api/src/zava_forward/api/web/style.css has constrained grids/definition lists; the existing browser baseline checks Overview, not the changed queue/case recovery flows.
* Concern: A panel can exist while its controls are clipped, off-screen horizontally, incorrectly ordered or unreachable. A focus assertion after programmatic focus is not keyboard-flow evidence; a nonempty live-region attribute is not evidence that the restored scope/count is updated in a stable status region.
* Impact: Narrow or enlarged layouts can fail the actual task while the advertised engineering criteria pass.
* Smallest useful change: Define a compact role/view matrix: queue and hazard case at all five widths, plus representative long labels/source values and 200% text enlargement with the exact method recorded. Check no unintended page-level horizontal overflow or clipping, unchanged permitted safety controls before routine forms, keyboard skip/nav/reset/case/back activation, visible focus, and correct aria-current on supported destinations including case/deep links. Verify the persistent status region reports final scope/count or an explicit error. Apply contractor minimum projection rather than adding staff safety fields or controls.
* Action owner: Planning parent; implementer adds assertions in the planned API browser check.
* Exact resolving evidence: P02-T01 specifies views, roles, enlargement method and pass/fail assertions. Browser output identifies each width/view and enlargement run; assertions inspect dimensions and control visibility/order, exercise keyboard activation, and verify current navigation/status/focus after reset and return. Injected list-load failure and session expiry produce explicit recovery rather than stale success or an uncaught promise rejection. Human/screen-reader conformance remains unchecked.
* Decision route: Direct planner correction. These are engineering checks, not owner-supported-device commitments.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: The delivery plan overstates CI SQL evidence and leaves the new browser check disconnected

* Related IDs: P02-T02/P02-T03; C10; honest evidence and persistent regression coverage.
* Evidence: Phase details P02-T03 says "Rely on CI for image and live SQL evidence." The inspected .github/workflows/src-ci.yml builds images and runs project tests plus checks.design_system_browser_check; it does not itself establish a live SQL connection, identity or restart/durability result. It also does not invoke the proposed new browser-check module by name.
* Concern: A passing workflow does not prove that environment-dependent SQL tests executed rather than skipped, and the new browser assertions will not automatically become a CI regression gate merely by adding their file.
* Impact: PR evidence can imply unobserved live-platform success; the principal changed-flow tests may run only once locally and silently disappear from ongoing validation.
* Smallest useful change: Replace the live-SQL promise with actual run-dependent evidence: record unexecuted SQL/model/Azure checks as Not run/Blocked, and only claim a live result with its executed check/version evidence. Within src/api-only scope, define how the existing CI-invoked browser entry point also executes the new check through the shared launcher/callback, without breaking standalone baseline/new-check commands. If CI integration is deliberately deferred instead, state that limitation explicitly rather than promising CI coverage.
* Action owner: Planning parent; implementer owns the API entry-point wiring and evidence report.
* Exact resolving evidence: Revised P02-T03 no longer treats generic CI success as live SQL proof. The existing CI command reaches the new assertions through API-only wiring, with a local execution showing both check sets, or the plan/README/PR explicitly records the regression-coverage deferral. Any eventual live SQL claim cites a non-skipped run and its actual environment/result; otherwise its criterion stays unchecked.
* Decision route: Direct planner correction. Do not change workflow/dependency scope or request new deployment access to resolve this finding.

## Strengths and Residual Risk

* Navigation is presentation metadata, not authorization. Existing projection and Finance/manager checks remain authoritative; the API is the correct home for the new descriptor.
* The candidate explicitly preserves existing permitted cross-team views instead of silently narrowing rights to interpret "own queues." Clear scope labels and an own default are compatible with the caller's no-policy-change direction.
* Reset restores urgent sort and clears all-cases override, rather than only clearing visible inputs. Record invariance and expanded early safety detail are appropriate test targets.
* Existing native Fluent tokens, sanitized synthetic loopback launch, typed new Python, no new dependencies and unchanged existing tests are sound foundations.
* Owner device/browser support, full eleven-perspective/nine-workflow acceptance, assistive-technology/human validation and live SQL/model/Azure evidence are explicitly deferred. These are not newly invented blockers to this bounded slice.
* The issue must remain partial: engineering widths and declared deferrals do not satisfy all five unchanged issue criteria. Use Refs #152, not an unsupported closure claim.

## Questions or Blocking Evidence Gaps

* No significant/divergent user decision is required to resolve PC-001 to PC-006.
* The supplied evidence is sufficient to assess this candidate, so execution is Complete rather than Blocked. The verdict is Revise because implementation instructions and test oracles need correction.
* Do not reopen owner device choices, invent profile-to-auth-role equivalence or seek private/live data to fill synthetic test gaps.

## Limitations

* This is a source-grounded plan critique. No executable validation, deployment, live inference, SQL connection or human accessibility assessment was performed.
* References to code describe the inspected pre-implementation baseline, not observed regressions from an implementation that does not yet exist.
* Existing test fixtures' use of system temporary directories was read only; those tests were not executed by this critique.
* Historical merge/foundation claims in research were considered as supplied dependency context, not independently re-certified.
* No plan, detail, research, code, existing review or knowledge-base source was edited; no commit, delegation or PR operation was performed.

## Recommended Next Action

* Highest-impact finding: PC-001, missing delivery-blocking disposition.
* Action owner: Planning parent.
* Smallest next action: Revise the plan and matching phase details directly to resolve all six findings, beginning with the final delivery gate and independent synthetic fixture oracle. Record dispositions against PC IDs, then finalize without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/role-workbench-ia-152-plan.md](.copilot-tracking/plans/2026-10-15/role-workbench-ia-152-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-15/role-workbench-ia-152-phase-details.md](.copilot-tracking/details/2026-10-15/role-workbench-ia-152-phase-details.md) | Assessed task details and delivery instructions |
| [.copilot-tracking/research/2026-10-15/role-workbench-ia-152-research.md](.copilot-tracking/research/2026-10-15/role-workbench-ia-152-research.md) | Supplied research and evidence boundary |
| [.copilot-tracking/reviews/2026-10-15/role-workbench-ia-152-plan-critique.md](.copilot-tracking/reviews/2026-10-15/role-workbench-ia-152-plan-critique.md) | Complete independent critique; Revise |

## Next Steps

The active planning parent resolves PC-001 to PC-006 directly in the plan/details and records each disposition before implementation. No user action and no second critique are required. This critique stops here; it does not invoke implementation or post-implementation Review.
