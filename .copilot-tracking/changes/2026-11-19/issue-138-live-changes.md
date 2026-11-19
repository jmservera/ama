# Changes record, issue 138 (Refs #138)

Tier: FOCUSED. Basis: adds a read-only verifier operation; no deployment, SQL, permission, secret or gate-semantics change; workflows untouched.

Files: infra/scripts/pipeline.py (verify_federation + CLI), infra/tests/test_pipeline.py (1 test), infra/README.md, docs/reference/README.md, docs/reference/log.md, docs/reference/research/issue-138-live-r6-2026-11-19.md (+ evidence dir).

Validation: `cd infra && PYTHONPATH=scripts python3 -m unittest tests.test_pipeline` 34 OK; mutation (ignore subject) fails the new test; `ruff format --isolated --line-length 100 --check` clean. mypy not applicable (no src/<project> change). Repo-config `ruff check` reports only pre-existing SIM/EXE001 patterns in this file; none new beyond the existing nested-with style.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| C1 OIDC scoped per environment | Unproven (verifier added; live 0 federated credentials) |
| C2 what-if on infra PRs attached | Unproven (0 runners, gate unset) |
| C3 approval per environment | Unproven (0 protection rules, admin bypass) |
| C4 versioned image pushed and referenced | Unproven (no pipeline run) |
| C5 post-deployment checks fail run | Unproven (no pipeline run; unit tests only) |
| C6 no secret in logs or repo | Unproven (no live log audit) |
