---
title: Issue 2191 live critique (2026-11-21)
ms.date: 2026-11-21
---

Critique executed once on the final candidate plan. Verdict: proceed, 0 blocking, 3 non-blocking applied.

* Raising `MAX_COHORT` is a safety-control change. Applied: 500 stays well under the 1,250 home quota ceiling, `check_capacity` still gates every start, and the change is recorded in the changes note.
* A skip must not look like a sink failure or a control fence. Applied: separate `skipped` counter and `DEVICE_SKIPPED` code, not counted in `failed`.
* Default must preserve behaviour. Applied: rate 0 draws nothing and changes no existing output; invalid rates give `SIM_CONFIG_INVALID`.
