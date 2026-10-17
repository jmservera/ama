<!-- markdownlint-disable-file -->
# RPI Plan Critique: Controlled bulk preview

## Metadata

* Task ID: jmservera/ama#78
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md
* Research: .copilot-tracking/research/2026-10-17/controlled-bulk-preview-78-research.md
* Critique execution status: Complete
* Critique count: One final-candidate assessment. Findings below are the complete actionable set for the supplied boundary, not a request for another critique.

## Inputs and Criterion Boundary

* Caller direction: complete ordered Research -> Plan -> Implement -> Review and deliver a pushed main-targeted PR; this critique writes only this artifact.
* Preserve the three issue criteria: retain source/version/actor/time/reason; show exact targets, changes, failures and per-case outcomes before apply; prohibit controlled bulk approvals/actions, including technical, consent, safety, procurement, budget, invoice, payment, claim, quality, defect, complaint and contractor-instruction boundaries.
* Keep a closed allowlist without widened authority, existing SQL transactions and hash-chain audit, and server-enforced freshness/authority races. No cloud, private data, UI overhaul or framework change.
* Supplied research C1-C9/W1-W2, its findings and residual uncertainty were assessed against the plan and both implementation phases.
* Bounded source inspection covered PRD FR-005/006/007 and AC-007/008/009/010, Store actor/detail/persistence behavior, handoff semantics, SQL sync/save/discard/audit hooks, role projection, API authentication/POST routing, SQL dialect hooks and existing synthetic test patterns.
* Repository context read: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and docs/reference/research/sector/housing-association-primer.md. Memory was context, not evidence.
* The supplied issue and PR pointers were checked read-only with gh. Issue #78 has no declared dependency; #73 is its parent. PR #377 is open against main and overlaps store.py, sqlstore.py, projection.py, server.py, route inventory, component documentation and KB index/log. Its forms module/routes remain separately owned, not a dependency.
* Locked ownership: removals none; at most one new core module, one core test module and one API test module, plus required RPI artifacts. Corrections below fit these boundaries and existing integration/documentation files.
* Assessment establishes plan credibility, not implementation correctness, operational approval, accessibility conformance or live SQL Server acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Issue criterion 1; PRD FR-005; AC-007 | Partial | New bulk edit provenance is explicit; evidence-reference, task-owner and individual-edit coverage is not reconciled. PC-001. |
| Issue criterion 2; PRD FR-006; AC-009 | Partial | Ordered server-owned preview is a sound direction; request binding and failure/no-op contract need resolution. PC-004, PC-005. |
| Issue criterion 3; PRD FR-007; AC-010 | Covered in direction | Closed fields, no ownership transfer and explicit controlled-category negative tests preserve the boundary. No recommendation here authorizes additional bulk fields. |
| C1-C2; research Q1 | Partial | PRD/BRD numbering difference is correctly identified, but the narrow slice is not evidence of full FR-005 delivery. PC-001. |
| C3-C4; named staff, ownership and handoffs | Partial | Existing owner/manager checks are reused; fresh disclosure authorization and identity binding need exact treatment. PC-003. |
| C5; SQL atomicity and checked documents | Partial | Transactional revalidation is required, but pending audit and shared-document rollback need concrete recovery steps and tests. PC-002. |
| C6; privacy projection | Covered in direction | Nested free-text redaction is required. Implementation must explicitly handle old/new/source/reason values, not assume existing key-based redaction already does so. |
| C7/C9; P02-T01 | Partial | Authenticated routes, CSRF and role inventory are specified; identity and response semantics need sharper contracts. PC-003, PC-005. |
| C8; inherited SQL Server path | Covered with limitation | Portable SQL and dialect regressions are planned; live cloud SQL is deliberately not run. |
| Case ABA, authority race, replay | Partial | Case rowversion is explicitly required, including changed-away-and-back; deterministic cross-store schedules and issuance binding remain underspecified. PC-002 through PC-004. |
| P01-T01 | Partial | Broad test topics exist; transaction recovery, binding and requirements coverage need implementation-ready resolving assertions. PC-001 through PC-005. |
| P02-T02; ordered RPI/pushed main PR | Partial | Validation and preparation for Review are included, but the accepted delivery endpoint lacks an explicit completion gate. PC-006. |
| W1/W2; dependencies and file limits | Covered | No invented #73/#377 dependency; additive reconciliation and locked ownership are credible. Preserve concurrent edits rather than replacing shared files. |
| No cloud/private data/UI/framework change | Covered | Backend-only synthetic validation and explicit non-goals are appropriate. |

