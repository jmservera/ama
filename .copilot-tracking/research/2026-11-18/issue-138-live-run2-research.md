---
title: Issue 138 live research
ms.date: 2026-11-18
---

## Scope

Refs #138. Demo, desktop only, live Azure authorised (rg ama, cap USD 700, read-only here).
Goal: prove or precisely explain each of six unticked criteria. Prior note
docs/reference/research/issue-138-live-cicd-oidc-evidence-2026-11-18.md exists; this run repeats the
checks fresh and records a new dated note. Research disposition: executed.

## Planned checks

* Workflow audit: infra-plan.yml, src-deploy.yml (OIDC, environments, what-if, image, smoke).
* gh api: variables, environments, runners, workflow runs.
* az what-if of infra/main.bicep against rg ama (read-only), az identity federated credentials.
* infra/tests/test_pipeline.py, smoke() against ca-cutover-test-demo-api.
* Secret pattern scan of tree and recent logs.

Planning Readiness: Ready.

## Findings (executed 2026-11-18, all read-only)

* Repository variables: only `GH_AW_DEFAULT_MAX_DAILY_AI_CREDITS`; secrets: only `COPILOT_GITHUB_TOKEN`. No
  `INFRA_PLAN_ENABLED`, `AZURE_*` or `DEPLOY_PARAMETERS`. Zero self-hosted runners. Environments: copilot,
  dev-plan, test-plan, pilot-plan, none with protection rules, admin bypass true. No dev/test/pilot or *-release.
* infra-plan.yml: 2509 runs, latest skipped (gate `INFRA_PLAN_ENABLED`). src-deploy.yml: zero runs.
* Six managed identities in ama: zero federated credentials each. ACR `crcutovertestrzsrg` private (public access
  disabled, Premium); repository listing denied from this host. API runs a digest-pinned image.
* what-if of infra/main.bicep (test parameters, throwaway values, apps off): Succeeded; 99 Create, 15 Modify, 81 Ignore,
  14 Unsupported; no Delete. `summarize_plan` refuses it (Unsupported). Temp parameter file removed.
* test_pipeline.py OK; `smoke()` against live API PASS; unreachable host fails as expected; /healthz 200, /api/me 401.
* Secret scan: value-shaped patterns matched only two test fixtures; neither workflow uses `secrets.`; one CI log
  (23703 lines, run 44266028749) had zero matches.
* Prior committed run (docs note 2026-11-18, same findings) preserved, not overwritten.

Planning Readiness: Ready. Outcome: criteria remain unproven for the demo; see changes record.
