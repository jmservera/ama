---
title: Issue 108 live changes, third 2026-11-23 round
ms.date: 2026-11-23
---

Refs #108. Tier: focused (test and research data only; no runtime, permission, package or deployment change). Synthetic demo, desktop only; Azure used read-only (resource group `ama`); no resource created; no credential read or printed. Hosted CI not observed; rpi-checks --all not run.

Changed: `serving_region_record.json` (resident-mini capacity 10, 10 rpm, 10000 tpm, `live_observed_on`), `src/agents/tests/test_ai_eval.py` (new `test_recorded_rate_limits_follow_capacity`), the attestation note, index and log. Validation: `tests.test_ai_eval` 27 tests OK; ruff clean.

## Per-criterion result

| Criterion | Status | Limit |
| --- | --- | --- |
| Critical misses fail the run (ticked) | Proven earlier | Offline, scripted |
| Model, prompt version, latency, reviewer outcomes reported (ticked) | Proven earlier | Offline, scripted |
| Model names, versions and quotas confirmed in the chosen region | Partly proven | Names, versions, capacity and rate limits confirmed live (uksouth); `usage list` returns only GlobalBatch rows, so Standard TPM headroom is unconfirmed |
| Benefit not claimed without calibration (ticked) | Proven earlier | Unchanged |
| Frozen independent held-out split | Unproven | Needs an independent labeller |
| Human detection of seeded critical errors | Unproven | Needs people |
| Effort and cost comparison, Finance validation | Unproven | Needs measured effort and Finance |
| Hashes, split, actual serving version, usage | Partly proven | Serving deployment and limits recorded; no held-out batch hashes |
| Call/token authorisation, payload approval | Unproven | Production authority, not needed for the demo |
| Real AI, SQL, Azure proof (CON-009, AC-057) | Unproven | Restart check is drill-like; excluded |

No criterion is newly tickable.
