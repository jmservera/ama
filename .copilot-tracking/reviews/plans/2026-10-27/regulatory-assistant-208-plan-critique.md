---
title: Regulatory Assistant 208 Final-Candidate Plan Critique
description: Independent assessment of the bounded synthetic completion plan
ms.date: 2026-10-27
---

## Metadata

* Task ID: 208
* Task slug: regulatory-assistant-208
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/regulatory-assistant-208-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/regulatory-assistant-208-phase-details.md
* Critique execution status: Complete
* Assessment: One independent final-candidate critique, one complete actionable finding set.

## Inputs and Criterion Boundary

* Read the canonical research, plan and phase details named above, the original
  case study, relevant addendum context, reference index and owner memory.
* Checked the supplied evidence pointers against existing regulatory chat,
  privacy, chat repositories, audit storage, deterministic engine, comparator,
  API status endpoint, chat UI, browser harness and regulatory chat tests.
* Checked BRD FR-051/AC-099/OD-50, PRD FR-060/AC-104 to AC-106/OQ-026,
  and ADR 0005's synthetic-development and operational authority boundaries.
* Requirements considered: ordered RPI for #208 and #214/#216/#215/#217;
  src-only executable changes; local constructed data; no paid calls, Azure,
  private data, secrets or uv; no invented human decisions; exactly one
  post-implementation independent Review.
* The independent slice is automatic conflict referral, content-free offline
  consumption, Unknown costs, existing UI and evidence. Full issue acceptance,
  legal interpretation, actual appointments, privacy approval, staff value and
  operational use are not deliverable through this slice.
* The test ownership, zero removals, maximum 20 added methods, generated target
  and historical-output restrictions are accepted constraints, not suggestions
  to broaden. Proposed validation additions below can extend or parameterize
  the locked existing tests.
* Publication remains blocked by the caller's exclusion of the mandatory full
  gate. This critique does not recommend a waiver, protection change, alternate
  publication path or unauthorized execution.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #214; C5/C6; P01-T01 | Partial | Shared transaction/referral extraction is appropriate; authorization and retry boundaries need explicit contracts, PC-003/PC-004. |
| P01 atomicity and rollback acceptance | Partial | SQL and JSON boundaries are distinguished, but failure semantics and real commit validation remain incomplete, PC-002/PC-005. |
| #214/#217; C7-C10; P01-T02 | Partial | Content-free zero-inference accounting is credible; metadata query work is not bounded, PC-001. |
| #216; C8; privacy and role isolation | Partial | Simulated admission and unknown retention are preserved; transactional reauthorization needs resolution, PC-003. |
| #217; P02-T01 | Covered for slice | Independent frozen oracle, negative controls, Unknown cost inputs and cards_only remain appropriate. No actual accepted-check denominator or staff value is asserted. |
| #215; P02-T02 | Covered for slice | Existing native controls, plain mode, stored receipt restoration and pinned browser harness are appropriate; no WCAG or comprehension acceptance is claimed. |
| P03-T01; test ownership/budget | Partial | Relevant suites and regression escalation are planned; true commit-path and retry cases must be assigned within the existing budget. |
| Full #208/#214/#216/#215/#217 acceptance | Partial | Broad human blockers are named; supplied artifacts lack a criterion-level disposition, PC-006. |
| #440 and publication dependency | Covered as blockers | Neither synthetic evidence nor a scoped gate is represented as whole-epic or publication acceptance. |

## Verdict

* Verdict: Revise
* Severity summary: 2 High, 4 Medium, 0 Critical, 0 Low.
* Rationale: The proposed slice is coherent and properly restricted, but the
  implementation contract leaves material storage, authorization and read-cost
  behavior underspecified. All six findings are direct planner corrections
  within the authorized slice. None requires guessing a human decision.
* Full-issue acceptance and publication remain separately Blocked; this verdict
  does not replace those blockers or require an additional critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Zero inference does not bound usage-query work

* Related IDs: P01-T02, P02-T02, content-free current-role/day aggregation.
* Evidence: The phase details require metadata-only aggregation but give no
  query interface, traversal bound or incomplete-result contract.
  src/core/src/zava_forward/core/sqlstore.py audit_entries fetches the complete
  ledger before yielding, including other actors' detail values.
  src/core/src/zava_forward/core/store.py audit_entries traverses the file
  ledger. The existing SQL audit index is case/sequence, not actor/day.
  src/core/src/zava_forward/core/regulatory_chat.py privacy_status also lists
  all own threads. The UI calls the status endpoint when opening the panel.
