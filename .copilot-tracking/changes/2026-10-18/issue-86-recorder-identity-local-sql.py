"""Run existing resident contracts on a uniquely owned loopback SQL container."""

import os
import secrets
import subprocess
import sys
import time
import uuid
from pathlib import Path

from zava_forward.core.mssqlstore import _Conn, connection_string

root = Path(__file__).resolve().parents[3]
name = "issue86-recorder-" + uuid.uuid4().hex[:12]
environment = {
    "PATH": os.environ["PATH"],
    "HOME": "/tmp",
    "ACCEPT_EULA": "Y",
    "MSSQL_PID": "Developer",
    "MSSQL_SA_PASSWORD": "Syn86!" + secrets.token_hex(20),
}
started = False
try:
    subprocess.run(
        [
            "docker", "run", "-d", "--name", name,
            "-e", "ACCEPT_EULA", "-e", "MSSQL_PID", "-e", "MSSQL_SA_PASSWORD",
            "-p", "127.0.0.1::1433",
            "mcr.microsoft.com/mssql/server:2022-latest",
        ],
        env=environment, check=True, stdout=subprocess.DEVNULL,
    )
    started = True
    port = subprocess.check_output(
        ["docker", "port", name, "1433/tcp"], text=True
    ).strip().rsplit(":", 1)[1]
    environment.update(
        ZF_RESIDENT_MSSQL="1",
        ZF_SQL_SERVER="127.0.0.1",
        ZF_SQL_PORT=port,
        ZF_SQL_DATABASE="master",
        ZF_SQL_AUTH="password",
        ZF_SQL_USER="sa",
        ZF_SQL_PASSWORD=environment["MSSQL_SA_PASSWORD"],
        ZF_SQL_TRUST_CERT="1",
        PYTHONPATH="tests",
    )
    deadline = time.monotonic() + 150
    while True:
        try:
            admin = _Conn(connection_string(environment))
            row = admin.execute("SELECT 1").fetchone()
            admin.close()
            assert row == (1,)
            break
        except Exception:
            if time.monotonic() >= deadline:
                raise
            time.sleep(3)
    print("Task-owned loopback SQL Server ready; existing UUID fixture databases only.", flush=True)
    result = subprocess.run(
        [
            sys.executable, "-m", "unittest",
            "test_resident_decisions.MssqlResidentControls", "-q",
        ],
        cwd=root / "src/core", env=environment,
    )
    raise SystemExit(result.returncode)
finally:
    if started:
        subprocess.run(["docker", "rm", "-f", name], check=True, stdout=subprocess.DEVNULL)
        print("Task-owned SQL container removed; no idle service or volume retained.", flush=True)
