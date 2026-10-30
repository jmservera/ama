<!-- markdownlint-disable-file -->
# Review: regulatory-assistant-208

## Scope and Evidence

* Task ID: 208
* Review date: 2026-10-27
* Review scope: complete P01-P03 synthetic slice and all 35 issue-criterion boundaries.
* Assessed implementation commit: c6ea1f05.
* Compared baseline: 0ded682bab690d24eb59b78e704be82d337bf6cd.
* Research: .copilot-tracking/research/2026-10-27/regulatory-assistant-208-research.md
* Plan: .copilot-tracking/plans/2026-10-27/regulatory-assistant-208-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/regulatory-assistant-208-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-27/regulatory-assistant-208-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/regulatory-assistant-208-changes.md

## Opening Review State

* Interpreted review goal: independently assess routing/authorization/atomicity,
  bounded content-free usage, evaluation/UI consistency and truthful acceptance
  evidence; retain the original one-pass outcome.
* Review scope: complete synthetic implementation, not operational approval.
* Evidence readiness: reconciled P01-P03 markers, details, 35-row actual
  criterion matrix, original Revise critique and six direct dispositions,
  local test/evaluation/browser summaries and original adverse outcomes.
* Acceptance basis: named issues, ADR 0005/0006, linked BRD/PRD boundaries,
  current plan requirements and synthetic slice acceptance criteria.
* First comparison boundary: implementation commit against recorded baseline;
  transaction-time role/case checks and complete saved conflict evidence,
  then metadata bounds and acceptance claims.
* Active read-only boundaries: no source, plan, details, critique, changes or
  research edits. Only this canonical review record may be updated by reviewer.
  No new model/cloud/data access, gate run, fixes or second Review.
* Initial blockers: mandatory complete publication gate conflicts with caller's
  explicit no-full-gate limit. DPO/Legal/Compliance, staff measurement,
  actual identity/deployed SQL and #440 acceptance remain unmet. Local tests
  cannot satisfy these human/publication gates.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one independent assessment completed on 2026-10-27
  against c6ea1f05b926d912ca38e901bf5509c554a65f7d and baseline
  0ded682bab690d24eb59b78e704be82d337bf6cd. Compared the frozen diff, affected
  functions and canonical tests, original critique/dispositions, all 35
  criterion rows, generated evaluation, supplied execution logs and browser
  output. Independently ran three pure usage tests and file-free SQL/JSON/
  grader probes. No full-suite rerun, gate, provider call or operational
  assessment was performed.
* Publication is Blocked; this does not mean the independent assessment was
  blocked. Task acceptance is separately Not accepted, as explained below.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Durable automatic conflicts and shared selected-turn referral writer | Reconciled | Supported conflict appends the stored question/answer pair, owner inbox and sender receipt in one repository transaction. No whole-request retry guarantee is claimed. |