## Verdict

* Verdict: Revise
* Severity summary: 4 High, 2 Medium, 0 Critical, 0 Low.
* Rationale: The core architecture is credible, but this is not yet an implementation-ready account of the complete issue. The plan must reconcile its requirements claim and pin the recovery, authorization, issuance-binding and response contracts. Existing SQL behavior makes these substantive correctness concerns, not documentation preferences.
* All findings are direct planner corrections under current user direction. No user response or widened authority is required. The planning parent should disposition this one complete set and finalize without another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The administrative allowlist is not a demonstrated reconciliation of the full controlled-editing requirement

* Related IDs: Issue criterion 1; PRD FR-005, AC-007/008; research Q1/C1/C3/C4; P01-T01; P02-T02.
* Evidence: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md:13-19,31-33,48-60,82-87 limits implementation to case_reason and two handoff fields while claiming preservation of FR-005/006/007. docs/prds/zava-forward-retrofit-programme-demonstrator.md:840-842 includes individual case fields, evidence references, task owners, due dates and permitted workflow details. Issue #78's summary likewise includes evidence references and owners. src/core/src/zava_forward/core/workflows.py:167-235 proves acceptance-only ownership transfer, not that every existing owner/evidence edit retains source/version/reason. For example, accept_handoff records the ownership transition and history but does not itself establish the complete FR-005 provenance contract.
* Concern: Research treats three candidate administrative fields as sufficient without a requirement-to-existing-operation evidence matrix. Avoiding unsafe bulk owner changes is correct; treating that exclusion as proof that individual controlled editing and provenance are already complete is not. There is also no explicit mapping of API aliases to stored paths or justification that the stock-query owner/manager boundary is the intended field authority for each new edit.
* Impact: The implementation could pass every new bulk test yet leave material issue scope unimplemented or claim unsupported FR-005 acceptance. Expanding the bulk allowlist to compensate would violate the confirmed authority boundary.
* Smallest useful change: Add a bounded matrix for each FR-005 category identifying the existing authorized single-record operation, its source/version/actor/time/reason history evidence, and any remaining gap. Define case_reason -> case.reason, handoff_due_at -> case.handoff.due_at and handoff_next_action -> case.handoff.next_action explicitly, including eligible states, field-level read/write rights and unchanged controlled fields. Resolve actual provenance gaps through existing bounded integration where feasible; otherwise explicitly retain them as unmet scope rather than declare full issue/FR acceptance. Do not add bulk ownership transfer, evidence approval or controlled decisions.
* Action owner: Planning parent.
* Exact resolving evidence: Revised plan/details with the category-to-operation/provenance matrix, exact field mapping and tests assigned to the locked test modules; an explicit acceptance statement distinguishing the delivered bulk slice from any still-unmet individual-edit criteria. Existing behavior must be evidenced by a specific operation/history shape or test, not the issue's starting assertion that controlled edits exist.
* Decision route: Direct planner correction. Current user direction already rules out widened authority; no significant or divergent user decision is requested.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Atomicity needs an explicit full rollback and audit-queue recovery contract

