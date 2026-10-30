---
title: Employee chat skills 530 final-candidate plan critique
description: Independent assessment of the bounded employee chat implementation plan
ms.date: 2026-10-29
---

## Metadata

* Task ID: 530 / employee-chat-skills-530.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md.
* Critique execution status: Complete.
* Assessment count: One independent final-candidate assessment. No delegation,
  implementation, source revision, commit, push or az invocation performed.

## Inputs and Criterion Boundary

* Caller requirements: one read-only employee ChatPanel, the five
  assistants.REGISTRY skills and general work help, native employee-wide dialog,
  existing role/case projection and privacy gates, minimal audit, API/core
  Ruff/format/mypy/units and browser/axe, separately qualified SQL/live evidence,
  local commits only and no push or az.
* Candidate evidence: the supplied plan and phase details; C1-C6 and the
  decisions in
  .copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md.
* Source verification: src/core/src/zava_forward/core/chat_panel.py,
  chat_isolation.py, chat_privacy.py, chatthreads.py, assistants.py and
  export_fields.py; src/api/src/zava_forward/api/server.py; employee
  web/app.js, web/chat.js, web/index.html and web/async-action.js.
  Source filenames abbreviated in this bullet share the immediately preceding
  full directory.
* Validation evidence considered: src/core/tests/test_chat_panel.py,
  src/api/tests/test_chat_panel.py, src/core/tests/test_chatthreads.py,
  src/api/tests/test_mssqlstore.py, src/api/checks/design_system_browser_check.py,
  src/api/checks/case_journey_browser_check.py,
  src/api/checks/regulatory_ux_check.py, API/core pyproject.toml,
  src/README.md and tools/rpi-checks.py.
* Project context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory supplies context, not acceptance evidence.
* Decisions and dependencies: explicit selection rather than model routing;
  no new tools, provider SDK or proposal authority; preserve legacy callers,
  the case panel and regulatory panel; retain independent Review and original
  adverse evidence. P02 depends on the P01 wire contract; P03 verifies both.
* Boundary: assess implementation credibility and planned evidence, not actual
  runtime correctness, legal approval, live inference quality, SQL success or
  accessibility conformance. No tests or external research were executed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C3 / P01-T01: single model, projected sources and advisory skills | Partial | Appropriate reuse; general/legacy request distinction needs PC-002. |
| C4 / P01-T02: authorization, ownership and privacy gates | Covered | Per-turn current-user/case checks and unchanged privacy references are explicit; no proposal call is authorized by selection. |
| P01-T01: minimal audit | Covered | Thread/question reference, selected skill and outcome without content are specified; implementation must use the actual persisted question sequence. |
| C5 / P02-T01: native global dialog and context lifecycle | Partial | Route reset is planned; session expiry and late completion require PC-001. |
| P02-T02: existing case/regulatory UI and shared feedback | Covered | Preservation, native semantics, Fluent tokens and AsyncAction reuse are explicit. |
| C6 / P03-T01: browser, synthetic data and missing-model behavior | Partial | Constructed server is suitable; it does not itself supply dialog axe coverage, PC-003. |
| P03-T02: API/core static and unit suites, shared lock | Partial | Required checks are named, but the specified execution paths need PC-004. |
| P03-T02: actual SQL versus SQLite/mocks/live | Covered | Separate evidence and owned disposable SQL are explicit; no successful run is yet established. |
| P03-T03: documentation, local commits and independent Review | Partial | Correct local-only direction; final-gate disposition needs PC-005. |
| Acceptance criteria: isolation, citations, failure and unchanged case | Covered | Existing ownership is retained and these semantic checks are explicitly required. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 3 Medium, 0 Low.
* Rationale: The architecture is appropriately bounded. Five actionable planning
  gaps remain around session cleanup, explicit request modes, accessibility
  evidence and executable validation. They are direct planner corrections, not
  reasons to introduce a router, widen data access or seek a new scope decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Dialog invalidation does not cover session expiry

