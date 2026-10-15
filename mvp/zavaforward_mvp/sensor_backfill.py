"""Deterministic two-year indoor sensor backfill tied to the stock home IDs.

Wholly synthetic (ADR 0005): every row carries source_type=SYNTHETIC and a scenario label,
and nothing here is real device data. Homes and IDs come from scale_fixture.homes(), so a
series resolves to the 60,000-home register. One seed gives byte-identical output.

Outdoor climate is a labelled synthetic UK-style seasonal model. Met Office and Environment
Agency open data have not been retrieved or verified; swapping them in is an open item and
the manifest records climate_source accordingly.

    PYTHONPATH=. python3 -m zavaforward_mvp.sensor_backfill --estimate-only
    PYTHONPATH=. python3 -m zavaforward_mvp.sensor_backfill --homes 500 [--out DIR] [--seed N]
"""
import argparse
import csv
import hashlib
import io
import json
import math
import random
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import scale_fixture

VERSION = "sensor-backfill-v1"
SCHEMA_VERSION = "reading-v1"
SEED = 183
SOURCE_TYPE = "SYNTHETIC"
SCENARIO = "BACKFILL_2Y"
CLIMATE_SOURCE = "synthetic-uk-seasonal-model-v1 (Met Office/Environment Agency open data not yet retrieved)"
START = datetime(2024, 10, 1, tzinfo=timezone.utc)
DAYS = 730
CADENCE_MIN = 60
SHARD_HOMES = 1000
DWELLINGS = {"apartments": 0.7, "terrace": 1.0, "semidetached_house": 1.15, "detached": 1.3, "bungalow": 1.2}
AGE_BANDS = {"pre-1919": 1.3, "1919-1944": 1.2, "1945-1979": 1.1, "1980-2002": 0.95, "2003+": 0.8}
BOUNDS = {"temperature_c": (-10.0, 45.0), "humidity_pct": (0.0, 100.0)}
READING_FIELDS = ["sensor_id", "reading_id", "home_id", "observed_at", "temperature_c", "humidity_pct",
                  "source_type", "scenario", "seed", "schema_version", "injected_fault"]
SENSOR_FIELDS = ["sensor_id", "home_id", "dwelling_type", "age_band", "retrofitted", "heating_pattern",
                 "fault_profile", "source_type"]
SQL_DDL = """CREATE TABLE sensor_register (sensor_id VARCHAR(20) NOT NULL PRIMARY KEY, home_id VARCHAR(12) NOT NULL,
  dwelling_type VARCHAR(30), age_band VARCHAR(12), retrofitted BIT, heating_pattern VARCHAR(12),
  fault_profile VARCHAR(12), source_type VARCHAR(12) NOT NULL);
CREATE TABLE sensor_reading (sensor_id VARCHAR(20) NOT NULL, reading_id VARCHAR(40) NOT NULL, home_id VARCHAR(12) NOT NULL,
  observed_at DATETIME2(0) NOT NULL, temperature_c DECIMAL(5,2) NULL, humidity_pct DECIMAL(5,2) NULL,
  source_type VARCHAR(12) NOT NULL, scenario VARCHAR(20) NOT NULL, seed BIGINT NOT NULL, schema_version VARCHAR(12) NOT NULL,
  injected_fault VARCHAR(12) NULL, CONSTRAINT pk_sensor_reading PRIMARY KEY (sensor_id, reading_id));"""


def sensor_id(home_id):
    return "SENS-SYN-" + home_id[3:]


def sensor_for(home, seed=SEED):
    """One sensor per home; fabric attributes are a labelled synthetic draw, not an EPC record."""
    rnd = random.Random(f"{seed}-sensor-{home['id']}")
    return dict(sensor_id=sensor_id(home["id"]), home_id=home["id"],
                dwelling_type=rnd.choice(sorted(DWELLINGS)), age_band=rnd.choice(sorted(AGE_BANDS)),
                retrofitted=rnd.random() < 0.25, heating_pattern=rnd.choice(["morning_evening", "all_day", "low"]),
                fault_profile=rnd.choices(["none", "outlier", "stuck", "dropout"], [70, 12, 6, 12])[0],
                source_type=SOURCE_TYPE)


def _magnus_sat(t):
    return 6.112 * math.exp(17.62 * t / (243.12 + t))


def outdoor_series(seed=SEED, days=DAYS, cadence=CADENCE_MIN):
    """Shared synthetic outdoor (temperature, RH) per step: seasonal + diurnal + autocorrelated noise."""
    rnd = random.Random(f"{seed}-outdoor")
    steps = days * 24 * 60 // cadence
    out, noise = [], 0.0
    for k in range(steps):
        ts = START + timedelta(minutes=k * cadence)
        doy = ts.timetuple().tm_yday
        hour = ts.hour + ts.minute / 60
        noise = 0.97 * noise + rnd.gauss(0, 0.6)
        t = 10.5 - 7.0 * math.cos(2 * math.pi * (doy - 20) / 365) - 2.5 * math.cos(2 * math.pi * (hour - 3) / 24) + noise
        rh = max(35.0, min(100.0, 82 - 1.8 * (t - 10) + rnd.gauss(0, 3)))
        out.append((t, rh))
    return out


