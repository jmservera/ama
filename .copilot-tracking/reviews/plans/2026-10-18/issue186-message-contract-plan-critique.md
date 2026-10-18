<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue186 shared message contract and volume

## Metadata

* Task ID: issue186
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md
* Research: .copilot-tracking/research/2026-10-18/issue186-message-contract-research.md
* Critique execution status: Complete
* Assessment: exactly one independent final-candidate critique; not implementation or the original Review.

## Inputs and Criterion Boundary

* Caller requirements take precedence: bounded documentation and unchanged-consumer verification on docs/sensor-message-contract-186 at base 100ead1bacdb72a8ea7ce5867233db30b22b2f50. No runtime, producer, schema, store or test edits; maximum new tests zero and no removals. No private data, cloud access, packetization adoption or live acceptance claims.
* Reviewed the complete supplied plan, details and research; read project original/context, relevant addendum sections, KB index/memory and housing-association primer.
* Verified relevant primary evidence in src/core/src/zava_forward/core/sensor_consumer.py, src/api/src/zava_forward/api/sensor_ingestion.py, src/core/src/zava_forward/core/synthetic/sensor_faults.py, src/core/src/zava_forward/core/synthetic/sensor_stock.py, src/core/src/zava_forward/core/synthetic/sensor_backfill.py, src/core/tests/sensor_consumer_fixture.py, src/core/tests/test_sensor_consumer.py, src/api/tests/test_sensor_ingestion.py and src/core/tests/test_sensor_faults.py. Checked SQL backend selection against src/core/src/zava_forward/core/mssqlstore.py and src/core/src/zava_forward/core/sqlstore.py.
* Checked existing documentation homes in docs/reference/research/iot-sensor-analytics-research-plan.md and docs/case_study_48_addendum.md, and accepted status/history in docs/adrs/0003-journey-derived-capabilities-runtime-fit.md.
* Contract dependency #110 is satisfied by merged #411 according to supplied research and caller direction; whole-issue #110/live gates remain separate. Downstream #187/#188 compatibility is explicitly deferred, not a documentation blocker.
* Assessed FR1-FR4, non-functional requirements, AC1-AC5, P01/P02, all three implementation tasks, six canonical documentation targets, test ownership, dependencies, measurement/reproduction and later lifecycle boundaries.
* This assessment establishes plan credibility, not test success, actual measured bytes, final documentation correctness, PR status or live readiness. No git operation, cloud call, test execution, implementation or subagent dispatch was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1; AC1; research C1/C5; P01-T02 | Covered | Consumer imports READING_FIELDS and SCHEMA_VERSION from synthetic.sensor_faults. Details require all 13 strings, exact identity/number/seed/time rules, units, closed observation shape and separate envelope/control checks. |
| FR2; AC2; research C2/C6/C8; P01-T02 | Covered | process preserves exact accepted historical replay, validates retained witness/reading, rejects changed content under an occupied stable key and does not overwrite. API exposes completed prefix on failure; details prohibit atomic-batch claims. |
| FR3; AC3; research C3/C5/C7/C10; P01-T01 | Covered | Unchanged observations()[0], sorted ASCII JSON/default separators/no newline, byte length/hash, imported authority and shape assertions, exact Fraction rates and executed B-times-3N accounting. Actual results correctly belong to implementation. |
| FR4; AC4; research C9/C11; P01-T02 | Covered | Stock prefix plus full lowercase SHA-256 gives 73-character IDs and embedded reading IDs exceed 40. Plan explicitly prohibits remapping/truncation/relaxation and separates #187/#188 decisions. |
| FR3/FR4; P01-T02 | Covered | Three paired records, not six scalar records; N=1 and fictional N=60,000; finite API batches distinct from conditional wire counts and unmeasured Hub billing/throughput. No packetization choice. |
| Documentation scope; P01-T02 | Covered | Exactly six existing canonical Markdown targets, current synthesis section before dated privacy history, KB index and append-only log. Existing ADR accepted status and historical Proposed wording remain intact. |
| Non-functional offline/no-private-access boundary; P02-T01 | Partial | Unchanged suites have meaningful semantic coverage, but the literal command inherits a backend-selection flag capable of selecting SQL Server: PC-001. |
| Non-functional execution boundary; P02-T01 | Partial | Suites use default TemporaryDirectory locations; no repository-local tempfile root is specified: PC-002. |
| Test change lock; AC2; P02-T01 | Covered | Existing core/API/fault suites exercise admission, replay, conflict, refusal and partial failure without any proposed test additions/removals or runtime tools. |
| AC5; dependencies and lifecycle | Covered | One critique, direct dispositions, implementation then one original Review. Coordinator owns subsequent exact-head whole-PR review and merge; no second Review, live acceptance or closure is inferred. |

