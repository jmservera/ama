---
title: "Issue 110 bounded offline sensor consumer original RPI Review"
ms.date: 2026-10-18
---

## Opening Review State

* Goal: execute the one original post-implementation Review of the bounded observations-only consumer, not another plan critique or implementation.
* Scope: exact pinned diff `578631ac75cc8c6a7af53922c6aaae4435e7761c..de54472fc06d1ac16efa6dbd4f306afc1c98598e`, complete bounded source, task artifacts and full session log, plus necessary existing SQL and requirements context.
* Evidence readiness: paths and validation claims supplied by the parent; contents and reconciliation not yet compared. Current unstaged inventory/state/log edits are expected parent lifecycle evidence, not source changes.
* Acceptance basis: approved P01/P02 requirements, original PC001-PC007 dispositions, owner invariants, FR050/AC066, ADR0003 decision 6. This Review cannot grant whole-issue or live acceptance.
* First comparison boundary: establish current plan/details/changes/log coherence, then compare complete candidate source against the bounded controls and recorded validation.
* Read-only boundaries: only this review record may be written. No workers, fixes, private datasets, environment files, live calls, new dependencies/containers, UI or Playwright execution. Existing exact-replay loader and shared SQL stores are preservation boundaries.
* Initial blockers: none established; evidence readiness remains subject to inspection.

## Review Progress

Opening state recorded before substantive comparison. The complete bounded source
and supplied artifacts have now been compared. A focused actual, memory-only
SQLite probe confirms an in-scope malformed-persistence defect, recorded as
RV-001. It does not require source writes, a container or private data.

## Evidence Readiness and Reconciliation

* Reviewed branch: `feat/offline-sensor-consumer-110`.
* Pinned base: `578631ac75cc8c6a7af53922c6aaae4435e7761c`.
* Committed implementation candidate: `de54472fc06d1ac16efa6dbd4f306afc1c98598e`.
* The exact base-to-candidate diff contains 22 paths: six new source/test/helper
  files, two pyproject changes, six narrow documentation changes and eight
  task artifacts. The original Review is the intended twenty-third path.
  All six new files were read completely; because their diff is entirely
  additions, those complete files are the complete source additions. The
  working source/docs have no diff against the candidate.
* The complete research, plan, details, immutable critique, changes, inventory,
  47-line state and all 15 JSONL events were read. The three parent unstaged
  diffs change only the canonical Review path and Review lifecycle state/log.
  They introduce no implementation change.
* Current plan markers check P01-T01/P01-T02/P02-T01/P02-T02. P03-T01 is this
  active Review; P03-T02 is later publication. Their unchecked state is correct
  at this boundary, not a missing implementation finding.
* The changes record's final evidence and ordered log establish P01/P02
  completion. Its final handoff contradicts that state: RV-002. This does not
  prevent a credible boundary because the pinned source, checked tasks,
  explicit final results and implementation-completed log event agree.
* The earlier P02 "Remaining" prose is explicitly labelled historical by the
  later final-evidence section. Unlike the final handoff, that earlier line is
  adequately reconciled.
* The original critique hash was independently recomputed:
  `ad56b59a8df472fff31ed3ae906eca63505ea76fca0f63a457dda4acf540942b`.
  Its Complete execution, Revise verdict and original 3 High/4 Medium findings
  remain preserved. No second critique or worker was invoked.
* Relevant context read: original case, indexed owner context, housing-sector
  introduction, relevant addendum sensor framing, PRD FR-050/AC-066 and ADR 0003
  decision 6. No private datasets, environment files, support material or
  original private 60,000-home data were read.

## Completed-Work Assessment

