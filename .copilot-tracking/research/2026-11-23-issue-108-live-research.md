---
title: Issue 108 live research 2026-11-23
ms.date: 2026-11-23
---

Refs #108. Research disposition: executed. Planning Readiness: Ready.

* First unticked criterion: model names, versions and quotas confirmed in the chosen region.
* Azure CLI (read-only, existing login, 2026-11-23): account `aif-cutover-test-rzsrg` (AIServices, uksouth) holds `standard` (gpt-4.1-nano 2025-04-14, GlobalStandard, capacity 10, 10 requests and 10000 tokens per 60 s) and `resident-mini` (gpt-4.1-mini 2025-04-14, Standard, capacity 1). Model catalogue lists both as retiring 2027-04-14. `usage list -l uksouth` returns only GlobalBatch rows; no per-model TPM headroom row.
* Code gap: the committed serving-region record under docs is checked by `ai_eval.region_confirmation` but nothing ties its model names and versions to the infra pins (`infra/main.bicep`, `infra/resident-assistant.bicep`).
* Buildable: one offline drift test in `src/agents/tests/test_ai_eval.py`. Focused tier; no rpi-checks --all.
* Other criteria need an independent labeller, people, Finance or a production authority: not provable for the demo.
