"""Closed case-field contracts for external context, not semantic text redaction."""

import math
from collections.abc import Mapping

Scalar = str | int | float | bool | None
HOME = ("address", "town", "postcode", "area", "type", "built", "epc", "tenure")
CASE = ("id", "stage", "status", "needs_notice", "named_contact", "waiting_on", "owner")


def scalars(value: object, fields: tuple[str, ...]) -> dict[str, Scalar]:
    """Unknown fields are unauthorized; malformed selected fields explicitly refuse."""
    if not isinstance(value, Mapping):
        raise ValueError("External context requires a field object; use the manual record.")
    result: dict[str, Scalar] = {}
    for key in fields:
        if key not in value:
            continue
        item = value[key]
        if item is not None and type(item) not in (str, int, float, bool):
            raise ValueError("External context has a malformed field; use the manual record.")
        if isinstance(item, float) and not math.isfinite(item):
            raise ValueError("External context has a nonfinite field; use the manual record.")
        result[key] = item
    return result


def measure_values(value: object) -> str | list[str] | None:
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError("External context has malformed measures; use the manual record.")


def chat_case(value: Mapping[str, object]) -> dict[str, object]:
    result: dict[str, object] = dict(scalars(value, CASE))
    if "measures" in value:
        result["measures"] = measure_values(value["measures"])
    for field, keys in (
        ("home", HOME),
        ("resident", ("adjustment", "preferred")),
    ):
        if field in value:
            result[field] = scalars(value[field], keys)
    contacts = value.get("contacts", [])
    if not isinstance(contacts, list):
        raise ValueError("External context has malformed contacts; use the manual record.")
    result["contacts"] = [scalars(c, ("channel", "outcome")) for c in contacts[:4]]
    return result


def status_inputs(value: Mapping[str, object]) -> None:
    """Check raw contributors, not their already-stringified manual status."""
    scalars(value, ("closed", "stage"))
    if value.get("closed"):
        return
    hazards = value.get("hazards", [])
    if not isinstance(hazards, list):
        raise ValueError("External context has malformed hazards; use the manual record.")
    for hazard in hazards:
        fields = scalars(hazard, ("released",))
        if not fields.get("released"):
            scalars(hazard, ("owner",))
            return
    scalars(value, ("waiting_on", "reason"))


def prompt_case(value: Mapping[str, object]) -> None:
    """Validate before legacy interpolation, including citation and briefing fields."""
    status_inputs(value)
    scalars(value, CASE + ("days_in_stage", "reason"))
    for field, keys in (
        ("home", HOME),
        ("resident", ("name", "adjustment", "preferred", "unavailable")),
        ("funding", ("route", "status")),
    ):
        scalars(value.get(field, {}), keys)
    measure_values(value.get("measures"))
    for field, row_keys in (
        ("contacts", ("at", "outcome", "channel")),
        ("hazards", ("category", "released")),
        ("documents", ("name",)),
    ):
        rows = value.get(field, [])
        if not isinstance(rows, list):
            raise ValueError("External context has malformed records; use the manual record.")
        for row in rows:
            scalars(row, row_keys)
    history = value.get("history") or []
    if not isinstance(history, list):
        raise ValueError("External context has malformed history; use the manual record.")
    for event in history:
        if isinstance(event, Mapping):
            scalars(event, ("at",))


def map_case(value: Mapping[str, object]) -> None:
    scalars(value, ("id", "stage", "days_in_stage"))
    scalars(value.get("resident", {}), ("name",))
    home = scalars(value.get("home", {}), ("address", "postcode", "lat", "lon"))
    if any(type(home.get(key)) not in (int, float) for key in ("lat", "lon")):
        raise ValueError("Map coordinates are unavailable; use the manual record.")
