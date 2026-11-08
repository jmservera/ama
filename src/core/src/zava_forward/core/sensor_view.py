"""Bounded retained reading read model for employees and Quality evidence (issue 1288).

Read only. It selects from the retained `sensor_reading` rows admitted by the sensor consumer,
never generates values, never reads weather as an indoor observation, never invents variables and
never queries unbounded history. The same `capture_source` output feeds the employee view and the
quality-evidence snapshot, so the reading ids and values a person sees (the latest included) are the
ones the model request carries. The capture holds no clock value, so unchanged evidence keeps one
digest. Values are withheld unless the sensors' recorded monitoring consent is granted.
"""

import json
from datetime import UTC, datetime

from .synthetic.sensor_identity import home_key, sensor_key

VERSION = "retained-reading-view-v2"
KIND = "synthetic-retained-readings"
UNITS = dict(temperature_c="degC", humidity_pct="%RH")
WINDOW_MAX = 12
CONTEXT_MAX = 4
SEAL_SECONDS = 21600
FRESH_SECONDS = 900
STAMP = "%Y-%m-%dT%H:%M:%SZ"
COLUMNS = (
    "reading_id",
    "sensor_id",
    "observed_at",
    "temperature_c",
    "humidity_pct",
    "scenario",
    "schema_version",
)
STATES = ("ok", "no-readings", "consent-withheld", "unavailable")
MANUAL = "Use the ordinary quality check; no one is waiting on sensor values."
CALIBRATION = "Not calibrated. These values are not a verified indoor measurement."
CLASSES = {
    "synthetic-weather-derived": "Synthetic simulator reading derived from outdoor weather. "
    + CALIBRATION,
    "synthetic-modelled-indoor": "Synthetic modelled indoor reading. " + CALIBRATION,
    "synthetic-unclassified": "Synthetic reading of unknown origin. " + CALIBRATION,
}
RETROFIT = dict(
    available=False,
    text=(
        "No installation date or marker is recorded, so no before or after retrofit "
        "comparison is made."
    ),
)
ANCHOR_NAME = "quality_record_anchor"
ANCHOR_MEANING = (
    "Time of the first active quality evidence record. It is not an installation date and "
    "readings around it are not a retrofit effect."
)


def _utc(epoch):
    return datetime.fromtimestamp(epoch, UTC)


def _text(value):
    return value.strftime(STAMP)


def parse_reference(value):
    """UTC instant of a quality record, or None when it is missing or unreadable."""
    try:
        stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return (
        (stamp if stamp.tzinfo else stamp.replace(tzinfo=UTC))
        .astimezone(UTC)
        .replace(microsecond=0)
    )


def reference_for(quality_records):
    """First active quality evidence record time. It is not an installation date."""
    stamps = [
        parse_reference(r.get("recorded_at"))
        for r in quality_records or []
        if r.get("state") != "Superseded"
    ]
    stamps = [s for s in stamps if s]
    return min(stamps) if stamps else None


def classify(row):
    """Provenance class from the retained contract fields, never from the label a sender chose."""
    version, scenario = str(row.get("schema_version")), str(row.get("scenario"))
    if version.startswith("live-sim-reading") and scenario == "live-simulator":
        return "synthetic-weather-derived"
    if version in ("reading-v1", "sensor-fault-input-v1"):
        return "synthetic-modelled-indoor"
    return "synthetic-unclassified"


def _controls(db, home_id, sensor_ids):
    """Per-home control records by primary key; bounded to the sensors this home's rows name."""
    wanted = set(sensor_ids)
    if home_key(home_id):
        wanted.add(sensor_key(home_id))
    if len(home_id) > 3:
        wanted.add("SENS-SYN-" + home_id[3:])
    found = {}
    for sensor_id in sorted(wanted):
        row = db.execute(
            "SELECT body FROM sensor_consumer_control WHERE sensor_id=?", (sensor_id,)
        ).fetchone()
        if row is None:
            continue
        control = json.loads(str(row[0]))
        if control.get("home_id") == home_id:
            found[sensor_id] = control.get("consent")
    return found


def consent(db, home_id, sensor_ids=()):
    """Trusted per-home consent; anything unclear is unknown, never granted."""
    found = _controls(db, home_id, sensor_ids)
    states = set(found.values())
    if "declined" in states:
        return "declined"
    named = {s for s in sensor_ids}
    if states == {"granted"} and named <= set(found):
        return "granted"
    return "unknown"


def _bound(value, mssql):
    return value.replace(tzinfo=None) if mssql else _text(value)


def _reading(row):
    out = dict(zip(COLUMNS, row, strict=True))
    stamp = out["observed_at"]
    if isinstance(stamp, datetime):
        out["observed_at"] = _text(stamp.replace(tzinfo=UTC))
    for key in COLUMNS:
        if key != "observed_at":
            out[key] = str(out[key])
    out["provenance_class"] = classify(out)
    out.pop("schema_version")
    out.pop("scenario")
    return out


