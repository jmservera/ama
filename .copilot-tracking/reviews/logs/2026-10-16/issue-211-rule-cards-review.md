---
title: Issue 211 rule cards implementation review
description: One bounded post-implementation RPI review
ms.date: 2026-10-16
---

## Opening Review State

* Interpreted review goal: compare the implemented local labelled exercise rule-card lifecycle, law ingestion transactions and authenticated HTTP identity authority against the finalized plan, critique and validation evidence.
* Review scope: issue #211, twelve changed tracked files and the five supplied canonical evidence artifacts.
* Evidence readiness: supplied artifacts exist; detailed source and evidence comparison is beginning.
* Acceptance basis: finalized plan lifecycle criteria, recorded critique dispositions, local exercise boundary and supplied validation record; no real legal approval or live Azure acceptance inferred.
* First comparison boundary: reconcile plan and changes before tracing rule cards, law transactions and HTTP identity.
* Active read-only boundaries: only this review record may be written; no source, plan, changes, state, private-data, commit or remote writes; no delegation or second Review.
* Initial blockers: none established.

## Execution Status

* Execution status: Complete
* Review execution evidence: exactly one Review completed on 2026-10-16. Inspected the five canonical artifacts, all twelve tracked-file diffs, relevant complete source paths, tests, component documentation, ADR 0006 and issue #211 body/comments. Performed one bounded in-memory compatibility investigation and diff checks; did not rerun full suites.
* Outcome: Conformant for the bounded local labelled exercise slice. Operational acceptance remains residual work, not an inferred delivery.

## Scope and Evidence

* Task ID: #211 / issue-211-rule-cards.
* Review date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/issue-211-rule-cards-plan.md.
* Phase details: .copilot-tracking/details/2026-10-16/issue-211-rule-cards-phase-details.md.
* Plan critique: .copilot-tracking/plans/2026-10-16/issue-211-rule-cards-critique.md.
* Changes: .copilot-tracking/changes/2026-10-16/issue-211-rule-cards-changes.md.
* Research: .copilot-tracking/research/2026-10-16/issue-211-rule-cards-research.md.
* Branch: feat/src-rule-cards-211. Existing dirty source/docs and untracked RPI evidence were preserved. No source, plan, changes, state, commit or remote write was performed by Review.
* Actual changed-file boundary: docs/reference/README.md; docs/reference/log.md; src/core/README.md; src/core/src/zava_forward/core/rulecards.py; src/core/src/zava_forward/core/lawstore.py; src/core/tests/test_rulecards.py; src/api/README.md; src/api/src/zava_forward/api/auth.py; src/api/src/zava_forward/api/server.py; src/api/tests/test_auth.py; src/api/tests/test_lawstore.py; src/api/tests/test_role_endpoint_inventory.py.
* Additional context: docs/case_study_48_original.md, relevant opening/exercise context in docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md, docs/adrs/0006-src-layout-and-cutover.md, src/core/src/zava_forward/core/mssqlstore.py and component pyproject.toml exemptions. Context is not evidence of legal approval.
* Excluded: properwarm.json, .env, .vscode, private inputs, security-vulnerability audit, live Azure/SQL/ingress tests, real legal approval, deployment, UI and rule-engine implementation. No delegation.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Adapter reuse, portable append-only tables, serialized writes and rollback | Reconciled | Complete mutations take the adapter RLock and database transaction before version/state reads; no second store implementation or workload import into core. |
| P01-T02 | Draft validation, source reviews and unassigned exercise seeds | Reconciled | Source versions/provisions/reviews share the outer transaction; card history is untouched. Immutable orphan blobs and separately committed derived index are explicitly documented. |
| P02-T01 | Dedicated capabilities and canonical provisioned actor | Reconciled | Unique object binding is distinguished from fallback login; reserved rule claims cannot map into workbench roles. |
| P02-T02 | Staff reads, draft and owner transition routes | Reconciled | HTTP actor/date/exercise values are server-derived; state and named-owner checks remain in the core lifecycle. |
| P03-T01 | Existing tests extended, no extra test file | Reconciled | Positive/negative HTTP lifecycle, auth ambiguity, rollback, concurrency, index retry and adapter contract coverage are present. |
| P03-T02 | Full suites, tools, running app and related docs | Reconciled | Recorded full-suite results precede bounded final refinements; later targeted/tooling results cover them. Counts and platform skips are explicit. |
| P03-T03 | Review and publication pending | Reconciled | Review is now complete in this record only. Commit/push/PR remain the parent's authorized publication work, not falsely completed implementation markers. |
| Follow-Up Items | Human approval, tenant roles, platform verification, UI/engine | Reconciled | Explicit non-goals/open operational work, mirrored in changes and READMEs; routed below without expanding active scope. |