* Related IDs: C5, P02-T01, P03-T01, authorization/context acceptance criteria.
* Evidence: The phase details require navigation to close/remove the dialog
  and hide its launcher before login. In
  src/api/src/zava_forward/api/web/app.js, api() handles a 401 by setting
  me to null and calling login(); login() replaces the main workspace and hides
  existing navigation/account elements. These are separate from route(), which
  aborts the route controller. A new shell-level dialog is not automatically
  disposed by replacing main content.
* Concern: The plan addresses route changes but not a login/session-expiry
  transition while chat is open, a permission/case denial on the next turn, or
  a delayed completion after disposal. Hiding a launcher is not the same as
  clearing a visible dialog or its retained transcript.
* Impact: Previously displayed case answers could remain visible at sign-in,
  or a late answer could update an obsolete dialog/session. Server-side
  authorization alone does not clear already rendered sensitive content.
* Smallest useful change: Extend P02-T01's disposal contract to session
  invalidation/account transition and relevant authorization/case denial.
  Close/remove the dialog, discard its transcript/thread/context references
  and suppress completions from its old session/context generation. Do not
  introduce polling or a new identity subsystem.
* Action owner: Planning parent, with implementation owned by P02-T01.
* Exact resolving evidence: Revised phase details and browser assertions for
  an open dialog receiving session-expiry/denial, plus a delayed successful
  response released after disposal. No old answer, transcript or stale focus
  update may appear in the sign-in or replacement context.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: General help has no explicit legacy-compatible wire mode

* Related IDs: C1-C2, P01-T01, P01-T02, five-skills/general acceptance criteria.
* Evidence: The phase details say to use an optional skill argument and
  preserve legacy no-case behavior. Currently
  src/api/src/zava_forward/api/server.py passes content only to ChatPanel.ask();
  src/core/src/zava_forward/core/chat_panel.py deliberately abstains without
  case sources. In src/core/src/zava_forward/core/chatthreads.py,
  chat_create_thread() accepts nonempty task values only from
  assistants.REGISTRY; general help is not one of those five task IDs.
* Concern: The candidate does not distinguish an omitted legacy skill from an
  explicitly selected general-help mode at the HTTP/service boundary, or say
  how that mode relates to the existing thread task field. A default alone
  cannot both preserve legacy no-case abstention and enable new general help.
* Impact: An implementation could unintentionally change legacy callers,
  leave the new general option abstaining, or persist an invalid task ID.
* Smallest useful change: Specify the accepted ask request shapes and explicit
  general selector value, omission behavior and invalid/null/type behavior.
  Keep the existing thread task schema unless a change is separately justified;
  define how the per-turn selection is recorded in minimal audit. General
  citations must identify trusted workflow knowledge, not imply case access.
* Action owner: Planning parent, P01-T01/P01-T02.
* Exact resolving evidence: A compact request/behavior table in the details
  and table-driven tests covering omitted legacy skill, explicit general with
  no case, all five registry IDs and invalid values. Invalid input must cause
  neither message persistence nor inference.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Reused browser harness does not establish global-dialog axe coverage

* Related IDs: C6, P02-T01, P03-T01/P03-T02, browser/axe acceptance criteria.
* Evidence: src/api/checks/design_system_browser_check.py main() provides the
  constructed server but does not execute axe. The scan() helper in
  src/api/checks/case_journey_browser_check.py:510-526 runs axe against
  document.querySelector('main'). The proposed launcher/dialog is shell-level,
  and src/api/src/zava_forward/api/web/index.html places the header outside main.
* Concern: The plan names browser/axe globally without specifying an axe target
  or invocation for the new open dialog. Reusing the server fixture or running
  existing main-only scans can pass without checking this new surface.
* Impact: Reported browser/axe success could omit the central new interaction,
  including its accessible name, controls, transcript and error states.
