---
title: Plan for #184 live simulator container (stacked slices)
ms.date: 2026-11-04
---

* Slice 1 (this PR, Refs #184): generator, runner with fake and stdout sinks, Dockerfile, authored job template, docs and cost estimate. Details: [details](../details/2026-11-04-live-simulator-184-details.md).
* Slice 2 (owner gated): approve live sending, register `SYN-` devices from the #185 manifest, certificate share, SQL read grant, image push, deploy the job, then Hub-side evidence for the leak criterion.
* Slice 3 (#110 and #140): consumer and route accept `live-sim-reading-v1` including `sunlight_wm2`.
* Critique: executed once inline; compatible findings applied (fail closed on capacity, fixed error codes, no credential in env or image, dry run default, tag-less image refused). Verdict: proceed.
* Validation tier: focused. The slice touches infrastructure (Bicep) and deployment artefacts, so the complete gate is not run here and is left to the coordinator.
* [ ] Human review of copy, cost and approval boundaries is required and left unchecked.
