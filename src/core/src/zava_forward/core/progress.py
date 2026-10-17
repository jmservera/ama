"""Read-only event evidence and declared delivery scenarios, never inferred history."""

import csv
import io
import json
from datetime import UTC, datetime
from typing import Any

from .insights import STAGE_ORDER

Record = dict[str, Any]
PAUSED = {"Contact paused", "Resident paused works"}
HANDOFF_STATES = {
    "Offered",
    "Received",
    "Escalated",
    "Accepted",
    "Declined",
    "Withdrawn",
    "Completed",
}
STAGES = frozenset(STAGE_ORDER) | {"Completed"}
LIMITS = [
    "Partial coverage: forward progression is not fully recorded as structured UTC events.",
    "Current records, stage_since, days_in_stage, narrative and prose audit are not clocks.",
    "Cohort filters use current authorized records, not reconstructed as-of membership.",
    "Independent safety, resident, technical, quality and finance states are not reconstructed.",
    "A stage, case closure or forecast never establishes accepted handover or financial closure.",
    "Source references are supplied, not verified; missing provenance remains unresolved.",
    "The deterministic baseline neither validates AI nor implies no AI elsewhere.",
]


def timestamp(value: object, label: str) -> datetime:
    if not isinstance(value, str) or "T" not in value:
        raise ValueError(f"{label} must include a date, time and timezone.")
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("Timezone is required.")
        return parsed.astimezone(UTC)
    except (ValueError, OverflowError):
        raise ValueError(f"{label} must include a valid date, time and timezone.") from None


def _iso(value: datetime) -> str:
    return value.isoformat()


def _exception(out: list[Record], code: str, source: str) -> None:
    out.append(dict(code=code, source=source, status="Unresolved"))


def _events(
    case: Record, key: str, as_of: datetime, exceptions: list[Record]
) -> tuple[list[Record], bool]:
    rows = case.get(key, [])
    if not isinstance(rows, list):
        _exception(exceptions, "malformed_history", key)
        return [], False
    result: list[Record] = []
    valid = True
    previous: datetime | None = None
    offer_identity: tuple[str, str, str] | None = None
    for index, raw in enumerate(rows):
        source = f"{key}/{index}"
        if not isinstance(raw, dict):
            _exception(exceptions, "malformed_event", source)
            valid = False
            continue
        try:
            at = timestamp(raw.get("at"), "Event time")
        except ValueError:
            _exception(exceptions, "unknown_event_time", source)
            valid = False
            continue
        if at > as_of:
            continue
        if type(raw.get("version")) is not int or raw["version"] != index + 1:
            _exception(exceptions, "invalid_event_version", source)
            valid = False
        if previous is not None and at < previous:
            _exception(exceptions, "contradictory_event_order", source)
            valid = False
        previous = at
        has_source = isinstance(raw.get("source"), str) and bool(raw["source"].strip())
        actor = raw.get("actor")
        has_actor = (
            isinstance(actor, dict)
            and all(
                isinstance(actor.get(k), str) and actor[k].strip()
                for k in ("email", "code", "name", "role")
            )
        ) or (isinstance(raw.get("by"), str) and bool(raw["by"].strip()))
        if not has_source:
            _exception(exceptions, "unknown_source_reference", source)
        if not has_actor:
            _exception(exceptions, "unknown_event_actor", source)
        version = raw.get("version")
        event = dict(at=_iso(at), version=version if type(version) is int else None, source=source)
        # Raw actors, supplied references and free text are deliberately not exported.
        event["actor_status"] = "Recorded, withheld" if has_actor else "Unknown"
        event["source_status"] = "Supplied, unverified" if has_source else "Unknown"
        if key == "returns":
            old, new = raw.get("from_stage"), raw.get("to_stage")
            if (
                not isinstance(old, str)
                or old not in STAGES
                or not isinstance(new, str)
                or new not in STAGES
                or type(raw.get("reopened")) is not bool
                or old == new
                or (
                    raw.get("reopened") is True
                    and new != ("Aftercare issue" if old == "Completed" else "Contacting resident")
                )
                or (
                    raw.get("reopened") is False
                    and (
                        old == "Completed"
                        or new == "Completed"
                        or STAGE_ORDER.index(new) >= STAGE_ORDER.index(old)
                    )
                )
            ):
                _exception(exceptions, "unmappable_stage_event", source)
                valid = False
                continue
            event.update(
                kind="reopen" if raw["reopened"] else "return",
                from_stage=old,
                to_stage=new,
            )
        else:
            state = raw.get("state")
            if not isinstance(state, str) or state not in HANDOFF_STATES:
                _exception(exceptions, "unmappable_handoff_event", source)
                valid = False
                continue
            if not all(
                isinstance(raw.get(k), str) and raw[k].strip()
                for k in ("from_code", "to_code", "offered_at")
            ):
                _exception(exceptions, "unknown_handoff_identity", source)
                valid = False
            else:
                identity = (raw["from_code"], raw["to_code"], raw["offered_at"])
                if state == "Offered":
                    offer_identity = identity
                elif offer_identity != identity:
                    _exception(exceptions, "contradictory_handoff_identity", source)
                    valid = False
            event.update(kind="handoff", state=state)
        result.append(event)
    return sorted(result, key=lambda e: (e["at"], e["version"] or 0)), valid


