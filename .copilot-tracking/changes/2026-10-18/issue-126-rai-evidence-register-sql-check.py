"""Owned disposable SQL parity receipt runner; no configured database is used."""

import os
import secrets
import subprocess
import time
import unittest
import uuid

name = "zf-rai126-sql-" + uuid.uuid4().hex[:10]
env = dict(
    os.environ,
    ACCEPT_EULA="Y",
    MSSQL_PID="Developer",
    MSSQL_SA_PASSWORD=secrets.token_urlsafe(30) + "aA1!",
)
started = False
try:
    subprocess.run(
        [
            "docker", "run", "-d", "--name", name, "--memory", "3g",
            "-e", "ACCEPT_EULA", "-e", "MSSQL_PID", "-e", "MSSQL_SA_PASSWORD",
            "-e", "MSSQL_MEMORY_LIMIT_MB=2048", "-p", "127.0.0.1::1433",
            "mcr.microsoft.com/mssql/server:2022-latest",
        ],
        env=env, capture_output=True, text=True, check=True,
    )
    started = True
    port = subprocess.check_output(
        ["docker", "inspect", "--format",
         '{{(index (index .NetworkSettings.Ports "1433/tcp") 0).HostPort}}', name],
        text=True,
    ).strip()
    os.environ.update(
        ZF_SQL_SERVER="127.0.0.1", ZF_SQL_PORT=port, ZF_SQL_DATABASE="master",
        ZF_SQL_AUTH="password", ZF_SQL_USER="sa",
        ZF_SQL_PASSWORD=env["MSSQL_SA_PASSWORD"], ZF_SQL_TRUST_CERT="1",
        ZF_RAI126_MSSQL="1",
    )
    from zava_forward.core.mssqlstore import _Conn, connection_string

    ready = False
    for _ in range(90):
        try:
            connection = _Conn(connection_string())
            connection.execute("SELECT 1").fetchone()
            connection.close()
            ready = True
            break
        except Exception:
            time.sleep(2)
    if not ready:
        raise RuntimeError("Owned SQL readiness failed; credentials suppressed.")
    print("Actual disposable loopback SQL Server ready; UUID database per test", flush=True)
    print(subprocess.check_output(
        ["docker", "image", "inspect", "--format", "{{.Id}}",
         "mcr.microsoft.com/mssql/server:2022-latest"], text=True).strip(), flush=True)
    import test_governance

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_governance.MssqlEvidenceRegister)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(
        f"SQL parity: {result.testsRun} run; {len(result.failures)} failures; "
        f"{len(result.errors)} errors; {len(result.skipped)} skipped",
        flush=True,
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
finally:
    if started:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, check=True)
        print("Owned SQL container removed", flush=True)
