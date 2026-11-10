import argparse
import os
import sqlite3
import sys
from pathlib import Path

from zava_forward.core.exception_queue import STEWARD, ExceptionQueue
from zava_forward.core.exception_register import staff_from_env
from zava_forward.core.factory import open_store
from zava_forward.core.import_refusals import PartiallyRecordedError
from zava_forward.core.sqlstore import CommittedReloadError
from zava_forward.core.store import ConflictError

from zava_forward.importer.exceptions import RefusalLedger, route, submit_file, transfer
from zava_forward.importer.mapping import STRUCTURES, preview_file
from zava_forward.importer.quarantine import ImportError_, QuarantineStore
from zava_forward.importer.version import __version__
from zava_forward.importer.xlsx import WorkbookError


def _ensure_schema(conn: sqlite3.Connection) -> tuple[QuarantineStore, RefusalLedger]:
    store, ledger = QuarantineStore(conn), RefusalLedger(conn)
    present = {
        row[0]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    }
    if "import_batches" not in present:
        store.create_schema()
    if "import_refusals" not in present:
        ledger.create_schema()
    return store, ledger


def _database_failure(exc: sqlite3.Error, action: str) -> int:
    """Exit 2 is never a recorded refusal: the database could not be used, so nothing is claimed."""
    print(f"Cannot {action}: the database failed ({exc}). Nothing was recorded.", file=sys.stderr)
    return 2


def _close(conn: sqlite3.Connection | None) -> None:
    if conn is None:
        return
    try:
        conn.close()
    except sqlite3.Error:
        pass


