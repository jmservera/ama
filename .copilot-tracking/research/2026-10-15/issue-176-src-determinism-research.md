---
title: Issue 176 src synthetic determinism research
description: Focused post-pivot evidence and remaining acceptance boundaries
ms.date: 2026-10-15
---

## Research brief

Execute the explicitly requested full RPI loop for #176 on
`feat/src-synthetic-determinism-176`. Convergence output for implementation:
determinism, seed/date recording, versioning and safe refresh, not new sensor
physics, real stock/address retrieval, deployment or approval authority.
Research root: `.copilot-tracking/research/2026-10-15/`.
Posture: focused, selected for the caller's bounded internal task.

## Extensions and participation

Repository instructions, ADR 0006 and parity matrix selected as architecture
constraints. RPI phase skills selected as lifecycle contracts. Python practices
apply to new typed helpers. No specialist research lane is needed for this
continuous trace. No interaction: scope and owner direction are explicit.
Prior research is historical evidence, not a current completion claim.

## Questions

* Q1: Which missing criteria now have migrated implementation to reuse?
* Q2: What metadata and byte-level tests are still absent?
* Q3: Which refresh and external-evidence decisions must remain unapproved?

## Cycle 1

### Wider

Read issue body/comments and confirmed merged #296 through #302. Existing
support generators and their tests already cover pack, operational dataset,
fabric and EPC determinism. Unlike the earlier research, a sensor generator
now exists in core. The private stock-register generator remains absent.
Reflection: reuse the moved sensor and scale generators; do not invent a
replacement for the private register.

### Deeper

Sensor output has a fixed UTC start but no explicit as-of parameter or
generator revision; its existing test compares only one readings shard.
Scale fixture has fixed event dates, a seed and version but no revision.
Both writers overwrite existing outputs and accept invalid sizes.
Reflection: add date/provenance and whole-directory byte comparisons, plus
fail-before-write protection and parameter validation.

### Contrarian

The wholly fictional scale register is not the private OSM-anchored stock
register. Its determinism cannot close private-register acceptance. A local
sensor sample cannot prove the full two-year/60,000-home run or live sensor
contract. Automatic overwrite or an escape hatch would undermine refresh
protection; prefer a new or empty destination, preserving existing bytes.
Source fingerprints must include shared generator dependencies, not Git HEAD
or wall-clock time. Keep historical default series unchanged.
Reflection: scope is engineering evidence only; cadence/approver approval and
private source reproduction remain open. No second cycle is needed: the
remaining gaps cannot be resolved by additional in-scope source inspection.

## Evidence

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/176 (retrieved 2026-10-15) | Three unchanged ACs; owner says manifests alone are insufficient; src pivot only changes location |
| W2 | https://github.com/jmservera/ama/pull/298 (retrieved 2026-10-15) | Synthetic modules moved to core in M3 |
| W3 | https://github.com/jmservera/ama/pull/302 (retrieved 2026-10-15) | Per-project guides replace executable mvp tree |
| C1 | docs/adrs/0006-src-layout-and-cutover.md:49 | New code in src, core imports no workload, private data outside packages |
| C2 | docs/architecture/mvp-to-src-parity-matrix.md:201 | Generator work reuses core/synthetic; private register reproduction unproven (issue row at 366) |
| C3 | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:162 | Existing deterministic writer, fixed start, no revision or refresh guard |
| C4 | src/core/src/zava_forward/core/synthetic/scale_fixture.py:81 | Existing fictional stock-scale writer and manifest |
| C5 | src/core/tests/test_generated_dataset.py:133 | Existing support-generator determinism and revision tests |
| C6 | docs/reference/research/retrofit-synthetic-data/README.md:102 | Proposed refresh cadence, owner approval and protected live state |
| C7 | src/core/tests/test_sensor_backfill.py:20 | Existing single-shard seed comparison, idempotent portable insert coverage |

## Decisions and alternatives

Accept extending existing src generators with dependency-aware revision,
recorded as-of, parameter validation, new-destination-only writes and exact
output comparisons. Reject changing support generators or replacing the
missing private register. Preserve existing sensor physics, consent,
human-approval and AI configuration. Do not enable an unevidenced model or
claim real inference; local app evidence will distinguish AI-enabled from
real-model execution.

## Readiness and residuals

Research disposition: executed. Planning Readiness: Ready for the bounded
engineering slice. Full AC1/AC2 remain unproven for the private stock generator;
AC3's proposed values require owner approval. Sensor climate/device evidence,
full-scale generation and actual Azure model/deployment evidence remain outside
this slice. No private data will be read or committed.
