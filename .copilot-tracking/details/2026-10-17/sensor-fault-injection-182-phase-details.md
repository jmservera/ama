---
title: Sensor fault injection phase details
description: Evidence and completion conditions for task 182
ms.date: 2026-10-17
---

## Metadata

Task 182 / sensor-fault-injection-182.
Plan: .copilot-tracking/plans/2026-10-17/sensor-fault-injection-182-plan.md.
Research: .copilot-tracking/research/2026-10-17/sensor-fault-injection-182-research.md.
Initial direction: reuse the streaming writer, not a parallel generator.
No implementation blocker. Source/data outputs are distinct from tracking artifacts.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Opt-in contract | Ready | P01-T01, P01-T02 |
| P02 | Validate and document | Ready after P01 | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Implement opt-in contract

Context: research C2-C5 establish legacy labels, streaming helpers, stock
exclusions and golden bytes. Explicit opt-in is the compatibility boundary.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Tests and packet injector

Start with a focused test file importing the not-yet-existing module to prove
missing feature, then implement typed immutable validated rates and two-row
packet transforms. Independent Random stream keyed by seed/sensor. Keep
nominal clean rows in truth; output rows are copies, never mutated truth.
All packet classes, including stuck and progressive drift, have fixed labelled
exercise semantics. Empty granted population yields empty truth, no invented rows.
Tests maximum 16 methods, no test deletion; use subTests for named classes.
Completion: exact transformations, validation and deterministic semantics pass.
PC-001 completion: canonical class order, direct truth-sequence assertions across
equivalent option ordering, estimate calls, shard sizes and alternate seed.
2,000 packets, duplicate 0.2/gap 0.3, tolerance +/-0.04; a constant fault RNG
seed mutation must fail independently of the clean generator seed.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Integrate current writer

Preflight config/window/destination before preparing output. Opt-in uses same
sensor identity/fabric but fault_profile=none internally; strip profile on disk.
Use packet iterator for both estimate sampling and shard output, not independent
fault logic. Keep existing legacy branch and exact CSV serialization untouched.
Analysis row positions are zero-based within their shard; truth describes both
nominal observations even when no output exists. Write evaluator config and
payload hashes separately; no label-bearing config in analysis metadata.
Opt-in manifest/schema version distinct from reading-v1. Reject both snapshot
root and analysis subdirectory at load_into entry before DB operations.
Completion: CLI, output safety, hashes, estimates and stock exclusions tested.
PC-002 completion: at least three granted sensors over two-sensor shards;
valid/gap/duplicate/reversed packets; every emitted CSV position reconciles
exactly once to correct truth, no header offsets, correct duplicate identities,
empty gap positions and shard-only resets. Counter-reset mutation must fail.

<!-- rpi:phase id=P02 -->
## P02: Validate and document

<!-- rpi:task id=P02-T01 -->
### P02-T01: Executable evidence

Use own session venv (pip-only editable src/core[dev]) after confirmed missing
dependencies. Run focused tests and selected deliberate mutant substitutions
for missing corruption, embedded labels, no reorder, lost gap truth and rates
ignored. Mutations may run in memory; no persistent changed source is required.
Run current core suite and existing Ruff/mypy commands from src/core.
CLI tiny fictional register subset demonstrates granted/declined/unknown,
nonempty refusal, byte rerun and emitted-row/truth/hash reconciliation.
No private source, full-stock run, SQL/IoT/AI/Azure or spending.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Documentation and handoff

Document packet-rate semantics, every corruption magnitude, paths, evaluator-only
truth, new-schema consumer limitation and legacy compatibility. Update the
existing synthesis/index/log, no new knowledge-base page. Changes evidence
records commands and actual failures/corrections. Reconcile plan markers and
details with completed work before a single post-implementation Review.
Publication follows Review with criterion-by-criterion PR audit and verified
noreply author/committer, requested trailer, ordinary topic push only.
