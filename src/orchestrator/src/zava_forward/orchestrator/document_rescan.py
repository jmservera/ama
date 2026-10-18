"""Run one explicitly configured SQL document-rescan page. No deletion or hosted timer."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys

from mssql_python import Error as MssqlError
from zava_forward.core.document_rescan import run
from zava_forward.core.documents import DocumentStoreError
from zava_forward.core.factory import open_store


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--after", nargs=2, metavar=("CASE_ID", "DOC_ID"))
    parser.add_argument(
        "--synthetic-local",
        action="store_true",
        help="explicitly allow the synthetic local test scanner, not antivirus",
    )
    args = parser.parse_args(argv)
    if (
        not os.environ.get("ZF_DATA", "").strip()
        or os.environ.get("ZF_STORE") not in ("sqlite", "mssql")
        or os.environ.get("ZF_SCANNER") not in ("local", "defender")
        or (os.environ.get("ZF_SCANNER") == "local" and not args.synthetic_local)
        or not 1 <= args.limit <= 100
        or (args.after is not None and any(not part.strip() for part in args.after))
    ):
        parser.error(
            "Set explicit ZF_DATA, ZF_STORE=sqlite|mssql and ZF_SCANNER=defender|local; "
            "local requires --synthetic-local; limit is 1..100 and cursor parts nonempty."
        )
    store = None
    try:
        store = open_store()
        result = run(
            store,
            limit=args.limit,
            after=(args.after[0], args.after[1]) if args.after is not None else None,
        )
        result["scanner"] = store.scanner.name
        print(json.dumps(result, sort_keys=True))
        if result["failed"] or result["committed"]:
            return 1
        return 2 if result["pending"] or result["next_after"] is not None else 0
    except (ValueError, TypeError, OSError, DocumentStoreError, sqlite3.Error, MssqlError):
        print(
            "DOCUMENT_RESCAN_ERROR: check configuration and persisted scan/audit.", file=sys.stderr
        )
        return 1
    finally:
        if store is not None:
            store.db.close()


if __name__ == "__main__":
    raise SystemExit(main())
