---
title: Issue 135 C5 details
date: 2026-11-10
---

## Phase 1

Append to `src/importer/pyproject.toml` after the existing core override:

```toml
# Optional SQL driver (the sql extra); importer CI installs core without it.
[[tool.mypy.overrides]]
module = ["mssql_python"]
ignore_missing_imports = true
```

Success: bare `mypy` in an environment without the driver exits 0 with 12 files; with the driver installed it also exits 0.

## Phase 2

* Isolated venv `/tmp/issue135-c5-1110-venv`: `mypy`, `ruff check .`, `ruff format --check` on the unchanged python files, `python -m unittest discover -s tests`.
* Driver-present venv `/tmp/issue135-c3-1110-venv` (has `mssql_python`): same mypy and tests.
* Driver-absent unit coverage: the CLI MSSQL branch is only reached with a `--target` MSSQL connection; existing tests exercise the SQLite branch. No runtime change, so no SQL run is required.

## Phase 3

Fill changes record, single Review, commit with privacy-safe identity and trailer.
