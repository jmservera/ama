---
title: Sensor fault injection final-candidate plan critique
description: One bounded critique of the task 182 implementation candidate
ms.date: 2026-10-17
---

## Metadata

* Task ID: 182 / sensor-fault-injection-182
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/sensor-fault-injection-182-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/sensor-fault-injection-182-phase-details.md
* Critique execution status: Complete
* Candidate assessments performed: exactly one

## Inputs and Criterion Boundary

* Caller requirements: genuine implementation in the continuing src/core
  stock/generator; independently injectable AC-066 fixture classes and
  outlier/stuck/drift/gap; seeded configurable packet rates; separate clean
  evaluator truth without analysis leakage; unchanged historical CSV bytes.
* Locked implementation envelope: one new typed helper, existing writer/CLI,
  documentation and tracking; src/core/tests/test_sensor_faults.py at most
  16 methods; no test removals; only the source-dependency list may change in
  src/core/tests/test_synthetic_determinism.py. Golden hashes remain locked.
* Research considered:
  .copilot-tracking/research/2026-10-17/sensor-fault-injection-182-research.md,
  including W1-W2 and C1-C7. Issue/PR descriptions are supplied research
  evidence, not independently refreshed remote evidence in this critique.
* Current code considered:
  src/core/src/zava_forward/core/synthetic/sensor_backfill.py,
  src/core/src/zava_forward/core/synthetic/sensor_stock.py,
  src/core/src/zava_forward/core/synthetic/provenance.py,
  src/core/tests/test_synthetic_determinism.py,
  src/core/tests/test_sensor_stock.py and src/core/pyproject.toml.
* Context considered: original case study, relevant addendum sensor section,
  reference index and owner memory, src/core/README.md and PRD AC-066.
* Accepted design decisions: exclusive two-row packet classes, total rate at
  most one, valid remainder, even nominal slot count of at least two, sibling
  analysis/ and truth/ directories, fixed fictional corruption magnitudes.
* Dependencies: #177 is parent context; #110/#111 are related work, not
  ordering gates. Full ordered RPI and publication are authorized, not merge.
* Boundary: assess implementation credibility and planned evidence, not live
  IoT/SQL/AI acceptance, operational calibration or implementation results.
  No private data, live services, infrastructure changes or spending.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| All named faults, valid controls; W1; P01-T01 | Covered | Explicit packet transformations and forced-rate-one/zero-rate assertions; no missing requested class |
| Seeded configurable rates; P01-T01; P02-T01 | Partial | PC-001: changed output bytes do not isolate changed fault assignment; equivalent rate-map ordering is unspecified |
| Separate truth and no leakage; C2-C3; P01-T02 | Covered | Removes legacy labels, separates manifests/config, retains clean packets and emitted positions |
| Complete truth across variable cardinality and shards; P01-T02; P02-T01 | Partial | PC-002: no explicit cross-sensor/shard positional reconciliation case |
| Historical bytes and test locks; C5; P01-T02 | Covered | Legacy branch retained; existing exact hashes not weakened; dependency-list-only exception |
| Continuing stock and resident choices; C4; P01-T02 | Covered | Existing stock adapter retained; granted/declined/unknown and empty selection addressed |
| Streaming and safe destinations; C3; P01-T02 | Covered | Two-row buffer, shared iterator, preflight and nonempty refusal specified |
| Loader boundary; P01-T02 | Covered | Root and analysis subdirectory rejected before schema/database operations |
| Typed helper, tooling, mutations; P02-T01 | Covered | Existing core tooling and exemptions retained; missing-feature and mutation evidence planned |
| Documentation, ordered RPI and publication; P02-T02 | Covered | Existing synthesis/index/log, completion markers, one Review and ordinary topic publication |
| AC-066 live-platform scope; C1; follow-up items | Covered | Correctly does not equate generated fixtures with live acceptance |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 2 Medium, 0 Low.
* Rationale: the architecture and requested scope are credible. Two narrow
  evidence gaps leave deterministic fault selection and evaluator joins
  vulnerable to false-positive validation. Both can be corrected within the
  existing tasks and test-method limit, without changing the selected design
  or obtaining another user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Isolate fault-selection determinism from clean-series seed changes

* Related IDs: seeded configurable rates, per-sensor RNG requirement,
  P01-T01, P02-T01.
* Evidence: plan lines 69-79 require repeatability, per-sensor independence and
  mixed output differing for another seed. Details lines 31-38 specify an
  independent Random stream but not a canonical class traversal or a
  fault-assignment comparison. Current sensor_backfill.readings() already
  seeds the clean indoor series; SensorStockTests.test_repeat_bytes_seed_and_date_variation_and_shards
  already obtains changed bytes from changing that seed.
* Concern: a different-seed payload comparison can pass even if fault
  assignments ignore the seed, because clean temperatures change. Iterating
  user mapping/CLI insertion order also permits equivalent rate settings to
  select different classes from the same random draws. The planned empirical
  coverage and rates-ignored mutation do not explicitly resolve these two
  cases.
