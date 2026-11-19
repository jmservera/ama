# Research: issue 138, eighth demo run (2026-11-19)

Refs #138. Read-only recheck against the r7 baseline (docs/reference/research/issue-138-live-r7-2026-11-19.md).

* GitHub: variables list only GH_AW_DEFAULT_MAX_DAILY_AI_CREDITS (no AZURE_* variable); secret name COPILOT_GITHUB_TOKEN only; environments copilot, dev-plan, pilot-plan, test-plan with 0 protection rules and admin bypass; 0 runners; src-deploy.yml has 0 runs.
* Azure (ama): six user-assigned identities, 0 federated credentials each.
* Code: pipeline.smoke already fails on unhealthy API or successful unauthenticated access, with unit tests (infra/tests/test_pipeline.py); verify-federation added in r6.
* Disposition: no criterion is buildable or provable for the demo; each needs owner Entra/GitHub settings, a runner or a pushed workflow run.
