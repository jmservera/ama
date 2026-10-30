<!-- markdownlint-disable-file -->
# RPI Review: Capacity page correction

## Opening Review State

Task 523-correction, slug capacity-page-523-correction, parent task 523.
One independent original Review for the explicitly selected new correction cycle.
Compare current correction research, plan, details, critique and changes against
the complete retained source repair plus RV-002/RV-003 corrections and actual
local SQL/Chromium/full API evidence. Preserve the earlier Review unchanged.

P01 and P02-T01 complete; P02-T02 is this Review. P03 remains deliberately
unchecked: commit, complete full exact-head gate, current-base verification and
separate final publication assessment are not yet executed. Neither this Review
nor local runtime evidence establishes owner live/hosted approval.

Scope: source/acceptance correctness, draft and mutation semantics, exact browser
proof, PC-001 disposition, implementation-time refinements, validation and
follow-up reconciliation. No source/artifact edits except this one Review,
no heavy execution, no lock probing, no Azure, secrets, environment files,
private datasets or foreign output. Fresh web-guidelines review required for
the supplied web boundary.

* Evidence readiness: All six correction artifacts and historical Review are present;
  source and named task-owned runtime logs will be compared read-only.
* Acceptance basis: AC1-AC5, P01/P02 completion claims, PC-001 disposition,
  retained compatibility behavior and explicit authority/publication boundaries.
* First comparison boundary: Full correction artifacts against retained repair
  and complete changed files, then owning route/draft/authority contracts.
* Initial blockers: None to performing this bounded Review. P03 and owner live
  approval remain pending, not source-defect findings.

## Scope and Evidence

* Task ID: 523-correction; parent issue #523.
* Task slug: capacity-page-523-correction.
* Review date: 2026-10-28.
* Branch: fix/capacity-page-523.
* Review scope: One independent Review of the complete retained repair and
  correction candidate, including the completed implementation/validation and
  the still-pending publication contract. No second Review is performed.
* Candidate: ac8d403761b45b57f17a2bff84aff5e523dd6ce4 plus the working-tree
  corrections in src/api/src/zava_forward/api/web/ops.js,
  src/api/checks/capacity_browser_check.py and src/api/README.md.
* Retained source boundary also includes
  src/core/src/zava_forward/core/appointments.py and
  src/api/tests/test_procurement_api.py. All four executable files were read
  in full, not only their changed lines. The complete README change, its
  capacity/appointment/shared-workbench/design-system/test guidance and its
  file-wide section inventory were assessed.
* All correction research, plan, phase details, critique, changes and opening
  Review were read in full. Historical
  .copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-review.md was
  read in full and remains unchanged.
* Owning contracts inspected: app.js API/session/route/draft guards,
  index.html and shared style.css rules, manager destination implementations,
  procurement authority/projection, supplied_contract_fixture and inherited
  MssqlProcurementApi ownership.
* Context: original case study, addendum, reference index, owner memory,
  housing-association primer and the owner-selected Fluent 2, WCAG baseline
  and plain-language standard. No new customer or legal conclusion is made.
* Runtime evidence: Parent-supplied personally executed SQL/Chromium and full
  API results, recorded in the correction changes. The two named task-owned
  external logs identify that evidence; raw logs were not independently
  reopened and no heavy validation was repeated during this Review.

Independent SHA-256 checks matched the parent's successfully tested source:

* ops.js:
  49b91f128719bb6968e8709caa891d2c6251b5dc01d80868e503b3bb74f772c3.
* capacity_browser_check.py:
  d32c617373ba3f91ff4f3e8d7c9c5cfcf23885fc848d24e8b4964aee84c39c46.

The candidate is not yet a clean committed correction head. No fetch,
commit, receipt verification, push, PR, lock probe or Azure operation belongs
to this Review.

## Execution Status

* Review execution status: Complete.
* Full delivery-plan execution status: Partial. P01/P01-T01/P01-T02 and
  P02-T01 have completion evidence. This record supplies P02-T02's independent
  assessment; the parent owns subsequent marker updates. P03/P03-T01 remain
  deliberately unchecked.
* Review execution evidence: Artifact/source comparison, fresh web-guidelines
  retrieval, independent source identity checks, Node syntax and whitespace
  checks completed on 2026-10-28. Runtime results are attributed to the parent,
  not represented as an independent browser/SQL/API execution.
