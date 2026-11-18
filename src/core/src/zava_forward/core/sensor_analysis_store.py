"""Retained-reading entry point for the exercise sensor analysis (issue 111).

Reads stored readings and trusted consent through a store-neutral read-only retained-reading
source (`SqlStore` / `SensorConsumer` or configured JSON `Store` / `JsonRetainedStore`) and passes
them to the pure derivation. Reading never writes, never creates a task and never ranks. If the
retained store cannot be read, the result is INSUFFICIENT with no priority effect and the manual
review route stays available.
"""

from collections.abc import Mapping, Sequence
from contextlib import AbstractContextManager
from dataclasses import asdict, replace
from datetime import datetime, timedelta
from typing import Any, Protocol

from .sensor_analysis import (
    INSUFFICIENT,
    AnalysisPolicy,
    ReproducedReviewTask,
    Signal,
    derive_signal,
    format_reproduced_review_task,
    review_task_candidate,
    version_provenance,
)
from .sensor_consumer import (
    LIVE_FIELDS,
    READING_COLUMNS,
    ConsumerError,
    Observation,
    SensorConsumer,
    SensorControl,
    utc,
)
from .sensor_sql import SensorMssqlConnector
from .sqlstore import SqlStore
from .store import Store
from .synthetic.live_readings import LIVE_VERSIONS
from .synthetic.sensor_faults import READING_FIELDS, SCHEMA_VERSION
from .synthetic.sensor_identity import home_key
from .synthetic.sensor_scenarios import Window

UNAVAILABLE = "RETAINED_READINGS_UNAVAILABLE"
WEATHER_NOT_INDOOR = "WEATHER_INPUT_NOT_INDOOR_MEASUREMENT"
JSON_RETAINED_KEY = "sensor_retained"
_LEGACY_V1_FIELDS = tuple(col for col in READING_COLUMNS if col != "injected_fault")


class RetainedReadingSource(Protocol):
    """Read-only consent and retained-envelope interface shared across store backends."""

    def home_consent(self, home_id: str) -> str: ...
    def retained_envelopes(
        self,
        home_ids: Sequence[str],
        windows: Mapping[str, tuple[str, str]] | None = None,
    ) -> list[dict[str, str]]: ...


class _JsonStoreCarrier(Protocol):
    lock: AbstractContextManager[object]
    data: dict[str, Any]

    def save(self) -> None: ...


RetainedInput = SensorConsumer | SqlStore | SensorMssqlConnector | Store | RetainedReadingSource


def _validate_control_dict(raw: object) -> dict[str, object]:
    if not isinstance(raw, Mapping):
        raise ConsumerError("SENSOR_CONTROLS_MALFORMED")
    try:
        control = SensorControl(
            sensor_id=raw["sensor_id"],
            home_id=raw["home_id"],
            mapping_start=raw["mapping_start"],
            mapping_end=raw["mapping_end"],
            consent=raw["consent"],
            calibration_start=raw["calibration_start"],
            calibration_end=raw["calibration_end"],
            calibration_confirmed=raw["calibration_confirmed"],
            temperature_unit=raw["temperature_unit"],
            humidity_unit=raw["humidity_unit"],
        )
        if not all(
            type(v) is str
            for k, v in raw.items()
            if k != "calibration_confirmed" and k in asdict(control)
        ):
            raise ConsumerError("SENSOR_CONTROLS_MALFORMED")
        if set(raw) != set(asdict(control)):
            raise ConsumerError("SENSOR_CONTROLS_MALFORMED")
        control.validate()
    except (KeyError, TypeError, ValueError):
        raise ConsumerError("SENSOR_CONTROLS_MALFORMED") from None
    return dict(asdict(control))


def _validate_retained_envelope(
    raw: object,
    controls_by_sensor: Mapping[str, Mapping[str, object]],
    *,
    require_v1_control: bool,
) -> dict[str, str]:
    if not isinstance(raw, Mapping) or any(
        type(k) is not str or type(v) is not str for k, v in raw.items()
    ):
        raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
    string_row: dict[str, str] = {str(k): str(v) for k, v in raw.items()}
    observation: Observation = dict(string_row)
    version = string_row.get("schema_version")
    if version in LIVE_VERSIONS:
        if (
            set(string_row) != set(LIVE_FIELDS)
            or SensorConsumer._live_shape(observation) is not None
        ):
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        return {key: string_row[key] for key in LIVE_FIELDS}
    if version == SCHEMA_VERSION:
        if set(string_row) != set(READING_FIELDS) or SensorConsumer._shape(observation) is not None:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        return {key: string_row[key] for key in READING_FIELDS}
    if version == "reading-v1":
        if set(string_row) != set(_LEGACY_V1_FIELDS):
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        if (
            not home_key(string_row["home_id"])
            or not string_row["sensor_id"]
            or not string_row["reading_id"]
        ):
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        try:
            utc(string_row["observed_at"])
        except ValueError:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED") from None
        if require_v1_control and string_row["sensor_id"] not in controls_by_sensor:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        return {key: string_row[key] for key in _LEGACY_V1_FIELDS}
    raise ConsumerError("SENSOR_OUTCOME_MALFORMED")


