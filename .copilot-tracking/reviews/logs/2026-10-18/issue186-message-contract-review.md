<!-- markdownlint-disable-file -->
# Review: Issue186 shared message contract and volume

## Scope and Evidence

* Task ID: issue186
* Task slug: issue186-message-contract
* Review date: 2026-10-18
* Scope: full bounded task, six canonical documents and issue186 RPI evidence.
* Base: 100ead1bacdb72a8ea7ce5867233db30b22b2f50
* Plan: .copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md
* Details: .copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-18/issue186-message-contract-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-18/issue186-message-contract-changes.md
* Research: .copilot-tracking/research/2026-10-18/issue186-message-contract-research.md

## Opening Review State

* Goal: one independent original assessment of the unchanged-consumer
  documentation, measured volume and evidence boundaries, not full issue acceptance.
* Readiness: plan phases/tasks complete, details/changes/state reconciled;
  final80-test result passed; original failing temp-root attempt retained.
* Acceptance basis: owner bounded direction, plan FR1-FR4/AC1-AC5, direct
  critique dispositions and recorded execution refinement.
* First boundary: exact source authority/behavior versus six-doc diff and
  completed plan; then arithmetic, reproduction, gaps and tracking evidence.
* Authority: one fresh independent worker may write only this record. No source,
  plan, changes, critique, research or state changes; no nested agents.
* Initial blockers: none reported; publication/frozen-head inventory follows
  Review and is not yet executed or independently accepted.

## Execution Status

* Review execution status: Complete.
* Bounded implementation execution status: Complete for P01/P02 and all three
  tasks. This does not assert completion of publication or full issue acceptance.
* This is the one independent ORIGINAL post-implementation Review. The opening
  state above is preserved unchanged. No implementation, correction, second
  Review, subagent, remote operation or issue mutation was performed.
* Evidence comparison covers the six canonical documentation diffs against the
  pinned base, the complete supplied RPI task set, state/execution evidence,
  raw validation logs, relevant unchanged source and semantic tests.
* Local HEAD and local origin/main ref both resolve to the specified base;
  branch remains docs/sensor-message-contract-186. No remote freshness claim is
  made by this reviewer.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| Goal; FR1; AC1; P01-T02 | Imported contract described in existing synthesis | Reconciled | Consumer directly imports READING_FIELDS/SCHEMA_VERSION; all 13 table fields match the authority in order. No duplicate executable schema or public API. |
| FR2; AC2; P01-T02 | Stable append, historical replay, conflict, refusals and bounded output | Reconciled | Source and unchanged semantic tests support the described behavior; current controls are not reapplied as fresh admission to historical replay. |
| FR3; AC3; P01-T01 | Executed current public fixture measurement and exact rate arithmetic | Reconciled | Independently reproduced 366 bytes, exact digest and both declared population calculations. Two measures remain one observation. |
| FR4; AC4; P01-T02 | Stock incompatibility and separate transport/approval gates | Reconciled | Stock sensor ID construction and embedded reading ID do not satisfy unchanged admission. No silent adapter, remap, truncation or validation relaxation. |
| P01; P01-T01; P01-T02 | Measurement followed by six-document integration | Reconciled | Completed task markers, phase details, changes and execution record agree. All six diffs inspected. |
| P02; P02-T01; non-functional requirements and test lock | Focused tests, documentation checks and cleanup | Reconciled | Original failure retained; final 80-test run passes with SQLite and owned session TMPDIR. No source/test additions, removals or edits. |
| AC5, completed portion | One critique, direct dispositions, implementation evidence, this original Review | Reconciled within current stage | Critique remains Complete/Revise, not retrospectively Pass. Review completes here; subsequent draft publication/frozen-head inventory is coordinator-owned and not yet done. |
| AC5, later lifecycle portion; Handoff | Publish then stop, final-head assessment remains separate | Correctly pending | Not an active implementation defect or falsely completed delivery claim. This Review does not tick criteria, close an issue or accept a future PR head. |
| Follow-Up Items | Separate downstream compatibility decision and live gates | Reconciled | Both exclusions are mirrored in changes and canonical documentation; routing is recorded below without enlarging P01/P02. |

