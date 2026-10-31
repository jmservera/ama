---
title: Browser asset matcher final-candidate plan critique
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: pr-594-browser-asset-matchers-568
* Task slug: browser-asset-matchers-568
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md
* Critique execution status: Complete
* Assessment count: exactly one final-candidate critique
* Source disposition: read-only; only this critique artifact was written

## Inputs and Criterion Boundary

* Caller direction: correct PR #594, Refs #568, on fix/employee-chat-cache-568 through ordered RPI stages; local commit only; no push, Azure or secrets; pip-installed src packages; serialized heavy browser/tests; Ruff lint/format and relevant tests. This assessment does not authorize implementation, another critique or another agent.
* Candidate inputs: .copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md, .copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md and .copilot-tracking/research/2026-10-30/browser-asset-matchers-568-research.md.
* Necessary cited source: .github/workflows/src-ci.yml:93-116; src/api/checks/workspace_scripts_browser_check.py:60-354; src/api/checks/loading_briefing_browser_check.py:57-155; src/api/checks/employee_workspace_browser_check.py:39-143; asset routing and wait locations in src/api/checks/chat_widget_browser_check.py, src/api/checks/case_journey_browser_check.py and src/api/checks/case_view_ux_browser_check.py; src/api/checks/asset_cache_browser_check.py:73-162; src/api/src/zava_forward/api/static_assets.py:19-54; src/api/tests/test_static_assets.py:43-83; src/api/tests/test_ui_support.py:45-46; src/api/pyproject.toml; src/README.md.
* Repository context considered: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory is context, not evidence for a company or technical claim.
* C7 observation: the supplied external baseline-ci.log was read at its research-recorded location. Its traceback independently confirms the case-journey fallback timeout at src/api/checks/case_journey_browser_check.py:1489. This assessment did not repeat the baseline or retrieve hosted evidence.
* Locked decisions: one standard-library helper, seven existing harnesses, one new test file, no removals, at most six independently named test methods, related API guide, exact canonical asset suffix and optional version-directory/query/fragment matching. No application asset-generation or UI change.
* Acceptance boundary: AC1-AC5, C1-C7, P01/P02 and all four task IDs; dependencies, risks, evidence ownership and local-only closeout. The assessment judges implementation readiness, not completed tests, release acceptance, hosted approval, live employee behavior or served segment-version URLs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller scope, AC5 | Covered | Existing branch and local-only RPI evidence/commit boundary are explicit; Refs only; no publication or issue-closure claim. |
| AC1, C1, C5, C7 | Covered | Workflow source and supplied baseline traceback substantiate the exact fallback failure before source edits. |
| C2-C5, P01-T01 | Covered | Seven named targets cover routes, unrouting, waits, response/failure observations, DOM identification and companion coverage. Bare API routes remain excluded. |
| Matcher precision, AC2, P01-T02 | Covered | Canonical vendor suffix, filename/path negatives and query spoofing are required; native route/wait and JavaScript parity tests complement classification. |
| CDP/original lexical assertions, C2, AC2 | Covered | Preserve same-origin filtering, duplicate-script rejection, original roleScreensView lookup and evaluation/view counts; fixture extraction checks complement actual harness regression evidence. |
| C3, C6, cache assertions | Covered | StaticAssets.headers and byte-derived ETags justify replacing the stale Leaflet no-store assertion, not deleting MIME, length or warm-cache assertions. |
| Test ownership/change budget | Covered | One new test file and six-method limit can accommodate parameterized matrices and native/fixture semantics without removing existing tests. |
| AC3, P02-T01 | Partial | Original three-command sequence and all seven affected harnesses are enumerated; execution-location prerequisites require PC-001 and traffic enforcement requires PC-002. |
| AC4, P02-T02 | Partial | Targeted suites, API Ruff, isolated checks and typing are identified; heavy test execution also depends on PC-001. Baseline typing discrepancies must not absorb new errors. |
| Heavy-lock/scratch/output dependency | Missing | PC-001: the prescribed execution paths are not compatible with the current file-location constraint. |
| Synthetic-only/external-traffic boundary | Partial | PC-002: existing shell context lacks external-traffic blocking; context-level handlers also cannot alone constrain higher-priority page asset routes. |
| Ordered critique/Implement/Review handoff | Covered | One critique precedes implementation, one independent original Review follows, and local commit comes after original evidence preservation. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low
* Rationale: the correction strategy, preservation rules and semantic-versus-regression split are credible. Two executable validation prerequisites need planner disposition before the candidate can be treated as ready. Neither finding calls for an asset-serving redesign, a larger test budget or another critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Resolve execution-location constraints without losing the shared heavy lock

