---
title: Resident demo bulkhead capacity decision (#1054, slice 3) research
---

* Merged: #1067 (Retry-After, busy wording), #1115 (client retries a shed view once). Both Refs #1054.
* Unmet: decision on whether 8 is right (needs live re-measured burst); live verification on ca-resident-demo.
* Evidence: infra/resident-demo.bicep scale minReplicas 0, maxReplicas 1; docs/reference/research/ux/zava-forward-prototype-profile-review.md burst record.
* Planning readiness: Ready. Slice: record decision (keep 8) in code, add boundary and signed-in shed tests. No security, SQL, infra or deployment change.
