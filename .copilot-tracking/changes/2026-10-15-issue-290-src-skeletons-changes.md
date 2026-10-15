---
title: Issue 290 changes, src project skeletons
ms.date: 2026-10-15
---

Plan: `.copilot-tracking/plans/2026-10-15-issue-290-src-skeletons-plan.md`. Branch `feat/src-project-skeletons`. No file under `mvp/` changed (`git diff origin/main -- mvp` is empty).

## Files added or changed

| Path | Change |
| --- | --- |
| `src/<project>/pyproject.toml` (5) | setuptools backend, namespace discovery, dynamic version, ruff, mypy strict; core extras `sql` and `blob`; `dev` extra pins ruff 0.17.1 and mypy 2.4.0 |
| `src/<project>/src/zava_forward/<name>/{version,__main__}.py` (10) | Version module and entry point that prints `<distribution> <version>` |
| `src/<project>/tests/test_version.py`, `test_dependency_rule.py` (10) | Version, namespace and dependency-rule tests; agents also asserts core is required without extras and no SQL or blob dependency |
| `src/<project>/requirements.in`, `requirements.txt` (10), `src/build-requirements.{in,txt}` | Hashed pins from `pip-compile --generate-hashes` |
| `src/{api,agents,orchestrator,importer}/Dockerfile` (4), `src/.dockerignore` | Pinned base digest, wheel build stage, user 10001, no data, `ZF_DATA` and `ZF_STATE` |
| `.github/workflows/src-ci.yml` | New checks `src-core`, `src-api`, `src-agents`, `src-orchestrator`, `src-importer`, `src-namespace`, `src-no-working-data` |
| `.gitignore` | `/src/**/data/` and build, venv and cache folders under `src/` |
| `src/README.md`, `docs/adrs/0006-src-layout-and-cutover.md`, `docs/reference/README.md`, `docs/reference/log.md` | Index, build-context clarification, catalog row, log entry |

## Divergences and decisions

* Docker build context is `src/`, not the project folder (the ADR sentence is amended). Reason: images need the sibling `core`.
* Core extras per workload are provisional: api `sql`, orchestrator `sql` and `blob`, importer `blob`, agents none.
* `mvp-validation.yml` was not edited; the no-working-data check for `src/` is a new job in `src-ci.yml`.
* The Trivy scan is in CI only; the SBOM step of `mvp-ci` is not repeated.
* Docker is permission denied for the user; images were built with `sudo -n docker` (passwordless), and the four local images were removed afterwards.

## Commands and results (local, 2026-10-15)

| Command | Result |
| --- | --- |
| `python3 -m venv /tmp/zfenv/<project>` and `pip install -e ../core [-e ../agents] -e ".[dev]"` per project | installed for all five |
| `python -m unittest discover -s tests -q` in each project | core 5, api 4, agents 6, orchestrator 4, importer 4 tests, all OK |
| `ruff check .`, `ruff format --check .`, `mypy` in each project | all clean |
| `pip install -e core -e agents -e api -e orchestrator -e importer`, then `python -m zava_forward.<name>` | five installed side by side; each prints its version; `zava_forward.__path__` has five roots, `__file__` is `None` |
| `pip install --require-hashes -r build-requirements.txt`, `pip wheel --no-deps --no-build-isolation` core and agents, install wheels | works; `mssql_python` and `azure` absent |
| `pip-compile --generate-hashes` per project | agents file has no requirements; core pins match `mvp/requirements.txt` except transitive `pycparser` 3.11 (mvp has 3.1) |
| `git ls-files ':(glob)src/**/data/**'` with a forced-added probe file | lists the probe; empty on the real tree |
| `git check-ignore -v` on `src/**/data`, `build`, `*.egg-info` probes | all ignored |
| `sudo -n docker build -q -f src/<project>/Dockerfile src` for api, agents, orchestrator, importer | all four built |
| Image checks for each: `id -u` is 10001; `/app/data` and `/data/zavaforward.json` absent; `docker run --read-only --cap-drop ALL --security-opt no-new-privileges --tmpfs /tmp --tmpfs /state` prints `<distribution> 0.1.0` | all pass |
| Import probe inside images | agents: no `mssql_python`, no `azure`; api and orchestrator: both; importer: `azure` only; no image has `setuptools` |
| `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` | Ran 719 tests, OK (skipped=92) |
| YAML load of `src-ci.yml` | jobs `project`, `namespace`, `no-working-data` |

Not verified locally: the GitHub Actions run, the Trivy scan and the `mssql` job (CI only).
