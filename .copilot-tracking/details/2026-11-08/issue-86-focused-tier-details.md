---
title: Issue 86 focused-tier validation details
description: Commands and evidence layout for the focused SQL run
ms.date: 2026-11-08
---

* Evidence directory (new): `/home/azureuser/.local/share/ama/gates/g86-focused-sql-1108`, with `.out`, `.err`, `.exit` per command; own venv from a whole `git archive` of HEAD, non-editable installs of core, agents and api (install only after a real missing-package failure), import-origin proof, `PYTHONDONTWRITEBYTECODE=1`.
* Lock: `flock -n /tmp/ama-rpi-heavy.lock <command>`; non-zero means blocked, no waiting.
* Container: `docker run -d --label ama.rpi.owner=g86-focused --memory=3g --cpus=2 --publish=127.0.0.1::1433 --env=ACCEPT_EULA=Y --env=MSSQL_PID=Developer --env=MSSQL_MEMORY_LIMIT_MB=2048 --env=MSSQL_SA_PASSWORD mcr.microsoft.com/mssql/server:2022-latest` with a generated throwaway password passed only by environment; readiness by `SELECT 1` against master.
* Environment: `ZF_TEST_MSSQL=1 ZF_SQL_SERVER=127.0.0.1 ZF_SQL_PORT=<mapped> ZF_SQL_DATABASE=rpi_disposable ZF_SQL_AUTH=password ZF_SQL_USER=sa ZF_SQL_TRUST_CERT=1`, `PYTHONPATH=tests:../core/tests:../agents/tests`.
* Selectors from `tools/rpi-checks.py` `SQL_SELECTORS`, `python -m unittest -v`, from `src/api`; then from `src/core` `ZF_RESIDENT_MSSQL=1 python -m unittest -v tests.test_resident_decisions.MssqlResidentControls`.
* Counts: `grep -c ' \.\.\. ok$'`, skips and failures listed by name.
