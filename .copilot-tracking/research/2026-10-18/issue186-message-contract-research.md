<!-- markdownlint-disable-file -->

# Task Research: issue186-message-contract

| Field | Value |
| --- | --- |
| Date | 2026-10-18 |
| Researcher / agent | RPI coordinator / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-18/issue186-message-contract-research.md |

## Research Brief

* What: verify the unchanged paired-observation contract used by the merged
  issue 110 consumer and identify the existing documentation home for issue 186.
* Why / audience: support downstream implementers and coordinator review without
  asserting live producer interoperability or complete issue 110 acceptance.
* Scope: public source, relevant READMEs, existing sensor synthesis and addendum;
  three observations/home/day; declared N=1 and N=60,000; reproducible synthetic
  JSON byte measurement.
* Non-goals: source/runtime/schema/producer changes, stock reads, private data,
  transport design, cloud activity, approval changes or whole-issue closure.
* Criteria: exact source authority, field constraints, replay/conflict behavior,
  bounded receipts/DQ, arithmetic and explicit compatibility/acceptance gaps.
* Requested outputs: research, plan/details, one independent critique with
  dispositions, implementation evidence, one original Review, state/execution log.
* Output mode: convergence; prepares planning.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Q1 authoritative schema; Q2 replay/rejection; Q3 rate/bytes; Q4 compatibility and delivery boundary |
| Codebase scope | docs, src/core sensor modules/tests, src/api ingestion/tests, relevant build configuration |
| External scope | GitHub issue/PR metadata only, no product or legal research |
| Initial internal candidate areas | sensor_consumer, synthetic.sensor_faults, sensor_stock, sensor_backfill, component READMEs, existing sensor synthesis |
| Initial external candidate areas | issue 186, merged PR 411, origin/main ref |
| Research posture | focused |
| Posture provenance | caller's bounded exact-base delivery |
| Explicit limits | One independent critique, one original Review; zero correction cycles; no implementation workers or base movement |
| Completion basis | In-scope evidence coverage and materiality |
| Edits allowed | Research evidence and required execution tracking only |
| Resolved evidence root | .copilot-tracking/ |
| Exclusions | original case edits, private .env, ZF_DATA, support, actual stock dataset, Azure actions |

## Extension Registry and Provenance

Precedence: platform safety, caller scope, repository guidance, RPI phase
contracts, selected domain helpers.

| Kind | Candidate | Provenance / authority | Disposition |
| --- | --- | --- | --- |
| Instructions | Repository instructions, applyTo ** | Required source reads, branch/privacy/KB conventions | Selected |
| Skill | rpi-research | Ordered wider/deeper/contrarian evidence | Selected |
| Skills | rpi-plan, rpi-implement, rpi-review | Later phase contracts | Deferred until respective phase |
| Skill | documentation | Canonical documentation authoring | Deferred to implementation |
| Specialist | RPI Researcher | Available bounded research worker | Skipped; single tightly coupled source trace |
| Specialist | independent critique / Review | Explicit caller requirement | Deferred until plan / implementation complete |
| Skills | UI, accessibility, security audit | No changed UI/runtime or requested vulnerability audit | Skipped |

## User Participation and Research Decisions

| Checkpoint | Rationale | Direction |
| --- | --- | --- |
| Intake | Detailed owner direction explicitly authorizes automatic ordered RPI and publication | Proceed without routine confirmation |
| Boundary | No widening needed | Stop affected work if source changes become necessary |

## Scope and Success Criteria

Verify the supplied contract claims rather than assume them. Existing tests may
already suffice; do not add test constants or a public schema API. Keep
observation counts distinct from API batches, hypothetical wire packets and
unmeasured Hub billing.

## Task Research Requests

Owner scope is the live issue 186 literal contract/rate/idempotency request.
Parent 184 is hierarchy, not ordering. The contract dependency on 110 is
satisfied by PR 411 merged at exact base; broader 110 gates remain separate.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Narrow | User | Document unchanged consumer, not producer/backfill interoperability |
| Exclude | User | No consumer/stock/fault/store/schema/runtime changes; no identity remap |
| Preserve | User | Three paired observations/day; ADR accepted 2026-10-15 with Basic amendment |
| Freeze | User | Base 100ead1bacdb72a8ea7ce5867233db30b22b2f50, branch docs/sensor-message-contract-186 |

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Exact authoritative shared fields and validation? | depth | High | Answered C1/C5 |
| Q2 | Stable replay/conflict and bounded output behavior? | depth | High | Answered C2/C6/C8 |
| Q3 | Reusable example/serialization and correct N/bytes accounting? | depth | High | Answered C3/C5/C7/C10; actual byte measurement belongs to implementation |
| Q4 | Stock compatibility, existing documentation and approval boundaries? | depth | High | Answered C4/C9/C11/W3-W5 |

## Prior Knowledge Gate

Read unchanged original case, full addendum, index routing and memory. Supplied
prior art is a hypothesis to verify. Initial shell confirms clean worktree,
expected branch, exact base, no existing matching PR, live issue scope and merged
PR 411. origin/main equals base at intake. Memory is context, not evidence.

