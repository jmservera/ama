---
title: Sensor ingestion consistency original Review
ms.date: 2026-10-30
---

## Scope and Evidence

Task 188; one original post-implementation Review, dated 2026-10-30.
Plan/details/research/changes/critique use sensor-ingestion-consistency-188
under their canonical dated 2026-10-30 directories.
Assessed boundary: full bounded local implementation, not live Azure acceptance.

* Branch: feat/sensor-ingestion-consistency-188.
* Observed HEAD and supplied reviewed main base:
  a31048f15fa3120c58bacd22a375d86ae5ab7431.
* Candidate: tracked working-tree diff plus untracked new implementation/tests
  and original RPI evidence; not a committed or receipt-verified candidate.
* Read evidence: canonical research, plan, details, original critique and
  changes; all changed source, tests, manifests and documentation; immediately
  relevant backfill, observation, consumer, SQL fixture and receiver contracts.
* Validation evidence: parent-reported focused/static/migration results and
  directly inspected external API/SQL log summaries under
  /home/azureuser/.copilot/session-state/b669b987-2355-43d4-99ca-bf7c5c0215a9/files/validation-188.
* Acceptance basis: issue AC1 joint per-home live/backfill query, AC2 declared
  statistical handover tolerance and AC3 window rerun idempotency, evaluated
  only within the explicitly authorized local scope.

## Opening Review State

Goal: independent assessment of composed replay, strict statistical evidence,
SQL handover and replay, requirement/critique reconciliation and truthful gates.
Implementation markers reconciled; exact caller API discovery, project static
checks and actual owned SQL proof passed. Source changes and original artifacts
are available. Read-only boundary: source and phase evidence; write only this
canonical Review. No source fixes, second Review, Azure, deployment or push.
Initial residuals: actual live Hub/Azure SQL, complete committed-candidate gate
and hosted/human approval are not established.

* First comparison boundary: reconcile current P01/P02 markers and critique
  dispositions with the implemented generator/report and actual SQL selector;
  then assess what the negative controls and restart assertions establish.
* Initial blockers to this read-only Review: none. Live and publication
  prerequisites limit acceptance, not the ability to assess local evidence.
* Authority: no agents, source fixes, other artifact edits, test/gate execution,
  Azure, deployment, sign-in, credential files, commit or push.

## Execution Status

* Execution status: Complete.
* Review execution evidence: independently read and compared the full bounded
  candidate on 2026-10-30, including untracked sensor_consistency.py,
  test_sensor_handover.py and test_sensor_consistency.py. Inspected supplied
  API/SQL log summaries and ran only read-only Git checks.
* Planned implementation status: P01/P01-T01 and P02/P02-T01/P02-T02 complete
  within their reconciled implementation boundary. Original Review, candidate
  commit and final local gate are separate lifecycle steps; the last two have
  not completed. Whole issue acceptance is not complete.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Shared model and statistical contract | Reconciled | Optional composed inputs reuse full-origin readings; legacy defaults remain unchanged; strict reference-based report implemented. |
