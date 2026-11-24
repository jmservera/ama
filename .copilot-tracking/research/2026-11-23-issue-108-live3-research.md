---
title: Issue 108 live research, third 2026-11-23 round
ms.date: 2026-11-23
---

Refs #108. Research disposition: executed (live read-only Azure probe). Planning Readiness: Ready.

Issue text read through the REST API. Unticked criteria: region names, versions and quotas; frozen held-out split; human detection; effort and cost comparison; hashes and serving version; call authority; real AI/SQL/Azure proof. Only the region criterion is machine-checkable for the demo.

Findings (2026-11-23, `az cognitiveservices`, group `ama`, account `aif-cutover-test-rzsrg`, uksouth):

* Live `resident-mini` (gpt-4.1-mini 2025-04-14, Standard) has capacity 10, rate limits 10 requests and 10000 tokens per 60 s. The committed serving record says capacity 1 and 1 request, 1000 tokens: stale (Bicep default).
* `standard` (gpt-4.1-nano 2025-04-14, GlobalStandard) capacity 10, matches.
* `az cognitiveservices usage list -l uksouth` now returns rows, but only `OpenAI.GlobalBatch.gpt-4.1*` for these models; no Standard or GlobalStandard TPM quota row, so headroom stays unconfirmed.
