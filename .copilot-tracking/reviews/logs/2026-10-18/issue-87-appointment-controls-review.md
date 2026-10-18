<!-- markdownlint-disable-file -->
# Review: Issue 87 appointment commitment controls

## Scope and Evidence

* Task ID: 87; review date: 2026-10-18.
* Scope: full task, one original independent Review.
* Source candidate: 22c98267 against base
  99056cae7bc679d2ace3e42c75f28577cfce8887.
* Plan: .copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md.
* Details: .copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-18/issue-87-appointment-controls-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-18/issue-87-appointment-controls-changes.md.
* Research: .copilot-tracking/research/2026-10-18/issue-87-appointment-controls-research.md.

## Opening Review State

* Goal: independently assess complete issue87 correctness against exact sources,
  all four AC and cross-cutting authorization, persistence, UI and human limits.
* Evidence readiness: full P01-P03 implementation reconciled; final core323/API85,
  actual SQL61, browser and hardened installed-source-image receipts available.
* Acceptance basis: explicit user criteria, sourced plan F1-F8 and AC1-8, one
  frozen critique with PC-001/002 parent dispositions; no implied live approval.
* First comparison: plan/details/changes and exact full source diff against base,
  including new appointments module, retained capacity and consent controls.
* Read-only boundary: independent reviewer may write only this one record;
  no source/test/plan/critique/state mutation, fix or second Review.
* Initial blockers: none asserted; verdict remains unassessed.

## Execution Status

* Execution status: Complete.
* Outcome: Not accepted.
* Source: 22c98267ae6da365d6a2d9fceed7113c8f4578ea.
* Pinned base: 99056cae7bc679d2ace3e42c75f28577cfce8887.
* Severity: 0 Critical, 2 High, 5 Medium, 0 Low.
* This is the task's one original independent Review and its complete finding
  set. It is not a security-specific audit or a plan critique. No nested
  reviewer, fix, second Review, commit, push or remote mutation occurred.
* Evidence comparison covered the complete candidate/base patch, including
  lifecycle artifacts, documentation, every changed application source file,
  shared fixture, changed test and browser check. Current parent lifecycle
  edits were read as the finalized handoff, not treated as source changes.
* Only this canonical review record was edited. Bounded executions used the
  existing task .venv and public synthetic fixtures; ephemeral fixture directories
  were rooted beneath that existing worktree-local environment and cleaned.
  No SQL Server, browser or image resource was started by this reviewer.

## Scope and Acceptance Evidence

The acceptance basis is the caller's exact issue AC1-AC4 and cross-cutting
conditions, not only the implementation's positive assertions. Read:

* Full current plan and matching phase details, P01-P03, F1-F8 and plan AC1-AC8.
* Changes record, including the FINAL continuation receipt. Its final
  core323/API85/SQL61/browser/image evidence supersedes historical blocked and
  pre-continuation receipts. References to initial source 99056cae are historical,
  not fresh tests on that unchanged base.
* Corresponding research and its complete current-code source inventory.
  Research's planning-time statements that validation remained future work are
  chronological context, not an unresolved final implementation blocker.
* Frozen Complete/Revise plan critique and parent PC-001/PC-002 dispositions.
* PRD DD-006, FR-031, FR-048, AC-033, AC-062 and AC-065 in
  docs/prds/zava-forward-retrofit-programme-demonstrator.md.
* BRD FR-046/AC-088, RULE-006/AC-025 and RULE-007 in
  docs/brds/agentic-retrofit-programme-brd.md.
* Original case specification, addendum context and EXA-014/missed-appointment
  wording, reference index, memory as context only, housing-association primer,
  and regulatory-register evidence boundaries. No new legal-currentness or
  operational-approval assertion is made.
* Existing procurement, resident authority/consent/update/remedy, controlled
  event, case advance/reopen, role projection and SQL writer/recovery seams.
* Fluent 2 foundations, WCAG baseline and plain-language standard in
  docs/reference/research/ux/design-system.md,
  docs/reference/research/ux/wcag-conformance-baseline.md and
  docs/reference/research/ux/content-standard.md.
* Fresh COMPLETE Web Interface Guidelines fetched by this reviewer on
  2026-10-18 from
  https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
  Retrieval succeeded, including every rule family and the source's reporting
  format. The changed-web boundary is ops.js only.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01, F1-F4 | New appointments.py; procurement guarded readers/writers; explicit supplied fixture | Reconciled as implemented | Tri-party record model, bounded appointment-only authority, current capacity and independent works consent are present. RV-004 and RV-005 prevent full acceptance. |
