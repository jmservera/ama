"""Observed controls for the resident demo image (Dockerfile.resident-demo).

Builds the exact image from the current checkout, then checks it is non-root, refuses missing,
expired and unsafe settings without echoing secrets, and starts it for real (read-only root,
all capabilities dropped, no-new-privileges, loopback bind) against a task-owned SQL Server
database with fake fixtures: health, host allowlist, a forged 401, sign-in, and sign-out.
Needs the same ZF_SQL_PORT/ZF_SQL_PASSWORD loopback container as resident_demo_browser_check.
Only the image tag and containers it creates are removed. Run from src/api.
"""

from __future__ import annotations

import base64
import http.client
import json
import os
import subprocess
import time
import uuid
from datetime import UTC, datetime, timedelta
from http.cookies import SimpleCookie

from zava_forward.core import resident_showcase as rs

from checks.resident_demo_browser_check import (
    FAKE_PASSWORD,
    ROOT,
    check,
    database,
    free_port,
    sql_settings,
)

LABEL = "ama.rpi.owner=resident-demo-image-check"
DOCKER_RUN = [
    "docker",
    "run",
    "--label",
    LABEL,
    "--read-only",
    "--cap-drop=ALL",
    "--security-opt=no-new-privileges",
    "--tmpfs=/tmp",
]


def docker(*args: str, timeout: int = 900) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", *args], capture_output=True, text=True, timeout=timeout, check=False
    )


def settings_env(db: str, port: int, expires: datetime) -> dict[str, str]:
    sql = sql_settings(db)
    return {
        "ZF_DEMO_EXPIRES_AT": expires.isoformat(),
        "ZF_DEMO_ALLOWED_HOSTS": "127.0.0.1",
        "ZF_DEMO_PASSWORD_VERIFIER": rs.make_verifier(FAKE_PASSWORD, n=2**14),
        "ZF_DEMO_SESSION_KEY": base64.urlsafe_b64encode(os.urandom(32)).decode(),
        "ZF_DEMO_BIND": "127.0.0.1",
        "PORT": str(port),
        "ZF_SQL_SERVER": sql["server"],
        "ZF_SQL_DATABASE": db,
        "ZF_SQL_AUTH": "password",
        "ZF_SQL_USER": sql["user"],
        "ZF_SQL_PASSWORD": sql["password"],
        "ZF_SQL_PORT": sql["port"],
        "ZF_SQL_TRUST_CERT": "1",
    }


def run_args(env: dict[str, str], name: str, detach: bool) -> list[str]:
    args = [*DOCKER_RUN, "--network=host", "--name", name]
    if detach:
        args.append("-d")
    for key in env:
        args += ["--env", key]
    return args


