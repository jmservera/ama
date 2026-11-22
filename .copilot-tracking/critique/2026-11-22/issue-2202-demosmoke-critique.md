---
title: Issue 2202 demo smoke critique (2026-11-22)
---

Executed once. Verdict: approve with direct dispositions.

* Risk: concurrent workers change the same estate, so a failure may not be caused by the deployed code. Disposition: record revision list and timestamps with each failure and state unproven causes.
* Risk: probes print credentials. Disposition: scripts read files at run time and assert the secrets are absent from output before saving.
* Risk: consent toggling changes demo data. Disposition: the resident probe does not toggle consent.
* Risk: criteria cannot all be proven by a smoke. Disposition: reuse the earlier deploy note for rollout and consent evidence; mark the rest unproven with reasons.
* No source change, so tier is focused; no rpi-checks --all.
