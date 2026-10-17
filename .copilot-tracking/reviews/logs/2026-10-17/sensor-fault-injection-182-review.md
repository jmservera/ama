---
title: Sensor fault injection review
description: Single post-implementation review for task 182
ms.date: 2026-10-17
---

## Scope and Evidence

Task 182 / sensor-fault-injection-182; full P01/P02 implementation at 7562515.
One Review, not a security audit or live-platform acceptance.

* Research: .copilot-tracking/research/2026-10-17/sensor-fault-injection-182-research.md
* Plan: .copilot-tracking/plans/2026-10-17/sensor-fault-injection-182-plan.md
* Details: .copilot-tracking/details/2026-10-17/sensor-fault-injection-182-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/sensor-fault-injection-182-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/sensor-fault-injection-182-changes.md

## Opening Review State

Goal: compare exact issue criteria, bounded plan, final source and evidence.
Evidence set ready: source/test/docs committed, all plan markers complete,
details/changes reconciled, PC-001/PC-002 dispositions recorded. Initial
comparison: packet semantics, deterministic rates, separate evaluator truth,
stock reuse, default compatibility and validation. Read-only source boundary;
this review writes only its canonical record. No initial blocker.
No delegation: a single direct code/evidence trace fits this context.

## Execution Status

Complete, executed once on 2026-10-17 against implementation 7562515.
No source changes during Review. No worker or second review was used.

## Plan-to-Change Reconciliation

| Scope | Evidence assessed | Reconciliation |
| --- | --- | --- |
| P01-T01 | Typed sensor_faults helper and ten new test methods | Every class has observable semantic assertion, clean copies and separate seed/sensor RNG |
| P01-T02 | Existing writer, estimate, CLI, loader guard | Shared packet injector, actual delivery reversal, units/calibration and separate evaluator files; default branch unchanged |
| P02-T01 | Changes command/results, in-memory mutation report, CLI receipts | Focused/core/tooling pass; one live gate explicitly skipped |
| P02-T02 | Core README, synthesis/index/append-only log | Exact interface, exercise semantics and remaining acceptance limits documented |
| Plan/details | All four task markers and two phases checked; details Complete | No remaining implementation task or blocker |

## Exact Issue Acceptance Assessment

| Issue criterion | Assessment | Evidence |
| --- | --- | --- |
| Each fault injectable and labelled in a separate truth file | Met locally | All ten names forceable at rate one; per-shard truth JSONL records class/clean packets/emitted positions; valid control explicit |
| Rates configurable and seeded | Met locally | Unique NAME=RATE options and typed mapping, finite [0,1], exclusive total <=1, canonical order, separate sensor/seed RNG |
| AC-066 valid/duplicate/out-of-order/unmapped/wrong-unit/clock-skewed/uncalibrated inputs | Met as fixture classes | Valid remainder, identity-preserving duplicate, actual pair reversal, missing-register sensor, Fahrenheit-declared conversion, +24-hour observed time and calibrated=false |

This is not acceptance of AC-066's deployed consumer, exception ownership,
IoT Hub authentication, SQL persistence after restart or registered real AI.

## Completed Work Assessment

Compared the full changed source and tests, tracked commit diff, exact issue
research, #320 prior-art boundary, documentation and execution output.

* Clean observations reuse the current _indoor/outdoor model and existing
  sensor_stock selection/fabric. Fault mode sets historical implicit profile
  to none internally and does not write that profile to analysis.
* The packet transformer copies rows before mutation; clean nominal packets
  retain both observations, including gaps. Duplicate positions include every
  occurrence. Counters are initialized once per shard, not per sensor.
* Out-of-order reverses actual rows without altering timestamps; clock skew
  changes timestamps independently. Wrong-unit data retains an explicit unit
  despite the historical temperature_c column name, documented prominently.
* Analysis has no embedded injected_fault, fault_profile, rates, clean
  counterfactuals or truth links. Unit/calibration/mapping defects are observable
  input stimuli, not separate answer columns. Seed and schema remain ordinary
  synthetic provenance, as required by AC-066.
* Truth stays in an evaluator sibling directory, with clean values and labels.
  The manifest binds analysis-manifest bytes and hashes every truth payload.
  This is an interface/file boundary, not OS access control; operator separation
  is explicit. No analysis/truth consumption is wired into AI or runtime flows.
* Config/window preflight precedes output preparation; even >=2 nominal slots
  and exclusive packet probabilities are documented, not silent fallbacks.
  Clock-skew calendar overflow is preflighted.