* Smallest useful change: Specify the new browser module's executable selector
  and pinned axe input. Scan the actual open dialog subtree or a documented
  whole-document scope that includes it, in the answer and failure states;
  retain separate keyboard/focus, narrow viewport and reduced-motion checks.
* Action owner: Planning parent, P03-T01/P03-T02.
* Exact resolving evidence: Revised details naming the invocation, axe scope
  and checked states; subsequent browser evidence must record axe as executed
  on the global dialog, not skipped or inferred from existing case scans.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Planned environment writes conflict with execution constraints

* Related IDs: P03-T02, shared-lock and validation dependencies.
* Evidence: P03-T02 explicitly installs editable distributions into /tmp/mv
  and uses flock -n /tmp/ama-rpi-heavy.lock. This execution context prohibits
  /tmp file operations. In addition, the fixed venv path is shared rather than
  issue-owned; editable installs mutate package/source bindings before the
  plan explicitly places suites under a lock.
* Concern: The validation recipe cannot be executed as written. Moving only
  the test process under the heavy lock would not protect a prior editable
  install from simultaneous shared-environment mutation.
* Impact: Execution may stop before required checks, or tests may use
  another worktree's installed package bindings. Creating a differently named
  private lock would not preserve shared heavy-suite exclusion.
* Smallest useful change: Choose an issue-owned persistent project-local
  environment and worktree-bound installation/test paths. Retain the canonical
  shared nonblocking exclusion contract; if its location cannot be used under
  the execution constraints, mark heavy checks blocked rather than silently
  substituting an independent lock or using forbidden paths. Any intentionally
  shared environment mutation must be serialized as well.
* Action owner: Planning parent, P03-T02.
* Exact resolving evidence: A permitted setup recipe naming environment and
  source paths, lock admission behavior and safe blocked disposition. Later
  logs must identify the tested worktree and separate completed targeted
  checks from unadmitted full suites.
* Decision route: Direct planner correction. Do not weaken exclusion or
  request permission to bypass execution constraints.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Final-gate disposition is not reconciled with the no-az decision

* Related IDs: P03-T02/P03-T03, local commit/Review and publication boundaries.
* Evidence: The plan mentions a complete publication gate only in Follow-Up
  Items, without an executable phase task or blocked disposition.
  src/README.md, Local RPI gate, separates committed-candidate receipts from
  focused checks and independent exact-head assessment. In
  tools/rpi-checks.py the full gate invokes az bicep version/build/lint and uses
  the canonical /tmp heavy lock. The user expressly forbids az and push.
* Concern: The plan does not state how local implementation/Review commits
  close out while the complete gate cannot run under the current constraints.
  A passing package/browser run is not a full receipt; offline az invocations
  are still az invocations.
* Impact: The parent could accidentally violate the no-az direction or
  overstate final gate/publication readiness after permitted local checks.
* Smallest useful change: Add the final-candidate evidence/disposition step
  after implementation and original Review commits. Preserve their original
  outcomes and record the full gate as blocked when its prerequisites require
  forbidden operations; do not invoke it, fake a receipt, alter gate tooling or
  push. Keep permitted scoped validation and separately qualified SQL/live
  evidence distinct from publication readiness.
* Action owner: Planning parent, P03-T03.
* Exact resolving evidence: Revised closeout sequencing and explicit blocked
  full-gate status in the planned changes/Review evidence, with local commit
  identity retained and no full-gate or live acceptance claim.
* Decision route: Direct planner correction under the already confirmed
  no-az/local-only decision; no new user response required.

## Strengths and Residual Risk

* One injected model call, explicit selection and no tool/proposal invocation
  keep this substantially smaller than a router architecture.
* Existing role projection, closed external-context allowlist and privacy
  references remain authoritative. Do not replace them with assistants.capture()
  or direct raw-store access to fill skill-specific knowledge gaps.
