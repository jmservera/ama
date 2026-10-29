<!-- markdownlint-disable-file -->
# RPI Plan Critique: loading-startup-correction-531

## Metadata

* Task ID: 531-correction-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/loading-startup-correction-531-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/loading-startup-correction-531-phase-details.md
* Critique execution status: Complete
* Critique boundary: Exactly one independent final-candidate assessment. Preserve this original outcome; do not commission another critique.

## Inputs and Criterion Boundary

* Caller requirements: Correct stale helper errors on retry and startup hanging when workspace-shell.js fails, following a complete loading-surface audit. Retain same-control fail/succeed and succeed/fail regressions, overlap isolation and real blocked-download browser coverage. Extend the existing watchdog to law entry-point failure without making main completion depend on it.
* Workflow requirements: Continue feat/loading-briefing-hax-531 / PR #538, with the supplied completed git pull --rebase prerequisite, full dated RPI evidence and local-only Conventional Commits. No push, az, force push, closing keywords, implementation, delegation or heavy execution in this critique.
* Supplied research: .copilot-tracking/research/2026-10-29/loading-startup-correction-531-research.md, including Q1-Q3, C1-C10/W1, complete script/helper inventories and accepted alternatives.
* Source context inspected: src/api/src/zava_forward/api/web/async-action.js; src/api/src/zava_forward/api/web/workspace-shell.js; src/api/src/zava_forward/api/web/index.html; src/api/src/zava_forward/api/web/law.html; src/api/src/zava_forward/api/web/law.js; startup, helper and loader portions of src/api/src/zava_forward/api/web/app.js; src/api/tests/test_loading_feedback.py; loader fixtures in src/api/tests/test_workspace_scripts.py; relevant portions of src/api/checks/loading_briefing_browser_check.py and its synthetic-server owner src/api/checks/design_system_browser_check.py; component validation guidance and strict-tool configurations.
* Project context: Original case study, introductory addendum and knowledge-base index, owner memory and sector-primer context. These introduce no new customer facts, approval authority or acceptance evidence.
* Existing outcome considered: .copilot-tracking/reviews/plans/2026-10-29/loading-briefing-review-correction-531-plan-critique.md. Its original Revise verdict and findings remain unchanged; this artifact assesses only the new supplied candidate.
* Decisions, dependencies and acceptance: P01 precedes P02; preserve pending-promise identity, per-operation ownership, disabled-state ownership, script retry budgets, route/session guards, optional case fallback and manual controls. Require API/core configured strict mypy, Ruff lint/format, units and relevant browser evidence when prerequisites and nonblocking heavy admission permit them. Busy/unavailable admission permits targeted checks only with unmet full checks explicitly recorded.
* Locked test boundary: No removals; at most two new helper unit methods, one loader unit method and three new parameterized browser functions. All corrections below fit existing files and this budget.
* Assessment boundary: Assess requirements, research, phases, tasks, dependencies, acceptance criteria, decisions, risks and missed concerns once. Source inspection supports design findings, not claims that proposed code or tests pass. No open-ended research, browser execution, fresh web-guideline retrieval or test execution was performed. Read-only git inspection confirmed the named topic branch and existing untracked parent artifacts.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1-C3, P01-T01: Helper feedback ownership | Covered | Pending guard remains first; weak per-control disposal precedes task invocation and does not erase inline errors or unrelated notices. |
| P01-T01: Sequential and overlapping regressions | Covered | Fail/succeed, succeed/fail, repeated rejection, synchronous outcomes, abort, timer cancellation, same-control identity and independent out-of-order controls/null reads are explicit. |
| Q2, C4-C5, P01-T02: Independent workspace completion | Covered | All current login/start/error dispatch sites acquire app-owned removal while retaining the completion event for watchdog cancellation. |
| C5, C8-C9, P01-T02: Download failure browser matrix | Covered | Blocked watchdog covers signed-out, authenticated and 503 outcomes; other index scripts retain terminal recovery or optional plain-case fallback. Existing held/failed app coverage remains. |
| C6, P01-T02: Law entry-point recovery | Covered | Shared timed native reload, named startup region and blocked law.js coverage are bounded extensions of the existing watchdog. |
| C6, P01-T02: Law terminal service errors | Partial | show() owns successful completion, but the initial list rejection calls fail(), which never replaces law-out. PC-001. |
| C7: Sibling audit and scope | Covered | Supplied research inventories shared helper consumers and all employee startup scripts; resident pages and welcome are classified separately without proposing unrelated changes. |
| C9-C10: Test ownership, budget and pins | Covered | Existing VM/browser owners are retained; pinned files are not planned targets, and pin verification is required. |
| P02-T01: API/core strict, lint/format, units and browser | Partial | Required checks and source/fixture precedence are present, but the named environment/lock recipe is not executable within the current filesystem boundary. PC-003. |
| W1, P01, P02-T02: Scoped web-guideline execution evidence | Partial | General applicability and a research retrieval do not specify the pre-edit activation and fresh independent-review retrieval/reporting steps. PC-002. |
| P02-T02: Local commits and one independent Review | Covered | Identity/trailer, local-only delivery, original evidence and blocking-findings limitation are explicit. No repeat Review or publication acceptance is implied. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: The helper ownership correction and independent workspace completion are credible and appropriately bounded. The proposed law startup region introduces an uncovered terminal service-error path. Two execution-plan corrections are also needed so the required web assessment and validation limitations are recorded honestly. All are direct planner corrections; no significant or divergent user decision is required.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Law startup completion omits the initial API failure path

