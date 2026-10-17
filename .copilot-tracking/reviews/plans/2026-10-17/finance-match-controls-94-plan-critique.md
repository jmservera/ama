---
title: Finance match controls 94 plan critique
ms.date: 2026-10-17
---

## Metadata

* Task ID: jmservera/ama #94; #93 is hierarchy only.
* Critique date: 2026-10-17.
* Plan: .copilot-tracking/plans/2026-10-17/finance-match-controls-94-plan.md.
* Phase details: .copilot-tracking/details/2026-10-17/finance-match-controls-94-phase-details.md.
* Critique execution status: Complete.
* Assessment count: One final-candidate critique; no implementation, worker delegation or delivery.

## Inputs and Criterion Boundary

* Read the exact candidate plan, phase details and supplied finance research.
  Current caller direction is the acceptance authority for this assessment.
* Read repository context in docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory is context, not evidence.
* Bounded verification reads: src/core/src/zava_forward/core/finance.py,
  src/core/src/zava_forward/core/sqlstore.py,
  src/core/src/zava_forward/core/change_provenance.py,
  src/core/src/zava_forward/core/controls.py,
  src/core/src/zava_forward/core/store.py,
  src/core/tests/test_finance_signoffs.py and relevant FR-018/AC-021/AC-042
  portions of docs/prds/zava-forward-retrofit-programme-demonstrator.md.
* Assess nothing paid by the product, actual line-level exceptions, actual
  same/different staff identity including OID, unknown-input refusal,
  budget/commitment preservation and held record-only disposition. Assess
  failing-first, reopen, rollback, concurrency and fresh permission at writes.
* Preserve locked production/test targets, finance test ownership, maximum two
  new test files, no removals and only the obsolete null-line assertion change
  in the existing suite. No new authority, currency or payment model, private
  dataset access, Azure activity or paid AI is needed.
* No explicit dependency is declared. The sole planned shared SQL save
  validation hook has disclosed possible overlap with #90; #84 signoff behavior
  and ownership remain unchanged. No dependency is inferred from either.
* The authorized ordered RPI continues only after blocking findings are
  disposed. Maximum two coordinator correction batches; do not repeat this
  critique. Delivery remains parent-owned, with the final-push stop retained.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Exact no-payment criterion; plan AC1; C1/C7 | Partial | Record-only boundary is explicit; negative ledger and forbidden-side-effect test obligations need precision, PC-002. |
| Line-level exceptions; plan AC2; C2; P01-T01/T02 | Covered | Explicit actual zero-based invoice lines, aggregate blockers on affected lines and ambiguous-commitment refusal; existing milestone/quantity/scope tests remain regression evidence. |
| Actual independence; plan AC3/AC4; C3/C6 | Covered | Same-role positive cases and email/staff-code/OID aliases, stable snapshots, fail-closed legacy lookup and each independent decision are required rather than role-only denial. |
| Unknown inputs and current matching; C2/C4; P01-T01/T02 | Covered | Missing budget/commitment/milestone must block clean matching; acceptance rechecks current inputs. No new accepted-evidence authority is invented or broader PRD acceptance claimed. |
| SQL atomicity and fresh authority; C5/C6; P01-T02/P02-T01 | Covered | Existing writer transaction and rowversions retained; actor/independence rechecked at save, role/OID change without case-sequence change tested, pending success audit discarded on errors. |
| JSON rollback; plan NFRs/AC5; P02-T01 | Partial | In-memory restoration and crash limitation are stated, but ordinary durable failure guarantees are not distinguished or explicitly tested, PC-001. |
| Budget, commitment and held disposition preservation; plan AC1/AC5 | Partial | Existing lifecycle retained and held HTTP coverage required; exact unchanged-ledger assertions are missing, PC-002. |
| Failing-first, reopen and concurrency; P01-T01/P02-T01 | Covered | Baseline failures before edits, reopen, error injection, separate SQL connections and transaction-boundary authority change are planned. JSON scope correction remains PC-001. |
| Ownership, locked targets and #90/#84 boundaries | Covered | Finance-private implementation, one SQL hook, exactly two possible new owned test files, no removals or signoff changes. |
| Ordered RPI, independent Review and correction gate; P02-T02 | Covered | One canonical Review, blockers corrected within two batches, execution separated from outcome, no repeat full Review and no operational approval claim. |
| Local-only validation and evidence limits; P02-T01 | Covered | Fictional fixtures, responsive loopback HTTP and cleanup; local isolated MSSQL conditional with skipped evidence disclosed, no cloud/application acceptance claim. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 1; Medium 1; Low 0.
* The candidate is credible in architecture and scope, but two test-contract
  gaps allow an implementation to claim acceptance without the exact durable
  and financial-state evidence the caller requires. Both are direct
  corrections within existing targets. Neither needs a human policy choice.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Distinguish ordinary JSON write rollback from the accepted crash limitation

