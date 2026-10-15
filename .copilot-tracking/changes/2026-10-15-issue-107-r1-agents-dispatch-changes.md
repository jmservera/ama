---
title: Issue 107 R1 agents dispatch changes
ms.date: 2026-10-15
---

## Changes

* `src/core/.../assistants.py`: extracted `build_request` and `shape_result` from `Assistants.execute` (logic unchanged) and added an injectable `provider` port, defaulting to a late-bound `store.ai.evidence`.
* `src/agents/.../dispatch.py` (new): `TaskMessage`, `ResultMessage`, `AgentWorker` (bounded slots, timeout watchdog, stop event, never raises), `TaskQueue` and `ResultSink` ports, `InMemoryQueue`, `run_once`. No SQL, blob, Key Vault or secret access; the worker never approves or writes a domain record.
* `src/api/.../server.py`: `App` composes `AgentWorker(...).provider_call` as the assistants provider.
* Tests: `src/agents/tests/test_dispatch.py` (14), `src/api/tests/test_assistants_dispatch.py` (2). `src/agents/pyproject.toml` and `src/api/pyproject.toml`: mypy and ruff config for the new files.
* Docs: parity matrix (`assistants.py` and R1 rows), `docs/reference/README.md`, `docs/reference/log.md`.

## Validation (local, venv with pip only)

| Command | Result |
| --- | --- |
| baseline `src/api`: `test_assistants test_assistant_release` | 110 tests OK, 46 skipped (MSSQL) |
| `src/agents`: unittest discover | 45 OK (31 before) |
| `src/core`: unittest discover | OK |
| `src/orchestrator`: unittest discover | 17 OK |
| `src/api`: unittest discover with `PYTHONPATH=../core/tests:../agents/tests` | 438 OK, 94 skipped before the 2 composition tests; the assistants trio 112 OK after |
| `ruff check` and `ruff format --check` in core, agents, api | clean |
| `mypy` in core, agents, api | clean |
| `python3 tools/rename-zava-tests.py` | 7 errors, identical on the unchanged tree: `pptx` and `PIL` not installed (environmental) |
| local app run (sqlite store, synthetic fixture data, port 18088) | `/` 200, `/api/assistants` unauthenticated 401, no startup error |
| docker | permission denied on the socket; image and `mssql` jobs rely on CI |

## Not implemented (owner decisions or #144)

* Release approvers (`ZF_ASSIST_RELEASE_APPROVERS` unset).
* Retention of events, envelopes and quarantine digests.
* Break-glass for suspension and revocation.
* Authoritative serving attestation, Azure SQL race evidence, routine versus material change distinction, export reliance, ungated JSON dev store, delivered-build acceptance (CON-009/AC-057).
* Queue transport adapter, API post-back authentication, moving leases and fences out of the API, poison queue handling (#144).

## Divergences

The provider call is agents code but still runs in the API process until #144; #107 is not closed.