* Related IDs: C6; P01-T02; functional requirements for terminal errors and independent main completion; law browser acceptance.
* Evidence: .copilot-tracking/details/2026-10-29/loading-startup-correction-531-phase-details.md:46-58 makes law show() replace the new startup region and signal completion, and tests law entry/watchdog download failures. In src/api/src/zava_forward/api/web/law.js:68, fail() only changes law-status; the initial read at line 84 uses list().catch(fail). Only show() at line 11 replaces law-out. The existing browser's law service-error exercise occurs after an initial successful list, not during startup.
* Concern: If the initial /api/law/sources request rejects or returns an error, the proposed startup child under law-out survives because show() is never called. With a working watchdog, its timers later display misleading startup/deadline feedback after the service has already failed. With the watchdog blocked, stale loading remains indefinitely beside the actual error. A later successful list can clear it, but that does not make the first failure a correct terminal outcome.
* Impact: The sibling correction can introduce the same stale-startup failure it is intended to eliminate, and the planned happy-path watchdog-block test would miss it.
* Smallest useful change: Specify idempotent law-owned startup removal and watchdog cancellation for both successful rendering and the initial terminal read failure. Retain fail()'s useful error and existing All sources/search retry controls; do not clear previously rendered reference content on later action errors. Extend the existing law browser coverage, or the already-budgeted parameterized law function, with an initial 503/rejection under watchdog-present and watchdog-blocked conditions. Advance beyond both deadlines, assert no connected startup region or stale startup feedback, retain the service error, then retry successfully. No new framework, test owner or budget increase is needed.
* Action owner: Planning parent revises P01-T02 and acceptance; implementation owner executes the correction.
* Exact resolving evidence: Plan/details explicitly cover law success and initial failure completion independently of the watchdog. The subsequent original implementation evidence identifies parameterized browser cases proving initial failure, post-deadline stability and successful retry, with no pageerror and within the locked budget.
* Decision route: Direct planner correction. The accepted law extension and independent terminal-completion requirement already resolve the design direction; no user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Required execution-time web-guideline steps are not assigned

* Related IDs: W1; P01-T01; P01-T02; P02-T02; non-functional requirements.
* Evidence: The plan says current web guidelines apply, and research W1 records a dated source retrieval. Neither P01 task assigns the pre-edit skill/current-source step, and .copilot-tracking/details/2026-10-29/loading-startup-correction-531-phase-details.md:80-87 requests an independent Review without its own source refresh and changed-web-file assessment. The same execution-evidence distinction is preserved in the earlier loading-briefing-review-correction-531 critique's PC-002.
* Concern: A general applicability statement and inherited research citation can be mistaken for completed execution-time evidence, especially when delegating the single independent Review. This candidate changes status ownership and native startup/reload behavior.
* Impact: Engineering tests could pass without the required scoped web review, or evidence could incorrectly imply a fresh review from a prior retrieval.
* Smallest useful change: Assign pre-edit web-design-guidelines activation/current-source use to P01, and fresh retrieval plus assessment of changed web files to the existing single independent Review. Require file:line findings, repository Fluent/native/plain-language precedence, and disclosure of failed/partial retrieval or unperformed checks. Reuse existing evidence artifacts; do not add another review, broaden the UI audit or alter the test budget.
* Action owner: Planning parent; implementation owner and the already-planned independent reviewer execute their respective steps.
* Exact resolving evidence: Plan/details name both execution points and reporting requirements. Subsequent implementation evidence records the pre-edit source status, and the original independent Review records its own refresh, changed-file coverage, findings and limitations.
* Decision route: Direct planner correction to an existing scoped requirement. No significant or divergent decision and no user response are needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Validation assumes paths unavailable within the current execution boundary