| P01-T02 | Closed offline usage and privacy inventory | Reconciled | Zero inference, finite audit read window, current actor/role/day and explicit audit-only/partial coverage agree with code and tests. |
| P02-T01 | Comparator, independent usage expectations and regenerated report | Reconciled | Exact contract mutations, Unknown cost inputs and cards_only remain consistent; targets and human results are not accepted evidence. |
| P02-T02 | Existing native alert/chat presentation and browser extension | Reconciled | Receipt restoration uses persisted referred-turn records; usage and historical-usage states agree with API contracts. Scoped browser evidence is not WCAG or comprehension acceptance. |
| P03-T01 | Regressions, quality checks, documentation and criterion matrix | Reconciled | Supplied local results and original adverse outcomes are retained. The completed implementation marker covers evidence/handoff, not prior execution of this Review. |
| Follow-Up Items | Owner, Legal/Compliance/DPO and coordinator boundaries | Reconciled; open | Still outside implementation completion. Routes RV-001 to RV-006 preserve these boundaries. |
| Changes-discovered UX follow-up | Inherited draft-loss warning and raw provenance display | Reconciled; open | Kept outside active P01-P03 work; RV-007. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/regulatory_chat.py; src/core/tests/test_regulatory_chat.py | Shared automatic/manual referral writer; final sender/thread/owner/case checks; explicit JSON committed-audit-failure contract | ask, doubt, _owner and _refer; exact-pair/restart/idempotency/revocation/rollback tests | Supplied core/API results; actual SQL COMMIT injection read independently | No confirmed implementation defect in the supplied synthetic referral boundary. |
| P01-T02 | src/core/src/zava_forward/core/regulatory_usage.py; regulatory_chat.py; regulatory_privacy.py; rule_engine.py; src/core/tests/test_regulatory_usage.py | Closed zero-model counters and finite own-role/day read model; usage retained with parent records | MAX(seq)/primary-key window/CASE; JSON byte and complete-line tail; closed schema/type validation | Three pure tests and independent in-memory SQL/JSON probes passed; supplied affected core and API evidence | Engineering contract supported; no exact-turn, anonymity, intake-quota or retention-approval claim follows. |
| P02-T01 | src/agents/src/zava_forward/agents/regulatory_gates.py; src/agents/tests/regulatory_gate_fixture.py; test_regulatory_gates.py; src/agents/evals/regulatory_gates_results.json | Independently specified usage shape, negative controls and explicit economic unknowns | grade_answer, oracle and comparison; generated separate check outcomes and not_evaluated entries | Supplied agents suite/report; independent positive and six forged/missing-usage probes passed | Consistent closed-template engineering evidence, not independent human/legal grading or measured value. |
| P02-T02 | src/api/src/zava_forward/api/server.py; web/chat.js; src/api/tests/test_regulatory_chat_api.py; test_rule_alerts.py; src/api/checks/regulatory_ux_check.py | Guarded usage endpoint; zero-call labels; automatic receipt and restored sent state | Capability/generic-route guards; persisted receipt map; real conflict and history assertions | Supplied API suite and second browser report, 21 states with axe | UI/API behavior consistent with the slice; inherited residual UX and unperformed human checks remain explicit. |
| P03-T01 | src/core/README.md; src/agents/README.md; src/api/README.md; docs/reference/README.md; log.md; research/chat-memory-dpia.md; research/ux/regulatory-literacy-for-journeys.md | Update existing guides, synthesis, DPIA data map and index; append new log entry | Frozen diff preserves prior log/history and unapproved human decisions; no legal snapshot or memory update | Diff whitespace check passed; changed relative destinations and authority statements inspected | Documentation correctly distinguishes local synthetic evidence, separate JSON audit and operational/publication blockers. |

### Referral, authorization and persistence trace

* ask renders the bounded server-selected reply, then re-enters thread
  admission under the store lock and repository transaction before mutation.
  The original rowversion must still match. Conflict alone requires a uniquely
  named, currently registered exercise owner; missing/ambiguous owner and
  insufficient role/case access fail before storing that conflict.
* SQL admission rereads sender and recipient staff rows. Trusted-proxy sender
  role/capability claims survive re-admission rather than being replaced by
  wider staff-register rights. A trusted referral separately checks the
  recipient's recorded regulatory_chat capability. This is local request/
  store authorization, not evidence of live Entra revocation synchronization.
* The question copied is the exact stored, redacted question; the answer copy
  retains the exact stored cited versions/excerpts and metadata. No fresh
  retrieval substitutes evidence during referral. The recipient owns a new
  two-message thread and never gains access to the sender's original thread,
  other history or memory. This is inbox persistence, not email or human receipt.
* _refer scans stored receipt identities and deduplicates by source thread and
  assistant sequence. A subsequent manual doubt cannot duplicate an automatic
  referral for that stored turn. Equal-text new asks intentionally create new
  work; stale rowversions fail. Lost acknowledgements after successful commit
  are not covered by a request-idempotency promise.
* SqlRepo.txn owns BEGIN/COMMIT/ROLLBACK; repo.commit is only a no-op hook.
  The new real-COMMIT test wraps the connection, records an attempted COMMIT,
  raises before it takes effect, reopens and compares sender/inbox/receipt,
  ledger head and chain integrity. Separate tests exercise append-audit and
  message/inbox failures. These are credible SQLite engineering checks, not
  proof of deployed SQL or post-COMMIT acknowledgement recovery.
* JSON restores the chat preimage on pre-save failure. After a successful save,
  a separate audit failure retains durable pair/inbox/receipt and reports
  reload guidance. Its usage may therefore be missing. The core error, HTTP
  503 guidance, history restoration and coverage note agree; no cross-file
  atomicity or exact audit-derived daily turn total is asserted.

### Usage, deterministic checks and evaluation trace

* offline_usage contains task/schema/version identifiers, outcome, UTC day,
  the none model marker and zero counters/allowance. Callers supply fixed task
  versions and closed outcomes; questions, sources, resident facts and messages
  do not enter this shape. Audit envelopes still contain staff/case/thread
  identifiers and are not anonymous.
* SQL usage reads MAX(seq), then at most 1,000 primary-key sequence positions.
  CASE projects foreign actor/action details as NULL before Python receives
  them. JSON reads at most 256 KiB from the tail, discards a leading partial
  line when starting inside the file and keeps at most 1,000 lines. These are
  read bounds, not human-intake or deterministic-check limits.
