---
title: Issue 108 live changes, second 2026-11-23 round
ms.date: 2026-11-23
---

Refs #108. Tier: focused (tests only under `src/agents/tests`; no runtime, permission, package or deployment change). Changed: `src/agents/tests/test_ai_eval.py` (new test), the attestation note, knowledge-base index and log. Validation: `tests.test_ai_eval` OK, ruff clean; hosted CI not observed; rpi-checks --all not run.

Refs #108. Synthetic demo, desktop only; live Azure read-only in resource group `ama`. No resource was created and no credential was read or printed. The GitHub issue text was unavailable (API rate limit), so the criteria follow [issue-108-harness-audit-live-r2-2026-11-18.md](./issue-108-harness-audit-live-r2-2026-11-18.md).

## Evidence

* `az containerapp show -g ama -n ca-resident-demo` (2026-11-23): latest ready revision `ca-resident-demo--0000028`, created 2026-11-23T12:31:09Z, active, Healthy, traffic 100.
* Image: `crcutovertestrzsrg.azurecr.io/zava-resident-demo@sha256:e6c7e755343a02efdc594aa10c2af66dd1818ea9a6ce06c806ae4ae59adf1054`.
* `ZF_DEMO_ASSISTANT_ENDPOINT` is `https://aif-cutover-test-rzsrg.openai.azure.com`; the code deployment name is `resident-mini` (`resident_demo/aoai.py`), which the [serving record](./issue-108-live-r4-2026-11-19/serving_region_record.json) lists as gpt-4.1-mini 2025-04-14, Standard, capacity 1.
* New test `test_resident_deployment_names_match_serving_record` (`src/agents/tests/test_ai_eval.py`): the code and Bicep deployment names agree and appear in the record. `tests.test_ai_eval` passes, ruff clean.

## Per-criterion result

| Criterion | Status | Limit |
| --- | --- | --- |
| Critical misses fail the run; reported fields | Proven earlier (ticked) | Offline and scripted |
| Model names, versions, quotas in the chosen region | Partly proven | Names, versions and capacity confirmed; per-model quota headroom not returned by `usage list`; production region owned by other issues |
| Serving version attestation (hashes, serving version) | Partly proven | Serving revision, image digest and deployment recorded; no signed attestation or held-out batch hashes tied to this revision |
| Frozen independent held-out split | Unproven | Needs an independent labeller |
| Human detection of seeded critical errors | Unproven | Needs people |
| Effort and cost against alternatives | Unproven | Needs measured effort and Finance |
| Call authority and payload approval | Unproven | Production authority, not needed for the demo |
| Real AI, SQL and Azure under CON-009 and AC-057 | Unproven | Restart check is drill-like; excluded |

No criterion is newly tickable.
