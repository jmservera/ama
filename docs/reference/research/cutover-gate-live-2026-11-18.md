---
title: Cut-over gate demo proof, live run 2026-11-18 (issue 201)
description: Per-criterion proven and unproven results for the three unticked issue 201 acceptance criteria, measured with repo checks and read-only Azure CLI on the synthetic demo
ms.date: 2026-11-18
---

Refs #201. Scope: the synthetic demo only, desktop only, resource group `ama`. Owner decisions of 2026-11-18 apply: live Azure is authorised (cap USD 700, no drills, no Key Vault rotation, no production change); billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed. Only read commands ran. Nothing was created in Azure, so nothing needed deleting. No credential was read or printed. Repository head: `e173f50d9`.

## Result

| # | Unticked criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | CI, Docker, Bicep image paths and scripts repointed; a build from `src/` is deployed and healthy | Partly proven; build provenance unproven | Repointing proven by repo checks; healthy deployment proven live; that the running digest was built from `src/` cannot be shown here |
| 2 | Private `mvp/data/` relocated and backed up outside git | Not provable by an agent; deferred | Owner-only attestation by design |
| 3 | Owner signs off in this issue | Not provable; deferred | Human decision |

Production-only items stay deferred under #1905 to #1908.

## 1. Repointing and deployed health

Repointing (repo checks at `e173f50d9`):

* `git ls-files | grep -E '^(mvp|prototype)/'` returns 0 files and neither directory exists in the worktree.
* `.github/workflows/mvp-ci.yml` builds with `docker build -f src/api/Dockerfile ... src`; `src-deploy.yml` builds `src/$PROJECT/Dockerfile` with context `src`. `src/api/Dockerfile` copies only `core/`, `agents/` and `api/` sources from the `src` context.
* `cd infra && python3 -m unittest tests.test_pipeline`: Ran 32 tests, OK (pipeline, deploy and image-release shape checks).
* The workflow filenames `mvp-ci.yml` and `mvp-validation.yml` keep their names by owner rule (checks keep names until a deliberate branch-protection update); remaining `mvp/data` mentions in workflows are exclusion guards (`test -z "$(git ls-files mvp/data ...)"`), not build inputs.

Deployed and healthy (read-only Azure CLI, 2026-11-18):

* `ca-cutover-test-demo-api`: provisioning `Succeeded`, latest and ready revision `ca-cutover-test-demo-api--0000031` (created 2026-11-17T19:42:06Z), active, health `Healthy`, running, 1 replica, traffic 100.
* Image `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`.
* `ca-resident-demo`: provisioning `Succeeded`, image `zava-resident-demo@sha256:65481780...`.
* `GET /healthz` on the public FQDN returns 200 with body `ok`; `/health` and `/api/health` return 401 (authenticated paths). The Playwright proof that signed-in pages render from this revision is in [deployed-parity-live-2026-11-18.md](deployed-parity-live-2026-11-18.md).

Unproven: that this digest was built from `src/`. The registry `crcutovertestrzsrg` has public network access `Disabled`, so tags, manifests and image labels cannot be read from here; the container app sets no build or commit variable; the `src-deploy.yml` workflow has no recorded runs (`gh run list` returned an empty list), so the digest cannot be tied to a workflow run. The image name and the only Dockerfile in the repository (`src/api/Dockerfile`) are circumstantial evidence only. Closing this needs a build-provenance label or run record, or reading the registry from a permitted network.

## 2. Private `mvp/data/`

The dataset is git-ignored, real-address data that no agent may read. The worktree has no `mvp/` and the default `ZF_DATA` path `~/.zava-forward/data` does not exist on this host, so there is nothing an agent can inspect. [cutover-evidence-pack.md](../../architecture/cutover-evidence-pack.md) already records this row as owner-only and UNMET. The demo runs on synthetic data, so this is not a demo blocker; it remains an owner attestation.

## 3. Sign-off

Owner action only; no agent evidence applies. Open decision in the issue (minimum soak period) is unresolved.

## Adverse finding

`python3 tools/check-legacy-references.py` reports 11 violations (retired path without archive tag `v0.21.0`) in `tools/test_epic_legacy_path_retirement.py`, `tools/test_epic_parity_matrix_old_paths.py` and `tools/test_private_mvp_data_exclusion.py`, and `tools.test_check_legacy_references.ReferenceTests.test_repository_has_no_violations` fails (18 tests, 1 failure; the other 17 pass). Those three test files, added by #1610 and #1879, name `mvp/` and `prototype/` paths without the archive tag. No workflow or `rpi-checks.py` invokes this checker, so CI does not catch it. Left unfixed here (outside this evidence-only scope); recommended follow-up: add the tag or an allow-list entry.
