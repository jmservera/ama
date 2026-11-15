"""Reproducible, read-only work queue context; never an approval or assignment."""

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime, time, timedelta
from typing import Any

VERSION = "work-queues-1"
MEMBERSHIP_REVISION = 5
UNKNOWN = "Unknown"
HELD = "Held for roles with a recorded need"
PENDING = ("Offered", "Received", "Escalated")
SAFEGUARDING_ITEM_KEYS = frozenset(
    {
        "id",
        "status",
        "state",
        "priority",
        "category",
        "kind",
        "item_kind",
        "aware_at",
        "raised_at",
        "reported_at",
        "noticed",
        "response_due_at",
        "due_at",
        "responded_at",
        "completed_at",
        "resident_update_due_at",
        "resident_updated_at",
        "owner",
        "named_owner",
        "accountable_owner",
        "sender",
        "destination",
        "accepted_by",
        "accepted_at",
        "follow_up",
        "referred",
        "repaired",
        "released",
    }
)
UNRECORDED_OWNER_TOKENS = frozenset(
    {"", "unknown", "anonymous", "unassigned", "none", "tbd", "to be named", "not assigned"}
)
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
        "A recorded pending handoff, resident update, nomination or self-referral next update, "
        "or external safety-service deadline is before the snapshot and completion is not "
        "evidenced. Not a statutory calculation, and never a priority or eligibility change.",
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


def timing(due: object, done: object, now: datetime) -> str:
    """Plain state of one recorded external deadline; never a statutory calculation."""
    end, finished = instant(due), instant(done)
    if finished is not None and finished <= now:
        return "Completed"
    if end is None:
        return UNKNOWN
    return "Overdue" if end < now else "Open"


def _utc_iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _clean_name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or text.lower() in UNRECORDED_OWNER_TOKENS:
        return None
    return text


