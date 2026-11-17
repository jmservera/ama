---
title: Issue 138 CI/CD pipeline assessment against main
ms.date: 2026-11-17
---

# Research: issue 138 CI/CD deployment pipeline (evidence only)

* Task: issue-138. Base `eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4`; fetched `origin/main` was `f5ed8c40942a73f8dff5a980beec307b2a4d094d` at 2026-11-17 22:10 UTC (assessed base kept as instructed).
* Tier: FOCUSED, record evidence only. No dispatch, Azure, OIDC or deployment action was performed.
* Research disposition: executed. Planning Readiness: Ready.

## Scope check

The change touches no workflow, infrastructure or deployment file; only evidence documents change. FULL tier is not triggered because nothing is altered in deployment behaviour.

## Measurements (read-only GitHub API and local helper, 2026-11-17)

| Probe | Result |
| --- | --- |
| Workflows `infra-plan.yml`, `src-deploy.yml` | state `active` |
| `src-deploy.yml` runs | `total_count` 0 (never dispatched) |
| `infra-plan.yml` runs | 2452 total; latest 100 completed runs all `skipped` (job guard `vars.INFRA_PLAN_ENABLED == 'true'` is unset) |
| Repository Actions variables | only `GH_AW_DEFAULT_MAX_DAILY_AI_CREDITS`; no `INFRA_PLAN_ENABLED` |
| GitHub environments | `copilot`, `dev-plan`, `test-plan`, `pilot-plan`; no `dev`, `test`, `pilot`, `*-release` |
| Environment protection | all four: `protection_rules` empty, `can_admins_bypass` true, no deployment branch policy |
| `dev-plan` variables | 0 (no `AZURE_*_CLIENT_ID`, `DEPLOY_PARAMETERS`) |
| Self-hosted runners | 0 registered |
| Branch protection / rulesets on `main` | main not protected (404); 0 rulesets |
| `pipeline.py verify-environment` with live config | `dev-plan`: "Environment requires reviewers, no self-review/bypass and branch rules" (fail-closed); `dev-release`: gh operation failed (environment absent) |
| `python3 -m unittest infra.tests.test_pipeline` | 30 tests OK offline |

## Criteria assessment

| Criterion | Status | Evidence |
| --- | --- | --- |
| C1 OIDC per environment | Unproven | Workflow wiring exists; no client-id variables, no runners, no login ever run |
| C2 what-if on infra PRs, attached | Unproven | Trigger is gated off (`INFRA_PLAN_ENABLED` unset): all sampled runs skipped, none produced an artifact |
| C3 approval per environment, same templates | Unproven | Required `dev`/`test`/`pilot`/`-release` environments absent; existing `-plan` environments have no reviewers; helper refuses as designed |
| C4 versioned image pushed and referenced | Unproven | `src-deploy.yml` has zero runs |
| C5 post-deployment checks fail the run | Unproven live | Offline fake-orchestration tests pass; no deployed run |
| C6 no secret in logs/repo | Unproven | No live run logs exist to audit; no stored secrets in definitions |

## Findings

* F1: Plan workflow is silently skipped on every run; the skip reason is an unset repository variable, which is an owner action.
* F2: Required protected environments, reviewers, variables, OIDC identities and private runners are absent. These are owner setup actions in `infra/README.md`, not code defects.
* F3: Fail-closed behaviour is confirmed against live config, which supports the safety design but not acceptance.

No code defect was reproduced, so no source fix or new regression test is warranted; the existing 30 offline tests already cover the helper behaviour measured.

## Follow-ups

1. Owner: create the protected environments, reviewers and variables, then set `INFRA_PLAN_ENABLED`.
2. Owner: register ephemeral private runners and OIDC identities.
3. Dispatch a real release only after approval; then tick criteria with evidence.