* Related IDs: Plan Non-Functional Requirements and AC5; P01-T01, P01-T02,
  P02-T01; research C5/C6.
* Evidence: The plan promises JSON in-memory restoration but only explicitly
  promises SQL case/audit atomicity. Phase details P02-T01 puts error injection
  after a SQLite reopen instruction without identifying a JSON failure matrix.
  src/core/src/zava_forward/core/finance.py currently calls audit before save.
  src/core/src/zava_forward/core/store.py audit immediately appends a durable
  entry and advances last_hash; save writes/replaces the separate data file.
  Thus restoring an in-memory case alone cannot undo a success event after an
  ordinary save failure. The supplied change_provenance operation has a
  different JSON ordering and restoration path, so actor reuse alone does not
  establish the desired guarantee.
* Concern: The planned crash caveat could conceal a reproducible caught
  save/audit failure, rather than only an abrupt process/filesystem crash.
  The candidate does not explicitly require JSON reopened state, persisted
  success-audit absence and audit-chain continuity together after these errors.
* Impact: A refused finance approval/disposition could leave a durable success
  event or mismatched state despite passing SQLite rollback tests and restoring
  the visible in-memory object.
* Smallest useful change: Add a JSON-specific ordinary-exception contract to
  the existing tasks: inject save failure and audit failure, including a
  controlled failure after a completed write where applicable; compare
  in-memory and reopened financial state, durable success-event delta and
  subsequent ledger integrity. Require finance-owned recovery for caught
  failures, explicitly separating any unavoidable abrupt-crash limitation.
  Keep the correction in finance.py and the locked finance test file; do not
  expand Store, schema or the change budget.
* Action owner: Planning parent for the plan/detail correction; finance
  implementer for failing-first proof and recovery.
* Exact resolving evidence: Updated P01-T01/T02 and P02-T01 name JSON save/audit
  failure cases and expected state/audit invariants. Subsequent implementation
  evidence records failing-first and passing results in
  src/core/tests/test_finance_match_controls.py for unchanged in-memory and
  reopened state, no failed-operation success event, and a valid subsequent
  audit chain. SQLite transaction tests remain separately identified.
* Decision route: Direct planner correction; no user response. This does not
  require cross-file crash atomicity or a new persistence model.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Require explicit ledger invariance for record-only status and held decisions

* Related IDs: Exact no-payment/preservation criteria; plan AC1, AC3 and AC5;
  P01-T01 and P02-T01; research C1/C7/C8.
* Evidence: Plan AC1 expressly requires no execution call or cash/grant
  mutation, but P01-T01 lists identity, line, stale-match and transaction cases
  without the no-payment invariants. P02-T01 asks to verify held/unknown and
  record-only status over HTTP without naming unchanged ledgers.
  src/core/tests/test_finance_signoffs.py
  test_clean_invoice_matches_but_payment_is_never_executed checks the displayed
  status/note and audit action names; it does not assert absence of financial
  ledger mutation or external execution. Its grant isolation test exercises
  grant-to-finance isolation, not finance-status-to-grant/cash isolation.
* Concern: The planned tests could preserve a record-only label while allowing
  an unintended budget, commitment or grant/cash mutation. They also do not
  explicitly demand that refused held acceptance/status actions retain the
  hold and prior disposition after reopen.
* Impact: A result could satisfy superficial status/HTTP assertions without
  proving the caller's nothing-paid and preservation criteria.
