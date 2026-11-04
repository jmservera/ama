#!/usr/bin/env python3
"""One-off in-VNet job tool: synthetic sensor readings for one demo home (Refs #1072, #462).

Runs only inside the private network (the SQL server has public access Disabled) as a one-off
Container Apps job override, using the job's managed identity (`ZF_SQL_*` settings, MSI). It never
prints credentials, e-mail addresses or row bodies: only counts and synthetic identifiers.

Modes:
  inspect   counts-only: sensor tables, resident view principals, and the cases at an address.
  seed      create the stock-shaped sensor tables if absent, then load a deterministic synthetic
            window for one home from the existing sensor_backfill generator (idempotent).
  map       set `synthetic_stock_anchor_id` on exactly one named case that has no stock link.
  view      reapply infra/sql/resident-showcase.sql through resident_showcase_sql.render.
  verify    read the resident view as the resident principal (EXECUTE AS) and report counts only.
"""

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from zava_forward.core.synthetic import sensor_backfill as backfill
from zava_forward.core.synthetic import sensor_stock

HOME_ID = re.compile(r"[A-Za-z0-9._-]{3,64}")
NAME = re.compile(r"[A-Za-z0-9_-]{3,60}")


class _Loader:
    """The sqlite-shaped calls load_into makes, over the autocommit store connection."""

    def __init__(self, db):
        self.db = db

    def execute(self, sql, args=()):
        return self.db.execute(sql, args)

    def commit(self):
        return None


def connect():
    from zava_forward.core.mssqlstore import _Conn, connection_string

    env = dict(os.environ, ZF_SQL_AUTH="msi")
    if not env.get("ZF_SQL_CLIENT_ID"):
        raise SystemExit("An explicit user-assigned identity client id is required.")
    return _Conn(connection_string(env))


def emit(**fields):
    print(json.dumps(fields, sort_keys=True, default=str), flush=True)


def ddl_statements():
    parts = [s.strip() for s in backfill.STOCK_SQL_DDL.split(";") if s.strip()]
    out = []
    for stmt in parts:
        name = re.match(r"CREATE TABLE (\w+)", stmt).group(1)
        stmt = stmt.replace(f"CREATE TABLE {name}", f"CREATE TABLE dbo.{name}", 1)
        out.append(f"IF OBJECT_ID(N'dbo.{name}', N'U') IS NULL {stmt}")
    return out


def selection(home_id):
    if not HOME_ID.fullmatch(home_id):
        raise ValueError("home id must be 3 to 64 letters, digits, '.', '_' or '-'")
    row = dict(
        synthetic_home_id=home_id,
        building_form_osm="apartments",
        locality_theme="",
        is_synthetic="true",
        monitoring_consent="granted",
    )
    return sensor_stock.select([row], 1)


def generate(home_id, as_of, days, out):
    """Write the deterministic synthetic snapshot for one home; returns its selection."""
    stock = selection(home_id)
    backfill.write(out, stock=stock, seed=backfill.SEED, days=days, cadence=backfill.CADENCE_MIN, as_of=as_of)
    return stock


def seed(db, home_id, as_of, days, now=None):
    now = now or datetime.now(UTC)
    for stmt in ddl_statements():
        db.execute(stmt)
    with tempfile.TemporaryDirectory(prefix="zf-sensor-seed-") as scratch:
        out = Path(scratch) / "snapshot"
        stock = generate(home_id, as_of, days, out)
        result = backfill.load_into(_Loader(db), out, create_schema=None, stock=stock)
    # The generator window ends at the exclusive as-of date; never keep readings later than now.
    stamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    removed = db.execute(
        "DELETE FROM sensor_reading WHERE home_id = ? AND source_type = 'SYNTHETIC' AND observed_at > ?",
        (home_id, stamp),
    ).rowcount
    count, first, last = db.execute(
        "SELECT COUNT(*), CONVERT(VARCHAR(19), MIN(observed_at), 126), CONVERT(VARCHAR(19), MAX(observed_at), 126) "
        "FROM sensor_reading WHERE home_id = ? AND source_type = 'SYNTHETIC'",
        (home_id,),
    ).fetchone()
    others = db.execute("SELECT COUNT(DISTINCT home_id) FROM sensor_reading WHERE home_id <> ?", (home_id,)).fetchone()[0]
    emit(
        mode="seed",
        home_id=home_id,
        inserted=result["inserted"],
        rejected=result["rejected"],
        removed_future=removed,
        rows_for_home=count,
        first=first,
        last=last,
        other_homes_in_table=others,
    )