| P02 / P02-T01 | SQL/receiver proof and focused evidence | Reconciled | CSV prefix and SDK-decoded suffix are admitted and queried together for two homes; actual local SQL selection and reopened replay are explicit. |
| P02 / P02-T02 | Documentation, validation and Review readiness | Reconciled | Requested implementation tests/static checks recorded; owning guides and synthesis updated. Commit/full gate remain subsequent requirements, not checked acceptance. |
| Critique dispositions | Original Revise retained; PC-001/003 applied, PC-002 rejected | Reconciled | Concrete SQL selector and tolerance controls inspected; caller-specific lock/output direction explains the rejected recommendation without changing this Review's restrictions. |
| Follow-Up Items | Actual live Hub/Azure SQL after #110 and authority prerequisites | Reconciled | Mirrored in changes acceptance table and owning documentation; remains outside active implementation completion. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/synthetic/sensor_stream.py | Add optional climate/measures to replay and descriptor; preserve original RNG/model window before slicing. | _selected still validates actual synthetic/consent selection and scale first. _validate_model rejects measures without climate or unknown homes. Full-origin readings receive composed and dated-measure inputs. Descriptor history/hash and climate/model fields match the existing writer. | Existing replay controls plus new composed suffix and manifest comparisons; parent reports focused pass. | No implementation defect identified. Default outdoor generator, observation conversion, fault path, scale/rate controls and descriptor fields remain unchanged when optional inputs are absent. |
| P01-T01 | src/core/src/zava_forward/core/synthetic/sensor_consistency.py | Add strict per-home/sensor handover evidence with independent per-channel point, reference-adjusted mean-step and per-side population-stddev limits. | Lines 33-109 validate canonical shape, units/calibration, exact coverage/metadata, unique identities, unambiguous mapping, regular UTC cadence, boundary presence and at least two samples per side. Lines 111-167 compute each inclusive check and aggregate without masking individual failures. | New core negative controls exercise malformed/duplicate/missing data, identity/time/unit/schema changes, drift, invalid limits and independent metric failures. | Local model-parity claims supported. Reference adjustment correctly permits expected weather/works changes; this is not physical calibration or live-stream validity. |
| P02-T01 | src/core/tests/test_sensor_handover.py | Five new methods cover composed suffix/provenance and strict statistical semantics. | Boundary values 0.09/0.10/0.11 and 0.49/0.50/0.51; both channels; permissive other limits isolate each metric. Shared missing grid slot also fails. | Parent reports 27 focused core tests passed, including 12 existing stream and 10 writer tests. | Applied PC-003 is substantiated, not merely a positive zero-tolerance equality check. |
| P02-T01 | src/api/tests/test_sensor_consistency.py; src/api/tests/test_iot_stream.py | Persist actual writer CSV prefix plus EventData-decoded suffix through unchanged admission; extend existing fake receiver to composed climate. | New SQL method queries 12 rows for each of two canonical homes, including a long ID; trusted control units reconstruct observations. Reopened adapter replays all 24 rows, requiring accepted replay receipts and unchanged rows, delivery/DQ counts and cases/audit. | Directly inspected SQL log: 46 tests, OK; backend assertion resolves through SensorConsumer.mssql = isinstance(store, MssqlStore). API discovery also passed with skips recorded. | Local per-home query/statistics/restart claims supported. Constructed origin properties and fake transport do not authenticate a real Hub event. |
| P02-T01 | src/api/checks/sensor_sql_check.py | Include the exact handover method alongside the existing ingestion module on task-owned SQL Server. | Existing random loopback container/database, process-only connection settings, readiness and exact-name cleanup remain; both core/API test directories are importable. | Directly inspected log records responsive owned SQL Server, 46-test pass and owned-container removal. | PC-001 resolved. Standard full-gate SQL coverage is not substituted for this issue-specific selector. |
| P02-T02 | Owning READMEs; core/API pyproject.toml; docs/reference IoT synthesis/index/log | Document bounded evidence and test entry points; extend only test mypy overrides, with no dependency change. | Knowledge-base entry and append-only log agree with owning guides; no endpoint, transport, schema, approval or live-state change. Two new test files and six newly defined test methods fit plan limits; existing tests are not removed. | Parent reports owning-project Ruff/format/mypy and migration passes; current diff whitespace check passed. | Documentation and executable scope align; live/publication gates remain explicit. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 / PC-001 | Name concrete actual-SQL selector and owned execution route. | Original critique identified that ordinary discovery/full gate could leave sensor proof SQLite-only. | Plan disposition, phase details, helper selector, test backend assertion and final change evidence agree. | Applied compatible correction under original critique; no new scope decision. | Reconciled and executed. |
| P01-T01 / P02-T01 / PC-003 | Specify independent inclusive tolerance controls and invalid-limit tests. | Original critique identified equality-only and metric-masking risks. | Details, report comparisons and five core methods agree. | Applied compatible correction; original Revise preserved. | Reconciled and tested. |
| P02-T02 / PC-002 | Preserve caller's shared-lock and external-output instructions rather than worker recommendation. | Current caller explicitly confirms parent authority for those instructions; no authority transfers to this Review. | Rejection and rationale recorded in plan/changes; intermediate lock states retained, final test outcomes recorded. | Justified rejection against confirmed caller direction, not silent dismissal or retroactive critique replacement. | Supported within the supplied parent context. No lock/path operations were performed by this Review. |
| P02-T02 lifecycle sequencing | Checked task means documentation, implementation validation and readiness for original Review, not completion of Review/commit/gate. | Circular completion condition identified during implementation; user requires ordered RPI and local commit. | Plan handoff, phase index/task evidence and changes amendments all place Review, commit and complete gate afterward. | Clarification preserves accepted intent; no architecture, requirement or acceptance expansion requiring renewed planning/critique. | Reconciled. RV-002 retains the outstanding gate. |

