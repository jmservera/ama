---
title: Issue 130 PR 509 fix cycle 1 plan critique
description: Independent final-candidate assessment of the two proposed resident intake corrections
ms.date: 2026-10-29
---

## Metadata

* Task ID: issue-130-pr-509-fix-cycle-1.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/safety-consent-130-fix-cycle-1-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Read the exact supplied research, plan and phase details, including research
  C1-C7, all six acceptance criteria and P01-P03.
* Read the relevant supplied source and shared tests to assess decision
  semantics, nomination allocation, retention deletion, persistence, rollback
  and existing tombstone compatibility. Repository context included the
  original case study, addendum, reference index and owner memory.
* Caller direction controls the boundary: matching open docs/safety-consent-130
  branch and completed rebase are supplied context; runtime source stays in
  src/, tests outside packages, Refs only, local commit with required trailer,
  no Azure, latest.json edit, push or remote changes.
* Preserve all decision, tenure, authority, retention, privacy and manual
  safeguards. Preserve sequential NOM IDs and at most three added shared
  JSON/SQLite regression methods, removing none.
* This assesses implementation readiness, not implemented behavior, test
  success, issue closure, operational acceptance or publication readiness.
  No implementation, tests, commits, further agents or remote operations were
  performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Accepted status and exact heuristic preservation; C1-C2; AC1 | Covered | Decision-only helper removes the tenure dependency from status without changing the heuristic. Exact output and an ordering-sensitive competitor are specified. |
| Case/scoped tenure and decision safeguards; AC2; P01-T02 | Covered | Tenure fast-path stays in resident_gate; retention, current scope, review and representative checks move unchanged. |
| New deletion/recreation identity; C3-C4; AC3 | Partial | Cumulative deletion count works for complete post-change history, but does not recover an already-deleted legacy identity: PC-001. |
| Repeated/empty deletion and legacy compatibility; C7; AC4 | Partial | Repeated and empty-ledger accumulation are explicit. Missing legacy count is incorrectly treated as evidence of zero previous IDs: PC-001. Existing metadata assertion also needs reconciliation: PC-003. |
| Transaction/replay/rollback; P01-T01/P01-T02 | Partial | Nomination commands use _operation, but retention deletion does not. No deletion-counter fault regression is specified: PC-002. |
| Shared tests, no removals, at most three added methods | Covered with corrections | Existing inheritance supplies JSON/SQLite coverage. Findings can be covered within three added methods and a narrow existing assertion update. |
| Static checks and relevant modules; AC5; P02-T01 | Partial | Checks and honest skip reporting are explicit, but the specified tool location violates the execution environment restriction: PC-004. |
| Documentation, Review, evidence and local commit; AC6; P02-P03 | Covered | Existing README section, retained original outcomes, independent Review, attribution/trailer and no-push limit are explicit. Failed validation or material Review findings block completion. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 3 Medium, 0 Low.
* The status correction is credible and the cumulative counter is suitable for
  histories tracked from their first allocation. The unconditional legacy-zero
  fallback does not satisfy the promised stale-correction protection. The
  deletion persistence assumption and executable validation details also need
  direct correction before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Legacy-zero fallback can immediately reuse a deleted identity

* Related IDs: C3, C7, functional requirements, AC3-AC4, P01-T01, P01-T02.
* Evidence: src/core/src/zava_forward/core/resident_decisions.py:620-638
  currently removes nomination_records and retains only a contact count.
  Allocation at line 664 is length-based; correction at lines 692-694
  binds the resulting ID and version. The plan explicitly defaults legacy
  tombstones without the new count to zero.
* Concern: A pre-change deletion of NOM-1 leaves no nomination ledger and a
  tombstone without a nomination count. The planned formula then yields
  0 + 0 + 1 = NOM-1, version 1. An old correction for NOM-1/version 1 can
  therefore match the new intake again when its owner remains authorized.
  Deleting a currently retained legacy NOM-1 under the new code is a different
  scenario and does not prove this migration boundary.
