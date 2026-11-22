---
title: Issue 2191 half of homes fresh, plan (2026-11-22)
---

# Plan: re-prove that at least half of 443 homes show fresh simulated readings

* [ ] Phase 1: Measure live coverage with a throwaway read-only sampler job (30 minutes, 15 samples, 2 minute gap) after the S3 change of 13:51 UTC.
* [ ] Phase 2: Read back settings (SQL tier, simulator and receiver env and schedules, consent mix) without changing them.
* [ ] Phase 3: Delete the sampler; write the dated note under `docs/reference/research`, update the index and log.
* [ ] Phase 4: Run the focused checks (link review, git diff); no source edit, so no code tier.

Decision: no further live change unless the series falls below 222 homes (50 percent). Rollback of any change: `az sql db update ... --service-objective S0`.
