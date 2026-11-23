# Issue 2313 research: read-only what-if on infra pull requests

Date: 2026-11-23. Head `50dc2acf88`. Disposition: executed. Planning Readiness: Ready.

## Findings

* `.github/workflows/infra-plan.yml` already runs `az deployment group what-if` (via `infra/scripts/pipeline.py plan`) for PRs that change `infra/`. It triggers on `workflow_run` of "Source projects CI", loads from the default branch, diffs `infra/` between base and head, and uploads `what-if-<env>-<sha>` (7 days). Actions are pinned by SHA; top-level permissions are `contents: read`; only the what-if job adds `id-token: write` and `actions: read`, behind a `-plan` environment, a self-hosted runner and `verify-environment` before `azure/login`.
* `infra/tests/test_pipeline.py` already asserts structure, pinning and the workflow_run-only trigger for it. Its hash is pinned in `tools/rpi-checks.py`, so editing it would change the gate matrix; it is left unchanged.
* `src-deploy.yml` builds images only on `workflow_dispatch` from main and tags them `sha-<sha>-r<run>-a<attempt>` at publish. There is no PR-time versioned image build that stays out of the deploy path. `src-ci.yml` builds `zava-forward-<project>:ci` (not versioned).
* Live GitHub state: `INFRA_PLAN_ENABLED` is unset, so every infra-plan run is `skipped` (latest three runs 2026-11-23). The OIDC client, environment reviewers and the self-hosted runner are owner actions under #138.

## Gap and decision

Criteria 1, 2 and 4 are met by existing files (recorded, not rebuilt). Criterion 3 lacks a job. Add `.github/workflows/infra-image-build.yml`: `pull_request` on `infra/**` and `src/**` paths, `contents: read` only, no Azure login, no registry push, matrix over the four projects, `docker build` with `ZF_BUILD_COMMIT` and a version tag `sha-<head sha>-r<run>-a<attempt>` (same scheme as `release_tag()`), then `docker image inspect` and `src/check-container.py`. A unit test in `infra/tests/` asserts triggers, permissions, pinning, no deploy/push/login and the tag format.

Tier: focused for the new file, but a new workflow touches pinned actions, so it is classified Full by the instructions; the complete gate is the coordinator's responsibility. No `src` change.
