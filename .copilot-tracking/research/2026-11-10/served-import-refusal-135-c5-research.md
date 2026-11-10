---
title: Issue 135 C5 isolated Importer typing research
date: 2026-11-10
---

Research disposition: executed. Planning Readiness: Ready. Opened 2026-11-10T04:40Z at frozen head `25946393`, before any source edit.

## Evidence

* Hosted `src-importer` on PR 1357 failed at head `25946393`: `__main__.py:111: error: Cannot find implementation or library stub for module named "mssql_python" [import-not-found]`, 1 error in 12 files. Unit tests and Ruff passed. Raw log: session ROOT `1357-importer-ci-failed-1110.log`. This is preserved as failed hosted evidence.
* Reproduced exactly: a fresh venv `/tmp/issue135-c5-1110-venv` with only `./src/core` and `./src/importer` plus ruff 0.17.1 and mypy 2.4.0 (no API, no `sql` extra, no `mssql_python`), then bare `mypy` in `src/importer`, gives the same single error. C3/C4 local venvs had the optional driver installed through Core/API, which masked it.
* Cause: C3 added `import mssql_python` in `_store_errors` (`__main__.py:109-113`) to name the driver error type for the MSSQL store. Importer's mypy config skips `zava_forward.core.*` but has no override for the optional driver.
* Prior art: Core `pyproject.toml` (~line 75) has a per-module override `module = ["mssql_python"]` with `ignore_missing_imports = true`, commented as the optional SQL driver (the `sql` extra) that core CI and the isolated gate venv install without. Core code imports the driver lazily in the same style (`mssqlstore.py:243`, `lawstore.py:222`).
* Other known current-head failures: none in the supplied log.

## Options

1. Per-module override for `mssql_python` in Importer `pyproject.toml`, same as Core. Keeps MSSQL optional, no runtime change, all other imports still checked. Chosen.
2. Install the driver in Importer dev: rejected (task forbids; makes SQL mandatory).
3. Dummy stub, broad ignore, `# type: ignore`, removing the check: rejected.

Accepted limit: with the override, `mssql_python.Error` is typed `Any` when the driver is absent, and typed from the driver when present. Core's own handling is the same.