* summarize filters the authenticated current role and usage UTC day, validates
  the complete known metadata shape including numeric types, and reports
  recorded outcomes. Legacy same-role unmetered events are explicitly a window
  count, not a reconstructed current-day count. Older records without role or
  missing post-save audit events cannot be attributed or reconstructed.
  recorded_audit_only and bounded_partial correctly avoid exact-total claims.
* RuleEngine adds usage to new immutable checks before existing alert
  publication copies them. Check identity, checkpoint/version selection,
  source eligibility, clocks, visibility, throttling and alert decisions are
  unchanged. Historical records without usage remain readable and are labelled
  unrecorded in the UI.
* The usage oracle is written independently of offline_usage; grader equality
  includes closed shape and exact value types, rejecting False as a zero
  counter. Citation support and answer-envelope checks remain separate.
  Unknown cost and missing acceptance denominator, dated price,
  attributable billing/allocation and review effort are explicit.
  Zero inference is not zero total service cost, financial authority or an
  accepted nonzero per-role budget.
* The report's 60,000 seeded stateless identities, 78,000 rule-hit denominator,
  120,000 state comparisons and 42,000 hazard cases are development observations.
  Separate provisional check outcomes, small SQLite integration,
  not_evaluated fields and cards_only prevent an aggregate ship/value claim.
  No new model, dependency, provider, schema or workflow/check rename appears
  in the frozen implementation diff.

### Criterion-by-criterion assessment

The identifiers below reconcile the plan allocation and changes record's actual
35-row matrix, not independently refreshed GitHub checkboxes. Issue bodies were
read by the parent/research; this assessment does not claim another GitHub
retrieval. Full issue acceptance remains unavailable for every named issue.