* Existing output helpers reject repository, symlink and nonempty destinations
  for opt-in snapshots. No private baseline, full-stock materialization or
  changed domain approval/resident workflow is introduced.
* Default CSV serializations and legacy DDL remain unchanged; old exact hashes
  and idempotent-load tests pass. New-schema/root rejection precedes database
  writes and avoids accidentally using the legacy unit-unaware loader.

## Implementation-Time Update Assessment

No material design revision or additional user decision. Typed API parameter
annotations exposed a test-fixture inference problem; the local annotation
correction preserved accepted requirements and passed final tooling.
Formatting changes were confined to the two new files. One existing mypy
untyped-call test allowance was extended without ignore_errors. No existing
test or historical golden hash was removed or weakened.

## Critique Assessment

Exactly one final-candidate critique executed, verdict Revise. Compatible
PC-001/PC-002 corrections were applied before implementation; no re-critique.

| Finding | Resolving evidence | Assessment |
| --- | --- | --- |
| PC-001 | Canonical rates; 2,000-packet class-sequence oracle; alternate seed/sensor; reversed settings; prior estimate; shard changes; constant-seed mutant killed | Resolved |
| PC-002 | Three granted sensors with two-sensor shards; exact total row coverage and clean joins for valid/gap/duplicate/reversed cases; counter-reset mutant killed | Resolved |

## Plan Follow-Up Assessment and Findings

No implementation defects identified in the bounded feature. Existing external
follow-ups remain distinct and do not invalidate #182's fixture criteria.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: New-schema consumer and live AC-066 acceptance remain separate

Evidence: explicit loader refusal, README schema boundary, issue #183/#110 and
PRD AC-066. Impact: these generated inputs must not be presented as proof of
real ingestion, owned exceptions, SQL restart durability or live AI acceptance.
Destination: distinct #183/#110 implementation workstream.
Smallest next action: reuse these analysis inputs in the future unit/calibration-
aware consumer contract; retain evaluator truth only for grading.
This is existing residual scope, not a missing #182 implementation.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Source, method and monitoring authority remain unapproved

Evidence: research/plan exclusions, exercise-value manifest, source synthesis
and #178-#181. Impact: deterministic injected values and local passing tests do
not establish climate/calibration validity, building-physics thresholds or
resident permission. Destination: distinct source/method research and named
owner approval workstreams, not more #182 implementation.
Smallest next action: resolve the current climate/licence, indoor calibration,
dated measure and behaviour evidence before any scientific/operational claim.

## Validation Evidence

| Check | Status | Result |
| --- | --- | --- |
| Fail-before new tests | Executed, expected failure | ImportError proved missing module before implementation |
| Sensor tests | Passed | 37 tests; ten new methods include all class subTests and integrations |
| Golden determinism | Passed | Seven tests; historical reading/sensor CSV hashes unchanged |
| Full core | Passed with explicit skip | 546 run, 545 passed, one resident/Azure opt-in skipped |
| Semantic mutants | Passed | All 15 deliberately broken variants killed by assertions, no mutant errors |
| Tiny installed CLI | Passed | 5 selected/3 granted/1 declined/1 unknown; 292 rows/144 packets/all 11 classes; replay identical; estimate reconciles |
| Ruff check/format and mypy | Passed | 49 formatted files; 102 typechecked source files |
| Changed Markdown links and git diff --check | Passed | New/changed relative targets and anchors resolve; whitespace clean |
| Live IoT/SQL/AI/Azure and human acceptance | Not run | Explicitly outside authorization; no approval inferred |

The core suite's disposable fictional scale benchmarks do not touch the owner's
private stock. Existing ResourceWarnings were not new failures and were not
broadened into unrelated fixes. Other-component suites were not run for this
synthetic-only core change.

## Outcome

Execution: Complete. Outcome: Residual work, limited to RV-001/RV-002 existing
external acceptance. Bounded #182 implementation meets all three issue criteria;
no open code defect or material divergence identified. This outcome is not
whole-PRD conformance or production acceptance.

## Routing and Closeout

| Finding class | Destination | Next owner/action |
| --- | --- | --- |
| Implementation defect | None | No bounded implementation defect identified |
| Decision gap | None for #182 | No user-owned decision invented |
| RV-001 external ingestion evidence | Distinct #183/#110 work | Consumer owner implements/tests against analysis inputs |
| RV-002 source/method authority | Distinct #178-#181 research and human gates | Obtain evidence and explicit owner disposition |

No remaining active P01/P02 work or blocker. Return this one Review to the
parent for ordinary commit/push/PR publication, then stop as the caller requested.
No source fixes, repeat Review, merge, issue closure or follow-up loop authorized.
