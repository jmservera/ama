#!/usr/bin/env python3
"""Validate and derive bounds from a retrieved paired hourly climate sample.

Offline and hash-pinned. The inputs are modelled reanalysis products (Open-Meteo
ERA5 and NASA POWER MERRA-2), never station observations. Nothing is filled,
inferred or defaulted: any gap, misalignment or inconsistent humidity is rejected.
"""

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path
import re

RH_TOLERANCE = 1.0
PERCENTILE_RULE = (
    "Sorted values, rank p*(n-1), linear interpolation between neighbouring "
    "order statistics"
)
PERCENTILES = (1, 99)
STEP = timedelta(hours=1)

LICENCE = {
    "open_meteo": {
        "published_terms": "Open-Meteo API data are offered under CC BY 4.0; the "
                           "free API is for non-commercial use under 10,000 calls "
                           "per day (https://open-meteo.com/en/terms and "
                           "https://open-meteo.com/en/licence, read 2026-10-22).",
        "attribution": "Weather data by Open-Meteo.com, CC BY 4.0, link to "
                       "https://open-meteo.com/, indicate that values were "
                       "summarised; underlying ERA5 reanalysis is Copernicus "
                       "Climate Change Service (C3S) material.",
        "underlying_c3s_reuse_verified": False,
    },
    "nasa_power": {
        "published_terms": "Referencing guide asks for the POWER data reference "
                           "with service, version and access date "
                           "(https://power.larc.nasa.gov/docs/referencing/, read "
                           "2026-10-22). No licence text was retrieved: the NASA "
                           "data information policy page returned HTTP 403.",
        "licence_verified": False,
    },
    "approval_statement": "No approval of demonstrator, downstream or production "
                          "reuse is asserted; owner and legal confirmation remain "
                          "pending.",
}


def _check_https(url: str) -> None:
    if not url.startswith("https://"):
        raise ValueError("Source URL must use HTTPS")


def _check_inputs(raw: bytes, expected_sha256: str, source_url: str,
                  retrieved_on: str) -> str:
    _check_https(source_url)
    try:
        valid = date.fromisoformat(retrieved_on).isoformat() == retrieved_on
    except ValueError:
        valid = False
    if not valid:
        raise ValueError("retrieved-on must be YYYY-MM-DD")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(f"Input SHA-256 mismatch: got {digest}")
    return digest


def _number(value, label: str, index: int) -> float:
    if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Missing or non-numeric {label} at index {index}")
    if not math.isfinite(value):
        raise ValueError(f"Nonfinite {label} at index {index}")
    return float(value)


def _check_hourly(times: list[datetime]) -> None:
    if not times:
        raise ValueError("No hourly records")
    for i in range(1, len(times)):
        if times[i] <= times[i - 1]:
            raise ValueError(f"Timestamps not strictly increasing at index {i}")
        if times[i] - times[i - 1] != STEP:
            raise ValueError(f"Timestamp gap or non-hourly step at index {i}")


def _check_rh(rh: list[float]) -> None:
    for i, value in enumerate(rh):
        if not 0 <= value <= 100:
            raise ValueError(f"Relative humidity outside 0..100 at index {i}")


def _saturation(celsius: float) -> float:
    return math.exp(17.625 * celsius / (243.04 + celsius))


def magnus_rh(temperature: float, dew_point: float) -> float:
    return 100 * _saturation(dew_point) / _saturation(temperature)


def _no_duplicate_keys(pairs):
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate JSON object key")
    return dict(pairs)


def _parse_json(raw: bytes) -> dict:
    try:
        data = json.loads(raw, object_pairs_hook=_no_duplicate_keys)
    except ValueError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")
    return data


