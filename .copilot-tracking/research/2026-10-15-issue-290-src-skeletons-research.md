---
title: Issue 290 research, src project skeletons
ms.date: 2026-10-15
---

Task: `issue-290-src-skeletons` (child of epic #195). Research disposition: executed. Planning Readiness: Ready.

## Evidence

| Source | Finding |
| --- | --- |
| Issue #290 | Nine acceptance criteria: README index, five projects with own `pyproject.toml`, PEP 420 namespace, `sql` and `blob` extras on core, hashed requirements and four Dockerfiles, import test per project, one CI job per project with the existing `mvp` jobs kept, `.dockerignore` and `.gitignore` for `data/`, local-first verification |
| ADR 0006 (Accepted 2026-10-15) | Layout `src/<project>/src/zava_forward/<name>/`, tests outside the package, distribution names `zava-forward-{core,api,agents,orchestrator,import}`, dependency rule, Dockerfile properties, `ZF_DATA`, Verification (local first, Azure group `ama` only if needed) |
| ADR 0001 | Four workloads with separate identities; `agents` has no database, blob or Key Vault access |
| `mvp/Dockerfile` | Base digest `python@sha256:34386ef0...`, user 10001, `/data` and `/state`, `ZF_DATA`, `--require-hashes` install, no working data |
| `mvp/requirements.in` | `mssql-python==1.15.0`, `azure-storage-blob==12.31.0`; the hashed file is `pip-compile --generate-hashes` output |
| `.github/workflows/mvp-ci.yml` | Jobs `test`, `image`, `mssql`; image job asserts non-root, no data, read-only root with `--cap-drop ALL`, Trivy scan. Names must stay |
| `.github/workflows/mvp-validation.yml` | Existing step `Refuse committed working data` covers `mvp/data` only |
| Owner decisions in the task | Namespace `zava_forward`, isolated projects, new check names, no module moves, no edits in `mvp/`, pip only |

## Findings and risks

* A skeleton has no entry point. Each image runs `python -m zava_forward.<name>`, a `__main__` that prints the version, so the non-root, no-data and read-only checks are real.
* ADR text says the project folder is the Docker build context, but a workload image must also copy `core`. The sibling cannot be copied from a project-folder context. Decision: build context is `src/`, Dockerfile is `src/<project>/Dockerfile`, a single `src/.dockerignore` excludes data, tests and evals, and each Dockerfile copies named projects only. Recorded as a clarification in ADR 0006.
* Images install local packages as wheels built in a builder stage. The build tools (`setuptools`, `wheel`) are hash-pinned in `src/build-requirements.txt`, so no pin is loosened, and they are absent from the final image.
* The agents image installs `core` with no extras. Extras are provisional (api `sql`, orchestrator `sql` and `blob`, importer `blob`) and are reassessed when modules move (#199).
* Docker access: `docker ps` fails with permission denied for this user, so image criteria can be verified only by CI.
* Tests use `unittest` (the repository convention), run from each project folder against an editable install.

## Planning Readiness

Ready. No open question blocks implementation.
