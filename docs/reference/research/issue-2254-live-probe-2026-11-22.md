---
title: Issue 2254 safety count mismatch, live probe and cause (2026-11-22)
description: Live reproduction of the 23 versus 22 safety issue counts on the demo API, the source cause in the SQL derived column repair, and per-criterion evidence
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop 1440x900, resource group `ama`, owner decisions of 2026-11-18. Read-only live probe; no Azure change and no throwaway resource. Sign-in values were read at runtime from the owner files and are not recorded.

## Live reproduction

Probe: [probe_safety_count.py](./issue-2254-live-probe-2026-11-22/probe_safety_count.py), result [probe-safety-count-result.json](./issue-2254-live-probe-2026-11-22/probe-safety-count-result.json), screenshot [overview-2254.png](./issue-2254-live-probe-2026-11-22/screens/overview-2254.png). Run against `ca-cutover-test-demo-api` as the owner demo identity.

| Surface | Source in code | Count read |
| --- | --- | --- |
| Overview tile (`/api/stats` `kpis.hazards`) | `insights.has_hazard` on each open case body | 23 |
| Map (`/api/map`, mode `points`, kind `hazard`) | `insights.has_hazard` on each case body | 23 |
| Safety filter (`/api/cases?view=all&flag=hazard`) | SQL column `cases.hazard = 1` | 22 |

One case, ZF-2025-0148 (open, stage "Waiting for block programme"), is a safety case on the map and not in the list. Its case detail shows no released or open hazard rows and no safeguarding keys, so the body-level rule and the stored column disagree for that row.

## Cause

`has_hazard` and the SQL `hazard` column use the same function, `taskqueues.has_open_safety`, but the column is written only when a case row is written. `SqlStore._repair_identity_columns` rebuilds derived columns of any case whose `stage`, `area`, `wave`, `owner_code`, `closed` or `contractor` column differs from the body, and it never compared `hazard`. A body that gained or lost an open safety item (or a definition change in `has_open_safety`) without a matching column write kept a stale `hazard` flag indefinitely. The tile and map read the body, so they moved; the list filter read the stale column. Locally the new test reproduces 3 listed against 4 on the tile before the fix.

## Not provable for the demo

The live SQL server has public access disabled, so the stored `hazard` column and body of ZF-2025-0148 cannot be read without changing the estate. The link from the live row to this cause is inferred from the code path and the local reproduction, not observed.

## Criteria

The issue states no ticked acceptance list; the stated expectation is one definition across tile, map and list. Per-criterion results are in the changes record.
