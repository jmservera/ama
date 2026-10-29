<!-- markdownlint-disable-file -->
# Review: loading-briefing-hax-531-review-fixes

## Scope and Evidence

* Task ID: 531-review-fixes-2026-10-29
* Review date: 2026-10-29
* Review scope: one independent post-implementation Review of all four requested corrections.
* Assessed committed source: 2b37261be30e61cf8baf7494561def0607693e0d against intake 81ab4a0e76e1ab86ce0d7174c630c809d8487064.
* Plan: .copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-29/loading-briefing-hax-531-review-fixes-changes.md
* Research: .copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md

## Opening Review State

* Interpreted review goal: independently evaluate correctness, exact regression semantics, critique dispositions and honest validation limits for the four corrections.
* Review scope: seven changed source/documentation files under src; supplied task artifacts are evidence, not mutation targets.
* Evidence readiness: supplied artifacts exist; HEAD equals the assessed commit. Source diff is available. Detailed comparison is pending.
* Acceptance basis: approved correction requirements and current plan/detail acceptance, including Edit retry, quote/bracket punctuation, terminal suffix ownership, and absent AsyncAction fallback/browser assertions.
* First comparison boundary: reconcile current plan/details/critique/changes, then inspect complete seven-file committed source diff and relevant surrounding functions/tests.
* Active read-only boundaries: write only this canonical Review. Parent-owned uncommitted state transition is excluded from source assessment and remains untouched. No delegation, fixes, commits, push, Azure operations or repeated Review.
* Initial blockers: no blocker to bounded source Review. Heavy validation is unavailable following the recorded nonblocking lock refusal; do not retry, queue or poll. Full/browser/axe execution and publication approval remain distinct follow-ups.

## Execution Status

* Execution status: Complete.
* Exactly one independent Review executed on 2026-10-29. Compared the complete seven-file committed source diff, surrounding parser/loader/renderer/dispatch contracts, all five supplied artifacts and the freshly retrieved web guidelines.
* This is Review execution status, not a claim that full validation or P03-T02 persistence is complete. Parent owns the remaining local evidence commit.
* No source edits, nested delegation, heavy-lock inspection/retry, full suites, browser launch, editable setup or publication occurred.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Review dispatcher harness | Reconciled | Real Edit currentTarget and retained submit used; all eight outcomes retained. |
| P01-T02 | Statement boundaries | Reconciled | One shared sentence-ending fragment serves relocation and segmentation; exact ownership assertions, not count-only checks. |
| P01-T03 | Suffix ownership | Reconciled | Terminal name context differs from lowercase medial and title contexts; disclosed conservative heuristic retained. |
| P02-T01 | Helper recovery | Reconciled with validation limit | Actual renderer and loader regressions pass; authored browser scenario is inspected, not executed. |
| P03-T01 | User-authorized nonblocking validation fallback | Reconciled | Targeted/static checks are complete within authorized admission; broad/browser checks remain explicitly unperformed. |
| P03-T02 | Local persistence and original Review next | In progress under parent | Assessed implementation commit exists; this original Review and final state/evidence commit remain parent-owned closeout. |
| Follow-Up Items | FU-001 and FU-002 | Reconciled | Both are explicit in plan/details/changes; neither silently expands active implementation acceptance. |