* assistants.REGISTRY contains categories that export_fields.chat_case() does
  not export, including funding, survey and quality records. Skill help must
  disclose those unavailable facts, not imply complete domain-record grounding.
  This is compatible with the selected bounded scope, not a request to widen it.
* Existing lexical refusal and citation checks do not prove semantic accuracy.
  The plan correctly avoids equating synthetic output with live quality.
* The twelve-method budget can accommodate table-driven/subtest matrices;
  it must not remove existing tests or replace distinct negative cases with
  presence-only assertions.
* SQL Server, live employee-site, screen-reader/voice-control and human
  acceptance remain separate evidence. Their success is not asserted here.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents planner revision. The user has already
  resolved routing, authority, local-only delivery and no-az boundaries.
* Heavy-suite admission and complete-gate execution remain runtime
  prerequisites, not evidence supplied with this plan. Their blocked status
  must not be relabelled as a pass.

## Limitations

* This is a plan critique, not an implementation/security/conformance audit.
  Source was read only to substantiate candidate risks.
* No browser, axe, SQL, unit/static suite, paid model, hosted or live check was
  run. The research's earlier web-guideline retrieval was not freshly repeated.
* The supplied changes artifact is a future handoff target, not an existing
  result considered by this critique.
* Only this critique artifact was authored; supplied plan, phase details,
  research and state were not changed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add session-bound dialog disposal and its delayed-response
  browser cases, then incorporate PC-002 through PC-005 in the same revision.
* User response required: No.
* Return this single complete finding set to the active parent. The parent
  should revise and finalize without another critique pass.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md](.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md) | Assessed candidate plan. |
| [.copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md](.copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md) | Assessed task details. |
| [.copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md](.copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md) | Supplied C1-C6 research and decisions. |
| [.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-critique.md](.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-critique.md) | Complete / Revise; five actionable findings. |

## Next Steps

The active planning parent should apply the five direct corrections, preserve
this original verdict, and continue the ordered local-only RPI work without
another critique, push or az. No user action is required.

## PR #541 correction pass critique

### Metadata and boundary

* Independent assessor: GitHub Copilot correction-pass critique sub-agent,
  separate from the planning parent; 2026-10-29.
* Execution status: Complete. Verdict: Revise.
* Exactly one assessment of task 530 / employee-chat-skills-530, research
  correction cycle 2 C7-C9, plan P04 and phase-details P04. Earlier PC findings
  and original Review outcomes remain historical and are not reassessed,
  replaced or marked resolved here.
* Inputs: .copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md:94-158;
  .copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md:120-159;
  .copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md:75-107.
* Criterion boundary: the three requested correction threads, one bounded
  sibling audit, deterministic proof design, test-addition budget, requested
  local checks and evidence limits. Read-only inspection confirmed PR #541 is
  open from the current feat/employee-chat-skills-530 branch to main.
* Existing dirty research, plan, details and state belong to the parent; they
  were neither moved nor edited. Only this critique section was appended.

### Coverage assessment

