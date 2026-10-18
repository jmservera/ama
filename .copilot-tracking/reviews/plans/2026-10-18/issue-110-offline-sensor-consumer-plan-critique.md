---
title: Issue 110 offline sensor consumer original plan critique
description: One final-candidate assessment of the bounded offline SQL consumer plan
ms.date: 2026-10-18
---

## Metadata

* Task ID: issue-110 / issue-110-offline-sensor-consumer
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-110-offline-sensor-consumer-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-110-offline-sensor-consumer-phase-details.md
* Research: .copilot-tracking/research/2026-10-18/issue-110-offline-sensor-consumer-research.md
* Critique execution status: Complete
* Inspected branch: feat/offline-sensor-consumer-110
* Inspected HEAD: 578631ac75cc8c6a7af53922c6aaae4435e7761c
* Original critique invocation: one; no other reviewer or worker invoked.

## Inputs and Criterion Boundary

* The caller requires observations-only, finite core/API SQL processing, independently supplied mapping/calibration/consent/clock/range controls, stable SQL identity, transaction-current authority, actual independent SQLite/SQL Server concurrency and recovery, nonsensitive receipts and owned DQ.
* The plan's R1-R7, N1-N4, A1-A5, G1-G3 and P01-P03 are the assessment boundary. Research C1-C6 and W1-W3 supply the design rationale and upstream scope.
* Exact source checks covered src/core/src/zava_forward/core/synthetic/sensor_backfill.py, src/core/src/zava_forward/core/synthetic/sensor_faults.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/mssqlstore.py, src/api/tests/test_mssqlstore.py and src/api/Dockerfile.
* Context included docs/case_study_48_original.md, the relevant baseline in docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and the introductory customer context in docs/reference/research/sector/housing-association-primer.md.
* Upstream criteria checked directly were decision 6 in docs/adrs/0003-journey-derived-capabilities-runtime-fit.md and PRD FR-050/AC-066 in docs/prds/zava-forward-retrofit-programme-demonstrator.md. Their live Hub/Azure SQL/real AI gates are intentionally not acceptance criteria for this offline slice.
* No live issue retrieval, external research, implementation, tests, environment inspection or operational-policy approval was performed. W1-W3 are assessed as supplied research claims, not newly verified issue state.
* Existing untracked parent planning/research/session artifacts were present. They were not changed. Only this caller-authorized critique artifact is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| G1; C1/C3; R1/R3; P01-T01 | Partial | Existing connection and reading-table reuse is credible, but physical SQL compatibility is unresolved: PC-001. |
| R1/R2; A2; P01-T01/P01-T02 | Partial | Independent controls are required but concrete fixture values and expected boundary outcomes are not supplied: PC-002. |
| R2; N2; A3; P02-T01 | Partial | Transaction-current reads are specified, but the actual two-connection authority-change acceptance case is absent: PC-003. |
| R3/R5/R7; G2; A3 | Partial | Replay recovery is required without an explicit precedence contract under changed authority and time: PC-004. |
| R1/R5/R6; A2/A4; P01-T02 | Partial | Batch preflight, per-row DQ and partial-commit behavior need reconciliation: PC-005. |
| R4/R5; C5; A2 | Partial | A dedicated restricted DQ table is appropriate; manual route accountability and visibility need a concrete contract: PC-006. |
| R5/R7; A3; P02-T01 | Partial | Actual accepted-insert rollback/ack seams are specified; rejected-outcome atomicity and recovery need explicit evidence: PC-007. |
| N1/N3/N4; A4 | Covered at planning level | Bounded receipts, explicit failure, JSON refusal, no unrelated case/task/audit mutation and replay-loader preservation are explicit. Physical-schema preservation remains PC-001. |
| A1/A5; C6; P02-T02 | Covered at planning level | Failing-first adapter evidence, actual image execution, existing regressions and configured checks are required, without asserting they have run. |
| W1-W3; C4; P03 | Covered at planning level | Proposed ADR, incomplete upstream acceptance, pinned ancestry, one original Review, unchanged adverse outcomes, Refs #110 and no merge are retained. |
| Owner exclusions and issue 122 dependency | Covered | No shared-store edits, implementation workers, public route, transport, infrastructure change, AI, analysis, property mutation or task creation is proposed. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 3 High, 4 Medium, 0 Low.
* Rationale: The architectural boundary is credible and compatible with the owner direction. However, existing T-SQL cannot represent the proposed schema version unchanged, and several acceptance contracts permit materially different implementations or incomplete evidence. These are substantive planning gaps, not demonstrated implementation defects.
* Preserve this original verdict and artifact unchanged. Compatible findings may be dispositioned directly once by the automatic planning parent; no second critique is requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Reused SQL reading schema cannot represent the proposed contract unchanged

