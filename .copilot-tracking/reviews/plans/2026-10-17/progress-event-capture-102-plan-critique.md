---
title: "RPI Plan Critique: progress-event-capture-102"
description: Single final-candidate critique of prospective criterion-one event capture and transaction evidence
ms.date: 2026-10-17
ms.topic: reference
---

## Metadata

* Task ID: 102, progress-event-capture-102.
* Critique date: 2026-10-17.
* Plan: .copilot-tracking/plans/2026-10-17/progress-event-capture-102-plan.md.
* Phase details: .copilot-tracking/details/2026-10-17/progress-event-capture-102-phase-details.md.
* Critique execution status: Complete.
* Execution count: one final-candidate assessment; no additional workers,
  implementation, source edits or additional critique passes.

## Inputs and Criterion Boundary

* Caller requirements: criterion one only, covering prospective stage advance,
  return, reopen and supported pause boundaries; actual handoff offered,
  received and accepted; and independent per-measure quality acceptance and
  handover. Successful controlled transitions and their events must share the
  persistence outcome. SQL success audit must be exactly once after failed
  save, rollback, committed-refresh failure, retry and restart.
* Primary evidence: the supplied plan, phase details and
  .copilot-tracking/research/2026-10-17/progress-event-capture-102-research.md,
  including research conclusions C1-C7.
* Bounded corroboration: the source pointers supplied by C1-C7 in
  src/core/src/zava_forward/core/store.py, workflows.py,
  change_provenance.py, stock.py, quality.py, sqlstore.py and progress.py;
  existing progress and quality tests; and relevant repository context.
  Paths abbreviated in this sentence share the stated core source directory.
* Decisions retained: use existing histories and public domain methods,
  current registered fictional staff and writer-transaction identity checks;
  no new transition capability, history backfill, UI, API handler, service,
  finance or infrastructure changes. Retain #390 forecasts, authorized cohort
  and export roles, UTC/as-of semantics, source redaction and the mixed
  precision correction. Per-measure handover is not whole-home completion.
* Dependencies retained: #390 is the supplied merged base; #100 is hierarchy,
  not an invented blocker; parallel #88 quality overlap requires coordinator
  integration, and #391 remains excluded.
* Assessment covers P01-P03, their tasks, acceptance criteria, test ownership,
  failure boundaries, publication controls and explicit residual risks.
  It assesses implementation credibility, not completed behavior or acceptance
  of the wider issue. All current user requirements are treated as supplied
  and authoritative; none is reopened for negotiation.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Criterion one; C1; P01-T01 | Covered | The actual three stage writers are identified; supported pause entry/exit uses legitimate returns, with no generic resume or closure API invented. |
| C2-C3; P01-T01 | Covered | Existing handoff lifecycle, metadata-required offer/accept, expected handoff version and sender accountability are explicitly retained. |
| C5-C6; P01-T01 | Covered | Registered actor validation, independent quality decision scope, active-record replacement and staleness are retained rather than replaced by stage-based acceptance. |
| C6-C7; P01-T02 | Partial | Nested quality provenance is identified, but its report representation and supersession/as-of behavior are not fixed sufficiently to reconcile new measured evidence with the preserved schema; PC-001. |
| C7; P01-T02; existing audit trust contract | Partial | New quality-derived measurements are not explicitly included in the report's audit-integrity suppression and regression assertions; PC-002. |
| C4-C5; P01-T01; P02-T01 | Partial | Save/audit failure and second-writer post-COMMIT refresh are explicit. Failure during recovery I/O, where pending audit can escape at lock exit, lacks an explicit new-scope test obligation; PC-003. |
| C7; mixed precision; P01-T02 | Covered | Stage histories gain bounded legacy minute treatment; append/version order, uncertain periods, last-exit unknowns and no cross-stream ordering claim are explicit. |
| P02-T01; backend and guard acceptance | Covered with findings | Actual JSON, SQLite and isolated loopback MSSQL, genuine booking prerequisites, independent quality actors, source privacy and dependent guards are required; supplement only the specific gaps below. |
| Forecast/export roles; P01-T02; P02-T01 | Covered | Forecast algorithm, semantic CSV parity, role redaction and current authorized cohort semantics are preserved. PC-001 must not change those contracts. |
| P02-T02 | Covered | Direct component/KB documentation and image smoke are scoped; no browser or unrelated web work is introduced. |
| P03-T01; P03-T02 | Covered | One original Review, retained findings, at most two correction cycles, privacy-safe publication and Refs #102 are explicit; no merge, close or rewrite. |
| JSON cross-file crash limitation | Covered | The distinction between atomic case/event replacement and unavailable cross-file crash atomicity is disclosed, not promoted into a SQL-equivalent claim. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 2; Medium 1; Low 0.
* Rationale: the architecture and scope are credible. Three bounded omissions
  need explicit implementation and validation obligations: a quality projection
  contract, extension of the existing trust gate, and recovery-failure evidence
  for the newly shared operation scope. These are direct planner corrections,
  not reasons to expand scope or seek a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Fix the quality projection and historical replacement contract