| P01-T02, F5-F7 | Outcome/configuration/investigation history and cause/owner facts | Reconciled as implemented | Default sixth-event rule, exclusions and dedup are supported; configuration lowering is incomplete, RV-003. |
| P01-T02, F8 | FINAL human closure continuation | Reconciled, supersedes historical blocker | Explicit supplied-human closure of the existing same case, optimistic case version, atomic boundary and preserved histories/updates are implemented. No task/order/remedy closure is substituted. |
| P02-T01 | Existing HTTP route, projections and ops.js native forms | Reconciled as implemented, not fully correct | RV-001, RV-002 and RV-005 through RV-007 identify response, privacy and UI gaps. |
| P03-T01 | FINAL commands, counts, owned-resource and cleanup receipts | Reconciled as executed engineering | Reported checks are substantial and candidate-source-specific. Independent 95 core and 12 API checks pass, but narrow counterexamples show they are not complete semantic acceptance. |
| P03-T02 | Component guides, resident synthesis, index and append-only log | Reconciled | Changed guides distinguish exercise code from live policy. Earlier log entries are retained with a later correcting entry. No memory/original-case change or fabricated live approval. |
| Follow-Up Items | No remaining bounded implementation item; live prerequisites outside exercise | Reconciled | Existing human/live and accessibility limitations remain distinct follow-up work, not new active implementation scope. |

## Completed Work Assessment

| Related marker | Files or seam | What changed and why | Completion evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/appointments.py; procurement.py | Server-derived offer/commitment, separate confirmations, representative authority and existing capacity dependency snapshots | Source inspection; independent JSON/SQLite tests | Broad implementation complete; missing bundle-source validation and withdrawn-state handling are defects, not missing phase execution. |
| P01-T02 | appointments.py; procurement.py; sqlstore.py | Cause-aware unique visits, active-case counts, owned human investigation and supplied-human closure with durable outcomes | Source; independently passing closure, exclusion, event/retry and SQLite race tests; reported actual MSSQL receipt | Closure direction is supported. RV-001 and RV-003 remain acceptance defects. |
| P02-T01 | src/api/src/zava_forward/api/server.py; web/ops.js | Authorized action route, role projections and manual native controls | Independent API tests, response fault reproduction and in-memory UI rendering | Implemented but response serialization, unrelated-staff disclosure and UI state/detail protection are incomplete. |
| P03-T01 | Existing core/API tests and procurement_browser_check.py | Extend existing suites, retain legacy positive setup with supplied explicit agreement | 95 core and 12 API independently passed; final broader receipts assessed separately | No deleted assertion found. Browser keyboard confirmation starts from a focused submit button and verifies status headings, not the missing actual visit date/period or dirty-form preservation. |
| P03-T02 | Component READMEs; docs/reference research/index/log | Explain record-only limits and missing operational approvals | Complete documentation patch inspected | Useful, honest exercise boundary. Documentation completion does not override reproduced source defects. |

The changed positive Booked fixtures provide explicit synthetic source/channel/
person evidence through supplied_appointment_fixture. They do not merely assert
Committed or delete existing quota, scope, authority, consent, hazard, quality,
finance, event or building checks. Existing tests remain outside packages.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and decision | Reconciliation | Assessment |
| --- | --- | --- | --- | --- |
| F5/F6, AC4, P01-T02 | Bind accumulation/reset to the underlying active home case, not a threshold-created task | PC-001; exact PRD/BRD/addendum case wording | Plan, details, research interpretation and changes record agree | Supported correction preserving confirmed intent; counting before task creation and task-disposition-no-reset are tested. |
| F7, AC8, P01-T02/P02/P03 | Add independent preference-breach and abortive facts, overlap, cause/owner totals and Unknown reporting threshold | PC-002; PRD AC-065 and BRD AC-088 | Current plan/details and source/test/projection evidence agree | Disposition substantively implemented; no invented reporting threshold. |
| F8, P01-T02 and P03 | Fill the missing authorized record-only human case-closure writer | Parent clarification after first implementation identified no existing closure writer, despite explicit exercise permission in DD-006/AC-033, RULE-006/AC-025 and EXA-014 | Full current plan/details and FINAL continuation receipt supersede historical blocked sections | Justified engineering clarification, not new operational policy. Current actor/contract authority, source/version/reason, explicit confirmation and optimistic case hash are required; server records actor/time. |
| P03 completion | Replace historical incomplete validation with final changed-source receipts | Authorized F8 continuation and rerun affected gates | All P01-P03 markers checked; final commands/results/cleanup recorded | Execution reconciliation accepted. Correctness remains withheld by this Review's findings. |