## Critique and Material Revision Assessment

* Original critique remains Complete with verdict Revise and PC-001/002/003
  intact. This is the single post-implementation Review, not a second critique.
* PC-001 is resolved by the exact owned helper selector and inspected actual
  SQL pass; PC-003 is resolved by independent channel/metric controls,
  inclusive nonzero boundaries and invalid/nonfinite/boolean limit rejection.
* PC-002 rejection is explicitly attributed to confirmed caller direction.
  This Review neither re-executes that path nor relaxes its own prohibitions.
* No material new direction or invalid research assumption was identified.
  The sequencing clarification does not waive validation or turn a local
  substitute into live acceptance.
* No dependent-work resumption defect is evidenced: current artifacts contain
  the compatible critique corrections and show final validation afterward.
  This review does not certify an unrecorded historical edit-by-edit timeline.
* Earlier changes entries saying active, queued, pending or running are
  historical intermediate states, superseded by explicit final result and
  handoff sections, not additional current completion claims.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Actual live Hub/Azure SQL exercise after #110 | Explicit no-Azure/deploy/sign-in authority; constructed SDK/local SQL cannot prove actual transport, Azure joint query, statistical seam or restart. | Coordinator/owner retains distinct live follow-up and first establishes #110 readiness, action authority and budget evidence. | Open, correctly mirrored in changes and guides; RV-001. Not a source defect or newly active Pxx task. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Whole #188 acceptance still lacks actual live Hub/Azure SQL evidence

* Related scope: AC1, AC2, AC3; plan Follow-Up Items.
* Evidence: src/api/tests/test_sensor_consistency.py:61-100 constructs CSV and
  EventData origin properties locally; lines 102-154 prove queries/statistics
  and reopened replay on the selected local backend. The owned SQL helper
  selects loopback SQL Server, not Azure SQL. Plan/changes acceptance tables
  and both owning guides explicitly preserve actual live evidence as unproven.
* Impact: the bounded engineering implementation is supported, but none of
  these local substitutions proves the actual live portions of the three
  issue criteria. Whole-issue conformance or issue closure would overstate
  evidence. This is a declared residual, not an implementation defect.
* Destination: distinct existing live follow-up, coordinator/owner; no active
  rpi-implement, rpi-plan or rpi-research handoff is needed for the local task.
* Smallest useful next action: retain Refs #188 and all live criteria unmet;
  consider a separately authorized exercise only after #110 readiness,
  explicit authority and complete budget/prerequisite evidence. Do not execute
  it under this task.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Publication evidence is pending for the committed exact candidate

* Related scope: P02-T02 subsequent lifecycle gates; repository local RPI policy.
* Evidence: HEAD is still the supplied base and implementation/original evidence
  are uncommitted. Changes handoff and reconciled plan/details expressly place
  complete gate execution after this original Review and local commit.
  Inspected api-tests.log and sql-tests.log establish their named suites only;
  no complete external receipt or current-main verification is present.
* Impact: focused, API and issue-specific local SQL passes are not a complete
  committed-candidate receipt, independent exact-head publication assessment,
  hosted approval or human approval. The pending gate is expected sequencing,
  not a failed check or reason to relabel checked implementation tasks.
* Destination: active parent/coordinator's subsequent local candidate and
  publication-validation lifecycle; no source-fix handoff.
* Smallest useful next action: preserve this original Review and critique,
  then perform the authorized privacy-safe local commit. Run the required
  complete gate with external output only in the permitted parent context,
  using the reviewed base and recording actual results. Keep unavailable
  prerequisites blocked; verify a fresh receipt against current origin/main
  before any separately authorized publication/exact-head assessment.
  The no-push instruction remains binding.

## Defects

* No actionable implementation defect identified in the assessed candidate.
* In particular, no default legacy replay regression or admission-control
  weakening is evidenced. Existing consumer/receiver controls remain in place;
  the optional generator input is not a bypass around them.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct existing live follow-up | Coordinator/owner retains unmet live criteria; separately authorize prerequisites/exercise if later desired. | Known out-of-scope live evidence, not a new local defect or research task. |
| RV-002 | Parent's subsequent candidate/publication validation | Local commit, complete external gate and current-base receipt verification in a compliant authorized context; no push. | Expected lifecycle condition, not implementation acceptance or a passed gate. |

Later implementation of a routed finding does not require another original
Review. Separate exact-head publication policy is not waived by this statement.

