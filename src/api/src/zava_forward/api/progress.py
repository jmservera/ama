"""Read-only demonstration progress and archive views over explicitly synthetic cases."""

from __future__ import annotations

import math
import re
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from typing import Any, Literal

from zava_forward.core import insights, projection, taskqueues
from zava_forward.core.workflows import MANAGER_ROLES, handoff_view

DAY = timedelta(days=1)
JOURNEY = {
    "Survey": insights.STAGE_ORDER[:8],
    "Assessment": insights.STAGE_ORDER[8:13],
    "Funding": ["Funding check", "Final checks before ordering"],
    "Resident agreement": ["Waiting for resident decision", "Resident paused works"],
    "Contractor": [
        "Waiting for block programme",
        "With contractor",
        "Install booked",
        "Works under way",
    ],
    "Quality and handover": [
        "Handover to arrange",
        "Quality check",
        "Closing down",
        "Aftercare issue",
    ],
}
STEP = {stage: name for name, stages in JOURNEY.items() for stage in stages}
CLOSE_ACTIONS = {"Accepted handover", "Withdrawn", "Excluded"}
LifecycleKind = Literal["identified", "accepted", "closure", "reopened", "returned"]


class DateRangeError(ValueError):
    """The selected start and end dates do not form a supported range."""


def parameters(query: dict[str, list[str]], accepted: set[str]) -> dict[str, str]:
    if set(query) - accepted or any(len(values) != 1 for values in query.values()):
        raise ValueError("Use each supported filter once.")
    return {key: values[0] for key, values in query.items()}


def day(value: str) -> date:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("Enter dates as YYYY-MM-DD.")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError("Enter a valid calendar date.") from None


