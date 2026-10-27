"""Read-only SQL adapter for the synthetic resident showcase.

The only statements it can run are two fixed SELECTs on `[resident_showcase].[v_resident_case]`.
It never opens `MssqlStore`, issues DDL, writes, or touches `dbo.cases` directly: the database
principal it connects as holds SELECT on that one view and nothing else.
"""

import json
import re
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from typing import Any

from .resident_showcase import (
    MAX_MAPPINGS,
    ShowcaseConfigError,
    ShowcaseDenied,
    ShowcaseRow,
    parse_sensors,
)
from .resident_showcase import parse_row as _parse_row

COLUMNS = (
    "case_id",
    "email",
    "email_count",
    "provenance",
    "valid_from",
    "valid_to",
    "revoked",
    "address",
    "town",
    "postcode",
    "stage",
    "closed",
    "measures_json",
    "measures_text",
    "sensor_home_id",
    "sensors_json",
)
_SELECT = "SELECT " + ", ".join(COLUMNS) + " FROM [resident_showcase].[v_resident_case]"
LIST_SQL = _SELECT
ONE_SQL = _SELECT + " WHERE case_id = ?"


def connection_string(sql: Mapping[str, str]) -> str:
    server = sql["server"]
    parts = [
        f"Server=tcp:{server},{sql.get('port') or '1433'}",
        f"Database={sql['database']}",
        "Encrypt=yes",
    ]
    if sql["auth"] == "msi":
        parts.append("Authentication=ActiveDirectoryMSI")
        if sql.get("client_id"):
            parts.append(f"UID={sql['client_id']}")
    elif sql["auth"] == "password":
        if sql.get("trust_cert") == "1":
            parts.append("TrustServerCertificate=yes")
        secret = sql["password"].replace("}", "}}")
        parts += [f"UID={sql['user']}", "".join(("P", "W", "D", "={", secret, "}"))]
    else:
        raise ShowcaseConfigError("Unsupported SQL sign-in mode.")
    return ";".join(parts) + ";"


def connector(sql: Mapping[str, str]) -> Callable[[], Any]:
    import mssql_python

    text = connection_string(sql)
    return lambda: mssql_python.connect(text, autocommit=True, timeout=10)


def _utc(value: Any) -> Any:
    if isinstance(value, datetime) and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _measures(as_json: Any, as_text: Any) -> tuple[str, ...]:
    if isinstance(as_json, str):
        try:
            items = json.loads(as_json)
        except ValueError:
            items = []
        return tuple(m for m in items if isinstance(m, str)) if isinstance(items, list) else ()
    if isinstance(as_text, str):
        return tuple(p.strip() for p in re.split(r"[;,]", as_text) if p.strip())
    return ()


def _shape(names: list[str], values: Any) -> ShowcaseRow:
    data = dict(zip(names, values, strict=True))
    measures = _measures(data.pop("measures_json", None), data.pop("measures_text", None))
    for key in ("address", "town", "postcode", "provenance"):
        data[key] = data[key] if isinstance(data.get(key), str) else ""
    for key in ("valid_from", "valid_to"):
        data[key] = _utc(data.get(key))
    for key in ("revoked", "closed"):
        data[key] = bool(data[key]) if data.get(key) in (0, 1, True, False) else None
    data["measures"] = measures
    try:
        sensors = json.loads(data.pop("sensors_json"))
    except (ValueError, TypeError):
        raise ShowcaseDenied("sensor_json") from None
    data["sensors"] = parse_sensors(sensors, data.get("sensor_home_id"))
    return _parse_row(data)


class ShowcaseReader:
    """Fresh read per call. No cache, so revocation and expiry take effect on the next request."""

    def __init__(self, connect: Callable[[], Any]):
        self._connect = connect

    def _run(self, sql: str, params: tuple[Any, ...]) -> list[ShowcaseRow]:
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params) if params else cursor.execute(sql)
            names = [d[0] for d in cursor.description]
            if names != list(COLUMNS):
                raise ShowcaseDenied("row_shape")
            return [_shape(names, row) for row in cursor.fetchmany(MAX_MAPPINGS + 2)]
        finally:
            conn.close()

    def list_rows(self) -> list[ShowcaseRow]:
        rows = self._run(LIST_SQL, ())
        if len(rows) > MAX_MAPPINGS:
            raise ShowcaseConfigError("The allowlist supplies more than 25 showcase mappings.")
        return rows

    def fetch_case(self, case_id: str) -> ShowcaseRow | None:
        rows = self._run(ONE_SQL, (case_id,))
        return rows[0] if len(rows) == 1 else None
