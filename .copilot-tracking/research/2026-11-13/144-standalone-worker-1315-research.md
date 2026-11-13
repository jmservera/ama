# Research: issue 144 standalone agents worker (1315)

Task: `144-standalone-worker-1315`. Research disposition: executed. Planning Readiness: Ready.
Read: case study original and addendum, `docs/reference/README.md`, `memory.md` (context only).

## Evidence (base dafed6a27)

* `src/agents/Dockerfile` is already a real image (digest-pinned, `apt-get upgrade`, non-root 10001, core+agents wheels) but `CMD` is `python -m zava_forward.agents`, which prints the version and exits 0. A Container App replica would exit at once: the "placeholder" behaviour.
* `worker.py` `main(["serve"])` always refuses with exit 2 ("no task queue or result post-back is configured"). `serve`, `install_signal_handlers` exist and are tested.
* `queue_azure.py` `AzureTaskQueue` (stdlib REST, injected token source and transport) exists and is tested; nothing constructs it.
* `infra/modules/containerapps.bicep` agents app already sets `QUEUE_ENDPOINT`, `TASK_QUEUE`, `POISON_QUEUE`, `AZURE_CLIENT_ID`, `FOUNDRY_ENDPOINT`, `MODEL_DEPLOYMENT_DEFAULT/CAPABLE`, `API_BASE_URL`, `API_AUDIENCE`, a queue scale rule (0 to 5), but no `ZF_ASSIST_*` allowance. Core `Ai` reads `AI_ENDPOINT`/`AI_DEPLOYMENT`/`AI_DEPLOYMENT_STRONG`, not the Bicep names.
* No API route accepts worker results (`grep` of `src/api/src` finds none). The post-back endpoint is therefore a documented open dependency.
* `infra/README.md` lines 678 and 1626 still say the agents workload is a placeholder.
* `infra/tests/test_container_contract.py` requires, for every `src/*/Dockerfile`: `USER 10001:10001`, `CMD ["python", "-m", "zava_forward.`, no ENTRYPOINT, `apt-get upgrade -y --no-install-recommends`, digest-pinned FROM. CI (`src-ci.yml` line 220) and `check-container.py` run the image with no arguments and expect the version line, so the no-argument default must stay.

## Prior candidates (read-only)

* `issue-144` (9c279c861): tracking and log only, no source change for this slice.
* `issue-144-ci-recovery-1111` (696b77374): CI failure was a Playwright OS-dependency apt step failing on mirror DNS (run 43037357026); no source defect. Nothing to fix cleanly beyond avoiding browser-touching changes.

## Selected slice

1. `runtime.py`: environment wiring (`build_runtime`), managed-identity token source (stdlib, ACA `IDENTITY_ENDPOINT`), `ApiResultSink` (HTTPS POST to `API_BASE_URL` + `/api/agent-results`, bearer for `API_AUDIENCE`, refuses redirects), heartbeat file, `health` check.
2. `worker.main`: `serve` builds the runtime; missing or invalid settings refuse with exit 2 naming variables (never values); `health` exits 0/1 from heartbeat age; default prints version.
3. Dockerfile `CMD [... "zava_forward.agents", "serve"]` for agents only.
4. Tests and docs (`infra/README.md`, `src/agents/README.md`).

## Boundaries and risks

* The API result route and the `ZF_ASSIST_*` operator allowance are not delivered; without them the worker refuses or leaves messages for redelivery then poison. No acknowledgement before a successful post. This is documented, not claimed as done.
* No live calls, Docker or browsers.
