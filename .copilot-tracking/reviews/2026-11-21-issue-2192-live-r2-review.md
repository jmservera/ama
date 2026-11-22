---
title: Issue 2192 review (round 2)
date: 2026-11-21
---

Review executed once on the local diff. Outcome: conformant for local scope; live employee-effect proof routed to a follow-up.

* Diff: `apply` is small, the primary set still fails closed; only `ValueError` (unknown home) is swallowed for the secondary home. A non-ValueError from the secondary raises, giving the resident an error and the card re-read.
* Residual risk: two non-atomic writes; each is audited. Accepted for the demo.
* Evidence honesty: the live employee criterion and Azure SQL audit rows are recorded as unproven, with reasons.
* Routed: deploy the reviewed commit to ca-resident-demo and re-run `live_probe.py`.
