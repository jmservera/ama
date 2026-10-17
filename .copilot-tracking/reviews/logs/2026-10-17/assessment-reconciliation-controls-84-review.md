<!-- markdownlint-disable-file -->
# Review: Assessment reconciliation controls #84

## Scope and Evidence

* Task ID: 84; slug: assessment-reconciliation-controls-84; date: 2026-10-17.
* Review scope: Exactly one independent full-task post-implementation Review. This is not a generic security, architecture or web-conformance audit.
* Plan: .copilot-tracking/plans/2026-10-17/assessment-reconciliation-controls-84-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/assessment-reconciliation-controls-84-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/assessment-reconciliation-controls-84-changes.md
* Research: .copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md
* Compared the complete current tracked git diff: four core implementation modules, canonical core regression module, HTTP and SQL parity modules, component guides, existing UX synthesis, knowledge index and append-only log.
* Acceptance references: docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-012/FR-013; docs/brds/agentic-retrofit-programme-brd.md FR-037/AC-065 subset and RULE-017. The BRD's full nomination/referral/cohort and competence requirements are not replaced by this engineering subset.
* Context: Original case study, addendum, reference index, owner memory and sector primer. No private support/cohort/map dataset read. No new legal/source-policy authority determination.

## Opening Review State

* Interpreted review goal: Perform the single independent post-implementation Review for task84 against exact criteria, current authority and rollback correctness.
* Review scope: Full supplied task84 boundary, including PC001..003 dispositions and significant implementation concerns.
* Evidence readiness: All five canonical artifacts exist; current branch is feat/assessment-reconciliation-controls-84 with implementation changes present. Evidence assessment is starting; no outcome is assumed.
* Acceptance basis: Both conflicting stock values and query owner; four separate versioned assessment/design/building/coordination signoffs; only affected signoffs stale after design change; multi-factor ranking and Unknown rather than none for missing information; narrow stock.decision_scope with fresh authority at entry and SQL writer transaction, rollback and original-exception preservation.
* First comparison boundary: Canonical plan, details, research, critique and changes against the current complete implementation diff and relevant existing criteria tests.
* Active read-only boundaries: Only this review record may be written. No source, plan, state, docs or other artifact writes; no corrections, agents, repeated review, private/cohort/map reads, AI/provider/cloud calls or new authority policies.
* Initial blockers: None established before comparison. Unresolved exact-criterion, current-authority or rollback defects will block acceptance.

## Execution Status

* Execution status: Complete.
* Review execution evidence: All five supplied canonical artifacts, current implementation/test/documentation diff, relevant existing criterion tests and SQL cleanup seams were compared during this single Review. Two narrowly scoped in-memory fault cases and three fresh-process imports were executed offline. No full-suite rerun, agents, correction or repeated Review.
* Implementation execution versus acceptance: P01/P02 execution is recorded as complete in the supplied evidence, but RV-001 makes the result unacceptable. P03-T01 is this completed Review; P03-T02 publication remains pending and no plan/state markers are edited here.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Fail-before stock regression, strengthened existing criteria tests | Reconciled for sequence, scope and budget | Supplied actual red run: 24 tests, 14 failures, 5 errors before source edits. Eight new core methods total, one HTTP method, one opt-in parity class; no tests removed. Recovery-fault oracle is insufficient for RV-001. |
| P01-T02 | Bounded decision scope, reused actor helper, one SQL save hook | Partially conformant | Entry and transactional fresh authority are present; successful discard handles ordinary failure. Early discard failure still permits success audit or masks original error. |
| P02-T01 | Core/API/browser/SQL Server/static checks | Execution reconciled; acceptance blocked | Named checks and skips are recorded consistently. Passing checks do not cover RV-001's early/persistent recovery faults. |
| P02-T02 | Current guides/synthesis/index and append log | Scope reconciled | Documentation preserves four mechanisms and operational limits; its failed-decision/original-error guarantees are too broad while RV-001 remains. Correct those claims with the implementation if later authorized. |
| P03-T01 | Ready for exactly one Review, blockers cannot be accepted residuals | Reconciled through this record | RV-001 invokes the explicit incomplete-stop disposition; no review loop or correction. |
| P03-T02 | Normal privacy-safe main-targeted Refs #84 PR | Pending, not claimed complete | No publication, issue closure or merge occurs in this Review. Any later visibility PR must be clearly incomplete while the blocker remains. |
| Follow-Up Items | Professional/source-policy/full BRD and JSON limitations | Distinct residuals | Outside immediate engineering acceptance; owners/actions below. None absorbs RV-001. |

