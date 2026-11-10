---
title: Issue 135 C5 changes
date: 2026-11-10
---

Opened before the first source edit, after research, plan, details and critique (2026-11-10T04:41Z). Frozen start head `25946393`.

Planned changes: `src/importer/pyproject.toml` one mypy override. Results are filled below after implementation.

## Results

* Changed `src/importer/pyproject.toml` only: added a `[[tool.mypy.overrides]]` for `mssql_python` with `ignore_missing_imports = true`, mirroring Core. No Python or runtime change; no SQL change.
* Before (isolated venv, no driver, bare `mypy` in `src/importer`): 1 error, `__main__.py:111 import-not-found`.
* After, isolated venv (driver absent, confirmed `ModuleNotFoundError`): mypy exit 0 (12 files), `ruff check .` exit 0, `ruff format --check .` exit 0 (13 files), unittest 79 OK.
* After, driver-present venv `/tmp/issue135-c3-1110-venv`: mypy exit 0, ruff check and format exit 0, unittest 79 OK.
* Not run: SQL suites (no runtime/Core SQL change), API/Core suites (untouched), hosted CI (Root pushes and observes).
* No divergence from the plan.