* Impact: AC4 and the unqualified deleted-identity protection remain false for
  a supported legacy state. Missing history is treated as a verified zero.
* Smallest useful change: Distinguish never-deleted cases from cases with
  pre-existing deletion evidence and an unknown nomination high-water mark.
  Specify a trustworthy non-personal high-water reconciliation, or refuse new
  nomination issuance in that ambiguous legacy state until it is reconciled.
  Preserve sequential NOM IDs; do not silently reset an unknown history.
  If historical identifiers cannot be recovered, state that limitation rather
  than claiming the counter reconstructs deleted history.
* Action owner: Planning parent.
* Exact resolving evidence: Revised legacy rule in the plan/details and a
  shared regression starting from an already-deleted legacy state with only
  contacts_before_deletion and no ledger/count. A prepared old
  NOM-1/version-1 correction must never mutate a replacement record or audit;
  issuance must either use a proven non-reused sequential ID or be explicitly
  refused pending reconciliation. Retain the planned repeated/empty-cycle and
  valid-new-correction assertions within the three-method limit.
* Decision route: Direct planner correction. Do not waive identity protection
  or switch ID contracts; either would require a separately authorized user
  decision, not an assumption in this plan.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The new deletion counter lacks an established rollback boundary

* Related IDs: Non-functional transaction requirement, C5, P01-T01, P01-T02.
* Evidence: src/core/src/zava_forward/core/resident_decisions.py:388-460
  provides _operation rollback for resident_action commands.
  delete_resident_records at lines 620-642 instead mutates, audits and saves
  directly under the store lock. src/core/src/zava_forward/core/doc_controls.py:276-280
  delegates directly to it. src/core/src/zava_forward/core/store.py:102-114
  persists JSON and audit separately; SQL save/lock cleanup is implemented in
  src/core/src/zava_forward/core/sqlstore.py:629-645,668-780.
* Concern: "Use existing case transaction/replay" is not a demonstrated
  deletion guarantee. Existing intake failure tests exercise nomination and
  tenure commands, not the deletion that will maintain the cumulative count.
  A deletion audit/save failure may have different local, durable and audit
  outcomes; the plan supplies no counter-specific fault/retry assertion.
* Impact: The identity invariant relies on the counter and ledger deletion
  agreeing after failure, reload and retry, not only after successful saves.
  Intake rollback coverage alone cannot establish that invariant.
* Smallest useful change: Specify the actual deletion persistence boundary and
  add a bounded failure/retry matrix for the new counter and ledger. Correct
  behavior tightly coupled to maintaining that invariant if the test exposes
  a mismatch; do not assume _operation already wraps deletion or undertake an
  unrelated store-wide transaction rewrite.
* Action owner: Planning parent.
* Exact resolving evidence: Plan/details name deletion as a separate boundary.
  One of the three allowed shared methods injects precommit audit/save failure
  around deletion, compares same-instance and reopened ledger/count/audit,
  retries from the resolved durable state, and proves no double accumulation,
  count reset or deleted-ID reuse. Nomination failure after a nonzero offset
  must likewise preserve the offset and next valid sequential identity.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Unconditional new tombstone metadata conflicts with an existing safeguard test

* Related IDs: C7, P01-T02, P02-T01, no-removal requirement, AC5.
* Evidence: src/core/tests/test_resident_decisions.py:1052-1089,
  test_deletion_tombstone_contains_only_boundary_metadata, compares the full
  tombstone to {"contacts_before_deletion": 1} after a deletion without
  nominations. P01-T02 directs adding the cumulative count to the tombstone.
* Concern: Unconditionally writing even a zero-valued nomination count fails
  this existing inherited JSON/SQLite assertion. The plan only describes added
  methods and does not reconcile this exact metadata contract.
* Impact: The proposed implementation can fail its required existing suite;
  weakening or removing this test casually would lose the non-personal
  tombstone safeguard.