* Related IDs: C1/C3; R1/R3; N2/N4; A1/A3; P01-T01/P02-T01.
* Evidence: Phase details lines 16-19 require existing sensor_reading reuse and legacy preservation. In src/core/src/zava_forward/core/synthetic/sensor_backfill.py, SQL_DDL defines schema_version VARCHAR(12), sensor_id VARCHAR(20), reading_id VARCHAR(40), and DECIMAL(5,2) values; STOCK_SQL_DDL changes identity widths but retains VARCHAR(12) for schema_version. The proposed sensor-fault-input-v1 value has 21 characters. SQLite's loader table instead uses TEXT. The loader DDL also does not explicitly select the binary collation used by the shared MSSQL store tables.
* Concern: The plan does not select an additive, task-owned compatibility path or distinguish fresh, legacy and stock-created tables. Creating a suitably wide fresh table alone would conceal failure on existing loader-created SQL Server tables. Numeric rounding and database key equality can also differ from fingerprint/identity equality if left implicit.
* Impact: Actual MSSQL admission can fail or alter accepted values; differently spelled identities can collide according to database collation. SQLite-only success would not establish the promised parity or preservation.
* Smallest useful change: Specify task-owned schema inspection/initialization and the additive compatibility action for supported existing schemas, without editing shared stores or weakening load_into. Name column capacities, key comparison rules and accepted numeric precision. Explicitly refuse unsupported schemas before delivery writes rather than silently replacing tables or truncating data.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T01 identifies the compatibility strategy and supported table shapes. The locked tests require fresh and existing legacy/stock schemas on actual SQLite and MSSQL, retain pre-existing rows, persist the full schema version, assert exact value round-trip or declared precision rejection, and test key spellings relevant to case/trailing-space equality. Re-running the existing loader must remain supported for compatible existing data.
* Decision route: Direct planner correction. Additive task-owned compatibility follows existing direction; destructive replacement or shared-store edits would be divergent and must not be introduced.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Independent control fixtures are promised but not concretely defined

* Related IDs: R1/R2/R4; A2; P01-T01/P01-T02; C2.
* Evidence: Plan lines 55-60 and 88-90 enumerate checks. Phase details lines 21-25 refer to a supplied policy and lines 32-33 require independent controls, but neither document supplies fixture values, a named fixture matrix or exact boundary outcomes.
* Concern: The owner explicitly requires independent mapping, calibration, consent, clock and ranges fixtures. The candidate states that requirement without fixing the exercise contract. For example, it does not distinguish the observation time used for mapping/calibration validity from the receipt time used for current consent and skew, or define the inclusivity of value/skew bounds.
* Impact: Tests could derive authority or ranges from the generated observation, or encode opposite boundary interpretations while still appearing to satisfy A2.
* Smallest useful change: Add one compact, explicitly fictional fixture matrix with a fixed receipt time, mapping/calibration intervals, allowed units, granted/unknown/declined consent, observation window, skew allowance, temperature/humidity bounds and a manual route. Define which clock each check uses and expected results at, just before and just after every boundary. Controls must be installed independently, never inferred from Packet.clean, Packet.label or the observation claims.
* Action owner: Planning parent.
* Exact resolving evidence: Plan/details contain concrete exercise values and expected reason/status outcomes, including calibrated=true with expired/missing trusted calibration and calibrated=false despite otherwise valid controls. The same fixtures and assertions are assigned to the two locked test files and shared fixture module.
* Decision route: Direct planner correction. These are labelled exercise choices, not operational-policy or legal decisions.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Current-authority acceptance lacks an independent writer mutation test

* Related IDs: R2; N2; A3; P02-T01; C3.
* Evidence: Plan R2 and phase details lines 21-25/40-45 correctly require current controls/home existence under the writer lock. The named races only address same-key and timestamp-order delivery. src/core/src/zava_forward/core/sqlstore.py supplies independent connections; src/core/src/zava_forward/core/mssqlstore.py translates BEGIN IMMEDIATE into the transaction-owned zavaforward_write application lock.
* Concern: Two delivery writers do not prove that a consumer constructed before a control change re-reads the committed SQL authority rather than using a cached dataclass or store case snapshot.
* Impact: A stale consumer could admit input after consent withdrawal, remapping, calibration expiry/update or removal of the mapped home while passing all named delivery races.
* Smallest useful change: Add deterministic barrier-based authority-change cases using separate actual connections and the same database writer-lock protocol. Construct the consumer first, commit a control change on the other writer before its admission transaction acquires the lock, and assert that the changed authority is applied. Include the inverse lock ordering to make serialization expectations explicit, not timing-dependent.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T01 names actual SQLite and MSSQL cases for stale consent, mapping/calibration control and home-existence state. Assertions cover reason/status, zero unauthorized reading inserts, the appropriate DQ/outcome counts and unchanged unrelated case state. No shared-store source change or fake connection is needed.
* Decision route: Direct planner correction; the required current-transaction authority is already owner-confirmed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Replay reconciliation precedence under changed controls and clocks is ambiguous