## Residual Work

* RV-001 retains the plan's distinct live follow-up and its owner/prerequisites.
* RV-002 retains local commit/full-gate continuation and all later hosted,
  independent exact-head and human publication conditions.
* Physical model validity and sensor calibration are not claimed by this
  synthetic parity report and were not added to local acceptance scope.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active implementation work: none identified.
* Whole-issue live acceptance: unproven and unavailable under current authority;
  clearing it requires distinct authorized live follow-up, not cloud fallback.
* Publication readiness: not established until the subsequent committed
  candidate and required complete external gate/verification are evidenced.
  Missing prerequisites must remain blockers, not skips portrayed as passes.
* No hosted checks or human approval were obtained or inferred. No push is
  authorized, even if later local checks pass.

## Validation Evidence

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| Parent focused core unittest run | Five handover, twelve existing stream and ten composed writer tests | Passed, parent-recorded | 27 tests in 1.602s; not rerun by reviewer. Source controls independently inspected. |
| From src/api, PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q | Owning API regression suite | Passed with recorded skips | Inspected external api-tests.log: 1,408 tests in 492.700s, OK, 318 skips; skipped cases are not executions or live proof. |
| Task-owned src/api/checks/sensor_sql_check.py under parent lock | Existing ingestion suite plus exact new SqlHandoverTests method | Passed | Inspected external sql-tests.log: responsive owned loopback SQL Server, 46 tests in 20.649s, OK, exact owned container removed. Helper/source assertion establish MssqlStore selection. |
| Owning-project Ruff check, Ruff format --check and mypy | Core/API source and tests | Passed, parent-recorded | Changes record reports both projects passed; reviewer did not repeat static commands or independently attest every external static log. |
| python3 tools/rename-zava-tests.py in restored pinned-tool environment | Migration regressions | Passed, parent-recorded | 25 tests after missing pinned tool dependencies restored; initial missing-dependency failure preserved in changes. |
| git diff --check | Current tracked candidate diff | Passed, reviewer-executed | No whitespace errors; untracked source was read directly, not assumed present in Git diff. |
| Complete tools/rpi-checks.py --all committed-candidate run and --verify-receipt | Full local publication gate | Unavailable at this Review boundary | Intentionally subsequent to original Review/local commit. No receipt or approval claimed; RV-002. |
| Actual authenticated Hub transport, Azure SQL joint query/handover/restart | Live portions of AC1/AC2/AC3 | Unavailable | Explicit no-Azure/sign-in/deploy authority; RV-001. |
| Hosted checks, independent exact-head publication assessment and human approval | Subsequent publication/merge gates | Unavailable | Not performed or satisfied by this working-tree Review. |

No application tests, heavy gates, container operations or credential-file
reads were performed by this reviewer.

## Outcome

* Outcome: Residual work.
* Outcome rationale: the full bounded local implementation and negative
  controls substantiate common per-home queries, reference-adjusted declared
  handover tolerances and reopened whole-window idempotency on constructed
  SQLite/local SQL Server, with legacy replay and existing admission preserved.
  No source defect was identified. RV-001 and RV-002 prevent whole-issue or
  publication conformance claims.
* Review execution Complete is separate from this residual outcome and from
  incomplete live acceptance/publication lifecycle.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement handoff justified. |
| Decision gap or invalid assumption | None | Reconciled direction and caller-specific critique disposition do not need a new rpi-plan invocation. |
| Material in-scope research evidence gap | None | Known excluded live evidence does not require more local discovery or rpi-research. |
| Non-blocking residual work | RV-001 distinct live follow-up; RV-002 parent lifecycle | Coordinator/owner retains live prerequisites; parent preserves original evidence and continues local commit/gate without push. |

* Execution status: Complete.
* Outcome: Residual work.
* Finding summary: two Medium residual/lifecycle findings; no implementation
  defects found.
* Validation coverage: supplied local focused/API/static/migration and actual
  task-owned SQL passes considered within their stated boundaries; API/SQL
  summary logs and source controls independently inspected; no heavy reruns.
* Blockers: no blocker to Review completion. Live authority/evidence and
  committed-candidate publication prerequisites remain unmet.
* Decision need: none for the accepted local direction. This Review neither
  authorizes live work nor requests a second critique or original Review.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/sensor-ingestion-consistency-188-research.md](.copilot-tracking/research/2026-10-30/sensor-ingestion-consistency-188-research.md) | Research basis and local/live boundary. |
