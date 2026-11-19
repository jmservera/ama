# Details r5

Phase 1: in `run_live_check._select_budget`, accept a budget whose `filter.dimensions` is `ResourceId In` containing the hub resource id (case-insensitive), falling back to the name `budget-<hub>`. Tests: differently named budget with matching scope passes; budget scoped to another resource and unrelated name fails.
Phase 2: reuse the run 2 job pattern; driver outside the repo; no keys printed; cleanup verified by `az containerapp job list` and device/role readback.
Phase 3: documents only.
