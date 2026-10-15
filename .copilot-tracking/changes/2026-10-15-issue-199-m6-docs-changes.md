---
title: Issue 199 M6 changes
ms.date: 2026-10-15
---

## Changes

* New: `src/{api,core,agents,orchestrator,importer}/README.md`; `mvp/README.md` rewritten as a pointer (only tracked file in `mvp/`).
* Repointed docs and comments; removed dead `sys.path` lines in two infra tests; removed the `mvp/README.md` rubric glob; reworded api and orchestrator exemption comments as follow-ups.
* Importer exemptions removed; others remain (follow-up).
* Matrix, reference index and log updated.

## Validation

Baseline on `main` (e019293): 747 (core 252, agents 31, orchestrator 17, importer 9, api 438; 92 skipped).

| Command | Result |
| --- | --- |
| `src/core`: `python -m unittest discover -s tests` | 252 OK |
| `src/agents` (`PYTHONPATH=../core/tests`) | 31 OK |
| `src/orchestrator` (`PYTHONPATH=../core/tests`) | 17 OK |
| `src/importer` | 9 OK; ruff check, ruff format, mypy clean without exemptions |
| `src/api` (`PYTHONPATH=../core/tests:../agents/tests`) | 438 OK (skipped=92) |
| `infra/tests` | 75 OK |
| `python tools/rename-zava-tests.py` | 25 OK |
| `.github/rubric/scripts` pytest | 13 failed, identical to `main` (pre-existing), 121 passed |
| `git ls-files mvp` | `mvp/README.md` only |

Total 747, equal to baseline. No dependency change, so no pip-compile. Docker and SQL Server are unavailable locally (socket denied); image and `mssql` jobs rely on CI.

## #200 scope check

Done: CI paths, Docker context, Bicep job commands, infra imports and tests. Remaining: `mvp-ci`/`mvp-validation` workflow names and `mvp/**` filters (rename at cut-over), `build_mvp_dataset.py` data path, `tools/rename-zava*.py` live paths, job image split (A4), `.gitignore` `/mvp/data/`.

## Follow-ups

Remove exemptions in core (~1515 findings), api (~645), agents (~122), orchestrator (31 plus 61 mypy).
