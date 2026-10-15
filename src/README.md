---
title: Zava Forward source projects
description: Index of the isolated src projects, the dependency rule, local commands and image properties defined by ADR 0006
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

Skeleton projects created for issue #290 (ADR 0006 phase 1). They contain a version module, a `python -m` entry point that prints the version, and tests. Move-not-copy migration happens in #199: M1 moved `profile`, `rulecards` and `ai` into `core` (tests in `core/tests`, plus `agents/tests/test_ai_identity.py`). M2 moved the core hub (`store`, `sqlstore`, `mssqlstore`, `factory`, `ledger`, `continuity`, `chatthreads`, the document, finance, grants, governance, sign-off, workflow, quality, procurement, insights, projection and ranking modules, `ai_tasks`, `ai_registry`, `assistants`, `assistant_release` and `policies/ranking-v1.json`) into `core`, with the shared test fixtures in `core/tests/dataset.py` and `test_content_standard` in `api/tests`. M3 moved the synthetic tools (`scale_fixture`, `sensor_backfill`, `loadcheck`) into `core/synthetic`, `chat_fixture` into `agents/tests`, and the eval fixtures into the owning project's `evals/` folder (`core`, `agents` registry, `importer`), with their tests. M4 moved `chat_privacy`, `chat_isolation` and `recovery` into `core` (tests `test_chat_privacy`, `test_chat_memory`, `test_recovery` in `core/tests`), and `ai_eval` with `evals/ai_priority_golden.json` and `test_ai_eval` into `agents`; `test_chat_isolation` stays in `mvp/tests` until M5. The API server, web and remaining modules are still in `mvp/`. The decision record is [ADR 0006](../docs/adrs/0006-src-layout-and-cutover.md).

## Projects

| Project | Distribution | Import root | Image | Provisional core extras |
| --- | --- | --- | --- | --- |
| [core](./core/) | `zava-forward-core` | `zava_forward.core` | none | declares `sql` and `blob` |
| [api](./api/) | `zava-forward-api` | `zava_forward.api` | [Dockerfile](./api/Dockerfile) | `sql` |
| [agents](./agents/) | `zava-forward-agents` | `zava_forward.agents` | [Dockerfile](./agents/Dockerfile) | none |
| [orchestrator](./orchestrator/) | `zava-forward-orchestrator` | `zava_forward.orchestrator` | [Dockerfile](./orchestrator/Dockerfile) | `sql`, `blob` |
| [importer](./importer/) | `zava-forward-import` | `zava_forward.importer` | [Dockerfile](./importer/Dockerfile) | `blob` |

`zava_forward` is a PEP 420 namespace: there is no `__init__.py` at that level, so the five distributions install side by side. The extras column is provisional and is reassessed as modules move; the `agents` image must never install `core[sql]`, `core[blob]` or any SQL or blob client (ADR 0001 identity).

## Dependency rule

* `api`, `agents`, `orchestrator` and `importer` may import `core`.
* `api` may also import `agents` until #144 deploys `agents` as its own workload.
* No project imports `api`, and `core` imports no workload.

Each project has `tests/test_dependency_rule.py`, which parses every source and test file and fails on a forbidden `zava_forward.<project>` import.

## Commands

Run from a project folder (for example `src/agents`), in a virtual environment, with pip only:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ../core -e ".[dev]"        # api also needs -e ../agents; core needs neither
python -m unittest discover -s tests -v
ruff check . && ruff format --check . && mypy
```

Regenerate hashed requirements with `pip-compile --generate-hashes --no-emit-index-url --no-emit-trusted-host --output-file=requirements.txt requirements.in`. Pins are never loosened. `build-requirements.txt` holds the hashed build tools used only in the image build stage.

## Images

The build context is this `src/` folder, because a workload image also needs `core`:

```bash
docker build -f src/agents/Dockerfile -t zava-forward-agents:local src
```

Each image keeps the pinned base digest of `mvp/Dockerfile`, runs as user 10001, copies named packages only, contains no working data and runs with a read-only root file system. Working data is mounted at `/data` and state at `/state`; the location follows `ZF_DATA` and is never under `src/`. `src/.dockerignore` and the `/src/**/data/` entry in `.gitignore` keep data out of images and git.

## CI

[`.github/workflows/src-ci.yml`](../.github/workflows/src-ci.yml) runs the checks `src-core`, `src-api`, `src-agents`, `src-orchestrator`, `src-importer`, `src-namespace` and `src-no-working-data`. The `mvp-ci` and `mvp-validation` workflows keep their check names; they now also install `src/core` and `src/agents`, and the `mvp` image builds from the repository root (`docker build -f mvp/Dockerfile .`). Generated synthetic data defaults to the per-user `ZF_DATA` folder (`~/.zava-forward/data/` without it), never under `src/`. The files moved in M1, M2 and M3 keep their original formatting, so `core`, `api` and `agents` carry temporary ruff and mypy exemptions for them (see each `pyproject.toml`), removed in M6.
