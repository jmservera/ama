---
title: Cut-over gate demo proof, second live run 2026-11-18 (issue 201)
description: Second per-criterion proven and unproven table for the three unticked issue 201 acceptance criteria, adding in-container proof that the running image holds only src-layout distributions
ms.date: 2026-11-18
---

Refs #201. Second run after [cutover-gate-live-2026-11-18.md](cutover-gate-live-2026-11-18.md), which stays as the first record. Scope: synthetic demo, desktop only, resource group `ama`. Owner decisions of 2026-11-18 apply (live Azure authorised, cap USD 700, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed). Only read commands and one read-only in-container listing ran. Nothing was created in Azure, so nothing needed deleting. No credential was read or printed. Repository head: `8a21156d9`.

## Result

| # | Unticked criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | CI, Docker, Bicep image paths and scripts repointed; a build from `src/` is deployed and healthy | Proven for the demo, with one residual gap (no build-run record) | Repointing by repo checks; health live; new in-container proof that the running image contains the three `src` distributions and no `mvp` tree |
| 2 | Private `mvp/data/` relocated and backed up outside git | Not provable by an agent | Owner-only attestation; the demo uses synthetic data |
| 3 | Owner signs off in this issue | Not provable | Human decision; minimum soak period still open |

Production-only items stay deferred under #1905 to #1908.

## 1. Criterion 1

Repointing (repo checks at `8a21156d9`):

* `git ls-files | grep -cE '^(mvp|prototype)/'` returns 0; neither directory exists.
* `mvp-ci.yml:48` runs `docker build -f src/api/Dockerfile -t zavaforward-mvp:ci src`; `src-deploy.yml:66` runs `docker build -f "src/$PROJECT/Dockerfile" ... src`.
* `cd infra && python3 -m unittest tests.test_pipeline` passes (the post-deployment health and three authentication-denial checks report passed).

Deployed and healthy (read-only Azure CLI and Playwright, 2026-11-18 about 16:45Z):

* `ca-cutover-test-demo-api`: provisioning `Succeeded`; the only active revision is `ca-cutover-test-demo-api--0000032` (created 2026-11-18T16:20:23Z), health `Healthy`, 1 replica, traffic 100.
* Image digest `sha256:5368f4e4...e5fb` is unchanged from revision 0000031 of the first run, so the new revision reuses the same image.
* `curl` and Playwright on `/healthz` return 200 (`ok`).

New proof of image contents (one `az containerapp exec` listing of the running container, no files changed):

* `ls /app` returns only `evals`; `pip list` shows `zava-forward-agents 0.1.0`, `zava-forward-api 0.1.0` and `zava-forward-core 0.1.0`; `ls /app/mvp` fails with no such file.
* `src/api/Dockerfile` builds exactly those three wheels from `src/core`, `src/agents` and `src/api` and copies `agents/evals/ai_priority_golden.json` to `/app/evals`. The three distribution names match `name` in each `src/*/pyproject.toml`. The legacy tree had no such distributions and is absent from the image.

Residual gap: no build-run record ties the digest to a workflow run. The registry `[registry]` has public network access `Disabled` (tags, manifests and labels are unreadable); all 10 ACR task runs are `Failed`; the registry diagnostics workspace `log-cutover-test` rejects queries from this host (network perimeter); `src-deploy.yml` has no recorded runs. For the demo the image content is accepted as sufficient evidence that the deployed build comes from `src/`; a run record would need a permitted network or a provenance label in a later build.

## 2. Criterion 2

The dataset is git-ignored, real-address data that no agent may read. This host has no `mvp/` and no `~/.zava-forward/data`, so there is nothing to inspect. [cutover-evidence-pack.md](../../architecture/cutover-evidence-pack.md) records the row as owner-only and unmet.

## 3. Criterion 3

Owner action only. The open decision in the issue, a minimum soak period on the `src/` build, is unresolved.

## Adverse finding (carried and grown)

`python3 tools/check-legacy-references.py` now reports 45 reference violations (11 in the first run), 0 link violations. The earlier three test files still fail, and the increase comes from dated live-evidence notes that name retired paths or package names without the archive tag `v0.21.0`. The checker is not run by any workflow or by `rpi-checks.py`. Left unfixed because this is an evidence-only task; follow-up: add the tag or an allow-list for dated evidence notes.
