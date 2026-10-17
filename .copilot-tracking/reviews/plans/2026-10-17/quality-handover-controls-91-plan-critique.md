---
title: Quality handover controls issue91 plan critique
description: Independent final-candidate assessment against the supplied issue91 boundary
ms.date: 2026-10-17
---

## Metadata

* Task ID: issue91
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/quality-handover-controls-91-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/quality-handover-controls-91-phase-details.md
* Research: .copilot-tracking/research/2026-10-17/quality-handover-controls-91-research.md
* Critique execution status: Complete
* Assessment: Single independent final-candidate critique; no delegated agents or subsequent phases.

## Inputs and Criterion Boundary

The controlling criteria are the caller's exact three issue91 requirements:

* Contractors supply evidence only, never accept work, close defects or trigger payment.
* Remediation requires evidence and independent reverification.
* Replacing evidence invalidates dependent handover.

The supplied direction authorizes automatic full RPI, not skipped phases or
operational acceptance. Preserve #84 stock, #94 finance and merged #90 provider
safeguards. Do not introduce professional authority, risk policy, payment
execution or a contractor portal. The existing staff-assisted evidence route
is compatible with the criteria; direct contractor writes are not required.
Parallel #95 ownership of finance.py, dataset.py, app.js, server.py and the
manifest is preserved. Those source files were not edited; no other worktree
was inspected.

The complete candidate plan and phase details, research C1-C7, A1-A4,
P01-T01/P02-T01/P03-T01, test-count limits, non-goals, dependency declarations
and external acceptance limits were assessed together. Relevant supplied
source evidence was read directly:

* src/core/src/zava_forward/core/quality.py
* src/core/src/zava_forward/core/change_provenance.py
* src/core/src/zava_forward/core/stock.py
* src/core/src/zava_forward/core/sqlstore.py
* src/core/src/zava_forward/core/finance.py
* src/core/src/zava_forward/core/resident_decisions.py
* src/core/src/zava_forward/core/store.py
* src/core/src/zava_forward/core/projection.py
* src/core/tests/test_quality_procurement.py
* src/core/tests/test_resident_decisions.py, relevant scoped-quality references
* src/api/tests/test_role_matrix.py
* src/api/tests/test_mssqlstore.py
* src/api/src/zava_forward/api/server.py, quality dispatch
* src/api/src/zava_forward/api/web/ops.js
* docs/prds/zava-forward-retrofit-programme-demonstrator.md, FR-017/018,
  AC-013/020/042 and retained replacement learning
* docs/adrs/0002-pilot-readiness-architecture.md, retained #24/#27 and #58 learning
* docs/reference/research/ux/customer-journeys/programme.md
* docs/reference/research/ux/customer-journeys/suppliers.md

Repository context was read from docs/case_study_48_original.md,
docs/case_study_48_addendum.md, docs/reference/README.md,
docs/reference/memory.md and the housing-association primer. Memory is context,
not acceptance evidence. No external legal/currentness assertion is made.

This assesses implementation-plan credibility, not implementation completion.
Research's reported 50 baseline passes and temporary JSON/SQLite probes are
supplied evidence, not independently rerun results. Actual SQL Server parity
and browser execution remain implementation obligations.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Contractor evidence-only boundary; A1; C3/C5 | Covered | projection.py default-denies contractor writes; server.py passes the authenticated actor to existing quality actions. Staff-assisted submission remains the manual path. Finance is record-only. |
| Current staff and retained participant independence; A2; C2/C6; P01-T01 | Covered at requirement/design level | _actor checks current registered name/role/email/code/OID; stock.decision_scope supplies the existing SQL writer-time actor validator. Plan excludes all retained contributors, not just the latest fixer, and distinguishes labels from competence. Exact regression allocation is incomplete under PC-002. |
| Evidenced remediation and reverification; A2; P01-T01 | Covered at requirement/design level | Nonempty remediation retained on current/historical defects; legacy FIXED acceptance must not bypass it; reinspection is restricted to FIXED. Existing blank-note fixtures are to be updated, not deleted. PC-002 covers missing exact test ownership. |
| Replacement and legacy active decisions; A3; C2/C4; P01-T01 | Partial | Historical retention, new acceptance/handover and non-actionable superseded records are specified, but the singular predecessor algorithm does not settle multiple legacy same-measure handovers: PC-001. |
| SQL identity/transaction and recovery scope; A3/A4; C6; P01-T01/P03-T01 | Covered at invariant level | Existing writer-time identity validation, rowversions, safety/resident rechecks and _discard quarantine are suitable mechanisms. Preserving prior audit across the stock scope's unconditional discard requires a specific owned regression: PC-002. |
| JSON failure recovery; P01-T01; non-functional requirements | Covered at invariant level | Preimage and own-ledger-tail restoration with explicit uncertain durability; no false crash-atomicity claim. Concrete fault assertions still need allocation under PC-002. |
| #84/#94/#90 preservation and #95 overlap | Covered | No new stock/building/risk policy is proposed; existing helper and test boundaries are reused. Finance/grants must remain unchanged. Shared feature files are excluded unless an unavoidable dependency is declared. |
| Minimal web surface and documentation; C7; P02-T01 | Covered | ops.js only; remediation and superseded history, retained semantics and resident confirmation; current web-guidelines source/review and actual browser required. No broad redesign or WCAG acceptance claim. |
| Exact regression ownership; P01-T01/P03-T01; A1-A4 | Partial | Canonical files and method limits are identified, but no criterion-to-method/replay mapping or exact selected execution set is locked: PC-002. |
| Actual local SQL parity/browser and external limits; A4; P03-T01 | Covered as future gates | Owned disposable loopback SQL Server, actual connection readiness, secret suppression, cleanup and commands/counts/skips required. Human competence and Azure acceptance remain external. |
| Ordered RPI, dependency and delivery boundary | Covered | Research exists; critique precedes implementation; P02 depends on P01 and P03 on both; independent Review remains required. #89 is hierarchy, #90 already merged; no invented dependency or merge authorization. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The candidate is appropriately scoped and substantially grounded
  in existing delivery. A legacy supersession case can escape the detailed
  replacement algorithm, and the requested exact regression ownership has not
  been locked beyond file names and categories. Both are direct planning
  corrections within the already authorized issue91 boundary.