def raw_safeguarding_items(case: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return standalone safeguarding item dicts, ignoring note-only canary containers."""
    items: list[dict[str, Any]] = []
    explicit = case.get("safeguarding_items")
    if isinstance(explicit, list):
        items.extend(x for x in explicit if isinstance(x, dict))
    legacy = case.get("safeguarding")
    if isinstance(legacy, list):
        items.extend(x for x in legacy if isinstance(x, dict))
    elif isinstance(legacy, dict) and bool(set(legacy.keys()) & SAFEGUARDING_ITEM_KEYS):
        items.append(legacy)
    return items


def is_safeguarding_item(item: Mapping[str, Any], *, default_kind: str = "hazard") -> bool:
    if default_kind == "safeguarding":
        return True
    kind = str(item.get("item_kind") or item.get("kind") or "").strip().lower()
    category = str(item.get("category") or "").strip().lower()
    return kind == "safeguarding" or category.startswith("safeguard")


def is_open_safety_item(item: Mapping[str, Any]) -> bool:
    if bool(item.get("released")):
        return False
    status = str(item.get("status") or "").strip().lower()
    return status not in {"closed", "released", "resolved"}


def has_open_safety(case: Mapping[str, Any]) -> bool:
    return any(is_open_safety_item(h) for h in case.get("hazards", [])) or any(
        is_open_safety_item(s) for s in raw_safeguarding_items(case)
    )


def has_open_safeguarding(case: Mapping[str, Any]) -> bool:
    return any(
        is_open_safety_item(h) and is_safeguarding_item(h) for h in case.get("hazards", [])
    ) or any(is_open_safety_item(s) for s in raw_safeguarding_items(case))


def _staff_sort_key(member: Mapping[str, Any]) -> tuple[str, str, str]:
    return (
        str(member.get("code") or member.get("oid") or "").strip(),
        str(member.get("email") or "").strip().lower(),
        str(member.get("name") or "").strip().lower(),
    )


def _match_staff(
    *,
    code: str | None = None,
    email: str | None = None,
    name: str | None = None,
    staff: Sequence[Mapping[str, Any]],
) -> Mapping[str, Any] | None:
    if not staff:
        return None
    ordered = sorted(staff, key=_staff_sort_key)
    if code:
        code_clean = code.strip()
        if code_clean:
            for member in ordered:
                m_code = str(member.get("code") or member.get("oid") or "").strip()
                if m_code and m_code == code_clean:
                    return member
    if email:
        email_low = email.strip().lower()
        if email_low:
            for member in ordered:
                m_email = str(member.get("email") or "").strip().lower()
                if m_email and m_email == email_low:
                    return member
    if name:
        name_low = name.strip().lower()
        if name_low:
            for member in ordered:
                m_name = str(member.get("name") or "").strip().lower()
                if m_name and m_name == name_low:
                    return member
    return None


def _resolve_person(
    candidate: object,
    *,
    staff: Sequence[Mapping[str, Any]],
    fallback_role: str,
    fallback_id_prefix: str,
    explicit_code: object = None,
    explicit_role: object = None,
) -> tuple[str, str, str] | None:
    raw_name: str | None = None
    raw_role: str | None = _clean_name(explicit_role)
    raw_code: str | None = _clean_name(explicit_code)
    raw_email: str | None = None
    if isinstance(candidate, Mapping):
        raw_name = _clean_name(candidate.get("name"))
        raw_role = _clean_name(candidate.get("role")) or raw_role
        raw_code = (
            _clean_name(candidate.get("code") or candidate.get("id") or candidate.get("oid"))
            or raw_code
        )
        raw_email = _clean_name(candidate.get("email"))
    elif isinstance(candidate, str):
        cleaned = _clean_name(candidate)
        if cleaned:
            if "@" in cleaned:
                raw_email = cleaned
            else:
                raw_name = cleaned
    matched = _match_staff(code=raw_code, email=raw_email, name=raw_name, staff=staff)
    final_name = (
        (_clean_name(matched.get("name")) if matched else None) or raw_name or raw_email or raw_code
    )
    if not final_name:
        return None
    final_role = (
        raw_role or (_clean_name(matched.get("role")) if matched else None) or fallback_role
    )
    final_id = (
        raw_code
        or (_clean_name(matched.get("code") or matched.get("oid")) if matched else None)
        or raw_email
        or (_clean_name(matched.get("email")) if matched else None)
        or f"{fallback_id_prefix}:{final_name.upper().replace(' ', '-')}"
    )
    return (final_name, final_role, final_id)


def project_safety_clock_and_owner(
    item: Mapping[str, Any],
    *,
    case: Mapping[str, Any] | None = None,
    as_of: str | None = None,
    staff: Sequence[Mapping[str, Any]] | None = None,
    default_kind: str = "hazard",
) -> dict[str, Any]:
    """Deterministic fail-closed clock and non-blank accountable/escalation owner projection."""
    roster: Sequence[Mapping[str, Any]] = staff or ()
    case_map: Mapping[str, Any] = case or {}
    safeguarding = is_safeguarding_item(item, default_kind=default_kind)
    item_kind = "safeguarding" if safeguarding else "hazard"
    default_role = (
        _clean_name((item.get("hold") or {}).get("accountable_role"))
        if isinstance(item.get("hold"), Mapping)
        else None
    ) or "Building Safety Liaison"

    direct_candidates: list[tuple[object, object, object]] = [
        (item.get("accepted_by"), None, None),
    ]
    if bool(item.get("accepted_at")):
        direct_candidates.append((item.get("destination"), None, None))
    direct_candidates.extend(
        [
            (item.get("sender"), None, None),
            (item.get("follow_up"), None, None),
            (
                item.get("owner"),
                item.get("owner_id") or item.get("owner_code"),
                item.get("owner_role"),
            ),
            (
                item.get("named_owner"),
                item.get("owner_id") or item.get("owner_code"),
                item.get("owner_role"),
            ),
            (
                item.get("accountable_owner"),
                item.get("owner_id") or item.get("owner_code"),
                item.get("owner_role"),
            ),
        ]
    )
    direct: tuple[str, str, str] | None = None
    for cand, cand_code, cand_role in direct_candidates:
        direct = _resolve_person(
            cand,
            staff=roster,
            fallback_role=default_role,
            fallback_id_prefix="OWNER",
            explicit_code=cand_code,
            explicit_role=cand_role,
        )
        if direct is not None:
            break

    escalation: tuple[str, str, str] | None = None
    if not bool(item.get("accepted_at")) and item.get("destination"):
        escalation = _resolve_person(
            item.get("destination"),
            staff=roster,
            fallback_role=default_role,
            fallback_id_prefix="ESC",
        )
    if escalation is None and case_map.get("owner"):
        escalation = _resolve_person(
            case_map.get("owner"),
            staff=roster,
            fallback_role=_clean_name(case_map.get("owner_role")) or "Resident Liaison Officer",
            fallback_id_prefix="CASE-OWNER",
            explicit_code=case_map.get("owner_code"),
            explicit_role=case_map.get("owner_role"),
        )
    if escalation is None:
        ordered_roster = sorted(
            roster,
            key=lambda m: str(m.get("code") or m.get("email") or m.get("name") or ""),
        )
        for target_role in (
            "Building Safety Liaison",
            "Retrofit Programme Manager",
            "Programme Support Officer",
            "Resident Liaison Officer",
        ):
            for member in ordered_roster:
                if str(member.get("role") or "").strip() == target_role:
                    escalation = _resolve_person(
                        member,
                        staff=roster,
                        fallback_role=target_role,
                        fallback_id_prefix="ESC",
                    )
                    if escalation is not None:
                        break
            if escalation is not None:
                break
    if escalation is None:
        escalation = (
            (
                "Safeguarding duty lead",
                "Building Safety Liaison",
                "ESC-SG-DUTY",
            )
            if safeguarding
            else (
                "Building Safety Liaison duty lead",
                "Building Safety Liaison",
                "ESC-BSL-DUTY",
            )
        )

    esc_name, esc_role, esc_id = escalation
    if direct is not None:
        d_name, d_role, d_id = direct
        unassigned = False
        legacy_owner = d_name
        owner_named = True
        named_owner = d_name
        owner_role = d_role
        owner_id = d_id
    else:
        unassigned = True
        legacy_owner = UNKNOWN
        owner_named = False
        named_owner = esc_name
        owner_role = esc_role
        owner_id = esc_id

    priority_raw = _clean_name(item.get("priority")) or UNKNOWN
    pri_upper = priority_raw.upper()
    if safeguarding:
        if pri_upper in {"EMERGENCY", "IMMEDIATE", "URGENT", "P1"}:
            window_hours = 24
            clock_label = "Safeguarding 24h emergency response clock"
        else:
            window_hours = 48
            clock_label = "Safeguarding 48h referral response clock"
    else:
        if pri_upper in {"EMERGENCY", "P1"}:
            window_hours = 24
            clock_label = "Awaab's Law 24h emergency action clock (recorded reference)"
        elif pri_upper == "ROUTINE" or (
            pri_upper == "SIGNIFICANT" and bool(item.get("accepted_at"))
        ):
            window_hours = 336
            clock_label = "Operational 14d work-start clock (recorded reference)"
        else:
            window_hours = 168
            clock_label = "Operational 7d hazard investigation clock (recorded reference)"

    now = instant(as_of) if as_of else datetime.now(UTC)
    if now is None:
        now = datetime.now(UTC)
    raw_aware = item.get("aware_at") or item.get("raised_at") or item.get("reported_at")
    raw_due = item.get("response_due_at") or item.get("due_at")
    raw_done = item.get("responded_at") or item.get("completed_at")
    aware_dt = instant(raw_aware)
    valid_aware = aware_dt if (aware_dt is not None and aware_dt <= now) else None
    due_dt = instant(raw_due)
    done_dt = instant(raw_done)

    if due_dt is not None:
        deadline: datetime | None = due_dt
        clock_basis = "recorded_service_deadline"
    elif valid_aware is not None:
        deadline = valid_aware + timedelta(hours=window_hours)
        clock_basis = "operational_reference_from_awareness"
    else:
        deadline = None
        clock_basis = "missing_timestamp_fail_closed"

    if done_dt is not None and done_dt <= now:
        clock_status = "completed"
        clock_deadline_utc: str | None = _utc_iso(deadline) if deadline is not None else None
        clock_remaining_hours: float | None = 0.0 if deadline is not None else None
    elif deadline is None:
        clock_status = "fail_closed_missing_timestamp"
        clock_deadline_utc = None
        clock_remaining_hours = None
    else:
        clock_deadline_utc = _utc_iso(deadline)
        clock_remaining_hours = round((deadline - now).total_seconds() / 3600, 1)
        clock_status = "overdue" if deadline < now else "running"

    category = _clean_name(item.get("category")) or (
        "Safeguarding" if safeguarding else "Safety concern"
    )
    authority = (
        "Designated safeguarding lead and statutory safeguarding route"
        if safeguarding and default_kind == "safeguarding"
        else "Existing hazard and repairs service"
    )
    return dict(
        item_kind=item_kind,
        category=category,
        priority=priority_raw,
        owner=legacy_owner,
        owner_named=owner_named,
        named_owner=named_owner,
        accountable_owner=named_owner,
        owner_role=owner_role,
        owner_id=owner_id,
        unassigned=unassigned,
        escalation_owner=esc_name,
        escalation_owner_role=esc_role,
        escalation_owner_id=esc_id,
        clock_label=clock_label,
        clock_status=clock_status,
        clock_deadline_utc=clock_deadline_utc,
        clock_remaining_hours=clock_remaining_hours,
        clock_basis=clock_basis,
        aware_at=str(raw_aware) if valid_aware is not None and raw_aware else UNKNOWN,
        elapsed_hours=int((now - valid_aware).total_seconds() // 3600)
        if valid_aware is not None
        else None,
        response_due_at=str(raw_due) if raw_due else UNKNOWN,
        resident_update_due_at=str(item.get("resident_update_due_at"))
        if item.get("resident_update_due_at")
        else UNKNOWN,
        response_state=timing(raw_due, raw_done, now),
        resident_update_state=timing(
            item.get("resident_update_due_at"),
            item.get("resident_updated_at"),
            now,
        ),
        authority=authority,
    )


def overdue_tasks(
    case: dict[str, Any], *, as_of: str, handoff: dict[str, Any] | None
) -> list[dict[str, Any]]:
    """Evaluate recorded deadlines without building blockers or other work context."""
    now = instant(as_of)
    if now is None:
        raise ValueError("Queue evaluation requires a valid dataset as_of snapshot.")
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
                    case_id=case["id"],
                    source=f"case:{case['id']}/{path}",
                    version=UNKNOWN,
                    as_of=as_of,
                )
            )

    for index, hazard in enumerate(case.get("hazards", [])):
        follow = (
            hazard.get("accepted_by")
            or (hazard.get("destination") if hazard.get("accepted_at") else None)
            or hazard.get("sender")
            or {}
        )
        named = (
            (follow.get("name") if isinstance(follow, Mapping) else follow)
            or hazard.get("owner")
            or UNKNOWN
        )
        path = f"hazards/{index}"
        deadline(
            hazard.get("response_due_at"),
            hazard.get("responded_at"),
            "External safety service response",
            str(named),
            path,
        )
        deadline(
            hazard.get("resident_update_due_at"),
            hazard.get("resident_updated_at"),
            "External safety service resident update",
            str(named),
            path,
        )
    for index, sg in enumerate(raw_safeguarding_items(case)):
        if not is_open_safety_item(sg):
            continue
        follow = (
            sg.get("accepted_by")
            or (sg.get("destination") if sg.get("accepted_at") else None)
            or sg.get("sender")
            or {}
        )
        named = (
            (follow.get("name") if isinstance(follow, Mapping) else follow)
            or sg.get("owner")
            or sg.get("named_owner")
            or UNKNOWN
        )
        path = f"safeguarding/{index}"
        deadline(
            sg.get("response_due_at") or sg.get("due_at"),
            sg.get("responded_at") or sg.get("completed_at"),
            "Safeguarding referral response",
            str(named),
            path,
        )
        deadline(
            sg.get("resident_update_due_at"),
            sg.get("resident_updated_at"),
            "Safeguarding resident update",
            str(named),
            path,
        )
    update = case.get("resident_update") or {}
    deadline(
        update.get("due_at"),
        update.get("completed_at"),
        "Resident update",
        update.get("owner") or UNKNOWN,
        "resident_update",
    )
    if handoff and handoff.get("state") in PENDING:
        handoff_due = (
            handoff.get("effective_due_at") or handoff.get("due_at") or handoff.get("sla_due_at")
        )
        deadline(
            handoff_due,
            None,
            "Handoff acceptance",
            handoff.get("chase_owner") or UNKNOWN,
            "handoff",
        )
    for index, nomination in enumerate(case.get("nomination_records") or []):
        deadline(
            nomination.get("next_update"),
            None,
            "Nomination or self-referral next update",
            (nomination.get("owner") or {}).get("name") or UNKNOWN,
            f"nomination_records/{index}",
        )
    return overdue


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
    staff: Sequence[Mapping[str, Any]] | None = None,
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
    safeguarding_clocks: list[dict[str, Any]] = []

    def _append_safety_item(
        raw_item: Mapping[str, Any],
        path: str,
        *,
        default_kind: str,
    ) -> None:
        if not is_open_safety_item(raw_item):
            return
        projected = project_safety_clock_and_owner(
            raw_item,
            case=case,
            as_of=as_of,
            staff=staff,
            default_kind=default_kind,
        )
        named = projected["owner"]
        is_sg = projected["item_kind"] == "safeguarding"
        block(
            "Safeguarding review"
            if (is_sg and default_kind == "safeguarding")
            else "Safety review",
            "Retrofit work is stopped for safeguarding review."
            if (is_sg and default_kind == "safeguarding")
            else "Retrofit work is stopped for safety review.",
            named if named != UNKNOWN else projected["named_owner"],
            "Obtain external safeguarding confirmation and an independent decision to restart "
            "retrofit work."
            if (is_sg and default_kind == "safeguarding")
            else "Obtain external service evidence and an independent decision to restart "
            "retrofit work.",
            path,
            role=projected["owner_role"],
            version=raw_item.get("referral_version"),
        )
        service_label = "safeguarding route" if is_sg else "hazard service"
        owner_status = (
            "Named follow-up owner recorded."
            if projected["owner_named"]
            else f"No named follow-up owner is recorded. Escalation owner: "
            f"{projected['escalation_owner']} ({projected['escalation_owner_role']}). "
            f"Ask {owner} to record one through the existing {service_label}."
        )
        entry = dict(
            **projected,
            owner_status=owner_status,
            **origin(path, raw_item.get("referral_version")),
        )
        clocks.append(entry)
        if is_sg:
            safeguarding_clocks.append(dict(entry))

    for index, hazard in enumerate(case.get("hazards", [])):
        _append_safety_item(hazard, f"hazards/{index}", default_kind="hazard")
    for index, sg in enumerate(raw_safeguarding_items(case)):
        _append_safety_item(sg, f"safeguarding/{index}", default_kind="safeguarding")
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
    if case.get("funding_ok") is not True:
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
    overdue = overdue_tasks(case, as_of=as_of, handoff=handoff)
    pending = bool(handoff and handoff.get("state") in PENDING)
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
    returned_view: dict[str, Any] | None = None
    if not selected and pending and handoff:
        if handoff.get("next_action"):
            next_action = text(handoff.get("next_action"))
        elif (
            handoff.get("state") == "Escalated" or handoff.get("needs_escalation")
        ) and isinstance(handoff.get("escalation_next_action"), str):
            next_action = str(handoff["escalation_next_action"])
        else:
            next_action = (
                "Ask the proposed receiver to accept or decline; the sender must keep chasing."
            )
        source = origin("handoff")["source"]
        recorded_at = handoff.get("offered_at") or UNKNOWN
    returned = (case.get("returns") or [None])[-1]
    if (
        returned
        and returned.get("event_type") in (None, "return")
        and not returned.get("reopened")
        and returned.get("to_stage") == case["stage"]
    ):
        returned_view = dict(
            reason=text(returned.get("reason")),
            sender=text((returned.get("actor") or {}).get("name") or returned.get("by")),
            from_stage=returned.get("from_stage") or UNKNOWN,
            to_stage=returned.get("to_stage") or UNKNOWN,
            at=returned.get("at") or UNKNOWN,
            next_action=text(returned.get("next_action")),
        )
        if not selected and not pending:
            reason, next_action = returned_view["reason"], returned_view["next_action"]
            source, version = origin("returns")["source"], returned.get("version") or UNKNOWN
            evidence = text(returned.get("source"))
            recorded_at = returned_view["at"]
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
        returned=returned_view,
        blockers=blockers,
        hazard_clocks=clocks,
        safeguarding_clocks=safeguarding_clocks,
        safety_items=[dict(x) for x in clocks],
        overdue=overdue,
        evidence_freshness=freshness,
        technical_reassessment=reassess,
        handoff=dict(
            state=handoff.get("state") or UNKNOWN,
            status=handoff.get("status") or handoff.get("state") or UNKNOWN,
            accountable_owner=handoff.get("accountable_owner") or owner,
            destination=handoff.get("destination") or UNKNOWN,
            sender=handoff.get("from_name") or UNKNOWN,
            proposed_receiver=handoff.get("proposed_receiver") or UNKNOWN,
            confirmed_receiver=handoff.get("confirmed_receiver") or UNKNOWN,
            chase_owner=handoff.get("chase_owner") or UNKNOWN,
            resident_update_owner=handoff.get("resident_update_owner") or UNKNOWN,
            due_at=handoff.get("effective_due_at") or handoff.get("due_at"),
            approved_limit_hours=handoff.get("approved_limit_hours"),
            elapsed_hours=handoff.get("elapsed_hours"),
            overdue_hours=handoff.get("overdue_hours"),
            overdue=bool(handoff.get("overdue")),
            needs_escalation=bool(handoff.get("needs_escalation")),
            escalation_status=handoff.get("escalation_status") or UNKNOWN,
            escalation_target=handoff.get("escalation_target") or UNKNOWN,
            escalation_target_role=handoff.get("escalation_target_role") or UNKNOWN,
            escalation_next_action=handoff.get("escalation_next_action") or UNKNOWN,
        )
        if handoff
        else None,
        resident_update_owner=(case.get("resident_update") or {}).get("owner") or UNKNOWN,
    )
