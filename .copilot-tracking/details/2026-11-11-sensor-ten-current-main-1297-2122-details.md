---
title: Sensor ten-test MSSQL current-main phase details (issue 1297, AC2)
ms.date: 2026-11-11
---

Plan: [plan](../plans/2026-11-11-sensor-ten-current-main-1297-2122-plan.md).

## Phase 2 exact procedure

1. Open `/tmp/ama-rpi-heavy.lock` and take `flock -n` exclusive (the same lock `tools/rpi-checks.py` `heavy_lock` uses); fail immediately if held. Hold it for the whole run.
2. Require `MemAvailable` of at least 5 GiB (runner rule: 4 GiB per worker plus 1 GiB headroom) and at least 2 CPUs; record load.
3. Create a unique ownership token; start `docker run -d --label ama.rpi.owner=<token> --memory=3g --cpus=2 --publish=127.0.0.1::1433` with the `ACCEPT_EULA`, `MSSQL_PID=Developer`, `MSSQL_MEMORY_LIMIT_MB=2048` and a generated random `MSSQL_SA_PASSWORD` environment, using the already present image `mcr.microsoft.com/mssql/server:2022-latest` without a registry pull.
4. Prove with `docker inspect`: full container ID, the owner label, running, exactly one `1433/tcp` binding with `HostIp` `127.0.0.1`.
5. Run the runner's `SQL_QUERY` readiness (create database `rpi_disposable`) as the runner does, with its owned environment.
6. Run with cwd `src/api`: `python3 -m unittest -v test_sensor_analysis_mssql`, `ZF_SENSOR_MSSQL=1`, `ZF_TEST_MSSQL=1`, owned `ZF_SQL_*`, and `PYTHONPATH` listing this worktree's `src/{core,agents,api}/src` first and then `src/api/tests:src/core/tests:src/agents/tests`. Print the resolved `__file__` of `mssqlstore`, `sensor_analysis_store` and the test module as source proof.
7. Parse the verbose output: exactly the ten IDs from `SENSOR_MSSQL_REQUIRED_TESTS` are `ok`, `Ran 10`, `OK`, no `skipped`.
8. Always `docker rm -f` only the recorded container ID; verify absence with `docker ps -a` for the label and by ID.

Deviation from the canonical runner, recorded openly: no fresh venv and no `docker pull`; the host Python and the cached image are used, and source identity is proven by import paths.