The P02 checked marker means implementation and unit evidence are complete, not
that its browser success criterion ran. Its adjacent evidence qualification,
P03 fallback instructions and FU-001 consistently disclose that limitation.
The remaining P03/P03-T02 markers correctly remain open at this boundary.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/tests/test_case_journey.py | Activate Edit with its real event and retry the actual submit after ambiguous outcomes. | Lines 1472-1473 pass the selected button as currentTarget; line 1504 retries submit. | Independent dispatch method pass. | Correctly reaches pending, newer-value, refusal, committed, uncertain, transport and single-completion assertions; no assertions removed. |
| P01-T02 | src/core/src/zava_forward/core/ai_tasks.py; src/core/tests/test_ai_statement_sources.py | Include closing quotes/brackets in punctuation relocation and segmentation. | STATEMENT_END at line 31 is reused at lines 154 and 178; tests lines 9-80. | Independent owning parser suite pass. | Closing delimiters remain in clean text and references remain with their declared statement, including unknown references. |
| P01-T03 | src/core/src/zava_forward/core/ai_tasks.py; src/core/tests/test_ai_statement_sources.py | Leave terminal Jr./Sr. unshielded after capitalized name context before an uppercase claim. | Parser lines 164-168; new suffix tests lines 82-127 and unchanged title/abbreviation tests. | Independent owning parser suite pass. | Required terminal, medial and title semantics preserved for supplied fixtures. |
| P02-T01 | src/api/src/zava_forward/api/web/app.js; src/api/tests/test_workspace_scripts.py | Require callable handler before wrapping native listeners; exercise actual h()/startupFailed(). | app.js:21 and actual-renderer test lines 11-74; loader harness also covers unready state. | Independent workspace-script suite pass. | Empty/non-callable helper no longer throws while creating reload; absent helper passes through and healthy helper wraps once. |
| P02-T01 | src/api/checks/loading_briefing_browser_check.py; src/api/README.md | Author replay-safe unready-helper recovery scenario and document bounded behavior. | Browser lines 67-164; README describes callable fallback and parser boundaries. | Static inspection only for browser behavior. | Appropriate executable assertions authored; actual keyboard/reload/axe outcome remains FU-001. |

### Exact regression semantics

* Quoted golden: `The status is "Survey booked." [[First source]] Repairs are due. [[Second source]]` produces exactly two dictionaries with text `The status is "Survey booked."` / `Repairs are due.`, citations `["First source"]` / `["Second source"]`, and empty unresolved arrays. Test literals match phase details.
* Delimiter matrix: three punctuation marks, nine quote/bracket/nested pairs, four whitespace/newline separators and three citation placements yield 324 subcases. Each checks both exact statements, citation arrays, unresolved `Unknown source` ownership and unchanged closing order. Uncited first statements do not acquire the second statement's reference.
* Terminal goldens: for each of Jr./Sr., `Contact John Smith {suffix} Repairs are due. [[Second source]]` yields an uncited first dictionary and second-only citation, exactly as phase details require. First-only and both-cited variants also assert full dictionaries.
* Medial cases keep `Contact John Smith Jr./Sr. about the survey.` intact with its own first source. Existing `Contact Jr./Sr. Jones` title cases and other abbreviations/newline fixtures still pass.
* The suffix rule is intentionally a bounded capitalized-name heuristic, not general sentence inference. Ambiguous uppercase continuations remain the accepted conservative split limitation recorded in research/details; no broader language correctness claim is made.
* Dispatcher retains eight outcomes and prevents duplicate writes during pending, after history-ambiguous failure and after successful completion. Assertions inspect submitted snapshots versus newer dirty values, read-only preservation and completion count.
* Actual renderer VM evaluates extracted production h()/startupFailed(), not a fake replacement renderer. For absent, empty, non-callable and ready helpers it checks heading, alert, status text, ready event, native button/type/label, installed click listener and one reload invocation. It does not simulate browser focus or assistive technology.
* Browser fixture uses `var AsyncAction = {};` for both same-document evaluations; no lexical redeclaration is introduced. It asserts exactly two requests, stable after 800 ms, unready object identity, terminal heading/alert/live status, no `/api/me`, no pageerrors and no alternate retry. It removes interception before Tab/Enter native reload, then checks healthy helper, actual sign-in and account feedback. These are authored assertions, not observed browser passes.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 | Pin replay-safe var injection and exact two-request expectations. | PC-001; direct correction preserving confirmed intent. | Plan highlights, disposition and phase details agree with browser source. | Ready after disposition; original critique Revise preserved. | Reconciled; no material divergence or new user decision. |
| P01-T02/T03 | Record original literal goldens and full expected dictionaries. | PC-002; direct evidence clarification. | Details contain source mapping and exact quote/Jr./Sr. inputs; owning tests match. | Ready after disposition; no repeated critique. | Reconciled. |
| P03-T01; FU-001 | Use targeted/static fallback rather than blocked shared setup/full/browser work. | Admission exit 75, owner PID 679022, explicit user-authorized fallback. | Plan summary, task evidence, details, changes, blockers and follow-up all disclose unmet checks. | No material revision; original scope and approval boundaries preserved. | Justified execution adjustment, not fabricated acceptance. |
| P03-T02 | Implementation commit precedes original independent Review and final local evidence commit. | Assessed HEAD and current artifact handoff. | Open marker accurately reflects parent-owned continuation. | Ready for this one Review. | Correct sequencing; no claim that final local persistence is already complete. |