## Critique and Material Revision Assessment

* Exactly one frozen critique: Complete, verdict Revise, PC-001 High and PC-002
  Medium. Both have explicit parent dispositions and traceable changes in the
  current artifacts. Neither requires another critique or Review.
* PC-001 is not left blocked merely because the first implementation lacked a
  closure writer. F8 now records the source-authorized supplied human decision
  against the existing case identity and closed field. That is consistent with
  the caller's engineering clarification, not permission to infer readiness,
  technical acceptance, legal/financial settlement or live policy approval.
* Source and tests preserve the independent resident-update/remedy records and
  all outcome/configuration/consumed-reference history across closure/reopening.
  Both SQL closure/event winner orders appear in the final actual-MSSQL receipt
  and in the SQLite tests independently executed here.
* No unsupported significant divergent decision or resumed work contrary to a
  remaining planning blocker was found. The defects below fit the accepted
  direction; no new planning or research decision is needed to route them.

## Exact Acceptance Matrix

Issue AC numbers and expanded plan AC numbers are distinguished below.

| Exact issue criterion | Status | Evidence and remaining defect |
| --- | --- | --- |
| AC1: separate resident/explicit bounded appointment representative, authorized staff and current committed contractor capacity; offer never commitment early | Not fully met | Separate confirmations, explicit offer-bound representative validity/revocation and direct Booked/completion/advance gates are implemented. Unknown legacy Booked cannot satisfy them. However, withdrawing an order still projects its appointment as current Committed, RV-005, and staff/providers cannot read the actual new offer's selected date/period in the UI, RV-006. |
| AC2: bundle agreement and exact-scope competence; urgent safety independent | Not fully met | Exact binding and resident bundle agreement are checked; no new coupling to hazard intake/response exists. A blank whitespace competence source can nevertheless produce an Appointed/Committed bundle, RV-004. |
| AC3: household constraints/options/deferral/pause and named update owner; manual route and minimum necessary instructions | Partially met | Saved household fields and current update owner persist/project; separate provider projection excludes household reasons, authority evidence and investigations. Existing updates/remedies are not silently cleared. New work-order projections bypass unrelated-staff redaction, RV-002, and new manual drafts lack loss protection, RV-007. These cross-cutting gaps prevent accepting the complete workflow. |
| AC4: strict > configurable provisional default5; eligible confirmed verified resident no-access in same active home case; dedup; owned human investigation only; explicit human case closure reset with preserved history | Not fully met | Counts4/5/6 at default5, exclusions, event retry/conflicting reuse, independent task disposition, explicit closure/reset, reopening/replay and preserved history are supported. Lowering the current threshold below the already eligible active count never creates the required task until another eligible visit occurs, RV-003. |

| Expanded plan criterion | Status |
| --- | --- |
| Plan AC1 | Not fully met: RV-005; related readable appointment details RV-006. |
| Plan AC2 | Not fully met: RV-004. Urgent human hazard independence is retained. |
| Plan AC3 | Saved-state persistence and provider minimization supported; complete privacy/manual workflow not accepted, RV-002/RV-007. |
| Plan AC4 | Default and explicit-human-closure boundaries supported; configurable-threshold behavior incomplete, RV-003. |
| Plan AC5 | Denials/concurrency/audit/idempotent persistence substantially covered, but truthful response serialization and role projection incomplete, RV-001/RV-002. |
| Plan AC6 | Actual browser execution evidenced by FINAL receipt, not rerun here. Visible state/detail and draft-loss defects RV-006/RV-007 remain; engineering execution is not accessibility acceptance. |
| Plan AC7 | FINAL actual MSSQL61/61 and hardened installed-wheel image receipts are adequate evidence of executed gates on the supplied source tree. Not independently rerun or recertified here. |
| Plan AC8 | Supported by source and independently passing tests: separate cause/owner totals, preference-only/provider/overlap/retry/reload, provider minimization and Unknown reporting threshold. |

Cross-cutting findings apply even where the basic positive AC path passes. No
claim of full exact acceptance follows from phase checkboxes or passing tests.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Post-commit response serialization is outside the committed-outcome guard

* Related scope: P01-T02/P02-T01/P03-T01; plan AC5 and the explicit truthful
  POSTCOMMIT response condition.
* Evidence: src/api/src/zava_forward/api/server.py:851-857 guards
  _procurement but calls _json(200, result) after that guard.
  _json serializes at server.py:195-196. A serialization ValueError reaches the
  outer HTTP400 handler at server.py:975-976; other exceptions can escape without
  a structured committed response. The new projection guard at :745-750 does
  not cover this serialization boundary.
