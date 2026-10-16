---
title: Issue 176 reproducibility research
description: Offline generator provenance and refresh investigation
ms.date: 2026-10-16
---

## Brief and controls

Task #176, slug `synthetic-determinism-176`. Focused, internal convergence
research for implementation and acceptance audit. Read the issue and its
comments, original case study, addendum, reference index and memory. Work only
on the existing clean `feat/synthetic-determinism-176` topic. No Azure, private
datasets, legacy application edits, tenant identifiers or setup-entra changes.
The user explicitly requests the complete RPI delivery, tests and PR.

## Questions and participation

Which generators already reproduce? What prevents stock-register reproduction?
What input provenance and refresh protection are missing?
Research is inline: tightly coupled source investigation does not justify
delegation. RPI skills and ADR 0006 apply; UI, legal-source research and cloud
tools are excluded. No interaction is available or required for this brief.

## Cycle 1

### Wider

C1: src/core/tests/test_synthetic_determinism.py:40-114 already compares
every scale/sensor output byte, multiple sensor shards, seed/date changes
and exact windows. C2: src/core/tests/test_sensor_stock.py:138-160 repeats
register-backed sensor bytes. Both operate on fictional inputs.

### Deeper

C3: src/core/src/zava_forward/core/synthetic/stock_fabric.py:283-409 records
seed, algorithm version, full source revision and payload hashes. Its CLI
lacks an as-of input label and input digests; reconstructing optional linked
case output requires both the register and the case snapshot, not seed alone.
C4: src/core/src/zava_forward/core/synthetic/provenance.py:17-46 fingerprints
source dependencies and refuses nonempty output and direct symlinks.
C5: src/core/src/zava_forward/core/synthetic/sensor_backfill.py:176-260 records
seed, date, versions, sources, payload hashes and normalized stock input digest.
No generator reset authority follows from generating a new directory.

### Contrarian

C6: docs/reference/research/retrofit-synthetic-data/README.md:113-191 explicitly
records that the retained OSM-backed register generator is absent. Tracked
generator inventory and Git path-history search reveal no retained register
generator. A new fictional generator or scale fixture cannot reproduce that
register and would misstate AC1. No private dataset was opened.
C7: src/core/tests/test_generated_dataset.py:55-68 supplies a constructed
register to the retained builder. It proves conditional reproduction only.
Legacy support source stays unchanged; no new implementation outside src.

## Synthesis and decisions

Accepted: extend the existing fabric CLI, not create substitute stock.
Record optional explicit ISO as-of label (unknown when omitted) and exact
register/case input digests from the same bytes consumed. Preserve all
fabric draws, payloads, default paths and approval boundaries. Add exact
CLI-byte, seed/date/input sensitivity and refused-refresh evidence.
Rejected: invented register reconstruction and implied owner policy approval.
One complete focused cycle is sufficient: remaining private source and
approval gaps cannot be resolved by more offline code search.

## Disposition and readiness

Research disposition: executed. Planning Readiness: Ready for bounded
implementation and honest partial-acceptance audit. AC1 remains blocked for
the original stock register; policy adoption remains unapproved. User asks
for unmet criteria to be marked and a Refs PR, so these are acceptance gaps,
not reasons to withhold the independent offline improvement.
