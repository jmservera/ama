---
title: Issue 108 live demo criterion research
description: Opening research record for the unticked acceptance criteria of issue 108
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Research disposition: executed. Existing evidence reused: `docs/reference/research/ai-heldout-batch-432-live-2026-11-18.md` and `docs/reference/research/human-review-effectiveness-live-demo-2026-11-18.md`.

Unticked criteria in scope (8 RAI/tokenomics-related plus 1 model/quota): model/version/quota confirmation, frozen held-out split, human detection of seeded errors, effort/cost comparison, hashes/seed/denominators record, actual-call authorization, real AI/SQL/Azure proof, one-lever routing/caching.

Findings are appended below as probes complete.

## Findings

* Live deployments: `standard` gpt-4.1-nano 2025-04-14 (GlobalStandard, capacity 10, 10 req and 10,000 tokens per 60 s) in uksouth; `resident-mini` gpt-4.1-mini 2025-04-14 (Standard, capacity 1) in swedencentral. Subscription usages route empty.
* Live app report (signed in): consumption schema, registry hash, 132 release-admission denials, 2 recorded chat calls, cost Unknown. Three comparison routes are 403 for the available role.
* Offline: 115 focused harness tests OK; one-lever comparison enforced.
* Existing 12-call batch reused.
* Evidence: `.copilot-tracking/evidence/2026-11-18/issue-108-live/`; note `docs/reference/research/issue-108-live-demo-evidence-2026-11-18.md`.

Planning Readiness: Ready. No criterion becomes tickable; no source change needed (tier FOCUSED).