* Independent reproduction: existing ProcurementApi fixture, accepted synthetic
  capacity/order/offer, then POST a resident confirmation with
  event_ref=REVIEW-SERIAL. Inject a ValueError only when json.dumps receives the
  refreshed response containing work_orders[0].appointment_control, not when it
  serializes internal procurement. Actual HTTP result was 400 with only
  error="SYN response-only serialization failure"; the confirmation event was
  durably present. Identical retry returned 200.
* Impact: A successfully committed human action is reported as a request failure
  without outcome=committed or reconciliation guidance. A user/caller may change
  evidence or issue a new action instead of reconciling the consumed reference.
  The existing passing response test injects list_packages failure earlier and
  therefore misses this required boundary.
* Destination: later rpi-implement, once.
* Smallest useful next action: extend truthful committed-response handling
  through response serialization before headers, retaining idempotent references;
  add a response-only encoder-failure assertion for confirmation and human closure.
  Do not promise recovery of a connection after bytes have already been sent.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: New work-order projection bypasses existing resident-evidence role redaction

* Related scope: P02-T01; retained #88/PR-002 privacy and role-projection boundary.
* Evidence: src/core/src/zava_forward/core/procurement.py:482 passes only a
  contractor boolean into appointment_summary; list_work_orders at :488-509
  permits every registered staff role. appointments.py:487-508 returns the whole
  offer, current binding, closure_history and investigation to every non-provider.
  No resident-view/recorded-need filter is applied. In contrast,
  projection.py:139-179 hides resident workflow evidence and redacts source/reason
  text for unrelated roles on ordinary case reads.
* Independent reproduction on both JSON and SQLite: record a supplied-human
  closure with reason="SYN PRIVATE CLOSURE REASON", then read as Quality Inspector
  QUIL. Ordinary detail("ZF-1", QUIL).home_case_closures[0].reason was
  "Held for roles with a recorded need"; list_work_orders(QUIL)[0].
  appointment_control.closure_history[0].reason was the raw private marker.
  A separate offer with private household support text likewise appeared in
  that role's work-order response while its ordinary case hid resident_update.
* Impact: The same protected human reason becomes available through a second
  authenticated read surface. Representative sources and investigation
  contact/circumstances checks are also returned wholesale. The manager-only UI
  does not enforce API/domain read authority. The provider-only positive test
  does not protect unrelated staff roles.
* Destination: later rpi-implement, once.
* Smallest useful next action: make appointment projection role-aware and reuse
  the existing resident-view/recorded-need boundaries; retain minimum scheduling
  instructions and non-sensitive state without exposing source/reason histories.
  Add domain and HTTP canary assertions for unrelated staff as well as providers.
  Do not broaden live role entitlement as a fix.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Lowering the configured threshold leaves an already eligible active case without investigation

* Related scope: F6, P01-T02, issue AC4, plan AC4; PRD FR-031/AC-033 and BRD
  RULE-006.
* Evidence: appointments.py:216-230 only appends configuration. Task creation
  occurs solely inside _appointment_outcome at :437-458, conditional on that new
  outcome itself being eligible. No configuration action or read evaluates an
  already accumulated active count against the new threshold.
* Independent reproduction on both JSON and SQLite: record five distinct
  confirmed verified eligible visits on the same active case at default5, then
  configure threshold4. Result: eligible_no_access=5, stored threshold=4,
  investigation=None. Reload does not supply an evaluation path. Existing
  configuration coverage checks dedup/exclusions, not creation on lowering.
* Impact: The configured strict-greater-than rule is true but its named human
  investigation is withheld until an additional resident no-access event.
  Applying a new configuration must not require another failed appointment or
  recount consumed historical events.
* Destination: later rpi-implement, once.
* Smallest useful next action: atomically evaluate affected evidenced-active
  cases when configuration changes, creating at most one owned task with the
  already eligible event references and current rule version. Preserve history,
  human closure boundaries and task idempotency; test lowering, raising, retries,
  inactive cases and concurrent configuration/outcome/closure changes.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Whitespace is accepted as bundle competence evidence

* Related scope: F4, P01-T01, issue AC2, plan AC2; PRD AC-062/BRD AC-088.
* Evidence: appointments.py:279-288 checks competence.source for truthiness,
  unlike the nonblank string validation used by other supplied evidence fields.
  It neither strips nor type-checks the competence source.
* Independent reproduction on both JSON and SQLite: offer a bundle with
  bundle_agreed=True, exact current scope binding and competence.source="   ";
  record all three otherwise valid confirmations. The result is state Appointed
  and status Committed with missing=[] despite no usable competence reference.
