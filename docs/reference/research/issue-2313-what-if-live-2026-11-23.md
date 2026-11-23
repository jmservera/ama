---
title: Issue 2313 what-if workflow and PR image build (Refs #138)
description: Per-criterion proven or unproven record for issue 2313, with the new credential-free PR image build workflow
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, base `50dc2acf88`. Refs #2313, #138 and #136. No Azure resource was created or changed, no browser was needed, no sign-in value was read, and nothing was pushed. Tier: Full by instruction (a new workflow with pinned actions), but no `src` change; the complete gate is left to the coordinator.

## Finding

`.github/workflows/infra-plan.yml` already implements the read-only what-if on pull requests that change `infra/` (a `workflow_run` of "Source projects CI", a `git diff` path check in the `changes` job, the what-if job behind `-plan` environments, summary uploaded as `what-if-<env>-<sha>`). It was left unchanged because its hash is pinned in `tools/rpi-checks.py`. The missing piece was a versioned image build that does not deploy, so `.github/workflows/infra-image-build.yml` was added with `infra/tests/test_infra_image_build.py`.

## Evidence

| Check | Result |
| --- | --- |
| `python3 -m unittest infra/tests/test_infra_image_build.py` | 3 tests OK |
| `actionlint -config-file infra/tests/actionlint.yaml` on the new workflow | no findings |
| `ruff check` and `ruff format --isolated --line-length 100 --check` on the new test | clean |
| Local run of the workflow's build and check commands for `importer` with a simulated run identity | tag `zava-forward-importer:sha-<40-hex sha>-r1-a1`; `check-container.py`: "importer: Docker controls, negative probes and compatible startup PASS"; image then removed |
| `python3 -m unittest discover -s infra/tests` | 748 run, 3 errors, 4 skipped. All three errors come from the installed `zava_forward` package in `~/.local/lib/python3.12/site-packages` lacking `AI_SUSPENDED` (stale non-editable install); unrelated to this change, not fixed |
| GitHub state | `INFRA_PLAN_ENABLED` unset; the latest `infra-plan.yml` runs on 2026-11-23 are `skipped` |

## Per-criterion record

| Criterion | Status | Basis |
| --- | --- | --- |
| Workflow runs what-if only on PRs that change infra/ and uploads the result | Proven by inspection and existing tests; not proven live | `infra-plan.yml` `changes` job and upload step; `test_privileged_pr_workflow_is_default_branch_workflow_run_only`. A live run needs the owner's `INFRA_PLAN_ENABLED`, OIDC client and self-hosted runner (#138), outside demo authority. |
| Pinned action SHAs and least permissions recorded | Proven | `workflow_errors` over `infra-plan.yml` and `src-deploy.yml`; the new test asserts SHA pins, `contents: read` and no environment, login or secrets for the new workflow. |
| Image build job tags a versioned image without deploying | Proven locally; not run on GitHub | New workflow, plus the local `importer` run above. The hosted run happens when a PR is opened (not done: no push). |
| OIDC credential setup and environment approvals stay owner actions under #138 | Proven | No change to OIDC, environments or variables; the new workflow has no `id-token`. |

## Follow-up

Add `infra-image-build.yml` to the `WORKFLOWS` and `WORKFLOW_HASHES` matrix in `tools/rpi-checks.py` under the owner's gate update, and decide whether it duplicates the `:ci` build in `src-ci.yml`.
