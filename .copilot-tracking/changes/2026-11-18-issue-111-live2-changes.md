---
title: Issue 111 live2 changes
ms.date: 2026-11-18
---

Refs #111. Tier FOCUSED (docs and evidence only; no src, SQL, infra or deployment change; no Azure change).

## Changes

* Added docs/reference/research/issue-111-live2-sensor-evidence-2026-11-18.md and raw/ screenshot folder issue-111-live2-raw/.
* Updated docs/reference/README.md index and docs/reference/log.md.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Outputs are reproducible from retained readings | Proven (already ticked) | core-sensor-tests*.txt; live repeat call byte-identical |
| Thresholds are sourced or labelled exercise values | Proven (already ticked) | live payload `calibrated: false`, synthetic provenance |
| R1 to R3 complete before use beyond an exercise rule | Unproven; cannot be proven for the demo | Requires named reviewer and Asset sign-off (R2), agreed limits (R3), official standards texts (R1) |
