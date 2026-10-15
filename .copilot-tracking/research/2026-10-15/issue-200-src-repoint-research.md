# Issue 200 research: repoint CI, Docker, Bicep, scripts and docs to src

Disposition: executed. Planning readiness: Ready.

Sources: `gh issue view 200 --comments`, ADR 0006, `docs/architecture/mvp-to-src-parity-matrix.md`, `src/README.md`.

## Findings on main (a381532)

* Done in M1 to M6: pyproject packaging per project, `src-ci.yml` plus `mvp-ci.yml`/`mvp-validation.yml` filters and installs on `src/`, Dockerfiles with project build context, Bicep job commands `python -m zava_forward.orchestrator.token_store` and `digest_blob --publish`, `infra/README.md` `az acr build -f src/api/Dockerfile src`, `/src/**/data/` in `.gitignore`, infra tests free of `mvp` paths.
* Gaps: `build_mvp_dataset.py` still inserted `mvp` on `sys.path` and wrote `mvp/data/zavaforward.json`; `mvp-validation.yml` data check only covered `mvp/data`. `zf_mvp_coverage.py` already imports `zava_forward.core`. `tools/rename-zava*` keep `mvp` strings as historical identifiers (policy, tests pass).
* Owner decisions: keep workflow and check names until after cut-over. Not producible here: deploy of a new tag (needs Azure and Docker).