* Impact: fixtures could appear reproducible and configurable while their
  fault assignments are fixed, order-sensitive or affected by sampling order.
* Smallest useful change: specify a fixed canonical fault-class order and add
  assertions on the truth class sequence keyed by sensor and nominal packet
  index. Compare identical settings with reversed API mapping/CLI option
  order, repeated runs, another seed, an estimate call before writing and a
  changed shard size. Use a fixed explicit population with multiple nonzero
  rates and a declared empirical tolerance.
* Action owner: planning parent; implementation owner executes P01/P02.
* Exact resolving evidence: revised P01-T01/P02-T01 completion conditions name
  the canonical order and class-sequence oracle; subsequent test evidence
  shows the same per-sensor sequence for equivalent configurations, estimation
  and sharding changes, a different sequence for the selected alternate seed,
  and failure when fault RNG is replaced by a constant seed. Keep this within
  the existing maximum of 16 new test methods using subTests/helpers.
* Decision route: compatible direct planner correction; no significant or
  divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Require a cross-sensor, cross-shard truth-position reconciliation case

* Related IDs: complete separate truth, P01-T02, P02-T01.
* Evidence: plan lines 62-63 and 81-82 require complete emitted positions,
  including duplicates and absent gaps. Details lines 47-48 establish
  zero-based shard-local row positions; lines 65-66 promise reconciliation
  without specifying a multi-shard case. Current sensor_backfill.write.flush()
  places multiple sensor series in each shard and resets its row count on
  each flush.
* Concern: per-class forced cases and a tiny granted/declined/unknown CLI
  fixture can exercise only one monitored sensor and one shard. Such checks
  can miss resetting positions at every sensor, failing to reset at a shard
  boundary, counting headers as rows, or assigning duplicate/gap offsets to
  the wrong packet. Correct hashes would only authenticate these incorrect
  joins.
* Impact: evaluator truth could mislabel another packet's readings or omit
  duplicate occurrences, defeating the purpose of separate ground truth even
  when every corruption is independently visible.
* Smallest useful change: add one explicit integrated reconciliation case
  using at least three granted fictional sensors and a patched two-sensor
  shard size. Ensure valid, gap, duplicate and reversed packets occur, through
  a checked fixed seed/config or a controlled helper selection test seam.
  Reconcile actual CSV rows against truth without assuming nominal row counts.
* Action owner: planning parent; implementation owner executes P01/P02.
* Exact resolving evidence: revised P01-T02/P02-T01 require this case;
  subsequent assertions prove each emitted row position is accounted for
  exactly once, references the correct shard and clean nominal observation,
  duplicate occurrences retain equal reading identity, gaps have no emitted
  positions, and positions reset only at shard boundaries. A counter-reset
  mutation must fail. Use subTests/helpers within the same 16-method limit,
  without editing or removing existing tests.
* Decision route: compatible direct planner correction; no significant or
  divergent user decision.

## Strengths and Residual Risk

* The explicit opt-in branch protects historical CSV serialization while
  removing legacy embedded fault answers from the new analysis schema.
* Packet reversal is genuine delivery reversal, not disguised timestamp
  corruption; duplicate and gap cardinalities are explicitly defined.
* Separate manifests, retained clean packets, pre-database loader rejection
  and stock-consent exclusions address the relevant integration hazards.
* Exercise magnitudes and packet rates are deliberately fictional, not
  calibration evidence or guaranteed quotas. Live AC-066 acceptance remains
  outside this authorized local implementation.
* Two-row packets and even-window restrictions are accepted candidate
  decisions, not grounds to reopen the design.

## Questions or Blocking Evidence Gaps

* No decision-critical external evidence gap or unresolved user choice.
* PC-001 and PC-002 require planned validation corrections, not additional
  research, broader scope or a second critique.

## Limitations

* This is a plan assessment. No implementation, tests, mutations, service
  calls or publication were performed.
* Source evidence was read directly; supplied research's remote issue/PR
  facts were not independently re-fetched.
* Existing dirty tracking and candidate files were left untouched. The only
  write in this task is this requested critique artifact.

## Recommended Next Action

* Highest-impact finding: PC-002, because incorrect truth joins invalidate
  downstream evaluation despite apparently correct generated readings.
* Action owner: planning parent.
* Smallest next action: update the existing phase completion conditions and
  test allocation for PC-001 and PC-002, record their dispositions, then
  continue the authorized ordered RPI flow without another critique.
* User response required: no.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-17/sensor-fault-injection-182-plan.md | Assessed final-candidate plan |
| .copilot-tracking/details/2026-10-17/sensor-fault-injection-182-phase-details.md | Assessed phase completion conditions |
| .copilot-tracking/research/2026-10-17/sensor-fault-injection-182-research.md | Supplied bounded research evidence |
| .copilot-tracking/reviews/plans/2026-10-17/sensor-fault-injection-182-plan-critique.md | This complete single-pass critique |

## Next Steps

Planning parent resolves the two compatible planner-owned findings directly,
records disposition, and resumes the authorized implementation sequence.
No user action or further critique is required. This critique task stops here.
