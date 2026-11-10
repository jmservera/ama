---
title: Issue 111 parent adoption changes
ms.date: 2026-11-10
task_id: 111-parent-adoption-1855
---

## Prospective (registered before implement-start)

* One ordinary `--no-ff` merge of `feat/demo-sensor-review-109-1110` (`06374dfca`) into `feat/demo-sensor-drafts-111-1110`, plus these dated RPI records. No source line is authored by hand. No logic correction, no budget use.

## Actual changes

* `git merge --no-ff --no-commit` of the parent (`06374dfcac47cf6bcce9e7b91f573e8565ab45e8`, equal to `origin/main`, rechecked after fetch immediately before): automatic merge, 0 unmerged paths, only `server.py` auto-merged non-trivially. 497 files changed against the child. The merge is committed after review.
* `sensor_review_draft.py`, `test_sensor_review_draft.py` and `src/core/pyproject.toml` show an empty diff against `325cb5c0c`; the inherited repair and the scoped mypy stanza are intact. `pyproject.toml` parses with `tomllib`.
* No divergence, no conflict resolution, no defect found, no remaining-budget use.

## Validation (raw output in ROOT/checks-111-parent-adoption-1855/)

* Import origin: draft module and API server resolve to this worktree.
* Core draft: 65 tests, OK, 22 skipped (the opt-in MSSQL class locally; not MSSQL evidence). Analysis: 30 tests OK, 10 skipped (pre-existing opt-in). API draft: 6 OK.
* Configured Core ruff check and format check exit 0; mypy exit 0, no issues in 290 source files (scoped untyped-call exemption disclosed, not unchanged strict).
* Actual MSSQL: one non-queued `flock -n` admission, lock free, own disposable container `ama111-mssql-1855-*` on SQL Server 2022-latest, removed after; `MssqlDraftCases` ran 22, 0 skips, exit 0.
* Not run: sensor browser check, full gate, `--changed`.
* Unforced `ConflictError` and `CommittedReloadError` branches remain unproved coverage gaps.
