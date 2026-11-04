---
title: Plan for #99 slice 1
ms.date: 2026-11-04
---

* [x] Route `GET /api/finance/exposure` to `exposure_signal`, same permission kind as the finance queue.
* [x] Add the route to the role endpoint inventory.
* [x] Add loopback tests: Held without file, Breach with no record change, Unknown pauses, non-finance refused.
* [x] Document the route in `src/api/README.md`.
* Critique (single pass, self): read-only, no new authority, Held by default; no changes needed.