## Completed Work Assessment

| Related scope | Files and mechanism | Completion evidence | Assessment |
| --- | --- | --- | --- |
| Criterion 1; P01/P02 | src/core/src/zava_forward/core/store.py stock_reconcile and stock_query_event; src/core/tests/test_stock_reconciliation.py; src/api/tests/test_stock_reconciliation_api.py | Comparison test preserves D/E assertions, source dates/versions/validation, named owner, query versions and reopen history. HTTP test and rendered comparison test assert both values, owner, Unknown authority and case isolation. Actual Chromium pass is supplied implementation evidence. | Preserved. No winning source chosen, stock overwrite or inferred source authority introduced. |
| Criterion 2; P01/P02 | src/core/src/zava_forward/core/signoffs.py and canonical four-signoff test | Exact assessment/design/building/coordination key set, four distinct people, initial version 1, version-2 design reapproval and retained histories. Existing role/self-approval checks remain; selected SQL Server replay includes this method. | Preserved exercise mechanism, not proof of external competence/delegation. |
| Criterion 3; P01/P02 | _tech_design_change and test_four_human_signoffs_and_only_affected_reassessment | Explicit affects=[design, building] stales only those signoffs; assessment and coordination remain byte-for-byte equivalent at the object level. Version-2 history, sibling isolation and SQL reopen equality are asserted. | Preserved. No automatic reapproval or dependency-policy expansion. |
| Criterion 4; P01/P02 | src/core/src/zava_forward/core/stock.py support_status/support_coverage; unchanged ranking.py; canonical truth-table/ranking/SQL upgrade tests | Missing/partial observations produce Unknown; No requires explicit negative observations. Safety and waiting independently rank homes, reason codes expose unknown support, SQL and Python order agree, derived-data upgrade is idempotent. | Preserved BRD AC-065 subset. Boolean nonpositive ranking membership is not an assertion that missing observations mean none. Full referral/cohort acceptance remains outside scope. |
| Current authority; P01-T02 | stock.decision_scope, change_provenance._actor and sqlstore.py save | _actor selects current SQL staff at entry and again after BEGIN IMMEDIATE; verifies registered role, nonblank name and email/code/name/role/OID equality. Context snapshots the request. Three decision entry points use this scope. Canonical stale/deleted/OID/role/name and second-connection pre-save race assertions plus existing-session HTTP denial are present. | Conformant within the participating writer protocol. No new role grants or arbitrary external-write serialization guarantee. |
| Known failed SQL decision; P01-T02 | decision_scope and existing _discard/_finish | Supplied case/audit transactional failures and reopen/no-later-flush checks exercise successful recovery; independent Review probes exercise early failed recovery. | Not conformant: RV-001. This is a known-precommit failure, not a lost commit acknowledgement. |
| Scope containment | Complete git diff | Minimal Store entry changes, one SQL validation call, unchanged role mappings/independence/ranking. No web, architecture, procurement #90, infrastructure/package #381 changes. | Conformant scope; shared Store/SqlStore seams remain the only integration overlap. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Trigger/evidence and decision | Reconciliation and assessment |
| --- | --- | --- | --- |
| P01/P02 and test budget | Lifecycle matrix and selected canonical SQL Server replay incorporated after critique | PC-002/PC-003 compatible direct planner dispositions; no new policy decision | Plan, details and changes agree on eight core additions, one HTTP addition and one parity class. Execution is documented. Recovery-fault correctness remains deficient under RV-001. |
| P01-T02/P02-T01 import correction | Lazy actor-helper imports prevent introduced stock/projection/change_provenance import cycle | First actual fresh-driver import exposed cycle; fresh-process regression added before Review | Directly coupled correction, not a divergent architecture decision. Three independent fresh-process imports also passed during Review. Full-core escalation in Implement was justified by shared-seam/import risk. |
| P02-T01 local SQL readiness | Bounded connection-ready retry after startup login failure | Actual startup timing failure in owned local SQL Server, then successful readiness and eight tests | Recorded attempts are not hidden or counted as passes. No infrastructure edit, image pull or cloud acceptance claim. Container removal is supplied execution evidence, not newly performed by Review. |
| P03-T01 blocker gate | Failed exact criteria/authority/rollback cannot be accepted residuals | PC-001 direct disposition before Implement | Current plan/details explicitly require an incomplete stop. This Review follows it. |
| P01/P02 completion claims | Implementation and descriptive evidence marked complete before Review | Changes ledger records actual commands/counts, limitations and pending P03 | Execution markers are credible, but a green execution history does not establish successful outcome in the presence of RV-001. |

