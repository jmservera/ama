<!-- markdownlint-disable-file -->
# RPI Plan Critique: Grant lifecycle controls

## Metadata

* Task ID: 95
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/grant-lifecycle-controls-95-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/grant-lifecycle-controls-95-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate assessment; no further critique dispatched or performed.

## Inputs and Criterion Boundary

* Caller requirements: no dashboard presents opportunity as award/cash; only designated human financial authority submits, certifies or records receipt. Verify existing grant records and second approver, preserve #94, and assess authority versus role, transaction-time changes, actor aliases, rollback/audit and test ownership.
* Inputs: the supplied plan and phase details; .copilot-tracking/research/2026-10-17/grant-lifecycle-controls-95-research.md, especially C4-C8; original case, addendum, knowledge-base index and owner memory.
* Source evidence: src/core/src/zava_forward/core/grants.py, finance.py, change_provenance.py, store.py, sqlstore.py, mssqlstore.py and controls.py; src/core/tests/test_finance_signoffs.py and test_finance_match_controls.py; src/api/tests/test_finance_match_api.py; src/api/src/zava_forward/api/auth.py and web/panels.js and web/app.js. PRD FR-019/042 and AC-022/050 were checked for scope distinction.
* Decisions accepted: explicit scoped dated synthetic human designation in trusted staff; registered current actor; reuse existing finance operation/recovery/SQL hook; strict GBP; existing separate application records. No real delegation or automatic authority seed, private roster/data, Azure/model/financial execution, full pack/export/form workflow or base changes.
* Dependencies: existing #94 controls at the supplied d400eb8d base; #93 is hierarchy only. Read-only git inspection confirmed that base and the existing fix/grant-lifecycle-controls-95 branch. Supplied untracked parent artifacts were not moved or edited.
* Assessment boundary: planning credibility for these exact two criteria and preservation of shared finance behavior, not implementation acceptance or full PRD acceptance. All findings below are directly applicable planner corrections; none requires a divergent user decision.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Exact criterion 1; C7; acceptance criterion 1 | Partial | Grant history renders states separately, but the application panel explicitly calls confirm an award; PC-001. |
| Exact criterion 2; C4/C5/C8; P01-T02 | Partial | Trusted current actor and designation are correctly proposed; exact state/scope policy and commit-time temporal eligibility remain underspecified; PC-002/003. |
| Existing grant records and second approver; C4/C6 | Covered with compatibility gap | Existing state machine and email-only check verified; reuse of #94 independence is appropriate, but old pending provenance needs a disposition; PC-005. |
| Application/grant/provider-finance separation; C5; goals | Partial | Separate objects already exist; funding_step currently lacks per-event authority/evidence history; PC-004. |
| #94 rollback/audit and SQL hook; C6; P01-T02/T03 | Covered with test gap | Reuse is appropriate, including prior audit preservation and original-error behavior; path-specific ownership/evidence must be explicit; PC-006. |
| Alias, stale actor and legacy identity checks; P01-T01 | Covered with test precision needed | Email/code/OID capture and legacy lookup are specified; retain genuinely registered aliases and fallback refusal in the test matrix; PC-006. |
| GBP and event-local amounts; acceptance criteria 1/2 | Covered with compatibility gap | Strict currency refusal and no opportunity carry-forward are explicit; legacy pending amount/currency must not acquire invented provenance; PC-005. |
| Local SQL Server, API, docs and independent Review; P01-T03 | Covered | Actual SQL parity, authenticated loopback, honest blocked checks and one independent Review are appropriate; avoid inherited finance tests standing in for grant coverage; PC-006. |
| Full forms/export/pack scope, real authority and live actions | Covered | Explicit exclusions are compatible with caller direction; do not reopen them to resolve these findings. |

## Verdict

* Verdict: Revise
* Rationale: The bounded architecture is credible, but the final candidate still leaves an observable award-label counterexample, an incomplete executable authority contract, commit-time expiry semantics, application-event evidence, and legacy-pending compatibility unresolved. These are small, compatible planning corrections, not grounds for a new research phase or expanded form workflow.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Application confirmation can still announce an award without a grant award record

