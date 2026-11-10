# Details: #148 current-source local image and dry-run proof (2026-11-10)

Plan: `.copilot-tracking/plans/2026-11-10/issue-148-current-image-proof-1110-plan.md`.

## Execution unit

One script, `ROOT/run-148-current-image-proof-1110.sh`, is run once as `flock -n /tmp/ama-rpi-heavy.lock bash <script>` so all heavyweight work stays inside the held lock. Raw outputs go to `ROOT/evidence-148-current-image-proof-1110/` (not committed). The script is authored before implementation and is not part of the product.

## Phase detail

* P0: lock exit 1 means BUSY. The holder is inspected with `fuser`/`lsof` read-only if available; nothing is killed or waited on.
* P1: asserts `HEAD == 64c3f9191a2ffa97ef2dc07245422333ad4d6585` and no change under `src/` or `infra/`; otherwise stops with `SOURCE_IDENTITY_MISMATCH`.
* P2: `git archive HEAD src/core src/orchestrator` into an owned temp directory so pip leaves no build output in the worktree. Dry-run command, run for `rebuild` and `teardown`: `python -m zava_forward.orchestrator.rebuild_azure <op> --subscription 00000000-0000-0000-0000-000000000000 --registry acrdemo148 --image-tag p148cur-<sha12> --parameters infra/main.test.bicepparam --seed <owned seed> --roster <owned roster> --container-app ca-demo-api` with `env -i`, empty `HOME`, an empty `PATH` directory and `unshare -rn`. Third check: `python -m zava_forward.orchestrator.rebuild --dry-run`. Assertions: exit 0, empty stderr, scope text "no az or network call", four images in order, three operator-gated stages. The seed and roster hold no personal data (`{"cases":[],"staff":[]}`).
* P3: `docker build --no-cache --progress=plain --iidfile <f> --label ... -f src/<project>/Dockerfile -t zava-forward-<project>:p148cur-<sha12> src` for api, agents, orchestrator, importer in that order, under `nice -n 10 taskset -c 0,1`.
* P4: `python3 src/check-container.py <project> <image>` from the repository root. It runs hardened, negative-probe and plain launches, and for the API a loopback-only (`127.0.0.1`) detached service with an owned synthetic seed, readiness poll of `/healthz` and a logo fetch, then `docker rm -f` of its own container. A `docker events` watcher scoped to the image tag records each container ID created; the watcher PID is stopped by exact PID. Post-check lists any container whose ancestor is the owned image.
* P5: `docker image inspect` per image (ID, labels, user, cmd, size, created), post-run `git status`, Docker image and container counts and capacity, and `sha256sum` of the raw files.

## Expected runtime outcome (stated before running)

* Dry-run: exit 0, JSON plan, nothing else.
* Builds: four exits 0, user `10001:10001`, no ENTRYPOINT, CMD `python -m zava_forward.<project>`.
* Smoke: four lines `<project>: Docker controls, negative probes and compatible startup PASS`, exit 0. Agents/orchestrator/importer print `zava-forward-<dist> 0.1.0`; API serves `/healthz` 200 on loopback.

## Not covered

Registry tags or digests, ACR build, Azure inventory, whole rebuild or teardown stages, SQL, Entra, model, Container Apps, hosted CI, security acceptance. Container memory is not bounded because the maintained smoke exposes no such option and none is added.

## Critique dispositions applied

* Image IDs are run observations, not source-derived or registry digests (no `RepoDigests`); images are not reproducible because of the in-image `apt-get upgrade`.
* The smoke does not technically block container egress (default Docker network, no edit authorised); the claim is "no outbound call made by the smoke code", not network isolation.
* Container IDs not captured by the events watcher are reported as unobserved. If the network namespace is unavailable, the dry-run claim is reduced to no `az` on PATH and an empty credential environment.
* `git status` of `src/` and `infra/` is checked before and after; pip installs from an archive copy.

## Dependencies

Docker daemon, outbound access for ordinary package and base-layer fetches during build, a free canonical lock.
