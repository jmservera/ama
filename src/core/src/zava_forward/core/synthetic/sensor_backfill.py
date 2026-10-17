"""Deterministic two-year indoor sensor backfill tied to the stock home IDs.

Wholly synthetic (ADR 0005): every row carries source_type=SYNTHETIC and a scenario label,
and nothing here is real device data. Homes and IDs come from scale_fixture.homes(), so a
series resolves to the 60,000-home register. One seed gives byte-identical output.

Outdoor climate is a labelled synthetic UK-style seasonal model. Met Office and Environment
Agency open data have not been retrieved or verified; swapping them in is an open item and
the manifest records climate_source accordingly.

    python3 -m zava_forward.core.synthetic.sensor_backfill --estimate-only
    python3 -m zava_forward.core.synthetic.sensor_backfill --homes 500 [--out DIR] [--seed N]
"""
import argparse
from collections.abc import Mapping
from contextlib import nullcontext
import csv
import hashlib
import io
import json
import math
import random
import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from zava_forward.core.synthetic import output_dir, provenance, scale_fixture, sensor_stock, stock_fabric, sensor_faults

VERSION = "sensor-backfill-v2"
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
STOCK_SQL_DDL = (SQL_DDL.replace("sensor_id VARCHAR(20)", "sensor_id VARCHAR(73)")
                 .replace("home_id VARCHAR(12)", "home_id NVARCHAR(128)")
                 .replace("reading_id VARCHAR(40)", "reading_id VARCHAR(96)"))


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


def outdoor_series(seed=SEED, days=DAYS, cadence=CADENCE_MIN, start=START):
    """Shared synthetic outdoor (temperature, RH) per step: seasonal + diurnal + autocorrelated noise."""
    rnd = random.Random(f"{seed}-outdoor")
    steps = days * 24 * 60 // cadence
    out, noise = [], 0.0
    for k in range(steps):
        ts = start + timedelta(minutes=k * cadence)
        doy = ts.timetuple().tm_yday
        hour = ts.hour + ts.minute / 60
        noise = 0.97 * noise + rnd.gauss(0, 0.6)
        t = 10.5 - 7.0 * math.cos(2 * math.pi * (doy - 20) / 365) - 2.5 * math.cos(2 * math.pi * (hour - 3) / 24) + noise
        rh = max(35.0, min(100.0, 82 - 1.8 * (t - 10) + rnd.gauss(0, 3)))
        out.append((t, rh))
    return out


def _indoor(sensor, rnd, ts, t_out, rh_out):
    loss = DWELLINGS[sensor["dwelling_type"]] * AGE_BANDS[sensor["age_band"]] * (0.75 if sensor["retrofitted"] else 1.0)
    loss *= sensor.get("construction_loss", 1.0)
    hour = ts.hour
    heated = {"all_day": 7 <= hour < 23, "morning_evening": 6 <= hour < 9 or 17 <= hour < 22, "low": 17 <= hour < 21}[sensor["heating_pattern"]]
    setpoint = 20.5 if heated and t_out < 15 else 17.0
    base = setpoint + min(0.0, (t_out - 5) * 0.08 * loss) + max(0.0, (t_out - 16) * 0.35)
    t_in = max(8.0, base + rnd.gauss(0, 0.3))
    vapour = _magnus_sat(t_out) * rh_out / 100 + (1.6 * loss if heated else 1.2 * loss)
    rh_in = max(15.0, min(98.0, 100 * vapour / _magnus_sat(t_in) + rnd.gauss(0, 1.5)))
    return t_in, rh_in


def readings(sensor, seed=SEED, days=DAYS, cadence=CADENCE_MIN, outdoor=None, start=START):
    outdoor = outdoor if outdoor is not None else outdoor_series(seed, days, cadence, start)
    rnd = random.Random(f"{seed}-series-{sensor['home_id']}")
    stuck_at, stuck = None, None
    for k, (t_out, rh_out) in enumerate(outdoor):
        ts = start + timedelta(minutes=k * cadence)
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
                   home_id=sensor["home_id"], observed_at=ts.isoformat(timespec="seconds").replace("+00:00", "Z"),
                   temperature_c=f"{t_in:.2f}", humidity_pct=f"{rh_in:.2f}", source_type=SOURCE_TYPE,
                   scenario=SCENARIO, seed=seed, schema_version=SCHEMA_VERSION, injected_fault=fault)