| Criterion | Independent assessment of supplied slice evidence | Remaining boundary / route |
| --- | --- | --- |
| 208.1 | #440 is explicitly tracked, not represented by these regressions | Coordinator checkpoint, RV-006 |
| 208.2 | ADR 0005 accepts synthetic development only | Operational decisions, RV-003 |
| 208.3 | Existing ordered components and scoped regression evidence are reconciled | Child acceptance/order ratification, RV-002/RV-006 |
| 208.4 | Closed exact excerpts/refusals and independent deterministic checks retain no-decision authority | Human/Legal grading, RV-003/RV-004 |
| 208.5 | Synthetic-only/privacy/capability admission remains fail-closed | Actual appointments and live approvals, RV-003/RV-005 |
| 214.1 | Fixed sections preserve provision/fact identifiers, source status/dates and 7/7 citation cases | Not generated-prose semantic acceptance, RV-004 |
| 214.2 | Role-projected facts, source-only narrower role and trusted-role preservation are supported | Actual provider/query privacy evidence, RV-005 |
| 214.3 | 17 refusal cases and unsafe/mixed/future/terms negative controls support the closed path | Held-out/Legal acceptance, RV-003/RV-004 |
| 214.4 | Automatic conflict contains both stored versions and durable owner receipt | Only registered exercise owner, RV-003 |
| 214.5 | Manual selected-turn writer remains available and per-turn idempotent | No operational appointment or received human decision, RV-003 |
| 214.6 | Retrieved source text remains quoted data, with hostile-source/question controls | No actual-model assurance claimed, RV-004 |
| 214.7 | Added usage/referrals cannot change engine records; suppression tests preserve alerts/holds | No model-negative study claimed, RV-004 |
| 214.8 | Exact persisted pair/citations, restart and actual COMMIT-before-effect rollback are supported | JSON ledger separate; no lost-ack guarantee |
| 214.T1 | Question/check/alert zero calls, outcomes, current role/day, finite read window and explicit unknowns agree | No accepted paid/nonzero budget or exact turn total, RV-002 |
| 216.1 | Independent fixture and mutation grading are useful provisional checks | Owner agreement and independent graded set, RV-002/RV-004 |
| 216.2 | Hazard misses are classified critical; supplied seeded run has zero misses | Synthetic baseline only, RV-004 |
| 216.3 | Stateless 60,000-home report and small SQL integration are correctly labelled | Continuing-stock baseline/review, RV-002/RV-004 |
| 216.4 | Same-source comparator remains not_evaluated/cards_only | Paired staff value measurements, RV-002/RV-004 |
| 216.5 | Existing freshness metadata and source-changed browser states are retained | Live monitoring/currentness not established, RV-005 |
| 216.6 | Named check results and denominators remain separate | No aggregate acceptance |
| 216.T1 | Cost per accepted check is Unknown with four named missing-input groups | Acceptance denominator/prices/billing/review time, RV-002/RV-004 |
| 216.T2 | Finite zero-model path and absent paid authority/expiry are explicit | No paid run approved or needed; later model work needs a separate owner decision |
| 215.1 | Seven-role guidance and supplier denial are supported | Actual role-needs/comprehension evidence, RV-004 |
| 215.2 | Alert source/status/action/owner/clock and usage are coherent | Fictional clocks are not statutory acceptance, RV-003 |
| 215.3 | Native controls, text status, keyboard/plain mode and 21 browser/axe states are supported | No full WCAG/assistive-technology acceptance, RV-004; residual UX RV-007 |
| 215.4 | No-source/refusal/manual route and automatic/restored conflict receipt agree | Exercise routing is not legal approval, RV-003 |
| 215.5 | Staff comprehension is explicitly Not run | Repairs/housing/grants study, RV-004 |
| 217.1 | DPIA remains draft and actual/live use is denied | Actual DPO assessment, RV-003 |
| 217.2 | Unknown/simulated periods and inherited usage retention are honest | DPO periods/disposal/holds/rights, RV-003 |
| 217.3 | Offline minimised retrieval and content-free metering add no provider processing | Actual Foundry/privacy/terms evidence, RV-005 |
| 217.4 | Capability separation and trusted-role denial/read isolation are supported | Actual Entra assignments/ingress, RV-005 |
| 217.5 | SQL turn/referral/audit commits together; lifecycle/check/alert audit boundaries remain | JSON separate ledger and DPO retention, RV-003 |
| 217.6 | Supplied cross-role/injection and final transaction revocation checks support the local path | No deployed security acceptance, RV-005 |
| 217.7 | Existing named-human/reasons checks are retained | Legal applicability and real appointments, RV-003 |
| 217.T1 | Closed, scoped metadata, bounded reads, rollback and DPIA inventory are supported | Actual DPO periods/rights/assessment, RV-003 |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/P01-T02 | Clarify bounded audit-only reads, local authorization, per-turn dedupe and separate JSON failure outcomes | PC-001 to PC-005; compatible direct planner corrections, no new user decision required | Current FR/NFR/acceptance, phase sequencing and changes match | Original Revise retained; six dispositions recorded separately before implementation | Compatible clarification, not an unreviewed new authority or broader retry/storage feature. |
| P03-T01 | Add actual 35-row issue allocation and executed-evidence matrix | PC-006 and supplied issue retrieval | Plan allocation and changes actual-evidence rows match | Original critique remains unchanged | No issue checkbox or human approval inferred. |
| P01/P02 implementation | Correct unbound rollback flag, preserve trusted-role marker, fix formatting/types and duplicate status selector | Original failed tests/lint/mypy/browser runs preserved in changes and supplied logs | Current code and subsequent results reconcile those corrections | No material scope change; no second critique | Corrections preserve accepted direction; not open defects at frozen head. |
| P03 implementation marker | Mark local implementation/evidence ready for the next lifecycle Review | Actual test/browser/migration evidence and explicit handoff | Plan/details/changes agree that Review had not yet run | This record supplies the single independent Review | No retroactive claim of earlier Review success. |
| Follow-Up Items | Keep human acceptance, #440, publication and inherited UX outside implementation | Known missing authority/evidence and changed-web inspection | Mirrored in plan/changes where applicable | No active tasks silently added | Open routes remain explicit below. |

## Critique and Material Revision Assessment

* Latest critique dispositions: all PC-001 through PC-006 have compatible direct
  planner dispositions. Original verdict remains Revise with two High and four
  Medium findings; this Review does not replace it with a retrospective Pass.
* PC-001 resolves to finite SQL/JSON audit traversal and honest coverage;
  PC-002 to distinct JSON pre-save/post-save and SQL outcomes; PC-003 to
  sender/thread/owner/case checks under the local mutation boundary while
  retaining trusted authenticated role; PC-004 to stored-turn dedupe, not ask
  replay; PC-005 to actual SQL COMMIT-before-effect injection; PC-006 to the
  complete 35-row criterion inventory and actual evidence allocation.
* Material revisions: no material scope divergence identified in the supplied
  implementation. New code stays in the ADR 0006 src namespace, tests outside
  packages, with 11 added test methods and zero removals within the 20-method
  budget. Existing dated acceptance limitations are preserved.
* Dependent-work pause assessment: current plan/details explicitly record
  direct dispositions before implementation. This is artifact evidence of
  sequencing, not an independently reconstructed wall-clock event history.
  No evidence of resumed work depending on an unresolved divergent decision
  was identified.