* Related IDs: exact criterion 1; C5/C7; acceptance criterion 1; P01-T01/T03.
* Evidence: src/api/src/zava_forward/api/web/app.js:878-902 calls the application confirm control "Funder confirmed the award". src/core/src/zava_forward/core/store.py:891-921 changes only funding.status and funding_ok on confirm; it neither requires an Award grant event nor accepts new confirmation evidence. src/api/src/zava_forward/api/web/panels.js:50-66 correctly renders grant states separately. The plan asserts no web changes are needed from the narrower absence of monetary aggregates.
* Concern: A case may retain only an Opportunity grant while the separate application flow offers an award-confirmation label. Absence of GBP 40 million or monetary totals does not settle whether this visible language promotes application/opportunity evidence into award semantics.
* Impact: The first exact criterion could be claimed from projection tests while a contradictory existing rendered label remains.
* Smallest useful change: Add an explicit mixed-state scenario, with an Opportunity-only grant and a separately submitted/confirmed application, to the criterion-1 assessment. Resolve and document what confirm means. If it is application disposition only, include the smallest neutral label/projection correction required; do not redesign the page or infer an award. A no-web-change conclusion needs affirmative evidence for this counterexample, not just absence of grant totals.
* Action owner: Planning parent; implementation owner for the resulting scoped regression/correction.
* Exact resolving evidence: Revised acceptance mapping names this scenario and the actual displayed strings; returned funding/case/stat projections preserve Opportunity and do not create award/cash. Static trace of the final application/grant labels is consistent with that evidence, with any required narrow web validation disclosed.
* Decision route: Directly applicable planner correction. Caller prohibits misleading presentation, not a surgical correction needed to satisfy it; no full UI or pack workflow is requested.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Define designation as an exact transition-and-scope contract, not a generic grant approval capability

* Related IDs: exact criterion 2; functional requirements; P01-T01/T02.
* Evidence: src/core/src/zava_forward/core/grants.py:23-65 uses one grant_approve action for Opportunity, Award, Claimable, Submitted, Accepted/Rejected and Cash received. controls.py:10-11 supplies broad permitted roles. The plan requires an "action-scoped" designation but does not enumerate its match against the pending target state or define its case/scheme binding and validity fields.
* Concern: A single grant_approve designation could unintentionally authorize recording cash merely because it authorized approving an opportunity. Likewise, a designation scoped to one fictional scheme/case could be accepted for another. Human and synthetic labels without an exact validation predicate are not an implementable authority policy.
* Impact: Role-only access may be replaced by an equally overbroad capability; negative tests for missing designation alone would not detect it.
* Smallest useful change: Specify one compact trusted-staff designation schema and action/target-state matrix. Define exact case/scheme or route matching, subject binding, explicit human/exercise classification, accepted status, source, effective-from/expiry rules and runtime production refusal. Define malformed/ambiguous scope refusal and prohibit request-supplied widening. Retain the existing role gate as an additional constraint, not the authority source.
* Action owner: Planning parent defining the contract; implementation owner implementing its predicate.
* Exact resolving evidence: Plan/details contain the matrix and minimal fictional fixture. Targeted tests show that approval of Opportunity does not authorize Submitted/Accepted/Cash received, another scheme/case/route is refused, the wrong application action is refused, body-supplied designation cannot authorize, and only a correctly scoped registered human succeeds. Production-mode refusal is exercised independently of the designation's synthetic label.
* Decision route: Directly applicable planner correction, implementing the caller's already-selected scoped synthetic designation. No real authority administration is added.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Snapshot equality at commit does not establish that a designation is still effective

* Related IDs: current actor at write/commit time; functional requirements; P01-T01/T02.
* Evidence: src/core/src/zava_forward/core/change_provenance.py:15-35 compares only email/code/name/role/OID. finance.py:55-64 repeats registered actor and independence validation inside SqlStore.save's transaction. The phase details add exact designation snapshot comparison at commit, but do not explicitly repeat its time-window predicate.
* Concern: An unchanged persisted designation can expire between initial validation and save. Conversely, changes confined to designation fields pass the existing _actor comparison unless the new hook separately checks them. A snapshot equality test alone misses the first case.
* Impact: A submit/certify/receipt record can commit after its authority has expired even when no staff row changes; revocation tests alone can falsely establish current authority.
* Smallest useful change: Require the full designation predicate, including effective dates against a fresh timezone-aware server time, under the existing writer transaction as well as at entry. Compare the selected authority snapshot to detect replacement/revocation, and keep designation-only changes independent of case sequence/cache refresh. Do not use the dataset as_of date as the authorization clock.
* Action owner: Planning parent for the invariant; implementation owner of the shared validation extension.
* Exact resolving evidence: A controlled-clock test advances through expiry after initial validation but before transaction validation with no designation mutation, and refuses without state/success audit. Separate SQLite/actual MSSQL tests mutate only persisted designation scope/status/source before the transaction, without changing identity fields or case sequence, and show refusal and correct reopened state. A valid unchanged designation remains usable.
* Decision route: Directly applicable planner correction. No new locking implementation or live identity system is required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Application authority events need an explicit persistent evidence contract

