---
title: Issue 290 plan, src project skeletons
ms.date: 2026-10-15
---

Branch `feat/src-project-skeletons`. Pull request targets `main`, `Refs #290`. Research: `.copilot-tracking/research/2026-10-15-issue-290-src-skeletons-research.md`.

## Phases

* [x] 1 Project skeletons: `src/{core,api,agents,orchestrator,importer}` each with `pyproject.toml` (setuptools, namespace discovery, ruff, mypy, unittest), `version.py`, `__main__.py`, `tests/test_version.py`, `tests/test_dependency_rule.py`
* [x] 2 Requirements: `requirements.in` and hashed `requirements.txt` per project, shared hashed `src/build-requirements.txt`
* [x] 3 Images: Dockerfiles for api, agents, orchestrator, importer, base digest pin, user 10001, no data, `src/.dockerignore`, `.gitignore` entries
* [x] 4 CI: new workflow `src-ci.yml` with new check names (`src-<project>`, `src-namespace`, `src-no-working-data`); `mvp-ci.yml` and `mvp-validation.yml` untouched
* [x] 5 Docs: `src/README.md`, ADR 0006 clarification, `docs/reference/README.md` index, `docs/reference/log.md`
* [x] 6 Local validation: venv per project, tests, ruff, mypy, all five installed side by side, existing `mvp` suite, Docker attempt
* [x] 7 Changes and review artifacts, commit, push, pull request

## Critique (single pass, direct dispositions)

* Build context conflict with ADR text: accepted, documented in ADR 0006.
* Empty `requirements.txt` for projects with no third-party dependency: verify that `pip install --require-hashes` accepts it, otherwise omit the step.
* No `mvp/` file is touched; no module moves.

## Success criteria

Issue #290 acceptance criteria, with image criteria verified only by CI if Docker is unavailable.