* Severity summary for new correction-cycle findings: Critical 0; High 0;
  Medium 0; Low 0.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 / AC1 | Draft-safe local recovery | Reconciled | Retry invokes local go() with no mutation; failed reads retain the existing DOM; successful reads snapshot and restore current unsaved appointment forms. Both endpoint scenarios include real save, repeated failure, live draft edits and successful recovery. |
| P01-T01 / PC-001 | Recovery-origin navigation and 401 | Reconciled | Captured-signal guard prevents refresh after departure; catch suppresses obsolete/session-ended messages. Harness enters the changed go path after a real mutation, not only initial route loading. |
| P01-T02 / AC2-AC3 | Destination and read proof | Reconciled | Explicit manager contracts, fresh full-document visits, successful browser GETs, rendered row identity assertions and unexpected API HTTP/transport tracking replace the historical permissive checks. |
| P02-T01 / AC4 | Scoped, static, real SQL/browser and full API validation | Reconciled | Supplied PASS results cover the tested source hashes. Launcher/harness failures and the wrong-cwd API attempt remain adverse evidence; later successful runs do not erase them. |
| P02-T02 / AC4 | Pre-Review reconciliation and single independent Review | Reconciled | This is the new cycle's one original Review. Earlier Review and critique verdicts remain historical and unchanged. |
| P03-T01 / AC5 | Commit, complete gate, verify, exact-head assessment and PR | Reconciled as pending | The required ordering is explicit and compatible with repository policy. No gate/receipt/publication readiness is claimed. |
| Follow-Up Items | Owner live verification and historical RV-004/005/006 | Reconciled | Separate owners/actions remain outside active correction scope and completion claims. |

P02 being unchecked while P02-T01 is checked is correct at intake: the parent
must record this P02-T02 result before closing P02. P03's unchecked markers,
phase-detail status, changes remaining work and Handoff agree.

Research's initial "In progress"/open-question cells and the plan's early
prospective runtime-unknown prose retain their starting state. Their terminal
synthesis/readiness, current Handoff and dated changes resolve the questions
and report the actual validation. These initial cells are not evidence of an
unresolved design decision or permission to claim P03 complete.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| Retained repair | src/core/src/zava_forward/core/appointments.py | Missing legacy contract_version projects as null rather than raising KeyError. | _appointment_binding uses p.get; list_packages already uses the same optional projection. | Supplied procurement/full API results and generated SQL/browser read/render result. | Compatible read repair; no version, appointment agreement or delegation is invented. |
| Retained regression | src/api/tests/test_procurement_api.py | Exercises absent version/bindings, readable Unknown state, denied write with unchanged procurement and known-empty reads. | Two retained canonical methods; JSON/SQLite and opt-in MSSQL inheritance remain. | Supplied focused module PASS; full API PASS with opt-in skips. | Regression remains relevant; inherited real SQL execution still belongs to the later full gate. |
| P01-T01 | src/api/src/zava_forward/api/web/ops.js | Local read-only recovery preserves the editable screen and lifecycle boundaries. | go's no-op default, post-mutation abort check, guarded catch and success-only draft restoration. | Both supplied SQL/Chromium draft scenarios and mutation-refresh cancel/401 PASS. | Conformant for the accepted recovery direction. |
| P01-T02 | src/api/checks/capacity_browser_check.py | Proves destination/read/render success and tracks unexpected failed transports. | Response-derived package headings and ordered work-order IDs; explicit route contracts; actual response tracking. | Supplied 1-package/601-order SQL/browser result and all 11 manager destinations PASS. | Material historical assertion weaknesses are addressed. |
| P01-T02 | src/api/README.md | Documents draft-safe retry, actual browser proof and separate fictional authorization fixture. | Complete #523 section agrees with source and distinguishes the separate capacity check/full gate/live boundary. | Source and documentation comparison. | No unsupported deployment or live-acceptance claim. |

### Draft, mutation and lifecycle reasoning

* go() retries only capacity reads. It neither retains nor invokes the
  previous mutation callback when Try again is selected.
* Clearing savedForm.dataset.unsaved occurs only after fn resolves. A
  successful save followed by failed refresh therefore leaves that form clean
  while another unsaved appointment form remains editable.
