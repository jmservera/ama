---
title: Issue 108 live research 2026-11-24
description: Research record for the quota-headroom re-query
ms.date: 2026-11-24
---

Refs #108. Research disposition: executed. Planning Readiness: Ready.

Unticked criteria: region model/names/versions/quotas; frozen independent held-out split; human detection; effort/cost comparison; hashes/protocol/outcomes; call authorisation; real AI/SQL/Azure proof.

Finding (live, read-only, 2026-11-24, uksouth, rg `ama`): `az cognitiveservices usage list -l uksouth` now returns Standard and GlobalStandard rows for the served models: `OpenAI.Standard.gpt4.1-mini` current 10 of 5000 and `OpenAI.GlobalStandard.gpt4.1-nano` current 10 of 16000. Current usage equals the deployed capacity of `resident-mini` (10) and `standard` (10), so the rows are attributable to these deployments. The earlier 2026-11-19 record marked headroom `unavailable`. Only one account (`aif-cutover-test-rzsrg`) exists in `ama`; the recorded swedencentral account `aoai-resident-469` is absent. Evidence: [docs/reference/research/issue-108-live-20261124-2026-11-24/](../../docs/reference/research/issue-108-live-20261124-2026-11-24/).