The plan's generic implementation-ready status and unchecked P03-T03 do not invalidate the current review boundary: checked P01/P02 and P03-T01/T02 plus the changes handoff consistently identify completed implementation/local validation and pending Review/publication. Publication acceptance criterion 5 is not yet satisfied and is not claimed satisfied here.

## Completed Work Assessment

### Six issue lifecycle criteria

| Issue criterion | Source and test evidence | Local assessment |
| --- | --- | --- |
| Only a card approved by its named owner is active | RuleCardStore._owner_only, approve, activate and is_active; test_only_owner_approved_card_is_active; RuleHttpTests positive lifecycle and premature activation denial | Conformant. Activation requires approved state and the named owner; date eligibility additionally gates is_active. Local approvals remain simulated. |
| An author cannot approve their own card, with separate roles | AUTHOR/OWNER core checks; TrustedProxyProvider.authenticate; HTTP capability gate; test_author_cannot_approve_own_card; test_dual_roles_do_not_allow_self_approval | Conformant. Canonical provisioned email is the HTTP author/actor; even a dual-capability principal cannot self-approve. Workbench roles alone are insufficient. |
| Versions, approver, approval/effective dates and prior versions retained | Immutable version rows, append-only events/triggers, history; test_versions_preserved_and_append_only; rollback/reopen tests; actual HEAD-schema compatibility check below | Conformant. New drafts append versions, approvals append events and supersession appends retirement rather than rewriting prior evidence. |
| Authorized owner can hold | hold/release and is_active; test_hold_by_owner_only_and_stops_firing; HTTP positive lifecycle and missing-reason/wrong-owner checks | Conformant. Hold requires active state, named owner and reason; held versions are ineligible. |
| Two labelled exercise seed fixtures | SEED_CARDS, seed, EXERCISE_LABEL; test_seed_cards_are_labelled_exercise_drafts; running HTTP collection assertions | Conformant. Two idempotent unassigned drafts exist, no automatic approval; all new versions stay exercise-only and any approval remains simulated. |
| Source change never overwrites approved cards | LawStore._seed joins rules._source_changed; source-change immutability and review/provision failure tests | Conformant. Later source versions append reviews without changing card contents/events; first ingestion and unchanged retries add no review. |

### Persistence and transaction boundary

* RuleCardStore.transaction and LawStore.transaction hold the same adapter RLock; SQLite BEGIN IMMEDIATE and the existing SQL Server application-lock adapter start before state/version allocation. Rule reads use the same reentrant lock. No nested committing rule mutation is called from source ingestion: _source_changed joins the law transaction.
* Explicit MAX(id)/MAX(version) allocation occurs under the writer transaction. Draft/event writes, activation supersession and assessment holds roll back together on failure. Driver-specific integrity errors are translated without hard-coding sqlite3 for SQL adapters.
* Source ingestion commits source/provision/review rows as one unit. Derived reg_index rebuild owns a subsequent transaction; failure rolls that index transaction back, retains committed source/review evidence and permits unchanged retry. Immutable snapshot blobs are outside SQL rollback and may remain orphaned, as explicitly planned.
* src/core/tests/test_rulecards.py covers shared/independent writer serialization, injected supersession failure, invalid input atomicity, driver integrity translation and recovery. src/api/tests/test_lawstore.py covers changed-source preservation, failed review/provision insertion and index failure/retry. SQL Server tests remain opt-in; contract tests do not substitute for live driver acceptance.

