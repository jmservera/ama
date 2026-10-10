"""Existing generated stock and programme lineage, separate from test fixtures."""
import csv
import hashlib
import json
import math
from copy import deepcopy

from . import projection

SOURCE_KEYS = ("stock_sha256", "programme_sha256", "stock_count", "case_count", "built")


def workbench_metadata(case, source):
    """Add bounded review capabilities without rewriting generated case history."""
    from . import exercise
    cid = case["id"]
    contract = deepcopy(exercise.manifest()["lead_contract"])
    contract.update(contractor=case["contractor"]["name"],
                    status="Selected EXA simulation assumptions, not imported contractual approval")
    return dict(fixture_version="properwarm-programme-1", as_of=source["built"], fictional=True,
        population="story", property_register_id=cid, building_id=f"unverified-building:{cid}",
        stock_link_status="Unverified; shared map anchors do not establish property identity",
        field_authority_version="programme-field-authority-1", lifecycle="Intake",
        lifecycle_note="New bounded review workflow; original generated stage/history remain unchanged.",
        scheme=dict(id="proper-warm-exercise-fund", version="exercise-fund-1"),
        contract=contract, source_candidates=[], unknowns=["Stock identity linkage", "Current independent approvals"],
        source_lineage=source, evidence=[
            dict(id=f"{cid}-IDENTITY", version=source["programme_sha256"], authority="technical",
                 media_type="text/plain", raw_text=f'home_ids: ["{cid}"]\n',
                 field_ids=["home_ids"], by="Existing synthetic MVP snapshot", at=source["built"]),
            dict(id=f"{cid}-EPC", version=source["programme_sha256"], authority="survey",
                 media_type="text/plain", raw_text=f"epc_band: {case['home']['epc']}\n",
                 field_ids=["epc_band"], by="Existing generated home.epc; not an EPC certificate", at=source["built"]),
            dict(id=f"{cid}-SCOPE", version=source["programme_sha256"], authority="technical",
                 media_type="text/plain", raw_text=f"narrative: Synthetic planned measures: {case['measures']}\n",
                 field_ids=["narrative"], by="Existing generated measures; not approved design", at=source["built"]),
            dict(id=f"{cid}-FUND", version="exercise-fund-1", authority="funding",
                 media_type="text/plain",
                 raw_text=f"narrative: Synthetic planned measures: {case['measures']}\n",
                 field_ids=["narrative"],
                 by="Owner-selected EXA-015 fictional fund route; no eligibility, award or cash evidence",
                 at=source["built"]),
        ])


