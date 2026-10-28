<!-- markdownlint-disable-file -->
# RPI Plan Critique: employee-case-workspace

## Metadata

* Task ID: employee-case-workspace
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md
* Critique execution status: Complete
* Execution boundary: exactly one final-candidate plan critique; no implementation review or additional agents.

## Inputs and Criterion Boundary

* Caller requirements: full RPI continuation with source fixes and synthetic tests, normal topic-branch push and a PR using Refs rather than Closes; no deployment, private datasets, .env, secrets, uv or full gate. This invocation writes only this critique.
* Supplied evidence: the plan, phase details and .copilot-tracking/research/2026-10-27/employee-case-workspace-research.md, especially C1-C5 and W1-W3.
* Read-only corroboration: src/api/src/zava_forward/api/web/index.html; app.js; role-screens.js; chat.js; src/api/checks/design_system_browser_check.py; src/api/tests/test_ui_support.py; test_auth.py; test_ai_tasks.py; src/core/src/zava_forward/core/store.py; ai.py; identity.py; relevant component README and configuration excerpts.
* Repository context: original case study, addendum, knowledge-base index and owner memory. Existing artifacts are evidence to assess, not proof of their own assertions.
* Decisions and dependencies: existing topic branch, locked canonical targets, no test removals, at most eight added unittest methods and one browser module with at most three scenarios; pip-installed src distributions and existing Chromium. No expansion of that lock is recommended.
* Acceptance boundary: AC1-AC6, functional and non-functional requirements, P01-T01, P01-T02 and P02-T01, including error recovery, assignment scope, authorization preservation, configuration documentation and honest publication.
* Source inspection confirms the route-only retry and exact owner-code selection. Deployment/image observations remain supplied research evidence, not independently repeated management-plane or authenticated-browser measurements.
* Read-only branch inspection found fix/employee-case-workspace-qualitypanel tracking origin/main and no matching PR returned by the head-branch query. Existing untracked RPI inputs were left untouched.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C2; P01-T01; AC1/AC2 | Partial | A pre-render check and document reload address a real source defect, but the proposed all-route dependency set includes route-specific features; PC-001. |
| Generic API retry; URL/session preservation; P02-T01 | Partial | Explicit requirements lack corresponding negative-control and query-preservation assertions; PC-002. |
| AC3; C1; P02-T01 | Covered | Shell aliases, exact asset bytes, JavaScript MIME, CSP, no-store and trusted-proxy protection are named. Synthetic proxy headers stay loopback-only. |
| C3/C4; P01-T02; AC4 | Covered | JSON/SQLite assignment coverage, closed-case exclusion and unique tenant/object-ID continuity preserve scope without email-based ownership inference. |
| C5/W1; P01-T02; AC5 | Covered | Endpoint, both deployment tiers, model attestations, managed identity, network and independent release/incident prerequisites are named. Missing endpoint must produce template evidence with zero model calls. |
| P02-T01; validation dependency and test lock | Partial | Existing suites and harness make the bounded checks credible, but the interpreter dependency is under a prohibited path; PC-003. |
| Native semantics, focus and reflow | Covered | Keyboard recovery and 320/390/1280px checks are planned without claiming WCAG or user acceptance. Preserve these assertions when resolving PC-001/PC-002. |
| W2/W3; AC6; publication and later Review | Covered | Original live cause and current owner mapping remain unproven; no deployment, whole-issue closure or self-approval is claimed. Independent implementation Review remains a later parent-owned stage. |
| Caller restrictions | Partial | No full gate is the confirmed task direction, not a critique blocker. Forbidden scratch/interpreter paths still need correction under PC-003. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the bounded recovery and wording/runbook changes are supported by source evidence. However, the proposed guard can turn a route-specific failure into a wider outage, important recovery distinctions are not explicitly verified, and the named validation environment is unusable under current path restrictions.
* This is the complete actionable finding set for the supplied boundary. The planning parent should resolve it directly and finalize without another critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The readiness guard makes unrelated features prerequisites for every route