### HTTP identity authority

* TrustedProxyProvider preserves existing workbench-role selection but excludes the two reserved rule claims from that mapping. Capabilities are freshly derived only when exactly one oid matches exactly one provisioned staff identity. Unknown/missing/multiple oid and duplicate provisioned bindings cannot acquire capabilities through email fallback.
* _rulecards requires staff law access, trusted-proxy provider and the separate action capability. Draft owner resolves to provisioned staff; author and transition actor use canonical staff email. Only card fields or transition note are accepted; caller actor/role/author/event-date/exercise overrides are rejected.
* Existing authentication and CSRF precede rule POST dispatch. Password sessions and staff-file capability injection do not grant rule writes; contractors and unknown/agent identities are denied. Dedicated capabilities alone do not supply a staff workbench role.
* Tests exercise the actual loopback handler and principal parser, not token-signature verification. This boundary is accurately disclosed in src/api/README.md and the changes record. No live tenant role definition, assignment or ingress result is inferred.

### Documentation and placement

* All feature code stays in migrated src/core and src/api. The changed core modules import core/standard-library facilities only; no workload imports were added.
* Component READMEs explain the API, transaction semantics, preserved legacy identity strings and simulated approval boundary. docs/reference/README.md routes to those existing documents and docs/reference/log.md appends rather than rewrites history. The original case study and owner memory remain unchanged.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation and readiness | Assessment |
| --- | --- | --- | --- | --- |
| P01 transaction design | Shared adapter RLock, outer source transaction and non-committing review helper; explicit index/blob failure semantics | PC-001, accepted in finalized plan/details | Source implementation, tests, changes and core README agree | Preserves confirmed atomicity intent; no unresolved material decision. |
| P02 identity binding | Capabilities only for unique provisioned oid, not fallback or staff-file authority | PC-002, accepted | Plan/details, auth implementation and deny tests agree | Preserves separate trusted-principal capabilities; does not imply deployment assignments. |
| P01/P03 compatibility | Existing schema retained, initialization/reopen and portable SQL contracts tested; SQL cleanup includes rule tables | PC-003, accepted | Actual old HEAD-schema check supplements the committed reopen test | Compatible retained rows verified locally; live SQL remains residual. |
| P03 validation tooling | Preserve the parent's explicit tooling choice, reject PC-004's contrary planning assumption | Recorded parent disposition and supplied user direction | Plan/details/changes consistently disclose historical commands | No source-acceptance defect follows from this rejected critique item; this Review needed no scratch directory or package/tool installation. |
| P03 delivery gate | Single Review routes findings later; material findings require blocked/draft PR, not acceptance | PC-005 partially accepted under the one-pass protocol | Plan/details/changes preserve one Review and distinguish residuals from defects | No second Review or implementation restart is requested here. |
| Final bounded refinements | Dialect attribute, SQL field limits, atomic derived-index retry and canonical/reserved IDs | CLI module identity, portable column/route constraints and injected partial index failure; rationale recorded in changes | Existing P01/P02 scope and later targeted/tooling evidence cover them | Ordinary implementation details, not a material scope/autonomy change requiring another planning decision or critique. |
| Exercise display label | Explain that any approval remains simulated rather than claiming no named owner ever acted | Actual diff and legacy comparison | Consistent with exercise-only requirement and docs | Derived presentation text changed, not stored historical approval/version evidence. |

## Critique and Material Revision Assessment

