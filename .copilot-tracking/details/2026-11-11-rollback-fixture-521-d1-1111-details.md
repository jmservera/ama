---
title: Issue 521 rollback-fixture diagnostic D1 details
ms.date: 2026-11-11
task_id: 521-rollback-d1-1111
---

## Phase 1: critique

One independent critique of the final candidate. Apply compatible findings directly; no second critique.

## Phase 2 and 3: SQL route

* Admission: `flock -n /tmp/ama-rpi-heavy.lock` held by the validation command for its full duration, with a holder probe (`flock -n` fails while held).
* Container: `docker run -d --label ama.rpi.owner=521-d1-1111 --memory=3g --cpus=2 --publish=127.0.0.1::1433 -e ACCEPT_EULA=Y -e MSSQL_PID=Developer -e MSSQL_MEMORY_LIMIT_MB=2048 -e MSSQL_SA_PASSWORD mcr.microsoft.com/mssql/server:2022-latest` with a random in-run password never written to a file. Create database `rpi_disposable`, wait for a real `SELECT 1`.
* Env: `ZF_TEST_MSSQL=1 ZF_SQL_SERVER=127.0.0.1 ZF_SQL_PORT=<port> ZF_SQL_DATABASE=rpi_disposable ZF_SQL_AUTH=password ZF_SQL_USER=sa ZF_SQL_TRUST_CERT=1`, cwd `src/core`, no `PYTHONPATH`.
* RED: `python -m unittest -v test_resident_showcase_sql.SqlBoundaryTests.test_failed_migration_rolls_back_original_check_and_leaves_no_transaction` from `src/core/tests` on the unchanged fixture.
* GREEN: same selector after the edit, then the whole module, with zero skips required for the real-SQL class.
* Source and fake-CLI units: `src/core/tests/test_resident_showcase.py`, `infra/tests/test_resident_demo_deploy.py`, `infra/tests/test_resident_demo_secrets.py`.

## Phase 3: edit

`src/core/tests/test_resident_showcase_sql.py`: import `timedelta`; in the rollback test replace `end="2028-01-01T00:00:00"` with `end=(rs.AUTHORITY_END + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S")`.

## Phase 4: static

`ruff check`, `ruff format --check`, `mypy` from `src/core` per `pyproject.toml`, on the changed file; inherited findings reported separately.

## Phase 5: documentation

Add one dated subsection to `infra/README.md` after "Live state check (2026-11-04, Refs #521)".