| [.copilot-tracking/plans/2026-10-30/sensor-ingestion-consistency-188-plan.md](.copilot-tracking/plans/2026-10-30/sensor-ingestion-consistency-188-plan.md) | Reconciled plan, markers, critique dispositions and follow-up. |
| [.copilot-tracking/details/2026-10-30/sensor-ingestion-consistency-188-phase-details.md](.copilot-tracking/details/2026-10-30/sensor-ingestion-consistency-188-phase-details.md) | Detailed task contracts and lifecycle clarification. |
| [.copilot-tracking/reviews/plans/2026-10-30/sensor-ingestion-consistency-188-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/sensor-ingestion-consistency-188-plan-critique.md) | Original Revise and PC-001/002/003 preserved. |
| [.copilot-tracking/changes/2026-10-30/sensor-ingestion-consistency-188-changes.md](.copilot-tracking/changes/2026-10-30/sensor-ingestion-consistency-188-changes.md) | Implementation history, validation outcomes and bounded acceptance evidence. |
| [.copilot-tracking/reviews/logs/2026-10-30/sensor-ingestion-consistency-188-review.md](.copilot-tracking/reviews/logs/2026-10-30/sensor-ingestion-consistency-188-review.md) | This single canonical original Review. |
| [src/core/src/zava_forward/core/synthetic/sensor_stream.py](src/core/src/zava_forward/core/synthetic/sensor_stream.py) | Optional composed replay and descriptor. |
| [src/core/src/zava_forward/core/synthetic/sensor_consistency.py](src/core/src/zava_forward/core/synthetic/sensor_consistency.py) | Strict statistical report. |
| [src/core/src/zava_forward/core/synthetic/sensor_backfill.py](src/core/src/zava_forward/core/synthetic/sensor_backfill.py) | Existing shared writer/model contract. |
| [src/core/src/zava_forward/core/sensor_consumer.py](src/core/src/zava_forward/core/sensor_consumer.py) | Unchanged observation/admission/backend contract. |
| [src/core/tests/test_sensor_handover.py](src/core/tests/test_sensor_handover.py) | New semantic and negative controls. |
| [src/core/tests/test_sensor_stream.py](src/core/tests/test_sensor_stream.py) | Existing legacy replay, scale and budget controls. |
| [src/core/tests/sensor_consumer_fixture.py](src/core/tests/sensor_consumer_fixture.py) | Independent controls and SQLite/MSSQL store selection. |
| [src/core/tests/test_sensor_consumer.py](src/core/tests/test_sensor_consumer.py) | Existing durable admission and snapshot assertions. |
| [src/api/tests/test_sensor_consistency.py](src/api/tests/test_sensor_consistency.py) | Joint query/statistics/reopened full-window proof. |
| [src/api/tests/test_sensor_ingestion.py](src/api/tests/test_sensor_ingestion.py) | Existing API admission regressions selected by owned helper. |
| [src/api/tests/test_iot_stream.py](src/api/tests/test_iot_stream.py) | Composed fake receiver seam and origin negative controls. |
| [src/api/checks/sensor_sql_check.py](src/api/checks/sensor_sql_check.py) | Concrete task-owned local SQL selector. |
| [src/core/pyproject.toml](src/core/pyproject.toml) | Core test-only typing override update. |
| [src/api/pyproject.toml](src/api/pyproject.toml) | API test-only typing override update. |
| [src/core/README.md](src/core/README.md) | Owning replay/statistical contract. |
| [src/api/README.md](src/api/README.md) | Owning SQL proof commands and limitations. |
| [docs/reference/research/iot-sensor-analytics-research-plan.md](docs/reference/research/iot-sensor-analytics-research-plan.md) | Durable bounded evidence synthesis and live deferral. |
| [docs/reference/README.md](docs/reference/README.md) | Updated knowledge-base index. |
| [docs/reference/log.md](docs/reference/log.md) | Append-only knowledge-base change entry. |
| [src/README.md](src/README.md) | Candidate gate and publication policy. |

## Next Steps

Return this one Review to the active parent. Preserve the original critique
and Review, then continue the authorized privacy-safe local commit and required
external complete-candidate gate/receipt lifecycle in the parent's permitted
context. Record any unavailable prerequisites truthfully. No source-fix,
new planning/research phase, second original Review or user decision is
requested by this assessment. Retain the distinct live follow-up, use
Refs #188 only, and do not push or execute Azure work.
