# Issue 107 live changes

Status: complete. Tier: FOCUSED. Basis: test-only addition under src/api/tests; no production src, SQL schema, infra, workflow or dependency change.

## Files

* src/api/tests/test_assistant_restart_non_replenishment.py: `pool_state` helper, composite test `test_old_image_after_a_material_mismatch_cannot_reactivate_or_refill`, classes `MssqlAllowance` and `MssqlMaterialMismatch`.
* docs/reference/research/issue-107-live-r4-criteria-2026-11-19.md, docs/reference/README.md, docs/reference/log.md.

## Divergence

First SQLite run failed (10 subtests, `pool` is None before any spend); fixed with a None-safe `pool_state`. Recorded honestly; no other divergence.

## Validation

* SQLite: 30 tests OK, 15 skipped. Actual SQL Server 2022 (disposable container, deleted): 30 tests OK, 0 skipped.
* ruff format/check pass. mypy in src/api: 7 pre-existing opentelemetry stub errors, none in changed file.
* rpi-checks.py not run (FOCUSED; never --all).

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Independent SQL worker/race tests for material mismatches, revocation, restart; old images cannot restore approval or refill allowance | Proven on local actual SQL Server; not Azure SQL | research note above |
| Approved exercise record permits bounded proposals only; delivered-build real AI/SQL/Azure acceptance | Unproven | no approved release (OQ-017), real AI not authorised |
