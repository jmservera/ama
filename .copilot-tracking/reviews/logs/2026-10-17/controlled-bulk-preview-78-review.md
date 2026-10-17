<!-- markdownlint-disable-file -->
# Review: controlled-bulk-preview-78

## Scope and Evidence

* Task ID: 78; date: 2026-10-17.
* Scope: complete implemented P01/P02, issue's three criteria and declared
  partial broader FR-005 acceptance, not operational approval.
* Plan: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md
* Details: .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/controlled-bulk-preview-78-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/controlled-bulk-preview-78-changes.md
* Research: .copilot-tracking/research/2026-10-17/controlled-bulk-preview-78-research.md

## Opening Review State

Goal: compare implementation, exact preview/authority/audit/transaction evidence,
plan completion and all six critique dispositions once. Evidence ready: current
plan markers and details complete, changes include fail-before and focused
passing results, explicit live-server skips and older provenance boundaries.
First comparison: complete new core/API module/tests and surgical integration
diff, then documentation/criterion claims. Review writes only this record;
no source changes or second Review. No initial blocker. Direct bounded review;
no independent uncertainty warrants further delegation.

## Execution Status

Complete. One post-implementation Review executed directly on 2026-10-17.
No source changes made during Review; no second Review.

## Plan-to-Change Reconciliation

| Current scope | Changes evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Core module, Store wrappers, checked SQL document/validator, history projection and 32 core tests | Implemented, with RV-001 defect in tampered blocked-state handling |
| P02-T01 | Two authenticated routes, malformed/role refusal audit, explicit 503, six HTTP tests and two inventory entries | Implemented; normal HTTP cannot mutate retained preview status |
| P02-T02 | Focused controls/SQL/API results, existing component tooling and updated guides/synthesis/index/log | Reconciled; live-server and legacy provenance limitations explicit |
| Follow-Up Items | Live SQL, UI and human acceptance excluded from bounded backend slice | Remain separate follow-ups, not passed active work |

## Completed Work Assessment

Source comparison covered the complete new bulk_edits.py, both new test modules,
Store/SqlStore/projection/server/inventory integration diff, type overrides,
component guides and KB additions. No framework or web-asset edit; no forms
module/route change and no inferred #377 dependency.

Normal issuance/apply is server-owned, creator-bound and copied before return.
Strict request shape and three explicit field mappings prevent arbitrary JSON
or controlled transitions. SQL rechecks fresh staff/OID, whole-case digest and
rowversion plus governance snapshot after acquiring the writer transaction.
Success history, case writes, durable result and audit share that transaction.
Rejection recovery reloads cases/shared docs and clears staged success audit.
No-op records retain no fabricated case edit history. Existing note redaction
explicitly hides nested source/reason/change text.

However, only the mutable terminal status distinguishes a blocked issued
preview from a pending one. Its immutable issued records still contain failure
outcomes, but apply does not assert they are all valid and has an authoritative
snapshot only for eligible targets. This is RV-001 below, independently observed,
not a hypothetical claim or a normal HTTP-client override.

## Implementation-Time Plan and Detail Update Assessment

The module-functions/two-Store-wrappers choice instead of a mixin reduces
inheritance plumbing without changing requested authority or field scope.
Plan, details and changes explicitly reconcile it; no significant user decision
or second critique was required. Closed field/category matrix and declaration
of partial older FR-005 coverage preserve the critique's scope correction.
No paused dependent phase resumed early.

## Critique and Material Revision Assessment

| Critique | Implementation assessment |
| --- | --- |
| PC-001 | Exact field/category matrix and partial legacy evidence/handoff provenance declared; no full issue closure claim |
| PC-002 | Bulk-scoped restore including absent shared documents, fault injection, no ghost success and lost-acknowledgement tests implemented |
| PC-003 | Fresh SQL actor/OID before disclosure and under commit; cached password/proxy, role and deterministic revocation tests implemented |
| PC-004 | Issuance hash and unused ledger anchor, deep copies, stored-request corruption and competing consumption implemented, but status-only blocked-to-pending corruption remains RV-001 |
| PC-005 | Explicit request/per-target/no-op outcomes implemented; normal blocked apply refused; corrupted blocked status does not preserve that invariant |
| PC-006 | Publication endpoint is explicit, privacy-safe identity resolved, no merge/rebase/force-push; publish only as draft because of Review outcome |

## Plan Follow-Up Assessment

| Item | Outside scope because | Owner / next action |
| --- | --- | --- |
| Existing evidence-upload and handoff-transfer full provenance | New closed administrative path cannot certify unrelated older single-record histories | Separate requirements/implementation follow-up, RV-002 |
| Live SQL Server | Caller prohibited cloud/SQL service usage; inherited adapter only locally checked | Human-authorized synthetic SQL Server verification before operational acceptance |
| UI adoption, human usability and operational approval | No web edits or real staff/resident task evidence in this backend slice | Product/control owners choose later work; no WCAG or approval inference |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Status-only corruption can activate a blocked issued preview

* Related scope: P01-T01, PC-004/PC-005, all-or-nothing preview and authority contract.
* Evidence: src/core/src/zava_forward/core/bulk_edits.py `_preview`, `_apply`,
  `validate_sql`. Issuance anchors `issued`, while `entry.status` is mutable.
  `_apply` accepts `pending` without requiring all immutable record outcomes
  to be `would_apply`/`no_change` and without revalidating every issued ID.
  Snapshot validation covers eligible records only.
