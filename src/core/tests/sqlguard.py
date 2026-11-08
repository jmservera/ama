"""Admit only an endpoint the task's own disposable setup declared, before any connection or DDL."""

import hashlib
import ipaddress
import json
import os
import stat
import time
from collections.abc import Mapping

SCHEMA = "zf-task-sql/1"
MAX_AGE = 24 * 3600


def _refuse(reason: str) -> RuntimeError:
    return RuntimeError(
        f"Refusing to run SQL fixtures: {reason}. Only the disposable task-owned server created by "
        "admitted setup may be used, and it must be declared in a ZF_SQL_TASK_MANIFEST file."
    )


def write_manifest(
    path: str, host: str, port: str, password: str, created: float | None = None
) -> None:
    """Called by the admitted setup after it creates its own server with a new password.

    Only the password digest is stored, and the file is private to the current user."""
    body = dict(
        schema=SCHEMA,
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


def require_task_owned_loopback(env: Mapping[str, str]) -> None:
    """Raise before any connection unless ZF_SQL_* matches a current private task manifest.

    Loopback and password authentication are necessary but not sufficient: a shared local server or
    tunnel to a remote one passes them. The manifest binds this process to the endpoint and the
    one-time password the setup created."""
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
