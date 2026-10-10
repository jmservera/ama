"""Pure, deterministic exercise scheduler with separate installation and QA pools."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date

INPUT_VERSION = "exercise-forecast-input-1"
OUTPUT_VERSION = "exercise-forecast-output-1"
SOURCE_MAX_AGE: dict[str, int] = {
    "stock": 30, "assessment": 180, "resident_choice": 30,
    "funding": 7, "capacity": 7, "safety": 1,
}


@dataclass(frozen=True)
class Stage:
    """Concurrent occupied slots and whole-week duration, not throughput limits."""

    slots: tuple[int, ...]
    duration: int


@dataclass(frozen=True)
class Home:
    """Minimum non-identifying cohort input; ready asserts scenario prerequisites."""

    id: str
    priority: int
    state: str
    hold_reason: str


@dataclass(frozen=True)
class Event:
    """A home-specific start-week hold/withdrawal or end-week QA return."""

    week: int
    home_id: str
    kind: str
    reason: str


class InputError(ValueError):
    """Mandatory forecast inputs cannot support a prediction."""


def _mapping(value: object, path: str) -> Mapping:
    if not isinstance(value, Mapping):
        raise InputError(f"{path}: missing or invalid object")
    return value


def _positive(value: object, path: str, *, allow_zero: bool = False) -> int:
    if type(value) is not int or value < (0 if allow_zero else 1):
        raise InputError(f"{path}: expected {'nonnegative' if allow_zero else 'positive'} integer")
    return value


def _text(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{path}: missing text/version")
    return value


def _date(value: object, path: str) -> date:
    try:
        return date.fromisoformat(_text(value, path))
    except ValueError as error:
        raise InputError(f"{path}: expected ISO date") from error


def _stage(value: object, path: str, weeks: int) -> Stage:
    data = _mapping(value, path)
    slots = data.get("slots")
    if not isinstance(slots, list) or len(slots) != weeks:
        raise InputError(f"{path}.slots: supply one concurrent slot count per week")
    return Stage(tuple(_positive(n, f"{path}.slots", allow_zero=True) for n in slots),
                 _positive(data.get("duration_weeks"), f"{path}.duration_weeks"))


def _versions(inputs: Mapping, as_of: date) -> dict[str, str]:
    sources = _mapping(inputs.get("sources"), "sources")
    versions = {}
    for key, maximum in SOURCE_MAX_AGE.items():
        source = _mapping(sources.get(key), f"sources.{key}")
        versions[key] = _text(source.get("version"), f"sources.{key}.version")
        observed = _date(source.get("observed_at"), f"sources.{key}.observed_at")
        age = (as_of - observed).days
        if not 0 <= age <= maximum:
            raise InputError(f"sources.{key}: future or stale input (age {age}, trigger {maximum} days)")
    return versions


def _homes(inputs: Mapping, versions: Mapping[str, str]) -> tuple[list[Home], list[dict[str, str]]]:
    rows = inputs.get("homes")
    if not isinstance(rows, list) or len(rows) != inputs.get("denominator"):
        raise InputError("homes: exact declared denominator must reconcile to distinct input rows")
    homes, unknowns, ids = [], [], set()
    for row in rows:
        data = _mapping(row, "homes[]")
        home_id = _text(data.get("id"), "homes[].id")
        if home_id in ids:
            raise InputError(f"homes: duplicate ID {home_id}")
        ids.add(home_id)
        priority = _positive(data.get("priority"), f"{home_id}.priority", allow_zero=True)
        state = data.get("state")
        bindings = data.get("source_versions", versions)
        if state not in ("ready", "held") or bindings != versions:
            unknowns.append({"home_id": home_id, "reason": "Missing readiness or mismatched source versions"})
            continue
        if state == "held" and data.get("release_week") is not None:
            raise InputError(f"{home_id}: hold releases are unknown; explicit future release is unsupported")
        reason = _text(data.get("hold_reason"), f"{home_id}.hold_reason") if state == "held" else ""
        homes.append(Home(home_id, priority, state, reason))
    return sorted(homes, key=lambda home: (home.priority, home.id)), unknowns


def _events(inputs: Mapping, homes: list[Home], weeks: int) -> list[Event]:
    rows = inputs.get("events")
    if not isinstance(rows, list):
        raise InputError("events: mandatory schedule missing (use [] for no events)")
    ids = {home.id for home in homes}
    events, seen = [], set()
    for row in rows:
        data = _mapping(row, "events[]")
        week = _positive(data.get("week"), "events[].week")
        home_id = _text(data.get("home_id"), "events[].home_id")
        kind = data.get("kind")
        if week > weeks or home_id not in ids or kind not in ("hold", "withdrawal", "qa_return"):
            raise InputError("events: unknown home, week or event kind")
        key = (week, home_id)
        if key in seen:
            raise InputError("events: conflicting events for one home/week")
        seen.add(key)
        events.append(Event(week, home_id, kind, _text(data.get("reason"), "events[].reason")))
    return events


def _base(inputs: Mapping) -> dict[str, object]:
    sources = inputs.get("sources")
    versions = {key: source.get("version") for key, source in sources.items()
                if isinstance(source, Mapping)} if isinstance(sources, Mapping) else {}
    return {
        "version": OUTPUT_VERSION, "input_version": inputs.get("version"),
        "fixture_version": inputs.get("fixture_version"), "as_of": inputs.get("as_of"),
        "scenario": inputs.get("scenario"), "cohort_id": inputs.get("cohort_id"),
        "denominator": inputs.get("denominator"), "numerator": "Accepted QA/resident handovers",
        "source_versions": versions, "status": "abstained", "cumulative_handovers": None,
        "coverage": {"denominator": inputs.get("denominator"), "known": 0, "unknown": inputs.get("denominator"),
                     "ready": 0, "held": 0, "fraction": 0},
        "exclusions": [], "unknowns": [], "tables": {"weekly": [], "schedule": []},
        "note": "Constructed handovers, not starts, financial closure, confidence intervals or company outcomes.",
    }


def forecast(inputs: Mapping[str, object], *, evaluated_as_of: str | None = None) -> dict[str, object]:
    """Forecast four weeks from a manifest-shaped input without mutating it.

    Missing/stale mandatory cohort evidence abstains. Unknown home readiness or
    source bindings are excluded visibly and yield partial, unscored coverage.
    Holds never release automatically. QA returns occupy a full later QA stage.
    """
    result = _base(inputs)
    try:
        if inputs.get("version") != INPUT_VERSION:
            raise InputError("version: unsupported forecast input version")
        if inputs.get("fixture_version") != "properwarm-exercise-1":
            raise InputError("fixture_version: unsupported exercise fixture version")
        _text(inputs.get("cohort_id"), "cohort_id")
        _positive(inputs.get("denominator"), "denominator")
        frozen_date = _date(inputs.get("as_of"), "as_of")
        evaluation = _date(evaluated_as_of, "evaluated_as_of") if evaluated_as_of else frozen_date
        if evaluation < frozen_date:
            raise InputError("evaluated_as_of: cannot precede the frozen input date")
        result["evaluated_as_of"] = evaluation.isoformat()
        if inputs.get("weeks") != 4:
            raise InputError("weeks: this exercise contract requires exactly four weeks")
        installation = _stage(inputs.get("installation"), "installation", 4)
        qa = _stage(inputs.get("qa_handover"), "qa_handover", 4)
        versions = _versions(inputs, evaluation)
        result["source_versions"] = versions
        homes, unknowns = _homes(inputs, versions)
        events = _events(inputs, homes, 4)
        result["unknowns"] = unknowns
        held = [home for home in homes if home.state == "held"]
        ready = [home for home in homes if home.state == "ready"]
        result["coverage"] = {
            "denominator": inputs["denominator"], "known": len(homes), "unknown": len(unknowns),
            "ready": len(ready), "held": len(held), "fraction": len(homes) / inputs["denominator"],
        }
        result["exclusions"] = (
            [{"home_id": home.id, "reason": home.hold_reason, "kind": "initial_hold",
              "release_week": None} for home in held]
            + [dict(row, kind="unknown_input") for row in unknowns]
        )
        if not homes:
            return result
        weekly, schedule = _simulate(ready, events, installation, qa, result["exclusions"])
        result.update(status="partial" if unknowns else "forecast",
                      cumulative_handovers=[row["cumulative_handovers"] for row in weekly],
                      tables={"weekly": weekly, "schedule": schedule})
    except InputError as error:
        result.update(status="abstained", cumulative_handovers=None,
                      tables={"weekly": [], "schedule": []})
        result["unknowns"] = [*result["unknowns"], {"home_id": None, "reason": str(error)}]
    return result


def _simulate(homes: list[Home], events: list[Event], installation: Stage, qa: Stage,
              exclusions: list[dict[str, object]]) -> tuple[list[dict], list[dict]]:
    ranks = {home.id: (home.priority, home.id) for home in homes}
    pending = {home.id for home in homes}
    installed: dict[str, int] = {}
    active_install: dict[str, int] = {}
    active_qa: dict[str, int] = {}
    accepted: set[str] = set()
    blocked: set[str] = set()
    weekly, schedule = [], []
    for week in range(1, 5):
        this_week = [event for event in events if event.week == week]
        for event in this_week:
            if event.kind == "qa_return":
                continue
            if event.home_id in accepted:
                raise InputError("events: cannot retrospectively cancel an accepted handover")
            blocked.add(event.home_id)
            for entry in schedule:
                if (entry["home_id"] == event.home_id and entry["stage"] != "qa_return"
                        and entry["start_week"] < week <= entry["end_week"]):
                    entry["cancelled_at_start_week"] = week
            pending.discard(event.home_id)
            installed.pop(event.home_id, None)
            active_install.pop(event.home_id, None)
            active_qa.pop(event.home_id, None)
            exclusions.append({"home_id": event.home_id, "kind": event.kind,
                               "week": week, "reason": event.reason, "release_week": None})
        qa_candidates = {home_id for home_id, completed in installed.items()
                         if completed < week and home_id not in active_qa
                         and home_id not in accepted and home_id not in blocked}
        _start(qa_candidates, active_qa, qa, week, "qa_handover", schedule, ranks)
        started = _start(pending, active_install, installation, week, "installation", schedule, ranks)
        pending.difference_update(started)
        install_occupied, qa_occupied = len(active_install), len(active_qa)
        completed_install = sorted(home_id for home_id, finish in active_install.items() if finish == week)
        for home_id in completed_install:
            installed[home_id] = week
            del active_install[home_id]
        completed_qa = sorted(home_id for home_id, finish in active_qa.items() if finish == week)
        returned = {event.home_id for event in this_week if event.kind == "qa_return"}
        if not returned <= set(completed_qa):
            raise InputError("events.qa_return: must match a scheduled end-of-week QA completion")
        newly_accepted = []
        for home_id in completed_qa:
            del active_qa[home_id]
            if home_id in returned:
                installed[home_id] = week
                schedule.append({"home_id": home_id, "stage": "qa_return", "start_week": week,
                                 "end_week": week, "accepted": False})
            else:
                accepted.add(home_id)
                newly_accepted.append(home_id)
        weekly.append({
            "week": week, "installation_slots": installation.slots[week - 1],
            "qa_slots": qa.slots[week - 1], "installation_occupied": install_occupied,
            "qa_occupied": qa_occupied, "installed_ids": completed_install,
            "accepted_ids": newly_accepted, "cumulative_handovers": len(accepted),
        })
    return weekly, schedule


def _start(candidates: set[str], active: dict[str, int], stage: Stage, week: int,
           name: str, schedule: list[dict], ranks: Mapping[str, tuple[int, str]]) -> list[str]:
    last_week = min(4, week + stage.duration - 1)
    available = max(0, min(
        stage.slots[occupied_week - 1] - sum(finish >= occupied_week for finish in active.values())
        for occupied_week in range(week, last_week + 1)
    ))
    started = sorted(candidates, key=ranks.__getitem__)[:available]
    for home_id in started:
        finish = week + stage.duration - 1
        active[home_id] = finish
        schedule.append({"home_id": home_id, "stage": name, "start_week": week, "end_week": finish})
    return started


def compare_oracle(result: Mapping[str, object], expected: Mapping[str, object]) -> dict[str, object]:
    """Score complete predictions only; abstentions/partial coverage have null errors."""
    score = {"status": "Not scored", "week_four_absolute_error": None,
             "weekly_cumulative_mae": None, "within_thresholds": None}
    actual = result.get("cumulative_handovers")
    oracle = expected.get("cumulative_handovers")
    if result.get("status") != "forecast" or oracle is None:
        return score
    if not all(isinstance(series, list) and len(series) == 4
               and all(type(n) is int and n >= 0 for n in series) for series in (actual, oracle)):
        raise ValueError("Oracle comparison requires two four-week nonnegative integer series.")
    errors = [abs(a - b) for a, b in zip(actual, oracle)]
    score.update(status="Scored", week_four_absolute_error=errors[-1],
                 weekly_cumulative_mae=sum(errors) / 4,
                 within_thresholds=errors[-1] <= 2 and sum(errors) / 4 <= 1)
    return score