| IDs | Coverage | Evidence and assessment |
| --- | --- | --- |
| C7 / P04-T01 | Covered | chat.js:61-129 has metadata and submit catches covering metadata/thread/ask awaits. Shared current-only denial cleanup, 403/404 at each entry point, #app focus and preserved API-owned 401 login handling directly address the request. app.js:69-74,99-107 and index.html:42 support the proposed boundary. |
| C8 / P04-T02 | Covered | employee_chat_browser_check.py:112-133 currently permits absent arrival and abort instead of success; app.js:69 can discard even a successful transport response. P04 separately requires actual intercepted arrival and a controlled successful API promise ignoring abort, followed by awaited whole-form settlement. |
| C8 / disposal siblings | Covered | chat.js:38 and post-await guards bind dialog, session and abort state. Close, navigation/replacement and changed-session cases compare detached/current transcript, status and active element. async-action.js:40-82 returns task settlement; capture and await the outer form task, including its cleanup, as planned, rather than only resolving the held API promise. |
| C9 / P04-T03 | Covered | chat_panel.py:314-316 stores redacted content directly; chatthreads.py:322-323 rejects lengths above MAX_CONTENT. Planned final masked bound and reused prompt value restore the bounded write without altering the input contract. |
| C9 / regression siblings | Covered | One source audit included chat_isolation.py:115-119, chat_privacy.py:90-97,153-157 and existing core/API test owners. Legacy omitted skill, general and five registry skills share the write; parameterized expanding-postcode and sibling-identifier assertions fit the three-unit-method limit. Separate privacy/general and assistant-output bounds remain explicitly outside this correction. |
| P04-T04/T05 | Partial | Requested Ruff/format/mypy for core/API, core discovery, API chat/workspace selectors, feasible local browser/axe, independent Review and local trailer-bearing commit are specified. The temporary-path tooling instruction requires CP-PC-001. |
| Change and evidence limits | Covered | At most three new unit methods and two browser helpers; no removals, new dependencies or files. Synthetic fixtures, pinned axe, owned loopback server and nonblocking heavy admission are credible. Busy/unavailable browser evidence must remain blocked, not passed; no SQL, live/provider, deployment, human acceptance or publication receipt is inferred. |

### Complete actionable finding set

<!-- rpi:critique id=CP-PC-001 -->
#### CP-PC-001 [Medium]: Validation tooling path violates the execution boundary

* Related IDs: P04-T04/T05.
* Exact evidence:
  .copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md:100-104
  directs execution of installed /tmp/mv tools and session-external output.
  The current execution instructions prohibit any /tmp file operations and
  require newly created files to be workspace-relative. Prior availability of
  that environment does not authorize its reuse in this correction pass.
* Impact: the required validation recipe is not executable as written under
  the supplied constraints; implicit tool caches and synthetic-server output
  could also cross the prohibited boundary.
* Smallest useful change: replace that recipe with a permitted existing
  interpreter/tool environment and explicit workspace-relative output/cache/
  synthetic-data paths. If no permitted installed environment is available,
  record the affected checks as blocked; do not silently reuse /tmp, mutate a
  shared environment, add dependencies or claim a pass.
* Action owner: Planning parent.
* Exact resolving evidence: revised P04-T04/T05 names the permitted tool
  executable paths and workspace-relative write locations, including browser
  fixture/output and tool caches; subsequent validation records actual
  commands and outcomes or the concrete missing-environment blocker.
* Decision route: Direct planner correction; no new user decision required.

### Strengths, limitations and disposition

* No additional mandatory lifecycle, denial or bounds findings arise from
  this supplied boundary. The success-vs-abort distinction and full task
  settlement are explicit rather than inferred from a missing late answer.
* Preserve 401 sign-in focus and recoverable non-denial behavior; restore
  controlled wrappers after each browser case. Retain the real fallback,
  six-selection, keyboard/reflow/reduced-motion and pinned dialog-axe checks.
* This is planning credibility, not implementation acceptance or a fresh UI/
  accessibility conformance review. No implementation, unit/static/browser/
  SQL check, delegation, commit, push or az command was performed. Historical
  guideline retrieval and environment availability are supplied evidence, not
  newly verified results. Local-only correction evidence does not authorize
  publication or replace any required exact-head/publication/human gate.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Highest-impact finding: CP-PC-001. Owner: Planning parent. Smallest next
  action: correct the validation paths before implementation/validation.
  User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md](.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md) | P04 correction candidate assessed. |
| [.copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md](.copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md) | P04 tasks and validation recipe assessed. |
| [.copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md](.copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md) | Correction cycle 2 C7-C9 evidence. |
| [.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-critique.md](.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-critique.md) | Appended independent correction critique; historical text preserved. |

## Next Steps

The active planning parent should apply CP-PC-001 directly, then continue the
requested correction pass and its independent Review without another plan
critique. This assessor stops here. No user action is required.
