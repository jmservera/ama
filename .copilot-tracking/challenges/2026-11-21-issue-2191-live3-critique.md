---
title: Issue 2191 live pass 3 critique
ms.date: 2026-11-21
---

Execution: once, on the final candidate plan, by the RPI agent. Verdict: proceed with conditions, all applied directly.

* Risk: replacing the running job interrupts readings. Condition: deploy over the same job name in one step, then trigger one manual execution and read back the slot.
* Risk: stale hub devices for the old 20 homes. Condition: delete registrations for homes that leave the cohort.
* Risk: key material leaks. Condition: generate in a 0700 temp dir, pass through a 0600 secure parameter file, shred both, never print values or list job secrets with values.
* Risk: the 20 existing consents disagree with the new alternating plan. Condition: run `apply` for the whole new cohort so controls, index and marker are rewritten together.
* Risk: the receiver window now sees more traffic. Condition: read one receiver window's ingest and `sensor_delivery` rows after the change.
* Risk: 449 secrets near the proven 450. Condition: cohort is exactly `ceil(0.5 x homes)`; refuse if the home count grew so that 2n+1 exceeds 450 and report as the limit.
* Rejected: a bundled-certificate source change; unnecessary now that the secret limit is shown to be at least 450.