## Critique and Material Revision Assessment

* PC-001 [High]: Planning disposition resolved. Plan P03-T01, phase details and handoff distinguish blockers from accepted residuals. RV-001 must stop successful completion; it cannot be routed as accepted later work.
* PC-002 [Medium]: Lifecycle/error tests and plan commitments were added. Source restores the previous context on covered SQL exits and the tests cover success, entry rejection, body failure and a synthetic BaseException. The recovery-fault test completes discard before raising, so it does not satisfy the substantive original-error/no-success-audit guarantee when recovery itself fails early. Not fully resolved in implementation; linked once to RV-001 rather than duplicated as another finding.
* PC-003 [Medium]: Resolved within the recorded engineering evidence. One MssqlStockDecisions class aliases eight canonical changed-path methods; selected names, real local SQL Server 2022 run, zero skips, independent second-connection authority change, failures/reopen/no-delayed-audit and cleanup are recorded. No generic SQL suite is substituted for these cases. This does not cover RV-001 or establish Azure acceptance.
* Material revision assessment: No significant divergent user-owned decision or invalid architecture/policy assumption was found. Lazy imports and connection readiness are justified implementation-local corrections already reconciled in plan/details/changes. No new planning/critique loop or user authority policy is justified.
* Dependent-work pause assessment: Supplied chronology records critique dispositions before Implement, red evidence before production edits and P01/P02 reconciliation before this Review. No contradictory early-resumption evidence was found. Historical chronology is supplied evidence, not independently reconstructed from unavailable raw session transcripts.

## Plan Follow-Up Assessment

| Distinct follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| FU-001: Professional competence/delegation | Exercise role and identity enforcement cannot certify a person's professional competence or authority | Programme owner with relevant competent professional approves operational delegation/evidence | Remains unproved; separate human operational-acceptance work, not a role-mapping change in #84. |
| FU-002: Source authority/eligibility and deterministic policy approval | Competing assertions and Unknown labels intentionally do not select authoritative truth or approve eligibility/ranking policy | Source/data owner and programme owner approve operational rules with appropriate compliance input | Separate owner-governed policy/acceptance work; no new authority policy authorized here. |
| FU-003: Full BRD AC-065 referral/nomination/cohort | Supplied owner direction assigns nomination/referral/challenge to #130; broader cohort/coverage acceptance is not this subset | #130 owner for assigned routes; programme/data owner for cohort-with/without-flags and coverage evidence | Remains separate, with no full BRD completion claim. |
| FU-004: JSON cross-file crash atomicity | Existing snapshot and ledger are separate files; no backend redesign was approved | Persistence owner assesses a separately scoped backend durability task if required | Existing disclosed limitation, not SQL acceptance evidence and not a substitute for fixing RV-001. |
| FU-005: External staff writes outside shared lock protocol | Transaction recheck/application-lock participation is not universal external-writer serialization | Persistence/IAM owner defines a separately approved integration/operational contract if arbitrary writers are introduced | Disclosed boundary, not newly asserted guarantee or current engineering defect. |
| FU-006: Deployment/model/user/accessibility acceptance | Local synthetic SQL/browser/core tests cannot prove Azure/Entra, actual model, direct user or WCAG acceptance | Deployment owner and product/accessibility owner schedule distinct controlled acceptance work | Not performed or inferred; no external calls or fresh conformance claim in Review. |