* Justification assessment: the synthetic slice is consistent with ADR 0005,
  BRD FR-051/AC-099/OD-50 and PRD FR-060/AC-104 to AC-106/OQ-026.
  Those documents expressly do not supply actual human acceptance or release
  authority. Publication remains blocked rather than justified by divergence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Evaluation tasks/thresholds and paired staff trial | Code cannot ratify targets, define accepted checks or fabricate participant results | Exercise owner agrees protocol; authorised researchers then collect evidence | Open; RV-002 decision and RV-004 evidence routes |
| Actual appointments, DPIA, retention and role separation | Synthetic exercise identities and references are not actual authority | Legal/Compliance/DPO and identity owners, coordinated by parent | Open; RV-003 decision and RV-005 evidence routes |
| #440 stabilization and publication reconciliation | Separate checkpoint and mandatory full receipt are absent | Coordinator/owner resolves gate conflict and checkpoint without bypass | Open; RV-001 and RV-006 |
| Inherited unsaved question drafts/raw provenance display | Pre-existing UI behavior; not introduced by routing/usage slice | UX owner triages narrowly scoped draft recovery/localization work | Open distinct residual UX-208-DRAFTS; RV-007 |

Unresolved follow-ups remain outside active P01-P03 implementation, completion
and acceptance claims. They are not implementation defects merely because
this Review records them.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Mandatory publication evidence is unavailable and cannot be substituted

* Related scope: P03-T01; publication only, not a source-code defect.
* Evidence: repository instructions and src/README.md local RPI gate require a
  complete final-candidate gate for this boundary; plan/changes explicitly say
  neither --all nor --changed ran. The caller forbids both during Review and
  has not authorised the required complete run. Supplied tests are not a
  clean exact-head/base receipt.
* Impact: no push/publication-ready or hosted/human approval claim is supported.
  The local assessment can finish, but publication must remain Blocked.
* Destination: rpi-plan, parent/owner publication-policy reconciliation.
* Smallest useful next action: record an explicit compatible authority path
  before publication. If the required complete run becomes authorised, the
  parent must first commit the candidate and original dated evidence, run the
  complete gate with approved external storage, and verify its receipt against
  the then-current head/base. No waiver, partial substitute or run is authorised
  by this finding.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Owner acceptance and chat-value decisions remain unaccepted

* Related scope: 208.3, 214.T1, 216.1/216.3/216.4/216.T1; outside the code slice.
* Evidence: plan Follow-Up Items; changes criterion matrix; generated report
  threshold.status values provisional_not_agreed/unset_pending_baseline_review,
  paired_staff_comparison not_evaluated, null staff measurements and cards_only.
  ADR 0005 requires measured value before chat shipment.
* Impact: local engineering completion cannot close child acceptance, approve
  targets, provide an accepted-check denominator or ship chat as a proven
  improvement. Zero enabled inference is not a paid budget decision.
* Destination: rpi-plan, exercise owner.
* Smallest useful next action: obtain recorded owner decisions on eligible
  tasks, quality/hazard gates, accepted-check definition and a paired comparison
  protocol before collecting acceptance evidence. Retain cards_only and
  Unknown economics; do not infer a paid/nonzero budget.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Real Legal, Compliance and DPO decisions remain outside exercise authority

* Related scope: 208.2/208.4/208.5, 214.4/214.5, 215.2/215.4,
  217.1/217.2/217.5/217.7/217.T1; human decision boundary.
* Evidence: ADR 0005 exercise-owner table; BRD OD-50/PRD OQ-026;
  docs/reference/research/chat-memory-dpia.md draft, unresolved periods/rights
  and new automatic-disclosure review requirement; synthetic admission and
  SYNTH references; unchanged acceptance checkboxes.
* Impact: named exercise routing and stored receipts are not legal advice,
  applicability decisions, appointments, DPO approval, consent or assurance
  that any duty is satisfied. Automatic disclosure frequency and potentially
  identifying audit metadata still require actual privacy review.
* Destination: rpi-plan, parent to named actual Legal/Compliance/DPO owners;
  distinct human-authority follow-up HUMAN-208-AUTHORITY, not a source fix.
* Smallest useful next action: record actual accountable owners/delegations and
  their review decisions for necessity, recipients/notice, lawful purpose,
  role separation, retention/holds/disposal/rights and significant-decision
  applicability before proposing operational reliance. Preserve live blocking.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Engineering evaluation and axe evidence do not supply the missing human or continuing-stock evidence

* Related scope: 214.1/214.3/214.6/214.7; 216.1 to 216.5/216.T1;
  215.1/215.3/215.5; material evidence gap outside P01-P03.
* Evidence: report evidence.stock_scope and not_evaluated entries; same-source
  structural comparator; browser output staff_comprehension "Not run; unmet";
  changes recorded 60,000 stateless identities and no staff trial. The
  independently authored usage oracle is still development fixture evidence,
  not an independently human-graded held-out set.