## Verdict

* Verdict: Revise
* Rationale: Contract, measurement, documentation scope and acceptance boundaries are substantively ready. The planned verification command needs explicit execution isolation before it can honor the no-cloud and repository-local file restrictions. Both findings are direct planner corrections, not significant or divergent decisions.
* Severity summary: Critical 0; High 1; Medium 1; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Pin the semantic suites to the offline SQLite fixture

* Related IDs: non-functional offline/no-private-access requirements; AC2; P02-T01; research C7/C8.
* Evidence: .copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md, P02-T01 gives only PYTHONPATH and the unittest invocation. src/core/tests/sensor_consumer_fixture.py, store_at selects MssqlStore when inherited ZF_SENSOR_MSSQL equals "1", uses connection_string() and, with reset=True, deletes cases. src/core/tests/test_sensor_consumer.py, setUp calls store_at(..., reset=True) and additionally drops sensor tables on that backend. src/api/tests/test_sensor_ingestion.py inherits the same setup. src/core/src/zava_forward/core/mssqlstore.py, connection_string reads inherited ZF_SQL settings.
* Concern: The planned command is not unconditionally offline. A task-owned virtual environment isolates packages, not environment variables; an inherited opt-in flag can route these tests to an externally configured database and invoke destructive fixture setup. No evidence establishes that the flag is currently enabled; the concern is the command's conditional behavior, not a claim of actual access.
* Impact: Execution can violate the explicit no-cloud/private-environment boundary and mutate an unintended database, despite a documentation-only change.
* Smallest useful change: Amend P02-T01's literal command and verification instructions to force ZF_SENSOR_MSSQL=0 for the complete core/API/fault invocation, with the same pin on any additional admission/replay reproduction using store_at. Explicitly prohibit probing connections or reading/printing inherited SQL credentials. Retain all existing suites unchanged.
* Action owner: Planning parent; implementation worker applies the pinned invocation.
* Exact resolving evidence: Plan/details contain the SQLite-only environment prefix; implementation changes record reproduces that exact invocation and reports local SQLite results without any actual SQL Server/cloud run. Source inspection of store_at proves that the explicit value "0" cannot select its MssqlStore branch.
* Decision route: Direct planner correction. Existing user direction already resolves backend choice; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Route test temporary files into approved repository-local scratch

