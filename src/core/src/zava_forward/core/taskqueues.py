"""Reproducible, read-only work queue context; never an approval or assignment."""

from datetime import UTC, datetime, time
from typing import Any

VERSION = "work-queues-1"
MEMBERSHIP_REVISION = 2
UNKNOWN = "Unknown"
HELD = "Held for roles with a recorded need"
PENDING = ("Offered", "Received", "Escalated")
DEFAULT = dict(
    view="mine", q="", stage="", area="", flag="", sort="urgent", wave="", owner="", queue=""
)
DEFINITIONS = (
    ("new", "Newly arrived", "Current stage started within 7 days, including day 7."),
    (
        "priority",
        "Approved priority",
        "Open cases ranked under an owner-approved ranking policy; not AI advice.",
    ),
    (
        "stale",
        "Stale evidence",
        "Last supplied EPC record older than 30 days, Survey record older than 180 days, "
        "or a technical "
        "sign-off marked Needs reassessment. These are review triggers, not expiry dates.",
    ),
    (
        "blocked",
        "Blockers",
        "Recorded safety, stock or shared-building stops, or unmet final-check prerequisites. "
        "A future-step prerequisite does not stop the current stage.",
    ),
    (
        "overdue",
        "Overdue tasks",
        "A recorded pending handoff, resident update or external safety-service deadline "
        "is before the snapshot and completion is not evidenced. Not a statutory calculation.",
    ),
    (
        "unowned",
        "Unowned handoffs",
        "Sent, received or escalated handoffs without accepted ownership. "
        "The sender retains chase responsibility; a proposed receiver is not a confirmed owner.",
    ),
)


def approved_priority(policy: dict[str, Any]) -> bool:
    return policy.get("status") == "Approved" and policy.get("owner") not in (
        None,
        "",
        "Unknown",
        "to be named",
    )


def contract(policy: dict[str, Any]) -> dict[str, Any]:
    return dict(
        version=VERSION,
        default=dict(DEFAULT),
        selection=None,
        clock="Dataset as_of snapshot, not a live hazard-service clock",
        status="Engineering definitions; operational owner ratification remains open",
        definitions=[
            dict(
                id=key,
                label=label,
                definition=description,
                available=key != "priority" or approved_priority(policy),
                limitation=(
                    "Ranking policy approval with a named owner is not recorded."
                    if key == "priority" and not approved_priority(policy)
                    else None
                ),
            )
            for key, label, description in DEFINITIONS
        ],
    )


def validate_queue(value: str) -> None:
    if value and value not in {key for key, _, _ in DEFINITIONS}:
        raise ValueError("Choose one of the published work queues.")


