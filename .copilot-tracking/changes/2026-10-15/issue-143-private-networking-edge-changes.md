---
title: Issue 143 changes
date: 2026-10-15
---

## Changes

* Added `infra/modules/edge.bicep`.
* Modified `infra/main.bicep` (params, guard inputs, edge module, outputs), `infra/modules/guard.bicep` (two guards), `infra/modules/containerapps.bicep` (`behindPublicEdge`, forward proxy).
* Added `infra/tests/test_edge_module.py`; extended `infra/README.md`.

## Validation

`az bicep build` and `lint` clean; infra tests 64 pass. mvp is untouched (no knowledge-base files changed, so no log entry).

## Divergences

No deployment evidence; recorded as open items in `infra/README.md`.
