---
title: Issue 2191 half of homes fresh, critique (2026-11-22)
---

Critique executed once (self-critique of the final candidate). Verdict: approve with direct dispositions.

* Risk: a sampler that counts all stored rows could overstate freshness. Disposition: filter on `observed_at` in the last 15 minutes, as the owner's measure.
* Risk: the first sample after a receiver restart dips. Disposition: report every sample, including dips, and the mean with and without it.
* Risk: sampler leftover resource. Disposition: delete and read back the job list.
* Risk: attributing the fix. Disposition: cite the earlier DTU evidence; this task does not change the estate unless coverage falls below half.
