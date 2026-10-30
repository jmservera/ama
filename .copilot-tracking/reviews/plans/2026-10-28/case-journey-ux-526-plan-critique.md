---
title: Case journey UX 526 final-candidate plan critique
description: Independent single-pass assessment of the supplied implementation candidate
ms.date: 2026-10-28
---

## Metadata

* Task ID: 526
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/case-journey-ux-526-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/case-journey-ux-526-phase-details.md
* Critique execution status: Complete
* Assessment: exactly one independent final-candidate plan critique. This is the original verdict, not a post-disposition reassessment.

## Inputs and Criterion Boundary

* Caller requirements: employee six-step journey, six-value summary, nine retained tabs, fixed slide order, recorded funding/resident-decision evidence, AI presentation consistent with existing authority, native Fluent stack in src/api, synthetic local validation, full ordered RPI loop and a topic PR with Refs #526. Live and screen-reader acceptance remain pending the owner.
* Supplied evidence: both planning inputs, .copilot-tracking/research/2026-10-28/case-journey-ux-526-research.md and docs/reference/research/ux/employee-case-workspace-redesign.md.
* Context read: docs/case_study_48_original.md, the opening scope/authority sections of docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and the scoped WCAG baseline. Memory was context, not evidence.
* Scoped read-only code evidence: case rendering, routing, aiNotes, assistant cards/loaders, chat, challenge draft/history routing, existing assistant and employee browser checks, AI review authority, assistant listing and local gate locking.
* Decisions treated as settled: keep slide order and nine tabs; no new journey/confidence API; chat turns are advisory and use the existing separate proposal route, not invented recorded acceptance; no framework or authority expansion. None of these requires another owner decision.
* Assessment covers requirements, derivation, tasks/dependencies, retained state, authority, acceptance criteria, test ownership/change budget, regression compatibility and publication sequence. It assesses planning credibility, not implementation correctness, accessibility conformance or operational approval.
* Existing dirty inputs were inspected only. The supplied plan, details, research, specification and session state were not changed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Six ordered steps; P01-T01 | Covered | One map, Python STAGE_ORDER parity, closed and unknown states, current/blocked combination and blocker fallback are specified. Unknown stage intentionally does not invent a current step. |
| Funding/resident evidence; P01-T01 | Covered | Plan and details explicitly reject positional completion without recorded confirmation. |
| Six summary values; P01-T01/P02-T01 | Partial | Unknown owner, handoff and overdue coverage are present; AI state vocabulary, pagination and local-draft count ownership need PC-002. |
| Nine tabs, deep links, native manual activation; P01-T02 | Covered | Retained nodes, other query parameters, refresh/back, invalid tabs, focus and manual keys are specified. |
| Unsaved text and refresh; P01-T02 | Partial | PC-001: copying dirty fields does not recreate generated drafts, review context or their closures. |
| Safety, retained actions and role boundary; P01/P02 | Covered | One live open-hazard panel above all tabs; unchanged server authority and manual actions. Enhancement-failure coverage needs PC-004. |
| AI label/sources/confidence/reasons; P02-T01 | Covered | Existing draft and assistant endpoints, person-specific verification, revision checks, linked errors and disabled acceptance are retained. Chat's missing review endpoint is explicitly disclosed, not fabricated. |
| Test ownership, no removals and change budget; P03-T01 | Partial | Ownership and budgets are defined, not absent. PC-003 identifies a concrete incompatibility in the navigation-only adaptation restriction. |
| Acceptance criteria 1-8 and browser validation; P03 | Partial | Unit, browser/axe, keyboard, 200% and synthetic real-server checks are committed to. PC-005 makes the remaining geometry/state pass conditions executable. |
| Independent Review, committed original evidence and full local gate; P03-T02 | Covered | Correct high-level order, clean candidate, external exact-head receipt, fresh base, non-force push and no weakening of failure are specified. Research explicitly says not to double-lock the gate. |
| Knowledge-base integration and topic PR | Covered | Include supplied specification, update index, append log, reproduction documentation and Refs #526; human/live gaps remain explicit. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 4 Medium, 0 Low.
* Rationale: the selected architecture and authority boundaries are credible, but the candidate leaves concrete draft-loss and summary-count risks unresolved and contains a test adaptation constraint that conflicts with its own UI changes. These are bounded planner corrections, not reasons to reopen the owner's design decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Refresh preservation does not account for generated draft nodes and review context

