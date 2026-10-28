<!-- markdownlint-disable-file -->
# RPI Plan Critique: employee-briefing-manager-visibility

## Metadata

* Task ID: employee-briefing-manager-visibility
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/employee-briefing-manager-visibility-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/employee-briefing-manager-visibility-phase-details.md
* Critique execution status: Complete
* Assessment: one independent final-candidate critique; original outcome.
* Source baseline: 98b0bb98f2424dd23c00e386378f44892a7a79e0
* Branch: fix/employee-briefing-manager-visibility

## Inputs and Criterion Boundary

* Caller requirements: owner decision dated 2026-10-28, "Show all programme cases to manager roles on the briefing". Existing manager constants, permitted reads and authorization remain authoritative. Other staff keep assignment-only briefings; unbound identities gain no assignments. My cases intentionally stays personal. JSON and SQL unit coverage and actual browser label evidence are required.
* Primary evidence: .copilot-tracking/research/2026-10-28/employee-briefing-manager-visibility-research.md; .copilot-tracking/plans/2026-10-28/employee-briefing-manager-visibility-plan.md; .copilot-tracking/details/2026-10-28/employee-briefing-manager-visibility-phase-details.md.
* Direct implementation evidence: src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/projection.py, src/core/src/zava_forward/core/identity.py, src/core/src/zava_forward/core/ai_tasks.py, src/api/src/zava_forward/api/server.py and src/api/src/zava_forward/api/web/app.js.
* Direct validation evidence: src/api/tests/test_ai_tasks.py, src/api/tests/test_assistant_release.py, src/core/tests/dataset.py, src/core/tests/test_sensor_privacy.py, src/api/checks/design_system_browser_check.py and src/api/checks/workbench_browser_check.py. API README and test configuration were searched for directly relevant commands and selectors.
* Repository context: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md, read in relevant opening ranges. No new legal, customer or production claims are assessed.
* Decisions and dependencies: research C1-C10, FR1-FR7, AC1-AC8 and P01-P03, including the locked test owner, maximum nine new mixin methods, maximum two cache-internals reference adjustments, no test removals and one independent implementation Review.
* Assessment boundary: credibility and completeness for implementation, not implementation acceptance. The caller-supplied validation restriction governs: no --all; this small change uses focused checks, not --changed. The external brief's restriction is supplied context, not a fresh filesystem retrieval.
* No Azure, secrets, .env, private datasets, uv, tests, browser execution, nested agents or source edits were used. The critique artifact is the sole authorized write.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner decision; FR1; C2-C4; AC1 | Covered | Existing workflows.MANAGER_ROLES is already imported by Store. Role-dependent list_cases selection changes briefing scope without broadening endpoint or case authorization. Both managers and closed exclusion are explicit paired-store assertions. |
| FR2; FR3; AC3 | Covered | Store-level projection.allowed guard is explicitly before selection/cache. Denied roles and a restricted list_cases result test the boundary without changing authorization rules. |
| FR4; AC6; P01-T02 | Partial | Explicit scope, full eligible count and selected count distinguish programme visibility from the top-eight summary. Cache context does not yet guarantee freshness of the full eligible count; PC-001. |
| FR5; AC2; AC7; C6-C7 | Covered | Personal queues/counts are excluded from edits. Existing unbound non-manager regressions remain; new unbound manager tests distinguish view authority from assignment. |
| FR6; AC5; C4-C5 | Covered | Projected row status replaces raw status facts; selected cases retain export_fields.prompt_case and existing citation/release machinery. Controlled case mutation assertions are planned. |
| FR7; AC4 | Partial | Actor, role, reason visibility, selected IDs, mode and existing release/continuity checks are included. A permitted-set change outside the selected eight can collide; PC-001. |
| AC1-AC6; P02-T01; C8 | Covered with PC-001 correction | TasksMixin owns semantics on JsonTasks and SqlTasks. Existing release tests have exactly two direct cache-key references in scope; stale-release behavior must remain. Add the PC-001 scenario within the existing nine-method budget. |
| AC7; P02-T02; C9 | Covered | Existing real-server harness accepts browser/data callbacks, isolates server environment and checks loopback readiness. Plan requires both managers, an empty personal manager queue, ordinary staff, API-to-rendered labels/counts, keyboard toggle and reflow. |
| AC8; P02-T03 | Covered at planning boundary | API discovery, focused core privacy/cache, release/role checks and changed-file checks are planned. No runs or passes are inferred. Explicit owner gate restriction is preserved. |
| P01-T03; scope/non-goals | Covered | API README is the appropriate documentation owner; no historical research rewrite, navigation redesign, prompt/version change, schema or dependency expansion is planned. |
| P03-T01; P03-T02 | Partial | Original Review preservation and exact candidate inspection are planned, but routing every open finding to later work lacks a blocking publication disposition; PC-002. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 1; Medium 1; Low 0.
* Rationale: the selected implementation approach is credible and respects the explicit owner decision. Two bounded planner corrections are needed: make the cache cover full eligible-scope metadata, and prevent unresolved blocking Review findings from flowing automatically into publication. Neither correction changes AC1-AC8, test ownership/removals/budget or the user-selected scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Top-eight cache identity does not cover the full eligible scope