def _select(db, mssql, home_id, limit, newest, lower=None, upper=None):
    """At most `limit` retained synthetic readings for one home, bounded by count and time."""
    where, args = ["home_id=?", "source_type='SYNTHETIC'"], [home_id]
    if lower is not None:
        where.append("observed_at>=?")
        args.append(_bound(lower, mssql))
    if upper is not None:
        where.append("observed_at<?")
        args.append(_bound(upper, mssql))
    order = "DESC" if newest else "ASC"
    query = (
        f"SELECT {', '.join(COLUMNS)} FROM sensor_reading WHERE {' AND '.join(where)}"
        f" ORDER BY observed_at {order}, sensor_id {order}, reading_id {order}"
    )
    query += " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY" if mssql else " LIMIT ?"
    rows = [_reading(r) for r in db.execute(query, (*args, limit)).fetchall()]
    return sorted(rows, key=lambda r: (r["observed_at"], r["sensor_id"], r["reading_id"]))


def key_of(reading):
    """Citation key over the retained composite key (sensor_id, reading_id)."""
    return f"sensor:{reading['sensor_id']}:{reading['reading_id']}"


def citations(source):
    """Stable citation keys for every captured reading; each names the exact retained row."""
    rows = [r for key in ("readings", "before", "after") for r in source.get(key, [])]
    return {key_of(r): r for r in rows}


def _base(home_id, reference):
    return dict(
        version=VERSION,
        kind=KIND,
        units=dict(UNITS),
        home_id=home_id,
        max_readings=dict(window=WINDOW_MAX, context_each=CONTEXT_MAX),
        calibrated=False,
        retrofit_context=dict(RETROFIT),
        anchor=dict(
            name=ANCHOR_NAME,
            at=_text(reference) if reference else None,
            meaning=ANCHOR_MEANING,
        ),
    )


def _classes(rows):
    return sorted({r["provenance_class"] for r in rows})


def capture_source(db, home_id, reference, mssql=False):
    """Clock-free, bounded sensor source holding the newest readings, the latest included."""
    base = _base(home_id, reference)
    empty = dict(readings=[], before=[], after=[], latest=None, provenance={}, citation_keys=[])
    try:
        window = _select(db, mssql, home_id, WINDOW_MAX, True)
        before = after = []
        if reference is not None:
            before = _select(db, mssql, home_id, CONTEXT_MAX, True, upper=reference)
            after = _select(db, mssql, home_id, CONTEXT_MAX, False, lower=reference)
        sensor_ids = {r["sensor_id"] for r in window + before + after}
        state = consent(db, home_id, sensor_ids)
        if state != "granted":
            return dict(
                base,
                state="consent-withheld",
                detail=f"Monitoring consent is {state}; no values are shown.",
                **empty,
            )
    except Exception:
        return dict(
            base, state="unavailable", detail="Retained readings could not be read.", **empty
        )
    absent = (
        "No quality evidence record time exists, so no comparison around it can be shown."
        if reference is None
        else None
    )
    out = dict(
        base,
        state="ok" if window else "no-readings",
        detail=None if window else "No retained readings for this home.",
        readings=window,
        before=before,
        after=after,
        latest=window[-1] if window else None,
        before_absent=absent
        or (None if before else "No retained readings before the first quality evidence record."),
        after_absent=absent
        or (
            None if after else "No retained readings from the first quality evidence record onward."
        ),
        window_absent=None if window else "No retained readings for this home.",
    )
    rows = window + before + after
    out["provenance"] = {c: CLASSES[c] for c in _classes(rows)}
    out["citation_keys"] = sorted(citations(out))
    return {k: v for k, v in out.items() if v is not None or k == "latest"}


def signature(sensors):
    """Trigger signature: state, anchor and a six-hour bucket of the latest observation.

    It carries no clock. Evidence is always captured exactly; only the decision to request new work
    uses this coarse value, so one five-minute reading does not start a new model request.
    """
    latest = (sensors or {}).get("latest")
    bucket = None
    if latest:
        moment = datetime.strptime(latest["observed_at"], STAMP).replace(tzinfo=UTC)
        bucket = int(moment.timestamp()) // SEAL_SECONDS
    return dict(
        version=VERSION,
        state=(sensors or {}).get("state"),
        anchor=((sensors or {}).get("anchor") or {}).get("at"),
        bucket=bucket,
        classes=sorted((sensors or {}).get("provenance") or {}),
    )


def view(db, home_id, reference, now, mssql=False):
    """Employee read model: the captured source plus freshness from the capture's own latest."""
    out = capture_source(db, home_id, reference, mssql)
    out.update(
        generated_at=_text(_utc(int(now))),
        freshness="unknown",
        freshness_text="No reading is available.",
        manual_route=MANUAL,
    )
    if out["state"] in ("consent-withheld", "unavailable"):
        out["freshness_text"] = out["detail"]
        return out
    latest = out["latest"]
    if latest:
        age = int(now) - int(
            datetime.strptime(latest["observed_at"], STAMP).replace(tzinfo=UTC).timestamp()
        )
        fresh = age <= FRESH_SECONDS
        out.update(
            age_seconds=max(age, 0),
            freshness="fresh" if fresh else "stale",
            freshness_text=(
                "Latest reading is recent (within 15 minutes)."
                if fresh
                else "Latest reading is older than 15 minutes. Treat it as out of date."
            ),
        )
    return out