## Research Cycle Log

### Cycle 1

Focused; all waves inline because evidence forms one continuous contract trace.

#### Wave 1: Wider

Located the consumer import of READING_FIELDS/SCHEMA_VERSION from
synthetic.sensor_faults; all 13 required fields are strings and each row carries
both temperature and RH. API composition is explicitly not an HTTP route.
Existing component READMEs and sensor synthesis are suitable documentation homes.
Reflection: prioritize validation/replay internals and fixture/serialization
prior art; no independent schema file is warranted. The synthesis's older
"not an implemented IoT consumer" statement is dated history, not a description
of the newly merged offline consumer.

#### Wave 2: Deeper

Read full consumer validation/process path, fixture, core/API regression suites
and component commands. _shape enforces the shared closed field set; _reference
uses sorted ASCII JSON with default separators. Existing observations() supplies
unchanged valid Packet.rows and tests replay, conflict, schema, unit and time
semantics. Reflection: use that fixture plus exactly the existing reference
serialization expression for a sample, not a new serialization/schema API.
Existing semantic tests suffice; arithmetic can be asserted in the reproduction
snippet. No test-code change is needed. System python import failed because
zava_forward is not installed there; resolve an existing installed interpreter
or install src distributions only after this observed missing-dependency failure.

#### Wave 3: Contrarian

Read stock ID construction and backfill estimates: full SHA-256 hex IDs are
73 characters and contain lowercase, whereas consumer limits sensor IDs to
uppercase ASCII, max20. The generated reading IDs also embed the long sensor
ID and exceed40. Storage-column compatibility tests do not prove payload
interoperability. The fixture deliberately uses legacy sensor_for(ZF-1), not
stock Selection; do not disguise it as a stock adapter.
Existing estimate() measures CSV rows, default hourly/730 days, and fault mode
uses two-observation evaluator packets. None is a wire/day contract. "Packet"
therefore cannot imply a chosen transport batching policy.
Confirmed ADR acceptance directly from owner comment and preserved proposal
history. Downstream187/188 require replay/live/backfill work and must separately
resolve compatibility. Reflection: preserve all gaps; exact unchanged consumer
can be documented without a third110 correction. No further in-scope research
can turn these fixture checks into live acceptance.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Shared imported shape and current semantic tests | C1/C5-C8 | Accepted | Exact existing authority and meaningful tests, no duplication |
| 3N paired records/day, not six scalar records | C1/C3 | Accepted | Both measures occur in one row |
| Existing backfill CSV estimate as wire-byte evidence | C10 | Rejected | Different schema/format/cadence and fault counts |
| Existing synthesis with linked component source contract | C4 | Accepted | No new topic page needed |
| Stock/live interoperability | C9/W3/W4 | Deferred | Separate reviewed compatibility decision required |
| ADR approval still pending | C11/W5 | Rejected | Owner already accepted Basic amendment |

#### Cycle Re-entry Evaluation

No re-entry needed: all in-scope questions have primary source support and
existing tests. Byte counts will be executed, not guessed, during implementation.
Focused scope is complete; external live gates cannot be resolved in this task.
Planning Readiness: Ready.

## Evidence Log

### Codebase Evidence

| ID | Claim | Location | Tool | Confidence | Provenance |
| --- | --- | --- | --- | --- | --- |
| C1 | Consumer imports existing 13-field version authority | src/core/src/zava_forward/core/sensor_consumer.py:16; src/core/src/zava_forward/core/synthetic/sensor_faults.py:9 | read | High | Pinned base |
| C2 | API bounds and composes finite row processing, no HTTP route | src/api/src/zava_forward/api/sensor_ingestion.py:1 | read | High | Pinned base |
| C3 | Three simulated observations/day and independent human/live gates | docs/case_study_48_addendum.md:915 | read | High | Existing sensor section |
| C4 | Existing synthesis is suitable for maintained contract/rate evidence | docs/reference/research/iot-sensor-analytics-research-plan.md:1 | read | High | Historical privacy and climate findings stay intact |
| C5 | Closed shape, exact limits and sorted ASCII JSON digest serialization | src/core/src/zava_forward/core/sensor_consumer.py:376 | read | High | _shape and _reference |
| C6 | Historical replay before new admission controls, conflict without overwrite | src/core/src/zava_forward/core/sensor_consumer.py:558 | read | High | process |
| C7 | Existing unmodified fixture produces paired current-contract rows | src/core/tests/sensor_consumer_fixture.py:42 | read | High | observations() |
| C8 | Existing semantic tests cover schema/replay/unit/time and retained outcomes | src/core/tests/test_sensor_consumer.py:77; src/api/tests/test_sensor_ingestion.py:20 | read | High | No new test API required |
| C9 | Stock sensor ID is prefix plus full SHA-256 hexdigest | src/core/src/zava_forward/core/synthetic/sensor_stock.py:87; src/core/src/zava_forward/core/synthetic/sensor_backfill.py:124 | read | High | 73-character sensor and longer reading IDs incompatible |
| C10 | estimate() measures CSV; defaults hourly / 730 days | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:36; src/core/src/zava_forward/core/synthetic/sensor_backfill.py:149 | read | High | Not a wire contract |
| C11 | Current accepted ADR status separate from retained Proposed history | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:9 | read | High | No ADR edits needed |