def observed(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return stamp.replace(tzinfo=UTC) if stamp.tzinfo is None else stamp.astimezone(UTC)
    except (ValueError, OverflowError):
        return None


def synthetic(case: dict[str, Any]) -> bool:
    if "is_synthetic" in case:
        return case["is_synthetic"] is True
    history = case.get("history")
    return (
        isinstance(history, list)
        and bool(history)
        and all(isinstance(row, dict) and row.get("is_synthetic") is True for row in history)
    )


def lifecycle(case: dict[str, Any]) -> list[tuple[date, bool]] | None:
    """Return observed open/close transitions; contradictory or partial history is unknown."""
    history = case.get("history")
    closures = case.get("home_case_closures", [])
    returns = case.get("returns", [])
    if (
        not isinstance(history, list)
        or not all(isinstance(row, dict) for row in history)
        or not isinstance(closures, list)
        or not all(isinstance(row, dict) for row in closures)
        or not isinstance(returns, list)
        or not all(isinstance(row, dict) for row in returns)
    ):
        return None
    events: list[tuple[datetime, LifecycleKind]] = []
    for row in history:
        if row.get("is_synthetic") is not True:
            continue
        action = row.get("action")
        if not isinstance(action, str):
            return None
        if action in CLOSE_ACTIONS or action in {"Identified", "Reopened - aftercare"}:
            stamp = observed(row.get("at"))
            if stamp is None:
                return None
            if action == "Identified":
                kind: LifecycleKind = "identified"
            elif action == "Reopened - aftercare":
                kind = "reopened"
            elif action == "Accepted handover":
                kind = "accepted"
            else:
                kind = "closure"
            events.append((stamp, kind))
    for row in closures:
        if row.get("event_type") == "human_home_case_closed" or row.get("closed") is True:
            stamp = observed(row.get("at"))
            if stamp is None:
                return None
            events.append((stamp, "closure"))
    for row in returns:
        if row.get("reopened") is True or row.get("event_type") == "reopen":
            stamp = observed(row.get("at"))
            if stamp is None:
                return None
            events.append((stamp, "reopened"))
        elif row.get("event_type") == "return" or (
            "event_type" not in row and row.get("reopened") is False
        ):
            stamp = observed(row.get("at"))
            if stamp is None:
                return None
            events.append((stamp, "returned"))
    events.sort(key=lambda event: event[0])
    transitions: list[tuple[date, bool]] = []
    state = False
    last_change: tuple[datetime, LifecycleKind] | None = None
    for stamp, kind in events:
        if kind == "returned":
            if not state:
                return None
            continue
        # Repeated observations cannot cross an intervening episode boundary.
        if last_change and stamp == last_change[0]:
            if kind == last_change[1] or (
                kind in ("accepted", "closure") and last_change[1] in ("accepted", "closure")
            ):
                continue
        if kind == "identified":
            if transitions:
                return None
            opened = True
        elif kind == "reopened":
            if not transitions or state:
                return None
            opened = True
        else:
            if not state:
                return None
            opened = False
        transitions.append((stamp.date(), opened))
        state = opened
        last_change = (stamp, kind)
    if not transitions or state == bool(case.get("closed")):
        return None
    return transitions


def require_staff(user: dict[str, Any]) -> None:
    if user.get("role") not in projection.STAFF_ROLES:
        raise PermissionError("Only authorised staff can read demonstration progress.")


def date_range(values: dict[str, str], as_of: str) -> tuple[date, date]:
    end = day(values.get("end") or as_of)
    try:
        start = day(values["start"]) if values.get("start") else end - timedelta(days=29)
    except OverflowError:
        raise ValueError("Choose a date range within supported calendar dates.") from None
    if start > end or (end - start).days > 365:
        raise DateRangeError("Choose an end date on or after the start, covering at most 366 days.")
    return start, end


def _series(counter: Counter[str], labels: list[str] | None = None) -> list[dict[str, Any]]:
    return [{"label": label, "count": counter[label]} for label in labels or sorted(counter)]


def _ai(records: list[dict[str, Any]], ids: set[str], start: date, end: date) -> dict[str, Any]:
    outcomes: Counter[str] = Counter()
    unreviewed = unknown_date = non_ai = eligible = 0
    for record in records:
        links = record.get("case_ids")
        if (
            record.get("is_synthetic") is not True
            or record.get("task") != "briefing"
            or not isinstance(links, list)
            or not links
            or not all(isinstance(cid, str) and cid in ids for cid in links)
        ):
            continue
        eligible += 1
        if record.get("source") != "ai":
            non_ai += 1
            continue
        status = record.get("status")
        if status not in {"Accepted", "Edited", "Rejected"}:
            unreviewed += 1
            continue
        stamp = observed(record.get("resolved_at"))
        if stamp is None:
            unknown_date += 1
        elif start <= stamp.date() <= end:
            outcomes[{"Edited": "Changed"}.get(status, status)] += 1
    return dict(
        outcomes=_series(outcomes, ["Accepted", "Changed", "Rejected"]),
        eligible_records=eligible,
        unreviewed_or_unavailable=unreviewed,
        unknown_review_date=unknown_date,
        rules_or_templates=non_ai,
        basis="Explicitly synthetic AI briefing reviews recorded in the selected UTC dates.",
    )


def dashboard(store: Any, user: dict[str, Any], query: dict[str, list[str]]) -> dict[str, Any]:
    require_staff(user)
    values = parameters(query, {"start", "end"})
    with store.lock:
        start, end = date_range(values, store.as_of)
        cases = [case for case in store.cases.values() if synthetic(case)]
        histories = [lifecycle(case) for case in cases]
        valid = [events for events in histories if events is not None]
        opened: Counter[date] = Counter()
        closed: Counter[date] = Counter()
        reopened: Counter[date] = Counter()
        durations: list[int] = []
        for events in valid:
            episode = None
            for index, (when, active) in enumerate(events):
                if active:
                    opened[when] += 1
                    reopened[when] += index > 0
                    episode = when
                else:
                    closed[when] += 1
                    if episode is not None and start <= when <= end:
                        durations.append((when - episode).days)
        backlog = sum(n for when, n in opened.items() if when < start) - sum(
            n for when, n in closed.items() if when < start
        )
        daily = []
        weeks: dict[date, dict[str, Any]] = {}
        for offset in range((end - start).days + 1):
            when = start + DAY * offset
            backlog += opened[when] - closed[when]
            row = dict(
                date=when.isoformat(),
                opened=opened[when],
                closed=closed[when],
                reopened=reopened[when],
                backlog=backlog,
            )
            daily.append(row)
            monday = when - DAY * when.weekday()
            week = weeks.setdefault(
                monday,
                dict(date=monday.isoformat(), opened=0, closed=0, reopened=0, backlog=0),
            )
            for key in ("opened", "closed", "reopened"):
                week[key] += row[key]
            week["backlog"] = backlog
        current = [case for case in cases if not case.get("closed")]
        steps = Counter(STEP.get(case.get("stage"), "Unknown") for case in current)
        teams = Counter(case.get("owner_role") or "Unknown" for case in current)
        stalled = sum(case.get("days_in_stage", 0) >= insights.LONG_WAIT for case in current)
        overdue = sum(
            bool(taskqueues.overdue_tasks(case, as_of=store.as_of, handoff=handoff_view(case)))
            for case in current
        )
        durations.sort()
        count = len(durations)
        median = (durations[(count - 1) // 2] + durations[count // 2]) / 2 if count else None
        return dict(
            label="Demonstration data",
            start=start.isoformat(),
            end=end.isoformat(),
            as_of=store.as_of,
            coverage=dict(
                synthetic_cases=len(cases),
                excluded_unmarked=len(store.cases) - len(cases),
                known_lifecycle=len(valid),
                unknown_lifecycle=len(cases) - len(valid),
            ),
            daily=daily,
            weekly=list(weeks.values()),
            time_to_close=dict(
                median_days=median,
                p90_days=durations[math.ceil(count * 0.9) - 1] if count else None,
                samples=count,
            ),
            current=dict(
                open=len(current),
                stalled=stalled,
                overdue=overdue,
                journey=_series(steps, [*JOURNEY, "Unknown"]),
                teams=_series(teams),
            ),
            ai=_ai(store.data.get("recommendations", []), {c["id"] for c in cases}, start, end),
        )


def closed_cases(store: Any, user: dict[str, Any], query: dict[str, list[str]]) -> dict[str, Any]:
    require_staff(user)
    if user.get("role") not in MANAGER_ROLES:
        raise PermissionError("Only a manager can see closed cases.")
    values = parameters(query, {"start", "end", "status", "team", "q", "page", "limit"})
    start = day(values["start"]) if values.get("start") else None
    end = day(values["end"]) if values.get("end") else None
    if start and end and start > end:
        raise DateRangeError("Choose an end date on or after the start.")
    numbers = []
    for name, default, maximum in (("page", "1", 10**9), ("limit", "20", 100)):
        text = values.get(name, default)
        if not re.fullmatch(r"[0-9]{1,10}", text) or not 1 <= int(text) <= maximum:
            raise ValueError(f"Choose a {name} between 1 and {maximum}.")
        numbers.append(int(text))
    page, limit = numbers
    if len(values.get("q", "")) > 200:
        raise ValueError("Keep search text to 200 characters or fewer.")
    with store.lock:
        candidates = [
            case for case in store.cases.values() if case.get("closed") and synthetic(case)
        ]
        statuses = sorted({case.get("stage") or "Unknown" for case in candidates})
        teams = sorted({case.get("owner_role") or "Unknown" for case in candidates})
        rows = []
        unknown_dates = 0
        for case in candidates:
            events = lifecycle(case)
            closure = events[-1][0] if events and not events[-1][1] else None
            unknown_dates += closure is None
            status, team = case.get("stage") or "Unknown", case.get("owner_role") or "Unknown"
            if values.get("status") and values["status"] != status:
                continue
            if values.get("team") and values["team"] != team:
                continue
            if (start or end) and (
                closure is None or (start and closure < start) or (end and closure > end)
            ):
                continue
            summary = store.summary(dict(case, stage=status))
            text = " ".join(
                str(summary.get(key, ""))
                for key in ("id", "resident", "address", "town", "postcode")
            )
            if values.get("q", "").casefold().strip() not in text.casefold():
                continue
            rows.append(
                dict(
                    id=case["id"],
                    resident=summary["resident"],
                    address=summary["address"],
                    town=summary["town"],
                    postcode=summary["postcode"],
                    hazard=summary["hazard"],
                    status=status,
                    team=team,
                    closed_on=closure.isoformat() if closure else None,
                )
            )
        rows.sort(key=lambda row: row["id"])
        total = len(rows)
        pages = max(1, math.ceil(total / limit))
        page = min(page, pages)
        offset = (page - 1) * limit
        return dict(
            label="Demonstration data",
            items=rows[offset : offset + limit],
            total=total,
            page=page,
            pages=pages,
            limit=limit,
            facets=dict(statuses=statuses, teams=teams),
            unknown_closure_dates=unknown_dates,
        )