def _indoor(sensor, rnd, ts, t_out, rh_out):
    loss = DWELLINGS[sensor["dwelling_type"]] * AGE_BANDS[sensor["age_band"]] * (0.75 if sensor["retrofitted"] else 1.0)
    hour = ts.hour
    heated = {"all_day": 7 <= hour < 23, "morning_evening": 6 <= hour < 9 or 17 <= hour < 22, "low": 17 <= hour < 21}[sensor["heating_pattern"]]
    setpoint = 20.5 if heated and t_out < 15 else 17.0
    base = setpoint + min(0.0, (t_out - 5) * 0.08 * loss) + max(0.0, (t_out - 16) * 0.35)
    t_in = max(8.0, base + rnd.gauss(0, 0.3))
    vapour = _magnus_sat(t_out) * rh_out / 100 + (1.6 * loss if heated else 1.2 * loss)
    rh_in = max(15.0, min(98.0, 100 * vapour / _magnus_sat(t_in) + rnd.gauss(0, 1.5)))
    return t_in, rh_in


def readings(sensor, seed=SEED, days=DAYS, cadence=CADENCE_MIN, outdoor=None):
    outdoor = outdoor or outdoor_series(seed, days, cadence)
    rnd = random.Random(f"{seed}-series-{sensor['home_id']}")
    stuck_at, stuck = None, None
    for k, (t_out, rh_out) in enumerate(outdoor):
        ts = START + timedelta(minutes=k * cadence)
        t_in, rh_in = _indoor(sensor, rnd, ts, t_out, rh_out)
        fault, profile = "", sensor["fault_profile"]
        if profile == "dropout" and rnd.random() < 0.02:
            continue
        if profile == "outlier" and rnd.random() < 0.004:
            t_in, fault = t_in + rnd.choice([-1, 1]) * rnd.uniform(15, 30), "OUTLIER"
        elif profile == "stuck":
            if stuck_at is None and rnd.random() < 0.0005:
                stuck_at, stuck = k, (t_in, rh_in)
            if stuck_at is not None and k - stuck_at < 24 * 60 // cadence * 5:
                t_in, rh_in = stuck
                fault = "STUCK"
        yield dict(sensor_id=sensor["sensor_id"], reading_id=f"{sensor['sensor_id']}-{int(ts.timestamp())}",
                   home_id=sensor["home_id"], observed_at=ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   temperature_c=f"{t_in:.2f}", humidity_pct=f"{rh_in:.2f}", source_type=SOURCE_TYPE,
                   scenario=SCENARIO, seed=seed, schema_version=SCHEMA_VERSION, injected_fault=fault)


def _csv_line(row, fields=READING_FIELDS):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerow([row[f] for f in fields])
    return buf.getvalue()


def estimate(homes=scale_fixture.HOMES, days=DAYS, cadence=CADENCE_MIN, seed=SEED, sample_homes=20):
    """Volume and size estimate from a measured sample, computed before any full generation."""
    outdoor = outdoor_series(seed, days, cadence)
    rows = nbytes = 0
    for h in scale_fixture.homes(sample_homes, scale_fixture.SEED):
        for r in readings(sensor_for(h, seed), seed, days, cadence, outdoor):
            rows += 1
            nbytes += len(_csv_line(r).encode())
    per_row = nbytes / rows
    steps = days * 24 * 60 // cadence
    total = round(homes * steps * rows / (sample_homes * steps))
    return dict(homes=homes, days=days, cadence_minutes=cadence, readings_per_home_nominal=steps,
                estimated_rows=total, bytes_per_row_csv=round(per_row, 1),
                estimated_csv_gib=round(total * per_row / 2**30, 2),
                basis=f"measured on {sample_homes} homes; dropout faults reduce rows below nominal; SQL clustered index adds overhead")