def run(
    image: str, env: dict[str, str], name: str, detach: bool
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*run_args(env, name, detach), image],
        env={**os.environ, **env},
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def call(
    port: int, method: str, path: str, headers: dict[str, str], body: bytes | None = None
) -> tuple[int, dict[str, str], bytes]:
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request(method, path, body=body, headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    cookies = {}
    for header in resp.msg.get_all("Set-Cookie") or []:
        jar: SimpleCookie = SimpleCookie()
        jar.load(header)
        cookies.update({k: m.value for k, m in jar.items()})
    status = resp.status
    conn.close()
    return status, cookies, data


def refusal(image: str, label: str, env: dict[str, str]) -> None:
    name = "resident-demo-refuse-" + uuid.uuid4().hex[:6]
    done = run(image, env, name, detach=False)
    docker("rm", "-f", name)
    output = done.stdout + done.stderr
    check(f"refuses to start: {label}", done.returncode != 0)
    secrets = [FAKE_PASSWORD, env.get("ZF_SQL_PASSWORD", "<none>")]
    check(f"refusal output for {label} echoes no secret", not any(s in output for s in secrets))


def main() -> None:
    tag = "resident-demo-image-check:" + uuid.uuid4().hex[:10]
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=False
    ).stdout.strip()
    print(f"source head {head}", flush=True)
    names: list[str] = []
    try:
        build = docker(
            "build",
            "--label",
            LABEL,
            "-f",
            str(ROOT / "src" / "api" / "Dockerfile.resident-demo"),
            "-t",
            tag,
            str(ROOT / "src"),
            timeout=1800,
        )
        check("exact Dockerfile.resident-demo image builds", build.returncode == 0)
        user = docker("image", "inspect", "--format", "{{.Config.User}}", tag).stdout.strip()
        check("image user is 10001:10001, not root", user == "10001:10001")
        with database() as db:
            expires = min(datetime.now(UTC) + timedelta(hours=1), rs.AUTHORITY_END)
            good = settings_env(db, free_port(), expires)
            refusal(tag, "no configuration", {})
            refusal(
                tag, "expired window", {**good, "ZF_DEMO_EXPIRES_AT": "2020-01-01T00:00:00+00:00"}
            )
            refusal(
                tag,
                "no password verifier",
                {k: v for k, v in good.items() if k != "ZF_DEMO_PASSWORD_VERIFIER"},
            )
            refusal(
                tag, "no session key", {k: v for k, v in good.items() if k != "ZF_DEMO_SESSION_KEY"}
            )
            refusal(
                tag,
                "no host allowlist",
                {k: v for k, v in good.items() if k != "ZF_DEMO_ALLOWED_HOSTS"},
            )
            port = free_port()
            name = "resident-demo-run-" + uuid.uuid4().hex[:6]
            names.append(name)
            env = settings_env(db, port, expires)
            started = run(tag, env, name, detach=True)
            check(
                "container starts with read-only root and no capabilities", started.returncode == 0
            )
            host = {"Host": "127.0.0.1"}
            for _ in range(60):
                try:
                    if call(port, "GET", "/healthz", host)[0] == 200:
                        break
                except OSError:
                    time.sleep(0.5)
            else:
                logs = docker("logs", name)
                raise AssertionError("container not healthy: " + logs.stderr[-400:])
            check("health answers on the allowlisted host", True)
            listening = docker("exec", name, "python", "-c", "print(1)").returncode == 0
            check("container is running", listening)
            uid = docker("exec", name, "id", "-u").stdout.strip()
            check("process runs as uid 10001", uid == "10001")
            check(
                "unlisted Host is refused",
                call(port, "GET", "/healthz", {"Host": "evil.example"})[0] >= 400,
            )
            check("view is 401 without a session", call(port, "GET", "/demo/view", host)[0] == 401)
            forged = {**host, "Cookie": "__Host-zfdemo=v1.forged.forged"}
            check("forged session is 401", call(port, "GET", "/demo/view", forged)[0] == 401)
            _, cookies, _ = call(port, "GET", "/demo/session", host)
            csrf = cookies.get("__Host-zfdemo-csrf") or next(iter(cookies.values()), "")
            jar = "; ".join(f"{k}={v}" for k, v in cookies.items())
            post = {
                **host,
                "Origin": "http://127.0.0.1",
                "Content-Type": "application/json",
                "X-CSRF-Token": csrf,
                "Cookie": jar,
            }
            bad = json.dumps({"email": "alice.demo@example.com", "password": "wrong"}).encode()
            check("wrong password is 401", call(port, "POST", "/demo/login", post, bad)[0] == 401)
            good_body = json.dumps(
                {"email": "alice.demo@example.com", "password": FAKE_PASSWORD}
            ).encode()
            status, cookies2, _ = call(port, "POST", "/demo/login", post, good_body)
            check("fake demo sign-in succeeds in the container", status == 200)
            session = {
                **host,
                "Cookie": jar + "; " + "; ".join(f"{k}={v}" for k, v in cookies2.items()),
            }
            status, _, data = call(port, "GET", "/demo/view", session)
            check(
                "signed-in view shows only the synthetic home",
                status == 200 and b"1 Alder Close" in data and b"2 Birch Close" not in data,
            )
        print("resident demo image check complete", flush=True)
    finally:
        for name in names:
            docker("rm", "-f", name)
        docker("rmi", "-f", tag)


if __name__ == "__main__":
    main()
