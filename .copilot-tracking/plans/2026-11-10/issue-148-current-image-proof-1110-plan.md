# Plan: #148 current-source local image and dry-run proof (2026-11-10)

Task `issue-148-current-image-proof-1110`. Source `64c3f9191a2ffa97ef2dc07245422333ad4d6585` stays unchanged. Research: `.copilot-tracking/research/2026-11-10/issue-148-current-image-proof-1110-research.md`. Details: `.copilot-tracking/details/2026-11-10/issue-148-current-image-proof-1110-details.md`.

## Objective

Produce observed local evidence that (a) the existing offline dry-run of `rebuild_azure` needs no Azure, credential or network, and (b) the four affected images build fresh from the `src/` context at the exact source and pass the maintained container and entrypoint smoke. Record what this does not establish.

## Phases

* [ ] P0 Admission: attempt `flock -n /tmp/ama-rpi-heavy.lock` once at implement-start. BUSY means record the holder if visible, freeze a partial handoff, make no implementation attempt, and do not claim seven events as a pass.
* [ ] P1 Preflight inside the lock: exact HEAD, clean `src/` and `infra/`, capacity, Docker inventory counts, `az` absence.
* [ ] P2 Own venv and offline dry-run: archive copy of `src/core` and `src/orchestrator`, pip install into the own venv, three dry-run invocations under an empty environment, no `az` on PATH and a network-less namespace when the host permits it; assert output structure.
* [ ] P3 Four fresh builds, sequential, `--no-cache`, unique tag `p148cur-64c3f9191a2f`, labels for issue, task and source; image IDs recorded.
* [ ] P4 Maintained smoke `python3 src/check-container.py <project> <image>` for each built image; record exact container IDs from daemon events and confirm no owned leftover container.
* [ ] P5 Identity capture and postflight: image inspect, source unchanged, Docker counts, checksums of the raw bundle (kept outside the repository).
* [ ] P6 Reconcile, summarise evidence in the changes record, one review, commit dated records only.

## Stop rules

* First failure is preserved and classified (environment, own-environment dependency, source/packaging defect). No retry-until-green. One missing declared own-environment dependency may be restored with exact pins.
* A confirmed source or packaging defect freezes this lane for a separate scoped RPI. No source, test, config or documentation edit to the product.
* No `az`, cloud or tenant operation, no credential or private data read, no registry push, no model, provider or IMDS call, no prune, no change to existing images or containers.

## Exit criteria

* Every command has an exit status in the evidence. Skips are named.
* Handoff states exact head and tree, source, image IDs and container IDs, partial or full witness, residuals.
* Criterion 4 of #148 is not claimed delivered; Docker is not Azure acceptance.
