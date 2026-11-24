---
title: Issue 2202 live research b, 2026-11-24
description: Second same-day pass over the remaining #2202 demo criteria
ms.date: 2026-11-24
---

## Disposition

Research executed. Planning Readiness: Ready.

## Evidence

* Issue #2202 acceptance has four unticked criteria; the earlier pass is docs/reference/research/issue-2202-live-r68-2026-11-24.md.
* Live probes this pass (docs/reference/research/issue-2202-live-r2-2026-11-24.md): revisions Healthy, hardening enforced, charts, gauges, consent checkbox, chat routing and 58.9% coverage all hold on API 0000068 and resident 0000030.
* New finding: receiver execution job-live-receiver-29925840 Failed (exit 2, `Cannot run: RUN_STOPPED`) at the window edge, 1 of 12 recent runs. Source cause (probable): iot_stream.py on_event raises RUN_STOPPED after the deadline in a bounded window and records it as failure.
* Correction: simulator and receiver jobs run API digest 5a20dbd3, the API app 7610c41b; the earlier note said they matched.
* Unprovable: image digest to commit (registry firewall), rollback drill (not authorised), generative answers (owner actions).

## Plan input

Commit the note and evidence; fix the window-edge failure in src/api with one regression test (full tier for src, coordinator runs gates; rpi-checks --all not run).
