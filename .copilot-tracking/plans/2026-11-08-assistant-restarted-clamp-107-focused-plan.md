---
title: Issue 107 restarted clamp focused-validation plan
description: Prospective LIGHT plan after the owner narrowed local validation, with a focused actual-SQL route for three methods
ms.date: 2026-11-08
ms.topic: reference
---

## Research (executed)

* Candidate HEAD `4b90c6d742d284d3826d0336016206b1b209d11c`, tree `b862951cac67e1fe1efbc9849be22c4c999ae731`, ignored-inclusive clean. Fetched `origin/main` `0f05e9aae70768def8d1d9c300215f9ee2f11638` is unchanged, so no new merge.
* Canonical lock `/tmp/ama-rpi-heavy.lock` is held (flock PID 1499771, issue 86 actual SQL). Nothing heavy is started here.
* The owner's 08:15 direction supersedes the earlier FULL requirement: run focused unit, static and type checks plus the actual affected SQL locally; fresh actual-head hosted CI is the broad gate. No `--all` or `--changed` run.
* The runner has no SQL-only mode (`--extra-test` runs without `ZF_TEST_MSSQL=1` and would skip). The documented focused SQL route is the component pattern: a task-owned disposable local SQL Server, `ZF_SQL_*` plus `ZF_TEST_MSSQL=1`, then `unittest` on the class, as `Runner.sql()` does in `tools/rpi-checks.py`.

## Plan

1. Commit this plan and its critique before validation.
2. LIGHT now, outputs under `/home/azureuser/.local/share/ama/gates/g107-clamp-light-r1`: reuse the existing editable venv (origin check), run the three process methods on the SQLite proxy, `ruff check`, `mypy`, `git diff --check`, source and tool blob proof against main. No new test or source edit.
3. Record the two earlier deviations unchanged (in-tree temporary mutation and `git checkout`; narrower assertions and per-wave PIDs). Originals are not regraded.
4. Planned actual SQL route, not run, only after the coordinator confirms the lock is free and then holding it for the whole container lifetime without queueing: start one owned loopback `mcr.microsoft.com/mssql/server:2022-latest` container with a generated password never logged, create database `rpi_disposable`, then from `src/api` with `PYTHONDONTWRITEBYTECODE=1`, the editable venv and `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, the mapped port, `ZF_SQL_DATABASE=rpi_disposable`, `ZF_SQL_AUTH=password`, `ZF_SQL_USER=sa`, `ZF_SQL_TRUST_CERT=1`, run `python -m unittest -v` on the three exact ids `test_assistant_release.MssqlUnleasedRevocation.<method>` for `test_restarted_processes_keep_partially_used_allowance_and_stop_at_stored_calls`, `test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance` and `test_processes_after_revocation_and_restart_are_denied_without_calls_or_replenishment`. All three must read `ok`, none skipped; remove the container afterwards. Hosted CI on the fresh head remains the broad gate and its selection and skips must be inspected.
5. Stays open: independent exact-head review, hosted CI, human approvals, whole 107 and 104, real AI and attestation.

## Corrections after critique (appended)

* The SQL run also sets `ZF_SQL_PASSWORD` (the generated password, never logged) and `PYTHONPATH=tests:../core/tests:../agents/tests` from `src/api`.
* Lock: the actual run must itself take the canonical lock non-blockingly (`flock -n`) and hold it through container removal, with removal in a `finally`/trap on failure or interruption. A coordinator statement that the lock is free is not an acquisition.
* The fixture in `test_assistants.py` creates and uses its own `zf_test_assistants` database, so the login needs create-database rights (`sa` on the disposable container) and `rpi_disposable` is only the runner's readiness database. Add driver verification (`import mssql_python`) and bounded readiness retries before the unittest.
