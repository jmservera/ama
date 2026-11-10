# Research: #148 current-source local image and dry-run proof (2026-11-10)

Task `issue-148-current-image-proof-1110`; worktree branch `test/demo-current-image-proof-148-1110`; Research disposition `executed`; Planning Readiness `Ready`.

## Scope and authority

* Source-unchanged local validation of #148 criterion 4 residue. No source, test, config or documentation fix is authorised in this lane. The historical source-correction budget (1 of 5 used, four left) is neither spent nor reset by it.
* Exact source: `64c3f9191a2ffa97ef2dc07245422333ad4d6585` (after-care main). It contains the merged four-image wiring (`WORKLOAD_IMAGES` in `rebuild_azure.py`).
* Out of scope and not claimed: a whole Azure rebuild or teardown, an empty Azure inventory, images deployed, registry push, security or production acceptance, human approval, #132, #144, unmerged #109 behaviour. Docker is not Azure from-empty acceptance. #148 stays open.

## Issue state (read 2026-11-10 with `gh issue view 148`, read-only)

* Criteria 1 to 3 are checked. Criterion 4, "A dry-run mode is available and the sequence is tested in a disposable environment", is unchecked.
* The infra README (section "Scripted Azure rebuild and teardown") says the disposable-Azure part of criterion 4 "has not been run or authorised"; tests use a stateful fake `az`.
* The earlier 112-test orchestrator run (four-image candidate) used fake runners. It proves wiring, not a real build, Azure behaviour or image digests.

## Actual CLI and dry-run implementation (read before any run)

* Entry point: `python3 -m zava_forward.orchestrator.rebuild_azure {rebuild|teardown}` with required `--subscription --registry --image-tag --parameters --seed --roster --container-app`; optional `--apply --environment --workload --from-stage --parameter --build-pool --repo-root`.
* `main()` parses arguments, builds `AzureConfig`, calls `config.validate()` and, when `--apply` is absent, prints `plan()` and returns 0 before `AzureBackend` is constructed. `validate()` does regex checks and reads only the seed and roster files (`assert_synthetic`, email-domain scan). `check_account()` (the first `az` call) is reached only after the dry-run return.
* `plan()` calls `rebuild.dry_run()` (static stage list, no I/O) and lists the four images with Dockerfile and deploy input. No `az`, token, network or tenant read is needed. Static reading is not proof; the run below observes it with no `az` on PATH, an empty credential environment and a network-less namespace where the host permits it.
* Dry-run cannot show registry tags, tenant state, deployment or inventory. Those stay unverified.
* The second CLI, `python3 -m zava_forward.orchestrator.rebuild --dry-run`, is a static contract print and is a distinct, cheaper check of the authoring module.

## Four affected images and maintained build/smoke commands

* Images: `api` (`zava-forward-mvp` repository in Azure; `src/api/Dockerfile`), `agents`, `orchestrator`, `importer`. Maintained command from `src/README.md`: `docker build -f src/<project>/Dockerfile -t <tag> src` (context `src/`), then `python src/check-container.py <project> <image>` from the repository root.
* `check-container.py` asserts image metadata (user 10001:10001, no ENTRYPOINT, direct `python -m zava_forward.<project>` CMD), a hardened probe (read-only root, zero capabilities, NoNewPrivs, EROFS on write, writable `/state`, no baked data), negative probes per image, agents dependency isolation (no `mssql_python` or `azure`), and for agents/orchestrator/importer a version-line stdout (`zava-forward-<dist> 0.1.0`) under hardened and plain launch. For the API it starts a detached container with an owned synthetic `{"cases":[],"staff":[]}` seed, publishes `127.0.0.1` only, polls `/healthz`, fetches `/zava-logo.png`, writes `/state` and removes the exact container ID it created (`docker rm -f`).
* The script sets `ZF_AI=off`, mounts only its own temp directory read-only and makes no registry, Azure or model call. Container-side runtime network use is limited to the loopback health probe.
* Dockerfiles run `apt-get update/upgrade` and `pip install --require-hashes` during build. Those downloads are ordinary declared-manifest dependency fetches. Base image is digest pinned (`python@sha256:34386ef0...`).
* Coverage ceiling: build + container-control + entrypoint/health smoke. Not covered: service orchestration, SQL, Entra, ACR build (`az acr build`), digest in a registry, Container Apps hosting, or the full rebuild stage sequence.

## Environment and admission facts (2026-11-10 16:05 UTC)

* Disk: `/` 247G, 94G free (63%). Memory: 15G total, about 2G available at inspection; 4 CPUs; load about 1.9.
* Docker 29.9.0, overlayfs, buildx v0.38.0. Pre-existing shared state: 71 images, 0 containers, 2415 build-cache records. All belong to other lanes and are not to be modified, pruned or stopped.
* Canonical lock `/tmp/ama-rpi-heavy.lock` exists (zero bytes); holder unknown until a non-blocking `flock -n` is attempted at implementation start. BUSY means freeze a partial handoff; no wait, queue, spin or kill.
* Python 3.12.3. Own venv `~/.venvs/issue148-current-proof-1110` only; no global installs. Existing venvs belong to other lanes.

## Risks and decisions

* Layer cache could make a "fresh" build trivially cached: use `docker build --no-cache` with unique tags `zava-forward-<project>:p148cur-64c3f9191a2f` and labels naming source commit and task. The pinned base layer may be reused from the local store; this is recorded as such.
* Host memory is low. Run the build and smoke sequentially under `nice` and `taskset -c 0,1`; the maintained smoke script offers no container memory flag and none is added (no edit authorised). Record this as a bound gap.
* A failed build or smoke is preserved as first evidence and classified; no retry-until-green. A confirmed source or packaging defect freezes the lane for a separate scoped RPI.
* Free-port or Docker-daemon contention could cause an environmental failure; classify rather than retry, except one retry of a single missing declared dependency with exact pins.

## Evidence sources

* `infra/README.md` (sections "Scripted Azure rebuild and teardown", "Rebuild authoring and local rehearsal"), `src/README.md` (build command, hardened image CI), `src/orchestrator/src/zava_forward/orchestrator/rebuild_azure.py` (`main`, `plan`, `AzureConfig.validate`), `rebuild.py` (`dry_run`), `src/check-container.py`, `src/{api,agents,orchestrator,importer}/Dockerfile`, GitHub issue #148 body.

## Planning Readiness

`Ready`: scope, commands, exclusions, admission rule and failure handling are fixed above.