def import_stock(store, path, programme_sha256, built):
    """Operator-only atomic import; refuse replacing a different stock version."""
    with open(path, "rb") as source:
        stock_hash = hashlib.sha256(source.read()).hexdigest()
    with open(path, encoding="utf-8-sig", newline="") as source:
        records = list(csv.DictReader(source))
    if len(records) != 60000 or len({r["synthetic_home_id"] for r in records}) != 60000:
        raise ValueError("The existing stock must contain exactly 60000 distinct home IDs.")
    rows = []
    for record in records:
        latitude, longitude = float(record["latitude"]), float(record["longitude"])
        if not (math.isfinite(latitude) and math.isfinite(longitude)
                and -90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("Stock contains an invalid coordinate; nothing imported.")
        if record["is_synthetic"].lower() != "true":
            raise ValueError("Stock must be explicitly synthetic; nothing imported.")
        rows.append((record["synthetic_home_id"], record["local_authority"],
                     record["epc_need_group_model"], record["map_address"], latitude, longitude,
                     json.dumps(record)))
    with store.dblock:
        store.db.execute("BEGIN IMMEDIATE")
        try:
            existing = store.db.execute("SELECT value FROM meta WHERE key='programme_source'").fetchone()
            source = dict(stock_sha256=stock_hash, programme_sha256=programme_sha256,
                          stock_count=60000, case_count=980, built=built)
            count = store.db.execute("SELECT COUNT(*) FROM stock").fetchone()[0]
            if existing:
                if json.loads(existing[0]) != source or count != 60000:
                    raise ValueError("Existing stock lineage differs; no overwrite permitted.")
            else:
                if count or store.db.execute("SELECT COUNT(*) FROM cases").fetchone()[0] != 980:
                    raise ValueError("Expected empty stock and the retained 980-case programme.")
                store.db.executemany(
                    "INSERT INTO stock (id, area, epc_group, address, lat, lon, body) VALUES (?,?,?,?,?,?,?)",
                    rows)
                store._meta_set("programme_source", json.dumps(source))
            store.db.execute("COMMIT")
        except BaseException:
            store.db.execute("ROLLBACK")
            raise
    return source


def source_metadata(store):
    with store.dblock:
        row = store.db.execute("SELECT value FROM meta WHERE key='programme_source'").fetchone()
        if row is None:
            raise ValueError("Generated programme stock has not been imported.")
        return json.loads(row[0])


def _where(query):
    parts, values = [], []
    for key, column in (("area", "area"), ("epc_group", "epc_group")):
        if query.get(key):
            parts.append(f"{column}=?")
            values.append(query[key])
    if query.get("q"):
        text = query["q"]
        if len(text) > 200:
            raise ValueError("Stock search is limited to 200 characters.")
        text = text.replace("!", "!!").replace("%", "!%").replace("_", "!_").replace("[", "![")
        parts.append("(address LIKE ? ESCAPE '!' OR id LIKE ? ESCAPE '!')")
        values.extend((f"%{text}%", f"%{text}%"))
    return (" WHERE " + " AND ".join(parts) if parts else ""), values


def page_stock(store, user, query, limit=50, offset=0, zoom=6):
    """Return one SQL page and aggregate map of exactly the same stock filter."""
    if user.get("role") not in projection.STAFF_ROLES:
        raise PermissionError("Full stock is restricted to programme staff.")
    if not 1 <= limit <= 100 or not 0 <= offset <= 60000 or not 4 <= zoom <= 12:
        raise ValueError("Invalid stock page or map zoom.")
    where, values = _where(query)
    scale = 2 ** (zoom - 3)
    with store.dblock:
        source = source_metadata(store)
        total = store.db.execute("SELECT COUNT(*) FROM stock" + where, values).fetchone()[0]
        if hasattr(store, "_env"):
            sql = "SELECT body FROM stock" + where + " ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
            args = [*values, offset, limit]
        else:
            sql = "SELECT body FROM stock" + where + " ORDER BY id LIMIT ? OFFSET ?"
            args = [*values, limit, offset]
        records = [json.loads(row[0]) for row in store.db.execute(sql, args).fetchall()]
        clusters = store.db.execute(
            "SELECT x,y,COUNT(*),AVG(lat),AVG(lon) FROM "
            "(SELECT CAST(lat*? AS INT) AS x,CAST(lon*? AS INT) AS y,lat,lon FROM stock"
            + where + ") AS points GROUP BY x,y",
            [scale, scale, *values]).fetchall()
        areas = [row[0] for row in store.db.execute("SELECT DISTINCT area FROM stock ORDER BY area").fetchall()]
        groups = [row[0] for row in store.db.execute("SELECT DISTINCT epc_group FROM stock ORDER BY epc_group").fetchall()]
    if sum(row[2] for row in clusters) != total:
        raise ValueError("Stock list/map reconciliation failed.")
    return dict(source=source, total=total, limit=limit, offset=offset, records=records,
                areas=areas, epc_groups=groups,
                clusters=[dict(count=row[2], lat=row[3], lon=row[4]) for row in clusters],
                note="Real OpenStreetMap anchors; synthetic tenure/EPC/occupancy. No verified landlord or occupier. "
                     "Programme case linkage is not established by proximity or a shared map anchor.")


def main():
    """Explicit operator import; source data is never packaged in the image."""
    import argparse
    import os
    from .mssqlstore import MssqlStore

    parser = argparse.ArgumentParser(description="Import existing scripted MVP data into a dedicated Azure SQL database.")
    parser.add_argument("--stock", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--state", required=True)
    args = parser.parse_args()
    with open(args.data, "rb") as stream:
        raw = stream.read()
    snapshot = json.loads(raw)
    if len(snapshot["cases"]) != 980 or len({c["id"] for c in snapshot["cases"]}) != 980:
        raise ValueError("Expected the existing 980-case snapshot.")
    store = MssqlStore(args.data, env=os.environ, state_dir=args.state)
    try:
        source = import_stock(store, args.stock, hashlib.sha256(raw).hexdigest(), snapshot["built"])
        with store.lock:
            for cid, case in store.cases.items():
                if not case.get("exercise"):
                    store._touch(cid)
                    case["exercise"] = workbench_metadata(case, source)
            store.save()
        print(json.dumps(dict(source=source, cases=len(store.cases), audit=store.verify_ledger())))
    finally:
        store.db.raw.close()


if __name__ == "__main__":
    main()