* Related IDs: FR4, FR7, AC3, AC4, AC6, P01-T01, P02-T01; research C5 and selected cache alternative.
* Evidence: .copilot-tracking/details/2026-10-28/employee-briefing-manager-visibility-phase-details.md, P01-T01, specifies selected IDs in cache identity and returns the full eligible case_count. The research alternative likewise specifies permitted top IDs. src/core/src/zava_forward/core/store.py:726-765 caches the complete response, conditional on store version and release/continuity context. AC4 explicitly requires separation when the permitted set changes.
* Concern: at an unchanged store version, a current permitted read can change from ten eligible cases to nine while preserving the ordered top eight. Actor, role, reason visibility, mode and selected IDs are identical, so the planned key can return the prior case_count. The plan already treats permission changes independent of case writes as requiring fresh scope checks, but the specified key only covers the summarized subset.
* Impact: the briefing can display an incorrect eligible programme count even when selected model facts remain permitted. This fails the full-count contract and the literal permitted-set cache boundary in AC4.
* Smallest useful change: specify cache identity using the complete ordered eligible ID tuple, with the selected top eight derived from it. Alternatively recompute/replace scope metadata on every hit and explicitly justify why unchanged selected content is reusable. The complete-ID approach directly matches AC4 without weakening it.
* Action owner: planning parent, then P01/P02 implementer.
* Exact resolving evidence: amended P01-T01/FR7 details cover full eligible scope; an assertion within an already-budgeted TasksMixin cache method first returns more than eight permitted cases, then removes a non-top-eight case through the existing patched list_cases boundary without changing store.version. Both JsonTasks and SqlTasks must return the new case_count and unchanged correct summary_count/selected IDs, with no excluded case in model facts or record IDs. Preserve the maximum nine new methods and all existing tests.
* Decision route: direct planner correction. The owner already requires permitted cases and accurate full/selected counts; no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Publication has no explicit stop for blocking independent Review findings

* Related IDs: P03-T01, P03-T02, AC8; retained original independent Review outcome.
* Evidence: .copilot-tracking/details/2026-10-28/employee-briefing-manager-visibility-phase-details.md, P03-T01, states, "Any open findings route to later work, never a repeated Review within this task." P03-T02 then instructs committing and pushing the topic branch and opening a PR without conditioning that sequence on the Review disposition. The plan requires independent Review and preserves pending hosted/human checks, but supplies no classification separating blocking findings from deferrable residuals.
* Concern: the literal sequence permits publication to proceed even if the single Review finds an unresolved authorization regression, disclosure, failed required browser/unit check or other acceptance-blocking defect. The one-Review limit prevents serial review, not the need to honor its original result.
* Impact: an unsuccessful independent assessment can be retained as evidence while the same unacceptable candidate advances as if publication prerequisites were satisfied.
* Smallest useful change: make P03-T02 conditional on the original Review outcome and disposition. Require a per-finding resolution/defer/block record; unresolved acceptance-blocking findings stop publication and are handed off with the original outcome intact. Only explicitly justified nonblocking residuals may be deferred. Do not prescribe another Review or broaden the prohibited local gate.
* Action owner: planning parent; publication executor enforces the condition.
* Exact resolving evidence: P03-T01/T02 explicitly define the stop condition and original-outcome preservation. The eventual publication record identifies the reviewed candidate, original verdict, disposition of each finding, required validation outcomes and any exact-head changes. An unresolved blocker produces a stopped handoff, not a push/PR presented as a completed accepted candidate.
* Decision route: direct planner correction. No new user response is required to stop on an unresolved blocking result. A later proposal to waive such a blocker would need separate explicit authority, not assumed consent from the finite-loop request.

## Strengths and Residual Risk

* Existing manager constants and permitted list reads are reused; the plan does not confuse role authority with staff-roster binding or case ownership.
* My cases remains personal by explicit direction, including for a manager with no assigned cases. This is intentional, not a missing programme queue.
* Projected waiting status, retained export guards and release/continuity checks are substantive controls, not merely UI relabelling.
* Paired JSON/SQLite semantics and a real synthetic browser check are appropriate bounded evidence. SqlStore's unlimited page_cases path delegates to Store.page_cases; the plan does not claim native SQL paging or production SQL Server verification from this test.
* Existing AI identity tests and cache stale-release protections are retained with a narrowly controlled change budget.
* Live Entra mapping, production SQL Server, actual model execution, Azure deployment, human approval and accessibility acceptance remain explicitly outside this local result. Hosted checks remain pending until observed.
* The supplied owner restriction on --all/--changed is accepted; no full receipt, workaround or widened validation gate is requested by this critique.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents the two direct corrections.
* No decision-critical research gap was identified within the supplied boundary.

## Limitations

* Read-only source assessment; no implementation, tests, browser execution or fresh external-source verification was performed.
* The supplied research's prior PR and web-guideline retrievals are provenance, not fresh checks by this critic. The implementation and Review must perform their required web-guideline refresh.
* The worktree contained the caller's untracked dated planning/research/session directories. They were not changed or moved. HEAD matches the caller-supplied reviewed base.
* This is the complete actionable finding set from this one assessment. The original verdict is not a request for a repeated critique.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: planning parent.
* Smallest next action: add an explicit blocking-Review publication stop, then extend the cache-context specification/test scenario for PC-001 within the locked budget.
* User response required: no.
* Handoff: parent resolves both findings directly, records disposition and finalizes the plan without another critique.
