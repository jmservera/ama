"""Sensor-only SQL access for the live receiver: connections to an already provisioned database.

`MssqlStore` creates schema, indexes, seed data, metadata and queues when it is built, which the
receiver principal neither has nor needs. This connector only validates the connection settings and
opens a connection per write; it never runs DDL, seeding, migration or any statement of its own.
"""

from collections.abc import Mapping
from typing import Any

from .mssqlstore import _Conn, connection_string


class SensorMssqlConnector:
    def __init__(self, env: Mapping[str, str]) -> None:
        self._env = env
        connection_string(env)  # settings only: no connection, no SQL

    @property
    def dberror(self) -> Any:
        import mssql_python

        return mssql_python.Error

    def assistant_connection(self) -> Any:
        return _Conn(connection_string(self._env), self._env.get("ZF_SQL_TOKEN"))