## Critique and Material Revision Assessment

* Exactly one final-candidate critique records Complete / original Revise, Medium PC-001 and PC-002. Neither original finding nor verdict was overwritten.
* PC-001 is resolved directly in plan/details and source by replay-safe `var` injection, bounded request checks, no premature service read/pageerror and route removal before keyboard reload. Browser execution remains explicitly unperformed, as the critique permits under busy admission.
* PC-002 is resolved directly by the literal original goldens, mappings and expected dictionaries in phase details and matching owning tests.
* No significant or divergent implementation decision was found. No new planning/research destination or dependent-work pause is required; the supplied records place both direct critique dispositions before implementation.
* No additional critique or repeated Review is requested.

## Scoped Web Interface Guidelines Assessment

Fresh source retrieved successfully on 2026-10-29 before assessing changed web
behavior: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
All fetched rule categories were considered for the changed listener/readiness
behavior and its terminal-recovery consumers, not for unrelated app screens.

### src/api/src/zava_forward/api/web/app.js

* src/api/src/zava_forward/api/web/app.js:21 - PASS: callable-helper guard preserves native listener fallback and healthy wrapper.
* src/api/src/zava_forward/api/web/app.js:1539 - PASS, source inspection: terminal status retains existing polite live region contract in index.html.
* src/api/src/zava_forward/api/web/app.js:1540 - PASS, source inspection: terminal heading and alert retained.
* src/api/src/zava_forward/api/web/app.js:1543 - PASS: explicit native button/type/name/reload action; no div-click or inline navigation replacement.
* Existing style.css:45/48 preserves hover/visible-focus styles; existing reduced-motion rules remain untouched. No new animation, layout, image, form, locale, hydration or destructive-action surface is introduced.

No scoped guideline defect was identified. Source-level semantics and VM click
evidence do not establish rendered focus visibility, browser keyboard success,
axe results, screen-reader/voice usability or whole-app WCAG/Fluent acceptance.
The browser assertion for the polite live region is authored but unrun.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| FU-001 | Busy nonblocking heavy admission prevented full suites, current-worktree editable setup and browser/axe execution; user authorized targeted fallback only. | Coordinator explicitly schedules free-lock admission before running the existing full core/API and loading/briefing browser checks. | Open residual validation; RV-001. No queue, retry or polling by this Review. |
| FU-002 | Local correction round does not authorize publication or establish hosted/human accessibility approval. | Parent/owner retain separately authorized complete local gate, publication and hosted/human acceptance decisions. | Open approval boundary; RV-002. No push or operational action here. |

Unresolved follow-ups remain distinct work, not new active implementation tasks
or defects solely because they remain open.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Full and rendered-browser validation remains unperformed