def retain_json_readings(
    store: Store,
    controls: Sequence[SensorControl],
    readings: Sequence[Mapping[str, object]],
    *,
    save: bool = True,
) -> int:
    """Persist validated controls and canonical retained reading envelopes into a JSON `Store`."""
    if isinstance(store, SqlStore) or not isinstance(store, Store):
        raise ConsumerError("JSON_STORE_REQUIRED")
    if len(controls) > 100:
        raise ConsumerError("TOO_MANY_SENSOR_CONTROLS")
    seen_sensors: set[str] = set()
    control_dicts: list[dict[str, object]] = []
    controls_by_sensor: dict[str, dict[str, object]] = {}
    for control in controls:
        if not isinstance(control, SensorControl):
            raise ConsumerError("SENSOR_CONTROLS_MALFORMED")
        try:
            control.validate()
        except ValueError as exc:
            raise ConsumerError(str(exc)) from None
        if control.sensor_id in seen_sensors:
            raise ConsumerError("DUPLICATE_SENSOR_CONTROL")
        seen_sensors.add(control.sensor_id)
        dumped = dict(asdict(control))
        control_dicts.append(dumped)
        controls_by_sensor[control.sensor_id] = dumped
    control_dicts.sort(key=lambda item: str(item["sensor_id"]))

    carrier: _JsonStoreCarrier = store
    with carrier.lock:
        existing_raw = carrier.data.get(JSON_RETAINED_KEY)
        by_identity: dict[tuple[str, str], dict[str, str]] = {}
        if existing_raw is not None:
            if not isinstance(existing_raw, Mapping) or set(existing_raw) != {
                "controls",
                "readings",
            }:
                raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
            prior_readings = existing_raw.get("readings")
            if not isinstance(prior_readings, list):
                raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
            for entry in prior_readings:
                canonical = _validate_retained_envelope(
                    entry, controls_by_sensor, require_v1_control=False
                )
                ident = (canonical["sensor_id"], canonical["reading_id"])
                prior = by_identity.get(ident)
                if prior is not None and prior != canonical:
                    raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
                by_identity[ident] = canonical

        added = 0
        for incoming in readings:
            canonical = _validate_retained_envelope(
                incoming, controls_by_sensor, require_v1_control=True
            )
            ident = (canonical["sensor_id"], canonical["reading_id"])
            prior = by_identity.get(ident)
            if prior is not None:
                if prior != canonical:
                    raise ConsumerError("IDENTITY_CONFLICT")
                continue
            by_identity[ident] = canonical
            added += 1

        ordered = sorted(
            by_identity.values(),
            key=lambda row: (row["observed_at"], row["sensor_id"], row["reading_id"]),
        )
        carrier.data[JSON_RETAINED_KEY] = {
            "controls": control_dicts,
            "readings": ordered,
        }
        if save:
            carrier.save()
        return added