def inspect(db, address_like):
    tables = {}
    for name in ("sensor_register", "sensor_reading", "sensor_delivery", "sensor_data_quality_exception"):
        present = db.execute("SELECT OBJECT_ID(?, N'U')", (f"dbo.{name}",)).fetchone()[0] is not None
        tables[name] = db.execute(f"SELECT COUNT(*) FROM dbo.{name}").fetchone()[0] if present else None
    emit(mode="inspect", tables=tables, is_db_owner=db.execute("SELECT IS_MEMBER('db_owner')").fetchone()[0])
    cases = db.execute(
        "SELECT id, JSON_VALUE(body, '$.home.address'), JSON_VALUE(body, '$.home.stock_id'), "
        "JSON_VALUE(body, '$.synthetic_stock_anchor_id') FROM dbo.cases "
        "WHERE JSON_VALUE(body, '$.home.address') LIKE ?",
        (address_like,),
    ).fetchall()
    for case_id, address, stock_id, anchor in cases:
        link = stock_id or anchor
        shared = (
            db.execute(
                "SELECT COUNT(*) FROM dbo.cases WHERE COALESCE(JSON_VALUE(body, '$.home.stock_id'), "
                "JSON_VALUE(body, '$.synthetic_stock_anchor_id')) = ?",
                (link,),
            ).fetchone()[0]
            if link
            else 0
        )
        emit(mode="inspect_case", case_id=case_id, address=address, stock_id=stock_id, anchor=anchor, cases_sharing_link=shared)
    total, linked = db.execute(
        "SELECT COUNT(*), SUM(CASE WHEN COALESCE(JSON_VALUE(body, '$.home.stock_id'), "
        "JSON_VALUE(body, '$.synthetic_stock_anchor_id')) IS NULL THEN 0 ELSE 1 END) FROM dbo.cases"
    ).fetchone()
    allowed = db.execute(
        "SELECT COUNT(*), SUM(CASE WHEN revoked = 0 THEN 1 ELSE 0 END) FROM resident_showcase.allowed_case"
    ).fetchone()
    principals = [
        r[0]
        for r in db.execute(
            "SELECT DISTINCT pr.name FROM sys.database_permissions AS p "
            "JOIN sys.database_principals AS pr ON pr.principal_id = p.grantee_principal_id "
            "WHERE p.class = 1 AND p.major_id = OBJECT_ID(N'resident_showcase.v_resident_case') "
            "AND p.permission_name = N'SELECT' AND p.state IN ('G', 'W')"
        ).fetchall()
    ]
    emit(mode="inspect_totals", cases=total, cases_with_stock_link=linked, allowed_rows=allowed[0], allowed_active=allowed[1], view_select_principals=principals)