* Related IDs: P01-T01; AC1/AC2; normal-path preservation and manual-path non-functional requirements.
* Evidence: .copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md, P01-T01, requires checking panels, ops, assistants, chat, timecapture, role-screens and Leaflet before dispatching a route. src/api/src/zava_forward/api/web/app.js:143-181 dispatches routes separately; caseView uses case helpers, whereas Leaflet is used by mapPanel at line 1015 onward. src/api/src/zava_forward/api/web/role-screens.js defines the separate roleScreensView destination.
* Concern: the plan treats every loaded file as required for every destination. A failed vendor/leaflet.js or role-screens.js would therefore prevent an otherwise functional ordinary case or case-list view. The existing dispatch does not require either feature to enter those views. Loading scripts in the same shell does not establish an all-or-nothing runtime dependency.
* Impact: the repair would enlarge the failure domain, removing useful case/list manual paths during an unrelated asset failure rather than merely preventing a misleading partial case workspace.
* Smallest useful change: define the required export/path set for each affected route before guarding it. Retain the full case-helper guard where the case actually uses those helpers, but do not globally require map or specialist-screen dependencies for ordinary case/list routes. Missing dependencies on the selected route should still show their exact paths and document reload; do not silently omit required case controls.
* Action owner: planning parent.
* Exact resolving evidence: revised P01-T01 and acceptance wording explicitly distinguish common, case and route-specific dependencies. The locked browser module includes an unrelated-dependency failure assertion proving an ordinary case/list remains usable, alongside the affected-route named-error/reload assertion where applicable. Existing ops failure and same-case recovery assertions remain.
* Decision route: direct planner correction. This preserves current working paths and narrows the proposed fix; it does not require new user authority or a broader graceful-degradation redesign.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The browser verification does not distinguish document recovery from ordinary API retry

* Related IDs: P01-T01; P02-T01; AC2; generic API retry and hash/query/session preservation requirements.
* Evidence: the plan requires generic API errors to retain existing route retry. The phase details additionally require preserving hash, query and session, but their browser recipe verifies missing ops, another missing helper, keyboard reload and fragment preservation only. src/api/src/zava_forward/api/web/app.js:182-186 currently renders Try again with onclick: route; document reload is intentionally a different action.
* Concern: a change that replaces generic API retry with document reload could satisfy the listed missing-script tests. Likewise, a recovery that drops location.search could pass a fragment-only assertion. Neither existing healthy-path coverage nor static shell query-parity tests exercise these behavioral distinctions.
* Impact: the new handler could unnecessarily restart a healthy document on a transient API failure or lose deep-link query context while all specifically listed browser assertions pass.
* Smallest useful change: extend the existing planned scenarios, without adding a fourth scenario or increasing unittest limits. In a healthy-assets scenario, fail one case API response, restore it, activate Try again by keyboard and prove recovery without a new document/script fetch. In the ops-failure scenario, start with both a non-empty search string and a deep-link fragment; assert the reload refetches ops, preserves the complete URL context and retains the authenticated session without signing in again.
* Action owner: planning parent.
* Exact resolving evidence: P02-T01 explicitly names the API-failure negative control, document/script request-count or navigation assertion, full search/hash equality and session continuity assertion. The planned maximum remains one browser module and three scenarios, with no test removals.
* Decision route: direct planner correction. These assertions verify already-promised behavior rather than adding product scope.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The validation dependency points into a forbidden filesystem location