* Related IDs: P01-T02, P02-T01; design Tabs refresh rule and acceptance criteria 4-6.
* Evidence: phase details P01-T02 says to capture dirty fields/details on same-case refresh alongside challenge-node preservation. In src/api/src/zava_forward/api/web/app.js:473-493, refresh invokes caseView again, but draftBox is a new empty container; plain and AI drafts create their textareas only after a request. AI review handlers close over the returned draft object and textarea. In src/api/src/zava_forward/api/web/app.js:171, the leave guard recognizes only form[data-unsaved="true"], whereas the call inputs and generated draft textarea are not such forms. Challenge preservation in src/api/src/zava_forward/api/web/panels.js:239-257 retains actual nodes and closures, not just values.
* Concern: field-value copying cannot restore a generated textarea that has no replacement node, its record_id/review metadata, or the handler that edits that exact output. The plan also does not define how these non-form controls become dirty or how a successful action excludes only its own inputs from restoration.
* Impact: refreshing proposals or saving an unrelated record can erase resident wording or pending review notes; restoring text into the wrong review context can associate an edit with the wrong output. Merely retaining tabs does not solve same-case refresh.
* Smallest useful change: specify case-scoped stable draft identities and a lifecycle for dynamic output nodes plus their review context. Either retain those live nodes/closures safely or reconstruct the complete draft model and handlers. Define dirty tracking for standalone controls, successful-action clearing for that action only, and disposal on confirmed case/identity change. Do not retain obsolete record versions as actionable.
* Action owner: planning parent; implementation owner for P01-T02/P02-T01.
* Exact resolving evidence: revised details enumerate call fields, generated plain/AI resident drafts, AI review reason/edit fields and existing challenge drafts. Planned browser assertions cover edited generated text and pending review context surviving a tab switch and unrelated same-case refresh; saving one form clears that form but preserves an unrelated draft; guarded case departure does not leak drafts into another case; reviewing a restored draft targets its original record with current authority checks.
* Decision route: direct planner correction. No significant or divergent user decision and no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The AI count lacks a state definition and pagination contract

* Related IDs: P01-T01, P02-T01; six-value summary and AI tab count.
* Evidence: the plan promises asynchronously updated AI counts; the design summary describes proposals with approval "Not reviewed". Existing assistant objects instead use state/display_state, verification and review, as shown in src/api/src/zava_forward/api/web/assistants.js:11-27 and src/core/src/zava_forward/core/assistants.py:669-695. The case-filtered listing still has LIMIT 50 and next_after in src/core/src/zava_forward/core/assistants.py:706-754. The existing case loader reads one page at src/api/src/zava_forward/api/web/assistants.js:70-89. Resident draft results have their separate approval field and currently live only in draftBox.
* Concern: the plan does not say which assistant states count as an output awaiting review, how subsequent pages are handled, whether the live resident draft contributes, or who updates both counters after local draft generation/review. Matching approval alone cannot classify assistant proposals; counting the existing first page can undercount even one case.
* Impact: "No AI suggestions waiting" can be false while a later page contains unreviewed output. The summary and tab can disagree or remain stale after a resident draft review.
* Smallest useful change: define one role-visible count model for assistant output states versus local draft approval, excluding queued/failed/no-output work and reviewed output as appropriate. Handle the existing case-filtered cursor and update summary/tab together on load, generation, refresh and review. If a deliberately bounded read is incomplete, label the count as incomplete rather than exact; do not broaden permissions or add an API field.
* Action owner: planning parent; implementation owner for P01-T01/P02-T01.
* Exact resolving evidence: a state-to-count table in the details and named tests for no output, ready/unverified, stale, reviewed and failed states; a synthetic case with more than 50 proposals and a reviewable output beyond page one; resident draft generation/review updating both counts once; delayed assistance after tab navigation updating the same case only.
* Decision route: direct planner correction within the selected existing-API approach. No significant or divergent user decision and no user response required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Navigation-only test edits conflict with the proposed AI control semantics