* Both reads precede show(). Repeated failures do not replace the original
  workspace. On success appointmentDrafts captures the latest values,
  checkboxes, expansion and original appointmentContext immediately before
  replacement, then restores by form key. The event-reference field is
  included among named controls.
* The successful-mutation abort check runs before starting a new capacity
  view; the catch does not focus or render into an aborted or ended session.
  app.js supplies the matching route AbortController, post-response
  throwIfAborted and 401 login behavior. The two parallel reads cannot turn
  a rejected Promise.all into a successful stale render.
* Existing in-app confirmation and beforeunload protection remain. The draft
  scenarios explicitly accept the navigation dialog after proving recovery.
  The held-refresh cancellation scenario has only the successfully saved
  configure form, so no unrelated unsaved form requires a dialog there; it
  does not bypass a pending prompt.
* Existing server committed-but-unacknowledged responses still instruct
  reconciliation, not a new action. This correction does not change those
  HTTP semantics or claim to solve uncertain mutation acknowledgements.

### Authority and fixture reasoning

* _contract_authority still requires a truthy package contract version plus
  current named delegation for contract, supplier, scope, dates and action.
  Optional null read projection cannot satisfy it.
* _proc_operation still validates the current registered manager and
  appointment delegation, including configure. Neither the UI nor the
  correction grants production authority.
* appointment_summary and _wo_view retain role-based evidence projection
  and assigned-contractor filtering. No consent, closure, resident-update or
  approval boundary is broadened.
* The generated legacy data is read and all manager destinations are checked
  before supplied_contract_fixture is applied. The later fixture deliberately
  supplies fictional version/delegation/document evidence for one named
  supplier in the owned test store; real configure POSTs then persist through
  the normal endpoint. This is the plan's expressly allowed separate
  authorized-fixture alternative, not legacy read acceptance with invented
  authority or a mocked successful write.

### Browser proof assessment

The existing capacity() helper was retained. Exactly two helpers are new:
inject and verify_route. The route-contract dictionary and inline scenarios
stay in the canonical harness; no test file, production test export, dependency
or existing test was removed.

Fresh distinct /app?check=... documents and cleared read collections bind
destination assertions to actual visits. Expected path/query successes must be
present; a wrong heading, missing read, inline alert, unchecked navigation href
or unexpected API HTTP/requestfailed event fails instead of printing PASS.
The inventory comes from the authenticated manager's navigation, which app.js
renders directly; aria-current additionally proves each corresponding rendered
navigation destination exists.

Capacity's package headings must match each browser package response entry;
all rendered work-order IDs/versions must exactly equal the browser response
list, not a separate request-context result. Recovery scenarios additionally
wait for both successful reads and detachment of the old form before asserting
restored state. POST response counts and persisted configuration increments
prove one real successful mutation per draft scenario.

Expected injections use exact Request objects. Cancellation exemptions are
restricted to named departing capacity requests with net::ERR_ABORTED;
unexpected API transport failures remain recorded with their originating
scenario. External map traffic blocked by the loopback policy is outside
local API/provider acceptance. No blanket API transport exemption was found.

| Actual manager destination | Required successful read contract | Destination/content assessment |
| --- | --- | --- |
| #/ | /api/facets; /api/cases?view=mine | Exact own-queue heading, response-matched row count and resident content or explicit empty state. |
| #/all | /api/facets; /api/cases?view=all | Exact all-open heading and corresponding rows/empty state. |
| #/overview | /api/stats; /api/map | Exact overview heading, map control and Team workload content. |
| #/visits | /api/visits?view=all | Exact visits heading and response-matched rows or No booked visits. |
| #/funding | /api/funding | Exact funding heading and response-matched bounded table count. |
| #/finance | /api/finance | Exact finance heading and rows or Nothing is waiting. Successful read requirement rejects the inline error fallback. |
| #/capacity | /api/packages; /api/workorders | Exact capacity heading and appointment region; capacity() additionally compares package headings and all order IDs/versions. |
| #/closed | /api/cases?view=closed | Exact archive heading and rows or No closed cases. |
| #/assistants | /api/assistants/proposals | Exact role-owned heading, controls and explicit empty proposal state for this fixture. |
| #/time | /api/time/status | Exact Staff time capture heading, checklist and response-matched status. |
| #/screens | No page-data GET required for uninstalled menu | Exact specialist heading, explicit no-installed-screens content and manual return link. |