* Impact: no operational recall, staff alert precision/acknowledgement,
  comprehension, measured review effort/value/cost or full WCAG acceptance can
  be inferred. No actual-model assurance is needed or claimed for this
  zero-provider slice.
* Destination: rpi-research, authorised evaluation/UX research owner after
  RV-002 and any relevant RV-003 permissions.
* Smallest useful next action: define an evidence collection package separating
  continuing-stock validation, held-out human grading, paired repairs/housing/
  grants tasks and manual assistive-technology checks; preserve separate
  denominators and original provisional results. Do not start participants,
  private data or model calls under this Review.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: Local identity, SQLite and no-provider checks are not deployed-platform evidence

* Related scope: 208.5, 214.2, 216.5, 217.3/217.4/217.6; outside local slice.
* Evidence: supplied API skips, generated azure_sql/actual_model not_evaluated
  fields, synthetic trusted-role tests and current READMEs. No actual Entra
  assignments/ingress, deployed SQL, live currentness or Foundry privacy/terms
  evidence is supplied; none was retrieved during Review.
* Impact: transaction tests and capability mapping cannot establish production
  identity enforcement, platform atomicity, live source currentness or actual
  provider data minimisation. This is not a defect in the authorised offline
  implementation and is not permission to introduce a provider.
* Destination: rpi-research, identity/platform/privacy evidence owners under a
  separately authorised future scope.
* Smallest useful next action: inventory the exact deployment evidence needed
  for the intended future platform, mark unavailable items explicitly and
  obtain authority before any live verification or consequential legal-source
  currentness check.

<!-- rpi:review id=RV-006 -->
### RV-006 [Medium]: Epic stabilization and closure remain separate coordinator work

* Related scope: 208.1/208.3 and plan Follow-Up Items.
* Evidence: plan and changes name #440 as unmet; no checkpoint or full
  child-phase acceptance is supplied. All five named issues remain Refs,
  deliberately not Closes.
* Impact: this one bounded Review cannot certify whole-epic stabilization,
  satisfy #440 or close any issue in full.
* Destination: distinct follow-up STABILIZE-208-440, backlog coordinator/owner.
* Smallest useful next action: retain the dependency and obtain its independent
  checkpoint plus child acceptance decisions through its existing workstream;
  do not expand this Review or mark issue boxes.

<!-- rpi:review id=RV-007 -->
### RV-007 [Low]: Inherited draft-loss and timestamp presentation remain nonblocking UX residuals

* Related scope: P02-T02 changed-file review; existing behavior, not a newly
  introduced implementation defect.
* Evidence: src/api/src/zava_forward/api/web/chat.js:190 - question draft has
  no navigation-loss guard; src/api/src/zava_forward/api/web/chat.js:114 and
  :150 - source/alert provenance timestamps remain raw. The changes record
  already discloses these boundaries. New usage period/numbers use Intl.
* Impact: a draft can be lost when navigating; technical timestamp strings can
  be harder to read. Neither finding invalidates stored referral evidence,
  adds legal authority or turns scoped axe evidence into conformance.
* Destination: distinct follow-up UX-208-DRAFTS, UX/frontend owner.
* Smallest useful next action: triage draft recovery/navigation warning and
  readable provenance formatting while preserving exact source records and the
  repository's native/Fluent/plain-language constraints.

## Defects

* No confirmed in-scope implementation defect identified at the frozen head.
  No rpi-implement handoff is issued. This is a bounded assessment, not proof
  that the repository or deployed system has no defects.
* RV-001 to RV-006 are decision/evidence/dependency boundaries, not source bugs.
  RV-007 is inherited nonblocking residual work. Do not implement fixes during
  Review or convert these follow-ups into active P01-P03 tasks.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-plan | Parent/owner reconciles publication authority, then required exact-candidate gate if authorised | Publication decision conflict, no substitute receipt |
| RV-002 | rpi-plan | Exercise owner records acceptance tasks/thresholds/denominator and comparison protocol | Unaccepted owner decisions |
| RV-003 | rpi-plan; HUMAN-208-AUTHORITY | Actual Legal/Compliance/DPO owners record authority/privacy/rights decisions | Actual human decisions cannot be synthesized |
| RV-004 | rpi-research | Evaluation/UX research owner collects separately authorised evidence after decisions | Human/continuing-stock evidence absent |
| RV-005 | rpi-research | Identity/platform/privacy owners define then verify authorised deployment evidence | Local tests are not deployed acceptance |
| RV-006 | STABILIZE-208-440 follow-up | Backlog coordinator retains and resolves existing stabilization dependency | Outside active implementation scope |
| RV-007 | UX-208-DRAFTS follow-up | UX/frontend owner triages inherited draft recovery/provenance readability | Nonblocking residual, not new defect |