No active plan marker is stale or incomplete. The plan's context table and
handoff describe this Review/publication as later lifecycle actions; the
review-active state is consistent with the point at which evidence was supplied.
The research is complete for its questions, not proof of live interoperability.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | .copilot-tracking/changes/2026-10-18/issue186-message-contract-measurement.log | Measured unchanged observations()[0] using existing digest serialization | Exact public JSON, imported shape/version checks, digest and Fraction arithmetic | Parent log inspected; reviewer executed the literal documented snippet and independent comparisons | Complete; sample only, not a distribution or bound |
| P01-T02 | docs/reference/research/iot-sensor-analytics-research-plan.md | Added current authoritative contract, admission/replay, rate/sample reproduction and compatibility boundary before dated history | Full added section and unchanged source compared | Exact field order/types, source constraints, 366-byte/hash reproduction and local links pass | Complete; existing historical material and proposal boundaries retained |
| P01-T02 | src/core/README.md | Added short synthesis link and paired-count/stock-ID warning | Full diff and surrounding consumer documentation inspected | Relative link/anchor and source comparison pass | Complete; no new schema authority |
| P01-T02 | src/api/README.md | Added short reference distinguishing finite callable batches from wire packetization | Full diff and adapter source inspected | Relative link/anchor and preflight/API comparison pass | Complete; remains in-process, not HTTP/live ingestion |
| P01-T02 | docs/case_study_48_addendum.md | Added current bounded contract and volume summary in existing sensor section | Full diff and surrounding proposal/three-per-day baseline inspected | Counts, compatibility warning and destination anchor pass | Complete; no change to original case, gates, autonomy or operational rules |
| P01-T02 | docs/reference/README.md | Added index routing for the maintained contract | Full diff inspected | Target/anchor and bounded claims pass | Complete |
| P01-T02 | docs/reference/log.md | Appended dated KB entry | Base content remains an exact byte prefix | Independent append-only assertion passes | Complete; prior entries unchanged |
| P02-T01 | Plan/details/changes and four raw validation logs | Preserved failed attempt, recorded execution refinement, final pass and documentation checks | State, ordered execution log, raw results and task completion markers agree | 80 unchanged tests passed in 18.040s; reviewer did not rerun them | Complete; no correction to code or tests |

### Exact source-truth assessment

* The consumer imports the shared constants from
  src/core/src/zava_forward/core/synthetic/sensor_faults.py. The descriptive
  table matches sensor_consumer._shape: uppercase ASCII identity alphabet and
  first-character rule; sensor/reading/home limits 20/40/12; scenario limit20;
  13 required strings; exact imported version and SYNTHETIC source; decimal
  grammar; symmetric seed magnitude limit, including -0; valid UTC whole seconds.
  Units/calibration admission are correctly distinguished from closed shape.
* Independently installed policy/control checks cover mapping/home existence,
  monitoring consent, half-open mapping/calibration/window intervals, inclusive
  skew/ranges and strict observed-time ordering. Documentation does not promote
  payload claims or fictional controls into operational authority.
* preflight bounds the entire finite envelope before API writes: list/tuple
  1..100, primitive dictionaries, at most20 keys/4096 serialized bytes, key
  limit80 and symmetric integer bound. The observation schema and invalid
  trusted receipt time are accurately distinguished from per-row DQ.
* process preserves digest-based historical outcomes. Identical accepted replay
  checks retained witness/reading and adds no reading/delivery/DQ; changed valid
  content at an occupied key conflicts without overwrite; malformed shape may
  fail earlier. Historical rejected replay retains its rejection/Open DQ.
  Corrupt retained evidence raises bounded error, not success.
* Receipts expose reference/status/reason/replay, not raw IDs/readings.
  Restricted DQ ownership/manual routing and parseable observation/receipt
  times match source. Arbitrary malformed/unknown content is not persisted as
  an observation body. API failure preserves acknowledged prefix; uncertain
  acknowledgement does not imply rollback or whole-batch atomicity.
* Three paired observations per eligible fictional home give 3N, not6N:
  N=1 gives3/day and1/28800 per second; N=60000 gives180000/day and25/12 per
  second. The mean is not a measured peak or processing capability.
* Sorted ASCII default-separator JSON, UTF-8, no newline, gives366 bytes and
  SHA-256 efccea5eb698a3310aca7409837ad9b5ad3673b949ddb3c2395da21a8b01dc6c.
  Sample scaling gives1098 and65880000 bytes/day. The docs exclude framing,
  transport/security/properties/retry/rejection/storage/billing overhead and
  do not call these measured daily traffic or payload maxima.
