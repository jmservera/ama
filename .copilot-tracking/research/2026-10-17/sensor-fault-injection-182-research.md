---
title: Sensor fault injection research
description: Bounded implementation evidence for issue 182
ms.date: 2026-10-17
---

## Research Brief

Implement issue #182 in the continuing src/core sensor generator, with opt-in,
seeded configurable faults and a separate evaluator-only truth file. Audience:
implementers and PR reviewers. Output mode: convergence. Posture: focused,
selected from the caller's bounded scope. Evidence root: .copilot-tracking/.
Research writes only evidence and required lifecycle tracking.

## Scope, Controls and Participation

Read the exact issue and merged #320/#177 prior art. Preserve default historical
CSV bytes, stock identity, resident choices and human approval. No real-data
access, private baseline replacement, live services, spending or infra work.
Parent #177 and related #110/#111 are context, not ordering dependencies.
The caller explicitly requests the full ordered loop and publication; no
interactive checkpoint is needed or available. No nested delivery loops.

## Extension Registry

Repository instructions and rpi-research selected. Python implementation uses
existing package tooling. Web/design skills skipped: backend-only. Specialist
research delegation skipped: one tightly coupled code trace, handled inline.

## Prior Knowledge Gate

Clean supplied topic branch feat/sensor-fault-injection-182; no existing PR.
Fetched origin/main is abaca7881e2a4a77eacf865fe235d4af9196643f,
matching HEAD. Exact issue has three acceptance criteria. Merged #320 explicitly
leaves complete configurable fault classes and separate truth unfinished.
Original case study and memory read; index/addendum relevant sensor context
identified for targeted reading. No implementation dependencies inferred.

## Questions and Cycle 1

Q1: Where can injection reuse the historical writer without altering defaults?
Q2: What existing schemas, consent and deterministic-output rules apply?
Q3: What observable mutations prove all fault classes and truth separation?

### Wider

Located sensor_backfill, sensor_stock and sensor tests in src/core; located
AC-066/067/068 and existing sensor research synthesis. Reflection: real ingestion,
scientific bounds and operational approval are outside this local feature.

### Deeper

The writer already streams per sensor into bounded shards, estimates before
writing, fingerprints sources and refuses nonempty snapshots. Stock selection
excludes declined/unknown homes before creating sensors. Historical readings
carry injected_fault and sensor rows carry fault_profile: these cannot be the
new analysis schema. Retain them only in unchanged legacy mode.

Select explicit repeated NAME=RATE options, mutually exclusive per consecutive
two-observation packet, remainder valid. Two-observation packets make true
delivery-order reversal observable without changing observation timestamps or
buffering an entire history. Require an even number of at least two slots in
opt-in mode. Disable historical implicit faults only when opted in, preserving
the same indoor equations and existing stock adapter.

### Contrarian

Inline challenges: independent overlapping rates could cancel or obscure
faults; reject in favour of exclusive packet classes and total <=1. Merely
renaming timestamps would conflate clock skew and delivery disorder; reverse
actual delivery for out_of_order. Embedded injected_fault/fault_profile leaks
answers; opt-in output has analysis/ and evaluator-only truth/ sibling folders.
No rates, fault counts or truth references in analysis metadata. Truth retains
clean nominal values and emitted row positions, including absent gaps and
duplicate positions. The legacy loader must explicitly reject this new input
schema before touching a database, rather than silently misinterpret units or
calibration. New ingestion validation remains #183/#110 work.

Reject a standalone alternative stock generator: violates continuing identity.
Reject changing legacy schema/DDL: breaks historical byte and load contracts.
No further cycle needed: named sources and code paths cover the bounded ask.

## Evidence Log

| ID | Finding | Source | Confidence |
| --- | --- | --- | --- |
| W1 | Each fault injectable, separate truth, seeded configurable rates, seven AC-066 classes | https://github.com/jmservera/ama/issues/182 retrieved 2026-10-17 | High |
| W2 | Prior implementation deliberately leaves this feature unfinished | https://github.com/jmservera/ama/pull/320 retrieved 2026-10-17 | High |
| C1 | AC-066 includes live acceptance beyond fixture generation | docs/prds/zava-forward-retrofit-programme-demonstrator.md, AC-066 | High |
| C2 | Historical implicit faults and embedded labels | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:107-132 | High |
| C3 | Existing estimate, shard writer, hashes and loader | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:160-340 | High |
| C4 | Sorted stock subset and monitoring exclusions | src/core/src/zava_forward/core/synthetic/sensor_stock.py:65-166 | High |
| C5 | Golden historical hashes and refresh safety | src/core/tests/test_synthetic_determinism.py:103-228 | High |
| C6 | Synthetic-only signals, no diagnosis or consent inference | docs/case_study_48_addendum.md:866-920 | High |
| C7 | R3 synthetic faults support method evaluation, not method approval | docs/reference/research/iot-sensor-analytics-research-plan.md:75-103 | High |

## Disposition and Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Q1 answered by C2/C3; Q2 by C4/C5/C6; Q3 by W1/C5/C7 and contrarian
dispositions. All three waves executed inline; delegation adds no independent
evidence here. Selected design is implementable without runtime dependencies.
No external scientific claims or exercise values approved. All rates and
magnitudes remain fictional exercise parameters; live AC-066 and R1/R2/R3
analytics approval are not claimed.

Self-check: exact criteria covered, alternatives challenged, provenance retained,
bounded readiness established; no source edits during Research.
