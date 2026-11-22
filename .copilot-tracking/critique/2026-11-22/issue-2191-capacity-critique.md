---
title: Issue 2191 capacity critique
ms.date: 2026-11-22
---

Critique executed once (author self-critique) on the final candidate plan. Verdict: approve with direct dispositions.

* Risk: scaling mid receiver window drops the running execution's connections. Disposition: accepted; the next 30 minute window restarts the receiver and the sample starts at that boundary.
* Risk: S3 cost. Disposition: about USD 5 a day, inside the USD 700 cap; recorded so the owner can step down.
* Risk: estate change versus brief-common. Disposition: the goal explicitly authorises raising SQL capacity with az, never Bicep; no other estate change.
* Risk: sampler could read private data. Disposition: it only counts distinct synthetic home ids; no secrets are printed; the job is deleted afterwards.
* Honest sequencing: the diagnostic reads, the baseline samples and the scale were done during the research phase because the plan was a single reversible az command; the changes record states this.