* Concern: The obvious reuse of audit_entries performs all-history work before
  filtering user, role and day. A hard zero model allowance does not constrain
  SQL/file I/O, memory or repeated browser status reads. Output isolation alone
  does not prove that the metering path avoids materializing unrelated detail.
* Impact: An apparently cheap panel status read can scale with the entire
  shared audit history and unnecessarily handle unrelated audit content.
* Smallest useful change: Specify a dedicated metadata read boundary, trusted
  actor/action/time filtering, finite work/result limits and truthful
  incomplete/unmetered status when exact totals cannot be obtained within those
  limits. Keep SQL/file strategies explicit and compatible with the no-schema
  constraint. Do not fetch message content or silently return a capped count
  as an exact daily total. Do not turn the read bound into an intake limit.
* Action owner: Planning parent, P01-T02 implementer.
* Exact resolving evidence: Revised P01-T02 names the bounded read algorithm
  and completeness response; parameterized tests seed unrelated actors, roles,
  days, historic unmetered records and more records than the work bound.
  Assertions reject generic all-ledger/message reads on the SQL path, establish
  the file traversal limit, and prove exact versus incomplete status honestly.
* Decision route: Direct planner correction. No paid budget, schema expansion
  or user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: JSON audit failure needs an explicit committed-state contract

* Related IDs: P01-T01, P01-T02, P03-T01, atomic referral acceptance.
* Evidence: The details correctly preserve the separate JSON file-ledger
  boundary. Existing regulatory_chat.ask/doubt append JSON audit after saving
  chat state. In src/core/tests/test_regulatory_chat.py,
  test_json_post_commit_audit_error_is_not_misreported_as_rollback proves a
  raised audit error can coexist with a durable inbox and receipt.
* Concern: The plan says missing insertion, audit and commit are validated,
  but does not state what automatic ask or usage status means when JSON chat
  commits and the subsequent audit append fails. Restoring an in-memory
  preimage at that point would not roll back the file and must not be used as
  proof of failure atomicity.
* Impact: The browser may report an unsuccessful lookup despite a durable
  referral; consumption can be missing even though the turn exists. A blanket
  no-partial-state claim or exact usage count would be false.
* Smallest useful change: Define the JSON post-commit audit-failure outcome
  separately from pre-commit rollback and SQL audit rollback. Preserve durable
  referral/receipt state, state the missing-metering limitation, and specify how
  the existing history/manual route recovers the committed result. Do not add a
  cross-file atomicity promise or redesign storage.
* Action owner: Planning parent, P01 implementer.
* Exact resolving evidence: Acceptance wording and details distinguish the
  three failure boundaries; extend the existing JSON audit-failure test to the
  automatic conflict path, reopen the store, verify one complete referral and
  receipt, verify no false rollback claim, and verify honest metering status.
* Decision route: Direct planner correction consistent with the already
  accepted separate-file boundary.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Make authorization rechecks part of the referral transaction

* Related IDs: P01-T01, current-principal/role NFR, stale-role acceptance, #216.
* Evidence: The plan says to recheck the current principal and role.
  The details resolve/admit the owner before mutation but only explicitly
  recheck thread state/version inside the transaction. Existing
  regulatory_chat.ask and doubt admit the sender before entering the write
  transaction; doubt also resolves the owner before it. The rowversion check
  does not validate staff provisioning, current role or current case access.
* Concern: A sender or owner revoked or reassigned after the initial check
  could still reach the new automatic write unless admission and owner
  projection are revalidated at the locked transaction boundary. Existing
  stale-role tests change roles before invoking the operation, not between
  admission and persistence.
* Impact: The new automatic route could persist evidence to a stale owner-role
  inbox or accept a now-ineligible sender. This undermines the slice's specific
  isolation promise even though initial-request authorization is correct.
* Smallest useful change: Require fresh sender provisioning/role, thread
  owner-role, named owner provisioning/role and case-projection checks inside
  the existing transaction/lock, before any mutation. Preserve trusted-proxy
  role authority and do not substitute a database role for a currently trusted
  authenticated role. Name the local concurrency boundary being guaranteed.
