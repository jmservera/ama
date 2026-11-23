---
title: Issue 108 live research, second 2026-11-23 round
ms.date: 2026-11-23
---

Refs #108. Research disposition: executed. Planning Readiness: Ready. GitHub issue text was unavailable (API rate limit), so criteria come from the earlier notes under `docs/reference/research/issue-108-*`.

* Prior follow-up: attest the `ca-resident-demo` serving deployment.
* Azure CLI 2026-11-23 (read-only, existing login): `ca-resident-demo` latest ready revision `ca-resident-demo--0000028`, active, Healthy, traffic 100, created 2026-11-23T12:31:09Z, image `crcutovertestrzsrg.azurecr.io/zava-resident-demo@sha256:e6c7e755343a02efdc594aa10c2af66dd1818ea9a6ce06c806ae4ae59adf1054`; `ZF_DEMO_ASSISTANT_ENDPOINT` is `https://aif-cutover-test-rzsrg.openai.azure.com`.
* `src/api/.../resident_demo/aoai.py` sets `DEPLOYMENT = "resident-mini"`, which the committed serving record lists as gpt-4.1-mini 2025-04-14 on that account.
* Gap: nothing ties the code deployment name or the Bicep deployment names to the record. Buildable: extend the offline drift test in `src/agents/tests/test_ai_eval.py`.
* Other criteria need labellers, people, Finance or production authority: not provable for the demo.
