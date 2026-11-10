<!-- markdownlint-disable-file -->
# Research: issue 148 four-workload image wiring in the Azure rebuild adapter

Readback `date -u` 2026-11-10T01:21Z. Base `26bf987ca6c7d6c33d866de8a99cb2d43815c9cf`, branch `fix/demo-rebuild-images-148-1110`. Research disposition: `executed`. Planning Readiness: `Ready`.

## Lifecycle (supplied evidence, not re-queried)

* Original PRs #511, #672 and #1145 are merged. Old branch `feat/issue-148-r4` (`885687`) has zero unmerged commits and no PR. #1145 was docs-only. There is no failed or exhausted four-image implementation to restore. This is a new, source-qualified engineering gap, not a retry of a disposable Azure run.
* Criterion 4 of #148 (disposable Azure rebuild) stays unmet. This work is fake-command wiring evidence only. #148 stays open; use `Refs #148` only.

## Source facts (pinned main)

* `rebuild_azure.py` `images` stage runs one `az acr build` of `src/api/Dockerfile` with context `src/` as `zava-forward-mvp:<tag>`, and `verify` checks only that repository for the tag.
* `_deploy(True)` passes only `apiImage=<registry>/zava-forward-mvp:<tag>`. `RESERVED_PARAMETERS` protects only `deployApplications`, `deployEnvironmentOnly`, `apiImage`; an override could name `agentImage`/`importImage`.
* `infra/scripts/deploy.py` rejects `orchestratorImage` as a `--parameter` and exposes `--orchestrator-image`. Without it, `resolve_image` guesses from existing jobs, newest tag in `zava-forward-orchestrator`, or the quickstart placeholder.
* `infra/main.bicep`: `apiImage`, `agentImage`, `importImage` default to the quickstart placeholder; `orchestratorImage` defaults to empty (placeholder). `infra/scripts/pipeline.py` maps `api->apiImage`, `agents->agentImage`, `orchestrator->orchestratorImage`, `importer->importImage` and names registry repositories `zava-forward-<project>`.
* All four Dockerfiles (`src/{api,agents,orchestrator,importer}/Dockerfile`) use `src/` as build context (`docker build -f src/<project>/Dockerfile src`).
* `rebuild.py` stage `images` is described as "applicable workload images pinned to digests"; the adapter verifies tags only. Existing src-deploy digests come from the trusted pipeline, which is out of scope.

## Adapter contracts that must hold

* Dry run is the default and makes no `az`/network call (`main` returns before backend creation; `plan()` is static).
* `run_rebuild`: from-empty requires empty inventories; `--from-stage` after `discover` re-runs `discover` only (so `found['registry']` exists) and does NOT re-run `images`. A resume at `applications` therefore currently trusts that images exist.
* Stops: `GATED_STAGES` stop with exit 2; `RebuildError`/`ScriptExit` give `REBUILD_FAILED` exit 1; `subprocess_runner` timeout 3600; delete wait 900; teardown ordering untouched.
* Secret guard `assert_no_secret_argv` runs on every argv; image references and `--orchestrator-image` pass it.
* Private registry requires `--build-pool`; the pool existence check precedes the first build and carries the `--from-stage images` resume instruction.

## Gap and constraints

* A default rebuild produces/selects one image of four. Agents/importer keep placeholders; orchestrator is guessed.
* Legacy API repository `zava-forward-mvp` is pinned by existing tests, README and registries; keep it (no source contract proves a change). Others reuse `zava-forward-<project>` (`deploy.py` `REPOSITORY`, `pipeline.py`).
* A two-file solution honours existing contracts: existing parameter names plus explicit `--orchestrator-image`. No conflict found, no STOP.

## Residual (not addressed)

* Digest pinning of the four images, disposable Azure run, workload SQL/model probes, README wording (shared docs outside ownership; the `images` description there stays accurate for "image build").
