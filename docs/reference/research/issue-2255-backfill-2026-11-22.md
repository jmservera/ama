---
title: Issue 2255 demo hazards get an awareness time and target clock (demo, 2026-11-22)
description: Live backfill of aware_at and a reference response target on the synthetic demo hazards through the demo API replica, with before and after safety-queue proofs and a per-criterion table
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, owner decisions of 2026-11-18. Sign-in values were read at run time and never printed. Probe and outputs: [issue-2255-backfill-2026-11-22/](./issue-2255-backfill-2026-11-22/). Refs #2255. Nothing was deployed or pushed; no Azure resource was created.

## Cause

The 23 open demo hazards (22 cases in the safety queue) were generated without `aware_at` or `response_due_at`. `hazard_clock` in `src/core/.../taskqueues.py` fails closed to "elapsed time unknown; no response target window recorded" when they are absent. The queue evaluates time against the dataset `as_of` snapshot, not the wall clock.

## Path chosen

`SqlStore.merge_seed` is insert-only, and the SQL server has public access Disabled, so the existing private route was used: one interactive `az containerapp exec` into `ca-cutover-test-demo-api` (the app's own `ZF_STORE=mssql` settings and managed identity), staging [`infra/scripts/seed_demo_hazard_clock.py`](../../../infra/scripts/seed_demo_hazard_clock.py) in `/tmp` and removing it afterwards. The tool writes through `store._case`, `store.audit` and `store.save` only.

Rules, all counts-only output:

* Only open, non-safeguarding hazards without `aware_at`; never overwrites.
* `aware_at` from the hazard's own `recorded_at`, else `noticed` at 09:00 UTC; an anchor after `as_of` is skipped.
* `response_due_at` is the existing reference window from awareness (Emergency 24 h, Significant 7 d, Routine 14 d), only when absent; no `responded_at` or resident update time is written.
* An optional N re-dates N evenly spread hazards to 40 percent of their window before `as_of`, so some clocks are running. The original `noticed` is kept.
* Every change carries `demo_clock_seed` (synthetic marker); `revert` undoes exactly those changes; one audit entry per run.

## Live run

| Step | Output (counts only) |
| --- | --- |
| Inspect before | 980 cases, 23 hazards to write, 53 released skipped; all 23 are 14 days or older |
| First apply (wall-clock reference) | Applied; the probe showed 5 clocks still "unknown" because the re-dated ones fell after `as_of` |
| Fix | Reference time changed to the store `as_of`; `revert` added; revert reverted 23 |
| Second apply, awareness only | 22 of 22 queue clocks showed elapsed hours, but "no response target window recorded" remained |
| Third apply, with reference target | `revert` 23, `apply 6`: 23 written, projected 6 running and 17 overdue |
| Inspect after | 0 to write, 23 already have `aware_at` (idempotent) |

Queue before and after ([probe-before.json](./issue-2255-backfill-2026-11-22/probe-before.json), [probe-after.json](./issue-2255-backfill-2026-11-22/probe-after.json), screenshots in [screens/](./issue-2255-backfill-2026-11-22/screens/)): before 22 unknown, 0 with elapsed hours; after 0 unknown, 22 with elapsed hours, 22 named owners, 17 reading "response overdue".

Running example: "Hazard clock: 68 hours elapsed; service response due 2026-10-20T04:00:00Z; response open. Accountable owner: Karen Lawson ... Existing hazard and repairs service owns timing."

## Per-criterion table

The issue has no tick list; its expected behaviour is split into checks.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Safety cases show elapsed time | Proven | after probe: 22 of 22 "N hours elapsed" |
| Response target window shown | Proven | 22 of 22 carry "service response due ..."; samples above |
| A running clock is visible for some cases | Proven | 6 hazards re-dated; running sample "response open" (68 hours elapsed) |
| Named owner still shown | Proven | 22 named owners |
| Hazard service stays timing authority | Partly | no `responded_at` or update time written and the text states the service owns timing; the seeded due times are synthetic reference values, marked and revertible |
| Repo seeding path for synthetic demo data only | Proven | `infra/scripts/seed_demo_hazard_clock.py`, 4 unit tests, ruff check and format pass |
| Re-runnable and reversible | Proven | inspect after apply: 0 to write; `revert` reverted 23, then re-applied |
| Clock stays valid over time | Not proven | the queue reads the dataset `as_of`, so the state is stable until the dataset is re-seeded; a re-seed would drop these fields |
| No deploy, push or new Azure resource | Proven | none done; temp files removed from the replica |
| Independent exact-head review, hosted CI, full local gate | Unproven | not run here; live SQL write is the full tier and `rpi-checks.py --all` is the coordinator's |