def _stage(args: argparse.Namespace) -> int:
    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(args.db)
        store, ledger = _ensure_schema(conn)
        result = submit_file(store, ledger, args.file, args.staged_by, STRUCTURES[args.structure])
    except ImportError_ as exc:
        print(f"Cannot import: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        return _database_failure(exc, "stage")
    finally:
        _close(conn)
    if result.batch:
        print(f"staged batch={result.batch.batch_id} version={result.batch.version} status=staged")
        return 0
    refusal = result.refusal
    assert refusal is not None
    print(
        f"refused ref={refusal.ref} reason={refusal.reason} Nothing staged; the file is unchanged."
    )
    return 1


def _exceptions(args: argparse.Namespace) -> int:
    """Local diagnostic: shows the failed-import queue item; the served screen controls access."""
    if not args.db.is_file():
        print(f"Cannot read: {args.db} does not exist", file=sys.stderr)
        return 2
    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(f"{args.db.resolve().as_uri()}?mode=ro", uri=True)
        store, ledger = QuarantineStore(conn), RefusalLedger(conn)
        staff = staff_from_env(os.environ)
        owner = next((n for n in sorted(staff) if STEWARD in staff[n]), None)
        queue = ExceptionQueue({owner: staff[owner]} if owner else {})
        routing = route(queue, store, ledger, owner)
        items = queue.queue(owner) if owner and not routing.unrouted else []
    except sqlite3.Error as exc:
        return _database_failure(exc, "read")
    finally:
        _close(conn)
    print(
        f"local diagnostic, not access control; data={routing.data_label} "
        f"owner={routing.owner_label}"
    )
    for item in items:
        source = item["original_source"]
        print(
            f"  {item['id']} {item['kind']} ref={item.get('ref')} status={item['status']} "
            f"eligibility={item['eligibility']} source={source.get('source_name')} "
            f"sha256={source.get('source_sha256')} reason={item['error']}"
        )
    for line in routing.unrouted:
        print(f"  UNROUTED: {line}")
    print(f"  items={len(items)} Nothing was retried, approved or changed.")
    return 0


def _store_errors(kind: str) -> tuple[type[BaseException], ...]:
    """The database error type the chosen store raises when it cannot be opened."""
    if kind == "mssql":
        import mssql_python

        return (mssql_python.Error,)
    return (sqlite3.Error,)


def _stopped(message: str) -> int:
    print(f"Cannot transfer: {message}", file=sys.stderr)
    return 2


def _transfer(args: argparse.Namespace) -> int:
    """Copy refused files into the served store named by ZF_STORE, ZF_DATA and ZF_STATE."""
    if not args.db.is_file():
        print(f"Cannot read: {args.db} does not exist", file=sys.stderr)
        return 2
    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(f"{args.db.resolve().as_uri()}?mode=ro", uri=True)
        ledger = RefusalLedger(conn)
        refusals = ledger.all()
    except sqlite3.Error as exc:
        _close(conn)
        return _database_failure(exc, "read")
    open_errors: tuple[type[BaseException], ...] = (
        OSError,
        ValueError,
        SystemExit,
        *_store_errors((os.environ.get("ZF_STORE") or "json").lower()),
    )
    try:
        try:
            target = open_store(os.environ)
        except open_errors as exc:
            return _stopped(f"the served store could not be opened ({exc}). Nothing was recorded.")
        try:
            result = transfer(ledger, target)
        except ConflictError as exc:
            return _stopped(
                f"another writer changed the stored import refusals first ({exc}); this write was "
                "rolled back and nothing was recorded. Run the transfer again."
            )
        except CommittedReloadError as exc:
            return _stopped(
                f"the refusals were saved, but the refresh afterwards did not settle ({exc}). "
                "They may be recorded; run the transfer again to confirm, it adds nothing twice."
            )
        except PartiallyRecordedError as exc:
            return _stopped(f"{exc} Run the transfer again to confirm; it adds nothing twice.")
        except (OSError, ValueError) as exc:
            return _stopped(f"the served store refused it ({exc}). Nothing was recorded.")
        except getattr(target, "dberror", ()) as exc:
            return _stopped(
                f"the database failed ({exc}), so it is not known whether the refusals were "
                "recorded. Run the transfer again; it adds nothing twice."
            )
    finally:
        _close(conn)
    print(
        f"transferred added={result['added']} already_present={result['already_present']} "
        f"stored={result['total']} of ledger={len(refusals)}. Nothing was retried or approved."
    )
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(f"zava-forward-import {__version__}")
        return 0
    parser = argparse.ArgumentParser(prog="zava_forward.importer")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser(
        "preview", help="show mapping, conflicts and a row-level preview; changes nothing"
    )
    p.add_argument("file", type=Path)
    p.add_argument("--structure", default="case-list", choices=sorted(STRUCTURES))
    st = sub.add_parser(
        "stage", help="stage a clean workbook copy, or record durably why it was refused"
    )
    st.add_argument("file", type=Path)
    st.add_argument("--db", type=Path, required=True)
    st.add_argument("--staged-by", required=True)
    st.add_argument("--structure", default="case-list", choices=sorted(STRUCTURES))
    ex = sub.add_parser(
        "exceptions", help="read-only: show failed imports as steward-owned exception items"
    )
    ex.add_argument("db", type=Path)
    tr = sub.add_parser(
        "transfer", help="copy refused files from a ledger into the served store; repeat is safe"
    )
    tr.add_argument("db", type=Path)
    args = parser.parse_args(argv)
    if args.command == "stage":
        return _stage(args)
    if args.command == "exceptions":
        return _exceptions(args)
    if args.command == "transfer":
        return _transfer(args)
    try:
        prev, _ = preview_file(args.file, STRUCTURES[args.structure])
    except (WorkbookError, OSError) as exc:
        print(f"Cannot import: {exc}", file=sys.stderr)
        return 2
    print(
        f"{prev.message} source={prev.source_name} sha256={prev.source_sha256} sheet={prev.sheet}"
    )
    for c in prev.columns:
        print(f"  {c.field}: {c.header or '-'} ({c.how})")
    for text in prev.conflicts:
        print(f"  CONFLICT: {text}")
    print(f"  ready={prev.ready} to_fix={len(prev.to_fix)}")
    for r in prev.rows:
        print(f"  row {r.row}: {'OK' if not r.problems else '; '.join(r.problems)}")
    return 1 if prev.blocking else 0


sys.exit(main(sys.argv[1:]))
