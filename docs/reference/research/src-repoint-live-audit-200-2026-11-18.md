---
title: Repoint to src audit and live image evidence (Refs #200)
description: Per-criterion audit of issue 200 on main, with local image proof and read-only checks of the demo Container App, run 2026-11-18
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Owner decision 2026-11-18 authorises live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). No source code changed, so the focused tier applies. No image was pushed and no resource was created.

## Criterion status

Criteria 1, 4, 5, 6 and 7 were already ticked in the issue and were not re-audited beyond the checks below. Criteria 2 and 3 were unticked.

| Criterion | Status | Evidence |
| --- | --- | --- |
| 2. Path filters, test commands, Docker context and requirements path point to `src/`; names deliberate | Proven | See "Criterion 2" |
| 3. Image from `src/` keeps non-root, no-data, read-only behaviour; new tag deployed and verified; historical revisions keep tags | Proven in part: behaviour and verification proven, "deploy a new tag" not performed | See "Criterion 3" |

## Criterion 2

Commands run in the worktree at `6cbc88885`:

* `.github/workflows/src-ci.yml` line 5 path filter: `src/**`, `infra/**`, tools and the three legacy-named workflow files. Test commands run per project from `src/<project>` (`pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`).
* Docker: `docker build -f src/${{ matrix.project }}/Dockerfile ... src` in `src-ci.yml` and `src-deploy.yml`; the build context is `src`. The requirements path is `src/api/requirements.txt` (`pip install --require-hashes -r src/api/requirements.txt`).
* `mvp-ci.yml` (name `Source CI`) and `mvp-validation.yml` (name `Source validation`) remain as `workflow_dispatch` only and use `src/` commands. Only the file names keep the legacy prefix, so required-check names are not silently dropped. `prototype-validation.yml` was retired with `prototype/` in commit `a7e300465` (#295).
* `git ls-files .github/workflows | grep -i proto` returned nothing; no `mvp/` or `prototype/` directory exists.
* The "refuse committed working data" step covers `mvp/data` and `src/**/data/**`.

Residual: the owner decision on whether to keep the old workflow file names for branch protection is still open in the issue. The current state keeps them, which preserves continuity.

## Criterion 3

Local proof, 2026-11-18, Docker 29.9.0:

* `docker build -q -f src/api/Dockerfile -t zava-forward-api:issue200 src` succeeded (65 s).
* `python3 src/check-container.py api zava-forward-api:issue200` printed `api: Docker controls, negative probes and compatible startup PASS`. This is the same non-root (uid 10001), no-data, read-only root file system, capability-drop contract that CI runs. The local image was removed afterwards.

Live read-only proof (Azure CLI, existing login):

* `ca-cutover-test-demo-api` latest revision `ca-cutover-test-demo-api--0000031`, created 2026-11-17T19:42:06Z, active, traffic 100, health `Healthy`, running state `Running`.
* Image: `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`, a digest of the repository built from `src/api/Dockerfile`. The container has `command` and `args` null, so it runs the image `CMD ["python", "-m", "zava_forward.api"]`, not the legacy `zavaforward_mvp` module.
* Historical inactive revisions keep their own images: `--k810` is `.../zava-forward-api:891-1022`; `--m691-b6242b9` is `.../zava-forward-api@sha256:ee38b306...`.
* Unauthenticated `GET /healthz` on `ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io` returned HTTP 200.
* An earlier push of a `src`-built tag (`4d56cf609`, revision `--0000024`) is recorded in `docs/reference/log.md` and `infra/README.md`.

Not proven: a fresh tag pushed and rolled out inside this task. Pushing needs the owner-allowed short public window on the private registry (the tag listing via the CLI returned no data because public access is disabled), which is a security-posture change outside the demo authorisation. The existing revision shows the intended end state, so the criterion is left for the owner to tick rather than ticked here.

## Unmet or open

* Criterion 3, "a new tag is deployed": evidence of a previously deployed `src` image only.
* Owner decision on branch-protection workflow names stays open.