def instant(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if len(value) == 10:
        return datetime.combine(parsed.date(), time(), UTC)
    return parsed.astimezone(UTC) if parsed.tzinfo is not None else None


def context(
    case: dict[str, Any],
    *,
    as_of: str,
    reason_ok: bool,
    policy: dict[str, Any],
    stock_queries: list[dict[str, Any]],
    building_reasons: list[str],
    resident_reasons: list[str],
    technical_missing: list[dict[str, Any]],
    handoff: dict[str, Any] | None,
) -> dict[str, Any]:
    now = instant(as_of)
    if now is None:
        raise ValueError("Queue evaluation requires a valid dataset as_of snapshot.")
    cid = case["id"]
    owner = case.get("owner") or UNKNOWN

    def text(value: object) -> str:
        return str(value) if value and reason_ok else HELD if value else UNKNOWN

    def origin(path: str, version: object = None) -> dict[str, Any]:
        return dict(
            case_id=cid, source=f"case:{cid}/{path}", version=version or UNKNOWN, as_of=as_of
        )

    blockers: list[dict[str, Any]] = []

    def block(
        step: str,
        reason: str,
        named: str,
        action: str,
        path: str,
        *,
        active: bool = True,
        role: str = UNKNOWN,
        version: object = None,
    ) -> None:
        blockers.append(
            dict(
                step=step,
                reason=reason,
                owner=named or UNKNOWN,
                responsible_role=role,
                next_action=action,
                current_stop=active,
                **origin(path, version),
            )
        )

    clocks: list[dict[str, Any]] = []
    overdue: list[dict[str, Any]] = []

    def deadline(due: object, completed: object, label: str, named: str, path: str) -> None:
        end = instant(due)
        done = instant(completed)
        satisfied = done is not None and done <= now
        if end is not None and end < now and not satisfied:
            overdue.append(
                dict(
                    task=label,
                    owner=named or UNKNOWN,
                    due_at=due,
                    completion="Not evidenced",
                    **origin(path),
                )
            )

    for index, hazard in enumerate(case.get("hazards", [])):
        follow = hazard.get("accepted_by") or hazard.get("sender") or {}
        named = follow.get("name") or hazard.get("owner") or UNKNOWN
        path = f"hazards/{index}"
        if not hazard.get("released"):
            block(
                "Safety review",
                "Retrofit work is stopped for safety review.",
                named,
                "Obtain external service evidence and an independent decision to restart "
                "retrofit work.",
                path,
            )
            awareness = instant(hazard.get("aware_at"))
            clocks.append(
                dict(
                    owner=named,
                    aware_at=hazard.get("aware_at") if awareness and awareness <= now else UNKNOWN,
                    elapsed_hours=int((now - awareness).total_seconds() // 3600)
                    if awareness and awareness <= now
                    else None,
                    response_due_at=hazard.get("response_due_at") or UNKNOWN,
                    resident_update_due_at=hazard.get("resident_update_due_at") or UNKNOWN,
                    authority="Existing hazard and repairs service",
                    **origin(path, hazard.get("referral_version")),
                )
            )
        deadline(
            hazard.get("response_due_at"),
            hazard.get("responded_at"),
            "External safety service response",
            named,
            path,
        )
        deadline(
            hazard.get("resident_update_due_at"),
            hazard.get("resident_updated_at"),
            "External safety service resident update",
            named,
            path,
        )
    for query in stock_queries:
        block(
            "Stock review",
            f"Stock query {query['id']} remains unresolved.",
            (query.get("query_owner") or {}).get("name", UNKNOWN),
            "Ask the query owner to obtain a human reconciliation decision.",
            f"stock_reconciliation/{query['id']}",
            version=query.get("version"),
        )
    for reason in building_reasons:
        block(
            "Shared building review",
            text(reason),
            UNKNOWN,
            "Ask the case owner to identify the shared-building reviewer and evidence.",
            "building",
        )
    final_checks = case["stage"] == "Final checks before ordering"
    if not case.get("funding_ok"):
        block(
            "Final checks: funding",
            "Funding has not been confirmed.",
            owner,
            "Check funding evidence and record confirmation through the permitted review.",
            "funding",
            active=final_checks,
        )
    for reason in resident_reasons:
        block(
            "Final checks: resident decision",
            text(reason),
            owner,
            "Obtain the resident's supplied decision and current scope evidence.",
            "measure_decisions",
            active=final_checks,
        )
    for item in technical_missing:
        if item["assigned_to"] == "Stock query owner":
            continue
        block(
            "Final checks: technical review",
            text(item["item"]),
            UNKNOWN,
            "Ask the responsible role to record the required evidence or decision.",
            "technical",
            active=final_checks,
            role=item["assigned_to"],
            version=(case.get("technical") or {}).get("design_version"),
        )

    freshness: list[dict[str, Any]] = []
    stale = False
    for kind, days in (("EPC", 30), ("Survey", 180)):
        documents = [d for d in case.get("documents", []) if d.get("kind") == kind]
        doc = documents[-1] if documents else {}
        observed = instant(doc.get("at"))
        age = (now - observed).total_seconds() / 86400 if observed and observed <= now else None
        state = UNKNOWN if age is None else "Stale" if age > days else "Within review window"
        stale = stale or state == "Stale"
        freshness.append(
            dict(
                kind=kind,
                status=state,
                recorded_at=doc.get("at") if age is not None else UNKNOWN,
                evidence=text(doc.get("id")),
                **origin("documents", doc.get("version")),
            )
        )
    reassess = any(
        s.get("status") == "Needs reassessment"
        for s in (case.get("technical") or {}).get("signoffs", {}).values()
    )
    stale = stale or reassess
    update = case.get("resident_update") or {}
    deadline(
        update.get("due_at"),
        update.get("completed_at"),
        "Resident update",
        update.get("owner") or UNKNOWN,
        "resident_update",
    )
    pending = bool(handoff and handoff.get("state") in PENDING)
    if pending and handoff:
        deadline(
            handoff.get("due_at"),
            None,
            "Handoff acceptance",
            handoff.get("chase_owner") or UNKNOWN,
            "handoff",
        )
    started = instant(case.get("stage_since"))
    new = started is not None and 0 <= (now - started).total_seconds() <= 7 * 86400
    active = [b for b in blockers if b["current_stop"]]
    selected = active[0] if active else None
    next_action = selected["next_action"] if selected else None
    reason = selected["reason"] if selected else text(case.get("reason"))
    source = selected["source"] if selected else origin("stage")["source"]
    version: object = selected["version"] if selected else UNKNOWN
    evidence = UNKNOWN
    recorded_at = case.get("stage_since") or UNKNOWN
    if not selected and pending and handoff:
        next_action = (
            text(handoff.get("next_action"))
            if handoff.get("next_action")
            else ("Ask the proposed receiver to accept or decline; the sender must keep chasing.")
        )
        source = origin("handoff")["source"]
        recorded_at = handoff.get("offered_at") or UNKNOWN
    elif not selected and case.get("returns"):
        returned = case["returns"][-1]
        if returned.get("to_stage") == case["stage"]:
            reason, next_action = text(returned.get("reason")), text(returned.get("next_action"))
            source, version = origin("returns")["source"], returned.get("version") or UNKNOWN
            evidence = text(returned.get("source"))
            recorded_at = returned.get("at") or UNKNOWN
    if not next_action:
        next_action = f"Ask {owner} to record the next action."
    matched = [
        key
        for key, condition in (
            ("new", new),
            ("priority", approved_priority(policy)),
            ("stale", stale),
            ("blocked", bool(active)),
            ("overdue", bool(overdue)),
            ("unowned", pending),
        )
        if condition and not case.get("closed")
    ]
    return dict(
        case_id=cid,
        definition_version=VERSION,
        as_of=as_of,
        owner=owner,
        reason=reason,
        next_action=next_action,
        source=source,
        version=version,
        evidence=evidence,
        recorded_at=recorded_at,
        queues=matched,
        blockers=blockers,
        hazard_clocks=clocks,
        overdue=overdue,
        evidence_freshness=freshness,
        technical_reassessment=reassess,
        handoff=dict(
            state=handoff.get("state") or UNKNOWN,
            destination=handoff.get("destination") or UNKNOWN,
            proposed_receiver=handoff.get("proposed_receiver") or UNKNOWN,
            confirmed_receiver=handoff.get("confirmed_receiver") or UNKNOWN,
            chase_owner=handoff.get("chase_owner") or UNKNOWN,
            resident_update_owner=handoff.get("resident_update_owner") or UNKNOWN,
        )
        if handoff
        else None,
    )