def _object(value, label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def parse_open_meteo(raw: bytes, *, source_url: str, retrieved_on: str,
                     expected_sha256: str) -> dict:
    digest = _check_inputs(raw, expected_sha256, source_url, retrieved_on)
    data = _parse_json(raw)
    units = _object(data.get("hourly_units", {}), "hourly_units")
    expected_units = {"temperature_2m": "°C", "relative_humidity_2m": "%",
                      "dew_point_2m": "°C"}
    for key, unit in expected_units.items():
        if units.get(key) != unit:
            raise ValueError(f"Unexpected unit for {key}: {units.get(key)!r}")
    if data.get("utc_offset_seconds") != 0:
        raise ValueError("Open-Meteo response is not UTC")
    hourly = data.get("hourly")
    if not isinstance(hourly, dict):
        raise ValueError("Missing hourly block")
    series = {key: hourly.get(key) for key in ("time", *expected_units)}
    if any(not isinstance(v, list) for v in series.values()):
        raise ValueError("Missing hourly series")
    if len({len(v) for v in series.values()}) != 1:
        raise ValueError("Hourly series differ in length")
    try:
        times = [datetime.strptime(t, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
                 for t in series["time"]]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Unparseable timestamp: {exc}") from exc
    _check_hourly(times)
    temperature = [_number(v, "temperature", i)
                   for i, v in enumerate(series["temperature_2m"])]
    rh = [_number(v, "relative humidity", i)
          for i, v in enumerate(series["relative_humidity_2m"])]
    dew = [_number(v, "dew point", i) for i, v in enumerate(series["dew_point_2m"])]
    _check_rh(rh)
    residual = 0.0
    for i, (t, d, h) in enumerate(zip(temperature, dew, rh)):
        if d > t:
            raise ValueError(f"Dew point above temperature at index {i}")
        residual = max(residual, abs(magnus_rh(t, d) - h))
        if abs(magnus_rh(t, d) - h) > RH_TOLERANCE:
            raise ValueError(
                f"Relative humidity inconsistent with temperature and dew point "
                f"at index {i}"
            )
    return {
        "name": "open_meteo_era5", "times": times, "temperature": temperature,
        "rh": rh, "dew_point": dew, "sha256": digest, "bytes": len(raw),
        "source_url": source_url, "retrieved_on": retrieved_on,
        "grid": {"latitude": data.get("latitude"), "longitude": data.get("longitude"),
                 "elevation_m": data.get("elevation")},
        "max_rh_residual": round(residual, 3),
    }


def parse_power(raw: bytes, *, source_url: str, retrieved_on: str,
                expected_sha256: str) -> dict:
    digest = _check_inputs(raw, expected_sha256, source_url, retrieved_on)
    data = _parse_json(raw)
    header = _object(data.get("header", {}), "header")
    if header.get("time_standard") != "UTC":
        raise ValueError("NASA POWER response is not UTC")
    fill = header.get("fill_value")
    units = _object(data.get("parameters", {}), "parameters")
    t_units = _object(units.get("T2M", {}), "parameters.T2M")
    h_units = _object(units.get("RH2M", {}), "parameters.RH2M")
    if t_units.get("units") != "C" or h_units.get("units") != "%":
        raise ValueError("Unexpected NASA POWER units")
    properties = _object(data.get("properties", {}), "properties")
    parameter = _object(properties.get("parameter", {}), "properties.parameter")
    t_map, h_map = parameter.get("T2M"), parameter.get("RH2M")
    if not isinstance(t_map, dict) or not isinstance(h_map, dict):
        raise ValueError("Missing T2M or RH2M series")
    if list(t_map) != list(h_map):
        raise ValueError("T2M and RH2M timestamps differ")
    try:
        times = [datetime.strptime(k, "%Y%m%d%H").replace(tzinfo=timezone.utc)
                 for k in t_map]
    except ValueError as exc:
        raise ValueError(f"Unparseable timestamp: {exc}") from exc
    _check_hourly(times)
    temperature, rh = [], []
    for i, key in enumerate(t_map):
        for source, target, label in ((t_map, temperature, "temperature"),
                                      (h_map, rh, "relative humidity")):
            value = _number(source[key], label, i)
            if fill is not None and value == fill:
                raise ValueError(f"Fill value in {label} at index {i}")
            target.append(value)
    _check_rh(rh)
    geometry = _object(data.get("geometry", {}), "geometry")
    coordinates = geometry.get("coordinates", [None] * 3)
    if not isinstance(coordinates, list) or len(coordinates) < 3:
        raise ValueError("geometry.coordinates must be a list of three values")
    api = header.get("api")
    if not isinstance(api, dict):
        api = {}
    api = {key: api.get(key) for key in ("name", "version")}
    for key, value in api.items():
        if not isinstance(value, str) or not value.strip():
            api[key] = None
    return {
        "name": "nasa_power_merra2", "times": times, "temperature": temperature,
        "rh": rh, "sha256": digest, "bytes": len(raw), "source_url": source_url,
        "retrieved_on": retrieved_on, "api": api,
        "grid": {"longitude": coordinates[0], "latitude": coordinates[1],
                 "elevation_m": coordinates[2]},
    }


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    rank = p / 100 * (len(ordered) - 1)
    low = math.floor(rank)
    high = math.ceil(rank)
    return ordered[low] + (ordered[high] - ordered[low]) * (rank - low)


def _stamp(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%MZ")


def _extreme(series: dict, key: str, other: str, pick) -> dict:
    values = series[key]
    target = pick(values)
    return {
        "value": target,
        "occurrences": [
            {"time": _stamp(t), f"paired_{other}": series[other][i]}
            for i, t in enumerate(series["times"]) if values[i] == target
        ],
    }


def _monthly_extremes(series: dict, key: str, other: str) -> dict:
    indices: dict[str, list[int]] = {}
    for i, t in enumerate(series["times"]):
        indices.setdefault(t.strftime("%Y-%m"), []).append(i)

    def pick(idx: list[int], chooser) -> dict:
        target = chooser(series[key][i] for i in idx)
        return {
            "value": target,
            "occurrences": [
                {"time": _stamp(series["times"][i]),
                 f"paired_{other}": series[other][i]}
                for i in idx if series[key][i] == target
            ],
        }

    return {m: {"minimum": pick(idx, min), "maximum": pick(idx, max)}
            for m, idx in sorted(indices.items())}


def _summary(series: dict, key: str, other: str, unit: str) -> dict:
    values = series[key]
    return {
        "unit": unit,
        "count": len(values),
        "minimum": _extreme(series, key, other, min),
        "maximum": _extreme(series, key, other, max),
        "mean": round(sum(values) / len(values), 3),
        **{f"p{p:02d}": round(percentile(values, p), 3) for p in PERCENTILES},
        "monthly": _monthly_extremes(series, key, other),
    }


def derive(series: dict) -> dict:
    return {
        "temperature": _summary(series, "temperature", "rh", "degC"),
        "relative_humidity": _summary(series, "rh", "temperature", "percent"),
    }


def compare(first: dict, second: dict) -> dict:
    if first["times"] != second["times"]:
        raise ValueError("Sources do not share the exact same UTC hour set")
    n = len(first["times"])

    def stats(key: str) -> dict:
        diffs = [a - b for a, b in zip(first[key], second[key])]
        return {"mean_difference": round(sum(diffs) / n, 3),
                "mean_absolute_difference": round(sum(abs(d) for d in diffs) / n, 3)}

    return {
        "basis": "UTC, matched by timestamp; first source minus second source",
        "first": first["name"], "second": second["name"],
        "common_hour_count": n,
        "start": _stamp(first["times"][0]), "end": _stamp(first["times"][-1]),
        "temperature_degC": stats("temperature"),
        "relative_humidity_percent": stats("rh"),
    }


def _source_block(series: dict, request: dict) -> dict:
    return {
        "request_url": series["source_url"], "retrieved_on": series["retrieved_on"],
        "sha256": series["sha256"], "bytes": series["bytes"],
        "requested_location": request, "returned_grid": series["grid"],
        "period": {"start": _stamp(series["times"][0]),
                   "end": _stamp(series["times"][-1]), "timezone": "UTC",
                   "records": len(series["times"])},
    }


def build_report(primary: dict, secondary: dict, request: dict) -> dict:
    api = secondary["api"]
    if api["name"] and api["version"] and re.fullmatch(r"v?[0-9]+\.[0-9]+\.[0-9]+",
                                                     api["version"]):
        attribution = (
            f"The data was obtained from the POWER Project's {api['name']} "
            f"{api['version']}, retrieved on {secondary['retrieved_on']}; "
            "API identity and version are from the retained source metadata."
        )
    else:
        attribution = (
            "UNVERIFIED: NASA POWER API identity or precise version is unavailable "
            "in the retained source metadata; "
            f"retrieved on {secondary['retrieved_on']}. No version is inferred."
        )
    return {
        "analysis_version": "paired-modelled-hourly-bounds-v1",
        "classification": "MODELLED reanalysis demonstrator sample; not station "
                          "observations",
        "observed": False,
        "selected_demo_source": "open_meteo_era5",
        "sources": {
            "open_meteo_era5": _source_block(primary, request),
            "nasa_power_merra2": {**_source_block(secondary, request), "api": api},
        },
        "licence_and_attribution": {
            **LICENCE,
            "nasa_power": {**LICENCE["nasa_power"], "attribution": attribution},
        },
        "validation": {
            "rejects": ["hash mismatch", "non-HTTPS URL", "unit mismatch",
                        "non-UTC response", "null, non-numeric or fill value",
                        "unequal series length", "gap, duplicate or out-of-order hour",
                        "humidity outside 0..100", "dew point above temperature",
                        "humidity inconsistent with temperature and dew point",
                        "cross-source hour-set mismatch"],
            "humidity_consistency_tolerance_rh_points": RH_TOLERANCE,
            "open_meteo_max_rh_residual_rh_points": primary["max_rh_residual"],
            "formula": "Magnus, 17.625 and 243.04 degC",
            "nothing_filled_or_inferred": True,
        },
        "percentile_rule": PERCENTILE_RULE,
        "bounds": derive(primary),
        "cross_source_check": compare(primary, secondary),
        "nasa_power_bounds_for_sensitivity": derive(secondary),
        "interpretation": "Sample statistics for one grid cell and one calendar "
                          "year, not instantaneous design extremes, region-wide "
                          "bounds, replay limits or safety thresholds. Hourly "
                          "reanalysis smooths terrain and the coast.",
        "owner_reuse_approval": "UNMET",
        "production_status": "pending",
        "production_pending": [
            "station-grade or authorised source (for example MIDAS via an authorised account)",
            "licence and commercial-use confirmation, including underlying C3S terms",
            "precision against observations for the North East",
            "multi-year window and regional representativeness",
            "ERA5 versus ERA5-Land choice",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--open-meteo", type=Path, required=True)
    parser.add_argument("--open-meteo-url", required=True)
    parser.add_argument("--open-meteo-sha256", required=True)
    parser.add_argument("--power", type=Path, required=True)
    parser.add_argument("--power-url", required=True)
    parser.add_argument("--power-sha256", required=True)
    parser.add_argument("--retrieved-on", required=True)
    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--longitude", type=float, required=True)
    args = parser.parse_args()
    try:
        primary = parse_open_meteo(
            args.open_meteo.read_bytes(), source_url=args.open_meteo_url,
            retrieved_on=args.retrieved_on, expected_sha256=args.open_meteo_sha256)
        secondary = parse_power(
            args.power.read_bytes(), source_url=args.power_url,
            retrieved_on=args.retrieved_on, expected_sha256=args.power_sha256)
        report = build_report(primary, secondary, {
            "label": "Durham, North East England",
            "latitude": args.latitude, "longitude": args.longitude})
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False,
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