* PC-001: addressed by shared lock/transaction ownership, non-committing review helper, source/provision/review rollback tests, supersession rollback, writer serialization and separate derived-index retry semantics.
* PC-002: addressed by unique oid binding, reserved-claim exclusion, canonical staff actor and fallback/ambiguous/contractor/password/dual-role deny coverage. Signature validation and real tenant assignments remain explicitly external.
* PC-003: schema compatibility and SQL cleanup are addressed. The committed test named persisted legacy history constructs its initial store with current code, so by itself it proves reopen, not actual old-code initialization. The bounded Review check constructed data with pre-change HEAD code and verified unchanged stored rows, histories and reviews under the new adapter. No material upgrade evidence gap remains for this local schema.
* PC-004: rejected by the finalized parent disposition. It is not reinstated as a finding or used to invalidate earlier supplied evidence.
* PC-005: material-defect delivery gate retained, but its proposed immediate implementation return is rejected by the explicit one-pass direction. Review routes once, without starting corrections or another assessment.
* Material revision readiness: no significant unaccepted decision or scope divergence found. Accepted critique corrections appear in finalized plan/details before the supplied implementation handoff; later changes are bounded reliability refinements. Available evidence gives no indication dependent implementation resumed across an unresolved material decision.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Actual Entra capability definitions/assignments | Local parser/handler implementation is not tenant provisioning | Identity/deployment administrator | Open, RV-001, distinct deployment follow-up. |
| Live SQL Server/Azure/hosted ingress verification | Local-only validation and opt-in skips cannot establish deployed acceptance | Deployment/platform owner | Open, RV-002, distinct platform acceptance follow-up. |
| Human card and current-source approval | Engineering tests cannot authorize legal/operational interpretation | Named human Legal/Compliance/DPO owners | Open, RV-003, distinct human approval follow-up. |
| Rule-card UI and deterministic engine | Explicit non-goals of this store/API slice | Product/backlog owner | Open, RV-004, separate implementation/backlog work. |

These items are mirrored in changes and component documentation. They are not defects, new active P01-P03 tasks or evidence that issue #211 should close.

## Findings

No implementation defect, unaccepted decision gap or material local evidence gap was established. The complete substantive finding set is the following acknowledged residual work; severity describes its effect on this bounded slice, not its importance before operational use.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Actual tenant capability provisioning remains a deployment prerequisite

* Classification: Non-blocking residual work for this local slice; operational prerequisite.
* Related scope: P02-T01; plan Follow-Up Items.
* Evidence: src/api/src/zava_forward/api/auth.py, src/api/README.md and changes section Validation Boundaries and Remaining Acceptance. Separate trusted claims are required; current infrastructure role definitions/assignments are explicitly not delivered.
* Impact: Local principal fixtures prove code-level separation only; deployed users cannot be assumed able or authorized to exercise the dedicated rule capabilities.
* Destination: Distinct identity/deployment follow-up, owned by the tenant administrator, not active rpi-implement scope.
* Smallest useful next action: Define and explicitly assign the two dedicated capabilities alongside an eligible workbench role, then record deployment identity acceptance without conferring authority through fallback.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Live platform and authenticated-ingress acceptance is unperformed

* Classification: Non-blocking residual work for this local slice; release prerequisite.
* Related scope: P01/P02; P03-T02 and plan Follow-Up Items.
* Evidence: src/api/tests/test_lawstore.py opt-in SQL Server cases, src/core/tests/test_rulecards.py adapter contract, src/api/tests/test_auth.py synthetic principal/loopback harness and recorded platform skips.
* Impact: SQL Server execution, Azure Blob immutability and ingress isolation/signature validation cannot be claimed from SQLite, fake containers, portable DDL inspection or injected synthetic headers.
* Destination: Distinct platform acceptance follow-up, owned by deployment/platform maintainers.
* Smallest useful next action: Execute existing opt-in SQL/lifecycle checks in the intended environment and record actual Azure/ingress verification before any operational acceptance.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Specific cards still require real human review and approval

* Classification: Non-blocking residual work for this labelled exercise; mandatory before operational interpretation.
* Related scope: All six issue criteria as locally exercised; plan Follow-Up Items.
* Evidence: SEED_CARDS and EXERCISE_LABEL in src/core/src/zava_forward/core/rulecards.py, simulated approval events, src/core/README.md, src/api/README.md and changes remaining-acceptance section.
* Impact: Neither owner nomination, provisioned email, an app-role claim nor a successful synthetic approval establishes legal correctness or real delegation. The two seed fixtures intentionally stay unapproved/unassigned at startup.
* Destination: Distinct human approval follow-up, owned by the named Legal/Compliance/DPO reviewers.
* Smallest useful next action: Review current authoritative sources, citations, clocks and specific cards under explicit human decision rights; preserve exercise labels and do not activate operational rules on this Review's authority.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: UI and deterministic rule-engine integration remain separate work

