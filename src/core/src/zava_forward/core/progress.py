"""Read-only event evidence and declared delivery scenarios, never inferred history."""

import csv
import io
import json
import re
from datetime import UTC, datetime, timedelta
from typing import Any

from .insights import STAGE_ORDER
from .quality import EVENT_TYPES, TRANSITIONS

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
    "Partial coverage: only controlled writers capture prospective events; past gaps remain.",
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


def _handoff_latest(raw: Record, at: datetime) -> datetime:
    def minute(value: object) -> bool:
        return (
            isinstance(value, str)
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})", value)
            is not None
        )

    state = raw.get("state")
    if not isinstance(state, str) or state not in HANDOFF_STATES:
        return at
    truncated = minute(raw["at"])
    # Only these legacy writers also recorded a minute-resolution state timestamp.
    field = {
        "Received": "received_at",
        "Escalated": "escalated_at",
        "Declined": "answered_at",
        "Withdrawn": "answered_at",
        "Completed": "completed_at",
    }.get(state)
    recorded = raw.get(field) if field else None
    expanded_minute = (
        re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:00(?:Z|[+-]\d{2}:\d{2})", raw["at"])
        is not None
    )
    if expanded_minute and minute(recorded) and timestamp(recorded, "State time") == at:
        truncated = True
    return at + timedelta(seconds=59, microseconds=999999) if truncated else at


def _latest(raw: Record, key: str, at: datetime) -> datetime:
    if key == "handoff_history":
        return _handoff_latest(raw, at)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})", raw["at"]):
        return at + timedelta(seconds=59, microseconds=999999)
    return at


