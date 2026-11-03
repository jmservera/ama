---
title: Research, issue 176 fictional stock register generator
ms.date: 2026-11-03
---

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery (merged PRs, read from gh)

* #237, #257, #309, #368, #633, #703 delivered manifests, fabric and EPC determinism, protected refresh and a one-command replay audit (`determinism_audit.py`) over scale, sensor backfill, sensor scenarios, fabric, public pack and EPC.
* Issue comments: the refresh-policy criterion is ticked; criteria 1 and 2 are unmet because the original private OSM stock register generator and pinned inputs are absent.

## Gap

The audit builds an inline eight-home register, so no in-repo generator produces a register from a seed and as-of date. The original cannot be recovered; a fictional replacement can still be made reproducible and manifested.

## Slice chosen

Add `src/core/.../synthetic/stock_register.py` (seeded, manifest with seed, version, generator revision, as-of, payload hash) and replay it in the audit. No security, infrastructure, SQL or deployment surface; focused tier applies.

## Boundaries

Not the original register; no OSM data; no private data read; no approvals changed.
