---
title: Plan for #462 resident demo journey slice
ms.date: 2026-11-04
---

* Slice 1 (this PR): plain-language sensor statuses and a slow-start notice. Later slices (not started): local-time display, owner-run authenticated live checks after any deploy.
* Phase 1: reword the three sensor channel statuses in `resident_showcase._sensor_channel` and the gauge note in `demo.js`.
* Phase 2: add a slow-start status message after 4 seconds of loading, cleared when the session call settles.
* Phase 3: update unit tests and the browser check strings; add a static asset test.
* Validation tier: focused. No security, infrastructure, SQL or deployment change, so no gate. Live deploy is not part of this slice.
* Critique: executed once, inline, before implementation. Compatible findings applied: keep the 4 second timer scoped to the current transition so a sign in is not overwritten; keep the older-value fallback ban. No significant or divergent issue.
* Details: [details](../details/2026-11-04-resident-demo-journey-462-details.md).
