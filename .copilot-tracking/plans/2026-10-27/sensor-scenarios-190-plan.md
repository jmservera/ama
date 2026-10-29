<!-- markdownlint-disable-file -->
# RPI Plan: Sensor scenarios and documentation

## Task Metadata

* Task ID: 190
* Task slug: sensor-scenarios-190
* Plan date: 2026-10-27
* Planning status: Ready; original critique Revise, direct dispositions below
* Phase details: .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/sensor-scenarios-190-plan-critique.md

## Executive Summary

Add a bounded, reproducible scenario pack using clean merged backfill rows,
separate evaluator truth, exercise-only comparison and per-check JSON results.
Cover seven damp/data-quality cases and four paired before/after profiles.
Document both simulator stages honestly, including the absent live runner.

### What You May Not Know

#111 analytics, #133 lived-performance view and the live runner are not delivered.
Fixtures cannot prove actual downstream test use or whole-parent closure.
Air temperature/RH cannot diagnose mould or surface condensation. All new
thresholds, sizes, periods and classifications are exercise assumptions.
No new Legal/DPO decision is needed for independent synthetic fixtures.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order, committing dated artifacts.
* Use the supplied branch; one PR to main for #190/#192/#193/#194.
* Reuse src/core backfill and ADR 0006 layout; preserve workflow/check names.
* Local tests only, pip only, no private datasets, secrets, deployment or full gate.
* Prove criteria individually; use Refs for incomplete acceptance.

## Goals

* Provide reproducible, isolated test inputs and expected outcomes.
* Make errors, missingness and sensitivity visible rather than one overall pass.
* Correct stale dictionary claims without rewriting historical evidence.

## Scope and Non-Goals

In scope: one scenario/comparison module, external tests, existing core README,
sensor dictionary/research synthesis, KB index/log and RPI evidence.
Out of scope: live transport, approved analytics/tasks, AI, UI, real monitoring,
retrofit physics calibration and completion of #111/#133.

## Functional Requirements

* Seven labelled damp cases: normal, condensation-prone, sustained high humidity,
  overnight peaks, sensor fault, missing data and seasonal shift.
* Four retrofit cases: improvement, no change, delayed effect, adverse effect.
* Actual pack seed remains the common required observation seed across cases;
  internal RNG stream keys, labels and expected status/direction/size live in truth.
  Neutral case IDs and a common scenario marker in analysis; no label-bearing
  paths or embedded answers. Neutral observation windows may include measure date.
* Exercise comparator consumes only observations and neutral windows; truth
  joins happen afterward for confusion counts and per-check comparisons.
* Report per-case coverage, validity, flatline, threshold outcomes, confusion
  denominators and sensitivity at RH thresholds 70/75/85. Fault/missing cases
  must be INSUFFICIENT, never a reassuring negative.
* Before/after compare matching seven-day baseline, early and late windows;
  include observed denominators and exact exercise delta targets.
* New CLI writes only to explicit external new/empty snapshots; no network.

## Non-Functional Requirements

* Same seed/source/runtime yields byte-identical snapshots, including reports.
* Shared 13-field observation contract; no truth columns or per-case labels.
* No changes to default backfill bytes or existing package dependencies.
* Invalid seed/output/window/observation inputs fail explicitly.
* Package code is typed; tests live in src/core/tests, not the package.

## Acceptance Criteria

* Prove all three #192 criteria with scenario metadata, file separation and a
  reproducible confusion/sensitivity report. This does not approve R2/R3 limits.
* Prove #193 direction/size criteria; explicitly retain actual #111/#133 use
  as unmet if those consumers remain unavailable.
* Cover backfill and the live-stage contract/unavailable runner in docs;
  preserve exact climate retrieval/licence/limited approval caveats.
* Report every #190 child disposition and validation check independently.
  Do not close #190 without closed or owner-deferred children.

## Implementation Context Record