* Related scope: P02-T01, P03-T01, FU-001.
* Evidence: changes validation record and user-supplied admission evidence report `flock -n -E75 /tmp/ama-rpi-heavy.lock` exit 75, owner PID 679022. Full core/API discovery, browser/axe and editable setup did not execute. Browser source lines 93-124 contains new assertions without runtime results.
* Impact: focused tests establish exact parser and simulated renderer/dispatch contracts, but cannot demonstrate full-suite compatibility, actual two-request browser execution, focus/Enter reload or rendered accessibility. This limits acceptance coverage, not the credibility of the bounded source correction.
* Destination: distinct follow-up FU-001, coordinator-owned residual validation.
* Smallest useful next action: obtain explicit free-lock coordination, then execute existing current-worktree full core/API and loading/briefing browser/axe checks and persist actual outcomes. Keep failures visible and route any newly established defect through later implementation; do not repeat this Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Local source evidence does not establish publication or human acceptance

* Related scope: P03-T02, FU-002.
* Evidence: plan non-goals and FU-002, changes return-to-caller state, repository gate requirements and explicit local-only user restriction. No current complete local-gate receipt, hosted approval or human accessibility acceptance is supplied.
* Impact: this Review must not be used as permission to publish or as whole-app accessibility approval. This is a retained governance boundary, not a source defect.
* Destination: distinct follow-up FU-002, parent/owner-held approval work.
* Smallest useful next action: complete authorized local-only evidence persistence; leave publication and hosted/human decisions separately gated until explicitly authorized. No push, az, force-push or closing keywords.

## Defects

* None identified in the assessed seven-file correction boundary.
* Complete severity set: Critical 0, High 0, Medium 1, Low 1. Both findings are residual work, not implementation defects.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | FU-001 | Coordinator schedules explicit free-lock full/browser validation. | Authorized execution limit; not a new parser/renderer defect or research uncertainty. |
| RV-002 | FU-002 | Parent/owner preserves separately authorized publication and acceptance gates. | Approval boundary outside local correction scope. |

Later implementation of an established defect does not require another Review.

## Residual Work

* FU-001 retains full suites, browser keyboard/reload/axe checks and coordinated setup. No existing historical run substitutes for this committed candidate.
* FU-002 retains publication, hosted and human approval. Whole-app accessibility remains unestablished.

## Blockers and Remaining Work

* No blocker to completing this bounded independent Review.
* Heavy admission remains the recorded blocker to broad/runtime validation; no new lock observation or attempt occurred here.
* No remaining source correction identified. Parent owns P03-T02 final local Review/state/evidence persistence; this Review does not mutate those records or commit.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Independent source-first unittest command below | Owning parser suite, exact dispatch method, workspace scripts | Passed | 11 tests, 0.305s, exit 0. Includes 324 delimiter subcases, literal goldens and real renderer VM. |
| Independent `node --check src/api/src/zava_forward/api/web/app.js` | Changed web file | Passed | Exit 0. |
| Independent `git diff --check 81ab4a0e76e1ab86ce0d7174c630c809d8487064 2b37261be30e61cf8baf7494561def0607693e0d` | Assessed committed diff | Passed | Exit 0. |
| Independent concrete import identity checks | core ai_tasks, API server, agents version | Passed | All resolve beneath this worktree's respective src trees; agents namespace itself has no __file__, so concrete version module checked. |
| Parent-reported expanded source-first suite | test_ai_statement_sources, test_case_journey, test_workspace_scripts, test_loading_feedback, test_ai_tasks | Passed, supplied evidence | 103 tests, 20.925s; not rerun in full during Review. |
| Parent-reported test_needs_inventory | Scenario-manifest integrity | Passed, supplied evidence | 11 tests; unchanged pinned source paths. |
| Parent-reported strict mypy and Ruff lint/format | Complete core/API configured scope | Passed, supplied evidence | mypy 157 core / 101 API source files; Ruff 104 core / 53 API formatted files. No shared-tool mutation by Review. |
| Original regression-first failures | Parser goldens and actual renderer | Failed as expected, historical supplied evidence | Changes/research retain pre-fix failures; not claimed as independently reproduced pre-fix here. |
| Full API/core unit discovery | Both components | Unavailable/unperformed | Busy admission exit 75; FU-001. |
| Loading/briefing browser and axe | Actual synthetic browser runtime | Unavailable/unperformed | Busy admission; authored assertion inspection only, FU-001. |
| Current-worktree editable setup | Shared environment | Unperformed | Busy admission; foreign editable metadata not modified. Absolute source-first imports independently verified. |
| Fresh guideline fetch | Scoped changed web behavior | Passed | Current source retrieved and scoped source review completed; no whole-app acceptance claim. |
| Complete publication gate, hosted/human acceptance | Release and accessibility acceptance | Unperformed/not established | Local-only authorization; FU-002. |

