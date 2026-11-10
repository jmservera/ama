# Changes: #148 current-source local image and dry-run proof (2026-11-10)

Status: complete. No product file was edited. Source `64c3f9191a2ffa97ef2dc07245422333ad4d6585`; the worktree HEAD at run time was the docs-only commit `fbb1c6e52287eac711f14990c8ca296f59441187` whose `src` tree `c322b0f7a710c7f121fcd75b6685683ff57fa893` and `infra` tree `f7f31c0934cfe0bafb4505408706e55aa8ab61e7` are identical to the source commit's. `git status` of `src/` and `infra/` was empty before and after.

## Execution

One locked run (`flock -n -E 75 /tmp/ama-rpi-heavy.lock`, lock acquired immediately, 2026-11-10 16:09:04Z to 16:13:46Z, script exit 0). Raw bundle stays outside the repository (`ROOT/evidence-148-current-image-proof-1110/`, with `SHA256SUMS`). Correction 2026-11-10: the original `SHA256SUMS` hashes `steps.tsv` before the runner appended `DONE`, so it fails for that one file (48 other entries pass); it is kept unchanged as adverse evidence. A separately named external final-snapshot manifest and reconciliation note exist (`ROOT/evidence-148-current-image-proof-1110.final-snapshot.sha256` and `...final-snapshot-note.md`); see the documentary reconciliation changes record.

| Step | Command (abridged) | Exit |
| --- | --- | --- |
| Own venv, pip | `python3 -m venv ~/.venvs/issue148-current-proof-1110`; `pip install` of `git archive` copies of `src/core` and `src/orchestrator` | 0, 0 |
| Dry-run rebuild | `env -i PATH=<empty dir> HOME=<empty> python -m zava_forward.orchestrator.rebuild_azure rebuild ...` (zero-GUID subscription, synthetic seed and roster) | 0, empty stderr |
| Dry-run teardown | same, `teardown` | 0, empty stderr |
| Contract dry-run | `python -m zava_forward.orchestrator.rebuild --dry-run` | 0 |
| Dry-run assertions | scope "no az or network call", four images in order api/agents/orchestrator/importer (`zava-forward-mvp` repository for api), three operator-gated stages | 0 |
| Builds | `docker build --no-cache -f src/<p>/Dockerfile -t zava-forward-<p>:p148cur-64c3f9191a2f src` under `nice`/`taskset -c 0,1` | 0 x4 (api 73 s, agents 40 s, orchestrator 49 s, importer 39 s) |
| Smoke | `python3 src/check-container.py <p> <image>` | 0 x4, each printed `<p>: Docker controls, negative probes and compatible startup PASS` |

## Image identities (local observations of this run; none pushed)

| Image | ID | Size bytes |
| --- | --- | --- |
| zava-forward-api:p148cur-64c3f9191a2f | sha256:553805e20106a2c946e564c8b96dd482846188b581f4c049b1de284609ebe0b2 | 362141187 |
| zava-forward-agents:p148cur-64c3f9191a2f | sha256:54c54328a6ccf68d942b369dd4f00c4757bb3516a1ad5e90838af5cb7fdd5515 | 243254198 |
| zava-forward-orchestrator:p148cur-64c3f9191a2f | sha256:13377c0ffc4a2c882b1302ccac4845feeb3500c98f3c4976047e77819b60f327 | 329690033 |
| zava-forward-importer:p148cur-64c3f9191a2f | sha256:ae84989f78a8fd322e0c3a4af42a99e63dec29b60e40685f2aec1336e9b21662 | 282011108 |

Local `docker image inspect` (raw `inspect-<project>.json`) populated `RepoDigests` for all four, e.g. `zava-forward-api@sha256:553805e2...e0b2`, each equal to the image ID above. That is local Docker metadata for locally built images, not evidence of remote registry publication, resolution or deployment. Reproducibility of the images was not assessed.

Each has User `10001:10001`, CMD `python -m zava_forward.<project>` and labels `ama.issue=148`, `ama.task=issue-148-current-image-proof-1110`, `ama.source=<source sha>`. Images are retained.

## Deviations and gaps (first outcomes preserved, no retry)

* Network namespace isolation (`unshare -rn`) was not available, so the dry-run claim is reduced to: empty environment, empty `PATH` (an `az` exists at `/usr/bin/az` but was not reachable), empty `HOME`, nothing on stderr. Network non-use is not observed.
* Container ID capture failed: my `docker events` format string (`{{.ID}}`) is invalid for the Docker 29 event type, so no exact IDs were captured. IDs are unobserved. The smoke's own `--rm` and `docker rm -f` cleanup left no container: `docker ps -a -q --filter ancestor=<image>` was empty for all four and total containers were 0 before and after. Docker images rose from 71 to 75 (the four owned images).
* The smoke does not block container egress and sets no memory bound (the maintained script offers none).
* Capacity: `/` 94G free before, 93G after; memory available about 2.2 GB before and 3.0 GB after.

## Coverage

Established locally: the offline dry-run path of the existing script at this source; fresh `src/`-context builds of the four images; maintained hardened-launch, negative-probe and entrypoint/health (API on loopback with an owned synthetic seed) smoke. Not established: registry tags or digests, ACR build, Azure inventory, whole rebuild or teardown, images deployed, SQL, Entra, model, Container Apps, hosted CI, security acceptance. #148 criterion 4 is not delivered.