* Related IDs: plan Dependencies; P02-T01; synthetic-only and reproducible validation requirements.
* Evidence: .copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md names installed pip distributions in /tmp/ama-emp-ui-20261027. Current execution instructions prohibit file operations in /tmp or temporary directories and require scratch files under the project. The plan's bare python3/browser commands do not identify a permitted replacement interpreter. The existing browser harness already places its owned scratch below the repository's .venv directory.
* Concern: treating that external environment as an executable prerequisite would require prohibited filesystem access and leaves the advertised test commands without a usable, explicit permitted environment. The historical research statement can remain as provenance, but cannot define the next validation environment.
* Impact: implementation may be complete yet the focused tests cannot be run as planned, or validation may inadvertently use a different interpreter than the installed src distributions and browser tooling.
* Smallest useful change: replace the active dependency with an explicit project-local interpreter/environment and project-local scratch/cache prerequisites. Probe existing permitted dependencies first; restore/install with pip only following a missing-dependency failure, as required. Keep historical research unchanged and keep the no-uv/no-full-gate decisions. Treat the referenced /tmp/brief-common.md as supplied provenance, not a file to retrieve.
* Action owner: planning parent.
* Exact resolving evidence: revised Dependencies and P02-T01 name a repository-local interpreter, give commands using it consistently from src/api, and identify repository-local scratch configuration for tests that use tempfile defaults. No command reads, writes or executes files under the forbidden locations; dependency restoration remains conditional.
* Decision route: direct planner correction. Current instructions already settle the location constraint; no user decision or expanded tooling budget is needed.

## Strengths and Residual Risk

* The supplied image evidence refutes the simple missing-ops wiring hypothesis: revision 0000006 already includes ops.js before app.js and its bytes match source. The plan does not substitute a speculative wiring change for a demonstrated defect.
* Synthetic successful rendering of ZF-2026-0597 does not prove the owner's original live request succeeded. The exact authenticated request/execution failure remains an explicitly disclosed owner/operator follow-up.
* The observed route-only retry cannot refetch an absent script. A bounded, user-triggered document reload is a supported recovery repair, not proof that the original live cause has been diagnosed.
* Assignment wording is tightly scoped to a template. Exact owner_code equality and closed-case exclusion remain unchanged; an authorized all-case view is not personal assignment. No automatic ownership or role grant is proposed.
* Employee AI configuration is correctly separate from resident assistant configuration and activation authority. Source-required setting names and model attestation requirements do not establish that an actual model release is approved or live.
* The test ownership, zero-removal rule and maxima are retained. The findings can be addressed inside those limits by using assertions/subtests within the planned tests.
* No full gate is requested here because the caller explicitly excluded it. Passing focused checks must not be presented as a full-gate receipt, live acceptance or authorization to deploy.

## Questions or Blocking Evidence Gaps

* No user response is required for PC-001 through PC-003.
* An authenticated deployed network/console capture and permitted current owner mapping remain unavailable. They prevent an exact original live root-cause claim, but do not block the bounded source correction when that limitation remains disclosed in changes, Review and PR.
* No real inference, model release, managed-identity/RBAC, Azure SQL or deployed regression acceptance can be inferred from the proposed local checks.

## Limitations

* This assessment read the supplied final-candidate inputs once as a single critique; it did not inspect a future implementation or run tests.
* Azure observations, hashes and the prior browser run were assessed as supplied research claims. No authenticated HAR, deployment or private-data access was performed.
* Relevant source was inspected read-only to test plan credibility, not to audit the entire application or establish accessibility conformance.
* No fresh Web Interface Guidelines review was performed: this is a plan critique, not web editing or implementation review. The later implementation/review must load and refresh the required source under repository guidance.
* No file other than this critique was intentionally changed. Existing plan, details, research and other RPI records remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: revise P01-T01 to use actual route dependencies, then incorporate PC-002 assertions and PC-003 validation prerequisites in the same finalization.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md](.copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md) | Assessed final-candidate plan; unchanged. |
| [.copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md](.copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md) | Assessed task details and verification design; unchanged. |
| [.copilot-tracking/research/2026-10-27/employee-case-workspace-research.md](.copilot-tracking/research/2026-10-27/employee-case-workspace-research.md) | Supplied C1-C5/W1-W3 evidence and explicit live limitations; unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-27/employee-case-workspace-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/employee-case-workspace-plan-critique.md) | This single Complete / Revise critique. |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly,
record their disposition without rewriting this original critique, and finalize
the plan without a second critique. Continue implementation and the separate
independent implementation Review only under the caller's existing boundaries.
No user action is required.