Independent focused command (repository-root cwd; absolute import paths avoid
foreign editable resolution; bytecode writes disabled):

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/home/azureuser/source/ama-wt/issue-531/src/api/src:/home/azureuser/source/ama-wt/issue-531/src/api/tests:/home/azureuser/source/ama-wt/issue-531/src/core/src:/home/azureuser/source/ama-wt/issue-531/src/core/tests:/home/azureuser/source/ama-wt/issue-531/src/agents/src:/home/azureuser/source/ama-wt/issue-531/src/agents/tests \
/tmp/mv/bin/python -m unittest test_ai_statement_sources test_case_journey.CaseJourney.test_review_dispatch_preserves_newer_values_and_completes_only_once test_workspace_scripts -q
```

## Outcome

* Outcome: Residual work.
* All four corrections are supported by committed source and focused behavioral evidence, including exact dictionary ownership and actual renderer/native click behavior. No implementation defect or unaccepted decision gap was identified.
* Full/browser/axe acceptance remains unavailable under the explicitly authorized fallback. Complete Review execution does not turn that unavailable evidence into a pass.
* Recommendation: parent completes authorized local-only P03-T02 persistence, retaining this original Review, original critique and both follow-ups. No repeated Review, publication or approval inference.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement finding established. |
| Decision gap or invalid assumption | None | No rpi-plan finding established. |
| Material research evidence gap | None | No rpi-research finding established; runtime validation is explicitly FU-001. |
| Non-blocking residual validation | FU-001 / RV-001 | Coordinator schedules full/browser checks after explicit free-lock coordination. |
| Non-blocking approval boundary | FU-002 / RV-002 | Parent/owner retains publication and hosted/human acceptance gates. |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: independent 11-test focused run, syntax/committed-diff checks and concrete import identities pass; parent-supplied 103 targeted/11 manifest/strict checks accepted as supplied evidence; full/browser/axe not run.
* Blockers: no Review blocker; busy admission limits broad validation.
* Write boundary: only this canonical Review created; parent-owned uncommitted state and all source/evidence inputs untouched.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md](.copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md) | Compared research and original reproduction evidence. |
| [.copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan.md](.copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan.md) | Current acceptance, markers, dispositions and follow-ups. |
| [.copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md](.copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md) | Literal goldens and execution contracts. |
| [.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan-critique.md) | Preserved original Complete / Revise critique. |
| [.copilot-tracking/changes/2026-10-29/loading-briefing-hax-531-review-fixes-changes.md](.copilot-tracking/changes/2026-10-29/loading-briefing-hax-531-review-fixes-changes.md) | Implementation, validation and fallback evidence. |
| [.copilot-tracking/reviews/logs/2026-10-29/loading-briefing-hax-531-review-fixes-review.md](.copilot-tracking/reviews/logs/2026-10-29/loading-briefing-hax-531-review-fixes-review.md) | This single original independent Review. |

## Next Steps

Active parent completes local-only P03-T02 evidence persistence and retains
FU-001/FU-002 with their distinct owners. No user action, source correction,
repeat Review, heavy-lock retry, push or cloud operation is required by this
Review.