* Execution and verdict are separate: this critique is Complete; implementation
  readiness is Revise. No implementation, SQL parity or browser pass is asserted.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Singular predecessor invalidation leaves legacy same-measure handovers unresolved

* Related IDs: A3, research C2/C4, P01-T01, P02-T01.
* Evidence: .copilot-tracking/details/2026-10-17/quality-handover-controls-91-phase-details.md:30-36
  specifies an exact same-measure predecessor and clearing the old record.
  src/core/src/zava_forward/core/quality.py:73-101 permits another submission
  whenever all existing same-measure records are HANDED; it neither supersedes
  nor clears those records. hand_over_quality and add_aftercare at the end of
  that file continue to treat each HANDED record as actionable. Research also
  reports the surviving old handover after replacement.
* Concern: Repeating the existing submit/accept/handover sequence can leave
  several same-measure records with live handover state before this change.
  The broad A3 requirement intends invalidation, but the detailed single-old-record
  design does not define what happens to earlier such records. Invalidating
  only the latest predecessor leaves another old handover and its aftercare
  route active. This is a source-supported reachable legacy state, not a claim
  that private or deployed data has been inspected.
* Impact: Replacement can still leave dependent handover active, violating
  the exact third criterion even when the new two-record happy path passes.
* Smallest useful change: Specify that replacement atomically retires every
  prior active acceptance/handover for that exact measure, preserving their
  original evidence, decisions, defects and aftercare as explicitly historical.
  Define lineage for the new record and all affected legacy records; ignore
  already superseded history when checking duplicates, while continuing to
  reject genuinely in-progress duplicates. Keep other measures and
  finance/grants unchanged. Do not add a migration that fabricates acceptance
  or a new endpoint.
* Action owner: Planning parent, updating P01-T01 and its A3 regression allocation;
  implementation owner subsequently executes it.
* Exact resolving evidence: Revised plan/details explicitly address two
  legacy HANDED records for the same measure, and the case of an older HANDED
  record plus a newer ACCEPTED record. A named canonical planned regression
  must require replacement to leave neither prior decision active, retain all
  history, reject actions on every retired record, preserve a different
  measure and finance/grants, and require new independent acceptance and fresh
  handover. Assign JSON/SQLite execution and actual SQL Server replay, including
  reopen and stale-writer refusal, under PC-002. The planning gate is resolved
  by that explicit contract/allocation; runtime proof belongs to implementation.
* Decision route: Direct planner correction; directly planner-fixable: Yes.
  No significant/divergent user decision or new requirement is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Regression ownership is bounded but not exactly locked

* Related IDs: A1-A4, P01-T01, P03-T01, Test Ownership and Validation Lock.
* Evidence: .copilot-tracking/plans/2026-10-17/quality-handover-controls-91-plan.md:127-139
  names files, maximum additions and broad suites.
  .copilot-tracking/details/2026-10-17/quality-handover-controls-91-phase-details.md:84-95
  delegates selection of stale/actor/audit/replacement/recovery tests to execution.
  src/api/tests/test_mssqlstore.py:154-165 already provides
  MssqlProcurement inheriting test_quality_procurement.SqlFlows.
  src/core/src/zava_forward/core/stock.py:28-40 unconditionally calls
  _discard() on failure, whereas
  src/core/src/zava_forward/core/sqlstore.py:629-655 retains prior audit only
  when supplied through pending.