def write(out, homes=SHARD_HOMES, seed=SEED, days=DAYS, cadence=CADENCE_MIN):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    est = estimate(homes, days, cadence, seed, sample_homes=min(20, homes))
    (out / "estimate.json").write_text(json.dumps(est, indent=2) + "\n")
    outdoor = outdoor_series(seed, days, cadence)
    digest, shards, total, sensors_rows = hashlib.sha256(), [], 0, []
    batch, shard_no = [], 0

    def flush():
        nonlocal batch, shard_no, total
        name = f"readings-{shard_no:04d}.csv"
        count = 0
        with open(out / name, "w", encoding="utf-8", newline="") as f:
            f.write(",".join(READING_FIELDS) + "\n")
            for sensor in batch:
                for r in readings(sensor, seed, days, cadence, outdoor):
                    line = _csv_line(r)
                    digest.update(line.encode())
                    f.write(line)
                    count += 1
        shards.append(dict(file=name, sensors=len(batch), rows=count))
        total += count
        shard_no += 1
        batch = []

    for h in scale_fixture.homes(homes, scale_fixture.SEED):
        s = sensor_for(h, seed)
        sensors_rows.append(s)
        batch.append(s)
        if len(batch) == SHARD_HOMES:
            flush()
    if batch:
        flush()
    with open(out / "sensors.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, SENSOR_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(sensors_rows)
    manifest = dict(version=VERSION, schema_version=SCHEMA_VERSION, seed=seed, source_type=SOURCE_TYPE, scenario=SCENARIO,
                    synthetic_label="Synthetic demonstration data under ADR 0005; not real device or resident data.",
                    climate_source=CLIMATE_SOURCE, stock_fixture_version=scale_fixture.VERSION, stock_seed=scale_fixture.SEED,
                    stock_homes_declared=scale_fixture.HOMES, homes_covered=homes, start=START.isoformat(), days=days,
                    cadence_minutes=cadence, parameters=dict(dwellings=DWELLINGS, age_bands=AGE_BANDS, bounds=BOUNDS),
                    estimate=est, rows=total, shards=shards, readings_sha256=digest.hexdigest(),
                    storage="UTF-8 CSV shards; DDL in SQL_DDL for Azure SQL; load with load_into()")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def validate_reading(row, register_ids):
    """Minimal ingestion validation contract shared with the loader (#110 consumer to reuse)."""
    if row["schema_version"] != SCHEMA_VERSION:
        return "schema_version"
    if row["sensor_id"] not in register_ids:
        return "unmapped_sensor"
    if row["source_type"] != SOURCE_TYPE:
        return "source_type"
    for key, field in (("temperature_c", "temperature_c"), ("humidity_pct", "humidity_pct")):
        try:
            v = float(row[field])
        except (TypeError, ValueError):
            return f"bad_{key}"
        lo, hi = BOUNDS[key]
        if not lo <= v <= hi:
            return f"out_of_range_{key}"
    return None


def _insert_if_absent(table, cols, keys):
    """Portable conditional insert (SQLite and Azure SQL/T-SQL); '?' placeholders, key values repeated at the end."""
    where = " AND ".join(f"{k} = ?" for k in keys)
    return (f"INSERT INTO {table} ({', '.join(cols)}) SELECT {', '.join('?' * len(cols))} "
            f"WHERE NOT EXISTS (SELECT 1 FROM {table} WHERE {where})")


def _create_sqlite_schema(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS sensor_register (sensor_id TEXT PRIMARY KEY, home_id TEXT NOT NULL, dwelling_type TEXT, "
                 "age_band TEXT, retrofitted TEXT, heating_pattern TEXT, fault_profile TEXT, source_type TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS sensor_reading (" + ", ".join(f"{f} TEXT" for f in READING_FIELDS)
                 + ", PRIMARY KEY (sensor_id, reading_id))")


def load_into(conn, out, create_schema=_create_sqlite_schema):
    """Idempotent append keyed on (sensor_id, reading_id); rejects are counted by reason, not stored.

    Uses INSERT ... WHERE NOT EXISTS so it runs on Azure SQL as well as SQLite. For Azure SQL apply SQL_DDL
    first and pass create_schema=None (the default hook creates SQLite-only DDL).
    """
    out = Path(out)
    if create_schema:
        create_schema(conn)
    with open(out / "sensors.csv", encoding="utf-8", newline="") as f:
        sensors = list(csv.DictReader(f))
    reg_sql = _insert_if_absent("sensor_register", SENSOR_FIELDS, ["sensor_id"])
    for s in sensors:
        conn.execute(reg_sql, [s[k] for k in SENSOR_FIELDS] + [s["sensor_id"]])
    ids = {s["sensor_id"] for s in sensors}
    read_sql = _insert_if_absent("sensor_reading", READING_FIELDS, ["sensor_id", "reading_id"])
    inserted, rejected = 0, {}
    for shard in sorted(out.glob("readings-*.csv")):
        with open(shard, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                reason = validate_reading(row, ids)
                if reason:
                    rejected[reason] = rejected.get(reason, 0) + 1
                    continue
                cur = conn.execute(read_sql, [row[k] for k in READING_FIELDS] + [row["sensor_id"], row["reading_id"]])
                inserted += cur.rowcount
    conn.commit()
    return dict(inserted=inserted, rejected=rejected)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data" / "sensor-backfill"))
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--homes", type=int, default=SHARD_HOMES)
    ap.add_argument("--cadence", type=int, default=CADENCE_MIN)
    ap.add_argument("--estimate-only", action="store_true")
    a = ap.parse_args(argv)
    if a.estimate_only:
        print(json.dumps(estimate(cadence=a.cadence, seed=a.seed), indent=2))
    else:
        print(json.dumps({k: v for k, v in write(a.out, a.homes, a.seed, cadence=a.cadence).items() if k != "parameters"}, indent=2))


if __name__ == "__main__":
    main()