* Related IDs: separate funding application records; exact criterion 2; goals; functional history requirement; P01-T02.
* Evidence: src/core/src/zava_forward/core/store.py:891-921 records approved_by as a name, submission reference, and current status; audit detail is only the status. There is no funding event history, confirm accepts no separate evidence, and later state overwrites do not retain action-specific designation snapshots. The plan's history requirement does not identify the funding record shape or its per-action evidence mapping.
* Concern: Hardening funding_step's gate alone would not retain who exercised which designation for submission/confirmation. "History adds..." may be implemented only for the existing grants history, leaving the other newly controlled path unauditable.
* Impact: A reopened application cannot demonstrate that each authority-bearing transition was recorded by the designated human or distinguish submission evidence from confirmation evidence.
* Smallest useful change: Explicitly assign funding_step a minimal append-only event history for approve/submit/confirm with server action/time, current actor identity, relevant route/case, selected designation snapshot and the supplied evidence/reference appropriate to that event. Keep existing status/reference compatibility. Define missing evidence refusal without implementing pack/version/export workflows or inferring grant/cash.
* Action owner: Planning parent and store.py implementation owner.
* Exact resolving evidence: Named tests reopen funding after each transition and compare exact per-event identity/designation/reference fields. Different designated humans can submit and confirm without losing either identity; missing confirmation evidence refuses; grant/provider-finance records remain byte-for-byte logically unchanged. Earlier application events cannot be overwritten by later ones.
* Decision route: Directly applicable planner correction. This is minimal record provenance for the chosen controlled path, not full PRD AC-022/050 acceptance.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Resolve pre-existing pending grants without inventing identity or currency provenance

* Related IDs: existing grant compatibility; C4; GBP requirement; P01-T01/T02.
* Evidence: src/core/src/zava_forward/core/grants.py:44-59 persists pending source, amount, email/name and timestamp, but no code/OID or currency. Supplied research C4 reproduces USD input being silently ignored. The plan preserves old histories and optional amounts, but does not state how an old pending proposal becomes a newly enriched approved event.
* Concern: The new approval writer could silently stamp GBP/current metadata onto an old pending amount whose original currency and authority are not evidenced. Alternatively, requiring new fields could unexpectedly make all existing pending records unusable without a documented recovery path.
* Impact: New history can appear verified despite missing original provenance, or legacy records can dead-end. Legacy email fallback by itself resolves only identity, not currency/source classification.
* Smallest useful change: State a narrow legacy-pending policy: use #94 registered-email fallback for unresolved preparer identity and refuse if unknown; preserve old completed histories unchanged; require withdrawal/re-proposal or explicit re-attestation for missing mandatory new proposal evidence. Do not manufacture GBP verification for a previously currency-unknown amount.
* Action owner: Planning parent; grant implementation and regression owners.
* Exact resolving evidence: A fixture with the actual old pending shape and another with an unresolved preparer demonstrates the documented behavior. Known legacy identity is resolved or safely re-proposed; unknown identity refuses. Missing currency provenance cannot produce a newly attested GBP event by default. Withdrawal/re-proposal succeeds for designated independent people, with no history rewrite or opportunity amount carry-forward.
* Decision route: Directly applicable planner correction; no migration, private data or real delegation investigation is needed.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Assign path-specific rollback, alias and fixture tests rather than relying on inherited finance coverage

