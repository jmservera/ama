---
title: Issue 145 live plan critique
ms.date: 2026-11-18
---

# Critique (single pass, final candidate)

* Verdict: proceed.
* Risk 1: restored copy might not carry the managed identity user. Disposition: contained users restore with the database; probe confirms, else record the failure.
* Risk 2: a restore target on the same server inherits private-link access; no firewall change is needed. Accepted.
* Risk 3: C7 and C6 criteria need seeded revocation/erasure state absent from the demo; seeding would alter the live demo DB, which is outside "no production changes". Disposition: report unproven rather than seed.
* Risk 4: do not claim #121 retention match; #121 legal criteria are deferred to #1906. Disposition: C4 recorded as configuration only.
