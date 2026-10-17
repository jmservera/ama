<!-- markdownlint-disable-file -->
# RPI Plan Critique: Sensor privacy boundary

## Metadata

* Task ID: 112; slug: sensor-privacy-boundary-112.
* Critique date: 2026-10-17.
* Assessed base: 74617981b71bc3f10bd21d0b78691bc3cf36c473.
* Branch: fix/sensor-privacy-boundary-112.
* Plan: .copilot-tracking/plans/2026-10-17/sensor-privacy-boundary-112-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/sensor-privacy-boundary-112-phase-details.md
* Critique execution status: Complete.
* Execution count: one final-candidate critique; no further critique performed.

## Inputs and Criterion Boundary

* Caller requirements: exclude raw observations and device identifiers from actual AI, map, cluster and log boundaries; admit only verifiably generated observations, default-denying real/unknown input. Labels, filenames, pseudonymization and hashes alone do not establish synthetic origin.
* Preserve authorized manual detail, hazard and quality routes, current-actor checks and finance controls. Do not introduce broad service holds, sensor AI purposes, health thresholds, consent or legal authority.
* Inputs: the plan, matching phase details and .copilot-tracking/research/2026-10-17/sensor-privacy-boundary-112-research.md, particularly C1-C9. Repository context read: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md.
* Evidence verification was confined to local implementation and tests named by those inputs, including the referenced stock destination and provenance helpers. No external research, live/private datasets, cloud operations or other worktrees were used.
* Decisions assessed: deterministic current-generator replay; original manifest/hash comparison; loading replay-owned bytes; explicit caller-supplied stock Selection; closed chat projection; scalar legacy AI/map validation; no new sensor-analysis runtime or registered AI purpose.
* Dependencies: P01-T01 supplies failing-first boundary evidence for P01-T02; P02-T01 verifies and documents that implementation. Parent #109 is hierarchy only. Shared-file overlap with #88/#102 is acknowledged, not a new dependency.
* Test ownership is locked: src/core/tests/test_sensor_privacy.py, at most 18 new test methods, no removals. Existing test_sensor_stock.py may pass explicit stock arguments. Findings below must fit that budget through subtests/helpers, not transfer tests to another component.
* This is an implementation-credibility assessment, not an implemented privacy guarantee, legal approval, platform acceptance or broad security audit.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Synthetic-only admission; C1-C3; P01-T02 | Partial | Exact replay and original manifest/payload checks are materially stronger than labels or rehashing; scratch execution and parameter limits need correction, PC-001/PC-002. |
| Replay-owned bytes; explicit stock Selection; P01-T01/T02 | Partial | Correct design is stated, but source-mutation and stock-binding regression oracles are not committed, PC-003. |
| AI/chat exclusion; C4-C5/C7; P01-T01/T02 | Covered | Actual ChatIsolation/ChatPanel captures, closed authorized fields and rejection before container stringification are planned. Existing assistant scalar capture is retained. |
| Map points/clusters; C6/C8; P01-T01/T02 | Covered | Explicit display fields, malformed scalar refusal and forced-cluster payload checks address the observed seams without changing static tiles. |
| Logs and refusal output; P01-T01/T02 | Covered | Fixed refusal messages and no exception traceback/value echo are explicit; captured logs are an acceptance surface. |
| Manual detail and existing domain controls; P01-T02 | Covered | Boundary-only projection, no stored-record mutation, no broad service hold or finance/hazard/quality authority changes. |
| No existing sensor analysis or registered purpose; C9 | Covered | Deferral of new indicators and human-owned real-use prerequisites is appropriate, not an omitted runtime feature. |
| Regression validation/docs; P02-T01 | Partial | Component tests, configured checks, documentation and unperformed MSSQL disclosure are proportionate; scratch/test execution constraints need PC-001. |
| Candidate lock and handoff | Covered | Core ownership, maximum 18 methods, no removals, explicit stock test-call updates and one retained original Review are recorded. |

## Verdict

* Verdict: Revise.
* Severity summary: zero Critical, one High, two Medium, zero Low.
* Rationale: the selected boundary design is credible, but its literal replay procedure conflicts with the permitted execution environment, its claim of bounded replay parameters exceeds the cited validation, and its test plan does not yet prove two central replay guarantees. These are direct planner corrections; no user decision is required.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Resolve the replay scratch strategy without weakening the public stock-output guard