Unresolved follow-ups remain outside active P01/P02 implementation and acceptance. RV-001 is not among them.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High / BLOCKER]: Recovery failure leaves pending success audit exposed to outer lock cleanup and can replace the original error

* Related scope: P01-T02, P02-T01, PC-002, known-precommit rollback/audit and original-error requirements.
* Evidence: src/core/src/zava_forward/core/stock.py:32-40 catches a failed _discard, annotates/logs the operation error and rethrows, but leaves the existing _SyncLock exit active. src/core/src/zava_forward/core/sqlstore.py:_discard reads touched cases before clearing pending; _SyncLock.__exit__ unconditionally invokes _finish; _finish independently appends any remaining pending audit.
* Independent bounded reproduction: Two no-filesystem, in-memory SQLite fault probes used the actual SqlStore.technical_action, stock.decision_scope, _discard, _finish and _SyncLock, with a constructed coordinator/design and a known precommit save OSError. On the first recovery case-read failure only, outer cleanup subsequently succeeded: durable design_version remained 1 but audit contained technical_design_change for the failed version-2 action. With persistent recovery case-read failure, outer _finish raised the recovery OSError instead of the original save error and retained one pending success event. Recovery logging and original-error annotation occurred in both cases; neither prevents these outcomes.
* Coverage gap: src/core/tests/test_stock_reconciliation.py:test_sql_recovery_fault_preserves_original_failure calls the real discard successfully before raising its synthetic recovery error, and stages no failed action audit. It cannot expose an early recovery-read failure or the second exception from outer cleanup.
* Impact: This is a reproduced in-scope failed-decision integrity defect, not merely unproved rollback after an unknown commit acknowledgement. A known failed decision can gain a success audit, and a recovery error can mask its original failure. It blocks acceptance and successful-delivery claims.
* Destination: rpi-implement, only on a later explicitly authorized continuation; no correction or second Review is performed here.
* Smallest useful next action: Within the accepted narrow decision scope, prevent failed pending success events from reaching outer cleanup even when reload/discard fails, and preserve the original exception across that cleanup while reporting recovery uncertainty. Extend the canonical regression with failure before discard clears pending and with persistent cleanup failure. Do not broaden generic lock semantics or claim an uncertain case reload succeeded.

## Defects

* RV-001 is the sole substantive implementation finding: High, blocking. Its audit leak and original-error replacement share the same uncontained recovery/outer-cleanup root cause.
* Severity summary: 0 Critical, 1 High, 0 Medium, 0 Low new findings.
* No exact four-criterion regression or fresh-authority defect was otherwise found within the assessed evidence boundary. This does not negate the reproduced failure-integrity blocker.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Later rpi-implement, only if explicitly authorized | Parent records Not accepted/incomplete; later implementer repairs the bounded scope and adds the two early/persistent recovery-fault oracles, including related documentation claims | In-scope rollback/audit/original-error defect; cannot be accepted as residual or successful delivery. |

No second Review is required or authorized by this record. No automatic correction, new task selection or workflow is launched.

## Residual Work

* FU-001 through FU-006 retain separate owner actions above. They are pre-existing or explicitly disclosed evidence/operational boundaries, not accepted substitutes for an unresolved engineering defect.
* Normal main-targeted Refs #84 publication is still pending. Publication is parent-owned, not executed here; while RV-001 is unresolved any visibility PR must state incomplete/Not accepted. No issue closure or merge is authorized.

## Blockers and Remaining Work

* Acceptance blocker: RV-001, known failed-decision success-audit leakage and original-error replacement under failed recovery. Stop successful completion.
* Review progress blockers: None; this one Review is complete.
* Remaining active plan work: P03-T02 publication, subject to the incomplete-stop disposition. Plan/state/changes markers are not modified by Review; the parent owns subsequent lifecycle bookkeeping and publication decisions.
* No new significant decision gap or material research gap prevents this verdict. Existing external approvals remain unproved and separately owned.

