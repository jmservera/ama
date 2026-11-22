---
title: Issue 2191 critique
ms.date: 2026-11-22
---

Critique executed once on the final candidate plan. Verdict: approve with direct dispositions.

* Risk: more than 449 secrets was untested. Disposition: accepted; the update is atomic and rolls back to the captured 222 set.
* Risk: consent flips on homes already in the cohort change the demo story. Disposition: accepted; the owner goal requires stored coverage, and a declined minority remains.
* Risk: run time exceeds 240 s with 272 devices. Disposition: replicaTimeout raised to 270 s and run durations read back.
* Risk: freshness margin. Disposition: headroom 10% over the 94.6% measured instant freshness; the live proof is the arbiter, headroom is raised if the proof falls short.
* Risk: tools-only change could skip tests. Disposition: focused tests plus `test_demo_consent_mix` run.
