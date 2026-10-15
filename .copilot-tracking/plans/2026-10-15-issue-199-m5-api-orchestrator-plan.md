---
title: Issue 199 M5 plan
ms.date: 2026-10-15
---

## Phases

* [x] 1. Move modules, web, law register, checks, tests with `git mv`; delete `mvp/Dockerfile`, requirements and `__init__.py` after merging into `src/api`.
* [x] 2. Fix imports, path constants, package data, pyproject exemptions, mypy overrides.
* [x] 3. Regenerate `src/api/requirements.txt` with pip-compile; rewrite Dockerfile and ignore file for the `src/` context; update Bicep job commands.
* [x] 4. Update workflows (filters, PYTHONPATH, image build), docs, rubric registry, matrix, index, log.
* [x] 5. Validate, record, commit, open PR (Refs #199).

## Critique (executed once)

Verdict: accepted. Compatible findings applied: keep tests in `api/tests` because `core` and `agents` may not import `api`; install the orchestrator wheel in the api image so jobs run; keep check names; no shim. No conflict with a confirmed decision.

## Decisions

* Single PR, no M5a/M5b.
* Test destination divergence from the matrix (A3, A5) recorded.
