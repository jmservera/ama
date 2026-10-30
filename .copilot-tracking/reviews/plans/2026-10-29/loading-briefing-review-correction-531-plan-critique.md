<!-- markdownlint-disable-file -->
# RPI Plan Critique: loading-briefing-review-correction-531

## Metadata

* Task ID: 531-review-correction-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/loading-briefing-review-correction-531-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/loading-briefing-review-correction-531-phase-details.md
* Critique execution status: Complete
* Critique boundary: Exactly one final-candidate assessment; no further critique requested.

## Inputs and Criterion Boundary

* Caller requirements: Complete the local RPI correction on feat/loading-briefing-hax-531 / PR #538, covering the standalone law helper and full trailing punctuation runs after a sibling audit. Preserve source scope in src/, the locked test ownership/budget, no removals, existing pins, and the distinction between semantic and regression coverage. No push, Azure operations, force-push, heavy-suite execution or implementation in this critique.
* Canonical research: .copilot-tracking/research/2026-10-29/loading-briefing-review-correction-531-research.md, including Q1-Q3, C1-C8/W1, alternatives and accepted validation limitations.
* Planning inputs: The plan and phase-details paths above, including P01-T01, P02-T01, P03-T01 and P03-T02.
* Supplied source pointers inspected: src/api/src/zava_forward/api/web/law.js; src/api/src/zava_forward/api/web/law.html; the bootstrap/direct-consumer portion of src/api/src/zava_forward/api/web/app.js; src/core/src/zava_forward/core/ai_tasks.py; src/core/tests/test_ai_statement_sources.py; the loader fixtures in src/api/tests/test_workspace_scripts.py; relevant portions of src/api/checks/loading_briefing_browser_check.py; src/api/README.md; src/api/pyproject.toml; src/core/pyproject.toml; and the local-gate explanation in src/README.md.
* Project context: docs/case_study_48_original.md, relevant introductory addendum/index material and docs/reference/memory.md. These do not establish additional customer facts or implementation acceptance.
* Decisions and dependencies: Retain native law reload, bounded existing workspace recovery, the shared parser terminator and conservative abbreviation handling. P01/P02 follow the completed research; P03 follows both. Heavy admission is nonblocking, with targeted fallback and explicitly unmet full/browser checks when unavailable. Publication and hosted/human acceptance are excluded.
* Assessment boundary: Assess the entire supplied candidate once for requirements, evidence, phases, tasks, dependencies, acceptance, decisions, risks and missed concerns. Do not reopen research, redesign the solution, alter locked budgets or infer passing checks. Read-only git inspection confirmed the named topic branch and existing untracked parent artifacts; none was changed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1-C4, P01-T01: Complete helper sibling audit | Covered | Research identifies both direct consumers and HTML loaders before edits; the plan addresses law handler/run and workspace handler/run/feedback rather than only the reported page. |
| C2-C3, P01-T01: Standalone terminal recovery | Covered | Readiness precedes binding/read; native reload, live error, disabled inert controls, prevented submission and no helper reinjection are explicit. |
| C4, P01-T01: Workspace compatibility | Covered | Partial-interface fixtures, no premature service work/listeners and preservation of bounded recovery are required. |
| C5-C6, P02-T01: Complete punctuation ownership | Covered | Shared relocation/splitting terminator, full runs, Unicode ellipsis normalization and unchanged abbreviation behavior are specified. |
| P02-T01: Semantic versus regression coverage | Covered | Full statement objects assert text, resolved citations and unresolved references; literal supplied failures supplement existing parameterized matrices. |
| C6-C7, P01-T01, P02-T01: Regression-first evidence | Covered | Both tasks require actual pre-edit failure and post-edit success, using real scripts/parser behavior rather than replacement implementations. |
| C7, P01-T01: Browser recovery coverage | Covered | Blocked, missing-global and partial-helper modes; no reads/page errors; keyboard reload; restored list, search, source and provision handlers are explicit. |
| P03-T01: Strict tools, units and heavy admission | Covered | API/core configurations remain authoritative; source-first paths, lock-owned environment mutation, full units/browser when admitted and disclosed targeted fallback are specified. Availability is not presumed. |
| C8, test ownership/change budget: Scope and pins | Covered | Existing canonical files and parameterization contain the additions; no removals or unrelated repins are proposed. |
| W1, P01-T01, P03-T02: Required current web-guideline checks | Partial | Research records a retrieval, but implementation and independent Review do not explicitly carry the required activation/refresh and changed-file assessment. PC-002. |
| P03-T02: One independent Review and final disposition | Partial | Original outcomes are preserved, but all residual findings are routed to later work without a blocking/nonblocking distinction. PC-001. |
| P03-T02: Local-only delivery and acceptance limits | Covered | Authenticated local identity, Conventional Commits/trailer, retained original evidence and no publication/hosted/human acceptance claims are explicit. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The implementation design, sibling scope and bounded tests are credible. Two direct planning corrections are needed to prevent an unresolved blocking Review defect from being treated as completed work and to make the required web assessment executable. Neither correction changes the locked source/test budget or requires a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Unconditional deferral of residual Review findings can leave the correction incomplete

