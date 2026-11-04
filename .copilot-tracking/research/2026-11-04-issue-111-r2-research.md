---
title: Issue 111 round 2 research
ms.date: 2026-11-04
---

Research disposition: reused (round 1 research plus fresh code and PR check).

* Merged: #871 (pure exercise analysis, no store wiring) and #996 (scenario tests over production code). Issue comments confirm bounded read-only slice authorised in principle and R1 to R3 open.
* Gap routed by the round 1 review: analysis is not wired to retained store rows. `SensorConsumer.observed_series` already returns canonical retained rows; consent exists only inside control bodies and had no read accessor.
* Planning readiness: Ready for a read-only slice. Task creation, ranking and rule approval stay out of scope (no approved rule, R2/R3 missing).
* Touches SQL (read queries only): focused tier, gate not run; coordinator owns any gate.