def _provenance(raw: Record) -> Record:
    actor = raw.get("actor")
    owner = raw.get("receiving_owner")
    has_owner = isinstance(owner, dict) and any(
        all(isinstance(owner.get(k), str) and owner[k].strip() for k in fields)
        for fields in (("owner", "owner_code", "owner_role"), ("name", "code", "role"))
    )
    return dict(
        owner_status="Recorded, withheld" if has_owner else "Unknown",
        source_version_status="Recorded, withheld"
        if isinstance(raw.get("source_version"), str) and raw["source_version"].strip()
        else "Unknown",
        actor_status="Recorded, withheld"
        if isinstance(actor, dict)
        and all(
            isinstance(actor.get(k), str) and actor[k].strip()
            for k in ("email", "code", "name", "role")
        )
        else "Unknown",
        source_status="Supplied, unverified"
        if isinstance(raw.get("source"), str) and raw["source"].strip()
        else "Unknown",
    )


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
    cutoff = False
    offer_identity: tuple[str, str, str] | None = None
    for index, raw in enumerate(rows):
        source = f"{key}/{index}"
        if not isinstance(raw, dict):
            _exception(exceptions, "malformed_event", source)
            valid = False
            continue
        try:
            at = timestamp(raw.get("at"), "Event time")
            latest = _latest(raw, key, at)
        except ValueError:
            _exception(exceptions, "unknown_event_time", source)
            valid = False
            continue
        if type(raw.get("version")) is not int or raw["version"] != index + 1:
            _exception(exceptions, "invalid_event_version", source)
            valid = False
        if previous is not None and latest < previous:
            _exception(exceptions, "contradictory_event_order", source)
            valid = False
        previous = max(previous, at) if previous else at
        if at > as_of:
            cutoff = True
            continue
        if latest > as_of or cutoff:
            _exception(exceptions, "unknown_event_as_of", source)
            valid = False
            cutoff = True
            continue
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
        event.update(_provenance(raw))
        event["time_precision"] = "Minute (legacy writer)" if latest != at else "Recorded instant"
        event["latest_possible_at"] = _iso(latest)
        if latest != at:
            _exception(exceptions, "unknown_event_precision", source)
        # Raw actors, supplied references and free text are deliberately not exported.
        event["actor_status"] = "Recorded, withheld" if has_actor else "Unknown"
        event["source_status"] = "Supplied, unverified" if has_source else "Unknown"
        if key == "returns":
            old, new = raw.get("from_stage"), raw.get("to_stage")
            advance = raw.get("event_type") == "advance"
            if (
                not isinstance(old, str)
                or old not in STAGES
                or not isinstance(new, str)
                or new not in STAGES
                or type(raw.get("reopened")) is not bool
                or old == new
                or (
                    raw.get("event_type") is not None
                    and (
                        not isinstance(raw["event_type"], str)
                        or raw["event_type"] not in {"advance", "return", "reopen"}
                    )
                )
                or (
                    advance
                    and (old, new, raw["reopened"])
                    != ("Final checks before ordering", "Install booked", False)
                )
                or (raw.get("event_type") == "reopen" and raw["reopened"] is not True)
                or (raw.get("event_type") == "return" and raw["reopened"] is not False)
                or (
                    raw.get("reopened") is True
                    and new != ("Aftercare issue" if old == "Completed" else "Contacting resident")
                )
                or (
                    raw.get("reopened") is False
                    and not advance
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
                kind="advance" if advance else "reopen" if raw["reopened"] else "return",
                from_stage=old,
                to_stage=new,
            )
        else:
            state = raw.get("state")
            if not isinstance(state, str) or state not in HANDOFF_STATES:
                _exception(exceptions, "unmappable_handoff_event", source)
                valid = False
                continue
            event_type = "handoff_" + state.lower()
            if raw.get("event_type") is not None and raw["event_type"] != event_type:
                _exception(exceptions, "unmappable_handoff_event", source)
                valid = False
            event["event_type"] = event_type
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
    return result, valid


def _quality_history(
    case: Record, as_of: datetime, start: datetime | None, exceptions: list[Record]
) -> tuple[list[Record], list[Record]]:
    records = case.get("quality", [])
    events: list[Record] = []
    pairs: list[Record] = []
    if not isinstance(records, list):
        _exception(exceptions, "malformed_quality_history", "quality")
        return events, pairs
    for record_index, rec in enumerate(records):
        root = f"quality/{record_index}"
        if not isinstance(rec, dict) or not isinstance(rec.get("history"), list):
            _exception(exceptions, "malformed_quality_history", root)
            continue
        if not rec["history"]:
            _exception(exceptions, "unknown_quality_history", root)
        valid = True
        previous: datetime | None = None
        state: str | None = None
        accepted: Record | None = None
        observed: list[Record] = []
        superseded_at = None
        for index, raw in enumerate(rec["history"]):
            source = f"{root}/history/{index}"
            if not isinstance(raw, dict):
                _exception(exceptions, "malformed_quality_event", source)
                valid = False
                continue
            try:
                at = timestamp(raw.get("at"), "Quality time")
                latest = _latest(raw, "quality", at)
            except ValueError:
                _exception(exceptions, "unknown_event_time", source)
                valid = False
                continue
            if at > as_of:
                break
            if latest > as_of:
                _exception(exceptions, "unknown_event_as_of", source)
                valid = False
                break
            version = raw.get("evidence_version")
            to = raw.get("to_state")
            mapped = isinstance(to, str) and to in EVENT_TYPES
            kind = EVENT_TYPES.get(to) if isinstance(to, str) else None
            if (
                type(raw.get("version")) is not int
                or raw["version"] != index + 1
                or type(version) is not int
                or version < 1
                or type(rec.get("evidence_version")) is not int
                or version != rec.get("evidence_version")
                or not mapped
                or raw.get("event_type") != kind
                or raw.get("source") != f"{root}/evidence/{version}"
                or raw.get("source_version") != str(version)
                or not isinstance(raw.get("checklist_version"), str)
                or not raw["checklist_version"].strip()
                or raw["checklist_version"] != rec.get("checklist_version")
            ):
                _exception(exceptions, "unknown_quality_event_contract", source)
                valid = False
            if (
                raw.get("from_state") != state
                or (state is None and to != "Submitted")
                or (state is not None and to not in (*TRANSITIONS.get(state, ()), "Superseded"))
                or (previous is not None and latest < previous)
            ):
                _exception(exceptions, "contradictory_quality_chain", source)
                valid = False
            previous = max(previous, at) if previous else at
            state = to if mapped else None
            provenance = _provenance(raw)
            if any(value == "Unknown" for value in provenance.values()):
                _exception(exceptions, "unknown_quality_provenance", source)
                valid = False
            if latest != at:
                _exception(exceptions, "unknown_event_precision", source)
            event = dict(
                at=_iso(at),
                latest_possible_at=_iso(latest),
                time_precision="Recorded instant" if latest == at else "Minute (legacy writer)",
                version=raw.get("version") if type(raw.get("version")) is int else None,
                evidence_version=version if type(version) is int else None,
                source=source,
                kind=kind or "unknown",
                **provenance,
            )
            if start is None or at >= start:
                events.append(event)
            if to == "Accepted":
                accepted = event
            elif to == "Handed over":
                began = timestamp(accepted["at"], "Acceptance") if accepted else None
                left = max(began, start) if began and start else began
                precise = (
                    latest == at and accepted and accepted["time_precision"] == "Recorded instant"
                )
                if start is None or latest >= start:
                    observed.append(
                        dict(
                            source=accepted["source"] if accepted else None,
                            end_source=source,
                            evidence_version=version if type(version) is int else None,
                            accepted_at=accepted["at"] if accepted else None,
                            handed_over_at=_iso(at),
                            elapsed_seconds=(at - left).total_seconds()
                            if valid and precise and left is not None and left <= at
                            else None,
                            status="Observed historical handover"
                            if valid and precise
                            else "Unknown",
                            superseded_at=None,
                        )
                    )
            elif to == "Superseded":
                superseded_at = _iso(at)
        for pair in observed:
            pair["superseded_at"] = superseded_at
            if not valid:
                pair.update(elapsed_seconds=None, status="Unknown")
        pairs.extend(observed)
    return events, pairs


def history(case: Record, as_of: datetime, start: datetime | None) -> Record:
    exceptions: list[Record] = []
    transitions, valid = _events(case, "returns", as_of, exceptions)
    handoffs, handoff_valid = _events(case, "handoff_history", as_of, exceptions)
    quality_events, accepted_handovers = _quality_history(case, as_of, start, exceptions)
    intervals: list[Record] = []
    if not transitions:
        _exception(exceptions, "unknown_stage_history", "returns")
    else:
        _exception(exceptions, "unknown_initial_stage_entry", transitions[0]["source"])
    for index, event in enumerate(transitions):
        following = transitions[index + 1] if index + 1 < len(transitions) else None
        entered = timestamp(event["at"], "Event time")
        ended = timestamp(following["at"], "Event time") if following else as_of
        consistent = valid and event["time_precision"] == "Recorded instant"
        if following:
            consistent = consistent and following["time_precision"] == "Recorded instant"
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
    precise_wait = True
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
            precise_wait = True
        precise_wait = precise_wait and event["time_precision"] == "Recorded instant"
        if current in {"Accepted", "Declined", "Withdrawn"}:
            at = timestamp(event["at"], "Event time")
            began = timestamp(offered["at"], "Offer time") if offered else None
            wait_start = max(began, start) if began and start else began
            if not precise_wait:
                _exception(exceptions, "unknown_handoff_duration", event["source"])
            if (
                start is None
                or wait_start is None
                or wait_start <= timestamp(event["latest_possible_at"], "Event time")
            ):
                waits.append(
                    dict(
                        outcome=current,
                        source=event["source"],
                        offered_at=offered["at"] if offered else None,
                        ended_at=event["at"],
                        elapsed_seconds=(at - wait_start).total_seconds()
                        if handoff_valid and precise_wait and wait_start is not None
                        else None,
                    )
                )
            offered = None
        state = current
    if offered is not None:
        _exception(exceptions, "handoff_pending", offered["source"])
        began = timestamp(offered["at"], "Offer time")
        left = max(began, start) if start else began
        if not precise_wait:
            _exception(exceptions, "unknown_handoff_duration", offered["source"])
        if left <= as_of:
            waits.append(
                dict(
                    outcome="Pending",
                    source=offered["source"],
                    offered_at=offered["at"],
                    ended_at=None,
                    elapsed_seconds=(as_of - left).total_seconds()
                    if handoff_valid and precise_wait
                    else None,
                    censored=True,
                )
            )
    if not handoff_valid:
        for wait in waits:
            wait.update(elapsed_seconds=None, status="Unknown")
    # Independent source streams have no authoritative cross-stream sequence.
    events = transitions + handoffs + quality_events
    if start is not None:
        for event in transitions + handoffs + quality_events:
            if (
                timestamp(event["at"], "Event time")
                < start
                <= timestamp(event["latest_possible_at"], "Event time")
            ):
                _exception(exceptions, "unknown_event_period", event["source"])
    return dict(
        case_id=case["id"],
        coverage="Partial" if events else "Unknown",
        events=[e for e in events if start is None or timestamp(e["at"], "Event time") >= start],
        stage_intervals=intervals,
        handoff_waits=waits,
        accepted_handovers=accepted_handovers,
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
            intervals = item["stage_intervals"] + item["handoff_waits"] + item["accepted_handovers"]
            for interval in intervals:
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
            handoff_precision=(
                "Legacy minute timestamps bound a minute, not an exact instant; "
                "affected waits are unknown"
            ),
            event_order=(
                "Independent stage, handoff and per-record quality streams "
                "in append/version sequence, "
                "not cross-stream time order"
            ),
            pending_wait="Censored elapsed since observed offer, not a completed handoff",
            stage_interval=(
                "Consistent recorded advance/return/reopen boundaries; last exit unknown"
            ),
            accepted_handovers=(
                "Historical same-evidence-version quality acceptance to handover; "
                "not whole-home completion"
            ),
            event_period="Inclusive period; earlier boundaries may support clipped intervals",
            cohort="Current authorized membership in this response, not historical membership",
        ),
        sources=[
            "returns",
            "handoff_history",
            "quality/*/history",
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