* Classification: Non-blocking residual work; explicitly outside this slice.
* Related scope: Plan Scope and Non-Goals / Follow-Up Items.
* Evidence: Store/API-only changed-file boundary, component README limits and changes remaining-acceptance section.
* Impact: API lifecycle and is_active eligibility are not an end-user rule-card workbench or a rule execution engine.
* Destination: Distinct product/backlog follow-up, owned by the product and relevant implementation maintainers.
* Smallest useful next action: Keep those deliverables in separately scoped backlog items with their own acceptance; do not add them to this completed local slice or represent them as delivered.

## Defects

* None established within the supplied boundary.
* Severity summary: 0 Critical, 0 High, 0 Medium, 4 Low residual findings; no blocking implementation findings.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct tenant-capability follow-up | Tenant/identity administrator | Intentionally undelivered provisioning, not a code defect. |
| RV-002 | Distinct deployed-platform acceptance follow-up | Deployment/platform owner | Live verification remains outside recorded local evidence. |
| RV-003 | Distinct human card-approval follow-up | Named Legal/Compliance/DPO owners | Human authority cannot be manufactured by engineering tests. |
| RV-004 | Distinct UI/engine backlog work | Product and implementation owners | Explicit non-goals, not missing active-plan implementation. |

Later implementation of any routed work does not require another Review of this task. No rpi-implement, rpi-plan or rpi-research handoff is needed for the accepted local slice.

## Residual Work

* RV-001 through RV-004 remain open exactly as scoped above.
* Issue dependencies and the whole operational capability are not declared complete by this local Review. Keep Refs #211, not Closes #211.

## Blockers and Remaining Work

* Review blockers: none.
* Local engineering acceptance blockers: none established.
* Remaining active work: parent completes the publication portion of P03-T03, including authenticated privacy-safe commit identity, scoped commit with required trailer, push of the same topic and PR to main. No merge or issue closure is authorized by this Review.
* Delivery disposition: eligible for an honestly scoped PR, explicitly listing the operational residuals. No defect-driven draft/block is required by the findings here. If a separate material blocker is identified by the parent, preserve the one-pass rule and publish only draft/blocked rather than claiming acceptance.

## Validation Evidence

| Command or evidence | Scope | Status | Summary and provenance |
| --- | --- | --- | --- |
| Core unittest discovery | Full core suite | Passed, implementation-reported | Changes record: 398 tests, no skips after editable metadata restoration; earlier metadata errors and sensor ResourceWarnings disclosed. Not rerun by Review. |
| API unittest discovery | Full API suite | Passed, implementation-reported | Changes record: 532 tests, 103 skipped after metadata restoration. Skips prevent live-platform/browser acceptance claims. Not rerun by Review. |
| Core rulecards selection | Final bounded refinements | Passed, implementation-reported | 17 tests; invalid values, rollback, concurrency, persistence and adapter contract. |
| API RuleHttpTests plus lawstore selection | Final index/route refinements | Passed, implementation-reported | 40 tests, 14 skips. Earlier broader auth/law/inventory selection: 84 tests, 14 skips. |
| RuleHttpTests loopback server | Actual local HTTP lifecycle | Passed, implementation-reported | 6 tests, health/app responsiveness, lifecycle/denials, retained history and persistence reopen; exact server shutdown/join in harness. Synthetic claims, not ingress signature verification. |
| Per-project mypy, ruff check and ruff format --check | Touched core/API projects | Passed, implementation-reported | Existing migrated-module type/lint/format exemptions inspected and disclosed; command success does not prove strict checking of exempted legacy files. |
| In-memory actual pre-change schema investigation | Legacy compatibility | Passed after comparison correction, Review-observed | Executed pre-change HEAD rulecards source via git show against in-memory SQLite, seeded synthetic rows/approval/review, initialized the current adapter twice, compared all four persisted rule tables and history/reviews, added v2 and confirmed append-only rejection. Initial strict history comparison failed solely because the derived exercise label intentionally changed; stored evidence and all other history fields were unchanged. No disk fixture or package installation. |
| git diff --check | Tracked diff | Passed, Review-observed | No whitespace errors. Twelve-file diff count reconciles with the supplied boundary. |
| Narrow core workload-import search | Changed core modules | Passed, Review-observed | Tool-based search found no zava_forward workload imports. A shell rg attempt was unavailable; the available search tool completed the check. Not a source/test failure. |
| Live SQL/Azure/hosted-ingress and real human approval | Operational acceptance | Skipped / unavailable | Explicitly outside this local exercise; routed RV-001 through RV-003. No operational approval inferred. |

