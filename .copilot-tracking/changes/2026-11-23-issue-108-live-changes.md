---
title: Issue 108 live changes 2026-11-23
ms.date: 2026-11-23
---

Refs #108. Tier: focused. One file changed: `src/agents/tests/test_ai_eval.py` gains `test_serving_region_record_matches_infra_model_pins`, which fails if the committed Azure serving-region record and the Bicep model pins (`infra/main.bicep`, `infra/resident-assistant.bicep`) drift. Validation: `tests.test_ai_eval` 25 tests OK; ruff check clean. Hosted CI not observed; rpi-checks --all not run.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Critical misses fail the run | Proven earlier (ticked) | Existing tests |
| Model, prompt version, latency, reviewer outcomes reported | Proven earlier (ticked) | Existing tests |
| Model names, versions and quotas in the chosen region | Partly proven | Azure CLI 2026-11-23: gpt-4.1-nano and gpt-4.1-mini 2025-04-14, capacity and rate limits on `aif-cutover-test-rzsrg` (uksouth); IaC pins now tested against the record. Per-model quota headroom not returned by `usage list`; the production region stays with other issues |
| Frozen independent held-out split | Unproven | Needs an independent labeller |
| Human detection of seeded critical errors | Unproven | Needs authorised participants |
| Effort and cost against alternatives | Unproven | Needs people and Finance |
| Hashes, serving version, reviewer protocol | Unproven | Needs a real held-out batch and reviewers; `ca-resident-demo` serving deployment not attested |
| Actual-call authorization and consent | Unproven | Production authority, not needed for the demo |
| Real AI/SQL/Azure proof under CON-009/AC-057 | Unproven | Production build |

No criterion is newly tickable. No Azure resource was created.