* Related IDs: Test Ownership and Change Budget, P02-T01, P03-T01.
* Evidence: the plan says existing assertions stay and "only explicit tab navigation is added where needed"; details repeat that existing browser checks receive only tab navigation changes. The supplied design changes the visible review vocabulary and Reason field. src/api/checks/assistants_browser_check.py:85-93 locates the old "Source verification or review note" name and exact "Accept proposal only" button. At line 105 it requires zero matching accept buttons for stale output, while the candidate requires native disabled acceptance for stale/unverified output.
* Concern: following the navigation-only rule literally can prevent the accessible-name and disabled-state changes, or make the required regression check fail even when the new UI preserves the authority boundary.
* Impact: the implementer may preserve obsolete wording, weaken the test covertly or exceed the declared edit budget without an approved disposition.
* Smallest useful change: permit narrowly enumerated selector/assertion adaptations for intentional review labels and unavailable acceptance, while preserving the original behavioral guarantees. Keep the person-specific source-check/revision flow and the unchanged-case-data assertion. Assert that stale output cannot be accepted, using the chosen disabled-control semantics rather than requiring the old button's absence.
* Action owner: planning parent; owner of existing browser selector adaptations.
* Exact resolving evidence: details name src/api/checks/assistants_browser_check.py and identify the old/new accessible names and the stale non-actionability assertion. Validation requires that adapted check to pass without removed scenarios or weakened authority/domain-data assertions.
* Decision route: direct planner correction to the test adaptation boundary, not a test-removal request. No significant or divergent user decision and no user response required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The new tab module has no enhancement-failure fallback contract

* Related IDs: P01-T01/P01-T02; design Tabs scripting-failure rule and retained-action requirement.
* Evidence: P01-T01 introduces a new module loaded before app.js, and P01-T02 changes caseView composition. The design explicitly requires stacked headed sections when the tab enhancement fails. Existing dependency recovery is deliberate in src/api/src/zava_forward/api/web/app.js:141-161 and exercised in src/api/checks/employee_workspace_browser_check.py:89-155, but the plan does not define the new module's failure behavior.
* Concern: hiding sections before successful tab initialization, or calling a missing module unconditionally, can leave the employee without the specified stacked-case fallback. Existing required-file recovery does not itself implement that fallback for an optional tab enhancement.
* Impact: a tab-module download or initialization failure can make otherwise renderable case controls unavailable, contrary to the selected progressive-enhancement requirement.
* Smallest useful change: specify atomic enhancement: construct reachable headed sections first, and hide inactive panels only after the tab controller has initialized successfully. If the new enhancement is unavailable, retain the stacked case and visible safety/manual controls without changing the existing handling of missing mandatory modules.
* Action owner: planning parent; implementation owner for P01.
* Exact resolving evidence: details define the before/after-initialization states and fallback. The focused browser check blocks the new module or forces its initialization failure, then asserts headed case sections/manual actions remain reachable, open safety remains visible, and there is no uncaught page error or permanently hidden inactive content.
* Decision route: direct planner correction implementing the supplied design. No significant or divergent user decision and no user response required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Browser ownership is defined, but decisive layout and state assertions remain implicit

* Related IDs: P03-T01/P03-T02; design acceptance criteria 1, 3, 5 and 7 and automated test plan.
* Evidence: the candidate assigns one focused browser check to synthetic case/axe/tab/keyboard/zoom states and says criteria 1-8 are checked. It does not identify the concrete assertions for first-screen information, the state-by-tab axe boundary or forced-colour behavior. Existing employee check contexts use 1280x900 in src/api/checks/employee_workspace_browser_check.py:40, not the design's 1280x800 first-screen target. The supplied design requires all six summary values without scrolling at 1280x800, at most one swipe at 320px, axe on every tab in loading/empty/blocked/AI-unavailable/closed states, and forced-colour/reduced-motion checks.
* Concern: running the named checks and taking a zoom screenshot alone would not demonstrate these specific criteria. "One swipe" also lacks a defined viewport height or scroll-distance bound. This is an assertion gap, not missing test ownership or a request for additional test files.
* Impact: the receipt can report a passing focused browser script while the first-screen goal, hidden safety/nondependent actions, or non-colour state distinction remains untested.
* Smallest useful change: add a compact assertion/state matrix to P03 within the existing one-script budget. Pin the 1280x800 fit measurement, a documented 320px viewport and one-viewport scroll bound, zero serious/critical axe violations for the required tab/state combinations, and concrete forced-colour/reduced-motion and focus/reflow assertions. Specify tab-only navigation leaves in-flight work/dirty state intact while real route changes preserve existing guards. Record unavailable combinations explicitly rather than calling criteria complete.
* Action owner: planning parent; owner of the focused browser check.
* Exact resolving evidence: revised details list fixture/state, action, measurable pass condition and result artifact for each of the above. Planned browser results include actual browser version and 200% mechanism, geometry/focus/overflow results and axe counts by state/tab, without substituting device scale factor alone for zoom. No live, screen-reader or staff-usability result is inferred.
* Decision route: direct planner correction to executable acceptance evidence. No significant or divergent user decision and no user response required.