* Callable batch size is not packetization. One-observation/message and
  sum-of-ceilings grouping are explicitly conditional, with packing assumptions;
  no wire design, Hub billing, tier, cost or throughput decision is adopted.
* Stock Selection uses the nine-character prefix plus64 lowercase SHA-256
  hex characters, length73; backfill reading ID embeds it and exceeds40.
  Public fixture legacy sensor_for(ZF-1) proves this consumer contract only.
  No stock/private dataset was needed to establish the incompatibility.
* ADR0003 already records 2026-10-15 acceptance with Basic exercise amendment.
  Historical Proposed text is preserved and not presented as pending approval.
  The merged411 contract dependency is consistent with the exact local base and
  supplied research; whole110/live acceptance is not inferred.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01; PC-001 | Explicit ZF_SENSOR_MSSQL=0 pin | store_at selects MSSQL only for exact inherited value1; owner requires offline/no-private execution | Plan, details, changes and literal execution commands retain pin | Direct compatible disposition; original critique unchanged | Resolved; no ambient SQL values or credentials needed |
| P02-T01; PC-002 | Changed owned scratch from repository root to task-owned session TMPDIR | Initial run:80 tests/16 errors; stock_fabric._destination intentionally forbids repository outputs. Caller explicitly recognizes session scratch refinement | Current plan/details/disposition, changes, state and execution log agree; failed output retained; exact scratch cleanup recorded | Direct execution refinement, no material product decision or additional critique | Justified; preserves isolation, source/test lock and approved contract |
| Measurement/environment prerequisite | Installed local project distributions in owned venv after observed missing import; added required local agents distribution after dependency failure | ModuleNotFoundError and failed initial install retained in execution log | Source binding paths and successful installation recorded | No manifest or scope revision | Compatible prerequisite resolution, not a runtime change |

The temp-root adjustment changes execution hygiene, not contract, architecture,
scope, acceptance thresholds or producer behavior. No significant/divergent
decision needing new owner approval or planning is identified. No original
adverse evidence was replaced. Correction count remains0.

## Critique and Material Revision Assessment

* The one independent critique is Complete with original verdict Revise:
  PC-001 High and PC-002 Medium. Both have explicit direct dispositions in
  plan/details and corresponding executed-command evidence in changes/log.
* PC-001's offline pin is source-supported and present in both test attempts.
  Review reproduced no store/backend operation and did not inspect inherited
  SQL configuration.
* PC-002's literal repository scratch destination proved incompatible with the
  existing generator guard. Keeping that destination would not be a useful
  acceptance requirement. The current caller-authorized owned-session refinement
  preserves its isolation purpose without weakening the guard.
* Planning readiness is Ready after direct dispositions, not an invented second
  critique or retrospective Pass. No code/contract divergence triggered fresh
  planning or a dependent-work pause; the failed validation was resolved before
  P02 completion and Review handoff.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| FU-01: stock/live compatibility for187/188 | Owner expressly limits this delivery to unchanged consumer; source incompatibility is known, not repaired or waived | Coordinator assigns a separately reviewed compatibility decision before downstream producer/replay/live integration | Open distinct follow-up; not an issue186 implementation defect or new P01/P02 task |
| FU-02: independent operational/service/human gates | Contract documentation and local synthetic engineering cannot establish identity, transport, sizing/cost, network/provisioning/credentials, privacy/legal/OD-43, real AI, Azure or human acceptance | Coordinator retains each applicable gate with its named operational/human approval owner | Open distinct follow-up; no gate is waived, merged or claimed satisfied here |

These existing exclusions remain outside bounded completion and acceptance claims.
The changes record mirrors both; this Review does not convert them into active
implementation work or issue acceptance.

## Findings

No substantive actionable defect, unaccepted decision divergence or material
in-scope evidence gap was identified. No RV-xxx is fabricated for an intentional,
already recorded exclusion or pending publication action.

Severity summary: Critical0; High0; Medium0; Low0.
The two pre-existing non-blocking follow-up routes are listed once above and
remain distinct from review defects.

## Defects

None identified in the supplied bounded delivery.

## Routed Findings

No RV entries require rpi-implement, rpi-plan or rpi-research. No correction or
second Review is requested. Follow-up ownership is recorded in the Plan Follow-Up
Assessment, not duplicated as an implementation finding.

