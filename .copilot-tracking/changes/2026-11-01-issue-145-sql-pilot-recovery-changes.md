# Changes: issue 145 SQL pilot tier and recovery (2026-11-01)

Plan: [plan](../plans/2026-11-01-issue-145-sql-pilot-recovery-plan.md)

* `infra/modules/sql.bicep`, `infra/main.bicep`: `sqlTier`, vCores, auto-pause, backup redundancy and retention parameters; serverless-only properties set to null for provisioned (a `union()` form broke the compiled-module policy tests and was replaced).
* `infra/main*.bicepparam`: pilot example records `provisioned`; dev files record `serverless`.
* `infra/tests/test_sql_tier.py`: new contract and compile tests.
* `infra/sql-recovery-runbook.md`, `infra/README.md`, `docs/reference/log.md`: runbook, objectives undecided with owners, evidence status.

Validation: new test and Bicep policy, edge and RBAC tests pass except `test_manifest_matches_script_and_mvp_role_map` (`zava_forward` not installed in this environment; unrelated). `bicep build infra/main.bicep` clean. ruff check, ruff format --check and mypy clean for the touched Python file. Full-suite errors seen earlier were the same missing-package class plus the sql mutation tests fixed above.