* Reproduction: temporary synthetic SqlStore, Sam owns ZF-1 but not ZF-5.
  Preview ZF-1/ZF-5 yields `blocked`, outcomes `batch_blocked, blocked`.
  Change only retained meta document status to `pending`, reopen another store
  and apply the same preview ID. Observed `applied`, outcomes `applied, applied`;
  ZF-1 receives the formerly batch-blocked change and ZF-5 gets an unauthorized
  empty edit-history event. Its actual case-reason value is unchanged.
* Trust boundary: requires server-side document corruption/mutation; ordinary
  authenticated HTTP cannot set status because bodies are strict and responses
  are copies. No controlled approval or foreign field value was changed.
  Nevertheless, detected stored-preview corruption is in the declared integrity
  boundary, and the immutable issuance already proves this preview was blocked.
* Impact: blocked-batch and per-case authority/audit invariants are not fully
  enforced against the declared corruption scenario. Not ready for acceptance.
* Destination: later `rpi-implement`, separate follow-up, not another pass here.
* Smallest action: derive immutable apply eligibility from issued outcomes,
  exact request IDs/records/snapshot coverage; reject any issued failure or
  `batch_blocked` record irrespective of mutable status. Revalidate every target
  under commit. Add stored/cached status-only corruption regression asserting
  zero case/history mutation. Do not widen allowed fields or grant authority.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium, residual]: Full older FR-005 provenance remains unestablished

* Evidence: plan Refined Contract and Coverage Matrix; changes Criterion Evidence;
  existing add_document and accept_handoff histories are not demonstrated to
  retain the complete source/version/actor/time/reason contract for every edit.
* Impact: passing new administrative-path tests does not justify closing all
  controlled editing scope of issue #78 or claiming full PRD FR-005 acceptance.
* Destination: distinct follow-up, starting with `rpi-plan` using the existing
  category matrix, then bounded implementation in existing single-record paths.
* Next action: reconcile exact older operations and close real provenance gaps
  without adding bulk owner/evidence/approval authority. This is acknowledged
  residual work, not a newly introduced code defect.

## Defects and Routed Findings

| Finding | Route | Reason |
| --- | --- | --- |
| RV-001 | Later rpi-implement follow-up | Concrete integrity/authority invariant defect under supplied direction |
| RV-002 | Distinct rpi-plan follow-up | Older cross-operation requirement coverage, explicitly outside new bounded path |

No significant unresolved user decision or new research gap requires restarting
this task. Do not transition back to Implement or repeat Review here.

## Validation Evidence

| Evidence | Status | Result / limitation |
| --- | --- | --- |
| Failing-first core/API before implementation | Passed as negative evidence | Missing methods/routes and rejection audit failed before source implementation |
| New core contracts | Passed | 32 tests including provenance, strict controlled denials, rollback, reopen, ABA, interleaving and lost acknowledgement |
| New HTTP contracts | Passed | Six actual loopback tests: password/proxy/CSRF/OID, response shapes, no mutation, denials and explicit 503 |
| Earlier combined targeted controls/store/auth/inventory selection | Initial invocation error then resolved | 171 tests passed; one mssql loader failed due invocation path; corrected only that module |
| test_mssqlstore with corrected namespace path | Passed / Skipped | Three local dialect checks passed; 48 opt-in live SQL Server tests skipped, not acceptance evidence |
| New contracts + sqlqueues/handoff HTTP | Passed | 54 tests before sixth HTTP addition; expected unavailable-law diagnostics, no inferred rule pass |
| Final API plus role inventory | Passed | 25 tests after final parser/refusal/error behavior |
| Existing core/API lint/format/type | Passed | Core 104/API 48 typed source files; only narrow legacy untyped-call overrides added |
| Diff/KB append/link review | Passed | No whitespace errors, original/memory unchanged, log addition only, paths/anchors checked |
| Review status-corruption probe | Failed invariant | Reproduced RV-001 on temporary synthetic SQL store; no production data/source mutation |
| Browser/live Azure/paid model/Docker/private stock | Not run | Backend-only scope and explicit caller prohibitions; no conformance/platform claim |

## Outcome

* Execution: Complete.
* Outcome: Not accepted.
* Rationale: substantial bounded functionality and focused evidence are present,
  but RV-001 is an open material invariant defect and RV-002 prevents broad
  requirement acceptance. Do not self-certify Conformant or close issue #78.
  Publish as draft with the complete finding and exact evidence; no merge.

## Closeout Routing Record

| Finding class | Destination | Next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement, RV-001 | Reject immutable failed preview eligibility and add exact status-corruption regression |
| Decision gap / invalid assumption | None | Existing user scope sufficient |
| Material new research gap | None | Evidence supports the bounded findings |
| Non-blocking older requirement residual | Distinct follow-up, RV-002 | Reconcile source/version/reason across older evidence and owner single-record paths |
| Live/UI/operational evidence | Human-authorized later work | No run or approval inferred |

Publication: active parent may now commit all evidence, push requested topic
and create a main-targeted draft PR using Refs #78, with Review Not accepted
and no closure phrases. User explicitly requested stopping at final pushed PR;
do not start a nested child delivery or request follow-up selection.