## Residual Work

FU-01 and FU-02 remain intentionally outside this delivery. Publication,
frozen-head/base inventory and full-PR acceptance remain coordinator lifecycle
work, not residual feature defects.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active P01/P02 implementation work: none.
* Draft PR publication has not yet occurred in this evidence set. This reviewer
  did not commit, push, create a PR, inspect a future head or change criteria,
  closure, board state or merge status.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Recorded system Python import and first local distribution install | Environment prerequisite | Failed, retained | Missing zava_forward, then missing local agents dependency. Later installed local distributions and exact source bindings recorded; no manifest edits. |
| Parent measurement command/log | P01-T01 | Passed, inspected | Imported field/version/shape, exact existing reference expression and Fraction arithmetic; public fixture only. |
| Parent initial unittest test_sensor_consumer test_sensor_ingestion test_sensor_faults -q | P02-T01, forced SQLite/repository TMPDIR | Failed, retained | 80 tests in17.901s,16 errors. Direct traces show repository-output guard refusal; CLI case records nonzero subprocess rather than captured diagnostic text. Final run resolves execution setting, not code. |
| Parent final same unittest invocation | P02-T01, ZF_SENSOR_MSSQL=0 and owned external session TMPDIR | Passed, inspected; not rerun | Raw final log:80 tests in18.040s,OK. Exact prefixed command, effective tempfile check and cleanup are in execution log. |
| Parent documentation check/log | Six docs and measured example | Passed, inspected | Exact field table/fixture/snippet/bytes, relative links/anchors, append-only log and six-doc-only tracked diff. |
| Reviewer Python -B with PYTHONDONTWRITEBYTECODE=1, PYTHONPATH=src/core/tests and supplied installed interpreter | Independent read-only reproduction | Passed, executed | Executed literal documented snippet; exact sample/hash/count/rates/bytes; ordered imported table; 15 added local links/anchors; append-only KB log; exact six-document tracked diff. No store/temp/private setting access or artifact output. |
| Reviewer source/test inspection | Behavioral truth of documentation | Completed | Directly compared consumer import/_shape/preflight/_quality/process, API, fixture, producer construction and representative semantic assertions for replay, conflict, withdrawal, retained corruption, rejection and partial failure. |
| git branch/status/rev-parse, diff --check, diff --quiet against pinned base | Branch and unchanged-source boundary | Passed, executed | Expected branch/base, six canonical tracked docs only; whitespace clean; relevant source/tests/agents/infra/tools/original/memory/ADRs unchanged. No remote access. |
| Configured static checks, application image, UI, actual SQL Server, Azure/live services | Unchanged runtime | Skipped, justified | Documentation-only diff and no new runtime assertion; no such new validation needed for bounded delivery. This is not new SQL Server/cloud acceptance. |

### Validation limitations

* Reviewer relied on the preserved final test receipt and exact execution command,
  with supporting source/test inspection; the 80-test suites were not rerun.
  This avoids unnecessary stores/output and does not mislabel inherited evidence
  as a newly executed independent test pass.
* Initial adverse CLI subprocess stderr is not included in its unittest traceback;
  its exact root cause is therefore not independently proven by that traceback
  alone. Other guard traces, source and successful unchanged final invocation
  support the recorded temp-root explanation; no acceptance-relevant gap remains.
* External issue/PR/owner-comment metadata is supplied research/caller evidence.
  No remote freshness, future frozen-head CI, full-PR acceptance, legal-source
  refresh, actual SQL Server, image, Azure, device or private dataset validation
  is claimed.
* An attempted shell rg inventory was unavailable (command not found); the
  dedicated read-only search tool supplied the inventory. No required comparison
  was omitted and no package/tool installation was performed by this reviewer.
* Documentation checks execute existing implementation seams and compare to
  dated results; they establish this public fixture, not a producer population,
  peak, byte bound, distribution, transport or live operational outcome.

## Outcome

* Outcome: Conformant.
* Rationale: all bounded goals, FR1-FR4, AC1-AC4 and completed AC5 stage obligations
  match source and evidence; P01/P02 completion is supported across all six
  canonical documents. The temp-root refinement is justified execution hygiene,
  not product divergence or code correction. Later AC5 publication is explicitly
  pending, not falsely completed or an implementation defect.