* Related IDs: P03-T02; caller requirement to complete the correction round; plan Goals and Acceptance Criteria.
* Evidence: .copilot-tracking/details/2026-10-29/loading-briefing-review-correction-531-phase-details.md, P03-T02, says to route "any residual Review findings as later work without another Review." The plan requires correcting both reported failures and preserving existing behavior, but provides no exception for a blocking in-scope defect discovered by that Review.
* Concern: The single-Review limit is appropriate, but it does not authorize leaving a newly verified correction defect unresolved. The current instruction makes a broken readiness path, citation regression or failed required acceptance condition eligible for blanket deferral.
* Impact: Implementation could be committed and presented as complete even when the sole independent Review establishes that the requested outcome is not met.
* Smallest useful change: Distinguish blocking in-scope defects from nonblocking or unrelated follow-ups in P03-T02. Preserve the original Review verdict. Correct blocking in-scope defects on this branch and run their affected existing checks, without commissioning another Review. Record any such later fix as post-Review validation, not a fresh independent acceptance. If a blocking defect cannot be resolved within the authorized scope, stop with an explicit incomplete/blocked disposition rather than claiming completion. Defer only nonblocking/unrelated items with reasons.
* Action owner: Planning parent.
* Exact resolving evidence: The plan and P03-T02 consistently state the blocking/nonblocking disposition rule, the no-second-Review boundary and the distinction between original independent outcome and later targeted validation. Subsequent implementation evidence must enumerate Review findings and their resolution or explicitly unmet status.
* Decision route: Direct planner correction. The current request already authorizes completing in-scope fixes and limits the lifecycle to one Review; no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The required web-guideline activation and review refresh are absent from execution tasks

* Related IDs: W1; P01-T01; P03-T02.
* Evidence: .copilot-tracking/research/2026-10-29/loading-briefing-review-correction-531-research.md records web-design-guidelines and a dated W1 retrieval. P01-T01 plans web edits without an explicit pre-edit activation/current-source step, and P03-T02 plans independent Review without a fresh retrieval and changed-web-file assessment. Applicable repository web guidance requires those execution-time steps; a research citation is not evidence that the later reviewer performed them.
* Concern: An implementer or reviewer following the candidate literally can omit the required current web rules and their reporting contract, despite changing native error, focus and reload behavior.
* Impact: The terminal recovery can receive engineering validation without the required scoped web review evidence. A copied research retrieval must not be presented as a fresh review of changed files.
* Smallest useful change: Add the pre-edit web-design-guidelines activation/current-source requirement to P01-T01 and a fresh retrieval plus changed-web-file assessment to the existing single independent Review in P03-T02. Require file:line findings and disclosure of failed/partial retrieval or unperformed checks. Reuse the existing Review/evidence artifacts; do not introduce a second review, a broader UI audit, redesign, new tests or a larger test budget.
* Action owner: Planning parent; implementation owner and the already-planned independent reviewer execute their respective steps.
* Exact resolving evidence: The plan/details name both execution points and their evidence requirements. Implementation evidence subsequently records the pre-edit source status, and the original independent Review records its own refresh, changed-file coverage, findings and limitations.
* Decision route: Direct planner correction. This implements an existing scoped repository requirement and does not require user input.

## Strengths and Residual Risk

* The supplied research has already performed the requested sibling audit. Its two-consumer inventory and shared parser ownership justify bounded corrections rather than a loader refactor or tokenizer replacement.
* Existing full-object matrices provide a strong home for mixed punctuation, closers, whitespace and unresolved citations within the locked budget. The browser function can be parameterized rather than duplicated.
* Native recovery is explicitly independent of the failing helper; the plan also preserves no-read-before-readiness and prevents dead-form navigation.
* Heavy-suite availability is an explicitly accepted validation uncertainty, not an implementation assumption. Busy admission must leave full/browser checks unmet, avoid shared environment mutation and use the authorized targeted fallback without queuing.
* Package-level strict commands use existing configurations. Those configurations contain pre-existing migrated-module exclusions; a green command is not proof that every line of ai_tasks.py is individually type-checked/formatted. No exemption expansion or unrelated typing cleanup is requested.
* Local tests, browser/axe observations and local commits do not establish human usability, screen-reader/voice, live-site, hosted or publication acceptance. No complete publication gate is claimed for this no-push task.

## Questions or Blocking Evidence Gaps

* None requiring user clarification. Both findings are planner-owned corrections supported by existing direction.
* Tool/browser/lock availability remains an execution-time fact to record, not a missing fact that requires another research or critique loop.

## Limitations

* No source changes, tests, heavy suites, browser sessions, remote operations or fresh guideline retrieval were performed in this bounded plan critique.
* The supplied research's complete inventory and prior reproductions were assessed as supplied evidence, not rerun or expanded into another discovery pass.
* This assessment establishes planning credibility, not implementation correctness. Only the requested critique artifact was written; existing research, plan, phase details and state remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Apply the two direct plan/detail corrections, record their disposition against this original critique and finalize the plan without another critique.
* User response required: No.

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly, preserve this original Revise verdict and continue the already-authorized RPI lifecycle after finalization. No user command or response is required. Do not reopen research or commission another plan critique.