def map_case(db, case_id, home_id):
    selection(home_id)
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", case_id):
        raise ValueError("invalid case id")
    row = db.execute(
        "SELECT COALESCE(JSON_VALUE(body, '$.home.stock_id'), JSON_VALUE(body, '$.synthetic_stock_anchor_id')), "
        "ISJSON(body) FROM dbo.cases WHERE id = ?",
        (case_id,),
    ).fetchone()
    if row is None or row[1] != 1:
        raise SystemExit("Case not found or not JSON; refusing.")
    if row[0]:
        raise SystemExit("Case already has a stock link; refusing to overwrite.")
    taken = db.execute(
        "SELECT COUNT(*) FROM dbo.cases WHERE COALESCE(JSON_VALUE(body, '$.home.stock_id'), "
        "JSON_VALUE(body, '$.synthetic_stock_anchor_id')) = ?",
        (home_id,),
    ).fetchone()[0]
    if taken:
        raise SystemExit("Home id already linked to a case; refusing.")
    changed = db.execute(
        "UPDATE dbo.cases SET body = JSON_MODIFY(body, '$.synthetic_stock_anchor_id', ?) WHERE id = ?",
        (home_id, case_id),
    ).rowcount
    emit(mode="map", case_id=case_id, home_id=home_id, rows_changed=changed)


def apply_view(db, principal, client_id):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import resident_showcase_sql as showcase

    if not NAME.fullmatch(principal):
        raise ValueError("invalid principal name")
    batches = showcase.render(principal)
    cursor = db.raw.cursor()
    showcase.verify_principal(cursor, principal, client_id)
    for batch in batches:
        cursor.execute(batch)
    emit(mode="view", batches_applied=len(batches), principal=principal)


def verify(db, principal, case_id):
    if not NAME.fullmatch(principal):
        raise ValueError("invalid principal name")
    cursor = db.raw.cursor()
    cursor.execute(f"EXECUTE AS USER = N'{principal}'")
    try:
        cursor.execute(
            "SELECT case_id, sensor_home_id, (SELECT COUNT(*) FROM OPENJSON(sensors_json)), "
            "(SELECT COUNT(DISTINCT JSON_VALUE(j.value, '$.home_id')) FROM OPENJSON(sensors_json) AS j), "
            "(SELECT MIN(JSON_VALUE(j.value, '$.observed_at')) FROM OPENJSON(sensors_json) AS j), "
            "(SELECT MAX(JSON_VALUE(j.value, '$.observed_at')) FROM OPENJSON(sensors_json) AS j), "
            "(SELECT COUNT(*) FROM OPENJSON(sensors_json) AS j WHERE JSON_VALUE(j.value, '$.home_id') <> sensor_home_id "
            "OR JSON_VALUE(j.value, '$.source_type') <> 'SYNTHETIC') "
            "FROM resident_showcase.v_resident_case"
        )
        rows = [tuple(r) for r in cursor.fetchall()]
    finally:
        cursor.execute("REVERT")
    for cid, home, count, homes, first, last, mismatched in rows:
        if count or cid == case_id:
            emit(
                mode="verify_case",
                case_id=cid,
                sensor_home_id=home,
                readings_in_view=count,
                distinct_home_ids=homes,
                first=first,
                last=last,
                foreign_or_non_synthetic=mismatched,
            )
    emit(mode="verify_totals", view_rows=len(rows), rows_with_sensors=sum(1 for r in rows if r[2]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("inspect")
    p.add_argument("--address-like", default="Flat 1, Tebay Drive%")
    p = sub.add_parser("seed")
    p.add_argument("--home-id", required=True)
    p.add_argument("--as-of", required=True, help="YYYY-MM-DD exclusive UTC end of the window")
    p.add_argument("--days", type=int, default=30)
    p = sub.add_parser("map")
    p.add_argument("--case-id", required=True)
    p.add_argument("--home-id", required=True)
    p = sub.add_parser("view")
    p.add_argument("--principal", required=True)
    p.add_argument("--client-id", required=True)
    p = sub.add_parser("verify")
    p.add_argument("--principal", required=True)
    p.add_argument("--case-id", required=True)
    args = parser.parse_args(argv)
    db = connect()
    try:
        if args.mode == "inspect":
            inspect(db, args.address_like)
        elif args.mode == "seed":
            seed(db, args.home_id, args.as_of, args.days)
        elif args.mode == "map":
            map_case(db, args.case_id, args.home_id)
        elif args.mode == "view":
            apply_view(db, args.principal, args.client_id)
        else:
            verify(db, args.principal, args.case_id)
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