* Related IDs: C6-C7; P01-T01; P01-T02; P02-T01; acceptance criterion for
  actual independent quality submit/accept/handover.
* Evidence: .copilot-tracking/details/2026-10-17/progress-event-capture-102-phase-details.md:22-38
  identifies nested quality event locators and requires preserving the schema,
  but does not name the output location or pairing/replacement rules.
  src/core/src/zava_forward/core/progress.py:313-321 currently returns only
  stage/handoff history structures; progress.py:459-488 retains an unknown
  whole-home actual denominator and stage/handoff-only definitions and sources.
  src/core/src/zava_forward/core/quality.py:210-220 supersedes prior records,
  clears their current acceptance/handover fields and retains their histories.
* Concern: a report consumer cannot safely choose current active_records or
  current acceptance fields to answer historical as-of queries. Nor should
  acceptance from one evidence version pair with handover from another.
  The plan's general requirement to consume exact dictionaries does not settle
  the new projected shape, source identity, or what happens to an earlier
  observed pair when a later supersession exists.
* Impact: an implementation can capture every event yet omit the required
  measured quality evidence, accidentally join replacements, or make an earlier
  historical answer depend on a future replacement. Free-text checklist/source
  details could also escape if the output shape is left implicit.
* Smallest useful change: in P01-T02, specify the quality event/interval
  representation within the existing report contract, with stable internal
  record-index/evidence-version/history-version locators and redacted source
  status. Pair acceptance and handover only within the same evidenced record
  and valid append sequence. Apply as-of and period rules to these histories
  before evaluating supersession; later events must not rewrite an earlier
  answer. Distinguish historical observed pairs from current valid acceptance
  and keep accepted_handover_actuals unknown at whole-home level. State how
  unversioned legacy prefixes and malformed/contradictory quality boundaries
  remain unknown without synthesizing old events. Preserve progress/v1's
  existing fields, forecast behavior and semantic CSV serialization.
* Action owner: planning parent for the contract; implementer for P01-T02 and
  P02-T01 evidence.
* Exact resolving evidence: revised P01-T02 identifies the output shape,
  pairing key and temporal rules; the owned tests use actual public quality
  methods to produce two evidence versions, compare an as-of before and after
  supersession, show no cross-version pairing, preserve legacy missingness,
  and assert redacted JSON/CSV parity and an unchanged whole-home denominator.
  Use current-time prospective events and controlled test clocks, not
  backfilled production history.
* Decision route: direct planner correction. The caller already requires
  as-of preservation, independent quality evidence and no snapshot inference;
  no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Extend audit-integrity suppression to quality-derived measurements

* Related IDs: C7; P01-T02; P02-T01; preservation of existing report truth.
* Evidence: src/core/src/zava_forward/core/progress.py:439-449 explicitly
  nulls elapsed_seconds and marks intervals Untrusted only in stage_intervals
  and handoff_waits when audit integrity is false or unknown.
  .copilot-tracking/details/2026-10-17/progress-event-capture-102-phase-details.md:31-38
  adds quality consumption but does not identify this trust-gate extension;
  its P02-T01 likewise does not require a quality-specific untrusted report
  assertion.
* Concern: adding another quality interval collection without extending the
  enumerated gate leaves its numeric durations available inside a report
  otherwise labelled Untrusted. This is an anticipated integration risk in
  the plan, not a claim that unimplemented quality reporting already has
  that defect.
* Impact: callers or exports could treat quality-derived durations as observed
  evidence despite an unverifiable or failed audit ledger, weakening the
  existing fail-closed reporting contract.
* Smallest useful change: add an explicit P01-T02 obligation to apply the
  existing audit-integrity false/unknown policy to every new quality-derived
  measured interval or summary, using the existing null/Untrusted convention.
  Add focused assertions in P02-T01. Do not redesign ledger verification or
  add a service.
* Action owner: planning parent for the explicit obligation; implementer for
  the report gate and owned tests.
* Exact resolving evidence: revised details name the new quality projection
  in the trust gate; an actual independently accepted and handed-over measure
  has a known duration under audit_intact=True, but no trusted numeric quality
  duration under either False or None. Assert the same semantics after CSV
  serialization, while existing stage/handoff behavior and role filtering
  remain unchanged.
* Decision route: direct planner correction; no user response required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Prove failed recovery cannot flush a failed transition's audit

* Related IDs: C4-C5; P01-T01; P02-T01; exact-once SQL audit acceptance.
* Evidence: .copilot-tracking/details/2026-10-17/progress-event-capture-102-phase-details.md:17-26,53-55
  requires a shared controlled scope, save/audit failures and a post-COMMIT
  sync fault, but does not require failure of recovery reads themselves.
  src/core/src/zava_forward/core/sqlstore.py:513-543 flushes remaining pending
  audit on outer lock exit; sqlstore.py:631-645 quarantines pending work before
  recovery I/O. src/core/src/zava_forward/core/change_provenance.py:113-136
  is an existing recovery/rejection path that the new shared scope must handle
  truthfully. src/core/tests/test_quality_procurement.py:807 provides an
  existing recovery-read-failure test precedent, distinct from its
  test_quality_sql_postcommit_refresh at line 635.
