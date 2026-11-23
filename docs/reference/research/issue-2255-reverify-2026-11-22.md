---
title: Issue 2255 safety case target clocks re-verified live on revision 0000054 (demo, 2026-11-22)
description: Read-only desktop Playwright re-check that the synthetic demo safety queue still shows elapsed hazard clocks, response targets and named owners on revision 0000054, with a per-criterion table
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, owner decisions of 2026-11-18. Sign-in values were read at run time and never printed or stored. Refs #2255. Read-only: no Azure change, no SQL write, no deploy, no push, no resource created.

## Revision

`az containerapp revision list` shows `ca-cutover-test-demo-api--0000054` active (created 2026-11-22T23:14:23Z, image digest `sha256:3f2be664...`); `latestRevisionName` and `latestReadyRevisionName` both name it. The seeded fields from the [backfill note](./issue-2255-backfill-2026-11-22.md) live in the SQL store, not in the image, so a new revision should keep them.

## Probe

[probe_clock.py](./issue-2255-reverify-2026-11-22/probe_clock.py) signs in as staff, opens `/app#/all`, filters "Safety issue open", waits for the last ranked row and counts clock text. Output: [probe-rev54.json](./issue-2255-reverify-2026-11-22/probe-rev54.json); full-page screenshot: [safety-queue-rev54.png](./issue-2255-reverify-2026-11-22/screens/safety-queue-rev54.png).

| Measure | Result on 0000054 |
| --- | --- |
| Ranked rows in the safety queue | 23 (API total 23; dataset `as_of` 2026-10-16) |
| Rows with a hazard clock | 22 (the 23rd row shows a safeguarding 48 hour clock instead) |
| "elapsed time unknown; no response target window recorded" | 0 (issue observed 22 of 22) |
| Clocks with elapsed hours and a service response due time | 22 |
| Response overdue / response open (running) | 17 / 5 |
| Named accountable owners | 23 rows carry an owner |

Running example: "Hazard clock: 68 hours elapsed; service response due 2026-10-20T04:00:00Z; response open. Accountable owner: Karen Lawson ... resident update due: Unknown. Existing hazard and repairs service own[s timing]".

Method note: the first two runs counted only one clock because the queue had not finished rendering; the probe now waits for the last ranked row. The 5 running clocks compare with 6 re-dated hazards in the backfill note; the 23 rows include a safeguarding case whose clock is not a hazard clock, so the running count is not reconciled to the backfill figure and is reported as observed.

## Per-criterion table

The issue has no tick list; criteria come from its Expected paragraph and the backfill table.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Elapsed time shown against a target, not "unknown" | Proven on 0000054 | 22 of 22 hazard rows; 0 unknown |
| Some clocks running with a target window | Proven | 5 "response open" rows with a due time; 17 overdue |
| Named accountable owner still shown | Proven | owner on all 23 rows |
| Hazard service stays timing authority | Partly | text states the hazard and repairs service owns timing; seeded due times are synthetic reference values; no `responded_at` or update time written |
| Survives a new revision | Proven | state unchanged after 0000054 went live |
| Survives a dataset re-seed | Not proven | not tested; changing data in the demo store is outside this read-only pass; the backfill note records that a re-seed drops the fields |
| Independent exact-head review, hosted CI, full local gate | Unproven here | no src change; focused tier; not run |