* Impact: A required bundle competence check can be absent while the bundle
  passes the commitment gate. This is not a request to infer competence from
  capacity or invent a competence policy.
* Destination: later rpi-implement, once.
* Smallest useful next action: validate a bounded nonblank textual competence
  evidence reference, retain the exact-scope equality and explicit resident
  agreement, and cover whitespace/non-string/empty/wrong-scope denial through
  domain and direct HTTP.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: Withdrawing an order leaves its appointment projected as current Committed

* Related scope: F2/F3, P01-T01/P02-T01; issue AC1 and plan AC1.
* Evidence: appointments.py:129-183 derives current status without checking
  the order's Withdrawn state. procurement.py:456-466 withdraws the order and
  releases its allocation without ending the offer. Consequently both staff
  and provider appointment summaries still advertise Committed.
* Independent reproduction on both JSON and SQLite: make a correctly confirmed
  appointment, withdraw its work order through withdraw_work_order, then read
  appointment_status. Actual result: order state Withdrawn, appointment
  {status: Committed, missing: []}. Confirmed separately for an ordinary
  non-bundled appointment in each backend, as well as in the RV-004 experiment.
* Impact: Historical confirmation evidence is presented as a current appointment
  commitment after the order/allocation is withdrawn. Existing consequential
  state guards still reject execution; this finding concerns the new current
  server projection, not a demonstrated completion bypass.
* Destination: later rpi-implement, once.
* Smallest useful next action: derive an explicit non-current/ended appointment
  state for withdrawn orders while preserving all historical confirmations and
  events; assert staff/provider HTTP projections and retained execution refusal.

<!-- rpi:review id=RV-006 -->
### RV-006 [Medium]: Staff and contractors cannot read the actual selected appointment date and period

* Related scope: P02-T01, issue AC1/AC3 and readable manual confirmation.
* Evidence: ops.js:117 renders status/missing/instructions but drops the provider
  projection's date/period. The staff appointment summary at :321-330 displays
  options/constraints/pause/owner, not offer.date or offer.period. New proposal
  inputs at :246 are blank. The new third-confirmation path in
  appointments.py:378-382 moves to Appointed without populating the legacy
  appointments list, so the old Visits display is not a substitute.
* Independent reproduction: execute the unchanged ops.js functions in a Node VM
  with a minimal in-memory native-element builder and a synthetic committed
  new offer dated 2099-02-02, period "Evening 17:00-19:00", appointments=[].
  Neither workOrdersCard([w], true) nor appointmentControls(w, ...) included
  the agreed date or period anywhere in its resulting tree. This was a function
  rendering reproduction, not a browser/assistive-technology test.
* Impact: A contractor sees Committed but not when the visit is agreed, and staff
  are asked to record separate confirmations without being shown the current
  selected slot. Offered alternatives are not the selected commitment. The
  browser check verifies status headings and later manually adds legacy Booked,
  masking this omission.
* Destination: later rpi-implement, once.
* Smallest useful next action: render the current offer's selected date/period
  and necessary instructions alongside its status for each authorized audience,
  including before confirmation. Use the shared localized date helper and
  distinct Unknown/ended wording; test the new flow without adding legacy Booked.

<!-- rpi:review id=RV-007 -->
### RV-007 [Medium]: New manual evidence forms silently lose drafts on navigation or another action's refresh

* Related scope: P02-T01; household/manual evidence workflow and fresh Web
  Interface Guidelines Forms/Navigation rules.
* Evidence: ops.js:237-244 creates forms with only onsubmit; inputs at :220-223
  clear errors but never mark form.dataset.unsaved. The existing workbench
  beforeunload guard at app.js:651-653 only recognizes
  form[data-unsaved="true"]. The new case/safe-contact link at ops.js:325 changes
  route, and the inherited go callback at :131 reconstructs the whole
  capacityView after any successful action, dropping all other draft forms.
* Reproduction basis: direct source tracing of form construction, existing
  dirty-selector guard, show/route replacement and success refresh; no new
  browser-run claim. Enter investigation checks or household constraints, then
  follow the safe-contact case link or save another order's action. There is no
  draft retention or discard-confirmation path for these new forms.
* Impact: Manually collected resident preferences, investigation evidence or
  supplied closure details can disappear without warning, increasing repeated
  questioning and encouraging incomplete records. Saved server history remains
  intact; this finding is specifically unsubmitted manual evidence loss.