* Concern: save failure alone does not exercise the dangerous combination of
  a failed write and failed recovery I/O. Passing existing quality regressions
  does not demonstrate this property for new stage and non-metadata handoff
  callers or the altered offer/accept operation path. A pending success audit
  can otherwise survive until _finish even though its state/event rolled back,
  or recovery can replace the original error.
* Impact: this directly threatens the requested exact-once SQL audit contract:
  success audit without its event, lost legitimate prior audit, or an ambiguous
  failure on retry/restart.
* Smallest useful change: add a bounded SQL fault matrix to P02-T01 for the
  new shared scope and its metadata-backed path. Queue a legitimate prior
  audit, fail save/case-write/audit-insert before COMMIT, and fail recovery
  readback too. Assert pending quarantine before outer lock exit, preservation
  of the original error and prior audit, durable absence of the failed
  transition/event/success audit, and exactly one success after a clean retry.
  Retain the separately planned second-writer post-COMMIT case, which must
  report committed outcome rather than rejection. Use parameterized subtests
  within the existing 24-method limit and task-owned SQL backends.
* Action owner: planning parent for the matrix and expected outcomes;
  implementer for shared-scope handling and test evidence.
* Exact resolving evidence: revised P02-T01 names the combined recovery fault
  and caller families. Actual SQLite and loopback MSSQL runs show counts and
  hash-chain integrity through outer lock exit, independent connection,
  retry and reopened store; the legitimate prior entry remains once and failed
  success entries remain absent. The committed-refresh companion shows its
  event and success audit once, no rejection claim for that committed action,
  and a refused duplicate retry without another success event/audit.
* Decision route: direct planner correction. This tightens evidence for the
  caller's existing atomic/exact-once requirement; it introduces no broader
  persistence or infrastructure scope.

## Strengths and Residual Risk

* Research correctly limits capture to real writers rather than inventing
  progression capabilities or deriving clocks from stage_since, current
  snapshots, prose or closure.
* Append/version order and the mixed-precision legacy correction are explicit.
  Pause exits and final-stage exits remain unknown where no real boundary
  exists; no advice here authorizes inferred duration.
* Metadata-required handoff offer/accept and actor revalidation are preserved.
  Quality independence, replacement staleness, resident and safety controls
  remain separate from progression reporting.
* SQL post-COMMIT refresh failure is already identified as a committed
  outcome, not a rejected write. PC-003 supplements rather than replaces that
  required proof.
* JSON cross-file process-crash atomicity remains a disclosed architectural
  limitation. This critique does not request a new journal, table or service
  or treat that known boundary as an undisclosed blocker.
* The quality.py overlap with #88 is declared. Coordinator integration and
  final-head evidence remain necessary; no change to #88 is authorized here.

## Questions or Blocking Evidence Gaps

* None requiring a user decision. The supplied sources support this
  assessment. The three findings are planner-owned corrections within the
  confirmed scope, not missing customer facts or new approval gates.

## Limitations

* No implementation, tests, image build or backend execution was performed
  during this read-only critique. Research's reported baseline tests are
  historical supplied evidence, not independently rerun results.
* Source inspection was bounded to the supplied engineering evidence and
  closely coupled tests; no external research, private data, live authority
  assessment, UI audit or broader issue acceptance was attempted.
* Existing plan, details, research and other review records were unchanged.
  Pre-existing untracked planning artifacts were read in place, not moved
  or committed.

## Recommended Next Action

* Highest-impact finding: PC-003, because failed recovery can separate a
  persisted success audit from a rolled-back controlled transition.
* Action owner: planning parent.
* Smallest next action: revise P02-T01 with the recovery-fault matrix and
  expected durable outcomes; resolve PC-001 and PC-002 in the same direct
  revision of P01-T02 and its owned test obligations.
* User response required: no.
* Return this complete finding set to the active planning parent. Finalize
  after direct correction without commissioning another plan critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/progress-event-capture-102-plan.md](.copilot-tracking/plans/2026-10-17/progress-event-capture-102-plan.md) | Assessed final candidate; not edited |
| [.copilot-tracking/details/2026-10-17/progress-event-capture-102-phase-details.md](.copilot-tracking/details/2026-10-17/progress-event-capture-102-phase-details.md) | Assessed phase details; direct revision belongs to planning parent |
| [.copilot-tracking/research/2026-10-17/progress-event-capture-102-research.md](.copilot-tracking/research/2026-10-17/progress-event-capture-102-research.md) | Supplied C1-C7 evidence and scope decisions |
| [.copilot-tracking/reviews/plans/2026-10-17/progress-event-capture-102-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/progress-event-capture-102-plan-critique.md) | Complete single-critique finding set |

## Next Steps

The active planning parent resolves PC-001 through PC-003 directly, records
disposition and finalizes the plan without another critique. No user command
or response is required. This critique stops here; implementation and the one
original post-implementation Review remain the parent's subsequent stages.
