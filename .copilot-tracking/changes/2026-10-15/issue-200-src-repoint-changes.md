# Changes: issue 200

## Files changed

* `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py`
* `.github/workflows/mvp-validation.yml`
* `src/api/README.md`, `docs/reference/log.md`

## Acceptance criteria status

* Packaging via pyproject and installed packages: met (M1 to M6).
* Workflow paths, commands, build context, requirements: met; names kept (owner decision 2026-10-15).
* Image from `src/` same behaviour: Dockerfiles and CI image job exist; NOT verified locally (Docker permission denied). New tag deploy and verification: UNTICKED, needs Azure and CI image.
* Bicep commands and `bicep build`/`lint`: met locally (exit 0).
* Private output location, `.gitignore`, committed-data check: met after this change.
* `rename-zava-tests.py` and `infra/tests`: pass.
* Historical identifiers exact: unchanged.
* Rename of workflow names: deferred to after cut-over (#201).

## Validation commands (venv, pip only)

* `pip install -e src/core -e src/agents -e src/api -e src/orchestrator`: ok
* api unittest (`PYTHONPATH=../core/tests:../agents/tests`): 440 tests OK (92 skipped)
* core unittest: 252 OK; orchestrator: 17 OK
* `python3 tools/rename-zava-tests.py`: 25 OK (needs python-pptx, pillow, pyyaml)
* `python -m unittest discover -s infra/tests`: 75 OK
* `az bicep build` and `az bicep lint` on `infra/main.bicep`: exit 0
* `ruff check src`: all checks passed; `mypy src/core/src` reports 3 relative-import errors, identical on main (invocation style)
* Generator with `ZF_DATA=/tmp/zfd/zavaforward.json --seed 20260901 --as-of 2026-10-13`: wrote 980 cases, 10 staff
* Local server run with that data: `/healthz` 200
* `docker ps`: permission denied, image checks rely on CI. No Azure deployment performed.
