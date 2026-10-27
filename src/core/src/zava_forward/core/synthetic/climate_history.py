"""Hash-pinned, paired outdoor ERA5 history for synthetic indoor projections.

The strict hourly/unit/Magnus checks reuse the approach in candidate 72f52358's
tools/climate_paired_bounds.py. No interpolation, repetition or clipping occurs.
"""

import copy
import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import NoReturn, cast
from urllib.parse import parse_qs, urlsplit

VERSION = "climate-history-v1"
UNITS = {"temperature_2m": "°C", "relative_humidity_2m": "%", "dew_point_2m": "°C"}
RH_TOLERANCE = 1.0
HOUR = timedelta(hours=1)


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return cast(dict[str, object], value)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> NoReturn:
    raise ValueError(f"Nonstandard JSON numeric constant: {value}")


def _json(raw: bytes, label: str) -> dict[str, object]:
    try:
        return _object(
            json.loads(raw, object_pairs_hook=_unique_object, parse_constant=_invalid_constant),
            label,
        )
    except (UnicodeError, ValueError) as exc:
        raise ValueError(f"Invalid {label}: {exc}") from exc


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric, not null or boolean")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{label} exceeds the finite numeric range") from exc
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def _hash(raw: bytes, expected: object, label: str) -> str:
    if not isinstance(expected, str) or not re.fullmatch("[0-9a-f]{64}", expected):
        raise ValueError(f"{label} requires a lowercase SHA-256")
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise ValueError(f"{label} SHA-256 mismatch: got {actual}")
    return actual


def _stamp(value: object, *, raw: bool = False) -> datetime:
    text = _text(value, "UTC timestamp")
    pattern = "%Y-%m-%dT%H:%M" if raw else "%Y-%m-%dT%H:%MZ"
    try:
        parsed = datetime.strptime(text, pattern).replace(tzinfo=UTC)
    except ValueError as exc:
        raise ValueError(f"Invalid UTC timestamp: {text}") from exc
    if parsed.strftime(pattern) != text or parsed.minute:
        raise ValueError(f"Timestamp must be an exact UTC hour: {text}")
    return parsed


def _window(metadata: dict[str, object]) -> tuple[datetime, datetime, int]:
    coverage = _object(metadata.get("coverage"), "coverage")
    start = _stamp(coverage.get("start"))
    end = _stamp(coverage.get("end_exclusive"))
    records = coverage.get("records")
    if (
        type(records) is not int
        or records <= 0
        or end - start != records * HOUR
        or coverage.get("step_seconds") != 3600
        or coverage.get("timezone") != "UTC"
    ):
        raise ValueError("coverage must declare a positive, complete hourly UTC window")
    return start, end, records


def _source(metadata: dict[str, object], start: datetime, end: datetime) -> None:
    source = _object(metadata.get("source"), "source")
    for key in ("provider", "model", "dataset_version", "api_version", "resolution_reference"):
        _text(source.get(key), f"source.{key}")
    if source["provider"] != "Open-Meteo" or source["model"] != "ERA5":
        raise ValueError("Only the explicitly requested Open-Meteo ERA5 model is supported")
    retrieved = _text(source.get("retrieved_on"), "source.retrieved_on")
    try:
        if date.fromisoformat(retrieved).isoformat() != retrieved:
            raise ValueError("Noncanonical retrieval date")
    except ValueError as exc:
        raise ValueError("source.retrieved_on must be YYYY-MM-DD") from exc
    resolution = _object(source.get("resolution"), "source.resolution")
    if resolution != {"temporal_seconds": 3600, "grid_degrees": 0.25}:
        raise ValueError("Expected ERA5 hourly, 0.25-degree source resolution")
    url = urlsplit(_text(source.get("request_url"), "source.request_url"))
    if (
        url.scheme != "https"
        or url.netloc != "archive-api.open-meteo.com"
        or url.path != "/v1/archive"
        or url.fragment
    ):
        raise ValueError("Source request must use the official HTTPS archive endpoint")
    query = parse_qs(url.query, strict_parsing=True)
    expected = {
        "models": "era5",
        "timezone": "UTC",
        "temperature_unit": "celsius",
        "timeformat": "iso8601",
        "start_date": start.date().isoformat(),
        "end_date": (end - HOUR).date().isoformat(),
        "hourly": ",".join(UNITS),
    }
    if any(query.get(key) != [value] for key, value in expected.items()):
        raise ValueError("Source request model, units or period contradict the contract")
    if start.hour or end.hour:
        raise ValueError("Archive request must cover complete UTC days")
    location = _object(source.get("requested_location"), "source.requested_location")
    for key in ("latitude", "longitude"):
        if query.get(key) != [str(_number(location.get(key), f"requested {key}"))]:
            raise ValueError(f"Source request contradicts requested {key}")


