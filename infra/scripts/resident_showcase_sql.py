#!/usr/bin/env python3
"""Render or apply the synthetic resident showcase SQL boundary (issue 462).

Dry run is the default and prints the batches that would run, with the principal name filled in.
`--apply` connects with the current Azure CLI login, which must be the SQL Entra admin, from a
host the private endpoint allows, and creates the schema, the EMPTY allowlist table, the view and
the grants. It is a billable private-job step that stays behind the budget and approval gates; it
never inserts allowlist rows and never grants a role. `--create-principal CLIENT_ID` also creates
the contained user for a managed identity (same SID pattern as create-sql-users.py).

Usage: resident_showcase_sql.py PRINCIPAL [--create-principal CLIENT_ID] [--apply SERVER DATABASE]
Example (dry run): resident_showcase_sql.py id-cutover-test-resident-demo
Install the driver first: pip install --require-hashes -r src/api/requirements.txt.
"""

import argparse
import re
import struct
import subprocess
import sys
import uuid
from pathlib import Path

SQL_FILE = Path(__file__).resolve().parent.parent / "sql" / "resident-showcase.sql"
NAME = re.compile(r"[A-Za-z0-9_-]{3,60}")


def render(principal: str, text: str | None = None) -> list[str]:
    """Return the non-empty batches with the validated principal substituted."""
    if not NAME.fullmatch(principal):
        raise ValueError("The principal name must be 3 to 60 letters, digits, _ or -.")
    source = SQL_FILE.read_text(encoding="utf-8") if text is None else text
    batches = [b.strip() for b in re.split(r"^GO\s*$", source, flags=re.MULTILINE)]
    return [b.replace("{{PRINCIPAL}}", principal) for b in batches if b]


def principal_statement(principal: str, client_id: str) -> str:
    if not NAME.fullmatch(principal):
        raise ValueError("The principal name must be 3 to 60 letters, digits, _ or -.")
    sid = "0x" + uuid.UUID(client_id).bytes_le.hex()
    return (
        f"IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'{principal}') "
        f"CREATE USER [{principal}] WITH SID = {sid}, TYPE = E"
    )


def _token() -> str:
    return subprocess.run(
        [
            "az",
            "account",
            "get-access-token",
            "--resource",
            "https://database.windows.net/",
            "--query",
            "accessToken",
            "-o",
            "tsv",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("principal")
    parser.add_argument("--create-principal", metavar="CLIENT_ID")
    parser.add_argument("--apply", nargs=2, metavar=("SERVER", "DATABASE"))
    args = parser.parse_args(argv)
    batches = render(args.principal)
    if args.create_principal:
        batches.insert(0, principal_statement(args.principal, args.create_principal))
    if not args.apply:
        print("-- dry run: nothing executed\n" + "\nGO\n".join(batches))
        return 0
    import mssql_python

    raw = _token().encode("utf-16-le")
    attrs = {1256: struct.pack("<I", len(raw)) + raw}  # SQL_COPT_SS_ACCESS_TOKEN
    server, database = args.apply
    conn = mssql_python.connect(
        f"Server=tcp:{server}.database.windows.net,1433;Database={database};Encrypt=yes;"
        "TrustServerCertificate=no",
        autocommit=True,
        attrs_before=attrs,
    )
    cursor = conn.cursor()
    for batch in batches:
        cursor.execute(batch)
    conn.close()
    print(f"applied {len(batches)} batches for principal {args.principal}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
