---
title: CI/CD pipeline audit and what-if evidence for issue 138, second demo run
description: Fresh read-only audit of the deployment workflows, repository settings and the live ama resource group for issue 138, with a per-criterion proven or unproven record
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

Refs #138. This is the second dated run on 2026-11-18 and repeats the checks of the
[first run](./issue-138-live-cicd-oidc-evidence-2026-11-18.md) from a clean worktree so the
result does not rest on one session. It is the synthetic demo, desktop only. The owner
authorised live Azure use (resource group `ama`, cap USD 700, no drills, no Key Vault
rotation, no production changes). No workflow, source file, GitHub setting or Azure resource
was changed; every Azure command was `show`, `list` or `what-if`, and the temporary parameter
file was deleted. Subscription and tenant identifiers are omitted. Tier: focused
(documentation only).

## Findings

* Repository variables: only `GH_AW_DEFAULT_MAX_DAILY_AI_CREDITS`. Secrets: only
  `COPILOT_GITHUB_TOKEN`. None of `INFRA_PLAN_ENABLED`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`,
  `AZURE_PLAN_CLIENT_ID`, `AZURE_PUBLISH_CLIENT_ID`, `AZURE_DEPLOY_CLIENT_ID`,
  `AZURE_REGISTRY_NAME` or `DEPLOY_PARAMETERS` exist, so both workflows cannot authenticate.
* Self-hosted runners: 0. The `what-if` job and the release and deploy jobs request the labels
  `ama-private-plan`, `ama-private-release` and `ama-private-deploy`.
* Environments: `copilot`, `dev-plan`, `test-plan`, `pilot-plan`; none has a protection rule and
  administrators can bypass. The `dev`, `test`, `pilot` and `*-release` environments that
  `src-deploy.yml` targets do not exist.
* Runs: `infra-plan.yml` has 2509 recorded runs and the latest were `skipped` (its `changes` job
  needs `vars.INFRA_PLAN_ENABLED == 'true'`). `src-deploy.yml`, which is `workflow_dispatch` only, has 0 runs.
* Workflow wiring (static): both workflows use `permissions: id-token: write` with `azure/login`
  and per-job client-id variables, no `secrets.*` context, per-environment `environment:` keys, and
  `upload-artifact` for the what-if summary. Wiring is not federation.
* Federated credentials: each of the six user-assigned managed identities in `ama` has 0.
  App-registration credentials were not read (the first run recorded "Insufficient privileges").
* Registry: `crcutovertestrzsrg` (Premium, public access disabled) refused repository listing from
  this host. `ca-cutover-test-demo-api` runs a digest-pinned image from it; no workflow run
  produced that image.
* What-if: `az deployment group what-if -g ama` of the real `infra/main.bicep` with the `test`
  parameter file (throwaway valid values, applications off) returned `Succeeded`: 99 Create, 15
  Modify, 81 Ignore, 14 Unsupported, 0 Delete. The template names resources `*-forward-test-*`
  while the demo group holds `*-cutover-test-*`, so the pipeline would not update the demo in
  place. `summarize_plan` refuses this plan because of the 14 Unsupported entries.
* Post-deployment checks: `pipeline.smoke()` passed against `ca-cutover-test-demo-api` ("health and
  all three authentication-denial checks passed") and failed against an unreachable host with
  "expected HTTP 200". Direct probes: `/healthz` 200, anonymous `/api/me` 401.
  `infra/tests/test_pipeline.py` passed.
* Secret audit: value-shaped patterns (account and shared-access keys, SAS signatures, private-key
  headers, GitHub tokens) matched only two test fixtures in `src/`. Neither deploy workflow uses a
  secrets context. The full log of `Source projects CI` run 44266028749 (23703 lines) had 0 matches
  for the same patterns plus JWT shapes.

## Acceptance criteria

| Criterion | Status | Evidence and reason |
| --- | --- | --- |
| OIDC federated credentials scoped per environment | Unproven | Workflow wiring present; no client-id variables, no environment configured, 0 federated credentials on the identities, app registrations unreadable. Proof needs repository-administrator settings and an Entra app registration with per-environment subjects, outside the demo scope. |
| `what-if` on PRs that change `infra/`, result attached | Partly proven (mechanism) | Live what-if succeeded. The PR job has never run (`INFRA_PLAN_ENABLED` unset, runs skipped, no runner), so the attached step summary and artifact are unobserved. |
| Approval per environment, same templates and parameter set | Unproven | Gate code and unit tests exist; no environment has required reviewers and `src-deploy.yml` has 0 runs. |
| Versioned image built, pushed and referenced | Unproven | Demo uses a digest-pinned image, but no pipeline run built or pushed it; registry tags not listable here. |
| Post-deployment checks run automatically and fail on unhealthy or unauthenticated success | Partly proven (check logic, live target) | `smoke()` passes live and fails on an unreachable host; automatic execution inside a deployment run is unobserved. |
| No secret value in workflow logs or repository | Partly proven | Tree and one CI log are clean for the tested patterns; one log and one pattern set do not establish absence across all runs. |

No criterion can be ticked from this evidence, and the issue stays open.

## Owner actions that would unblock proof

* Set `INFRA_PLAN_ENABLED`, the six `AZURE_*` variables and `DEPLOY_PARAMETERS`; register a private
  runner; create the `dev`, `test`, `pilot` and `*-release` environments with reviewers and no
  admin bypass; create per-environment federated credentials. Workflow edits would be FULL tier.
* Decide whether the demo group is parameterised to match the `cutover-test` naming before any
  pipeline deployment.

## Reproduction

`gh api repos/jmservera/ama/{actions/variables,actions/secrets,actions/runners,environments}`;
`gh run list -w infra-plan.yml`; `az identity federated-credential list -g ama --identity-name <name>`;
`az acr list -g ama`; `az deployment group what-if -g ama --template-file infra/main.bicep --parameters @<temp> --mode Incremental`
(parameters built with `pipeline.parameters`, temp file deleted);
`python3 -m unittest discover -s infra/tests -p test_pipeline.py`; `pipeline.smoke` against the API FQDN;
`git grep -nIE` value-shaped secret patterns; `gh run view <id> --log` scanned locally and discarded.
