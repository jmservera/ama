---
title: Issue 2192 review (round 3)
date: 2026-11-22
---

Review executed once. Outcome: conformant for the local and live scope stated.

* Boundary: image-only roll of `ca-resident-demo`; projected diff and registry readback match the plan.
* Evidence: employee state change `consent-withheld`, `ok`, `consent-withheld` for the resident case, with the resident restored. No credential or email in committed artifacts (emails scrubbed in the probe output).
* Open items routed to a later task: read Azure SQL `sensor_consent_audit` rows with an operator principal (audit criterion stays proven locally only); diagnose the single transient stall of the checkbox re-enable on the first run.
* Hosted CI, independent exact-head review and merge approval remain with the owner.