| Contract | Assessment | Evidence |
| --- | --- | --- |
| P01-T01 / A1 / G1 | Covered | API import-first failure history identifies absent distributions separately from the subsequently missing adapter. The new adapter calls the core processor, which opens actual SQL connections. No public route is registered. |
| R1 / A2 | Covered for new observations | Closed string-field schema, bounded uppercase IDs, signed bounded seed, decimal precision, UTC whole seconds and explicit unit/calibration checks. Envelope preflight is separate from durable per-row DQ. |
| R2 / PC-002 / PC-003 | Covered | Independently declared POLICY/CONTROL fixtures, half-open mapping/calibration/window, inclusive ranges/skew, current SQL consent and mapped-home existence under the writer transaction. Tests mutate authority through another connection while admission waits. |
| R3 / R4 / N2 | Covered for normal persisted state | SQL composite reading key, digest outcome key, writer lock, replay/conflict precedence and equal/older-time rejection. No process-local duplicate set. Each operation owns/closes an independent connection. |
| R5 / PC-005 / PC-006 | Covered | One outcome/DQ transaction per rejected observation, separate observed/received time, Open status, exercise accountable role/manual route, reviewer or Unassigned. Missing route fails trusted setup. Restricted inspection excludes raw observation bodies. |
| R6 / N3 / A4 | Defect | JSON refusal, whole-envelope preflight and unavailable-table errors are explicit. Malformed persisted reading handling is incomplete: RV-001. |
| R7 / PC-004 / PC-007 / A3 | Covered with RV-001 qualification | Actual-engine test code uses triggers for accepted/rejected rollback and a post-COMMIT acknowledgement seam for reopen/reconciliation. API reports committed-prefix receipts for ConsumerError failures. A malformed persisted timestamp bypasses that stopped-batch contract. |
| N1 / N4 | Covered within this slice | Outward receipts expose bounded codes/reference/replay only. New modules have no AI, map, UI, task, ranking, resident, consent-record or property mutation path. Existing replay loader, fault generator and shared SQL stores have no diff. |
| A5 / P02-T02 | Scoped evidence supplied | Broad local regressions, SQL Server and hardened image results are recorded; full API mypy is explicitly not green. RV-003 preserves that limitation without calling it an introduced defect. |
| P03 | Correctly active/pending | Original Review runs now. Publication and exact-published-head independent source/artifact/log assessment have not yet occurred. |

Existing SQL prior art was checked directly: SQLite independent connection and
busy-timeout behavior, SQL Server transaction-owned application lock and
independent connection, and the exact-replay loader's explicit fault-input
refusal. No shared-store edit, new dependency, daemon, SDK, service, transport,
provisioning, analysis or task side effect appears in the candidate.

## Critique and Implementation-Time Update Assessment

| Original finding | Recorded disposition compared with source/evidence |
| --- | --- |
| PC-001 | Task-owned schema inspection, additive SQL Server schema_version widening, bounded key/numeric representation, populated legacy/stock preservation test. The loader and shared stores remain unchanged. |
| PC-002 | Concrete independent fictional matrix is present in details and shared fixture, with semantic boundary checks in the owned tests. No evaluator truth becomes admission authority. |
| PC-003 | Current SQL control/home reads occur under the writer lock. Waiting-writer mutation tests cover consent, mapping, calibration and home removal. Historical admission followed by withdrawal establishes the inverse historical outcome behavior. |
| PC-004 | Exact digest lookup precedes current controls/window; changed accepted identity conflicts; rejected exact retry remains historical after repair. Tests cover withdrawal, later receipt time and rejected repair. |
| PC-005 | Complete envelope preflight, digest-keyed malformed-row DQ, independent row commits, prefix-aware BatchStopped and middle-row rollback/ack retry tests implement the clarified contract. RV-001 exposes a remaining malformed-SQL exception path. |
| PC-006 | Durable reference/reason/status/times/role/route/reviewer fields and metadata-only restricted inspection are implemented. Reviewer None becomes Unassigned, not invented staff assignment. |
| PC-007 | Real accepted/rejected engine-trigger rollback and accepted/rejected postcommit-loss/reopen cases are present in the shared suite, inherited by the API and SQL Server runs. |

The single compatible planning refinement preserves owner intent. Recorded
implementation-time additions (persisted-outcome checks, equal-time rejection,
actual JSON refusal and restricted retention of schema-valid observations)
fit the approved immediate scope; no significant divergent policy decision was
introduced. Test corrections, static fixes, runner interpreter/PATH handling and
populated-legacy test strengthening are documented with their triggering failures.
The type-check import exclusions leave the owned sensor boundary checked and
legacy core checking owned by core; they do not establish a green full API check.
The stale final handoff and incomplete malformed-reading behavior remain adverse
findings rather than being silently repaired by this Review.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Malformed persisted readings can produce success-shaped replay or escape stopped-batch reporting

* Related contracts: R3/R6/R7, N3, A3/A4, PC-005, P01-T01/P01-T02.
* Evidence: `SensorConsumer.process` accepted replay branch
  (`src/core/src/zava_forward/core/sensor_consumer.py:464-485`) checks only that
  a reading with the stable key exists. It does not check whether its persisted
  timestamp/numeric values remain well-formed or consistent with the witnessed
  observation. `_quality` (`:442-447`) then parses persisted MAX(observed_at)
  without converting a parsing failure to ConsumerError. The API's
  `consume` (`src/api/src/zava_forward/api/sensor_ingestion.py:30-35`) preserves
  prefix receipts only for ConsumerError.
