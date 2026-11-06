---
title: Plan for #188 live-sim-reading-v1 admission (stacked slices)
ms.date: 2026-11-05
---

* Slice 1 (this PR, Refs #188): the SQL sensor consumer admits `live-sim-reading-v1`, retains sunlight in the accepted witness, returns it in `observed_series`, tests and README. Details: [details](../details/2026-11-05-live-sim-ingest-188-details.md).
* Slice 2 (owner-gated SQL): add a `sunlight_wm2` column to `sensor_reading` and the stock DDL, with migration; needs SQL gate.
* Slice 3 (after deploy and #185): run the live container for several homes, then run the existing handover verifier (#645) on live plus backfill and record the tolerance result.
* Critique: executed once inline; compatible findings applied (no new column, fail closed to data-quality exceptions with the manual route, no Azure access, scenario pattern widened only for live rows). Verdict: proceed.
* Validation tier: focused. The consumer is SQL-facing code but no schema, DDL, infrastructure or deployment changed; MSSQL path was not run. The complete gate is left to the coordinator if the owner treats it as SQL-sensitive.
* [ ] Human review of the change is required and left unchecked.