* Related IDs: Issue criteria 1/2; C5; P01-T01; SQL atomicity, rollback/reopen and authority-race acceptance.
* Evidence: .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md:30-40 calls for a transient validator, standard permission/value errors and no published success after generic failure. src/core/src/zava_forward/core/sqlstore.py:501-637 shows that _finish flushes pending audit independently, save invokes _discard only for ConflictError/GateError, generic exceptions roll back without clearing pending/shared state, and _proc_sync loads existing document rows without removing an in-memory document whose row is absent.
* Concern: The stated invariant is correct, but the planned recovery action only expressly clears validation context. A PermissionError/ValueError raised inside the new transaction validator, or a generic write/audit/commit failure, can leave queued success events for outer lock exit to flush separately. Case cleanup does not establish shared-document cleanup: a failed first bulk_edits creation can leave an in-memory document without a persisted row, and a failed terminal update can remain dirty for a later unrelated save. These are distinct from duplicate success events and are not resolved solely by a COMMIT/ROLLBACK pair.
* Impact: A denied or failed batch could produce a hash-valid success audit, ghost preview/terminal result, or delayed unrelated publication despite no atomic case commit.
* Smallest useful change: Specify one bulk-scoped recovery path for all pre-commit failures, including validator permission/value exceptions: discard staged case/history mutations, pending success/batch audit, touched sets, validation context and modified shared-document state; restore absence as well as existing document content. Emit only the separate metadata-only refusal after restoration. An unavailable refusal audit must never turn the failed apply into success. Preserve existing unrelated operations and SQL checks rather than introduce a second transaction system.
* Action owner: Planning parent, with P01-T01 implementation owner.
* Exact resolving evidence: Named tests inject failure after an earlier case write, during document write, during audit append and before commit; also deny authority inside the locked validator. Each asserts original cases/history and preview state, no success ledger entries, valid audit chain, cleaned local state, and identical reopened state. Include absent bulk_edits on first-write rollback and a subsequent unrelated successful save proving no ghost state/audit is published. For a lost commit acknowledgement, document outcome uncertainty and verify persisted preview/result before any retry; do not infer rollback from the client exception alone.
* Decision route: Direct planner correction; no user decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Fresh identity must protect preview disclosure and include the authenticated identity binding

* Related IDs: Issue criteria 2/3; C3/C5/C7; P01-T01; P02-T01; cached-identity and authority-race acceptance.
* Evidence: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md:58-67 expressly places the fresh check at apply. .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md:28-34 mentions actor/staff context but does not define identity fields or a preview disclosure transaction. src/core/src/zava_forward/core/sqlstore.py:420-451 caches staff after initial load. src/core/src/zava_forward/core/store.py:398-405 compares code/role/name against the cached staff record. src/api/src/zava_forward/api/auth.py:74-87,136-163 resolves password identities or trusted-proxy OID bindings from that cache; trusted-proxy roles come from authenticated app-role claims.
* Concern: A fresh apply check does not prevent an already revoked/deleted staff identity from obtaining old field values in a new preview. Moreover, copying _stock_actor's comparison is insufficient for an OID rebind that preserves email/code/name/role: an old cached proxy identity could still compare equal to the new staff record. The plan has not distinguished provider role evidence from registered staff attributes.
* Impact: Preview can disclose content after revocation; a stale principal binding can survive the apply guard even while ordinary role/owner tests pass.
* Smallest useful change: Require a coherent fresh SQL authorization snapshot before producing any sensitive preview fields, and repeat it under the apply writer transaction. Define creator binding and the comparison to the fresh staff record, including provider-relevant OID binding where present, existing role constraints, registered named identity, case ownership and field visibility. Do not replace trusted-proxy claim authority with a client-supplied or database-granted role. Implement through the bounded bulk integration; no general authentication rewrite is authorized.
* Action owner: Planning parent; P01-T01 and P02-T01 implementation owner.
* Exact resolving evidence: Two-store tests prime cached staff, then delete/revoke/rebind staff through the database without restarting or relying on a case-sequence change. Preview must deny without old/new content; apply must deny with no case mutation. Include changed OID with unchanged email/code/name/role, foreign creator, owner change, and a deterministic revocation between preparation and transaction validation. Use synthetic password and trusted-proxy HTTP fixtures to prove the actual identity boundary, not only fabricated user dictionaries.
* Decision route: Direct planner correction; no user decision.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Checked-document concurrency does not itself prove the applied preview is the one originally presented

