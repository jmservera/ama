#!/usr/bin/env python3
"""Create the contained SQL users for the workbench managed identities (idempotent).

Runs the equivalent of create-sql-users.sql with the current Azure CLI login, which must be
the SQL Entra admin, from a host the SQL firewall or private endpoint allows. The users are
created from the managed identity client id as a literal SID, so the SQL server does not need
a Directory Readers identity.

Usage: create-sql-users.py <resource-group> <sql-server-name> <database> <identity-prefix>
Example: create-sql-users.py ama sql-forward-test-rzsrg retrofit id-forward-test
Needs the mssql-python driver (src/api/requirements.txt), for example on PYTHONPATH.
"""
import json
import struct
import subprocess
import sys
import uuid

import mssql_python

GRANTS = {
    "api": ["db_datareader", "db_datawriter", "db_ddladmin"],  # ddladmin: the app creates its tables on first start
    "import": ["db_datareader", "db_datawriter"],
}


def az(*args):
    return subprocess.run(["az", *args], check=True, capture_output=True, text=True).stdout.strip()


def main(group, server, database, prefix):
    token = az("account", "get-access-token", "--resource", "https://database.windows.net/", "--query", "accessToken", "-o", "tsv")
    raw = token.encode("utf-16-le")
    attrs = {1256: struct.pack("<I", len(raw)) + raw}  # SQL_COPT_SS_ACCESS_TOKEN
    fqdn = f"{server}.database.windows.net"
    conn = mssql_python.connect(
        f"Server=tcp:{fqdn},1433;Database={database};Encrypt=yes;TrustServerCertificate=no",
        autocommit=True, attrs_before=attrs)
    cur = conn.cursor()
    for workload, roles in GRANTS.items():
        name = f"{prefix}-{workload}"
        client_id = az("identity", "show", "-g", group, "-n", name, "--query", "clientId", "-o", "tsv")
        sid = "0x" + uuid.UUID(client_id).bytes_le.hex()
        cur.execute(f"IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'{name}') "
                    f"CREATE USER [{name}] WITH SID = {sid}, TYPE = E")
        for role in roles:
            cur.execute(f"ALTER ROLE {role} ADD MEMBER [{name}]")
        print(json.dumps({"user": name, "roles": roles}))
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