* Smallest useful change: Explicitly choose either omission of a known-zero
  count where compatible with PC-001, or a narrow update to the existing
  expected metadata allowing the new integer count. Preserve all personal-data
  canary, field-removal and contact-prefix checks, and remove no method.
* Action owner: Planning parent.
* Exact resolving evidence: Plan/details identify the existing assertion and
  chosen representation; the existing shared metadata test passes with its
  privacy checks intact, alongside positive-count and empty-cycle assertions.
* Decision route: Direct planner correction.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Planned validation uses a prohibited tool location

* Related IDs: Research Brief, plan validation requirement, P02-T01, AC5.
* Evidence: The supplied research, plan and details repeatedly require tools
  under /tmp/mv. The current execution environment expressly prohibits file
  operations in /tmp and temporary directories.
* Concern: The proposed absolute executable paths cannot be used within that
  restriction. This critique did not inspect or execute them.
* Impact: P02-T01 is not executable as written; later reporting must not imply
  that those exact commands ran.
* Smallest useful change: Record the path conflict and use an allowed existing
  interpreter/tool environment or a repository-relative environment for the
  same Ruff, format, mypy and unittest checks. Keep scratch datasets and outputs
  in an allowed project-relative location. Preserve the missing-dependency-only
  installation rule and explicit reporting of unavailable checks.
* Action owner: Planning parent.
* Exact resolving evidence: Revised allowed command paths and scratch policy
  in the plan/details, followed by actual tool versions, command exits and
  test counts in the implementation changes artifact. No forbidden-path access
  or fabricated validation receipt.
* Decision route: Direct planner correction required by the execution boundary;
  no user response is needed to honor that restriction.

## Strengths and Residual Risk

* Extracting all existing non-tenure checks unchanged is appropriately scoped.
  resident_gate can retain its current fast-path and release protection while
  resident_status continues to represent current resident decisions.
* Exact heuristic output equality, citations and an ordering-sensitive
  competitor are stronger than merely checking a status label.
* Post-change cumulative deletion counts naturally preserve sequential IDs
  across successful repeated and empty-ledger deletion cycles, provided the
  previous count is retained and its unknown legacy boundary is handled.
* The plan preserves legal holds, tenure holds after payload deletion, named
  human ownership, non-digital routes, existing tests and privacy boundaries.
* Actual MSSQL, Azure, human/operational acceptance and publication/hosted gates
  remain explicitly unproven and outside this local correction.

## Questions or Blocking Evidence Gaps

* No unresolved user choice is required for the direct corrections above.
  There is no supplied historical nomination high-water evidence for an
  already-deleted legacy case; the planner must not invent it.

## Limitations

* Read-only source assessment, not an implementation review or executed
  regression result. No cloud, configured database, private dataset, GitHub
  inspection or fresh publication gate was used.
* Initial status showed the three supplied artifacts and the RPI state file as
  untracked. They were left untouched; this critique is the only file written.
* Matching PR lifecycle and completed rebase were accepted as caller context.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Replace unconditional legacy-zero allocation with an
  explicit safe legacy policy and its regression, then reconcile PC-002 through
  PC-004 in the same plan revision.
* User response required: No.
* No second critique is requested or authorized. Preserve this original Revise
  outcome and record the parent's dispositions.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/safety-consent-130-fix-cycle-1-research.md](.copilot-tracking/research/2026-10-29/safety-consent-130-fix-cycle-1-research.md) | Supplied focused research, C1-C7. |
| [.copilot-tracking/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan.md](.copilot-tracking/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-29/safety-consent-130-fix-cycle-1-phase-details.md](.copilot-tracking/details/2026-10-29/safety-consent-130-fix-cycle-1-phase-details.md) | Assessed task details. |
| [.copilot-tracking/reviews/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan-critique.md) | This single independent critique. |

## Next Steps

The active planning parent should revise directly against PC-001 through
PC-004, retain this original outcome and finalize without another critique.
No user action is required. This reviewer stops here without implementation,
commit, delegation or remote changes.