## Strengths and Residual Risk

* Retained native DOM and a single derivation map are appropriate for the existing stack. Dependencies are ordered and the implementation/test ownership and no-removal budget are explicit.
* Funding and resident-decision evidence do not silently become approval or consent; a blocked step does not authorize blocking unrelated work.
* A single open safety panel remains above all tabs. Unknown owners/stages and missing confidence are not fabricated.
* Chat has no recorded-review endpoint. The plan appropriately preserves advisory answers and the separate proposal route, explicitly flags the design criterion exception, and does not invent client-only audit or acceptance. Keep that exception in implementation/Review evidence.
* Existing server authorization, person-specific assistant verification and proposal revisions remain authoritative. Harmonized labels cannot imply new powers.
* Original adverse Review outcomes, exact-head gate requirements and hosted/human approval boundaries are preserved.
* Live deployment, screen-reader and real-staff usability checks remain explicit pending owner work. A successful synthetic implementation is not acceptance of those hypotheses.

## Questions or Blocking Evidence Gaps

* No unresolved owner choice is needed to address PC-001 through PC-005.
* No additional open-ended research is required. Resolve the findings in the existing plan/details and implementation evidence.
* Missing local gate prerequisites remain publication blockers, not permission for skips, cloud fallback or weakened checks.

## Limitations

* Read-only assessment of the supplied final candidate and narrowly scoped existing code. No source or plan changes, browser execution, test run, Azure access, credentials, .env or private dataset inspection occurred.
* The supplied research's issue/web retrievals were considered as supplied evidence; no fresh external retrieval was performed.
* This is not a standalone UI audit, fresh web-guideline review, accessibility certification or a second critique. Implementation and exact-head review/gate evidence do not yet exist at this boundary.

## Recommended Next Action

* Highest-impact finding: PC-001, generated draft/review context loss during same-case refresh.
* Action owner: planning parent.
* Smallest next action: revise P01-T02 to define complete dynamic draft lifecycle and successful-action clearing, then disposition the remaining four bounded findings directly in the same planning candidate.
* User response required: No.
* Preserve this original Revise verdict. Finalize by direct disposition, without another plan critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/case-journey-ux-526-plan.md](.copilot-tracking/plans/2026-10-28/case-journey-ux-526-plan.md) | Supplied plan, unchanged |
| [.copilot-tracking/details/2026-10-28/case-journey-ux-526-phase-details.md](.copilot-tracking/details/2026-10-28/case-journey-ux-526-phase-details.md) | Supplied phase details, unchanged |
| [.copilot-tracking/research/2026-10-28/case-journey-ux-526-research.md](.copilot-tracking/research/2026-10-28/case-journey-ux-526-research.md) | Supplied research, unchanged |
| [docs/reference/research/ux/employee-case-workspace-redesign.md](docs/reference/research/ux/employee-case-workspace-redesign.md) | Supplied design and acceptance boundary, unchanged |
| [.copilot-tracking/reviews/plans/2026-10-28/case-journey-ux-526-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/case-journey-ux-526-plan-critique.md) | Original single-pass critique |

## Next Steps

The active planning parent should directly resolve and disposition PC-001 through PC-005, then finalize planning and continue the owner-requested ordered RPI loop after its gates. No user action or second critique is required. This reviewer stops after writing this artifact.