* Related IDs: C3; P01-T02; P02-T01; valid normal/stock replay acceptance.
* Evidence: .copilot-tracking/details/2026-10-17/sensor-privacy-boundary-112-phase-details.md:26-30 specifies reuse of write() under TemporaryDirectory. src/core/src/zava_forward/core/synthetic/sensor_backfill.py:195-215 routes stock generation through stock_fabric._destination(). src/core/src/zava_forward/core/synthetic/stock_fabric.py:308-319 rejects every repository-contained stock output. src/core/tests/test_sensor_stock.py:test_destination_and_refresh_refusal_precede_payload_writes explicitly preserves that refusal. The execution instructions prohibit temporary directories and require created files to remain relative to the current worktree.
* Concern: default TemporaryDirectory is not an executable choice here. Merely relocating it beneath this worktree still makes public write(stock=...) refuse. The plan supplies no compatible internal rendering path and P02 also runs existing tempfile-based tests without an execution arrangement.
* Impact: the implementation cannot literally deliver and validate stock replay as planned without either violating execution constraints or weakening an existing stock-output safeguard.
* Smallest useful change: specify a worktree-local, non-committed execution-artifact location and an internal replay rendering path that preserves the public CLI/write destination guard. If required, factor only the shared deterministic rendering into an internal helper; do not relax the public stock destination refusal. State how test scratch paths are routed into permitted worktree-local execution artifacts, cleaned up and excluded from commits. Do not authorize external/private locations or use TemporaryDirectory as a workaround.
* Action owner: planning parent, with the P01-T02/P02-T01 implementer.
* Exact resolving evidence: revised details name the compatible internal replay procedure and test execution setup; implementation evidence subsequently shows valid normal and supplied-stock replay/load/idempotency, retains the stock repository-output refusal test, uses no forbidden filesystem location, and leaves no generated snapshot committed.
* Decision route: direct planner correction. Current execution constraints and preservation requirements already determine the boundary; no user response or new legal authority is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Define replay parameter validation before expensive generation

* Related IDs: C3; P01-T02; malformed-manifest refusal; replay resource risk.
* Evidence: .copilot-tracking/details/2026-10-17/sensor-privacy-boundary-112-phase-details.md:27-28 calls manifest parameters bounded by existing window validation. src/core/src/zava_forward/core/synthetic/sensor_backfill.py:137-149, resolve_window(), checks positive days/cadence, cadence divisibility and calendar representability, not a practical replay work budget. write() and outdoor_series() generate from caller-controlled counts before manifest equality can reject an altered candidate.
* Concern: calendar validity does not bound rows, memory or disk to a practical replay envelope, and the plan does not specify strict parameter types or a pre-generation work limit. A valid-looking manifest with excessive days/home counts can trigger substantial replay before eventual mismatch refusal.
* Impact: default-denial can still consume uncontrolled local resources before rejecting malformed/unknown input. The stated bounded-replay property is not supported by its cited helper.
* Smallest useful change: define strict types and a checked pre-generation work estimate covering homes, steps and output volume, including stock coverage. Specify an explicit supported offline replay envelope or caller-selected budget with a conservative default; reject out-of-envelope inputs with fixed messages before rendering or SQL. Preserve supported existing fixtures and document larger-snapshot handling. This is a computational limit, not a new sensor-health threshold or service hold.
* Action owner: planning parent, with the P01-T02 implementer.
* Exact resolving evidence: revised details identify the accepted parameter schema, resource-limit policy and rejection order; parameterized core tests prove malformed types and over-budget candidates do not invoke the renderer, schema hook or connection execute, while supported tiny normal/stock fixtures still pass.
* Decision route: direct planner correction within the selected replay approach. No significant/divergent user choice is needed; do not invent an operational monitoring threshold.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Lock replay race and explicit-stock binding into the boundary test matrix

