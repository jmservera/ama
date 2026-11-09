---
title: Issue 1288 E8 Agents lint correction changes and review
ms.date: 2026-11-09
---

# Issue 1288 E8 changes and review

## Changes

* `src/agents/src/zava_forward/agents/dispatch.py`: the single `with` at line 215 wrapped by `ruff format` (0.17.1) into a parenthesized two-item `with`. No behavior, config, ignore, cast or abstraction change.
* AST of the module before and after is identical (`ast.dump` equal).

## Evidence (owned SDK-free venv, editable Core plus Agents, ruff 0.17.1, mypy 2.4.0, from `src/agents`)

* Before: `ruff check .` exit 1 (E501 109>100 at line 215), `ruff format --check .` exit 1.
* After: `ruff check .` 0, `ruff format --check .` 0, `mypy` 0 (47 source files), `unittest discover -s tests -v` with `PYTHONPATH=src/core/tests`: 303 tests OK, 0 failures, no skips reported.
* Raw logs: session files `logs-1288-e8/`.

## Review (original, direct)

* Executable delta is one behavior-preserving wrap, proved by AST equality. Core/API results at the 2aa/final-target trees remain historical and reusable because no Core/API input changed.
* No findings. Remaining: real-provider route OFF, ordinary-dispatch post-fence risk, local-only cancellation, final-head SQL audit persistence unproven, whole #1288 open.

## Counters

E1-E8 spent; E9-E10 remain.