* Concern: There is no exact mapping from the new invariants to named planned
  canonical methods/subcases, backend owners and the actual SQL replay selector.
  The implementer still has to choose what the purported locked acceptance
  evidence contains. In particular, a simple save-failure test does not prove
  that wrapping stock.decision_scope preserves a legitimate pending audit
  prefix after its own discard, or that an actual transactional audit-insert
  failure and persistent recovery-read failure cannot later flush success.
  Existing MSSQL inheritance also means new aliases are not automatically
  necessary; duplicate aliases must not inflate apparent coverage.
* Impact: All broad suites could pass while the highest-risk newly promised
  behavior is untested or absent from the actual SQL Server run. This misses
  the caller's explicit exact-regression-ownership planning condition.
* Smallest useful change: Add a compact acceptance matrix to the plan/details
  identifying planned method/subcase names, canonical class/file, expected
  refusal or state/audit assertion, JSON/SQLite/HTTP/MSSQL applicability and
  selected command/class. Reuse parameterized subcases within the existing
  18 core/4 HTTP/one browser limits; no new test framework, source feature or
  extra acceptance criterion is required. State that inherited MSSQL methods
  are replayed once rather than copied or redundantly aliased.
* Action owner: Planning parent; implementation owner supplies the recorded
  results against that locked matrix.
* Exact resolving evidence: The revised matrix allocates all of the following:
  current registered actor denial for every quality write; populated
  name/email/code/OID aliases and original/earlier fixer exclusion over repeated
  cycles, including conservative legacy participant handling; blank remediation
  and legacy FIXED without evidence; pass/fail reinspection state restrictions;
  malformed indices; Accepted/HANDED replacement and PC-001 legacy cases;
  missing/stale resident bindings and unchanged safety/resident boundaries;
  unchanged finance/grants; SQL writer-time actor change and stale replacement
  writes; pre-save, case-write and actual transactional audit failure;
  early/persistent recovery-read failure with original error, clean failed
  audit tail/cache and preserved legitimate pending prefix; JSON state/ledger
  recovery and explicit uncertain-durability behavior. It names
  src/core/tests/test_quality_procurement.py, src/api/tests/test_role_matrix.py
  and the actual src/api/tests/test_mssqlstore.py replay owner, plus the one
  bounded real-app browser journey. Existing tests may satisfy entries if
  identified precisely; not every entry requires a new method. Local SQL
  selectors must exercise the canonical quality cases with ZF_TEST_MSSQL=1,
  not only the server-independent portability checks. Runtime results and
  unperformed checks are recorded later, not invented to resolve planning.
* Decision route: Direct planner correction; directly planner-fixable: Yes.
  No user response or expansion of the authorized implementation is required.

## Strengths and Residual Risk

* Research checked existing delivery and counterevidence: HTTP contractor
  denial and record-only finance are preserved, not reimplemented as new features.
* Actor validation is not merely an API role check. The selected _actor and
  stock transaction hook can revalidate the current staff row inside save;
  rowversions prevent a stale case write from restoring retired decisions.
  The pending-prefix interaction above is a regression/design obligation,
  not grounds to replace shared SQL transaction machinery.
* The candidate retains all contributing identities over repeated repairs and
  does not misrepresent fixture roles as professional competence. Legacy
  remediation without positive evidence cannot become accepted by default.
* Explicit measure/resident revision bindings, independent fresh acceptance,
  historical preservation, non-actionable superseded records and unchanged
  financial history align with the exact issue rather than full PRD adoption.
* JSON recovery is correctly bounded to caught failures; crash-atomic
  multi-file persistence is not promised.
* Existing stock/building/provider controls are safeguards to preserve, not
  authorization to introduce new risk policy or professional approval rules.
* Actual SQL Server and changed-web browser checks are appropriately required
  in implementation. They cannot establish Azure, real staff competence,
  resident understanding, legal sufficiency or WCAG conformance.

## Questions or Blocking Evidence Gaps

* No user question or decision-critical external research gap blocks these
  planner-owned revisions.
* No new authority, risk threshold, payment action, shared #95 feature edit or
  contractor-upload capability is recommended.

## Limitations

* Source inspection establishes reachable legacy states and helper behavior;
  this critique did not execute fault probes, tests, Docker, SQL Server or a
  browser, and did not inspect private data or other worktrees.
* The research transcript is accepted as supplied evidence with its stated
  scope; its commands/results were not independently reproduced here.
* Relevant source slices were inspected, not an open-ended repository audit.
  No new delivery, regulatory-currentness or platform-acceptance claim follows.
* Only this critique artifact was written. Plan, phase details, research,
  session state, source and existing review records remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the legacy same-measure invalidation contract and
  exact regression/replay matrix, then disposition both findings in planning.
* User response required: No.
* Return this one complete PC-001/PC-002 finding set to the automatic RPI parent.
  The parent can revise directly and proceed through its authorized gates
  without a second critique. No further agent or phase is invoked here.

## Next Steps

Planning parent resolves PC-001 and PC-002 in the plan/details and records their
disposition before implementation. No user action is required. This critique
stops here; its Complete execution status does not override its Revise verdict.