* Smallest useful change: Add an explicit before/after invariant matrix to
  the two existing test tasks, owned by the locked new finance test files.
  Exercise permitted external status notes through Paid outside this system;
  require approved budget/commitment and existing grant/cash records unchanged
  while allowing the intended invoice fields/audit. Exercise held acceptance
  and non-payable status refusals and Keep on hold followed by permitted
  independent disposition; require the appropriate hold/disposition to
  persist. Assert exact HTTP refusal/success and reopened state. Use existing
  side-effect seams as fail-on-call sentinels where available; do not introduce
  a banking adapter merely to test that none exists.
* Action owner: Planning parent for the explicit matrix; finance/API test
  owner for runtime and persistence evidence.
* Exact resolving evidence: P01-T01 and P02-T01 identify these scenarios and
  permitted versus forbidden field deltas. Implementation evidence maps them
  to src/core/tests/test_finance_match_controls.py and
  src/api/tests/test_finance_match_api.py with before/after comparisons of
  budget, commitments, grant/cash, hold and disposition, persisted audit and
  exact HTTP outcomes. Any absent external-execution seam is disclosed;
  labels or audit action names alone are not treated as no-payment proof.
* Decision route: Direct planner correction; no human decision, new authority,
  new file or signoff/procurement change.

## Strengths and Residual Risk

* Identity is not reduced to roles: the candidate explicitly covers actual
  same/different staff, same-role approvals, email/code/OID aliases, legacy
  preparer lookup and fresh transaction-time independence.
* The proposed SQL hook reuses existing transactions and rowversion conflicts
  instead of replacing shared infrastructure. Its #90 overlap is disclosed;
  #84 remains a regression boundary, not implementation scope.
* Broader contract/home allocation and accepted-evidence authority are
  explicitly not established. That limitation must remain visible; this
  critique does not authorize inventing a milestone authority model.
* Local MSSQL may be unavailable and JSON separate-file abrupt-crash
  atomicity is not promised. These are disclosed validation/design boundaries,
  not permission to waive the ordinary failure proof in PC-001.

## Questions or Blocking Evidence Gaps

* No decision-critical human question. Both findings block implementation
  handoff until the planning parent records concrete corrections.
* If a correction cannot fit the locked targets/budget or two correction
  batches, stop and report that blocker; do not silently broaden scope or
  convert missing proof into an accepted outcome.

## Limitations

* No tests, application services, local MSSQL, network research, private data,
  Azure or paid AI were executed. Research baseline test results remain
  supplied evidence, not fresh execution by this critique.
* GitHub issue/dependency statements are assessed from the supplied research
  and caller direction, not independently refreshed.
* Coverage assesses plan readiness, not implementation correctness, full PRD
  acceptance, real human independence verification or operational adoption.
* Only this critique artifact was written. Existing untracked candidate and
  session artifacts were not moved, committed or edited.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Record both direct dispositions and revise existing
  task acceptance evidence in one bounded correction batch, then finalize
  planning without another critique. Proceed to P01 only when both blockers
  have objective planned resolving evidence.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/finance-match-controls-94-plan.md](.copilot-tracking/plans/2026-10-17/finance-match-controls-94-plan.md) | Exact assessed candidate |
| [.copilot-tracking/details/2026-10-17/finance-match-controls-94-phase-details.md](.copilot-tracking/details/2026-10-17/finance-match-controls-94-phase-details.md) | Exact assessed task details |
| [.copilot-tracking/research/2026-10-17/finance-match-controls-94-research.md](.copilot-tracking/research/2026-10-17/finance-match-controls-94-research.md) | Supplied evidence and scope decisions |
| [.copilot-tracking/reviews/plans/2026-10-17/finance-match-controls-94-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/finance-match-controls-94-plan-critique.md) | Complete one-pass findings |

## Next Steps

The active planning parent directly resolves PC-001 and PC-002 within the
existing ownership and correction limits, records their dispositions and
continues the authorized ordered RPI only after the planning gate clears.
Do not invoke another critique or request another user authorization. This
worker stops here; implementation, independent Review and final-push delivery
belong to the parent.