* Related IDs: non-functional heavy-lock requirement; task-owned environment/output dependencies; AC3, AC4; P02-T01, P02-T02.
* Evidence: the plan prescribes flock -w 600 /tmp/ama-rpi-heavy.lock and generated outputs in external session files; phase details require fresh external outputs. src/README.md identifies the same host-wide lock as the coordination contract. src/api/checks/asset_cache_browser_check.py:83 and src/api/tests/test_ui_support.py:46 use default tempfile directories. The current execution context disallows file operations in temporary directories and requires newly created files to be project-relative.
* Concern: future validation commands would open the prescribed disallowed lock path, write external outputs and, unless explicitly configured, create default temporary fixture/browser files. The already-recorded baseline does not establish that these future operations are permitted. The dependency list nevertheless declares all prerequisites available.
* Impact: AC3/AC4 cannot be performed as written in this execution context. Substituting an unrelated project-local lock would also break serialization with other heavy runners; an apparently passing run would not resolve that requirement.
* Smallest useful change: the planning parent must disposition the execution-location conflict before validation. Specify a permitted execution context and concrete scratch/output/environment configuration that retains coordination with the actual shared heavy lock, or mark P02 blocked until such a context is established. Do not simply rename the lock, run unlocked, reproduce the baseline again or weaken the restriction. Preserve historical baseline evidence unchanged.
* Action owner: planning parent for dependency/command disposition; Implement owner for subsequent execution in the established context.
* Exact resolving evidence: revised plan/details state the allowed lock-entry mechanism or execution context, concrete allowed output/scratch locations and how Python fixtures and browser child processes inherit them. Evidence must demonstrate coordination with the existing heavy-lock contract, rather than merely name another lock. If that cannot be established, explicit blocked P02 readiness and an unperformed-validation disclosure resolve the misleading readiness claim, but not AC3/AC4.
* Decision route: direct planner correction and environment prerequisite. No divergent product decision or user permission to bypass the current restriction is requested. If no permitted execution context is available, return the execution blocker to the parent rather than claim validation.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make the promised external-traffic boundary executable

* Related IDs: non-functional synthetic-loopback/external-traffic requirement; P01-T01, P01-T02, P02-T01; AC2, AC3.
* Evidence: src/api/checks/loading_briefing_browser_check.py:57-96 creates shell_check's browser context without a local-only context route. Other affected contexts use context-level local-only routing, while asset fault injection is registered with page.route. The selected helper intentionally accepts absolute HTTP(S) URLs without binding an origin. Phase details attribute loopback readiness, sanitized server environment and cleanup to the existing helper, but do not specify per-context traffic enforcement.
* Concern: expected loopback navigation and sanitized server environment are not an enforced external-traffic block. Furthermore, a matching page asset route takes precedence over a context route; a cross-origin URL with the same canonical suffix can enter its callback instead of reaching the context block. Matching arbitrary origins is valid for the reusable classifier, but does not itself enforce the harness's origin boundary.
* Impact: all listed modules could pass while the stated external-application-traffic control remains unproven. Synthetic fixtures should not silently depend on whether a scenario happens to avoid external requests.
* Smallest useful change: add an explicit bounded disposition for external-traffic handling in every affected browser context, including shell_check. Keep the helper origin-independent; ensure page asset callbacks reject non-local requests or delegate them to the local-only guard before abort/hold/continue behavior. Make the native browser test context fail closed for unexpected requests. This is harness plumbing, not an application or UI change.
* Action owner: planning parent to specify the control and validation; Implement owner to apply it within existing owned harnesses.
* Exact resolving evidence: revised P01/P02 details identify the guard and callback precedence strategy. The post-implementation Review verifies the affected context constructors and asset callbacks; a bounded native test within the existing six-method budget demonstrates that an off-origin canonical-looking asset cannot be continued to the network, while same-origin bare/query/segment routing and waits still work. Existing retry, coverage and cache assertions remain unchanged.
* Decision route: direct planner correction implementing the candidate's already-declared non-functional requirement. No significant or divergent user decision is needed.

## Strengths and Residual Risk

* The source-backed and observed CI failure is specific: versioned enhancement loading bypasses the original fallback injection, not an unspecified browser flake.
* Anchored canonical suffix matching is better bounded than filename globs; the chosen vendor-path and query-spoofing negatives address real overmatching risks.
* Preservation of fault counts, exact retry identity where asserted, same-origin CDP coverage and original lexical functions avoids passing by removing the behavior under test.
* The Leaflet correction follows the actual revalidation/ETag contract and retains the 147552-byte/MIME/body-length checks.
* Mocked CDP fixtures establish filtering/count-extraction semantics, not actual V8 execution. Actual original-function execution remains established by existing real-browser harness assertions; this distinction must be maintained in the changes and Review evidence.
* Synthetic segment URLs establish matcher compatibility only. The explicitly accepted absence of production segment serving, full publication-gate evidence, hosted rerun and live/human acceptance is appropriate for this local-only correction.

## Questions or Blocking Evidence Gaps

* No unresolved product question requires a user response.
* PC-001 is an execution prerequisite, not missing evidence about the matcher root cause. A permitted shared-lock execution context must be established or validation must remain blocked.
* No additional findings are withheld for another pass. The parent should dispose this complete set directly.

## Limitations

* No source implementation, browser execution, lint, type check, package installation, commit, remote write or additional agent was performed.
* The provided baseline traceback was checked; this critique does not claim an independent full hosted-log review or reexecution of every baseline command.
* Exact future regex syntax and test code do not yet exist. Their delimiter handling and Python/JavaScript parity must satisfy the plan's negative matrix; this assessment does not preapprove an arbitrary implementation.
* Dirty worktree entries are the supplied new RPI artifacts. They were not moved, committed or altered.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: revise P02 prerequisites to establish permitted shared-lock execution and output/scratch handling, or explicitly mark validation blocked; then disposition PC-002's bounded traffic guard.
* User response required: no.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md | Assessed final candidate; unchanged. |
| .copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md | Assessed implementation and validation details; unchanged. |
| .copilot-tracking/research/2026-10-30/browser-asset-matchers-568-research.md | C1-C7 research and original baseline pointer; unchanged. |
| .copilot-tracking/reviews/plans/2026-10-30/browser-asset-matchers-568-plan-critique.md | This single complete critique and actionable finding set. |

## Next Steps

The active planning parent disposes PC-001 and PC-002 directly, records the
resolution or execution blocker, and finalizes without another critique.
Implementation and validation may proceed only after the corresponding
prerequisites are resolved. No user action is required. This critique stops here.