* Related IDs: preserve #94; P01-T01/T02/T03; acceptance criteria 2/3.
* Evidence: src/core/tests/test_finance_match_controls.py:26-50 creates finance fixtures; JsonFinanceChecks and SqlFinanceChecks contain substantive finance-only tests; MssqlFinanceChecks inherits SqlFinanceChecks, not merely setup. src/core/tests/test_finance_signoffs.py shares module-level STAFF/U. src/api/tests/test_finance_match_api.py also imports STAFF. Existing #94 fault tests specifically exercise finance_budget_approve and finance subtrees. The plan correctly warns against duplicate inheritance but does not allocate its new failure scenarios or isolate changed designation fixtures from these shared imports.
* Concern: Reusing the concrete test classes can rediscover finance tests while counting them as grant parity. Adding authority to shared STAFF can make formerly unauthorized actors globally designated or contaminate unrelated tests. A shared rollback helper passing #94 does not prove that each new caller enters it before mutating a new grant or funding state.
* Impact: The tests can stay green while grant_open leaks a partially opened record, funding confirmation leaves funding_ok true after failure, a registered alias self-approves, or failed SQL success audit flushes on lock exit.
* Smallest useful change: In P01-T01 allocate named semantic cases to the two new modules and each backend; use a setup-only helper/non-discovered mixin or composition, not a concrete finance TestCase. Deep-copy and add designations only to task-owned fixtures. Keep #94 finance assertions and action semantics unchanged. Require representative boundary failures on grant_open/grant_approve and funding approve/submit/confirm, not only finance_action.
* Action owner: P01-T01 test owner; P01-T02 shared-boundary owner; P01-T03 validation owner.
* Exact resolving evidence: Test inventory maps collected grant/application cases to JSON, SQLite and opt-in actual MSSQL executions with skips disclosed. Cases include registered same-code and same-OID aliases with distinct emails, known/unknown legacy preparer fallback, distinct same-role success, audit/save faults, early/persistent recovery-read failure with a prior legitimate SQL audit prefix, and rowversion conflict. Assertions compare in-memory/reopened grants, funding/funding_ok and provider finance, preserved audit/hash chain and original exception, cleared transient validation state, and a subsequent healthy retry with exactly one success event. New tests fail against the unfixed baseline for the intended reason; unchanged #94 suites still pass independently.
* Decision route: Directly applicable planner correction. Parameterized semantic cases can honor the planned test budget; do not substitute inherited finance counts for required grant/application evidence.

## Strengths and Residual Risk

* Existing grant records and second approval are real, not merely documentation claims. Their specific input-role and email-only weaknesses are correctly identified.
* Existing separate application and grant records should be retained. No full replacement ledger, payment executor, pack exporter or regulatory research is justified.
* Captured email/code/OID independence with fail-closed legacy fallback is an appropriate reuse of #94. Different people with the same permitted role should remain valid.
* Reusing the existing finance operation and SqlStore.save hook is preferable to parallel recovery/transaction code. Preserve the provenance, bulk, stock, safety and resident validation hooks.
* Exercise designation establishes synthetic mechanics only. Source references remain supplied rather than externally verified; real financial authority and human acceptance remain unproven.
* JSON rollback can preserve caught-error behavior but does not establish cross-file abrupt-crash atomicity; the existing core README already discloses this limitation. No new distributed/crash-atomic storage project is requested.

## Questions or Blocking Evidence Gaps

* No user decision is required for these findings. The planning parent can define the minimal synthetic contract and apply compatible revisions directly.
* Real delegation evidence remains intentionally unavailable and out of scope. This is not a blocker to exercise-only engineering and must not be claimed as delivered.

## Limitations

* This was one static, bounded plan critique. No source implementation, tests, containers, API server, browser, Azure/model call or financial action was executed.
* Research probe results and remote issue/PR retrievals were assessed as supplied evidence, not independently rerun. Read-only git inspection confirmed the base; source reads verified the cited runtime and test mechanisms.
* Frontend code was read only to test the existing no-web-change/no-award-promotion claim. This is not a fresh web-guidelines, accessibility or browser-conformance review.
* Only this critique artifact was written. Parent plan/details/research/state and all source files remain untouched.

## Recommended Next Action

* Highest-impact finding: PC-002, because an underspecified designation can authorize the wrong financial transition even after replacing role-only checks.
* Action owner: Automatic planning parent.
* Smallest next action: Define the transition/scope/temporal designation contract in P01-T02 and map its negative tests in P01-T01, then reconcile PC-001 and the remaining compatible findings in the same revision.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/grant-lifecycle-controls-95-plan.md](.copilot-tracking/plans/2026-10-17/grant-lifecycle-controls-95-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-17/grant-lifecycle-controls-95-phase-details.md](.copilot-tracking/details/2026-10-17/grant-lifecycle-controls-95-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-17/grant-lifecycle-controls-95-research.md](.copilot-tracking/research/2026-10-17/grant-lifecycle-controls-95-research.md) | Supplied bounded research evidence |
| [.copilot-tracking/reviews/plans/2026-10-17/grant-lifecycle-controls-95-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/grant-lifecycle-controls-95-plan-critique.md) | Complete finding set: four High, two Medium |

## Next Steps

The active automatic planning parent applies compatible PC-001 through PC-006 dispositions directly and finalizes the plan without another critique. Implementation and the separately authorized independent RPI Review remain later parent-owned stages. No user action is required. This critique task stops here.
