#!/usr/bin/env python3
"""Dry-run or apply the permanent USD20 resident accounting boundary using Entra SQL admin."""

import argparse
import struct
from pathlib import Path

from resident_showcase_sql import _token, render, verify_principal

SQL_FILE = Path(__file__).resolve().parent.parent / "sql" / "resident-assistant.sql"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("principal")
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--apply", nargs=2, metavar=("SERVER", "DATABASE"))
    args = parser.parse_args(argv)
    batches = render(args.principal, SQL_FILE.read_text())
    if not args.apply:
        print("-- dry run: no SQL executed\n" + "\nGO\n".join(batches))
        return 0
    import mssql_python

    raw = _token().encode("utf-16-le")
    server, database = args.apply
    # Refuse connection-string injection and anything outside the existing Azure SQL service.
    import re

    if not re.fullmatch(r"[a-z0-9-]+", server) or not re.fullmatch(r"[A-Za-z0-9_-]+", database):
        raise ValueError("Use the existing Azure SQL short server and database names.")
    conn = mssql_python.connect(
        f"Server=tcp:{server}.database.windows.net,1433;Database={database};Encrypt=yes;"
        "TrustServerCertificate=no",
        autocommit=True,
        timeout=10,
        attrs_before={1256: struct.pack("<I", len(raw)) + raw},
    )
    try:
        cursor = conn.cursor()
        verify_principal(cursor, args.principal, args.client_id)
        for batch in batches:
            cursor.execute(batch)
        verify_principal(cursor, args.principal, args.client_id)
    finally:
        conn.close()
    print("Applied resident accounting schema; lifetime reservations preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