The bounded compatibility check was necessary because the committed legacy-named test starts with current code. This Review did not repeat expensive full suites, mutate tests or create a second review pass. Full-suite results are historical implementation evidence; final refinements have narrower later evidence and are not represented as having preceded those full runs.

## Outcome

* Outcome: Conformant.
* Acceptance boundary: local labelled exercise store/API implementation only.
* Rationale: all six lifecycle criteria are locally represented and tested; law source/review mutations and supersession use the finalized atomic transaction design; HTTP authority derives from distinct trusted, uniquely provisioned principal capabilities rather than request strings, fallback or password sessions. Retained legacy rows were additionally verified. No implementation defect or material unaccepted divergence was established.
* Limit: this is not acceptance of legal correctness, real card approval, Entra deployment, live SQL/Azure/ingress, UI or rule-engine completion. Publication remains pending, so the entire plan and issue are not declared complete.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No defect established; do not restart implementation in this one-pass loop. |
| Decision gap or invalid assumption | None | Finalized critique dispositions preserve confirmed direction. |
| Material evidence gap | None for local slice | The bounded legacy check closes the only additional local compatibility uncertainty. |
| Non-blocking residual work | RV-001 through RV-004 distinct follow-ups | Identity administrator, platform owner, human card reviewers and product/backlog owner respectively. |

* Execution status: Complete.
* Outcome: Conformant for the local exercise slice.
* Validation coverage: inspected source/tests/docs and supplied full/targeted/tooling results; one bounded in-memory compatibility investigation and diff checks observed by Review.
* Blockers: none for this Review/local slice; operational prerequisites remain open.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-16/issue-211-rule-cards-research.md](.copilot-tracking/research/2026-10-16/issue-211-rule-cards-research.md) | Research and evidence boundary |
| [.copilot-tracking/plans/2026-10-16/issue-211-rule-cards-plan.md](.copilot-tracking/plans/2026-10-16/issue-211-rule-cards-plan.md) | Finalized plan and dispositions |
| [.copilot-tracking/details/2026-10-16/issue-211-rule-cards-phase-details.md](.copilot-tracking/details/2026-10-16/issue-211-rule-cards-phase-details.md) | Transaction, authority and one-pass task details |
| [.copilot-tracking/plans/2026-10-16/issue-211-rule-cards-critique.md](.copilot-tracking/plans/2026-10-16/issue-211-rule-cards-critique.md) | Single critique compared with final dispositions |
| [.copilot-tracking/changes/2026-10-16/issue-211-rule-cards-changes.md](.copilot-tracking/changes/2026-10-16/issue-211-rule-cards-changes.md) | Implementation and validation evidence |
| [.copilot-tracking/reviews/logs/2026-10-16/issue-211-rule-cards-review.md](.copilot-tracking/reviews/logs/2026-10-16/issue-211-rule-cards-review.md) | This one complete Review |

## Next Steps

The active parent owns the remaining authorized P03-T03 commit/push/PR publication to main on the same topic, with Refs #211 and the four residual routes disclosed. Do not close #211, merge, restart implementation or request another Review. No user action or new RPI command is required for this completed Review.