* Destination: later rpi-implement, once.
* Smallest useful next action: integrate the new forms with dirty-state
  protection, including in-app navigation and unrelated refresh, and clear only
  successfully saved drafts. Verify cancellation preserves input and successful
  actions do not silently discard another pending form.

## Changed Web Review

### src/api/src/zava_forward/api/web/ops.js

src/api/src/zava_forward/api/web/ops.js:117 - drops the current agreed date/period from the contractor card; RV-006.

src/api/src/zava_forward/api/web/ops.js:237 - manual forms do not participate in dirty-state/navigation protection; unrelated refresh also discards drafts; RV-007.

src/api/src/zava_forward/api/web/ops.js:326 - staff summary omits the selected current offer date/period before separate confirmation; RV-006.

Every changed web file, ops.js only, was read in full against the freshly
retrieved complete rules. Native buttons, links, forms, details/summary,
labels, checkbox hit targets, names/autocomplete, required-field errors,
aria-invalid/live text, cancellable explicit closure confirmation and existing
focus/motion foundations were assessed. No new media, image sizing/loading,
font/CDN, animation, hydration, dragging, modal safe-area or theme implementation
was introduced; those rule families do not justify unrelated changes. Existing
shared styles supply visible focus, motion reduction and layout behavior.
No generic typography/colour/framework rewrite is requested; project ASCII/plain
language and Fluent 2 foundations take precedence over conflicting generic
typography/copy preferences.

Source review is not rendered conformance. The FINAL actual Chromium receipt
supports the stated keyboard/manual/Unknown/Offer/Committed/provider denial/
closure-cancel-accept/reflow checks, but it does not test all rules, speech
announcement, all input modalities, full zoom/AT behavior or direct human
comprehension. It does not cover RV-006/RV-007. No WCAG certification is claimed.

## Defects and Routing

All seven findings are implementation defects within the accepted direction.
Each is routed once below; acceptance wording and affected documentation should
be reconciled in that later implementation receipt, not by editing this verdict.

| Finding | Destination | Smallest owner action |
| --- | --- | --- |
| RV-001 | rpi-implement | Extend truthful post-commit response handling through serialization and reproduce the boundary. |
| RV-002 | rpi-implement | Apply existing role-sensitive resident-evidence projection to the new read surface. |
| RV-003 | rpi-implement | Evaluate existing eligible active counts on configuration change without recount/duplicate tasks. |
| RV-004 | rpi-implement | Reject missing/blank/non-text competence references for bundles. |
| RV-005 | rpi-implement | Stop projecting withdrawn orders as current appointment commitments; retain history. |
| RV-006 | rpi-implement | Display the actual current date/period/instructions in authorized manual/provider views. |
| RV-007 | rpi-implement | Protect and preserve unsubmitted manual evidence across navigation/unrelated refresh. |

No rpi-plan decision gap or rpi-research evidence gap is required to explain
these counterexamples. Later implementation does not require another Review.

## Plan Follow-Up Assessment and Residual Work

| Distinct follow-up | Why outside immediate scope | Owner or next action | Assessment |
| --- | --- | --- | --- |
| Existing OD-40/OQ-014 live threshold, lifecycle/configuration governance and closure authority | Exercise code records supplied human decisions; no live company policy/evidence was supplied | Housing/Repairs and Resident Engagement ratify before live adoption | Remains open human prerequisite, not a source defect or new plan task. |
| Existing real appointment/representative/competence/capacity evidence | Synthetic fixtures cannot establish actual household/supplier entitlement | Named human operational/contract owners supply and review evidence before real use | No approval, contact, booking, instruction, allocation or spend inferred. |
| Existing UX #150/#151/#153 acceptance | Native foundations and browser engineering are not completed Fluent adoption, AT testing or resident-copy approval | Existing design/accessibility/content owners retain human validation and acceptance actions | Distinct existing follow-up; no unrelated UI audit or framework change added here. |

No additional residual engineering item is substituted for an RV defect.
The plan correctly leaves live ratification outside bounded P01-P03 completion.

## Retained Boundaries

* Existing #90/#384 package quota, one-home/work-order/package-period unit,
  committed-versus-offered capacity, source document/hash/version/review,
  coverage, delivery period, accepting authority and delegation checks remain.
  No crew/weekly-slot allocator or inferred competence was introduced.
* Works consent, measure-scoped decisions and representative attendance/works
  authority remain independent of appointment agreement. Capacity-only changes
  preserve resident agreement records while invalidating the dependent capacity
  confirmation; scope/bounded representative changes fail current agreement.
* Legacy Booked remains historical/unverified. Direct Booked/completion/advance
  readers now demand current appointment evidence as well as existing gates.
  RV-005 identifies a reader projection flaw, not an assertion that these
  consequential writer guards were bypassed.
