---
title: Issue 2202 deployment receipt and repeatable check (demo, 2026-11-23)
description: Read-only live receipt of image digests, hardening and revision health for the demo apps and jobs, produced by the extended demo preflight tool
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, owner decisions of 2026-11-18. No Azure write and no throwaway resource. Output without secrets: [preflight.txt](./issue-2202-live-receipt-2026-11-23/preflight.txt), run 2026-11-23T15:39:50Z.

## Tool change

`tools/demo_preflight.py` now adds a deployment check for the API, resident, agents app and the five jobs. It reads the first container image and only the value of `ZF_CONTAINER_HARDENING`, prints the 12 character digest prefix, and fails unless the digest exists and hardening is `enforced`. Tests: `tools/test_demo_preflight.py` (10 tests).

## Live result

* API `--0000055` and resident `--0000028` are Healthy, 100% traffic, `/healthz` 200.
* All eight workloads report `ZF_CONTAINER_HARDENING=enforced`, including the agents app, so there is no agents difference to explain on this read.
* Digests differ: API `b628e0678f72`, simulator `295164ca739d`, receiver `541068a62d81`. The jobs do not run the API image, so a single rebuild from current main is not shown.
* The cohort and consent counts were unavailable (SQL not reachable from this host).

## Per-criterion table (issue 2202)

| Criterion | Status | Evidence and limit |
| --- | --- | --- |
| Images rebuilt from main and rolled | Unproven | Digests differ across API, simulator and receiver; the registry is firewalled and the image carries no build commit in its template, so the source commit cannot be read. A rebuild needs a registry firewall opening, which this pass did not do |
| Revisions Running and Healthy; hardening enforced; rollback noted; agents difference explained | Proven (rollback not exercised) | preflight.txt; rollback target is the previous revision, activated with `az containerapp revision activate` |
| Owner demo checks (charts, gauges, consent, chat routing, half of homes) | Not re-run here | Proven on earlier revisions in [live deploy](./issue-2202-live-deploy-2026-11-22.md); half of homes as stored readings stays unproven |
| Live receipt and log entry | Proven | this note and the log entry |
