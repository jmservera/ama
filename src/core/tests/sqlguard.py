"""Refuse any SQL Server destination that is not an explicit task-owned loopback endpoint."""

import ipaddress
from collections.abc import Mapping


def require_task_owned_loopback(env: Mapping[str, str]) -> None:
    """Raise before any connection unless ZF_SQL_* names a loopback server with password auth."""
    host = (env.get("ZF_SQL_SERVER") or "").strip().strip("[]")
    if host.lower() != "localhost":
        try:
            loopback = ipaddress.ip_address(host).is_loopback
        except ValueError:
            loopback = False
        if not loopback:
            raise RuntimeError(
                "Refusing to run SQL fixtures: ZF_SQL_SERVER must be localhost or a loopback "
                "address of a disposable task-owned server."
            )
    if (env.get("ZF_SQL_AUTH") or "").lower() != "password":
        raise RuntimeError(
            "Refusing to run SQL fixtures: ZF_SQL_AUTH must be password for a disposable "
            "container, never Entra or a managed identity."
        )