* Related IDs: Issue criterion 2; C5; P01-T01; preview tampering, case ABA and replay acceptance.
* Evidence: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md:64-71 requires request rechecking and a server preview ID. .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md:27-43 names durable snapshots and preview-tampering tests but no immutable issuance binding. src/core/src/zava_forward/core/sqlstore.py:621-637 compares current meta content to the last locally read content; this detects a concurrent change, not the validity of content already loaded before apply.
* Concern: Restricting apply to preview_id correctly blocks client-carried edits, but the candidate does not say what immutable reference proves the loaded request, ordered targets, old/new fields, actor and expected versions are still the issued preview. A mutable returned dictionary or modified cached preview can change the server-side request. Re-reading a modified stored document and validating it only against itself is not tamper detection. Case rowversion prevents case ABA; it does not bind the preview request or prevent simultaneous application of one preview by two stores.
* Impact: Apply may execute different allowed edits from those the user inspected, or execute a single preview twice, despite using only allowed fields and fresh case data.
* Smallest useful change: Define the canonical issued-preview content and an integrity reference anchored independently of its mutable request representation, using existing audit/persistence facilities. Deep-copy response data. Under the writer transaction, compare the canonical stored preview to issuance evidence, revalidate its closed request/field schema, current case rowversions and creator, and atomically transition the still-pending preview with the case writes/result. State the trust boundary: this protects API/cached-state mutation and detected stored-preview corruption, not an attacker able to rewrite both the database and trusted ledger.
* Action owner: Planning parent, with P01-T01 implementation owner.
* Exact resolving evidence: Explicit issuance-binding design plus tests that mutate the returned preview, mutate cached request targets/values/source/version, and modify a stored request before a new store loads it. None may apply changed instructions. Include allowed-to-different-allowed edits, not only forbidden keys. Preserve the explicit case changed-away-and-back rowversion test and add a two-store apply interleaving proving exactly one case/history/audit/result commit.
* Decision route: Direct planner correction; no user decision and no new service required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Preview failures and no-ops have test topics but no deterministic response/state contract

* Related IDs: Issue criterion 2; PRD AC-009; P01-T01; P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md:54-69,84-85 specifies would_apply/blocked/batch_blocked and mentions no-op tests. .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md:41-43,54-56 lists invalid/no-op/mixed cases alongside 200 preview, malformed/forbidden 400, permission 403 and stale/replay 409.
* Concern: The candidate does not separate malformed batch requests from well-formed requests containing target-level permission/rule failures. It does not define whether unchanged fields are no-ops or writes, whether no-op targets receive versions/history, or how blocked previews transition on attempted apply. An implementer could return only a top-level error for a mixed target set, hiding the per-case outcomes required before apply, or invent misleading successful change events for unchanged values.
* Impact: HTTP and core implementations can disagree, and listed tests can pass without a complete inspectable per-case result.
* Smallest useful change: Define a compact schema/state table: request-wide validation errors versus per-target failures, ordered outcomes for every submitted ID, no-content inaccessible/missing targets, no-op treatment, batch-blocking behavior and allowed apply transitions. A well-formed inspectable blocked preview should retain all safe per-target outcomes; it must not become a partial apply. Choose and document whether no-op records change edit versions/history, without presenting an unchanged value as an actual field change.
* Action owner: Planning parent; P01-T01/P02-T01 implementation owner.
* Exact resolving evidence: Plan/details examples and assigned exact-shape HTTP assertions for all-valid, all-no-op, valid-plus-no-op, valid-plus-invalid, inaccessible/missing, all-blocked and apply-of-blocked cases. Assertions cover response codes, complete ordering, disclosure suppression, zero mutation on blocked batches and persisted audit/result semantics.
* Decision route: Direct planner correction; no user decision.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: The implementation handoff does not define completion of the required Review and pushed main PR

* Related IDs: Caller ordered RPI/pushed main PR requirement; P02-T02; delivery handoff.
* Evidence: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md:31,38 requires the full workflow and pushed PR, but P02-T02 at 117-121 and the final handoff at 148-152 stop at implementation/evidence. .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md:59-69 stops at preparation for one Review.
* Concern: Review is correctly separate from implementation, but the candidate does not define the parent's final continuation/done gate. There is no explicit resolving evidence for addressing review findings, committing reviewed evidence, pushing the topic branch and opening/verifying a main-targeted PR. The task can otherwise be marked complete after local tests or Review preparation.
* Impact: The requested persistent delivery can be missed even if the backend implementation is correct.
* Smallest useful change: Add a parent-owned closeout gate after implementation: execute the ordered Review once against the implemented candidate, resolve its actionable findings, record real checks and limitations, obtain gh api user privacy-safe local author/committer identity, commit evidence/code with the required trailer, push feat/controlled-bulk-preview-78 and create/verify a PR against main. Preserve #377 as a concurrent overlap, not a stacked base or dependency. Record CI/rubric status honestly and leave merge to the owner.
* Action owner: Planning parent/RPI coordinator, not the bounded core implementation task.
* Exact resolving evidence: Revised handoff and done criteria naming the Review artifact, final reviewed commit SHA, remote branch/head and main-targeted PR URL, with check outcomes or pending/blocked states recorded. No merge, force-push or second plan critique is implied.
* Decision route: Direct planner correction; no user decision.