Later implementation of any routed work does not require another Review of
this task. Preserve this original outcome and its adverse/limited evidence.

## Residual Work

* HUMAN-208-AUTHORITY: actual owner/delegation, privacy and legal decisions,
  coordinated through RV-003, remain outside this synthetic slice.
* EVAL-208-ACCEPTANCE: owner decisions precede the continuing-stock, held-out,
  paired-value, comprehension and manual accessibility evidence in RV-002/
  RV-004. No acceptance result is fabricated.
* PLATFORM-208-EVIDENCE: separately authorised identity/deployed SQL/source/
  provider evidence in RV-005; no live check or model run authorised here.
* STABILIZE-208-440: coordinator checkpoint and issue-level acceptance remain
  distinct. UX-208-DRAFTS is a separate nonblocking frontend follow-up.

## Blockers and Remaining Work

* Publication blocker: RV-001, mandatory complete gate not run and forbidden
  by current caller authority. No push, PR, issue mutation or waiver is
  authorised by this Review.
* Task/full-issue and operational acceptance blockers: RV-002/RV-003 decisions,
  RV-004/RV-005 evidence and RV-006 stabilization remain unmet. They did not
  block independent assessment of the agreed synthetic slice.
* Remaining active P01-P03 implementation work: none identified from supplied
  scope/evidence. No source correction, new plan task or second Review was
  performed.
* Review write boundary: only this canonical record changed. The pre-existing
  modified session-state file and all original research/plan/details/critique/
  changes/source/test artifacts were left untouched. No commit/push occurred.

## Validation Evidence

Supplied implementation results below were inspected, not independently
rerun unless explicitly marked. Successful exit status does not convert
skipped, unavailable or outside-scope acceptance checks into passes.

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| git diff baseline..c6ea1f05; current function/test reads | Complete supplied affected slice and direct helpers | Passed, independent inspection | Frozen source and recorded semantics reconcile; no confirmed in-scope defect. |
| PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/tests session-venv/bin/python -m unittest test_regulatory_usage -q | Three pure metadata/economics tests | Passed, independently executed | 3 tests, 0.000s, OK; no data files or provider calls. |
| Inline Python probe using the supplied venv and test-only PYTHONPATH | In-memory SQL ledger, BytesIO JSON tail and independently authored oracle | Passed, independently executed | 1,105 SQL positions include foreign invalid-JSON detail, own other-role/day and legacy events; correct partial/own-day result. JSON excludes foreign content. Positive oracle and six forged/missing-usage controls behave correctly. No files/provider calls. |
| git diff --check 0ded682..c6ea1f05 | Frozen implementation diff | Passed, independently executed | No whitespace errors. |
| Affected eight core suites | Chat/usage/privacy/engine/cards/freshness/thread/privacy paths | Passed, supplied log inspected | 114 tests, OK; transaction and restart tests read in source. |
| Agents unittest discovery | Agents package | Passed, supplied log inspected | 106 tests, OK; no duplicate discovery run during Review. |
| API unittest discovery with test-only PYTHONPATH | API package | Passed with skips, supplied log inspected | 1,122 run in 797.893s; 808 passed, 314 skipped. Skips are not deployment/cloud acceptance. |
| Ruff check and format; mypy per core/agents/API; node --check chat.js | Affected packages/JS | Passed, supplied implementation evidence | Typed source counts 155/23/88; no independent quality rerun claimed. |
| python tools/rename-zava-tests.py in prepared venv | Namespace/migration guard | Passed, supplied log inspected | 25 tests, OK after existing declared dependency installation; original missing-dependency errors preserved. |
| Existing frozen evaluation runner/report | Seed 174 stateless 60,000-home development run | Passed provisional checks / human checks unavailable | Citation 7/7; contract 24/24 including 17 refusal cases; rule hits 78,000/78,000; agreement 120,000/120,000; hazards 42,000, zero misses; small SQLite integration. Not ongoing-stock/model/human acceptance. |
| regulatory_ux_check.py, first attempt | Original changed-surface browser run | Failed, preserved | Duplicate role=status caused strict selector failure. Existing log retained; corrected code uses a polite usage paragraph without duplicate status role. |
| regulatory_ux_check.py, second attempt with pinned axe | Actual loopback Chromium 156.0.8078.4 / axe 4.10.3 | Passed, supplied report inspected | 21 states, keyboard/roles/widths/plain mode/conflict/restoration/usage; no participant or whole-WCAG claim. Axe SHA-256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb. |
| Fresh web-interface-guidelines retrieval and complete changed chat.js read | Changed UI, repository Fluent/WCAG/plain-content rules take precedence | Completed, independent inspection | Full source fetched from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md on review date. RV-007 records inherited residuals; this is not whole-file conformance. |
| tools/rpi-checks.py --all / --changed | Publication gates | Not run, blocked by explicit boundary | Neither was invoked. No partial evidence substitutes for the mandatory complete receipt. |
| Actual Entra/deployed SQL, DPO/legal decisions, staff studies, ongoing stock, full assistive-technology acceptance and #440 | Outside authorised local synthetic slice | Unavailable / not performed | Remain distinct decision/evidence/coordinator routes RV-002 to RV-006. No operational acceptance inferred. |