The PC-001 cancellation scenario starts after a real configure POST, holds the
resulting packages refresh, leaves for #/time and releases the held request.
It verifies the exact time destination/read, focus within the new app, no stale
capacity error, no new capacity reads after departure and no POST replay.
The separate recovery-origin 401 verifies Sign in, session-ended alert, focus,
absence of Try again and stable POST count after network completion. Existing
initial-route abort/401 coverage is also retained; it is not substituted for
these changed-closure scenarios.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 / PC-001 | Add changed-closure cancellation and 401 scenarios. | Critique identified that initial-route checks alone were insufficient. Existing requirements already demanded lifecycle isolation. | Plan, details, changes and inline browser scenarios agree. | One original critique remains Complete / Revise; PC-001 is applied, not retrospectively regraded. | Direct compatible correction; no new user decision or repeat critique needed. |
| P01-T01 / test fixture | Use supplied_contract_fixture before real configure mutations. | _proc_operation requires delegation even for configure. The plan expressly allowed a separately constructed authorized fixture. | Changes explain the distinction from the unmodified legacy read fixture; README documents it. | Within accepted plan alternative and existing authority boundary. | Justified implementation choice, not a material divergence. |
| P01-T02 / P02-T01 | Refine helper typing, route setup, visible selectors, empty specialist menu and request timing. | Actual adverse runs exposed missing fresh reads, hidden controls, handler dispatch and asynchronous timing/copy assumptions. | Changes preserve failures and explain the final assertions; source uses two new helpers, fresh documents and response/form-detachment waits. | Ordinary test refinements under the same plan/critique. | Strengthens the original proof contract without expanding production scope. |
| P02-T01 | Correct launcher interpreter and full API working directory. | Early imports used an unsuitable interpreter; root-cwd discovery failed. | Both failures and subsequent correct-cwd/interpreter PASS results are retained. | No dependency replacement or changed acceptance direction. | Execution correction, not hidden successful validation. |
| P03-T01 / evidence sequence | Keep final receipt and exact-head assessment external after committing original Review. | Repository full-gate and self-invalidation policy. | Plan/details/changes agree; this Review makes no publication claim. | Still pending; not permission to skip any gate. | Correct sequencing. |

## Critique and Material Revision Assessment

* Latest critique: One correction critique, Complete / Revise, Medium PC-001.
* PC-001 disposition: Applied and supported by inspected recovery-origin
  cancellation/401 scenarios and the parent's supplied successful actual
  SQL/Chromium execution. Scope and assertions are materially different from
  the older initial-route scenarios.
* Material revisions: No significant or divergent design decision was
  discovered. Capacity-local read-only recovery, native controls, retained
  authority and canonical test ownership match confirmed intent.
* Dependent-work pause: The current plan/details incorporate PC-001 before
  claiming implementation/runtime completion. No evidence of publication
  proceeding before Review or the required post-commit gate is present.
* Justification: The fixture, navigation, typing and timing refinements respond
  to observed evidence and preserve accepted requirements. They do not
  justify regrading the original critique/Review or rerunning this Review.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Owner live verification | No deployment/live operation is authorized in this source correction. | Owner after separately authorized deployment. | Correctly pending; distinct follow-up. Use Refs #523 only. |
| Historical RV-004 | Existing eager work-order DOM strategy predates the repair. Browser completion is not a measured latency/memory assessment. | UI/performance owner measures the generated case and evaluates draft-safe bounded rendering. | Preserve as distinct nonblocking performance follow-up. |
| Historical RV-005 | Existing free-text metadata omissions are unchanged. | UI/forms owner addresses metadata in separately scoped work. | Preserve as distinct nonblocking forms follow-up. |
| Historical RV-006 | Existing withdrawal confirmation/undo behavior is unchanged. | Work-order UX owner evaluates confirmation/undo under current server authority. | Preserve as distinct nonblocking UX follow-up. |

No unresolved plan follow-up is added to active correction implementation or
claimed complete by this Review.

## Findings

