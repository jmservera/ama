"""Run only issue-owned synthetic loopback SQL; never load deployment settings."""
import os
import secrets
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path("/home/azureuser/source/ama-wt/issue-122")
NAME = "zf-122-remediation-sql-fdcaa8b0"
PASSWORD = "Zf122!" + secrets.token_hex(20)


def docker(*args):
    return subprocess.run(["docker", *args], capture_output=True, text=True, check=True)


def main():
    docker("run", "-d", "--name", NAME, "--memory=3g", "-p", "127.0.0.1::1433",
           "-e", "ACCEPT_EULA=Y", "-e", "MSSQL_PID=Developer",
           "-e", "MSSQL_SA_PASSWORD=" + PASSWORD,
           "mcr.microsoft.com/mssql/server:2022-latest")
    try:
        port = docker("port", NAME, "1433/tcp").stdout.strip().rsplit(":", 1)[1]
        env = dict(ZF_SQL_SERVER="127.0.0.1", ZF_SQL_PORT=port,
                   ZF_SQL_DATABASE="master", ZF_SQL_AUTH="password", ZF_SQL_USER="sa",
                   ZF_SQL_PASSWORD=PASSWORD, ZF_SQL_TRUST_CERT="1",
                   ZF_ISSUE122_OWNED_SQL=NAME, ZF_CONTINUITY_MSSQL="1")
        for key in list(os.environ):
            if key.startswith("ZF_SQL_"):
                del os.environ[key]
        os.environ.update(env)
        from zava_forward.core.mssqlstore import _Conn, connection_string
        deadline = time.monotonic() + 120
        while True:
            try:
                db = _Conn(connection_string(env))
                version = db.execute("SELECT CAST(SERVERPROPERTY('ProductVersion') AS varchar(30))").fetchone()[0]
                db.close()
                break
            except Exception:
                if time.monotonic() >= deadline:
                    raise RuntimeError("Owned loopback SQL did not become ready") from None
                time.sleep(2)
        print("Owned local SQL ready; version=" + version, flush=True)
        suite = unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:])
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        return 0 if result.wasSuccessful() else 1
    finally:
        docker("rm", "-f", NAME)
        print("Exact owned SQL container removed.", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