## Validation Evidence

Recorded implementation evidence below is supplied by the user and canonical changes record. Those suites were not rerun during Review, and raw session transcripts were not accessed. The reproduced defect does not erase their passing results; it limits their acceptance coverage.

| Command/check | Scope | Status | Evidence and limit |
| --- | --- | --- | --- |
| PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_stock_reconciliation -q, before production edits | Fail-before regressions | Failed as expected, supplied | 24 tests, 14 failures, 5 errors. Red-before-source chronology is supplied evidence. |
| From src/core: ../../.venv/bin/python -m unittest discover -s tests -q | Full core | Passed, supplied | 631 tests; one existing resident-browser opt-in skip. Not rerun. |
| From src/core: PYTHONPATH=tests ../../.venv/bin/python -m unittest test_stock_reconciliation test_finance_signoffs test_sqlstore test_sqlreads -q | Canonical stock/signoff/SQL | Passed, supplied | 88 tests; independent hazard/building command also passed 27. Not rerun. |
| From src/api: PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_stock_reconciliation_api test_ranking_policy test_mssqlstore.SharedSqlIsPortableTests test_role_matrix test_mvp test_workflows -q | Targeted API/ranking/roles/workflows | Passed, supplied | 72 tests; one opt-in stock-browser skip, separately exercised below. Not rerun. |
| ZF_STOCK_BROWSER=1 and canonical test_stock_reconciliation_api.StockApi.test_rendered_comparison_and_case_switch | Actual Chromium stock comparison | Passed, supplied | One actual rendered test; both values/owner/metadata/Unknown/case navigation. Not human or WCAG acceptance. |
| Existing localhost opt-in settings and python -m unittest test_mssqlstore.MssqlStockDecisions -v | Actual SQL Server 2022 changed paths | Passed, supplied | Eight named canonical cases, zero skips. Owned container removed. No container created or SQL Server rerun in Review. |
| Core/API Ruff check, Ruff format --check and mypy | Component static checks | Passed, supplied | Core 57 formatted/110 typed files; API 19 formatted/50 typed files. Not rerun. |
| Relative-link and old knowledge-log prefix check | Four touched guides/index/synthesis and append log | Passed, supplied | 345 local targets exist; prior log prefix byte-identical. No new legal/source evidence introduced. |
| git diff --check | Current tracked diff | Passed in Review | No whitespace errors. |
| PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B with fresh subprocess imports | mssqlstore, ranking, store | Passed in Review | Three fresh processes import successfully; no bytecode/file fixture writes. |
| PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B with actual decision_scope/SqlStore/_SyncLock and in-memory SQLite | Early and persistent discard-read faults after known precommit save failure | Failed acceptance in Review, reproduced | First case: version=1, audit=[technical_design_change], original error preserved. Persistent case: version=1, audit=[], pending=1, original error replaced by recovery error. Both log uncertainty, annotate original and restore context. Exact output below. |
| Full suites, browser, SQL Server, cloud/provider/AI and human/WCAG acceptance in Review | Outside narrowly useful offline checks | Not run | Full-suite repetition prohibited; actual implementation evidence supplied. External calls and private reads prohibited; no new conformance claim. |

### Independent fault-probe observations

The probe built SqlStore via __new__ with only constructed in-memory tables/state, used the real technical design-change entry, decision scope, discard and outer lock cleanup, and injected a known precommit save OSError. A connection wrapper failed the actual recovery case-read once or persistently; no schema/source/test file was changed. It did not instantiate AI, use filesystem fixtures or call a provider.

```json
{"context_restored": true, "durable_audit_actions": ["technical_design_change"], "durable_version": 1, "exception": "Constructed original precommit save failure", "original_annotated": true, "original_exception_preserved": true, "pending_count": 0, "persistent_recovery_fault": false, "recovery_logged": true}
{"context_restored": true, "durable_audit_actions": [], "durable_version": 1, "exception": "Constructed recovery read failure", "original_annotated": true, "original_exception_preserved": false, "pending_count": 1, "persistent_recovery_fault": true, "recovery_logged": true}
```

