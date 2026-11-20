# Plan: issue 2061 single external demo environment (2026-11-20)

Research: ../research/2026-11-20-issue-2061-live-research.md. Details: ../details/2026-11-20-issue-2061-live-details.md. Critique: 2026-11-20-issue-2061-live-critique.md.
Tier: FULL for any `infra/` change (stated by owner and issue). The complete local gate (`rpi-checks.py --all`) is forbidden by the coordinator for this run, so it is reported as not run. No push, no deploy.

* [ ] Phase 1: `demoSingleEnvironment` parameter, guards and internal identity in `infra/main.bicep`, `modules/identity.bicep`, `modules/containerapps.bicep`.
* [ ] Phase 2: Role assignments for the internal identity (storage, registry), SQL grants script, `role-assignments.json`, tests.
* [ ] Phase 3: ADR 0005-style decision record, teardown and migration runbook, README, parameter example.
* [ ] Phase 4: Validation (bicep build, infra tests, ruff), live read-only evidence note, changes record with per-criterion table.