* Outcome eligibility is explicit and cause-aware. Provider/cancel/reschedule/
  Unknown/unconfirmed/unverified/inactive events do not independently add eligible
  resident no-access. Preference/abortive facts are separate, may overlap and
  deduplicate across retry/reload; reporting threshold remains Unknown.
* Explicit supplied-human closure changes the existing same case closed state
  and active-count boundary atomically. Task disposition, ordinary completion,
  pause and remedy/update closure do not invoke it. Preserved event references
  and reopening prevent old-event recount; closure does not clear #88 updates.
* Current SQL writer revalidates procurement snapshots, registered actors/
  delegations, case dependencies and retained consent/safety/source dependencies;
  pending-audit failure rolls back. Independently passing SQLite tests and the
  actual MSSQL receipt support these boundaries. RV-001 remains a distinct
  response-serialization defect after successful persistence.
* #85 urgent human hazard intake/response was not routed through appointment,
  bundle, investigation or threshold gating. #91 quality, #102 controlled events,
  #101 coordinator and #117 rescan contracts remain in the base and were not
  replaced. No unmerged #92/#389 blanket hold or invented legal clearance appears.
* No mvp source, private dataset, real contact/roster, cloud IAM, paid AI,
  new-spend or operational-approval invention was required or performed.

## Validation Evidence

All independent commands used the existing editable-installed task .venv, public
tiny fixtures, PYTHONDONTWRITEBYTECODE=1 and worktree-local TMPDIR=$PWD/.venv.
Tests outside packages were added to import paths, not mvp. Fixture and HTTP
server cleanup ran; no persistent reproduction script was written.

| Command or experiment | Scope | Status | Result and interpretation |
| --- | --- | --- | --- |
| git status --short; git branch --show-current; git rev-parse HEAD; complete git diff pinned-base candidate | Boundary and complete patch | Passed | Branch/source match supplied candidate; only parent lifecycle artifacts and this review are dirty. |
| PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_quality_procurement.JsonFlows test_quality_procurement.SqlFlows -q | Existing focused procurement/quality JSON and SQLite classes | Passed | 95 tests, 0 skips, 17.543s. Expected injected recovery logs appeared. Passing assertions do not cover all counterexamples. |
| PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest test_procurement_api -q | Existing focused HTTP JSON/SQLite procurement suite | Passed | 12 tests, 0 skips, 9.512s, including confirmation and closure committed-projection retry assertions. |
| Inline existing-fixture reproduction: five eligible visits then threshold4 | JSON and SQLite configuration semantics | Counterexample confirmed | Count5, threshold4, investigation=None in both backends, RV-003. |
| Inline existing-fixture reproduction: whitespace competence, three confirmations, withdrawal | JSON and SQLite bundle/status semantics | Counterexamples confirmed | Blank competence reached Appointed/Committed; withdrawal retained Committed/missing=[], RV-004/RV-005. |
| Inline HTTP response-only json.dumps fault | Actual loopback HTTP with SQLite fixture | Counterexample confirmed | HTTP400 without committed marker despite durable REVIEW-SERIAL event; identical retry200, RV-001. Initial broader encoder injection also hit internal procurement serialization before commit and was not used as post-commit evidence; refined response-only predicate isolates the required boundary. |
| Inline role-canary reads | JSON and SQLite ordinary case versus work-order views | Counterexample confirmed | Same closure reason held on Quality Inspector case response but raw in work-order closure_history; private household text also exposed, RV-002. |
| Inline Node VM rendering of current ops.js functions | New committed offer, no legacy Booked entry | Counterexample confirmed | Both staff and provider trees omit actual selected date and period, RV-006. Not an actual-browser claim. |
| New form construction -> existing dirty guard -> route/success replacement trace | Changed web source and shared existing guard | Source-confirmed defect | No new-form dirty registration, retention or discard warning, RV-007. |
| node --check src/api/src/zava_forward/api/web/ops.js; git diff --check | Changed JS syntax and workspace whitespace | Passed | No syntax or diff-whitespace issue. |
| git diff --quiet 22c98267 -- src docs; sha256sum ops.js; review-record integrity check | Final read-only/source identity and persistent artifact | Passed | No source/docs drift; ops.js ec95ef3ad0def5772c389cb644df0e5d524691469a57a2909a0ad07cd4cdf3b8 matches the supplied final served-asset receipt. Exactly seven RV markers, no trailing whitespace or pending-verdict placeholder in this record. Matching the source hash is not a new image/browser run. |
| Fresh complete guidelines fetch and every changed web file read | Scoped web assessment | Completed | ops.js only; source-format findings recorded above. No full WCAG claim. |
| FINAL core323/API85/static-check receipts | Broader affected regressions and configured ruff/format/mypy | Assessed, not rerun in full | Reported 264 core passes/59 skips and 84 API/web passes/1 skip; final configured static checks passed. No failure is relabelled as a pass here. |
| FINAL actual MSSQL61/61 receipt | Owned SQL Server concurrency, audit, recovery, both closure/event winner orders and replay | Assessed, not rerun | Credible final candidate-source receipt; no actual SQL Server session was started here. |
| FINAL actual Chromium receipt | Manual confirmation, closure checkbox/cancel/accept, provider denial, keyboard and 320/390/1280 reduced-motion reflow | Assessed, not rerun | Engineering coverage accepted as stated, not all-rules/AT/human acceptance. |
| FINAL rebuilt hardened image receipt | Installed wheels, nonroot/read-only/cap-drop/no-new-privileges; health/login/order/closure/app and served ops hash | Assessed, not rerun | Actual source-context rebuild/runtime evidence is supplied. Reviewer did not build/run an image or independently certify it. |