* Confirmed actual-engine reproduction: create a memory-only SQLite SqlStore
  subclass supplying independent connections to a shared in-memory database;
  create only a constructed cases table, configure independent exercise controls,
  admit one valid row, then update its stored observed_at to
  `invalid-sql-time` and temperature_c to `not-a-number`. An exact replay returns
  `status='accepted', reason='ACCEPTED', replay=True`. A new valid reading for
  that sensor raises `ValueError('UTC_SECONDS_REQUIRED')`, not BatchStopped,
  and has no `.completed` metadata. Counts remain reading/delivery/DQ = 1/1/0.
  This probe uses the unchanged candidate modules and actual SQLite, not a
  fake connection or transaction implementation.
* Impact: malformed SQL state can look successfully reconciled, contrary to the
  explicit malformed-SQL refusal contract. In a finite batch containing an
  earlier committed row, a later persisted-time parsing failure escapes the
  advertised bounded stopped-batch/prefix protocol. This is not a claim of
  duplicate admission, unauthorized new admission, or a live exploit.
* Scope qualification: the reproduction deliberately creates malformed
  restricted persistence. Normal consumer-only writes do not create that
  corruption. The defect matters because malformed persistence is expressly
  in the accepted failure boundary and the implementation already claims
  persisted-outcome corruption detection.
* Destination: a **later** `rpi-implement` invocation owned by the coordinator,
  if separately authorized. Validate the persisted reading/witness sufficiently
  to refuse malformed/inconsistent state without rechecking present-day
  admission authority; translate persisted-state parsing failure to bounded
  ConsumerError so BatchStopped retains the prefix. Add actual SQL regression
  cases, including a later-row failure after an earlier commit.
* This Review makes no fix and requests no second original Review. Correction
  count for the current parent run must remain zero.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Final changes handoff still says P01/P02 are pending

* Evidence: the changes record's `## Remaining work and handoff` ends with
  `P01/P02 pending. Review not executed; correction count 0.` The current plan
  checks both phases, its final validation table reports their completion and
  the session log has an Implement/completed event followed by Review/started.
* Impact: the final handoff is not reconciled with the otherwise credible
  completion evidence. The Review-not-executed wording was valid at candidate
  handoff and is not itself a pre-Review defect; the unqualified P01/P02 pending
  claim is contradictory even at that boundary.
* Destination: later coordinator-owned evidence reconciliation within
  `rpi-implement` if authorized; preserve the historical text and adverse Review
  rather than rewriting evidence to claim it was already reconciled. This
  Review writes no other artifact. Do not call P03 publication missing
  implementation or convert this observation into another active plan phase.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low, residual]: Full API mypy remains failed on baseline browser imports

* Evidence: changes records full API mypy ultimately failing on nine missing
  `playwright.sync_api` imports in nine existing files, with the same nine
  failures under pinned-baseline configuration. The phase state and plan
  explicitly retain this limitation. Owned API checking passes three files;
  core full checking passes 128 files.
* Impact: scoped type-check success must not be presented as a green full API
  check or green whole-project static acceptance. This is a known baseline
  environment limitation, not an introduced sensor defect or concealed failure.
* Destination: distinct non-blocking tooling follow-up owned by the API
  maintainer/coordinator, under a separately authorized dependency/browser
  environment decision. Do not install or execute Playwright/UI in this run.
  This is not routed to current implementation merely to force a correction.

## Follow-Up Assessment and Acceptance Limits

The plan's Follow-Up Items preserve live Hub identity/transport and infrastructure
owner decisions, Azure SQL/registered real AI acceptance, downstream analysis 111
and the exact-published-head review. Each is outside this finite offline
implementation and is not a new active P01/P02 task.

* Live Hub/infrastructure: infrastructure and product owners must resolve
  sizing/cost/provisioning/network/credential decisions in the separate issue
  140 workstream. The dependency is 140 on 110, not the reverse.
* Azure SQL and registered real AI: application acceptance owners must supply
  actual authorized environment/model evidence under the PRD gates.
* Analysis: issue 111 owns downstream deterministic analysis and any separately
  approved human review-task behavior. It is not a prerequisite for this slice.
* Publication/exact head: parent owns P03-T02; the later independent
  human/coordinator gate must assess the exact published head's complete source,
  artifacts and log. This candidate Review neither performs nor waives it.
* RV-003 adds the distinct API tooling follow-up. No live/legal/privacy authority
  or staff assignment is inferred from fictional fixtures.

All these items remain outside whole-issue acceptance claims. ADR 0003 remains
Proposed; FR-050 and AC-066 include actual Hub, Azure SQL restart and real AI
requirements which this slice does not satisfy. No issue closure, AC tick,
board change or acceptance approval follows.