### External Evidence

| ID | Claim | Source | Retrieved | Confidence |
| --- | --- | --- | --- | --- |
| W1 | Live literal scope and three unchecked criteria | https://github.com/jmservera/ama/issues/186 | 2026-10-18 | High |
| W2 | PR 411 merged at exact pinned base | https://github.com/jmservera/ama/pull/411 | 2026-10-18 | High |
| W3 | Replay/failure injection depends on182/186 | https://github.com/jmservera/ama/issues/187 | 2026-10-18 | High |
| W4 | Live/backfill consistency depends on110/183/186 | https://github.com/jmservera/ama/issues/188 | 2026-10-18 | High |
| W5 | Existing owner acceptance, Basic exercise amendment | https://github.com/jmservera/ama/issues/129#issuecomment-6194409951 | 2026-10-18 | High |

### Contradictions / Conflicts

Verified incompatible stock/consumer identity lengths/alphabet (C5/C9).
Document, do not truncate, remap or relax validation. Historical synthesis text
and historical Proposed ADR wording remain dated; add current boundary above them.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Implication |
| --- | --- | --- | --- |
| Q1 | 13 required string fields, version sensor-fault-input-v1 | C1/C5 | Source-linked descriptive table, not another schema |
| Q2 | Exact historical digest replay vs same-key changed content conflict | C2/C6/C8 | Explain stable key and bounded DQ/reconciliation |
| Q3 | 3 paired rows/home/day; reuse fixture and sorted JSON expression | C3/C5/C7/C10 | Measure sample, not upper bound or Hub throughput |
| Q4 | 73-char stock ID is invalid here; ADR accepted | C4/C9/C11/W3-W5 | Explicit downstream decision and live gates |

## Key Discoveries

The consumer's contract is already shared by import, not a new public schema
API. The canonical fixture is valid only within constructed independent controls.
Neither broader SQL column sizes nor evaluator Packet grouping establish live
producer compatibility or transport policy.

## Alternatives and Decision State

Select documentation-only delivery: extend existing sensor synthesis, link from
core/API READMEs and addendum, update KB index and append log. Reuse unchanged
fixture and existing JSON reference expression for measured sample accounting.
Reject a new schema/calculator/service: duplication and unnecessary runtime.
Reject a stock adapter repair: expressly excluded and requires separate review.
Reject CSV estimate reuse: different bytes, cadence and admission boundary.

## Current Decisions

Owner-confirmed automatic bounded delivery; no rebase, merge, force-push, closure
or correction cycle authorized. No private source access.

## Open Questions, Risks, and Residual Uncertainty

Live transport, identities, cost, privacy, real AI and Azure/human application
acceptance are separate gates and outside this delivery.

## Potential Next Research

High, deferred: downstream187/188 compatibility decision; trigger separate owner
assignment before producer/live work (C9/W3/W4). Do not begin it here.

## Unresolved Decisions

Stock/live identity compatibility remains a downstream human-reviewed decision,
not a blocker to describing the unchanged consumer. No source gap blocks this
documentation. Live packetization, cost and service acceptance are not selected.

## Planning Readiness

Ready, based on C1-C11/W1-W5. Research disposition: executed. Wider, Deeper,
Contrarian completed inline in order, with separate reflections. Automatic
coordinator owns Plan continuation after successful pre-transition state write.
No material implementation/source change is needed or authorized.

## Closeout Record

Research execution complete; disposition executed; Planning Readiness Ready.
All research inline, no worker implied. No blockers to bounded documentation.
Output mode convergence supports planning. User explicitly authorized automatic
continuation; remaining live decisions are excluded, not silently resolved.

## Advisory Next Step

Automatic parent activates rpi-plan with C1-C11/W1-W5 and these boundaries.
Then one independent final-candidate critique before implementation. Further
research would not change the exact existing contract; no widening justified.

## Sources

* W1 - Issue186 - https://github.com/jmservera/ama/issues/186 (retrieved2026-10-18).
* W2 - PR411 - https://github.com/jmservera/ama/pull/411 (retrieved2026-10-18).
* W3 - Issue187 - https://github.com/jmservera/ama/issues/187 (retrieved2026-10-18).
* W4 - Issue188 - https://github.com/jmservera/ama/issues/188 (retrieved2026-10-18).
* W5 - Owner ADR decision - https://github.com/jmservera/ama/issues/129#issuecomment-6194409951 (created2026-10-15; retrieved2026-10-18).

## Artifact Self-Check

Checked brief, extension/participation/direction controls, all questions, ordered
waves and reflections, stable evidence IDs, alternatives, decisions, risks,
readiness and sources. No unresolved placeholder or research blocker remains.
No source edits, delegated research, private-data access or secret recording.
This self-check is not executable validation; actual checks follow implementation.
