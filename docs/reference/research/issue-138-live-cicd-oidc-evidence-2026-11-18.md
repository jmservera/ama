---
title: CI/CD pipeline OIDC and what-if live evidence for issue 138 (demo)
description: Per-criterion record of read-only checks on 2026-11-18 against the GitHub repository settings and the live Azure demo resource group for issue 138
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 138
  - OIDC
  - what-if
  - GitHub Actions
  - deployment approval
---

## Scope and boundaries

Refs #138. The owner authorised live Azure use for the synthetic demo on 2026-11-18
(resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production
changes). This run changed no workflow, source file, GitHub setting or Azure resource.
Every Azure command was read-only (`what-if`, `show`, `list`), and the two HTTP probes
called the demo API anonymously. Subscription and tenant identifiers are omitted.
Production-only items stay deferred. Workflow and permission edits would be the FULL tier;
none were made, so this record is documentation-only (focused tier).

## Findings

* The two workflows exist and are active in GitHub: `Infrastructure PR what-if`
  (`.github/workflows/infra-plan.yml`) and `Source image release and deployment`
  (`.github/workflows/src-deploy.yml`).
* `infra-plan.yml` has recorded 2509 runs, and the five most recent (2026-11-18) all ended `skipped`.
  Its `changes` job requires the repository variable `INFRA_PLAN_ENABLED == 'true'`.
  The repository defines one variable (`GH_AW_DEFAULT_MAX_DAILY_AI_CREDITS`) and one secret
  (`COPILOT_GITHUB_TOKEN`). `INFRA_PLAN_ENABLED`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`,
  `AZURE_PLAN_CLIENT_ID`, `AZURE_PUBLISH_CLIENT_ID`, `AZURE_DEPLOY_CLIENT_ID`,
  `AZURE_REGISTRY_NAME` and `DEPLOY_PARAMETERS` are not defined.
* `src-deploy.yml` has no runs. The `what-if` and `publish` jobs use self-hosted runner labels
  (`ama-private-plan`, `ama-private-release`, `ama-private-deploy`); the repository lists no
  self-hosted runner.
* GitHub environments present: `copilot`, `dev-plan`, `test-plan`, `pilot-plan`. None has a
  protection rule, and `dev-plan` allows administrator bypass. The `dev`, `test`, `pilot` and
  `*-release` environments that `src-deploy.yml` targets do not exist.
* Fail-closed gate demonstrated live: `verify_environment` from `infra/scripts/pipeline.py`,
  run against the real repository, refused `dev-plan` ("Environment requires reviewers, no
  self-review/bypass and branch rules") and refused `dev-release` and `dev` (no environment).
* The Entra application listing returned "Insufficient privileges", so federated credentials on
  app registrations could not be read. The six user-assigned managed identities in `ama` each
  have zero federated credentials.
* A read-only `az deployment group what-if` of the real `infra/main.bicep` with the `test`
  parameter file (placeholders replaced by throwaway syntactically valid values, applications
  off) returned `status: Succeeded` in about 24 seconds: 99 Create, 15 Modify, 84 Ignore,
  14 Unsupported, no Delete. The template names resources `*-forward-test-*`, whereas the demo
  group holds `*-cutover-test-*`, so the demo is not an environment this pipeline would update in
  place. The pipeline summariser `summarize_plan` refused this plan because of the 14 Unsupported
  role-assignment entries (the pipeline treats Unsupported as a failure). Whether those entries
  would resolve against an initialised environment is a hypothesis, not tested here.
* Post-deployment checks: the repository `smoke()` function (health 200; anonymous, malformed
  bearer and forged principal each 401; sign-in redirect 302 in browser mode) passed against
  `ca-cutover-test-demo-api` in both modes. A negative control against an unreachable host failed
  with "Post-deployment health check failed; expected HTTP 200". Direct `curl`: `/healthz` 200,
  `/api/me` 401. `infra/tests/test_pipeline.py` ran 32 tests, all OK, including
  `test_wrong_health_and_any_unauthenticated_success_or_redirect_fail` and
  `test_approval_configuration_is_fail_closed`.
* Image: `ca-cutover-test-demo-api` runs a digest-pinned reference in the demo registry
  (`crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:5368f4...`). The registry is private,
  so tags were not listable from this host, and no workflow run produced this image.
* Secret audit: `git grep` of the tracked tree for key, SAS, private-key and token patterns
  matched only documentation text and test fixtures that describe such patterns. The deploy and
  plan workflows reference no `secrets.*` context. A full log of one recent `Source projects CI` run
  (23703 lines) contained zero matches for the same patterns. No dedicated scanner (gitleaks,
  trufflehog) is installed here.

## Acceptance criteria

| Criterion | Status | Evidence and reason |
| --- | --- | --- |
| Workflow authenticates with OIDC federated credentials scoped per environment | Unproven | Workflow definitions use `id-token: write` and `azure/login` with client-id variables, but none of the client-id variables exist, no environment is configured, no federated credential is readable (Entra privileges) and none exists on the managed identities. Proving it needs repository-admin settings and an Entra app registration with per-environment subjects, which the demo brief does not authorise. |
| `what-if` runs on PRs that change `infra/` and its result is attached | Partly proven (mechanism only) | Live what-if of the real template against `ama` succeeded. The PR-triggered job has never executed (`INFRA_PLAN_ENABLED` unset, runs skipped, no self-hosted runner), so the attachment (step summary and `what-if-*` artifact) is unobserved. |
| Deployment to each environment requires approval and uses the same templates and environment parameter set | Unproven | Gate code refuses unprotected environments live and unit tests pass, but no environment has required reviewers and `src-deploy.yml` has never run. |
| Versioned image is built, pushed and referenced by the deployment | Unproven | The demo app uses a digest-pinned registry image, yet no workflow run built or pushed it and the registry tags are not listable from here. |
| Post-deployment checks run automatically and fail on an unhealthy API or successful unauthenticated access | Partly proven (check logic and live target) | `smoke()` passed against the live demo API and failed on an unreachable host; unit tests cover failing cases. Automatic execution inside a deployment run is unobserved. |
| No secret value appears in workflow logs or the repository | Partly proven | Pattern scan of the tree and one CI log found nothing; the sample is one run and one pattern set, so absence across all logs is not established. |

## Next actions (owner or later work)

* Set `INFRA_PLAN_ENABLED`, the OIDC client-id and subscription variables, the release and
  deploy environments with required reviewers, and a private runner, then run the workflow
  once from `main` (repository-administrator and Entra work; FULL tier for workflow edits).
* Decide whether the demo group should be renamed or parameterised so the pipeline's
  environment naming matches `cutover-test` before any deployment through it.

## Reproduction

Commands used (outputs summarised above, none contained secrets): `gh api repos/jmservera/ama/{actions/variables,actions/secrets,environments,actions/workflows}`;
`gh run list -w infra-plan.yml` and `-w src-deploy.yml`; `az deployment group what-if -g ama --template-file infra/main.bicep --parameters @<temp file> --mode Incremental`
(temporary parameter file deleted afterwards); `python3 -m unittest discover -s infra/tests -p test_pipeline.py`;
`pipeline.verify_environment` and `pipeline.smoke` imported from `infra/scripts/pipeline.py`.