* Action owner: Planning parent, P01-T01 implementer.
* Exact resolving evidence: Revised task sequencing plus parameterized tests
  that revoke/change sender and owner or case access after initial admission
  but before the transaction's final check; JSON and SQLite leave no turn,
  inbox, receipt or SQL audit delta. Ordinary permitted routes still pass.
* Decision route: Direct planner correction; no real Entra provisioning or
  company appointment is requested.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: State what a retry identifies before promising no duplicates

* Related IDs: P01-T01, no-duplicate-inbox functional requirement, UI routing.
* Evidence: The plan promises no duplicate inbox on retry. Details only specify
  preserving manual selected-turn idempotency and testing a subsequent manual
  doubt. Existing ask accepts a question without a request identifier and
  appends a new pair each time; doubt deduplicates by referred_turn stored in a
  receipt. These are different retry units.
* Concern: The plan does not distinguish automatic/manual referral of one
  stored turn from replaying a successful ask after its response is lost.
  The latter currently creates a different stored turn and could create a
  second automatic inbox. Identical question text is not a safe dedupe key.
* Impact: Implementer and reviewer could disagree about whether the central
  idempotency criterion has passed, particularly after PC-002's failure path.
* Smallest useful change: Define idempotency as exactly one referral per stored
  source-thread/assistant-turn identity and document that a new ask is a new
  turn, not an idempotent replay. If broader HTTP ask retry safety is claimed,
  specify a stable request identity and its persistence instead; do not imply
  the selected-turn receipt already provides that guarantee.
* Action owner: Planning parent.
* Exact resolving evidence: Plan/details consistently name the retry unit;
  existing tests prove automatic routing followed by repeated manual referral,
  history restoration and stale-version/concurrent retry cannot duplicate that
  turn's inbox. A separate repeated-ask assertion records the chosen boundary
  without deduping legitimate equal-text questions.
* Decision route: Direct planner correction to bound the slice's existing
  promise. No broader retry feature is required by this finding.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Test the actual SQL commit boundary, not its no-op hook

* Related IDs: P01-T01, P01-T02, P03-T01, write/commit failure acceptance.
* Evidence: src/core/src/zava_forward/core/chatthreads.py SqlRepo.commit is a
  no-op; SqlRepo.txn executes COMMIT when its context exits. The existing
  test_pair_and_handoff_commit_failures_preserve_reopened_state patches
  chat_repo.commit, so its SQL branch raises before the real COMMIT attempt.
  Details require commit failure validation without identifying this difference.
* Concern: Reusing that test unchanged would establish pre-commit exception
  rollback, not failure of SQL transaction finalization.
* Impact: The strongest atomicity acceptance claim could be supported by a
  misleadingly named test while the real failure boundary remains untested.
* Smallest useful change: Assign a real transaction-finalization failure
  injection in the existing SQL test, alongside JSON save/replace failure and
  message/audit insertion failures. Keep a failure before COMMIT takes effect
  distinct from an acknowledgement lost after successful commit; do not claim
  either test proves both.
* Action owner: Planning parent, P03-T01 test owner.
* Exact resolving evidence: An extended parameterized canonical test records
  that the SQL COMMIT statement was actually attempted and failed before
  commit, then verifies reopened sender/inbox/receipt rows, usage audit,
  audit_head and ledger integrity equal their preimages. Existing success and
  restart assertions remain. Test additions stay within the locked budget.
* Decision route: Direct planner correction, no new infrastructure required.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Bring criterion-level issue disposition into the plan boundary

* Related IDs: #208/#214/#216/#215/#217, C1-C10, P03-T01 acceptance reconciliation.
* Evidence: Research says the actual gh issue views were read and requires every
  criterion to be evidenced or explicitly unproven, but supplies no
  criterion-by-criterion issue inventory. The plan cites issue numbers and
  defers the explicit unmet matrix to P03. BRD/PRD rows are available, but are
  not substitutes for the issues' potentially additional tokenomics, privacy,
  evaluation and human acceptance clauses.