def _csv_line(row, fields=READING_FIELDS):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerow([row[f] for f in fields])
    return buf.getvalue()


def resolve_window(days: int, cadence: int, as_of: str | None = None) -> tuple[datetime, datetime]:
    """Resolve the complete UTC half-open window before writing any output."""
    if days <= 0 or cadence <= 0 or 1440 % cadence:
        raise ValueError("days must be positive; cadence must be positive and divide 1440 minutes")
    try:
        if as_of is None:
            return START, START + timedelta(days=days)
        end = datetime.combine(provenance.parse_as_of(as_of), datetime.min.time(), timezone.utc)
        return end - timedelta(days=days), end
    except OverflowError as exc:
        raise ValueError("Requested sensor window is outside supported calendar dates") from exc


def estimate(homes=None, days=DAYS, cadence=CADENCE_MIN, seed=SEED, sample_homes=20,
             start=START, *, stock: sensor_stock.Selection | None = None,
             fault_rates: Mapping[str, float] | None = None):
    """Volume and size estimate from a measured sample, computed before any full generation."""
    if stock is not None and homes is not None:
        raise ValueError("Pass homes to stock selection, not alongside a prepared selection")
    sensors = stock.sensors(seed) if stock is not None else None
    homes = len(sensors) if sensors is not None else (scale_fixture.HOMES if homes is None else homes)
    if (homes <= 0 and stock is None) or sample_homes <= 0:
        raise ValueError("homes and sample_homes must be positive")
    _, end = resolve_window(days, cadence, (start + timedelta(days=days)).date().isoformat())
    faults = sensor_faults.configure(fault_rates) if fault_rates is not None else None
    if faults is not None:
        sensor_faults.validate_window(faults, days * 1440 // cadence, end)
    outdoor = outdoor_series(seed, days, cadence, start)
    rows = nbytes = 0
    sample = (sensors[:sample_homes] if sensors is not None else
              [sensor_for(h, seed) for h in scale_fixture.homes(sample_homes, scale_fixture.SEED)])
    for sensor in sample:
        series = readings({**sensor, "fault_profile": "none"} if faults is not None else sensor,
                          seed, days, cadence, outdoor, start)
        if faults is not None:
            series = (row for packet in sensor_faults.packets(series, faults, seed, sensor["sensor_id"])
                      for row in packet.rows)
        for r in series:
            rows += 1
            nbytes += len(_csv_line(r, sensor_faults.READING_FIELDS if faults is not None else READING_FIELDS).encode())
    per_row = nbytes / rows if rows else 0.0
    steps = days * 24 * 60 // cadence
    total = round(homes * rows / len(sample)) if sample else 0
    result = dict(homes=homes, days=days, cadence_minutes=cadence, readings_per_home_nominal=steps,
                estimated_rows=total, bytes_per_row_csv=round(per_row, 1),
                estimated_csv_gib=round(total * per_row / 2**30, 2),
                basis=f"measured on {len(sample)} homes; dropout faults reduce rows below nominal; SQL clustered index adds overhead")
    if stock is not None:
        result.update(coverage=stock.coverage(), stock_input_sha256=stock.input_sha256)
    if faults is not None:
        result["basis"] = f"measured on {len(sample)} homes; variable delivered row count; SQL/index overhead excluded"
    return result


def revision_sources(*, faults: bool = False) -> tuple[Path, ...]:
    return (*scale_fixture.revision_sources(), Path(__file__), Path(sensor_stock.__file__),
            Path(stock_fabric.__file__), *((Path(sensor_faults.__file__),) if faults else ()))


def write(out: str | Path, homes: int | None = None, seed: int = SEED, days: int = DAYS,
          cadence: int = CADENCE_MIN, *, as_of: str | None = None,
          stock: sensor_stock.Selection | None = None,
          fault_rates: Mapping[str, float] | None = None) -> dict[str, object]:
    start, end = resolve_window(days, cadence, as_of)
    faults = sensor_faults.configure(fault_rates) if fault_rates is not None else None
    if faults is not None:
        sensor_faults.validate_window(faults, days * 1440 // cadence, end)
    if stock is not None and homes is not None:
        raise ValueError("Pass homes to stock selection, not alongside a prepared selection")
    sensors = stock.sensors(seed) if stock is not None else None
    homes = len(sensors) if sensors is not None else (SHARD_HOMES if homes is None else homes)
    if homes <= 0 and stock is None:
        raise ValueError("homes must be positive")
    revision = provenance.source_revision(revision_sources(faults=faults is not None))
    out = stock_fabric._destination(out) if stock is not None or faults is not None else Path(out)
    est = estimate(None if stock is not None else homes, days, cadence, seed,
                   sample_homes=max(1, min(20, homes)), start=start, stock=stock,
                   **({"fault_rates": fault_rates} if faults is not None else {}))
    out = provenance.prepare_output(out)
    truth_dir = None
    if faults is not None:
        truth_dir = out / "truth"
        truth_dir.mkdir()
        out = out / "analysis"
        out.mkdir()
    reading_fields = sensor_faults.READING_FIELDS if faults is not None else READING_FIELDS
    sensor_fields = [key for key in SENSOR_FIELDS if faults is None or key != "fault_profile"]
    (out / "estimate.json").write_text(json.dumps(est, indent=2) + "\n", encoding="utf-8", newline="\n")
    outdoor = outdoor_series(seed, days, cadence, start)
    digest, shards, total, sensors_rows = hashlib.sha256(), [], 0, []
    batch, shard_no = [], 0

    def flush():
        nonlocal batch, shard_no, total
        name = f"readings-{shard_no:04d}.csv"
        count = 0
        truth_stream = ((truth_dir / f"truth-{shard_no:04d}.jsonl").open(
            "w", encoding="utf-8", newline="\n") if truth_dir is not None else nullcontext())
        with open(out / name, "w", encoding="utf-8", newline="") as f, truth_stream as truth_file:
            f.write(",".join(reading_fields) + "\n")
            for sensor in batch:
                series = readings({**sensor, "fault_profile": "none"} if faults is not None else sensor,
                                  seed, days, cadence, outdoor, start)
                if faults is not None:
                    for packet in sensor_faults.packets(series, faults, seed, sensor["sensor_id"]):
                        truth_file.write(json.dumps(dict(
                            sensor_id=sensor["sensor_id"], packet=packet.index, label=packet.label,
                            clean=packet.clean, shard=name,
                            emitted_rows=list(range(count, count + len(packet.rows)))),
                            sort_keys=True) + "\n")
                        for r in packet.rows:
                            line = _csv_line(r, reading_fields)
                            digest.update(line.encode())
                            f.write(line)
                            count += 1
                else:
                    for r in series:
                        line = _csv_line(r)
                        digest.update(line.encode())
                        f.write(line)
                        count += 1
        shards.append(dict(file=name, sensors=len(batch), rows=count))
        total += count
        shard_no += 1
        batch = []

    source_sensors = (sensors if sensors is not None else
                      (sensor_for(h, seed) for h in scale_fixture.homes(homes, scale_fixture.SEED)))
    for s in source_sensors:
        sensors_rows.append(s)
        batch.append(s)
        if len(batch) == SHARD_HOMES:
            flush()
    if batch:
        flush()
    with open(out / "sensors.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, sensor_fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(sensors_rows)
    manifest = dict(version=VERSION, schema_version=SCHEMA_VERSION, seed=seed, as_of=end.date().isoformat(),
                    generator_revision=revision, source_type=SOURCE_TYPE, scenario=SCENARIO,
                    synthetic_label="Synthetic demonstration data under ADR 0005; not real device or resident data.",
                    climate_source=CLIMATE_SOURCE, stock_fixture_version=scale_fixture.VERSION, stock_seed=scale_fixture.SEED,
                    stock_homes_declared=scale_fixture.HOMES, homes_covered=homes, start=start.isoformat(), end_exclusive=end.isoformat(), days=days,
                    cadence_minutes=cadence, parameters=dict(dwellings=DWELLINGS, age_bands=AGE_BANDS, bounds=BOUNDS),
                    estimate=est, rows=total, shards=shards, readings_sha256=digest.hexdigest(),
                    storage="UTF-8 CSV shards; DDL in SQL_DDL for Azure SQL; load with load_into()")
    extra_files = []
    if stock is not None:
        fabric_path = out / "stock-fabric.csv"
        with fabric_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, sensor_stock.FABRIC_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(stock.fabric_rows())
        extra_files.append(fabric_path)
        manifest.update(
            version="sensor-backfill-stock-v1", stock_fixture_version=None,
            stock_seed=stock_fabric.SEED, stock_homes_declared=stock.register_homes,
            stock_input_sha256=stock.input_sha256, stock_fabric_version=stock_fabric.VERSION,
            stock_adapter_version=sensor_stock.VERSION, coverage=stock.coverage(),
            ddl_contract="stock-reading-v1", storage="Apply STOCK_SQL_DDL for a fresh SQL Server store; load_into(create_schema=None)",
            retrofit_history="Not supplied; no dated retrofit effects modelled. retrofitted=False is a model assumption, not evidence of no works.",
            monitoring="Synthetic granted fixtures only; unknown/declined excluded. No real consent or monitoring authority.",
        )
        manifest["parameters"]["construction_loss"] = sensor_stock.CONSTRUCTION_LOSS
        manifest["parameters"]["classification"] = "All projection and fault parameters are exercise values, not calibrated building physics or resident judgements."
    if faults is not None:
        manifest.update(version=sensor_faults.VERSION, schema_version=sensor_faults.SCHEMA_VERSION,
                        storage="Synthetic CSV observations with explicit units/calibration; not compatible with the legacy SQL loader")
        manifest.pop("ddl_contract", None)
        if stock is not None:
            manifest["parameters"]["classification"] = "Projection parameters are exercise values, not calibrated physics or resident judgements."
    manifest["file_sha256"] = provenance.file_hashes(
        [out / "estimate.json", out / "sensors.csv", *extra_files, *(out / shard["file"] for shard in shards)])
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    if truth_dir is not None:
        truth_manifest = dict(version=sensor_faults.VERSION, seed=seed, source_type=SOURCE_TYPE,
                              fault_rates=dict(faults.rates), rate_basis="exclusive two-observation packets; remainder valid",
                              exercise_values=sensor_faults.EXERCISE_VALUES,
                              clean="Nominal observations before injected corruption; evaluator-only",
                              emitted_rows="Zero-based CSV data row positions within the named analysis shard, excluding header",
                              analysis_manifest_sha256=hashlib.sha256((out / "manifest.json").read_bytes()).hexdigest(),
                              file_sha256=provenance.file_hashes(truth_dir.glob("truth-*.jsonl")))
        (truth_dir / "manifest.json").write_text(json.dumps(truth_manifest, indent=2) + "\n",
                                               encoding="utf-8", newline="\n")
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


def load_into(conn, out, create_schema=_create_sqlite_schema, *, stock=None, max_rows=2_000_000):
    """Admit exact current-generator synthetic bytes, then append idempotently.

    Uses INSERT ... WHERE NOT EXISTS so it runs on Azure SQL as well as SQLite. For Azure SQL apply SQL_DDL
    first and pass create_schema=None (the default hook creates SQLite-only DDL). Stock snapshots require
    the original explicit Selection. max_rows bounds replay work, not an operational sensor threshold.
    """
    with tempfile.TemporaryDirectory(prefix="zf-synthetic-replay-") as scratch:
        replay = Path(scratch) / "snapshot"
        try:
            _verify_snapshot(Path(out), replay, stock, max_rows)
        except _FaultInput:
            raise ValueError("Opt-in fault inputs require a unit/calibration-aware consumer, not load_into") from None
        except (OSError, ValueError, TypeError, KeyError, OverflowError):
            raise ValueError("Sensor admission refused: verified current synthetic snapshot required; real-use approvals remain unverified.") from None
        return _load_verified(conn, replay, create_schema)


class _FaultInput(ValueError):
    pass


def _verify_snapshot(out, replay, stock, max_rows):
    if out.is_symlink():
        raise ValueError("Unsupported sensor location")
    if (out / "analysis").is_dir():
        raise _FaultInput()
    manifest_path = out / "manifest.json"
    if manifest_path.is_symlink() or manifest_path.stat().st_size > 16_000_000:
        raise ValueError("Unsupported sensor manifest")
    metadata = json.loads(manifest_path.read_text(encoding="utf-8"))
    if isinstance(metadata, dict) and metadata.get("schema_version") == sensor_faults.SCHEMA_VERSION:
        raise _FaultInput()
    if not isinstance(metadata, dict) or metadata.get("source_type") != SOURCE_TYPE:
        raise ValueError("Synthetic source required")
    stock_mode = metadata.get("version") == "sensor-backfill-stock-v1"
    if metadata.get("version") not in (VERSION, "sensor-backfill-stock-v1") or (
        metadata.get("schema_version") != SCHEMA_VERSION
        or metadata.get("generator_revision") != provenance.source_revision(revision_sources())
        or stock_mode != isinstance(stock, sensor_stock.Selection)
        or (not stock_mode and stock is not None)
    ):
        raise ValueError("Unsupported sensor provenance")
    seed, homes, days, cadence = (metadata[k] for k in ("seed", "homes_covered", "days", "cadence_minutes"))
    if any(type(v) is not int for v in (seed, homes, days, cadence, max_rows)):
        raise ValueError("Invalid replay parameters")
    if max_rows <= 0 or homes < 0 or homes > max_rows or abs(seed) > 2**63 - 1:
        raise ValueError("Replay budget exceeded")
    resolve_window(days, cadence, metadata["as_of"])
    steps = days * 1440 // cadence
    if steps > max_rows or homes * steps > max_rows:
        raise ValueError("Replay budget exceeded")
    if stock_mode and (
        metadata.get("stock_input_sha256") != stock.input_sha256
        or metadata.get("coverage") != stock.coverage()
        or homes != sum(row["monitoring_consent"] == "granted" for row in stock.rows)
        or len(stock.rows) > max_rows
    ):
        raise ValueError("Stock selection differs")
    expected = write(replay, None if stock_mode else homes, seed, days, cadence,
                     as_of=metadata["as_of"], stock=stock)
    if metadata != json.loads(json.dumps(expected)):
        raise ValueError("Synthetic manifest differs")
    files = expected["file_sha256"]
    if {p.name for p in out.iterdir()} != {"manifest.json", *files}:
        raise ValueError("Unexpected sensor payload")
    for name, digest in files.items():
        path = out / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size != (replay / name).stat().st_size:
            raise ValueError("Sensor payload differs")
        if provenance.file_hashes([path])[name] != digest:
            raise ValueError("Sensor payload differs")


def _load_verified(conn, out, create_schema):
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
    ap.add_argument("--out", default=str(output_dir("sensor-backfill")))
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--homes", type=int)
    ap.add_argument("--register", type=Path, help="Synthetic stock CSV; requires explicit --homes subset")
    ap.add_argument("--cadence", type=int, default=CADENCE_MIN)
    ap.add_argument("--days", type=int, default=DAYS)
    ap.add_argument("--as-of", help="YYYY-MM-DD exclusive UTC end; omitted preserves the historical start")
    ap.add_argument("--estimate-only", action="store_true")
    ap.add_argument("--fault-rate", action="append", metavar="NAME=RATE",
                    help="Opt in to exclusive two-observation fault packets; repeat for each rate, remainder valid")
    a = ap.parse_args(argv)
    try:
        fault_rates = sensor_faults.parse_rates(a.fault_rate) if a.fault_rate is not None else None
        stock = sensor_stock.read_register(a.register, a.homes) if a.register else None
        homes = None if stock is not None else a.homes
        start, _ = resolve_window(a.days, a.cadence, a.as_of)
        if a.estimate_only:
            result = estimate(homes=homes, days=a.days, cadence=a.cadence, seed=a.seed,
                              sample_homes=min(20, homes) if homes else 20, start=start, stock=stock,
                              fault_rates=fault_rates)
        else:
            result = {k: v for k, v in write(a.out, homes, a.seed, days=a.days, cadence=a.cadence,
                                             as_of=a.as_of, stock=stock, fault_rates=fault_rates).items() if k != "parameters"}
    except (OSError, ValueError) as exc:
        ap.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
