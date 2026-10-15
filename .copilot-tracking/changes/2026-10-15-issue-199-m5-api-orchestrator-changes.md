---
title: Issue 199 M5 changes
ms.date: 2026-10-15
---

## Summary

Single pull request (no M5a/M5b): the set is about 52 renames with small edits and no dependency cycle. Nothing is left in `mvp/` except `README.md` (M6).

## Moves

* `server`, `auth`, `timecapture`, `web/**` to `src/api`; `lawstore` and `law/` to `src/core`; `digest_blob`, `token_store` to `src/orchestrator`; browser checks to `src/api/checks`; 21 tests to `src/api/tests`, 2 to `src/orchestrator/tests`.
* `Dockerfile`, `requirements.in` and `requirements.txt` merged into `src/api`; `Dockerfile.dockerignore` moved and rewritten.

## Divergences from the matrix

* All remaining tests live in `api/tests` (server harness; dependency rule), not core-tests or agents-tests (A3, A5).
* The api image installs the orchestrator wheel; Bicep job commands now use the `zava_forward.orchestrator` modules; identity retarget stays #200 (A4).
* `mvp/zavaforward_mvp/__init__.py` removed here.
* Pre-existing SQLite-dialect DDL and `INSERT OR IGNORE` translation in `timecapture` and `lawstore` is unchanged and covered by the portability tests; no new non-portable SQL was added.

## Validation (local, venv with editable installs)

| Command | Result |
| --- | --- |
| core `python -m unittest discover -s tests` | 252 OK |
| agents (PYTHONPATH `../core/tests`) | 31 OK |
| api (PYTHONPATH `../core/tests:../agents/tests`) | 438 OK, 94 skipped |
| orchestrator (PYTHONPATH `../core/tests`) | 17 OK |
| importer | 9 OK |
| infra tests | 75 OK |
| ruff check, ruff format --check, mypy in all five projects | clean |
| `node --check` app.js and assistants.js, compileall | OK |
| `git ls-files -s` web assets | 16 files, all 100644 |
| wheels and installed-server smoke test | `/healthz` 200, logo identical, leaflet 200, law register found |

Total 747 against baseline 747 (equal). The baseline `mvp` 443 plus api 8 and orchestrator 4 became api 438 and orchestrator 17 (the pre-existing 8 and 4 are a subset).

## Not run locally

* `docker build` (socket permission denied) and a SQL Server service: CI `mvp-ci` image and mssql jobs must confirm, including the per-Dockerfile ignore precedence.