* Concern: A reviewer cannot verify from the supplied final-candidate artifacts
  that every requested issue clause is allocated to existing evidence, this
  implementation or an explicitly named blocker.
* Impact: Slice success could omit a non-human engineering criterion while
  correctly refusing full issue closure. General statements that human gates
  remain unmet do not establish completeness of the ordered delivery scope.
* Smallest useful change: Add the issue criterion disposition to the existing
  plan/details using the parent's already retrieved issue evidence, without
  changing issue checkboxes. Give each clause an issue-local identifier,
  disposition, evidence/test pointer or missing decision, and responsible owner.
  Distinguish existing functionality not freshly tested from fresh evidence.
* Action owner: Planning parent.
* Exact resolving evidence: A complete matrix for all five named issues,
  including #440 as epic dependency, maps each clause to an existing artifact,
  P01/P02/P03 task and planned check, or an explicit unmet condition. No
  threshold, appointment, retention approval or actual staff result is invented.
* Decision route: Direct planner correction. Gathering missing real human
  evidence remains a later blocker, not a prerequisite to this matrix.

## Strengths and Residual Risk

* Extracting a shared referral writer avoids nested SQL transactions and
  preserves manual selected-turn routing. Copying stored evidence rather than
  reretrieving it is appropriate.
* Zero model-call/token counters describe the actual offline path without
  creating financial authority or an urgent-intake quota.
* Unknown monetary cost, missing price/billing/allocation/review-effort inputs
  and the absent accepted-check denominator are correctly kept explicit.
* Frozen independently authored expectations and forged-metadata mutations
  complement, rather than replace, persistence/HTTP/browser tests.
* No source activation, rule suppression, real appointments, privacy disposal
  or operational acceptance is inferred. Historical retention records and
  unmetered records remain explicitly limited.
* The 60,000-home report is stateless constructed evidence, not continuing
  stock, actual model performance, legal grading or staff comprehension.
* UI changes are restricted to the existing Fluent/native panel and scoped
  browser checks. Missing axe execution must remain visible, not a pass.
* Original adverse results and the single independent Review outcome remain
  preserved. Publication is blocked, not bypassed by a scoped check.

## Questions or Blocking Evidence Gaps

* No user question is required to correct these six planning findings.
* Actual Legal/Compliance/DPO appointments, retention periods, real Entra
  assignments, agreed thresholds and staff comparison remain intentionally
  unavailable. They block full acceptance, not independent synthetic work.
* No legitimate reconciliation of the mandatory publication gate is supplied.
  Stop before publication while that conflict remains; do not execute --all.

## Limitations

* This was a read-only plan/interface assessment, not implementation Review or
  test execution. No current behavior was independently executed or certified.
* Actual issue bodies are not reproduced in the supplied artifacts and were
  not independently refreshed. PC-006 identifies that traceability limitation
  rather than inventing additional issue requirements.
* No external legal currentness, hosted checks, private data, live identity,
  Azure, paid service or human acceptance evidence was obtained.
* Only this critique artifact was authored; plan, details, research and source
  files remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define bounded usage-read and completeness semantics in
  P01-T02, then dispose PC-002 to PC-006 directly in this same planning pass.
* User response required: No for these revisions. Human acceptance and
  publication remain blocked separately.
* No second critique is requested. Preserve this original Revise verdict and
  record each disposition before the authorized implementation and one Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/regulatory-assistant-208-research.md](.copilot-tracking/research/2026-10-27/regulatory-assistant-208-research.md) | Canonical research and evidence boundary |
| [.copilot-tracking/plans/2026-10-27/regulatory-assistant-208-plan.md](.copilot-tracking/plans/2026-10-27/regulatory-assistant-208-plan.md) | Reviewed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/regulatory-assistant-208-phase-details.md](.copilot-tracking/details/2026-10-27/regulatory-assistant-208-phase-details.md) | Reviewed task and validation details |
| [.copilot-tracking/reviews/plans/2026-10-27/regulatory-assistant-208-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/regulatory-assistant-208-plan-critique.md) | Original independent critique |

## Next Steps

The active planning parent should apply the six compatible planner-owned
corrections and record resolving evidence without another critique pass.
No user action is required for those corrections. Continue only the authorized
local synthetic RPI stages; retain full-issue, operational and publication
blockers. This critique task stops after this artifact.