def history(case: Record, as_of: datetime, start: datetime | None) -> Record:
    exceptions: list[Record] = []
    transitions, valid = _events(case, "returns", as_of, exceptions)
    handoffs, handoff_valid = _events(case, "handoff_history", as_of, exceptions)
    intervals: list[Record] = []
    if not transitions:
        _exception(exceptions, "unknown_stage_history", "returns")
    else:
        _exception(exceptions, "unknown_initial_stage_entry", transitions[0]["source"])
    for index, event in enumerate(transitions):
        following = transitions[index + 1] if index + 1 < len(transitions) else None
        entered = timestamp(event["at"], "Event time")
        ended = timestamp(following["at"], "Event time") if following else as_of
        consistent = valid
        if following and (event["to_stage"] != following["from_stage"] or entered == ended):
            _exception(exceptions, "contradictory_stage_chain", following["source"])
            consistent = False
        left = max(entered, start) if start else entered
        if left > ended:
            continue
        # No last-event-to-as-of clock: unrecorded forward movement may have occurred.
        if following is None:
            consistent = False
            _exception(exceptions, "unknown_stage_exit", event["source"])
        intervals.append(
            dict(
                stage=event["to_stage"],
                classification="Paused stage" if event["to_stage"] in PAUSED else "Stage",
                entered_at=event["at"],
                ended_at=following["at"] if following else None,
                period_from=_iso(left),
                period_to=_iso(ended),
                elapsed_seconds=(ended - left).total_seconds() if consistent else None,
                status="Observed interval" if consistent else "Unknown",
                source=event["source"],
                end_source=following["source"] if following else None,
            )
        )
    waits: list[Record] = []
    offered: Record | None = None
    state: str | None = None
    allowed = {
        None: {"Offered"},
        "Offered": {"Received", "Escalated", "Accepted", "Declined", "Withdrawn"},
        "Received": {"Escalated", "Accepted", "Declined", "Withdrawn"},
        "Escalated": {"Accepted", "Declined", "Withdrawn"},
        "Accepted": {"Completed"},
        "Declined": {"Offered"},
        "Withdrawn": {"Offered"},
        "Completed": {"Offered"},
    }
    for event in handoffs:
        current = event["state"]
        if current not in allowed[state]:
            _exception(exceptions, "contradictory_handoff_chain", event["source"])
            handoff_valid = False
        if current == "Offered":
            offered = event
        if current in {"Accepted", "Declined", "Withdrawn"}:
            at = timestamp(event["at"], "Event time")
            began = timestamp(offered["at"], "Offer time") if offered else None
            wait_start = max(began, start) if began and start else began
            if wait_start is None or wait_start <= at:
                waits.append(
                    dict(
                        outcome=current,
                        source=event["source"],
                        offered_at=offered["at"] if offered else None,
                        ended_at=event["at"],
                        elapsed_seconds=(at - wait_start).total_seconds()
                        if handoff_valid and wait_start is not None
                        else None,
                    )
                )
            offered = None
        state = current
    if offered is not None:
        _exception(exceptions, "handoff_pending", offered["source"])
        began = timestamp(offered["at"], "Offer time")
        left = max(began, start) if start else began
        waits.append(
            dict(
                outcome="Pending",
                source=offered["source"],
                offered_at=offered["at"],
                ended_at=None,
                elapsed_seconds=(as_of - left).total_seconds() if handoff_valid else None,
                censored=True,
            )
        )
    events = sorted(transitions + handoffs, key=lambda e: (e["at"], e["source"], e["version"] or 0))
    return dict(
        case_id=case["id"],
        coverage="Partial" if events else "Unknown",
        events=[e for e in events if start is None or timestamp(e["at"], "Event time") >= start],
        stage_intervals=intervals,
        handoff_waits=waits,
        exceptions=exceptions,
    )