No new substantive correction-cycle RV finding was identified. No severity-
graded defect, unaccepted decision or material evidence gap needs a new
rpi-implement, rpi-plan or rpi-research route.

Historical disposition assessed without rewriting history:

* Original RV-002: Its introduced same-hash router retry is replaced with local
  read-only recovery. Inspected source and supplied repeated-failure/recovery
  browser scenarios support conformance of this correction.
* Original RV-003: Actual destination/read/content contracts, response-derived
  capacity row proof and unexpected failed-transport tracking address the
  historical weak assertions.
* Original RV-001: The previously missing local SQL/browser/full API execution
  evidence is now supplied for matching source hashes. This does not imply
  that the still-unrun complete exact-head publication gate passed.
* Original RV-004/005/006: Retained distinct follow-ups above, not new
  correction defects or newly closed findings.
* The original task's Partial / Not accepted outcome remains immutable. The
  caller explicitly selected this new complete correction cycle; its Review
  does not override the earlier task's one-pass boundary.

## Web-Guidelines Assessment

web-design-guidelines was freshly loaded and its complete current source
retrieved successfully on 2026-10-28 before reviewing ops.js:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.

All fetched rule categories were considered. Native Fluent-derived controls,
plain ASCII and sentence case take precedence over generic title-case,
curly-quote/ellipsis and stylistic recommendations. This is not a visual
redesign or full Fluent/WCAG acceptance review.

### src/api/src/zava_forward/api/web/ops.js

No new correction finding. Retained historical observations in current
file:line format:

* src/api/src/zava_forward/api/web/ops.js:233 - pre-existing eager order/control
  rendering; historical RV-004, distinct performance follow-up.
* src/api/src/zava_forward/api/web/ops.js:28 - pre-existing free-text control
  lacks name/autocomplete metadata; historical RV-005.
* src/api/src/zava_forward/api/web/ops.js:29 - pre-existing free-text control
  lacks name/autocomplete metadata; historical RV-005.
* src/api/src/zava_forward/api/web/ops.js:238 - pre-existing binding control
  lacks name/autocomplete metadata; historical RV-005.
* src/api/src/zava_forward/api/web/ops.js:246 - pre-existing withdrawal lacks
  confirmation/undo interaction; historical RV-006.

The changed retry is a native type=button with visible name, inherited hover
and focus-visible styling, busy/disabled feedback and the existing polite
status/focus mechanism. Non-colour error wording identifies the failed read
and offers recovery/support. Native appointment labels, details, form
validation and draft navigation guards are preserved. Empty data remains
different from failed reads; no layout-measurement, animation, gesture,
media/image, hydration, theme or locale mechanism is introduced.

Shared CSS/shell inspection supports the existing focus, overflow,
reduced-motion and skip-link mechanisms, not cross-device or assistive-
technology acceptance. Full keyboard/zoom/reflow, screen-reader announcements,
performance measurement and real-user acceptance were not run in this Review.
No new CSS, shell or unrelated-page remediation is inferred.

## Defects

None identified within the completed correction implementation and retained
repair boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| New correction findings: none | None | No later defect, decision or research stage required by this Review. | Completed source/evidence boundary is conformant. |
| Historical RV-004 | Distinct UI/performance follow-up | Performance owner measures rendering before selecting a bounded approach. | Pre-existing nonblocking concern. |
| Historical RV-005 | Distinct UI/forms follow-up | Forms owner reviews existing metadata. | Pre-existing nonblocking concern. |
| Historical RV-006 | Distinct work-order UX follow-up | UX owner evaluates confirmation/undo. | Pre-existing nonblocking concern. |
| Live verification | Distinct owner follow-up | Owner verifies after separately authorized deployment. | Local evidence cannot establish live acceptance. |

Later implementation of a routed historical follow-up does not require this
Review to run again.

## Residual Work

* P03/P03-T01 is planned active publication work, not a source-defect finding:
  commit source and original dated correction evidence, run the complete
  exact-head gate, verify a current-base receipt and obtain the separate final
  exact-head publication assessment before push/PR.
* Hosted checks, owner approval/merge and live verification remain separate.
* Historical UI/performance/forms/withdrawal follow-ups remain outside this
  correction. Local browser PASS does not close them.

## Blockers and Remaining Work