* Related IDs: P01-T01/T02; original manifest/hash verification; replay-owned bytes; explicit stock Selection.
* Evidence: .copilot-tracking/plans/2026-10-17/sensor-privacy-boundary-112-plan.md:48-49 requires replay-owned bytes specifically to avoid races. Details:18-20 enumerate missing/real/unknown, rehashed payload, register/revision tampering and valid replay, but no controlled mutation after validation or missing/mismatched supplied Selection oracle. Research Cycle 1, Wave 3 explicitly identifies reopening mutable originals as the race to avoid.
* Concern: the specified tampering tests can all pass in an implementation that verifies a source once and then reopens original files for SQL loading. A happy-path stock test with an added explicit argument likewise does not establish refusal when the argument is absent, different or inferred from untrusted snapshot content.
* Impact: a central admitted-byte guarantee and the caller-authorized stock binding could regress while the named acceptance suite remains green.
* Smallest useful change: add explicit parameterized scenarios within the locked core test file: mutate/replace an original shard and sensors.csv at a deterministic hook after comparison but before persistence and prove only captured replay bytes reach SQL; refuse missing or nonmatching stock Selection before any schema/execute call. Verify original payload mismatch with an unchanged original manifest as well as a rehashed malicious manifest. Do not infer Selection from manifest/stock-fabric bytes.
* Action owner: planning parent and P01-T01 test author.
* Exact resolving evidence: revised test matrix names the hook and SQL-parameter oracle; subsequent failing-first/corrected test results demonstrate no original-source reopen after verification, no sentinel in inserted parameters or logs, and zero SQL/schema calls on missing/mismatched Selection. Tests remain in src/core/tests/test_sensor_privacy.py with at most 18 methods and no removals.
* Decision route: direct planner correction; no user response required.

## Strengths and Residual Risk

* Exact comparison to current deterministic generator output, followed by loading replay-owned bytes, is a defensible construction check. Rehashing arbitrary real observations cannot satisfy it merely by changing a classification label.
* Requiring independently supplied stock Selection avoids silently rebuilding stock authority from candidate files. It does not prove real stock identity, consent, source truth or legal authority; the plan correctly preserves that distinction and #175's unresolved origins.
* Closed source-authorized chat fields address recursion without speculative sensor-key matching or deletion from authorized manual detail. Scalar checks must occur on raw selected values before interpolation or citation serialization, including legacy briefing/priority paths, not after a dictionary has become a string.
* Normal map filtering, bounds and forced clusters must retain existing semantics. Rejection must remain scoped to the malformed export, never a mutation of hazard/quality/manual service state.
* Free prose remains outside semantic DLP guarantees. The supplied candidate explicitly discloses that limit; this critique does not reopen it as a new feature.
* Current-revision regeneration, replay time/disk cost and unperformed live/MSSQL acceptance remain disclosed limits, not approvals or successful results.

## Questions or Blocking Evidence Gaps

* No unresolved user decision or decision-critical external research gap. The local evidence supports this Revise verdict.
* The parent should resolve all three findings directly and finalize without another critique, as required for this single final-candidate pass.

## Limitations

* Static evidence assessment only. No application tests, replay, private snapshot loads, model calls, SQL Server or deployments were executed.
* No independent retrieval of the current GitHub issue body or other branches was performed; caller requirements and the supplied research define the issue boundary.
* The three supplied artifacts were already untracked when inspected. They and all source files remain unchanged; this critique is the only file written by this execution.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: replace the incompatible TemporaryDirectory/public stock-write procedure with a permitted internal replay rendering and test-scratch plan, then incorporate PC-002/PC-003 into the same finalization.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/sensor-privacy-boundary-112-plan.md](.copilot-tracking/plans/2026-10-17/sensor-privacy-boundary-112-plan.md) | Assessed final-candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-17/sensor-privacy-boundary-112-phase-details.md](.copilot-tracking/details/2026-10-17/sensor-privacy-boundary-112-phase-details.md) | Assessed phase details, unchanged |
| [.copilot-tracking/research/2026-10-17/sensor-privacy-boundary-112-research.md](.copilot-tracking/research/2026-10-17/sensor-privacy-boundary-112-research.md) | Supplied C1-C9 evidence and residual limits, unchanged |
| [.copilot-tracking/reviews/plans/2026-10-17/sensor-privacy-boundary-112-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/sensor-privacy-boundary-112-plan-critique.md) | Complete single-pass critique |

## Next Steps

The active planning parent resolves PC-001 through PC-003 directly, preserves the test ownership/budget and original critique, and finalizes its plan without another critique. No user action is required. This critique execution stops here; no implementation or peer stage is invoked.
