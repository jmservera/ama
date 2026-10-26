# Issue 462 correction cycle 2 changes

Date: 2026-10-26. Base HEAD 323d955e. Plan: ../../plans/2026-10-26/resident-azure-showcase-462-correction2-plan.md

## Change

* `src/core/pyproject.toml`: added a module-scoped mypy override `mssql_python` with `ignore_missing_imports = true`, matching the existing optional-driver pattern in agents, api and importer. No runtime dependency added, no gate/allowlist change, no test change.
* Diff sha256 (git diff of pyproject): fc300b3ed02256abfbe3faecac46643ed5f95ab068f910f6c9a3d41360908ef1

## Validation (shared heavy lock, flock -n)

* Before fix: gate-2 core venv mypy from src/core: status 1, 2 import-not-found errors (reproduced).
* After fix: mypy status 0, no issues in 140 files; ruff check status 0.
* Core full unit (`python -m unittest discover -s tests`, ama462 venv): status 0. An earlier invocation with the wrong environment gave 59 errors; that was an invocation artifact, not a regression.

## Status

* Gate-2 receipt (a8492f7c...) remains FAILED and stale for any new head. It is retained unchanged.
* No pass is claimed. A fresh full gate needs coordinator capacity admission. Targeted SQL/browser/image runs on the committed source are recorded separately and are not gate coverage.
