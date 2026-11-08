"""Admit only an endpoint the task's own disposable setup declared, before any connection or DDL."""

import hashlib
import ipaddress
import json
import os
import re
import stat
import subprocess
import time
from collections.abc import Callable, Mapping
from datetime import datetime
from typing import Any

SCHEMA = "zf-task-sql/2"
TASK_LABEL = "1292-sql-disposable"
MAX_AGE = 24 * 3600


def _refuse(reason: str) -> RuntimeError:
    return RuntimeError(
        f"Refusing to run SQL fixtures: {reason}. Only the disposable task-owned server created by "
        "admitted setup may be used, and it must be declared in a ZF_SQL_TASK_MANIFEST file."
    )


def docker_inspect(container: str) -> dict[str, Any]:
    """Read container metadata only; the listener itself is never contacted."""
    result = subprocess.run(
        ["docker", "inspect", container], capture_output=True, text=True, timeout=30, check=True
    )
    found = json.loads(result.stdout)
    if not isinstance(found, list) or len(found) != 1 or not isinstance(found[0], dict):
        raise ValueError("unexpected docker inspect output")
    return found[0]


def write_manifest(
    path: str,
    host: str,
    port: str,
    password: str,
    container: str,
    created: float | None = None,
) -> None:
    """Called by the admitted setup after it creates its own labelled container with a new password.

    Only the password digest is stored, and the file is private to the current user. The manifest
    is a pointer: admission also needs the live container evidence checked below."""
    body = dict(
        schema=SCHEMA,
        container=container,
        host=host,
        port=str(port),
        password_sha256=hashlib.sha256(password.encode()).hexdigest(),
        created=time.time() if created is None else created,
    )
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(body, handle)


def _loopback(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _verify_container(
    container: str, port: str, password: str, inspect: Callable[[str], dict[str, Any]]
) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", container):
        raise _refuse("the manifest does not name a full container id")
    try:
        info = inspect(container)
    except Exception:
        raise _refuse("the task container cannot be inspected") from None
    if info.get("Id") != container:
        raise _refuse("the inspected container is not the one in the manifest")
    if not (info.get("State") or {}).get("Running"):
        raise _refuse("the task container is not running")
    config = info.get("Config") or {}
    if (config.get("Labels") or {}).get("zf.task") != TASK_LABEL:
        raise _refuse("the container was not created for this task")
    bindings = ((info.get("NetworkSettings") or {}).get("Ports") or {}).get("1433/tcp") or []
    if not bindings or any(b.get("HostIp") not in ("127.0.0.1", "::1") for b in bindings):
        raise _refuse("the container must publish its SQL port on loopback only")
    if not any(str(b.get("HostPort")) == port for b in bindings):
        raise _refuse("the container does not publish ZF_SQL_PORT")
    if f"MSSQL_SA_PASSWORD={password}" not in (config.get("Env") or []):
        raise _refuse("the container was not provisioned with this password")
    try:
        started = datetime.fromisoformat(
            re.sub(r"(\.\d{6})\d*Z$", r"\1+00:00", str(info["Created"]))
        )
        age = time.time() - started.timestamp()
    except (KeyError, ValueError):
        raise _refuse("the container creation time is unreadable") from None
    if age > MAX_AGE or age < -60:
        raise _refuse("the task container is not current")


def require_task_owned_loopback(
    env: Mapping[str, str], inspect: Callable[[str], dict[str, Any]] | None = None
) -> None:
    """Raise before any connection unless ZF_SQL_* names a live, labelled, task-created container.

    Loopback and password authentication are necessary but not sufficient, and a caller-written
    manifest proves nothing: a shared local server or tunnel passes both. Admission therefore reads
    the container's own metadata (label, loopback-only publish, port, provisioned password, age)
    and never connects to the listener."""
    host = (env.get("ZF_SQL_SERVER") or "").strip().strip("[]")
    if not _loopback(host):
        raise _refuse("ZF_SQL_SERVER must be localhost or a loopback address")
    if (env.get("ZF_SQL_AUTH") or "").lower() != "password":
        raise _refuse("ZF_SQL_AUTH must be password, never Entra or a managed identity")
    path = env.get("ZF_SQL_TASK_MANIFEST") or ""
    if not path:
        raise _refuse("ZF_SQL_TASK_MANIFEST is not set")
    try:
        info = os.lstat(path)
    except OSError:
        raise _refuse("the task manifest cannot be read") from None
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o022:
        raise _refuse(
            "the task manifest must be a regular file owned by this user, not writable by others"
        )
    try:
        with open(path, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, ValueError):
        raise _refuse("the task manifest is not valid JSON") from None
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        raise _refuse("the task manifest has an unknown schema")
    created = manifest.get("created")
    if (
        not isinstance(created, (int, float))
        or time.time() - created > MAX_AGE
        or created > time.time() + 60
    ):
        raise _refuse("the task manifest is not current")
    declared = str(manifest.get("host") or "").strip("[]").lower()
    if declared != host.lower():
        raise _refuse("the declared host differs from ZF_SQL_SERVER")
    if str(manifest.get("port")) != (env.get("ZF_SQL_PORT") or "1433"):
        raise _refuse("the declared port differs from ZF_SQL_PORT")
    digest = hashlib.sha256((env.get("ZF_SQL_PASSWORD") or "").encode()).hexdigest()
    if manifest.get("password_sha256") != digest:
        raise _refuse("the password is not the one generated for this task")
    _verify_container(
        str(manifest.get("container") or ""),
        env.get("ZF_SQL_PORT") or "1433",
        env.get("ZF_SQL_PASSWORD") or "",
        inspect or docker_inspect,
    )