class JsonRetainedStore:
    """Read-only retained-reading adapter over configured `Store.data['sensor_retained']`."""

    def __init__(self, store: Store) -> None:
        if isinstance(store, SqlStore) or not isinstance(store, Store):
            raise ConsumerError("JSON_STORE_REQUIRED")
        self._carrier: _JsonStoreCarrier = store

    def _snapshot(
        self,
    ) -> tuple[dict[str, dict[str, object]], list[dict[str, str]]]:
        with self._carrier.lock:
            payload = self._carrier.data.get(JSON_RETAINED_KEY)
            if payload is None:
                raise ConsumerError(UNAVAILABLE)
            if not isinstance(payload, Mapping) or set(payload) != {"controls", "readings"}:
                raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
            raw_controls = payload.get("controls")
            raw_readings = payload.get("readings")
            if not isinstance(raw_controls, list) or not isinstance(raw_readings, list):
                raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
            controls_by_sensor: dict[str, dict[str, object]] = {}
            for item in raw_controls:
                validated = _validate_control_dict(item)
                sensor_id = str(validated["sensor_id"])
                if sensor_id in controls_by_sensor:
                    raise ConsumerError("SENSOR_CONTROLS_MALFORMED")
                controls_by_sensor[sensor_id] = validated
            seen_ids: dict[tuple[str, str], dict[str, str]] = {}
            readings: list[dict[str, str]] = []
            for entry in raw_readings:
                canonical = _validate_retained_envelope(
                    entry, controls_by_sensor, require_v1_control=False
                )
                ident = (canonical["sensor_id"], canonical["reading_id"])
                prior = seen_ids.get(ident)
                if prior is not None and prior != canonical:
                    raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
                if prior is None:
                    seen_ids[ident] = canonical
                    readings.append(canonical)
            return controls_by_sensor, readings

    def home_consent(self, home_id: str) -> str:
        """Read-only trusted consent for a home; fails closed to unknown, never infers grant."""
        if not home_key(home_id):
            raise ConsumerError("INVALID_HOME_SELECTION")
        controls_by_sensor, _ = self._snapshot()
        states = {
            str(control["consent"])
            for control in controls_by_sensor.values()
            if control.get("home_id") == home_id
        }
        if "declined" in states:
            return "declined"
        return "granted" if states == {"granted"} else "unknown"

    def retained_envelopes(
        self,
        home_ids: Sequence[str],
        windows: Mapping[str, tuple[str, str]] | None = None,
    ) -> list[dict[str, str]]:
        """Read stored readings per home as exact retained wire envelopes with trusted units."""
        if (
            not home_ids
            or any(
                not home_key(home) or len(home.encode("utf-16-le")) // 2 > 64 for home in home_ids
            )
            or (windows is not None and set(windows) != set(home_ids))
        ):
            raise ConsumerError("INVALID_HOME_SELECTION")
        bounds: dict[str, tuple[str, str]] = {}
        try:
            if windows is not None:
                for home in home_ids:
                    first_raw, last_raw = windows[home]
                    first_dt = utc(first_raw)
                    last_dt = utc(last_raw)
                    bounds[home] = (
                        first_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        last_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    )
        except (ValueError, TypeError):
            raise ConsumerError("INVALID_HOME_SELECTION") from None

        controls_by_sensor, readings = self._snapshot()
        rows: list[dict[str, str]] = []
        for home in home_ids:
            home_bounds = bounds.get(home)
            matched = [
                record
                for record in readings
                if record["home_id"] == home
                and (
                    home_bounds is None or home_bounds[0] <= record["observed_at"] <= home_bounds[1]
                )
            ]
            matched.sort(
                key=lambda record: (
                    record["observed_at"],
                    record["sensor_id"],
                    record["reading_id"],
                )
            )
            for record in matched:
                version = record["schema_version"]
                if version in LIVE_VERSIONS:
                    rows.append({key: record[key] for key in LIVE_FIELDS})
                    continue
                if version == SCHEMA_VERSION:
                    rows.append({key: record[key] for key in READING_FIELDS})
                    continue
                control = controls_by_sensor.get(record["sensor_id"])
                if control is None:
                    raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
                projected = {key: record[key] for key in _LEGACY_V1_FIELDS}
                projected.update(
                    temperature_unit=str(control["temperature_unit"]),
                    humidity_unit=str(control["humidity_unit"]),
                    calibrated=str(control["calibration_confirmed"]).lower(),
                )
                rows.append(projected)
        return rows

    def observed_series(
        self,
        home_ids: Sequence[str],
        windows: Mapping[str, tuple[str, str]] | None = None,
    ) -> list[dict[str, str]]:
        """Indoor-contract rows for comparison and indoor analysis, excluding live-sim rows."""
        return [
            row
            for row in self.retained_envelopes(home_ids, windows)
            if row["schema_version"] not in LIVE_VERSIONS
        ]


def retained_source(source: RetainedInput) -> RetainedReadingSource:
    """Resolve a SQL store, JSON store, consumer, or protocol source to a read-only source."""
    if isinstance(source, (SqlStore, SensorMssqlConnector)):
        return SensorConsumer(source)
    if isinstance(source, Store):
        return JsonRetainedStore(source)
    return source


def analyse_retained(
    consumer: RetainedInput,
    home_id: str,
    window: Window,
    as_of: datetime,
    policy: AnalysisPolicy | None = None,
) -> Signal:
    """Derive the signal for one home from retained readings; fail closed to INSUFFICIENT."""
    source = retained_source(consumer)
    last = (window.end - timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    first = window.start.strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        consent = source.home_consent(home_id)
        envelopes = source.retained_envelopes([home_id], {home_id: (first, last)})
    except ConsumerError:
        empty = derive_signal(home_id, [], window, as_of, "unknown", policy)
        return replace(
            empty, sufficiency=INSUFFICIENT, outcome=INSUFFICIENT, reasons=(UNAVAILABLE,)
        )
    # Live-sim rows are climate-shaped outdoor readings, not indoor measurements.
    rows = [row for row in envelopes if row["schema_version"] not in LIVE_VERSIONS]
    if consent == "granted" and len(rows) < len(envelopes) and not rows:
        empty = derive_signal(home_id, [], window, as_of, consent, policy)
        return replace(
            empty, sufficiency=INSUFFICIENT, outcome=INSUFFICIENT, reasons=(WEATHER_NOT_INDOOR,)
        )
    return derive_signal(home_id, rows, window, as_of, consent, policy)


def reproduce_retained(
    consumer: RetainedInput,
    home_id: str,
    window: Window,
    as_of: datetime,
    policy: AnalysisPolicy | None = None,
) -> ReproducedReviewTask:
    """Re-derive signal, review-task candidate, and version provenance read-only from store."""
    effective = policy or AnalysisPolicy()
    effective.validate()
    signal = analyse_retained(consumer, home_id, window, as_of, effective)
    candidate = review_task_candidate(signal, effective)
    provenance = version_provenance(signal, effective, candidate)
    return format_reproduced_review_task(provenance, signal, candidate)
