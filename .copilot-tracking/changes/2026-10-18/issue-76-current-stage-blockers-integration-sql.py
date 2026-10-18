"""Exercise unchanged queue and upstream recorder contracts on owned local SQL."""

import os
import secrets
import subprocess
import sys
import time
import uuid
from pathlib import Path

from zava_forward.core.mssqlstore import _Conn, connection_string

root = Path.cwd()
name = "ama-issue76-integration-" + uuid.uuid4().hex[:12]
environment = {
    "PATH": os.environ["PATH"],
    "HOME": str(root / ".venv"),
    "TMPDIR": str(root / ".venv/issue76-integration-tmp"),
    "ACCEPT_EULA": "Y",
    "MSSQL_PID": "Developer",
    "MSSQL_SA_PASSWORD": "Synthetic76!" + secrets.token_hex(20),
}
started = False
try:
    subprocess.run(
        [
            "docker", "run", "-d", "--pull", "never", "--name", name,
            "-e", "ACCEPT_EULA", "-e", "MSSQL_PID", "-e", "MSSQL_SA_PASSWORD",
            "-p", "127.0.0.1::1433", "mcr.microsoft.com/mssql/server:2022-latest",
        ],
        env=environment, check=True, stdout=subprocess.DEVNULL,
    )
    started = True
    port = subprocess.check_output(
        ["docker", "port", name, "1433/tcp"], text=True
    ).strip().rsplit(":", 1)[1]
    environment.update(
        ZF_TEST_MSSQL="1", ZF_RESIDENT_MSSQL="1",
        ZF_SQL_SERVER="127.0.0.1", ZF_SQL_PORT=port,
        ZF_SQL_DATABASE="master", ZF_SQL_AUTH="password", ZF_SQL_USER="sa",
        ZF_SQL_PASSWORD=environment["MSSQL_SA_PASSWORD"], ZF_SQL_TRUST_CERT="1",
        PYTHONPATH=":".join(str(root / p) for p in (
            "src/core/tests", "src/api/tests", "src/agents/tests",
        )),
    )
    deadline = time.monotonic() + 150
    while True:
        try:
            admin = _Conn(connection_string(environment))
        except Exception:
            if time.monotonic() >= deadline:
                raise
            time.sleep(2)
        else:
            version = admin.execute(
                "SELECT CAST(SERVERPROPERTY('ProductVersion') AS VARCHAR(40))"
            ).fetchone()[0]
            admin.close()
            print("Responsive task-owned loopback SQL Server", version, flush=True)
            break
    methods = (
        "test_decision_recorder_snapshot_is_server_derived_and_immutable",
        "test_changed_email_recorder_denied_open_and_reassignment_by_code_or_oid",
        "test_review_binding_survives_new_versions_and_retention_ordinal_reuse",
        "test_legacy_recorder_unknown_never_backfilled_or_blocks_unrelated_service",
        "test_historical_recorder_identity_projection_and_model_canary",
        "test_decision_snapshot_rechecks_registered_actor_in_writer_transaction",
    )
    result = subprocess.run(
        [
            sys.executable, "-m", "unittest",
            "test_mssqlstore.MssqlQueueMembership",
            *("test_resident_decisions.MssqlResidentControls." + m for m in methods),
            "-v",
        ],
        cwd=root / "src/api", env=environment,
    )
    raise SystemExit(result.returncode)
finally:
    if started:
        subprocess.run(
            ["docker", "rm", "-f", name], check=True, stdout=subprocess.DEVNULL
        )
        print("Removed task-owned SQL container", name, flush=True)
