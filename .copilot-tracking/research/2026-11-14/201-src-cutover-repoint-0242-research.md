---
title: Research, src cutover repoint contract (Refs #201 criterion 5)
ms.date: 2026-11-14
---

## Scope

Local contract proof that CI, Docker, Bicep and scripts use `src/`. Live Azure deployment health is the separate Azure-only half of criterion 5 and is not covered.

## Evidence

* `.github/workflows/src-ci.yml`: matrix over core, api, agents, orchestrator, importer with `working-directory: src/<project>`, ruff, mypy, unittest and `docker build -f src/<project>/Dockerfile ... src`.
* `.github/workflows/src-deploy.yml`: builds `src/$PROJECT/Dockerfile` with context `src` for api, agents, orchestrator, importer.
* `mvp-ci.yml` and `mvp-validation.yml` keep legacy file names but build from `src/api/Dockerfile` with context `src`. The only retired-path text is negative guards (`git ls-files mvp/data`) asserting retired data stays absent.
* `src/{api,agents,orchestrator,importer}/Dockerfile`: COPY `core/`, own project and (api) `agents/` under the `src` context, build wheels, no `PYTHONPATH`.
* `infra/`: Bicep loads `../src/core/...` JSON; image guidance names `src/api/Dockerfile` and `src/api/live-simulator.Dockerfile`. Retired `mvp/` appears only in `infra/README.md` prose tagged with archive `v0.21.0`, and in cutover-proof material.

## Finding

No broken legacy path bug found. Workflows, `src/api/pyproject.toml` and `docs/reference/log.md` stay untouched.

## Planning Readiness

Ready. Disposition: executed.
