# Changes: issue 2313 what-if upload contract (Refs #2313)

Status: implemented, reviewed once. Tier: focused (test only, no src or workflow edit).

## Files

* `infra/tests/test_infra_image_build.py`: add `InfraPlanWorkflowContractTests` (what-if gated on infra path check, one SHA-pinned upload of `what-if-summary.json`, `if-no-files-found: error`, runs after failure, `id-token` only on the what-if job, no apply, deploy, push or secrets; plus a mutation test proving the checker fails when the upload is removed).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| What-if only on infra PRs and uploads result | Proven statically by new test plus existing path-filter test; live run unproven (`INFRA_PLAN_ENABLED` unset, OIDC owner action under #138) |
| Pinned SHAs and least permissions recorded | Proven (new and existing tests) |
| Versioned image tagged without deploying | Proven locally earlier (existing test, importer build); GitHub run unproven (no push) |
| OIDC credential setup and environment approvals stay owner actions | Owner-only; not changed, no Azure changes made |

## Validation

`python3 -m unittest test_infra_image_build` in `infra/tests`: 5 OK. ruff check and format clean. Complete gate not run (coordinator).