* Related IDs: non-functional execution/change boundary; P02-T01; test ownership and change lock.
* Evidence: .copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md, P02-T01 specifies no tempfile directory override. src/core/tests/test_sensor_consumer.py, setUp uses tempfile.TemporaryDirectory() without dir. src/core/tests/test_sensor_faults.py repeatedly uses the same default and launches subprocesses inheriting its environment. The task's execution constraints prohibit /tmp and /var/tmp file operations and allow project-local scratch.
* Concern: The literal suite invocation leaves tempfile destination to ambient configuration/platform defaults, which may select a prohibited system directory. Installing a task virtual environment does not change tempfile's directory selection.
* Impact: Otherwise appropriate validation may fail the execution restrictions or write fixture databases/generated fault artifacts outside the allowed repository-local area.
* Smallest useful change: Specify an issue-owned scratch directory beneath .copilot-tracking, created using a repository-relative path, and set TMPDIR to its absolute repository-local location before starting Python. Apply this to the full selected suite command and any reproduction creating SQL fixtures. Require cleanup of generated scratch contents and ensure they are excluded from the committed delivery. Do not change tests or add tooling.
* Action owner: Planning parent; implementation worker owns scratch setup and cleanup.
* Exact resolving evidence: P02-T01 includes the repository-local scratch setup, TMPDIR-prefixed command and cleanup requirement. The implementation execution record identifies the effective tempfile root beneath the worktree and records cleanup; final inventory contains only the approved documentation and issue186 evidence artifacts, not generated fixture stores.
* Decision route: Direct planner correction. This changes execution hygiene only, not feature scope or the test-addition budget; no user response required.

## Strengths and Residual Risk

* Shared authority is correctly an existing import, not a proposed replacement schema. Source constraints and independent controls are kept separate; no shape assertion is mistaken for operational admission.
* Replay and rejection evidence is genuinely semantic: existing tests verify persisted counts, unchanged authoritative readings, reopened-store replay, withdrawn controls, owned DQ and uncertain acknowledgement recovery.
* Byte reproduction reuses the current public fixture and existing digest serialization, with an explicit sample-not-bound caveat. The exact mean rates are correct: 3/86400 = 1/28800 and 180000/86400 = 25/12 observations/second.
* The fixture's two-observation evaluator packet does not establish scheduling or transport policy; details correctly keep those separate from three paired observations/home/day.
* Stock/consumer incompatibility is candid and intentionally unresolved here. The 60,000-home case scale is an accounting population, not evidence of 60,000 configured devices/controls.
* ADR 0003 already records 2026-10-15 acceptance with the Basic exercise amendment and preserves Proposed history. No new ADR or approval correction is warranted.
* Live identity, transport, throughput, billing, real AI, privacy, human approval and Azure application acceptance remain explicitly accepted exclusions. No additional implementation scope or acceptance gate is recommended by this critique.

## Questions or Blocking Evidence Gaps

* None requiring user input or additional research. The two execution safeguards are actionable from supplied source evidence.
* No blocker to bounded documentation after direct disposition of PC-001 and PC-002. Subsequent implementation results and original Review remain future gates, not evidence missing from this planning assessment.

## Limitations

* No tests or reproduction commands were executed and no byte measurement was generated; doing so is implementation work and would violate this worker's write boundary.
* Branch/base, merge metadata and external issue/owner decisions are accepted from the supplied caller/research record. They were not rechecked using git or GitHub; git operations were expressly forbidden.
* The assessment does not inspect private environment values, datasets, support material or cloud endpoints. Findings identify unsafe conditional execution paths without asserting that those paths were activated.
* This is the complete actionable finding set for the supplied final-candidate boundary. No additional critique pass or original Review was performed or requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Directly pin the verification backend and repository-local tempfile root in P02-T01, record both dispositions and finalize the plan without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md](.copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md) | Final-candidate plan assessed; unchanged by this worker. |
| [.copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md](.copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md) | Phase details requiring direct execution-safety corrections. |
| [.copilot-tracking/research/2026-10-18/issue186-message-contract-research.md](.copilot-tracking/research/2026-10-18/issue186-message-contract-research.md) | Supplied evidence and dependency boundary. |
| [.copilot-tracking/reviews/plans/2026-10-18/issue186-message-contract-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue186-message-contract-plan-critique.md) | Complete single critique and actionable finding set. |

## Next Steps

Active planning parent directly disposes PC-001 and PC-002, finalizes without another critique, then continues the authorized automatic RPI sequence. Implementation and the one original Review occur later; the coordinator retains exact-head whole-PR review and merge ownership. No user action is required.
