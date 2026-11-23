# Changes: issue 2313 round 2 (Refs #2313)

Status: implemented, reviewed once. Tier: Full (gate-tool edit); the complete gate is left to the coordinator.

## Files

* `tools/rpi-checks.py`: `infra-image-build.yml` added to `WORKFLOWS`, `WORKFLOW_HASHES` (sha256 of the file) and the coverage classification (`build` job).
* `tools/test_rpi_checks.py`: regression test `test_infra_image_build_workflow_is_in_matrix_and_classified`.

## Validation

`python3 -m unittest tools.test_rpi_checks`: 131 tests OK (includes drift tests now covering the new workflow). `ruff format` clean on both files; `ruff check` reports 20 findings, identical to the unmodified baseline. No Azure resource, browser or credential used; nothing pushed.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| What-if only on infra PRs and uploads result | Proven by inspection and existing tests; unproven live | `infra-plan.yml` `changes` job; `INFRA_PLAN_ENABLED` unset and OIDC is an owner action (#138) |
| Pinned SHAs and least permissions recorded | Proven | Contract test `infra/tests/test_infra_image_build.py` (merged) and the gate now hashes the workflow, so drift is detected |
| Versioned image tagged without deploying | Proven locally (prior note); unproven on GitHub (no push) | `docs/reference/research/issue-2313-what-if-live-2026-11-23.md` |
| OIDC and approvals stay owner actions | Proven | No OIDC, environment or variable change |