## Validation Evidence

| Check | Status and provenance |
| --- | --- |
| Exact candidate/source boundary | Independently checked: no working src/docs diff against candidate; complete six added source/test/helper files and both configuration changes read. |
| Whitespace | Independently passed `git diff --check` over pinned base..candidate. |
| Original critique integrity | Independently passed SHA-256 match recorded above. |
| Malformed persisted reading | Independently reproduced on actual memory-only SQLite through API -> core -> SQL; expected explicit refusal/prefix behavior fails as RV-001. No file-backed test data or extra write was needed. |
| Core sensor suite | Parent-recorded 75 tests, one existing sensor112 opt-in MSSQL skip; no failures. |
| SQL store regression | Parent-recorded 18 passed. |
| API preservation | Parent-recorded 124 passed, including expected law-store diagnostic during deliberately unavailable-law test. |
| Real SQL Server API | Parent-recorded final 28 passed, no skips, after populated legacy test strengthening; actual independent connections, rollback/reopen/ack paths. Not rerun here; no new container authorized. |
| Hardened image | Parent-recorded UID 10001, read-only, cap-drop ALL, no-new-privileges, network none: 66 tests, one existing opt-in skip. Separate finite adapter admitted two and reopened/replayed two. Image `52d3a038a16ed73e72ce4efa2b915e97f4e3b1eb763ed028d5e68799a5bde990`; no production source changed afterward. Not rerun here. |
| Populated legacy final rerun | Parent-recorded two SQLite core/API cases passed and final SQL Server API suite passed. |
| Ruff / formatting | Parent-recorded both full component checks passed; core formatter 75 files and API formatter 27 files within existing configured exclusions. Not independently rerun here. |
| Core mypy | Parent-recorded 128 source files passed. |
| Owned API mypy | Parent-recorded three selected files passed, with typed core boundary followed. |
| Full API mypy | Failed: nine existing missing Playwright imports; same failures reported under pinned-baseline configuration. RV-003. Not independently rerun; no UI/browser execution. |
| Live Hub/Azure/AI and acceptance | Unavailable/unexecuted in this scope, intentionally; no conformance claim. |
| Publication and exact-published-head gate | Not yet executed, correctly pending P03/later independent gate. |

Initial failures remain adverse evidence, not erased by later scoped passes:
absent project distributions; PEP-668 refusal; specifically absent adapter;
overbroad privacy assertion; missing Ruff/mypy; initial Ruff findings and long
lines; initial core typing/invariance errors; SQL runner unsupported connection
keyword and two child-import failures before its successful fourth attempt;
typed API/core-fixture lookup errors; 247 then 738 transitive/baseline typing
errors before configured ownership reconciliation; nine remaining baseline
browser imports; and the corrupt-witness test string/inference errors. The
changes record describes their dispositions without claiming failed attempts
were actual SQL acceptance runs. No failure is reclassified as a pass here.

Full file-backed suites were not rerun in this Review: their normal temporary
data writes would exceed the caller's only-review-record write boundary.
The independent behavioral probe instead used actual shared in-memory SQLite
and Python `-B`/`PYTHONDONTWRITEBYTECODE=1`.

## Outcome and Closeout Projection

* **Review execution: Complete.** This is the one original post-implementation
  Review; no workers, source corrections, second critique or repeated Review.
* **Outcome: Defects found.** RV-001 is confirmed against the candidate;
  RV-002 is a reconciled-boundary but unresolved evidence defect. RV-003 is
  non-blocking baseline residual work, not an implementation regression.
* Severity counts: **0 Critical, 0 High, 1 Medium, 2 Low**.
* Implementation evidence: P01/P02 executed with the scoped results above and
  failed full API static check explicitly retained. Overall P03/publication is
  still in progress. Complete Review execution is not complete delivery or
  acceptable whole-issue outcome.
* No blocker prevented this bounded Review. No new plan decision or material
  research gap requires `rpi-plan` or `rpi-research`.
* Every actionable finding has a destination: RV-001 and RV-002 to a later
  separately authorized coordinator-owned `rpi-implement`; RV-003 to the
  distinct API tooling follow-up. None authorizes corrections in the present
  parent run. Preserve original artifact/outcome and correction count zero.
* This record is not the separate exact-published-head source/artifact/log
  acceptance gate and does not approve merge, live use or issue closure.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue-110-offline-sensor-consumer-research.md](.copilot-tracking/research/2026-10-18/issue-110-offline-sensor-consumer-research.md) | Complete bounded research and upstream dependency claims. |