| Context | Artifact |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md |
| Plan | .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md |
| Details | .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-27/sensor-scenarios-190-plan-critique.md |
| Changes (implementation-owned) | .copilot-tracking/changes/2026-10-27/sensor-scenarios-190-changes.md |
| Continuation | Automatic, full-loop caller authorization |

## Sources

Research C2-C13 and W1-W4; PRD FR-050/AC-067/068, BRD FR-048/OD-43,
ADR 0003 decision 6 and ADR 0006. No new external scientific claim.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Scenario inputs and evaluator

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement deterministic packs, separate truth and per-check reports

Dependency: merged generator/schema. Canonical target:
src/core/src/zava_forward/core/synthetic/sensor_scenarios.py.

<!-- rpi:phase id=P02 -->
### [x] P02: Tests and documentation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add semantic/regression tests and update simulator knowledge

Depends on P01. Canonical test target: src/core/tests/test_sensor_scenarios.py.
Maximum one new test file and 24 test methods; exact removals: none.
Existing #191/backfill/fault/retrofit/consumer tests remain unchanged unless a
tightly coupled defect requires correction. Semantic coverage: expected scenario
outcomes, exact activation and delayed/no-change, confusion denominators and
insufficiency. Regression coverage: seeds/bytes, no truth leakage, safe outputs,
bad inputs, CLI, legacy generator/schema. Generated targets: new external
temporary directories only, not committed datasets.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and prepare independent Review

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run targeted local tests, lint/types and CLI for Review

Depends on P02. Run core sensor/retrofit/climate/household/provenance regression,
new tests, package dependency check and API existing tests per supplied command.
Use /tmp/ama-syn190-venv installed packages. Run ruff/format and mypy against
changed Python only (existing dependencies may be followed without inventing
global cleanliness). Record actual results, skipped checks and limits.
This is bounded fixture work, not a large feature: no heavy gate planned.
After implementation, exactly one independent Review; route its findings later,
do not rerun Review. Preserve human/hosted approval as unperformed.

## Dependencies

Merged #180/#182/#191/#186 components available. #179 physical calibration and
real-data OD-43 remain outside exercise scope. #184 live, #111 and #133 pending.

## Critique Disposition

Exactly one critique executed, original verdict Revise, preserved unchanged.

| Finding | Owner/disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Planner: applied with accurate provenance | Common actual pack seed in all observations; RNG keys and labels separate; comparator ignores identity/seed |
| PC-002 | Planner: applied | Details specify half-open grids, gap breaks, per-day/night and per-week sufficiency |
| PC-003 | Planner: applied | Fixed seven-case damp population, four excluded retrofit cases, explicit abstentions/rates and mutation tests |
| PC-004 | Planner: rejected | Alleged ban on /tmp is absent from caller/host instructions; caller explicitly names /tmp lock and new external output. Existing isolated pip environment remains allowed |
| PC-005 | Planner: applied | Exactly one new test file, max24 methods, zero removals in both artifacts |
| PC-006 | Planner: applied | Pre-write symlink-ancestor and .git directory/file checks plus file/nonempty refusal |
| PC-007 | Planner: applied | Truth manifest records generator/evaluator versions, source/runtime/windows/weather/parameters/seeds and relative hashes |

No significant/divergent user decision required; no repeat critique.

## Follow-Up Items

* #193: wire these fixtures into actual #111/#133 tests when consumers exist.
* #194: runnable live-stage instructions depend on #184; do not invent commands.
* #190: owner disposition of remaining incomplete child criteria.

## Handoff

Implementation P01-P03 complete with evidence in the changes record.
Core 173 tests (1 skip), API 1,121 tests (314 skips), new scenario tests 15,
scoped lint/format/types, installed CLI and added-link checks completed.
Ready for the one independent lifecycle Review. All markers, details and
summary reconciled. No unperformed SQL/live/hosted/human check is accepted.
