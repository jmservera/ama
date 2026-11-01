# Plan: issue 144 container hosting slice (2026-11-01)

Research: [research](../../research/2026-11-01-issue-144-container-hosting-research.md). Critique: [critique](./issue-144-container-hosting-critique.md).

## Phases

* [ ] Phase 1: API scale load harness `src/api/tests/scale_load.py` (in-process API, SQL store, 60,000 fictional homes, N sessions at R req/s for D s, per-route p50/p95/p99, NFR-002 observations, cost drivers per unit of load, no inference, no production claim) and `src/api/tests/test_scale_load.py` (small fixture).
* [ ] Phase 2: restart and single-replica audit persistence test (`src/api/tests/test_restart_audit.py`): ledger entries survive store reopen, chain intact, digest still verifies.
* [ ] Phase 3: Bicep API startup probe; compiled contract test for scale rules, probes, resource limits and Single revision mode in `infra/tests/test_bicep_policy.py`.
* [ ] Phase 4: record a 60,000-home run in `docs/architecture/` evidence, rollback-by-digest procedure and criteria status in `infra/README.md`, log entry. Keep unmet items explicit.

## Out of scope

Agents queue transport, API post-back, orchestrator real job, hosted hardening (platform-blocked), Azure restore proof, any deployment.

## Validation (focused tier)

Relevant unittest modules, `ruff check`, `ruff format --check`, `mypy` for touched projects, bicep compile via the existing infra test. Focused-test evidence is retained, but this slice changes `containerapps.bicep`, so the complete local gate (`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <external-dir>`), fresh `--verify-receipt` against the current origin/main and independent exact-head assessment are required before publication. A missing prerequisite blocks publication; CI does not substitute.