| [.copilot-tracking/plans/2026-10-18/issue-110-offline-sensor-consumer-plan.md](.copilot-tracking/plans/2026-10-18/issue-110-offline-sensor-consumer-plan.md) | Requirements, checked P01/P02 and pending P03. |
| [.copilot-tracking/details/2026-10-18/issue-110-offline-sensor-consumer-phase-details.md](.copilot-tracking/details/2026-10-18/issue-110-offline-sensor-consumer-phase-details.md) | Concrete fixtures, direct dispositions and phase contracts. |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-110-offline-sensor-consumer-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-110-offline-sensor-consumer-plan-critique.md) | Immutable original Complete / Revise critique, PC-001 through PC-007. |
| [.copilot-tracking/changes/2026-10-18/issue-110-offline-sensor-consumer-changes.md](.copilot-tracking/changes/2026-10-18/issue-110-offline-sensor-consumer-changes.md) | Complete validation history, retained failures and stale final handoff. |
| [.copilot-tracking/changes/2026-10-18/issue-110-offline-sensor-consumer-inventory.md](.copilot-tracking/changes/2026-10-18/issue-110-offline-sensor-consumer-inventory.md) | Complete intended 23-path delivery inventory. |
| [.copilot-tracking/rpi-sessions/2026-10-18/issue-110-offline-sensor-consumer-state.json](.copilot-tracking/rpi-sessions/2026-10-18/issue-110-offline-sensor-consumer-state.json) | Parent Review lifecycle state and known static limitation. |
| [.copilot-tracking/rpi-sessions/2026-10-18/issue-110-offline-sensor-consumer-log.jsonl](.copilot-tracking/rpi-sessions/2026-10-18/issue-110-offline-sensor-consumer-log.jsonl) | Complete ordered 15-event execution history at Review boundary. |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-110-offline-sensor-consumer-review.md](.copilot-tracking/reviews/logs/2026-10-18/issue-110-offline-sensor-consumer-review.md) | This one original Complete / Defects found Review. |
| [src/core/src/zava_forward/core/sensor_consumer.py](src/core/src/zava_forward/core/sensor_consumer.py) | Complete core consumer and confirmed RV-001 locations. |
| [src/core/tests/sensor_consumer_fixture.py](src/core/tests/sensor_consumer_fixture.py) | Independent fictional policy/control and constructed-only fixture. |
| [src/core/tests/test_sensor_consumer.py](src/core/tests/test_sensor_consumer.py) | Complete SQL semantics, concurrency, rollback/reopen and preservation tests. |
| [src/api/src/zava_forward/api/sensor_ingestion.py](src/api/src/zava_forward/api/sensor_ingestion.py) | Finite adapter and bounded stopped-batch contract. |
| [src/api/tests/test_sensor_ingestion.py](src/api/tests/test_sensor_ingestion.py) | Inherited full semantics and API batch integration tests. |
| [src/api/checks/sensor_sql_check.py](src/api/checks/sensor_sql_check.py) | Task-owned actual SQL Server validation helper. |
| [src/core/pyproject.toml](src/core/pyproject.toml) | Core static-check configuration change. |
| [src/api/pyproject.toml](src/api/pyproject.toml) | API static-check ownership/import changes. |
| [src/core/README.md](src/core/README.md) | Core contract and explicit incomplete live acceptance. |
| [src/api/README.md](src/api/README.md) | Adapter, error/prefix and validation helper contract. |
| [docs/adrs/0003-journey-derived-capabilities-runtime-fit.md](docs/adrs/0003-journey-derived-capabilities-runtime-fit.md) | Decision 6 and preserved Proposed status. |
| [docs/case_study_48_addendum.md](docs/case_study_48_addendum.md) | Narrow offline status within preserved sensor proposal. |
| [docs/reference/README.md](docs/reference/README.md) | Indexed bounded consumer evidence. |
| [docs/reference/log.md](docs/reference/log.md) | Append-only knowledge-base change entry. |
| [docs/prds/zava-forward-retrofit-programme-demonstrator.md](docs/prds/zava-forward-retrofit-programme-demonstrator.md) | FR-050/AC-066 live acceptance boundary, unchanged. |

## Next Steps

The active parent preserves this one original Review unchanged, records
Complete / Defects found and all RV IDs with correction count **zero**, performs
only its authorized publication/evidence handoff, and stops for the separately
required exact-published-head independent source/artifact/log gate. Do not fix
source in this run, invoke another original Review or claim whole-issue/live
acceptance. RV-001/RV-002 require a later separately authorized implementation/
evidence action; RV-003 remains with the distinct API tooling follow-up owner.
