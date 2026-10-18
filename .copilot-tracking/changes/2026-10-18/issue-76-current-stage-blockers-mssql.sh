#!/usr/bin/env bash
set -euo pipefail

root="$PWD"
name="ama-issue76-blockers-$$"
container=""
cleanup() {
    if [ -n "$container" ]; then
        docker rm -f "$container" >/dev/null
        echo "Removed task-owned SQL container $name"
    fi
}
trap cleanup EXIT

# Disposable localhost-only fixture credential, never an application secret.
password="Issue76-Local-Synthetic-2026!"
container=$(docker run -d --name "$name" --pull never \
    -p 127.0.0.1::1433 -e ACCEPT_EULA=Y -e MSSQL_PID=Developer \
    -e MSSQL_SA_PASSWORD="$password" mcr.microsoft.com/mssql/server:2022-latest)
port=$(docker port "$container" 1433/tcp | cut -d: -f2)
echo "Owned SQL container $name at 127.0.0.1:$port"

cd "$root/src/api"
env -i PATH="$PATH" HOME="$root/.venv" TMPDIR="$root/.venv/issue76-tmp" \
    PYTHONPATH="$root/src/core/tests:$root/src/api/tests:$root/src/agents/tests" \
    ZF_TEST_MSSQL=1 ZF_SQL_SERVER=127.0.0.1 ZF_SQL_PORT="$port" \
    ZF_SQL_DATABASE=master ZF_SQL_AUTH=password ZF_SQL_USER=sa \
    ZF_SQL_PASSWORD="$password" ZF_SQL_TRUST_CERT=1 \
    "$root/.venv/bin/python" - <<'PY'
import time
import unittest

from zava_forward.core.mssqlstore import _Conn, connection_string

for attempt in range(60):
    try:
        connection = _Conn(connection_string())
    except Exception:
        if attempt == 59:
            raise
        time.sleep(2)
    else:
        print("Actual local SQL Server responsive:", connection.execute(
            "SELECT CAST(SERVERPROPERTY('ProductVersion') AS VARCHAR(40))"
        ).fetchone()[0], flush=True)
        connection.close()
        break

suite = unittest.defaultTestLoader.loadTestsFromName("test_mssqlstore.MssqlQueueMembership")
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
PY
