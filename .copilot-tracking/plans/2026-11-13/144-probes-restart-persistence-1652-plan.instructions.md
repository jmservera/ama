---
applyTo: ".copilot-tracking/changes/2026-11-13/144-probes-restart-persistence-1652-changes.md"
---

# Plan: 144 probes and restart persistence (Focused tier)

Research: [research](../../research/2026-11-13/144-probes-restart-persistence-1652-research.md). Details: [details](../../details/2026-11-13/144-probes-restart-persistence-1652-details.md).

* [ ] Phase 1: infra contract test that `agents` has no probe (platform limit) and keeps queue scale, limits and Single mode.
* [ ] Phase 2: agents test tying `HEARTBEAT_MAX_AGE_SECONDS` to loop cadence and the 40 s task bound.
* [ ] Phase 3: agents restart test, abandoned lease redelivered to a fresh worker exactly once.
* [ ] Phase 4: infra README status row update; no overclaim.
* [ ] Phase 5: validation (contract, bicep policy, az bicep build, agents tests, ruff, mypy), review, commit.