## Blockers and Remaining Work

* No evidence-readiness blocker prevents completing this Review.
* Correctness/integration acceptance is blocked by RV-001 through RV-007.
  P01-P03 can remain executed Complete while their result is Not accepted.
* Parent must route a distinct later correction implementation and receipt,
  preserving this original adverse verdict. No source correction is made by
  the coordinator or this reviewer.
* Required original SQL/browser/image execution evidence exists; defects are
  not dismissed as hypothetical simply because those broader checks passed.
* Live policy, real authority/evidence, resident validation and accessibility
  acceptance remain human-owned limitations, not fabricated approvals.

## Outcome

* Execution: Complete.
* Outcome: Not accepted.
* Rationale: Seven substantive source-grounded defects remain, including
  reproduced post-commit misinformation and existing-role privacy bypass.
  Default sixth-event behavior and the authorized human closure engineering
  clarification are supported, but they do not cure these defects. No Conformant
  verdict is warranted by phase completion or the final positive receipts.
* This is the one immutable original finding set. Subsequent fixes/correction
  receipts must not amend this verdict or trigger a second Review.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defects RV-001 through RV-007 | Later rpi-implement | Parent delegates distinct correction work/receipt within accepted source direction; retain this Review. |
| Decision gap or invalid assumption | None found requiring rpi-plan | F8 and PC dispositions are reconciled and source-supported. |
| Material evidence gap | None requiring rpi-research | Supplied final gates plus independent counterexamples support a credible adverse verdict. |
| Non-blocking live/UX residual work | Existing OD-40/OQ-014 and #150/#151/#153 owners | Keep human ratification/evidence/AT/content acceptance separate from the correction task. |

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-87-appointment-controls-review.md](.copilot-tracking/reviews/logs/2026-10-18/issue-87-appointment-controls-review.md) | This single original Complete / Not accepted Review and complete finding set |
| [.copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md](.copilot-tracking/plans/2026-10-18/issue-87-appointment-controls-plan.md) | Current full P01-P03/F1-F8/AC plan with parent dispositions |
| [.copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md](.copilot-tracking/details/2026-10-18/issue-87-appointment-controls-phase-details.md) | Matching complete phase details and closure engineering boundary |
| [.copilot-tracking/changes/2026-10-18/issue-87-appointment-controls-changes.md](.copilot-tracking/changes/2026-10-18/issue-87-appointment-controls-changes.md) | FINAL implementation and validation receipts superseding historical blocks |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-87-appointment-controls-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-87-appointment-controls-plan-critique.md) | Frozen one critique, Complete/Revise, PC-001/PC-002 |
| [.copilot-tracking/research/2026-10-18/issue-87-appointment-controls-research.md](.copilot-tracking/research/2026-10-18/issue-87-appointment-controls-research.md) | Source-backed acceptance semantics and research boundaries |
| [.copilot-tracking/research/2026-10-18/subagents/issue-87-current-code-evidence.md](.copilot-tracking/research/2026-10-18/subagents/issue-87-current-code-evidence.md) | Supplied base-source inventory, not fresh validation |

## Next Steps

Active parent: preserve this original adverse Review unchanged; delegate a
separate later rpi-implement correction for RV-001 through RV-007 with a distinct
receipt and focused validation. Do not run another Review or claim this verdict
changed. Withhold the correctness/integration gate pending that separate
correction evidence; retain human live-adoption and UX follow-ups independently.