Original implementation failures (imports, rollback flag, trusted-role marker,
format/type checks, duplicate browser status and missing migration dependencies)
remain recorded in the unchanged changes record. This Review neither erases
them nor treats their later correction as acceptance by a human.

## Outcome

* Outcome: Not accepted.
* Outcome rationale: the bounded synthetic implementation is consistent with
  its plan and supplied engineering evidence, with no confirmed in-scope code
  defect identified. Nevertheless, required publication evidence and material
  owner/Legal/Compliance/DPO acceptance decisions remain unavailable, as do
  the explicitly required human/platform/continuing-stock evidence and #440.
  Complete Review execution and local engineering success do not accept
  #208 or any of #214/#216/#215/#217 in full, authorise chat shipment or permit
  operational/legal reliance.
* No source fix or second Review was performed or requested. The parent owns
  continuation through the distinct routes below, retaining this original
  outcome.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No confirmed in-scope defect; no rpi-implement handoff |
| Decision gap or invalid assumption | rpi-plan, RV-001/RV-002/RV-003 | Parent/owner reconciles publication and obtains actual acceptance/authority decisions |
| Material evidence gap | rpi-research, RV-004/RV-005 | Authorised evaluation/UX/identity/platform/privacy owners obtain separately scoped evidence after decisions |
| Non-blocking residual work | STABILIZE-208-440 and UX-208-DRAFTS | Coordinator handles existing stabilization dependency; UX owner triages inherited UI residual. Stabilization remains blocking for epic closure, not for this code slice. |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: independent frozen-diff/function/test/artifact
  assessment, three pure tests and file-free probes; supplied core/agents/API/
  quality/evaluation/migration/browser evidence inspected. Unperformed
  publication, deployed and human checks remain explicit.
* Blockers: no mandatory full receipt; no actual human acceptance/appointments/
  privacy decisions, required human/platform/ongoing-stock evidence or #440
  checkpoint. Publication stays Blocked.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/regulatory-assistant-208-research.md](.copilot-tracking/research/2026-10-27/regulatory-assistant-208-research.md) | Canonical research and authority boundary |
| [.copilot-tracking/plans/2026-10-27/regulatory-assistant-208-plan.md](.copilot-tracking/plans/2026-10-27/regulatory-assistant-208-plan.md) | Current P01-P03 plan and 35 criterion allocations |
| [.copilot-tracking/details/2026-10-27/regulatory-assistant-208-phase-details.md](.copilot-tracking/details/2026-10-27/regulatory-assistant-208-phase-details.md) | Current implementation and validation contracts |
| [.copilot-tracking/reviews/plans/2026-10-27/regulatory-assistant-208-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/regulatory-assistant-208-plan-critique.md) | Preserved original Revise critique |
| [.copilot-tracking/changes/2026-10-27/regulatory-assistant-208-changes.md](.copilot-tracking/changes/2026-10-27/regulatory-assistant-208-changes.md) | Actual criterion evidence and original adverse results |
| [src/agents/evals/regulatory_gates_results.json](src/agents/evals/regulatory_gates_results.json) | Separate provisional results and unmet human/platform measures |
| [.copilot-tracking/reviews/logs/2026-10-27/regulatory-assistant-208-review.md](.copilot-tracking/reviews/logs/2026-10-27/regulatory-assistant-208-review.md) | This task's one independent Review and original outcome |

## Next Steps

Return this record to the active parent and stop. The parent should route
RV-001/RV-002/RV-003 to planning and actual decision owners,
RV-004/RV-005 to separately authorised research, RV-006 to the existing #440
coordinator workstream and RV-007 to the distinct UX follow-up. No
rpi-implement action is supported by a confirmed defect in this assessment.
Do not invoke another Review, modify issue acceptance, or publish while the
mandatory gate and other applicable acceptance blockers remain unresolved.