* Acceptance limit: bounded documentation conformance only. This does not accept
  whole186/110, stock/live compatibility, a not-yet-published PR or any operational
  approval gate. No issue criteria/closure/board changes are authorized here.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No later implementation invocation required by this Review |
| Decision gap or invalid in-scope assumption | None | No additional planning required for this bounded delivery |
| Material in-scope evidence gap | None | No additional research required for this bounded delivery |
| Non-blocking residual work | Existing FU-01/FU-02 | Retain distinct routes in Plan Follow-Up Assessment |

* Review execution: Complete.
* Bounded implementation execution: Complete.
* Outcome: Conformant.
* Validation: independently reproduced documentation checks; inspected unchanged
  80-test final pass and retained adverse run; no new backend suites or cloud work.
* Blockers: none for this bounded assessment.
* Next owner: automatic parent/coordinator for authorized draft publication and
  frozen-head/base evidence; full-PR acceptance, criteria and merge stay separate.

## Compared Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue186-message-contract-research.md](.copilot-tracking/research/2026-10-18/issue186-message-contract-research.md) | Research questions, primary source mapping and downstream boundaries |
| [.copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md](.copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md) | Goals, FR/ACs, completed markers, critique dispositions and follow-ups |
| [.copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md](.copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md) | Execution and validation details, including TMPDIR refinement |
| [.copilot-tracking/reviews/plans/2026-10-18/issue186-message-contract-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue186-message-contract-plan-critique.md) | One original Complete/Revise critique retained |
| [.copilot-tracking/changes/2026-10-18/issue186-message-contract-changes.md](.copilot-tracking/changes/2026-10-18/issue186-message-contract-changes.md) | Implementation completion and evidence reconciliation |
| [.copilot-tracking/rpi-sessions/2026-10-18/issue186-message-contract-state.json](.copilot-tracking/rpi-sessions/2026-10-18/issue186-message-contract-state.json) | Review-active automatic continuation state |
| [.copilot-tracking/rpi-sessions/2026-10-18/issue186-message-contract-execution.log](.copilot-tracking/rpi-sessions/2026-10-18/issue186-message-contract-execution.log) | Ordered commands, failures, refinement and final results |
| [.copilot-tracking/changes/2026-10-18/issue186-message-contract-measurement.log](.copilot-tracking/changes/2026-10-18/issue186-message-contract-measurement.log) | Actual public-fixture measurement |
| [.copilot-tracking/changes/2026-10-18/issue186-message-contract-doc-check.log](.copilot-tracking/changes/2026-10-18/issue186-message-contract-doc-check.log) | Parent documentation-check receipt |
| [.copilot-tracking/changes/2026-10-18/issue186-message-contract-tests.log](.copilot-tracking/changes/2026-10-18/issue186-message-contract-tests.log) | Original adverse 80-test/16-error output |
| [.copilot-tracking/changes/2026-10-18/issue186-message-contract-tests-final.log](.copilot-tracking/changes/2026-10-18/issue186-message-contract-tests-final.log) | Final unchanged 80-test pass |
| [.copilot-tracking/documentation/2026-10-18-issue186-session.md](.copilot-tracking/documentation/2026-10-18-issue186-session.md) | Scoped documentation authoring evidence |
| [docs/reference/research/iot-sensor-analytics-research-plan.md](docs/reference/research/iot-sensor-analytics-research-plan.md) | Canonical contract, measurement, reproduction and compatibility section |
| [src/core/README.md](src/core/README.md) | Core contract cross-reference |
| [src/api/README.md](src/api/README.md) | Finite API/transport distinction |
| [docs/case_study_48_addendum.md](docs/case_study_48_addendum.md) | Existing sensor-section integration |
| [docs/reference/README.md](docs/reference/README.md) | Knowledge-base routing update |
| [docs/reference/log.md](docs/reference/log.md) | Append-only knowledge-base change entry |
| [.copilot-tracking/reviews/logs/2026-10-18/issue186-message-contract-review.md](.copilot-tracking/reviews/logs/2026-10-18/issue186-message-contract-review.md) | This single original independent assessment |

## Next Steps

Return this one completed Review to the automatic parent. Coordinator may continue
the authorized draft publication and frozen-head/base inventory, then stop under
the supplied workflow. Retain FU-01/FU-02 for distinct downstream review/approval.
No correction, second Review or user response is required by this assessment.
Full-PR exact-head acceptance, issue criteria and merge remain coordinator-owned.