These are two fault cases within this one Review, not repeated Review passes. No lost-commit-acknowledgement rollback or SQL Server recovery-fault execution is claimed.

## Outcome

* Outcome: Not accepted.
* Rationale: Four original mechanisms and current-authority revalidation are preserved within the engineering boundary, but a reproduced failure-integrity requirement remains broken. A completed implementation/test execution and completed Review do not make this a successful delivery.
* PC-001 gate applies: RV-001 is a blocker, not an accepted residual. No source correction or acceptance-ready publication is authorized by this Review.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement, only with explicit authorization | RV-001; parent stops incomplete and records the blocker. |
| Decision gap or invalid assumption | None newly identified | Existing professional/source/ranking authority remains unapproved, not silently decided. |
| Material evidence gap | None blocking this engineering verdict beyond the reproduced defect | External acceptance work stays separate; no rpi-research launch. |
| Non-blocking residual work | Distinct FU-001 through FU-006 | Relevant professional/programme/data/persistence/IAM/deployment/product/accessibility owners as listed. |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: Supplied full core, targeted API, actual Chromium, actual local SQL Server and static/docs checks; independent offline fresh imports and two recovery-fault reproductions.
* Blockers: One High in-scope implementation defect, RV-001.
* Write boundary: Only this canonical review record is written; all implementation, documentation, plans, details, research, critique, changes and lifecycle state remain untouched by Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md](.copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md) | Research evidence and accepted narrow root-fix scope |
| [.copilot-tracking/plans/2026-10-17/assessment-reconciliation-controls-84-plan.md](.copilot-tracking/plans/2026-10-17/assessment-reconciliation-controls-84-plan.md) | Current plan, blocker gate and distinct follow-ups |
| [.copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md](.copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md) | Phase execution commitments and pending publication |
| [.copilot-tracking/reviews/plans/2026-10-17/assessment-reconciliation-controls-84-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/assessment-reconciliation-controls-84-plan-critique.md) | Single critique PC-001..003 and resolving oracles |
| [.copilot-tracking/changes/2026-10-17/assessment-reconciliation-controls-84-changes.md](.copilot-tracking/changes/2026-10-17/assessment-reconciliation-controls-84-changes.md) | Implementation chronology, supplied actual validation and limitations |
| [.copilot-tracking/reviews/logs/2026-10-17/assessment-reconciliation-controls-84-review.md](.copilot-tracking/reviews/logs/2026-10-17/assessment-reconciliation-controls-84-review.md) | This single independent Review and blocking reproduction |

## Next Steps

Return Complete / Not accepted to the parent and stop. Parent must preserve the incomplete-stop outcome and route RV-001 to a later explicitly authorized rpi-implement continuation; this invocation performs no correction, repeated Review, publication, issue closure or merge. Any visibility-only Refs #84 PR remains parent-owned and must be labelled incomplete while the blocker is unresolved. Keep genuine residuals with their distinct owners.

## Correction ONE Disposition (2026-10-17)

The coordinator explicitly authorized same-PR RV-001 implementation after this
Review. All original bytes above, including the negative verdict and probes,
remain historical; they have not been rewritten as a pass.

Correction ONE disarms canonical pending writes/audits before fallible reload,
restores known case/recommendation/shared-document snapshots, invalidates sync
for retry and preserves stock/technical transaction refusal errors through
owning decision-scope cleanup. Six real early/persistent SELECT subcases and
two real GateError/ConflictError refusal subcases failed before their source
corrections and pass after them. Ten actual local SQL Server tests pass.

Bounded independent verification: **RV-001 Closed** for the fingerprinted
correction, with no remaining scoped blocker. See
[Correction ONE verification](assessment-reconciliation-controls-84-correction-one-verification.md)
for exact source SHA256 binding, 91 independent focused passes, two constructed
persistent-recovery snapshot probes, corrected no-op-save oracle and limits.
Final source fingerprints matched this record without further source edits.
This is not a repeated full RPI or second full-task Review, lost-commit-ack
guarantee, source-policy/ranking/professional approval or operational acceptance.
Normal same-branch publication remains parent-owned; no merge or issue closure.