* Related IDs: R2/R3/R5/R7; A3; P01-T01/P02-T01.
* Evidence: Plan R2 says current control is validated inside each writer transaction. R5 requires exact accepted/rejected replay to reconcile without new records. R7 requires recovery after uncertain acknowledgement. No ordering or changed-control replay case is specified.
* Concern: An exact retry after consent withdrawal or advancement beyond the acceptance window can either reconcile historical committed work or be newly rejected, depending on validation order. A previously rejected retry after control repair has the symmetric ambiguity. Conflicting reuse also needs to remain a conflict rather than inherit an existing success.
* Impact: Retry behavior can create extra DQ, appear to re-authorize historic data, or defeat post-COMMIT reconciliation.
* Smallest useful change: State an explicit transaction decision order separating historical outcome reconciliation from new admission. Exact witnessed replays return the recorded outcome without re-admission or latest advancement; changed input under a witnessed identity is a conflict; current controls/time govern new admission. Define how conflicting attempts are recorded without overwriting the original witness.
* Action owner: Planning parent.
* Exact resolving evidence: Revised decision table plus actual-engine tests replay an accepted input after withdrawal/window change, replay a rejected input after control repair, and reuse the same identity with changed content. Reopen and uncertain-ack retries must preserve the original outcome reference and reading/DQ counts.
* Decision route: Direct planner correction. This resolves the candidate's own idempotence requirements, not permission to ingest under withdrawn consent.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Batch preflight, malformed-row DQ and partial durability have no single contract

* Related IDs: R1/R5/R6/R7; A2/A4; P01-T02.
* Evidence: Plan line 69 requires the finite batch to be preflighted before writes. A2 includes missing/extra/boolean/time/ID faults as visible owned DQ. Phase details lines 29-34 describe the container and receipts but not preflight depth, unkeyable row identity or batch transaction boundaries.
* Concern: Whole-batch structural refusal before any write and durable per-row malformed-input DQ are different contracts. Rows missing stable identifiers cannot automatically use the sensor_id/reading_id witness key. The candidate also does not state whether a database failure or uncertain commit at row N leaves an acknowledged committed prefix, rolls back the whole batch, or permits processing later rows.
* Impact: Reasonable implementations can lose DQ visibility, persist a partial batch unexpectedly, fabricate stable identity for malformed input, or report a failed batch as if no rows committed.
* Smallest useful change: Separate batch-envelope rejection, unsupported primitive/unkeyable rows and keyed semantic rejection in a small decision table. Define which checks finish before writes, how unkeyable invalid rows receive a bounded visible/manual outcome without trusting invented device identity, and whether transactions are per-row or per-batch. Specify stop/continue and receipt semantics for failure/uncertain acknowledgement, including retry of already committed entries.
* Action owner: Planning parent.
* Exact resolving evidence: The revised contract assigns expected status/reason, SQL reading/delivery/DQ counts and retry behavior for valid-then-malformed, malformed-then-valid, missing-ID, repeated malformed input, database failure at a middle row and uncertain acknowledgement at a middle row on both actual engines. Outward results remain bounded and identifier-free.
* Decision route: Direct planner correction. Select a finite contract consistent with current requirements; do not add a transport, queue or automatic recovery service.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Unassigned reviewer and a route string do not establish owned actionable DQ

* Related IDs: R4/R5; A2; C5; P01-T01/P01-T02.
* Evidence: Plan R5 permits reviewer Unassigned and requires a manual route. Phase details name sensor_data_quality_exception and nonsensitive receipts but do not define accountable route ownership, durable action metadata or how restricted inspection reaches an actionable record.
* Concern: The distinction between an unknown individual reviewer and an accountable manual handling route is not fixed. A stored Unassigned value plus arbitrary text can satisfy the wording without anyone or any declared exercise role owning follow-up.
* Impact: Rejections can be durable but operationally unowned, undermining the explicit visible-owned-DQ criterion.
* Smallest useful change: Define minimal DQ fields and restricted inspection evidence: stable exception/outcome reference, reason, separate observed/received time where parseable, explicit status, declared constructed accountable role/route and reviewer identity or Unassigned. Reject an unusable trusted route configuration explicitly. Do not fabricate a staff assignment or create a case task/public route.
* Action owner: Planning parent.
* Exact resolving evidence: A fixture supplies a named fictional accountable route and tests show every keyed rejection resolves to exactly one inspectable DQ record with ownership/status/time metadata. An unknown reviewer remains Unassigned while the accountable route remains present; missing/invalid route configuration fails visibly. Receipts and errors expose no raw IDs or observation values.
* Decision route: Direct planner correction. The owner has already authorized explicit constructed controls and manual fallback, not real staff delegation.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Rejected-outcome atomicity and acknowledgement recovery are not explicitly exercised