def _integer(value: object, label: str, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{label} must be a whole number from {minimum} to {maximum}.")
    return value


def _simulate(ready: int, capacity: int, duration: int, weeks: int) -> list[int]:
    installation: list[int] = []
    quality: list[int] = []
    waiting, installed, completed = ready, 0, 0
    cumulative = []
    for week in range(weeks):
        completed += sum(end <= week for end in quality)
        quality = [end for end in quality if end > week]
        installed += sum(end <= week for end in installation)
        installation = [end for end in installation if end > week]
        take = min(installed, capacity - len(quality))
        quality.extend([week + duration] * take)
        installed -= take
        take = min(waiting, capacity - len(installation))
        installation.extend([week + duration] * take)
        waiting -= take
        cumulative.append(completed + sum(end <= week + 1 for end in quality))
    return cumulative


def forecast(denominator: int, scenario: Record | None) -> Record:
    limits = [
        "No verified committed capacity, dependency releases, readiness or outcome calibration.",
        "Ready homes are hypothetical; no current stage or consent establishes readiness.",
        "No target, approved plan, professional judgement, real outcome or promise.",
    ]
    if scenario is None:
        return dict(
            label="Forecast",
            status="Unavailable",
            assumptions=None,
            uncertainty="Unknown without declared scenario inputs",
            data_limits=limits,
        )
    if set(scenario) - {"ready", "capacity", "duration", "weeks"}:
        raise ValueError("Unknown forecast assumption.")
    ready = _integer(scenario.get("ready"), "Scenario ready homes", 0, denominator)
    capacity = _integer(scenario.get("capacity", 2), "Capacity per stage", 1, 1000)
    duration = _integer(scenario.get("duration", 1), "Stage duration weeks", 1, 52)
    weeks = _integer(scenario.get("weeks", 4), "Horizon weeks", 1, 52)
    variants = [
        ("Central", capacity, duration),
        ("Lower capacity", max(1, capacity - 1), duration),
        ("Higher capacity", capacity + 1, duration),
        ("Longer stage duration", capacity, duration * 2),
    ]
    projections: list[Record] = [
        dict(
            name=name,
            capacity_per_stage=cap,
            stage_duration_weeks=days,
            cumulative_handover_scenario=_simulate(ready, cap, days, weeks),
        )
        for name, cap, days in variants
    ]
    return dict(
        label="Forecast",
        status="Declared scenario, not validated",
        assumptions=dict(
            ready=ready,
            held=denominator - ready,
            capacity_per_stage=capacity,
            stage_duration_weeks=duration,
            weeks=weeks,
            resource_pools="Independent installation and QA/handover pools",
            dependencies="All hypothetical ready homes released at week one; no further releases",
            outcome="Hypothetical accepted handovers after both stages; not financial closure",
            source="Case study addendum EXA-009; user-declared scenario inputs",
        ),
        uncertainty="Sensitivity envelope, not a statistical confidence interval",
        data_limits=limits,
        projections=projections,
        lower=[
            min(p["cumulative_handover_scenario"][i] for p in projections) for i in range(weeks)
        ],
        upper=[
            max(p["cumulative_handover_scenario"][i] for p in projections) for i in range(weeks)
        ],
    )


def report(
    cases: list[Record],
    *,
    as_of: object,
    start: object,
    cohort: Record,
    scenario: Record | None,
    audit_intact: bool | None,
) -> Record:
    end = timestamp(as_of, "As-of")
    beginning = timestamp(start, "Period start") if start is not None else None
    if end > datetime.now(UTC):
        raise ValueError("As-of cannot be in the future.")
    if beginning is not None and beginning > end:
        raise ValueError("Period start must not be later than as-of.")
    histories = [history(case, end, beginning) for case in sorted(cases, key=lambda c: c["id"])]
    exceptions = [
        dict(case_id=item["case_id"], **exception)
        for item in histories
        for exception in item["exceptions"]
    ]
    if not cases:
        _exception(exceptions, "empty_authorized_cohort", "cohort")
    if not audit_intact:
        _exception(
            exceptions,
            "audit_integrity_unknown" if audit_intact is None else "audit_integrity_failure",
            "audit",
        )
        for item in histories:
            for interval in item["stage_intervals"] + item["handoff_waits"]:
                interval["elapsed_seconds"] = None
                interval["status"] = "Untrusted"
            item["coverage"] = "Untrusted"
    return dict(
        schema="progress/v1",
        status=("Partial evidence" if cases else "No cohort evidence")
        if audit_intact
        else "Untrusted evidence",
        as_of=_iso(end),
        period_start=_iso(beginning) if beginning else None,
        approval_status="Not reviewed; no operational or human approval",
        cohort=cohort,
        denominators=dict(
            selected_cases=len(cases),
            cases_with_recorded_events=sum(bool(h["events"]) for h in histories),
            cases_without_recorded_events=sum(not h["events"] for h in histories),
            complete_history_cases=0,
            accepted_handover_actuals=None,
        ),
        definitions=dict(
            elapsed_seconds="Calendar UTC seconds between consistent boundaries, clipped to period",
            unknown="Null means unrecorded, unmappable or contradictory; never zero",
            paused="Only Contact paused and Resident paused works observed stage intervals",
            handoff_wait="Offered to Accepted/Declined/Withdrawn; receipt is not acceptance",
            pending_wait="Censored elapsed since observed offer, not a completed handoff",
            stage_interval="Consistent recorded return/reopen boundaries; last exit unknown",
            event_period="Inclusive period; earlier boundaries may support clipped intervals",
            cohort="Current authorized membership in this response, not historical membership",
        ),
        sources=[
            "returns",
            "handoff_history",
            "Current authorized case filters",
            "Existing ledger integrity check; narrative/prose is not parsed",
        ],
        data_limits=LIMITS,
        audit_integrity="Unknown"
        if audit_intact is None
        else "Intact"
        if audit_intact
        else "Failed",
        histories=histories,
        forecast=forecast(len(cases), scenario),
        exceptions=exceptions,
    )


def export_csv(value: Record) -> str:
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["section", "value"])
    for key, item in value.items():
        writer.writerow([key, json.dumps(item, sort_keys=True, separators=(",", ":"))])
    return out.getvalue()
