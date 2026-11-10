---
title: Issue 1288 E8 Agents lint correction plan
ms.date: 2026-11-09
---

# Issue 1288 E8 Agents lint correction plan (prospective)

* Research: PR 1331 src-agents Lint failed E501 (109>100) at `dispatch.py` line 215 (`with call_context(context), captured_readings(...)`), introduced by this candidate. Core/API profiles do not cover the separately configured Agents package (`src/agents/pyproject.toml`: line-length 100, E/F/I/B/UP, strict mypy). CI job `src-agents`: install `-e ../core -e ".[dev]"`, `python -m unittest discover -s tests -v` with `PYTHONPATH=<ws>/src/core/tests`, `ruff check . && ruff format --check .`, `mypy`.
* Plan: wrap the single line with the pinned `ruff format` (0.17.1); no config change, ignore, cast or new abstraction. Prove AST equivalence before and after. Run the complete Agents profile and unit tests in an owned SDK-free venv.
* Counters: E8 productive correction, authorized under owner grant (issue comment 6747867150); E1-E7 spent; E9-E10 remain after this cycle.
* Limits: real-provider simulation stays OFF; no SQL, browser, push or GitHub write; Core/API results from the 2aa tree are historical and reused only with the proof that the sole executable delta is behavior-preserving wrapping.