* Related IDs: R5/R7; A3; P02-T01.
* Evidence: Phase details lines 43-45 specify a trigger between reading insert and outcome insert and an after-COMMIT acknowledgement exception. A rejected row does not take the accepted reading-insert path, and the details do not assign rejection-specific failure/recovery assertions.
* Concern: The planned failure seam can prove reading/witness atomicity without proving that rejection witness and DQ persist atomically. Accepted replay alone does not prove rejected replay recovers the same owned exception after uncertainty.
* Impact: A crash can leave a rejection without actionable DQ, an orphan DQ record, or duplicate exceptions on retry despite passing the named accepted-path checks.
* Smallest useful change: Extend the existing actual-engine matrix with a real trigger failure between rejection-ledger and DQ writes, and after-COMMIT acknowledgement loss for a rejected observation. Keep the existing accepted-path failure and independent-connection tests.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02-T01 requires SQLite and MSSQL assertions that neither rejection witness nor DQ survives rollback, followed by a successful retry; after a committed rejected outcome loses acknowledgement, a fresh consumer's exact retry returns the same outcome/DQ reference with exactly one of each and zero readings.
* Decision route: Direct planner correction; no new review or implementation worker is needed.

## Strengths and Residual Risk

* The consumer is correctly separate from the generator replay verifier. Only Packet.rows enters admission; labels, clean data and calibrated claims do not grant authority.
* Existing independent connections and database writer serialization are suitable prior art. The plan properly refuses process-local duplicate sets and fake SQL connections as runtime acceptance.
* Explicit legacy-row conflict avoids inventing provenance. Dedicated restricted SQL DQ avoids unrelated property, task, audit or ranking mutation.
* Local MSSQL/image results are not promoted to Azure, authenticated device transport, real AI, legal approval or full issue acceptance.
* One original Review, retained initial failures, immutable adverse outcomes, pinned lineage and a separate exact-published-head gate are correctly preserved.
* Dependency #122 remains a no-shared-store-edit boundary, not permission to defer required task-owned correctness.

## Questions or Blocking Evidence Gaps

* No new user choice is required for these seven findings. The automatic planning parent can resolve them inside the supplied scope.
* No decision-critical missing external evidence blocks this critique. Future actual-engine and image execution remains implementation evidence, not a result claimed here.
* If the parent discovers that additive task-owned compatibility cannot preserve supported loader schemas, that newly demonstrated conflict must be escalated rather than silently weakening loader preservation or editing shared stores.

## Limitations

* This is one final-candidate plan assessment, not source implementation acceptance, a second research cycle or a runtime review.
* Source inspection establishes the stated physical-schema mismatch and available lock/connection mechanisms. It does not prove an unimplemented consumer has any particular defect.
* Tests, containers, static checks, restart behavior and current external issue state were not executed or freshly verified.
* Only the relevant baseline portion of the large addendum and index was read; no full project, regulatory or security audit is claimed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Automatic planning parent.
* Smallest next action: Define the task-owned, non-destructive SQL compatibility contract and actual existing-schema acceptance cases, then directly disposition PC-002 through PC-007 in the plan/details once.
* User response required: No.
* Preserve this adverse original critique and its bytes. Do not run a second critique, invoke implementation workers or treat planner disposition as independent acceptance.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue-110-offline-sensor-consumer-plan.md](.copilot-tracking/plans/2026-10-18/issue-110-offline-sensor-consumer-plan.md) | Assessed final-candidate plan; unchanged by critique. |
| [.copilot-tracking/details/2026-10-18/issue-110-offline-sensor-consumer-phase-details.md](.copilot-tracking/details/2026-10-18/issue-110-offline-sensor-consumer-phase-details.md) | Assessed phase details; unchanged by critique. |
| [.copilot-tracking/research/2026-10-18/issue-110-offline-sensor-consumer-research.md](.copilot-tracking/research/2026-10-18/issue-110-offline-sensor-consumer-research.md) | Supplied bounded research and evidence pointers. |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-110-offline-sensor-consumer-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-110-offline-sensor-consumer-plan-critique.md) | Original Complete / Revise critique; preserve unchanged. |

## Next Steps

The active automatic planning parent directly dispositions the seven compatible
findings once and finalizes planning under the existing gates. No second critique
or new user command is required. This critique task stops after writing and
verifying this artifact; implementation and the one original implementation
Review remain parent-owned later stages.
