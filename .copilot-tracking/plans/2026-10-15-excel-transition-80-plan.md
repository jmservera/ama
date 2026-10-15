---
title: Plan for issue 80 Excel transition
description: Plan for the src/importer Excel transition library
ms.date: 2026-10-15
---

## Phases

* [x] Phase 1: `xlsx` reader and writer with guards.
* [x] Phase 2: `mapping` declared structure, conflicts, row preview, lineage, scan, unchanged-source check.
* [x] Phase 3: `quarantine` store with human approval gate and supersession history.
* [x] Phase 4: `export` CSV and read-only Excel with history; read-only comparison; CLI preview.
* [x] Phase 5: tests, ruff, mypy, local run; docs, index and log.

Details: [phase details](../details/2026-10-15-excel-transition-80-details.md).

## Critique (one pass, direct)

Verdict: proceed. Applied: reject XML entities; neutralise formula injection on export; approver must differ from stager; replace NVARCHAR(MAX) with NVARCHAR(4000) for portability. Rejected: add openpyxl (conflicts with stdlib decision and hashed pins).

## Not planned (needs owner or evidence)

Thresholds, web screens, per-list export wiring, AI assist, image and SQL role.
