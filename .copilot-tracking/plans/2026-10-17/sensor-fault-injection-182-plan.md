---
title: Sensor fault injection implementation plan
description: Ordered implementation and validation for issue 182
ms.date: 2026-10-17
---

## Task Metadata

Task 182 / sensor-fault-injection-182. Planning Complete, Ready after one critique.
Research: .copilot-tracking/research/2026-10-17/sensor-fault-injection-182-research.md.
Details: .copilot-tracking/details/2026-10-17/sensor-fault-injection-182-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-17/sensor-fault-injection-182-plan-critique.md.

## Executive Summary

Add opt-in deterministic fault packets to the current sensor writer, sharing its
stock selection, climate and indoor generator. Sibling analysis/ and truth/
directories physically separate inputs from evaluator labels and clean values.
Default mode retains historic payload bytes. Exclusive two-reading packet
rates make true out-of-order delivery streamable with constant extra memory.
No blocker; rates and fault magnitudes are exercise values, not scientific bounds.
This delivers #182 fixture inputs, not live AC-066 ingestion acceptance.

## User Decisions and Requirements

* Full ordered RPI with dated committed artifacts and explicit persistent phase completion.
* Implement all fault classes, seeded configurable rates and separate truth.
* Preserve default historical bytes, continuing stock, resident choice and approvals.
* Use src/core, outside-package tests, own pip-only venv and tiny fictional CLI inputs.
* No real/private data, live services, spending, infra/auth changes or nested delivery loops.
* Push topic branch and open Refs #182 PR with criterion audit; no merge or closure.

## Goals

* Reproducible fault fixtures with observable corruption and separately retained clean truth.
* Safe opt-in schema and bounded validation that cannot silently enter the legacy loader.

## Scope and Non-Goals

Scope: sensor_faults helper, existing writer/CLI, targeted tests, core README,
existing synthetic synthesis/index/log and RPI artifacts. No new data universe.
Non-goals: production ingestion, sensor analytics, calibrated bounds, real
monitoring or acceptance of AC-066 live IoT/SQL/AI requirements.

## Functional Requirements

* Repeated --fault-rate NAME=RATE activates the feature; API accepts optional rates mapping.
* Exclusive packet classes: outlier, stuck, drift, gap, duplicate, out_of_order,
  unmapped, wrong_unit, clock_skewed, uncalibrated. Remainder is valid.
* Rates finite [0,1], total <=1, reject unknown/repeated names; opt-in requires
  an even nominal slot count >=2. Validate before output.
* Two consecutive clean rows per packet. Same selected class for both; rates
  refer to packets, not independent overlapping faults or guaranteed quotas.
* Duplicate emits each original twice; gap emits none; out_of_order reverses
  delivery preserving IDs/times; unmapped changes sensor ID; wrong_unit converts
  Celsius to Fahrenheit and declares degF; skew adds 24 hours to observed time;
  uncalibrated sets calibrated=false; outlier adds 25 C; stuck holds first clean
  packet value for both samples; drift adds 0.05 C per nominal slot in the series.
* All input rows keep SYNTHETIC provenance and add unit/calibration fields.
  Analysis omits injected_fault and fault_profile. No rates, counts, truth
  references or clean values in analysis metadata. No truth used by estimation.
* Truth records class, clean packet, emitted shard row positions and fault config.
  Hash all analysis payloads and truth payloads in their respective manifests.
* Legacy loader refuses opt-in snapshots before DB/schema writes.

## Non-Functional Requirements

* Streaming two-row buffers, no extra full-history materialization.
* Same runtime/source/seed/config/input/date yields identical payloads/manifests.
* Output safety reuses current helpers; no nonempty snapshot replacement.
* New helper/test fully typed; existing migrated writer exemption unchanged.
* Seed selection is per sensor so sharding and estimate calls do not perturb it.
  Canonical class traversal is the documented order above, never mapping order.

## Acceptance Criteria

* Each class independently forced at rate 1 produces exact observable effects
  and complete evaluator truth; zero rates produces only valid, clean inputs.
* Mixed seeded rates reproduce, differ for another seed and have bounded
  empirical coverage checked on a small explicit packet population.
* AC-066 classes represented; duplicate identity and actual reverse order tested.
* No truth labels/profile/config in any analysis artifact; gap truth retains
  missing nominal observations and duplicates retain every emitted position.
* Existing historical hashes, stock exclusions and all core regressions pass.
* PC-001: compare truth class sequences keyed by sensor/packet, not payload bytes,
  across reversed settings order, prior estimate calls, shard sizes and seeds.
  Use 2,000 packets with 0.2 duplicate/0.3 gap and +/-0.04 empirical tolerance.
* PC-002: three granted sensors, two-sensor shards; reconcile every actual row
  exactly once to truth positions across valid/gap/duplicate/reversed packets.
  Gap positions empty; duplicate IDs equal; counters reset only per shard.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Implement opt-in contract

<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Add failing tests and typed packet injector

Own tests/test_sensor_faults.py, maximum 16 focused test methods, no removals.
Semantic assertions cover each corruption, rates, deterministic random choice
and clean truth. New source target synthetic/sensor_faults.py.

<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Wire writer, estimate, CLI, metadata and loader guard

Canonical target synthetic/sensor_backfill.py. Generated targets only ephemeral
fictional analysis/truth outputs outside the repository. Regression owner:
test_synthetic_determinism.py retains exact historical bytes and source tracking;
update dependency list only if required. No other test removals or weakening.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and document

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Run focused fail-before, mutations, CLI and core tooling

Run new tests before implementation; inject targeted mutations without committing
mutants and require failures; run sensor/determinism and core suite, Ruff
check/format and mypy. Tiny stock CLI includes granted/declined/unknown, rerun
byte comparison and truth reconciliation. Record actual outcomes/failures.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Update documentation and changes evidence

Core README, existing synthetic synthesis, index and append-only reference log;
no unrelated docs. Changes record owns commands, results and deviations.

## Dependencies

Merged #320/#177 code is present. #177/#110/#111 are not ordering edges.
Missing installed core/ruff/mypy restored with pip in a session-owned venv.

## Critique Disposition

Executed exactly once, verdict Revise; both Medium findings directly resolved
by strengthening existing completion criteria, without a new design decision.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Applied | Canonical class order, explicit class-sequence/seed/order/shard oracle and 2,000-packet tolerance above; constant-seed mutation required |
| PC-002 | Applied | Three-sensor/two-shard total positional reconciliation above; counter-reset mutation required |

## Follow-Up Items

* #183/#110 consumer contract and live AC-066 evidence remain separate.
* #178-#181 climate, calibration, dated measures and behaviour remain separate.

## Handoff

Implementation changes path:
.copilot-tracking/changes/2026-10-17/sensor-fault-injection-182-changes.md.
Proceed automatically after compatible critique disposition. Review exactly once;
publish then stop as explicitly requested, without child delivery loops.
