---
title: Issue 188 live proof details
ms.date: 2026-11-18
---

* Window: 12 backfill slots (seed 901, `weather-backfill-v1`) then 12 live slots (seed 184) at 5 minutes, homes ZF-2025-0029/30/31, end slot fixed and in the past.
* Stages: `ingest`, `verify`, `rerun`, all passing the same end slot.
* Success: seam join step inside tolerance; `sensor_handover_verify.run` passed; replay receipts all `replay`; snapshot sha256 unchanged.
* Cleanup list: job, two role assignments, SYN devices.