* Related IDs: P02-T01; validation dependencies; required strict/unit/browser checks and prerequisite fallback.
* Evidence: .copilot-tracking/plans/2026-10-29/loading-startup-correction-531-plan.md:44-46 and .copilot-tracking/details/2026-10-29/loading-startup-correction-531-phase-details.md:71-77 prescribe editable installation in /tmp/mv and admission through /tmp/ama-rpi-heavy.lock. Those file operations are unavailable within this execution's permitted workspace storage boundary. The candidate lists no planning blocker and does not distinguish an unavailable lock from a busy lock.
* Concern: The validation recipe cannot be followed as written here. Silently using a different lock would bypass the required shared coordination; running full suites without it is not an acceptable workaround. Similarly, an assumed shared environment is not evidence that the tools and correct worktree distributions are usable.
* Impact: Execution may either attempt unavailable operations or incorrectly report full validation after bypassing admission. This is a prerequisite limitation, not a reason to weaken the checks or expand scope.
* Smallest useful change: Record the environment/lock-access limitation explicitly in P02-T01. Use permitted project-relative storage for any newly created environment or output only where compatible with the existing validation contract, and install only after a missing-dependency/tool failure establishes the need. Preserve the canonical shared-lock identity: if it cannot be accessed through a permitted mechanism, mark full-suite admission unavailable and use only the authorized targeted fallback. Do not invent a replacement lock, queue, mutate the shared environment, or claim the required full suites passed.
* Action owner: Planning parent records the executable recipe and prerequisite disposition; validation owner records actual availability and outcomes.
* Exact resolving evidence: Plan/details distinguish busy and inaccessible prerequisites and require an explicit unmet-check list. Implementation evidence subsequently records permitted tool/environment provenance, actual admission if available, or targeted-only results with full strict/unit/browser checks individually identified as unperformed where applicable.
* Decision route: Direct planner correction using the already-authorized prerequisite-blocker fallback. No user response is needed; any later authorization to change shared coordination would be a separate decision and is not requested here.

## Strengths and Residual Risk

* Weak per-control notice disposal addresses the defect without global status selectors. Keeping pending deduplication first preserves the original promise, active notice and task invocation count.
* Null-control reads retain independent lifetimes; a keyed cleanup mechanism must not combine them into a shared pseudo-control.
* Main-owned removal plus the existing ready event keeps watchdog cancellation and independent completion separate. Adding the watchdog to required dependencies is correctly rejected.
* The supplied loading audit is complete for the selected shared-helper/employee-startup boundary, including every index script, optional case fallback and the standalone law page. No resident implementation expansion is justified.
* Existing VM and real Chromium owners can accommodate these corrections within the locked method/function counts by parameterization and extension. No test removal or generated test suite is needed.
* The plan already states that blocking independent Review findings prevent a complete-correction claim. Preserve that rule and all original adverse outcomes; local targeted follow-up is not a second independent acceptance.
* Busy or unavailable admission remains an accepted validation limitation, not a passing result. Configured strict mypy and existing Ruff rules remain authoritative without new suppressions or exemption changes.
* Human screen-reader/voice, real-staff usability, hosted/live checks and publication remain unestablished. Local-only commits do not authorize push or imply the complete publication gate has run.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents these direct corrections.
* Tool, browser and permitted shared-admission availability are execution-time facts. Record them and any unmet checks rather than reopening research or commissioning another critique.
* No decision-critical source gap prevents this assessment. The law failure concern follows directly from the existing initial catch path and proposed startup-region ownership.

## Limitations

* This critique evaluates the supplied final candidate, not an implemented correction. No tests, heavy checks, browser session, package installation, remote operation, rebase or commit was performed.
* Source context was inspected only as necessary to assess the supplied research and plan. Existing research inventory claims were not expanded into an unrelated audit.
* Only this requested artifact was written. Plans, phase details, research, state and all earlier critique/review outcomes remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add law initial-failure completion and its parameterized regression to P01-T02, then dispose PC-002 and PC-003 directly in the same finalization.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/loading-startup-correction-531-plan.md](.copilot-tracking/plans/2026-10-29/loading-startup-correction-531-plan.md) | Assessed final-candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-29/loading-startup-correction-531-phase-details.md](.copilot-tracking/details/2026-10-29/loading-startup-correction-531-phase-details.md) | Assessed phase details, unchanged. |
| [.copilot-tracking/research/2026-10-29/loading-startup-correction-531-research.md](.copilot-tracking/research/2026-10-29/loading-startup-correction-531-research.md) | Supplied loading audit and source evidence, unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-29/loading-startup-correction-531-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/loading-startup-correction-531-plan-critique.md) | Original Complete / Revise critique and full PC-001 through PC-003 set. |

## Next Steps

The active planning parent should apply the three direct corrections, preserve this original Revise verdict, record dispositions and finalize without another critique. Continue the authorized local-only RPI loop after finalization; record unavailable validation explicitly. No user command or response is required.