def _records(
    payload: dict[str, object], start: datetime, count: int
) -> tuple[tuple[tuple[float, float], ...], dict[str, object], float]:
    units = _object(payload.get("hourly_units"), "hourly_units")
    if units != {"time": "iso8601", **UNITS}:
        raise ValueError("Unexpected hourly units")
    if (
        type(payload.get("utc_offset_seconds")) is not int
        or payload["utc_offset_seconds"] != 0
        or payload.get("timezone") not in ("UTC", "GMT")
        or payload.get("timezone_abbreviation") not in ("UTC", "GMT")
    ):
        raise ValueError("Response must explicitly use UTC without an offset")
    hourly = _object(payload.get("hourly"), "hourly")
    columns: dict[str, list[object]] = {}
    for key in ("time", *UNITS):
        column = hourly.get(key)
        if not isinstance(column, list) or len(column) != count:
            raise ValueError(f"Missing or incomplete hourly series: {key}")
        columns[key] = column
    pairs: list[tuple[float, float]] = []
    dew_points: list[float] = []
    residual = 0.0
    for index in range(count):
        if _stamp(columns["time"][index], raw=True) != start + index * HOUR:
            raise ValueError(f"Gap, duplicate or misaligned UTC hour at index {index}")
        temperature, humidity, dew = (
            _number(columns[key][index], f"{key}[{index}]") for key in UNITS
        )
        if not 0 <= humidity <= 100:
            raise ValueError(f"Relative humidity outside 0..100 at index {index}")
        if dew > temperature:
            raise ValueError(f"Dew point above temperature at index {index}")
        try:
            derived_rh = 100 * math.exp(
                17.625 * dew / (243.04 + dew) - 17.625 * temperature / (243.04 + temperature)
            )
        except (OverflowError, ZeroDivisionError) as exc:
            raise ValueError(f"Invalid Magnus temperature/dew point at index {index}") from exc
        error = abs(derived_rh - humidity)
        if not math.isfinite(error) or error > RH_TOLERANCE:
            raise ValueError(f"Humidity inconsistent with temperature/dew point at index {index}")
        residual = max(residual, error)
        pairs.append((temperature, humidity))
        dew_points.append(dew)
    bounds: dict[str, object] = {}
    for key, values in (
        ("temperature_c", [pair[0] for pair in pairs]),
        ("relative_humidity_pct", [pair[1] for pair in pairs]),
        ("dew_point_c", dew_points),
    ):
        bounds[key] = {"minimum": min(values), "maximum": max(values)}
    return tuple(pairs), bounds, round(residual, 6)


@dataclass(frozen=True)
class ClimateHistory:
    """Validated, immutable hourly pairs; use ``read`` to construct from pinned bytes."""

    start: datetime
    end_exclusive: datetime
    _pairs: tuple[tuple[float, float], ...]
    _metadata: dict[str, object]

    @classmethod
    def read(
        cls,
        path: str | Path,
        metadata_path: str | Path,
        *,
        expected_sha256: str | None = None,
        expected_metadata_sha256: str | None = None,
    ) -> "ClimateHistory":
        """Read offline, checking raw bytes against metadata and optional external pins.

        The metadata file is the caller's trust contract unless independently pinned.
        No source version absent from the response is inferred.
        """
        raw = Path(path).read_bytes()
        metadata_raw = Path(metadata_path).read_bytes()
        metadata_hash = hashlib.sha256(metadata_raw).hexdigest()
        if expected_metadata_sha256 is not None:
            _hash(metadata_raw, expected_metadata_sha256, "Metadata")
        metadata = _json(metadata_raw, "metadata")
        if metadata.get("schema_version") != VERSION or metadata.get("units") != UNITS:
            raise ValueError("Unsupported metadata version or units")
        input_contract = _object(metadata.get("input"), "input")
        digest = _hash(raw, input_contract.get("sha256"), "Input")
        if expected_sha256 is not None:
            _hash(raw, expected_sha256, "External input")
        if type(input_contract.get("bytes")) is not int or input_contract["bytes"] != len(raw):
            raise ValueError("Input byte count mismatch")
        start, end, count = _window(metadata)
        _source(metadata, start, end)
        payload = _json(raw, "climate input")
        source = _object(metadata["source"], "source")
        grid = _object(source.get("returned_grid"), "source.returned_grid")
        for key in ("latitude", "longitude", "elevation"):
            if _number(payload.get(key), key) != _number(grid.get(key), f"grid.{key}"):
                raise ValueError(f"Returned grid mismatch: {key}")
        pairs, bounds, residual = _records(payload, start, count)
        if metadata.get("bounds") != bounds:
            raise ValueError("Declared bounds differ from actual hourly records")
        validation = _object(metadata.get("validation"), "validation")
        if validation != {
            "magnus_constants": [17.625, 243.04],
            "rh_tolerance_points": RH_TOLERANCE,
            "max_rh_residual_points": residual,
            "nothing_filled_or_inferred": True,
        }:
            raise ValueError("Validation metadata differs from actual checks")
        metadata.update(
            adapter_version=VERSION,
            input_sha256=digest,
            metadata_sha256=metadata_hash,
        )
        return cls(start, end, pairs, metadata)

    def series(self, start: datetime, days: int, cadence: int) -> list[tuple[float, float]]:
        """Return exact (degC, RH percent) pairs at ``cadence`` minutes.

        Cadence must be a whole number of hours dividing one day. The requested
        half-open window must fit entirely inside the retained UTC history.
        """
        if (
            not isinstance(start, datetime)
            or start.utcoffset() != timedelta(0)
            or start.minute
            or start.second
            or start.microsecond
        ):
            raise ValueError("start must be timezone-aware UTC on an exact hour")
        if type(days) is not int or days <= 0:
            raise ValueError("days must be a positive integer")
        if type(cadence) is not int or cadence <= 0 or cadence % 60 or 1440 % cadence:
            raise ValueError("cadence must be whole-hour minutes dividing 1440")
        try:
            end = start + timedelta(days=days)
        except OverflowError as exc:
            raise ValueError("Requested days exceed the datetime range") from exc
        if start < self.start or end > self.end_exclusive:
            raise ValueError("Requested window is outside the pinned climate history")
        offset = (start - self.start) // HOUR
        return list(self._pairs[offset : offset + days * 24 : cadence // 60])

    def manifest(self) -> dict[str, object]:
        """Return a detached provenance copy, including raw and metadata SHA-256."""
        return copy.deepcopy(self._metadata)