* Review blockers: None.
* New source/design/runtime defect blockers identified: None.
* P02-T02: Parent records this one original Review result and reconciles its
  phase markers without modifying historical outcomes.
* P03 eligibility: Not yet established. The correction remains uncommitted;
  no full receipt, current-base verification or final publication assessment
  has been supplied. These are explicit remaining prerequisites.
* The later gate must use the committed exact candidate and fetched reviewed
  main base, a new external evidence directory and all required local
  prerequisites. No cloud fallback, skip token or weakened protection.
* Fetch main and verify the receipt against current origin/main immediately
  before separate exact-head assessment and push. A later source/evidence
  commit, dirty/untracked/ignored input, base/tool/image change or rebase
  invalidates the relevant gate evidence. Keep the final receipt and
  publication assessment external.
* Preserve required hosted checks and the owner's merge decision. Refs #523
  only; no issue closure, deployment or live-causality claim.

## Validation Evidence

| Command or check | Scope | Status | Summary |
| --- | --- | --- | --- |
| Parent focused procurement API module | Existing canonical JSON/SQLite procurement suite | Passed, supplied | 32 tests, 26.737s. Includes retained absent-version/known-empty regression ownership. |
| Parent strict Ruff E/F/I/B/UP and format, line length 100 | Scoped Python changes | Passed, supplied | Final strict lint/format PASS; no new dependency. |
| Parent API mypy | API sources | Passed, supplied | 91 source files. Initial callback typing failure and correction remain recorded. |
| node --check src/api/src/zava_forward/api/web/ops.js | Current complete changed JS file | Passed, independently executed | Syntax only, not behavioral/browser acceptance. |
| git diff --check | Current tracked correction diff | Passed, independently executed | No whitespace errors. |
| sha256sum on ops.js and capacity_browser_check.py | Current source/runtime identity | Passed, independently executed | Both hashes exactly match the supplied successful SQL/browser candidate. |
| capacity_browser_check.py --mssql with installed API-dev interpreter and shared fixture paths | Generated fictional data, owned real SQL Server and Chromium | Passed, parent personally executed | Named log: /tmp/ama-capacity523-correction-validation-20261028-13/sql-browser-1793212006552977822.log. 1 package/601 rendered orders; 11 manager routes; both draft scenarios; mutation-refresh cancel/401; initial injected reads, transport/403/abort/401 and empty states. |
| python -m unittest discover -s tests -q, from src/api with shared fixture paths | Full API discovery | Passed, parent personally executed | Named log: /tmp/ama-capacity523-correction-validation-20261028-14/api-full-1793212676882593075.log. 1154 tests, 413.531s, 316 opt-in skips, exit 0. Not a substitute for the complete gate's required real SQL selectors. |
| Earlier launcher/browser/API attempts | Same correction implementation process | Failed, supplied and preserved | Missing interpreter Playwright, hidden selector, missing fresh read, legitimate specialist empty state, route-handler/timing/copy assumptions and wrong-cwd API discovery are explicitly retained in changes. No failed receipt/log was replaced or treated as PASS. |
| Owned SQL cleanup and generated-input preparation | Parent-owned runtime/publication preparation | Passed, supplied | Changes record named-container cleanup and archive/restore/hash-verified finite generated-input relocation. Independent ignored-input listing was empty; this alone is not full-gate acceptance. |
| Complete tools/rpi-checks.py --all | Committed exact candidate/base, all required integration/build/scanner contracts | Not run, planned P03 | Must follow the original Review/source/evidence commit. No receipt or skip waiver is supplied by this Review. |
| Current-base receipt verification and final exact-head publication assessment | Immediate pre-push eligibility | Not performed, planned P03 | Separate assessment after full receipt verification, not a repeat RPI Review. |
| Hosted checks, deployment and owner live verification | Hosted/live acceptance | Pending separate owners/gates | No hosted, Azure, user, screen-reader or live success is inferred. |

Supplied heavy results are execution evidence from the parent, corroborated
here by source identity and assertion inspection. This Review did not
independently reopen the raw external logs, run SQL/browser/API discovery,
inspect foreign output, read private data or probe a heavy lock.

## Outcome

* Outcome: Conformant for the completed correction source/runtime-evidence
  boundary; no material open correction defect found.
