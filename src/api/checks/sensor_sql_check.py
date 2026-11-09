"""Run only the constructed sensor suite against a task-owned loopback SQL Server."""

import argparse
import os
import re
import secrets
import subprocess
import sys
import time
import uuid
from pathlib import Path

DEFAULT_TESTS = (
    "test_sensor_ingestion",
    "test_sensor_consistency.SqlHandoverTests.test_composed_joint_query_statistics_and_reopened_window_replay",
    "test_sensor_consistency.WeatherContinuityTests",
    "test_sensor_consistency.LiveEnvelopeReplayTests",
    "test_sensor_consumer_live",
    "test_live_receiver_sql",
)
# Closed allowlist: each selector names fixed test targets, never caller-supplied modules.
SELECTORS = {"default": DEFAULT_TESTS, "analysis": ("test_sensor_analysis_mssql",)}
ANALYSIS_TESTS = 10


def validate(selector: str, returncode: int, output: str) -> bool:
    """Exit status alone cannot show skips: require the exact count and a clean OK."""
    if selector != "analysis":
        return returncode == 0
    return (
        returncode == 0
        and re.search(rf"^Ran {ANALYSIS_TESTS} tests? in ", output, re.MULTILINE) is not None
        and re.search(r"^OK$", output, re.MULTILINE) is not None
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selector", choices=sorted(SELECTORS), default="default")
    selector = parser.parse_args(argv).selector
    python = sys.executable
    os.environ["PATH"] = str(Path(python).parent) + os.pathsep + os.environ.get("PATH", "")
    original_env = dict(os.environ)
    import mssql_python

    root = Path(__file__).resolve().parents[3]
    name = "ama-sensor110-" + uuid.uuid4().hex[:12]
    password = "Aa1!" + secrets.token_urlsafe(24)
    env = dict(os.environ, ACCEPT_EULA="Y", MSSQL_SA_PASSWORD=password)
    started = False
    try:
        subprocess.run(
            [
                "docker",
                "run",
                "--detach",
                "--name",
                name,
                "--memory",
                "3g",
                "--cpus",
                "2",
                "-e",
                "ACCEPT_EULA",
                "-e",
                "MSSQL_SA_PASSWORD",
                "-p",
                "127.0.0.1::1433",
                "mcr.microsoft.com/mssql/server:2022-latest",
            ],
            env=env,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        started = True
        port = (
            subprocess.check_output(["docker", "port", name, "1433/tcp"], text=True)
            .strip()
            .rsplit(":", 1)[1]
        )
        connection = (
            f"Server=tcp:127.0.0.1,{port};Database=master;UID=sa;PWD={password};"
            "Encrypt=yes;TrustServerCertificate=yes;"
        )
        for _ in range(90):
            try:
                db = mssql_python.connect(connection, autocommit=True)
                db.cursor().execute("CREATE DATABASE sensor110")
                db.close()
                break
            except mssql_python.Error:
                time.sleep(2)
        else:
            print("Task-owned SQL Server unavailable; no acceptance claimed.", flush=True)
            return 1
        print(
            "Task-owned SQL Server responsive on loopback; actual API suite starting.", flush=True
        )
        test_env = dict(
            original_env,
            ZF_SENSOR_MSSQL="1",
            ZF_SQL_SERVER="127.0.0.1",
            ZF_SQL_PORT=port,
            ZF_SQL_DATABASE="sensor110",
            ZF_SQL_AUTH="password",
            ZF_SQL_USER="sa",
            ZF_SQL_PASSWORD=password,
            ZF_SQL_TRUST_CERT="1",
            PYTHONPATH=os.pathsep.join((str(root / "src/api/tests"), str(root / "src/core/tests"))),
        )
        command = [python, "-m", "unittest", *SELECTORS[selector], "-q"]
        if selector == "default":
            return subprocess.run(command, cwd=root, env=test_env, check=False).returncode
        result = subprocess.run(
            command, cwd=root, env=test_env, check=False, capture_output=True, text=True
        )
        print((result.stdout + result.stderr).replace(password, "***"), file=sys.stderr)
        accepted = validate(selector, result.returncode, result.stderr.replace(password, "***"))
        print(f"Selector {selector}: {'accepted' if accepted else 'rejected'}.", flush=True)
        return 0 if accepted else 1
    finally:
        if started:
            subprocess.run(["docker", "rm", "--force", name], check=True, stdout=subprocess.DEVNULL)
            print("Task-owned SQL container removed.", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
