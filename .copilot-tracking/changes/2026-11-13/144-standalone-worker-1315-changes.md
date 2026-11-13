# Changes: issue 144 standalone worker (1315)

Status: implemented and validated. Refs #144, #136.

* Added `src/agents/src/zava_forward/agents/runtime.py`: environment wiring, managed-identity token source (redirect-refusing), API result sink, heartbeat and health.
* `worker.py`: `serve` builds the runtime, handles SIGTERM, stops on allowance expiry (exit 3); `health` command; refusals name settings only.
* `infra/modules/containerapps.bicep`: agents container `command`/`args` run `serve` (image CMD kept as version line, per critique).
* Tests (RED first, then GREEN): `test_runtime.py` (new), `test_worker.py`, `infra/tests/test_container_contract.py`.
* Docs: `src/agents/README.md`, `infra/README.md`.

## Validation

* Agents unit tests: full discover 353 tests, one failure (assertion case, fixed); re-run of worker/runtime/queue/dependency tests 125 OK.
* `infra.tests.test_container_contract` 8 OK; `test_deploy` 19 OK; `test_bicep_policy` 61 tests, 1 error (`No module named zava_forward.orchestrator`, same on the base commit, package not installed here).
* `ruff check`/`ruff format --check` on changed files clean (repository-wide ruff reports pre-existing issues elsewhere); `mypy` in `src/agents` clean.

## Divergences and open work

* Dockerfile unchanged (critique 1). API `/api/agent-results` route, Bicep `ZF_ASSIST_*` allowance and financial meter remain follow-ups; no image build, queue or model call was run.