## Strengths and Residual Risk

* Closed fields, exact apply key, explicit negative controlled-category tests and all-or-nothing batches are preferable to arbitrary patches or approval denylisting.
* Ownership remains acceptance-only; resident commitments, safety clocks and controlled evidence/decisions remain outside this bulk feature.
* Case digest plus SQL rowversion explicitly addresses changed-away-and-back cases. Keep both; a digest alone is insufficient.
* The candidate correctly identifies cached staff and transaction-time validation rather than relying only on a pre-lock check.
* Existing SQL save/audit/document machinery and portable dialect hooks avoid a new persistence layer. Their rollback edge cases must be addressed as PC-002 specifies.
* Nested history free-text can bypass the existing projection's key-specific rules if represented as generic old/new values. The plan already requires redaction; implementation must test canaries in every retained free-text position and use the permitted projection.py integration where needed.
* Temporary synthetic fixtures must be located beneath the worktree, not system temporary directories. Existing tests using default temporary locations are not an instruction to violate the caller's environment constraints.
* Preview retention/document growth and whole-document contention remain engineering risks. Document the retained-record scope and avoid claiming scale guarantees from 100-target request limits.
* JSON's existing single-process/multi-file durability limitation is expressly disclosed, not repaired or promoted to SQL-grade atomicity.
* Live Azure SQL, human operational acceptance, actual staff/resident research and accessibility acceptance remain outside this offline backend slice. No tests or regulatory-currentness verification were inferred from source inspection.

## Questions or Blocking Evidence Gaps

* No user question. Current direction resolves the authority and delivery choices.
* PC-001 requires bounded evidence reconciliation, not open-ended research or a claim that missing scope is complete.
* If an FR-005 gap cannot be addressed inside confirmed boundaries, the parent must retain it explicitly as unmet acceptance rather than silently expand authority or close the whole issue.
* Source inspection was sufficient for this Revise verdict; no decision-critical missing external evidence prevents assessment.

## Limitations

* This is a plan critique, not an exploit assessment or implemented-code Review. No implementation was created or executed and no application tests were run.
* Only the supplied artifacts, relevant bounded source and supplied GitHub pointers were inspected. PR #377's open state is point-in-time context, not a future merge-order guarantee.
* The existing untracked plan/details/research/session artifacts were left unchanged. This critique does not authorize moving, committing or discarding them.
* All implementation test results and recovery guarantees remain unverified until the planned work executes.

## Recommended Next Action

* Highest-impact finding: PC-002, because a failed batch could leave a misleading success ledger or delayed shared-state publication.
* Action owner: Planning parent.
* Smallest next action: Add the explicit bulk rollback/cleanup contract and resolving fault-injection assertions to P01-T01, then disposition PC-001 and PC-003 through PC-006 in the same direct plan revision.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md](.copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md](.copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md) | Assessed implementation details |
| [.copilot-tracking/research/2026-10-17/controlled-bulk-preview-78-research.md](.copilot-tracking/research/2026-10-17/controlled-bulk-preview-78-research.md) | Supplied research and evidence |
| [.copilot-tracking/reviews/plans/2026-10-17/controlled-bulk-preview-78-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/controlled-bulk-preview-78-plan-critique.md) | Complete single-pass findings |

## Next Steps

The active planning parent should directly resolve/disposition PC-001 through
PC-006, finalize the plan without another critique, and continue the confirmed
ordered RPI workflow after its gates pass. No user action is required. This
critique invocation stops here; it neither implements nor opens a PR.
