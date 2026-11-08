"""Bounded retained indoor reading read model for employees and Quality evidence (issue 1288).

Read only. It selects from the retained `sensor_reading` rows admitted by the sensor consumer,
never generates values, never reads weather or other variables and never queries unbounded history.
The same `capture_source` output feeds the employee view and the quality-evidence snapshot, so the
reading ids and values a person sees are the ones the model request carries. Values are withheld
unless the home's recorded monitoring consent is granted. Any storage failure is an explicit state.
"""

import json
from datetime import UTC, datetime, timedelta

VERSION = "retained-indoor-view-v1"
KIND = "indoor-observation"
PROVENANCE = "synthetic"
UNITS = dict(temperature_c="degC", humidity_pct="%RH")
WINDOW_MAX = 12
CONTEXT_MAX = 4
SEAL_SECONDS = 21600
FRESH_SECONDS = 900
STAMP = "%Y-%m-%dT%H:%M:%SZ"
COLUMNS = ("reading_id", "sensor_id", "observed_at", "temperature_c", "humidity_pct", "scenario")
STATES = ("ok", "no-readings", "consent-withheld", "unavailable")
MANUAL = "Use the ordinary quality check; no one is waiting on sensor values."


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


def consent(db, home_id):
    """Trusted per-home consent; anything unclear is unknown, never granted."""
    states = set()
    for (body,) in db.execute("SELECT body FROM sensor_consumer_control").fetchall():
        control = json.loads(str(body))
        if control.get("home_id") == home_id:
            states.add(control.get("consent"))
    if "declined" in states:
        return "declined"
    return "granted" if states == {"granted"} else "unknown"


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
    return out


def _select(db, mssql, home_id, limit, newest, lower=None, upper=None, lower_inclusive=True):
    """At most `limit` retained synthetic readings for one home, bounded by count and time."""
    where, args = ["home_id=?", "source_type='SYNTHETIC'"], [home_id]
    if lower is not None:
        where.append("observed_at>=?" if lower_inclusive else "observed_at>?")
        args.append(_bound(lower, mssql))
    if upper is not None:
        where.append("observed_at<?")
        args.append(_bound(upper, mssql))
    order = "DESC" if newest else "ASC"
    query = (
        f"SELECT {', '.join(COLUMNS)} FROM sensor_reading WHERE {' AND '.join(where)}"
        f" ORDER BY observed_at {order}, reading_id {order}"
    )
    query += " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY" if mssql else " LIMIT ?"
    rows = [_reading(r) for r in db.execute(query, (*args, limit)).fetchall()]
    return sorted(rows, key=lambda r: (r["observed_at"], r["reading_id"]))


def _context(db, mssql, home_id, reference, seal):
    if reference is None:
        absent = (
            "No quality evidence record time exists, so before and after readings cannot be shown."
        )
        return dict(reference=None, before=[], after=[], before_absent=absent, after_absent=absent)
    before = _select(db, mssql, home_id, CONTEXT_MAX, True, upper=min(reference, seal))
    after = _select(db, mssql, home_id, CONTEXT_MAX, False, lower=reference, upper=seal)
    return dict(
        reference=_text(reference),
        before=before,
        after=after,
        before_absent=None
        if before
        else "No retained readings before the first quality evidence record.",
        after_absent=None
        if after
        else "No retained readings from the first quality evidence record onward.",
    )


def _compact(source):
    return {k: v for k, v in source.items() if v is not None}


def capture_source(db, home_id, reference, now, mssql=False):
    """Time-stable, bounded sensor source. Freshness and the live latest reading are excluded."""
    seal = _utc(int(now) // SEAL_SECONDS * SEAL_SECONDS)
    base = dict(
        version=VERSION,
        kind=KIND,
        provenance=PROVENANCE,
        units=dict(UNITS),
        home_id=home_id,
        window=dict(start=_text(seal - timedelta(seconds=SEAL_SECONDS)), end=_text(seal)),
        max_readings=dict(window=WINDOW_MAX, context_each=CONTEXT_MAX),
    )
    empty = dict(readings=[], before=[], after=[], reference=None)
    try:
        state = consent(db, home_id)
        if state != "granted":
            return _compact(
                dict(
                    base,
                    state="consent-withheld",
                    detail=f"Monitoring consent is {state}; no values are shown.",
                    **empty,
                )
            )
        window = _select(
            db,
            mssql,
            home_id,
            WINDOW_MAX,
            True,
            lower=seal - timedelta(seconds=SEAL_SECONDS),
            upper=seal,
        )
        context = _context(db, mssql, home_id, reference, seal)
    except Exception:
        return _compact(
            dict(base, state="unavailable", detail="Retained readings could not be read.", **empty)
        )
    if not window and not context["before"] and not context["after"]:
        return _compact(
            dict(
                base,
                state="no-readings",
                detail="No retained readings for this home in the sealed window.",
                **empty,
                before_absent=context["before_absent"],
                after_absent=context["after_absent"],
            )
        )
    return _compact(
        dict(
            base,
            state="ok",
            detail=None,
            readings=window,
            before=context["before"],
            after=context["after"],
            reference=context["reference"],
            before_absent=context["before_absent"],
            after_absent=context["after_absent"],
            window_absent=None if window else "No retained readings in the sealed window.",
        )
    )


def citations(source):
    """Stable citation keys for every reading, so a finding can name the exact retained reading."""
    rows = [r for key in ("readings", "before", "after") for r in source.get(key, [])]
    return {f"sensor:{r['reading_id']}": r for r in rows}


def view(db, home_id, reference, now, mssql=False):
    """Employee read model: the captured source plus the live latest reading and its freshness."""
    out = capture_source(db, home_id, reference, now, mssql)
    out.update(
        generated_at=_text(_utc(int(now))),
        latest=None,
        freshness="unknown",
        freshness_text="No reading is available.",
        manual_route=MANUAL,
    )
    if out["state"] in ("consent-withheld", "unavailable"):
        out["freshness_text"] = out["detail"]
        return out
    try:
        latest = _select(db, mssql, home_id, 1, True, upper=_utc(int(now) + 1))
    except Exception:
        out.update(
            state="unavailable",
            detail="Retained readings could not be read.",
            freshness_text="Retained readings could not be read.",
        )
        return out
    if latest:
        age = int(now) - int(
            datetime.strptime(latest[0]["observed_at"], STAMP).replace(tzinfo=UTC).timestamp()
        )
        fresh = age <= FRESH_SECONDS
        out.update(
            latest=latest[0],
            age_seconds=max(age, 0),
            freshness="fresh" if fresh else "stale",
            freshness_text=(
                "Latest reading is recent (within 15 minutes)."
                if fresh
                else "Latest reading is older than 15 minutes. Treat it as out of date."
            ),
        )
    return out