* Review execution: Complete. Full delivery-plan execution: Partial, pending
  P03, hosted controls and owner/live prerequisites as distinguished above.
* Rationale: Read-only retry now preserves current unsaved appointment drafts
  across repeated failure and restores them on success without replay.
  Browser assertions prove real response-backed rendering and manager
  destinations/reads, track unexpected failed transports and exercise the
  changed recovery closure's cancellation/401 lifecycle. The retained legacy
  compatibility repair remains fail-closed. Supplied actual local runtime
  evidence matches the inspected source.
* This is not publication-ready approval, AC5 completion, a full exact-head
  receipt, an alteration of the earlier Review or live verification.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No new correction defect identified. |
| Decision gap or invalid assumption | None | No unaccepted material divergence or rpi-plan handoff. |
| Material evidence gap | None for completed P01/P02-T01 | Parent's reported local runtime evidence is accepted at its stated boundary; P03 gate remains mandatory active work. |
| Nonblocking residual work | Distinct historical UI/performance/forms/UX and owner live follow-ups | Preserve original RV-004/005/006 and owner live verification without scope expansion. |
| Planned publication prerequisites | Active parent, P03-T01 | Commit, complete full local gate, current-base receipt verification, separate exact-head assessment, then eligible push/PR and hosted/owner gates. |

Only this canonical correction Review record was changed by the reviewer.
No source, other evidence, original prior Review or state artifact was edited.
No in-task correction, repeat Review or nested delegation was performed.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/capacity-page-523-correction-research.md](.copilot-tracking/research/2026-10-28/capacity-page-523-correction-research.md) | Complete correction research |
| [.copilot-tracking/plans/2026-10-28/capacity-page-523-correction-plan.md](.copilot-tracking/plans/2026-10-28/capacity-page-523-correction-plan.md) | Requirements, markers and publication sequence |
| [.copilot-tracking/details/2026-10-28/capacity-page-523-correction-phase-details.md](.copilot-tracking/details/2026-10-28/capacity-page-523-correction-phase-details.md) | Detailed behavior and lifecycle proof contract |
| [.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-correction-plan-critique.md) | Preserved Complete / Revise critique and PC-001 |
| [.copilot-tracking/changes/2026-10-28/capacity-page-523-correction-changes.md](.copilot-tracking/changes/2026-10-28/capacity-page-523-correction-changes.md) | Implementation, adverse attempts and supplied runtime evidence |
| [.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-review.md](.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-review.md) | Immutable historical Review and RV inputs |
| [src/core/src/zava_forward/core/appointments.py](src/core/src/zava_forward/core/appointments.py) | Retained optional-binding repair and appointment semantics |
| [src/api/tests/test_procurement_api.py](src/api/tests/test_procurement_api.py) | Complete canonical retained HTTP regression file |
| [src/api/src/zava_forward/api/web/ops.js](src/api/src/zava_forward/api/web/ops.js) | Complete retained/corrected web source |
| [src/api/checks/capacity_browser_check.py](src/api/checks/capacity_browser_check.py) | Complete browser assertion and owned-store source |
| [src/api/README.md](src/api/README.md) | Owning API/browser behavior and command guidance |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Shared route, API, session and draft boundaries |
| [src/core/src/zava_forward/core/procurement.py](src/core/src/zava_forward/core/procurement.py) | Owning authority and work-order/package projection |
| [src/core/tests/dataset.py](src/core/tests/dataset.py) | Explicit fictional delegation fixture |
| [src/api/tests/test_mssqlstore.py](src/api/tests/test_mssqlstore.py) | Retained opt-in SQL regression inheritance |
| [src/README.md](src/README.md) | Required complete local publication gate |
| [.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-correction-review.md](.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-correction-review.md) | This one independent correction Review |

## Next Steps

Return Complete / Conformant for the reviewed completed correction boundary to
the active parent, with full-plan execution still Partial. No new defect,
decision or research-stage handoff is needed. The parent records P02-T02 and
continues the already planned P03 sequence: source/original-evidence commit,
complete exact-head local gate, current-base receipt verification, separate
final exact-head publication assessment and only then eligible push/PR.
Keep hosted/owner/live gates and historical follow-ups distinct. No user action
is required to complete this Review. Stop here; no in-task correction or repeat
Review.
