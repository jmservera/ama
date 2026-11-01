# Changes: issue 145 SQL pilot tier and recovery (2026-11-01)

Plan: [plan](../plans/2026-11-01-issue-145-sql-pilot-recovery-plan.md)

* `infra/modules/sql.bicep`, `infra/main.bicep`: `sqlTier`, vCores, auto-pause, backup redundancy and retention parameters; serverless-only properties set to null for provisioned (a `union()` form broke the compiled-module policy tests and was replaced).
* `infra/main*.bicepparam`: pilot example records `provisioned`; dev files record `serverless`.
* `infra/tests/test_sql_tier.py`: new contract and compile tests.
* `infra/sql-recovery-runbook.md`, `infra/README.md`, `docs/reference/log.md`: runbook, objectives undecided with owners, evidence status.

Validation: new test and Bicep policy, edge and RBAC tests pass except `test_manifest_matches_script_and_mvp_role_map` (`zava_forward` not installed in this environment; unrelated). `bicep build infra/main.bicep` clean. ruff check, ruff format --check and mypy clean for the touched Python file. Full-suite errors seen earlier were the same missing-package class plus the sql mutation tests fixed above.

Review round 1 (Copilot threads on PR 673): the compile test now builds with `az bicep` and evaluates the compiled SKU and serverless properties for both tiers, including an overridden auto-pause delay; the runbook now requires native SQL ledger digests with storage location metadata (`path`, `last_digest_block_id`, `is_current`), keeps verification blocked without them, and treats orchestrator `count`/`head` anchors as a separate check. The failing `activation` check was the daily AIC guardrail ("inspection stopped to preserve GitHub API quota", transient) and was rerun.

Review round 2: `serverlessAutoPauseDelayMustBeSupported` added to `infra/modules/guard.bicep` and wired in `infra/main.bicep`, so serverless auto-pause delays other than -1 or 15 to 10080 minutes fail before deployment; `test_bicep_policy.py` covers the boundaries (0, 14, 15, 10080, 10081, -1) for both tiers, the guard mutation list, and the evaluator gained `greaterOrEquals`/`lessOrEquals`. `test_bicep_policy` and `test_sql_tier` pass (60 tests). `gh pr checks 673` reported no checks on the branch at this time; ruff shows one pre-existing RUF100 in the touched test file, unchanged.
