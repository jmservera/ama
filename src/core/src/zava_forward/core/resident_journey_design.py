"""Resident-facing and representative-facing journey projection and authority expiry enforcement.

Enforces task-limited representative views and request/session-time authority expiry (`FR-045`,
`FR-046`, `NFR-008`, `NFR-009`) by positive allowlist over recorded case and showcase authority
bounds. Staff projections (`projection.py` / `Store.detail`) are never reused: out-of-scope
measures, unrelated complaints, handover packs, unrelated decisions, resident identity/contact
details, and sensitive household/safeguarding notes are omitted rather than masked.
"""

from __future__ import annotations

import secrets
import threading
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Any

from . import controls as _controls_mod
from . import resident_decisions as _resident_decisions_mod
from . import resident_preview as _preview
from .insights import STAGE_ORDER

_controls: Any = _controls_mod
_domain: Any = _resident_decisions_mod

AUTHORITY_TASKS: tuple[str, ...] = (
    "Receive information",
    "Communicate",
    "Attend",
    "Works decision",
)
AUTHORITY_STATUSES: tuple[str, ...] = ("Confirmed", "Unclear", "Disputed", "Revoked")
JOURNEY_STAGE_ORDER: tuple[str, ...] = ("R1", "J1", "J2", "J3", "J4", "J5", "J6")

HELD_HEADLINE = (
    "We cannot share this task's details until a person checks your permission. "
    "Ask the named officer to confirm it safely with the resident."
)
EXPIRED_NOTICE = "Representative permission has expired. " + HELD_HEADLINE
HELD_NOTICE = HELD_HEADLINE
SCOPE_DENIED_NOTICE = "This action is outside your recorded task-limited representative permission."

OFFERED_APPOINTMENT_LABEL = "Offered - not booked"
CONFIRMED_APPOINTMENT_LABEL = "Visit confirmed"

TASK_JOURNEY_STAGES: Mapping[str, tuple[str, ...]] = {
    "Receive information": ("R1", "J4"),
    "Communicate": ("R1", "J4", "J6"),
    "Attend": ("R1", "J3"),
    "Works decision": ("R1", "J1", "J2"),
}

TASK_PERMITTED_ACTIONS: Mapping[str, tuple[str, ...]] = {
    "Receive information": ("view_task_briefing",),
    "Communicate": (
        "view_task_briefing",
        "send_scoped_message",
        "request_scoped_callback",
    ),
    "Attend": ("view_visit_arrangements",),
    "Works decision": (
        "view_task_briefing",
        "submit_measure_decision",
        "pause_measure",
        "withdraw_measure",
    ),
}

TASK_ASSISTANT_TOPICS: Mapping[str, tuple[str, ...]] = {
    "Receive information": (
        "status",
        "progress",
        "next_step",
        "regulations",
        "safety",
    ),
    "Communicate": (
        "status",
        "progress",
        "next_step",
        "regulations",
        "safety",
    ),
    "Attend": ("appointments", "safety"),
    "Works decision": ("consents", "forms", "regulations", "safety"),
}

TASK_BOUNDARY_NOTES: Mapping[str, str] = {
    "Receive information": (
        "Plain-language measure briefings and step updates are outside this task permission."
    ),
    "Communicate": (
        "Sending messages, requesting callbacks and viewing linked service updates are outside "
        "this task permission."
    ),
    "Attend": ("Viewing or confirming visit arrangements is outside this task permission."),
    "Works decision": (
        "Giving, pausing or withdrawing measure consent is outside this task permission."
    ),
}


def valid_representative_ref(value: Any) -> str | None:
    """Return a clean representative reference or None if missing, 'Unknown', or overlong."""
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not cleaned or len(cleaned) > 80 or cleaned.lower() == "unknown":
        return None
    return cleaned


def parse_iso_utc(value: Any) -> datetime | None:
    """Parse an explicit timezone-aware ISO-8601 timestamp or datetime and normalize to UTC."""
    if isinstance(value, datetime):
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            return None
        return value.astimezone(UTC)
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or ("T" not in text and " " not in text):
        return None
    normalized = text[:-1] + "+00:00" if text.endswith(("Z", "z")) else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.tzinfo.utcoffset(parsed) is None:
        return None
    return parsed.astimezone(UTC)


def utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""
    return datetime.now(UTC)


def format_iso_utc(moment: datetime) -> str:
    """Format a timezone-aware datetime as canonical ISO-8601 UTC (`...Z`)."""
    return moment.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _parse_iso_day(value: Any) -> date | None:
    if not isinstance(value, str) or len(value) != 10:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def review_date_ceiling_utc(
    review_date: Any,
    *,
    authority_date: Any = None,
) -> datetime | None:
    """Convert `YYYY-MM-DD` `review_date` into its exclusive UTC start-of-day ceiling."""
    end_day = _parse_iso_day(review_date)
    if end_day is None:
        return None
    if authority_date is not None:
        start_day = _parse_iso_day(authority_date)
        if start_day is None or end_day <= start_day:
            return None
    return datetime(end_day.year, end_day.month, end_day.day, 0, 0, 0, tzinfo=UTC)


def effective_authority_expiry(record: Mapping[str, Any]) -> tuple[datetime | None, str | None]:
    """Resolve effective UTC expiry from explicit `expires_at` and/or `review_date`.

    If `expires_at` is explicitly present on `record` with None, empty, naive, or malformed
    content, returns `(None, None)` so enforcement fails closed with `missing_expiry` rather
    than falling back to `review_date`. When both `expires_at` and `review_date` are valid,
    the stricter (earlier) ceiling governs.
    """
    auth_date = record.get("authority_date")
    has_review = "review_date" in record and record.get("review_date") not in (None, "")
    if "expires_at" in record:
        parsed_exp = parse_iso_utc(record.get("expires_at"))
        if parsed_exp is None:
            return None, None
        if auth_date is not None:
            start_day = _parse_iso_day(auth_date)
            if start_day is None:
                return None, None
            start_utc = datetime(
                start_day.year, start_day.month, start_day.day, 0, 0, 0, tzinfo=UTC
            )
            if parsed_exp <= start_utc:
                return None, None
        if has_review:
            review_ceiling = review_date_ceiling_utc(
                record.get("review_date"), authority_date=auth_date
            )
            if review_ceiling is None:
                return None, None
            effective = min(parsed_exp, review_ceiling)
            return effective, format_iso_utc(effective)
        return parsed_exp, format_iso_utc(parsed_exp)
    review_ceiling = review_date_ceiling_utc(record.get("review_date"), authority_date=auth_date)
    if review_ceiling is None:
        return None, None
    return review_ceiling, format_iso_utc(review_ceiling)


def renewal_route_payload(
    *,
    state: str,
    reason: str,
    expires_at: str | None,
) -> dict[str, Any]:
    """Return safe, plain-language staff and non-digital resident renewal routes."""
    return {
        "headline": HELD_HEADLINE,
        "state": state,
        "reason": reason,
        "recorded_expires_at": expires_at,
        "staff_route": (
            "Ask the named Housing Officer or Resident Liaison Officer to check and "
            "re-confirm task-limited permission privately with the resident through their "
            "confirmed safe contact route."
        ),
        "resident_route": (
            "The resident can confirm, renew, change or end representative permission directly "
            "by phone, letter, agreed visit or assisted service without a portal."
        ),
        "non_digital_supported": True,
    }


def allowed_assistant_topics(tasks: Sequence[str]) -> frozenset[str]:
    """Return the positive allowlist of resident-assistant topics permitted for `tasks`."""
    allowed: set[str] = set()
    for task in tasks:
        allowed.update(TASK_ASSISTANT_TOPICS.get(task, ()))
    return frozenset(allowed)


@dataclass(frozen=True)
class AuthorityEvaluation:
    state: str
    active: bool
    reason: str
    representative_ref: str
    expires_at: str | None
    record: Mapping[str, Any] | None = None
    tasks: tuple[str, ...] = ()
    measure: str | None = None
    context_revision: int | None = None
    scope: str | None = None
    design_version: str | None = None


class RepresentativeAccessBlockedError(PermissionError):
    """Raised when representative authority is expired, missing, revoked, disputed or held."""

    def __init__(
        self,
        *,
        state: str,
        reason: str,
        expires_at: str | None,
        renewal_route: Mapping[str, Any] | None = None,
    ) -> None:
        notice = EXPIRED_NOTICE if state == "expired" else HELD_NOTICE
        super().__init__(notice)
        self.state = state
        self.reason = reason
        self.expires_at = expires_at
        self.renewal_route: dict[str, Any] = (
            dict(renewal_route)
            if renewal_route is not None
            else renewal_route_payload(state=state, reason=reason, expires_at=expires_at)
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "error": str(self),
            "state": self.state,
            "active": False,
            "reason": self.reason,
            "expires_at": self.expires_at,
            "journey_stages": [],
            "permitted_actions": [],
            "authority_scope": [],
            "renewal_route": dict(self.renewal_route),
        }


class RepresentativeScopeDeniedError(PermissionError):
    """Raised when an active representative attempts an out-of-scope task, measure or topic."""

    def __init__(
        self,
        *,
        action: str,
        expires_at: str | None,
        permitted_actions: Sequence[str],
    ) -> None:
        super().__init__(SCOPE_DENIED_NOTICE)
        self.action = action
        self.expires_at = expires_at
        self.permitted_actions = tuple(permitted_actions)
        self.renewal_route = renewal_route_payload(
            state="scope_denied",
            reason="task_out_of_scope",
            expires_at=expires_at,
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "error": str(self),
            "state": "scope_denied",
            "active": True,
            "reason": "task_out_of_scope",
            "action": self.action,
            "expires_at": self.expires_at,
            "permitted_actions": list(self.permitted_actions),
            "renewal_route": dict(self.renewal_route),
        }


def _normalize_tasks(raw_tasks: Any) -> tuple[str, ...] | None:
    if not isinstance(raw_tasks, (list, tuple)) or not raw_tasks:
        return None
    if any(not isinstance(item, str) or item not in AUTHORITY_TASKS for item in raw_tasks):
        return None
    return tuple(task for task in AUTHORITY_TASKS if task in raw_tasks)


def evaluate_representative_authority(
    case: Mapping[str, Any],
    representative_ref: Any,
    *,
    now: datetime | None = None,
    today_str: str | None = None,
) -> AuthorityEvaluation:
    """Evaluate only the latest recorded authority version (`versions[-1]`) for a representative."""
    clean_ref = valid_representative_ref(representative_ref)
    if clean_ref is None:
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="missing_authority",
            representative_ref="",
            expires_at=None,
        )
    if now is not None:
        now_utc = parse_iso_utc(now)
        if now_utc is None:
            return AuthorityEvaluation(
                state="held",
                active=False,
                reason="missing_expiry",
                representative_ref=clean_ref,
                expires_at=None,
            )
        check_day = today_str if today_str is not None else now_utc.date().isoformat()
    else:
        now_utc = utc_now()
        check_day = today_str if today_str is not None else str(_controls.today())
    if _parse_iso_day(check_day) is None:
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="missing_expiry",
            representative_ref=clean_ref,
            expires_at=None,
        )

    schedule = _domain.retention_schedule(case)
    if isinstance(schedule, Mapping) and schedule.get("expired"):
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="retention_expired",
            representative_ref=clean_ref,
            expires_at=None,
        )

    authorities = case.get("representative_authorities")
    versions = authorities.get(clean_ref) if isinstance(authorities, Mapping) else None
    if (
        not isinstance(versions, Sequence)
        or isinstance(versions, (str, bytes))
        or len(versions) == 0
    ):
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="missing_authority",
            representative_ref=clean_ref,
            expires_at=None,
        )

    latest = versions[-1]
    if not isinstance(latest, Mapping):
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="malformed_authority",
            representative_ref=clean_ref,
            expires_at=None,
        )

    effective_dt, recorded_exp = effective_authority_expiry(latest)
    status = latest.get("status")
    if status == "Revoked":
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="revoked",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )
    if status == "Disputed":
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="disputed",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )
    if status == "Unclear":
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="unclear",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )
    if status != "Confirmed":
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="malformed_authority",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )

    if effective_dt is None or recorded_exp is None:
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="missing_expiry",
            representative_ref=clean_ref,
            expires_at=None,
        )

    tasks = _normalize_tasks(latest.get("tasks"))
    auth_date = latest.get("authority_date")
    if tasks is None or _parse_iso_day(auth_date) is None:
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="malformed_authority",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )

    rev_date = latest.get("review_date")
    review_day_expired = (
        isinstance(rev_date, str) and _parse_iso_day(rev_date) is not None and check_day >= rev_date
    )
    if now_utc >= effective_dt or review_day_expired:
        return AuthorityEvaluation(
            state="expired",
            active=False,
            reason="expired",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )

    if isinstance(auth_date, str) and check_day < auth_date:
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="not_yet_valid",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )

    safe_ref = latest.get("safe_contact_ref")
    safe_rev = latest.get("safe_contact_revision")
    contact_history = case.get("resident_contact_history", [])
    if (
        not isinstance(safe_ref, str)
        or not safe_ref
        or safe_ref != case.get("resident_safe_contact")
        or type(safe_rev) is not int
        or not isinstance(contact_history, list)
        or safe_rev != len(contact_history)
    ):
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="safe_contact_changed",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )

    measure = latest.get("measure")
    ctx_rev = latest.get("context_revision")
    measures = case.get("measures", [])
    live_ctx = (
        _domain.current_context(case, measure)
        if isinstance(measure, str)
        and isinstance(measures, Sequence)
        and not isinstance(measures, (str, bytes))
        and measure in measures
        else None
    )
    if (
        not isinstance(live_ctx, Mapping)
        or type(ctx_rev) is not int
        or ctx_rev != live_ctx.get("revision")
    ):
        return AuthorityEvaluation(
            state="held",
            active=False,
            reason="scope_changed",
            representative_ref=clean_ref,
            expires_at=recorded_exp,
        )

    return AuthorityEvaluation(
        state="active",
        active=True,
        reason="active",
        representative_ref=clean_ref,
        expires_at=recorded_exp,
        record=latest,
        tasks=tasks,
        measure=measure,
        context_revision=ctx_rev,
        scope=str(live_ctx.get("scope", latest.get("scope", ""))),
        design_version=str(live_ctx.get("design_version", latest.get("design_version", ""))),
    )


def _appointment_authority_valid(
    work_order: Mapping[str, Any],
    offer: Mapping[str, Any],
    representative_ref: str,
    *,
    check_day: str,
    now_utc: datetime,
) -> bool:
    appt_authorities = work_order.get("appointment_authorities")
    if not isinstance(appt_authorities, Mapping):
        return False
    record = appt_authorities.get(representative_ref)
    if not isinstance(record, Mapping) or record.get("revoked") is not False:
        return False
    if record.get("task") != "Appointment agreement":
        return False
    if record.get("offer") != offer.get("id") or record.get("binding") != offer.get("binding"):
        return False
    valid_from = record.get("valid_from")
    valid_to = record.get("valid_to")
    offer_date = offer.get("date")
    if (
        _parse_iso_day(valid_from) is None
        or _parse_iso_day(valid_to) is None
        or _parse_iso_day(offer_date) is None
    ):
        return False
    assert isinstance(valid_from, str)
    assert isinstance(valid_to, str)
    assert isinstance(offer_date, str)
    if not (valid_from <= check_day <= valid_to and valid_from <= offer_date <= valid_to):
        return False
    if "expires_at" in record:
        parsed_exp = parse_iso_utc(record.get("expires_at"))
        if parsed_exp is None or now_utc >= parsed_exp:
            return False
    return True


def _project_scoped_appointments(
    case_id: str,
    measure: str,
    context_revision: int,
    representative_ref: str,
    work_orders: Sequence[Mapping[str, Any]],
    *,
    check_day: str,
    now_utc: datetime,
) -> tuple[dict[str, list[dict[str, Any]]], bool]:
    offered: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    can_confirm_any = False

    for work_order in work_orders:
        if not isinstance(work_order, Mapping):
            continue
        if work_order.get("case_id") != case_id:
            continue
        state = work_order.get("state")
        if state not in ("Issued", "Appointed"):
            continue
        offer = work_order.get("appointment_offer")
        if not isinstance(offer, Mapping):
            continue
        binding = offer.get("binding")
        bindings = binding.get("resident_bindings") if isinstance(binding, Mapping) else None
        if not isinstance(bindings, Sequence) or isinstance(bindings, (str, bytes)):
            versions = work_order.get("versions")
            if (
                isinstance(versions, Sequence)
                and not isinstance(versions, (str, bytes))
                and versions
            ):
                last_ver = versions[-1]
                bindings = (
                    last_ver.get("resident_bindings") if isinstance(last_ver, Mapping) else None
                )
        if not isinstance(bindings, Sequence) or isinstance(bindings, (str, bytes)):
            continue
        matched = any(
            isinstance(item, Mapping)
            and item.get("measure") == measure
            and item.get("context_revision") == context_revision
            for item in bindings
        )
        if not matched:
            continue

        confirmations = offer.get("confirmations")
        offer_id = str(offer.get("id", ""))
        is_confirmed = (
            state == "Appointed"
            and isinstance(confirmations, Mapping)
            and all(
                key in confirmations
                and isinstance(confirmations[key], Mapping)
                and confirmations[key].get("offer") == offer_id
                for key in ("resident", "staff", "capacity")
            )
        )
        can_confirm = not is_confirmed and _appointment_authority_valid(
            work_order,
            offer,
            representative_ref,
            check_day=check_day,
            now_utc=now_utc,
        )
        if can_confirm:
            can_confirm_any = True

        options_raw = offer.get("options")
        options = (
            [str(opt) for opt in options_raw if isinstance(opt, str) and len(opt) <= 120]
            if isinstance(options_raw, Sequence) and not isinstance(options_raw, (str, bytes))
            else []
        )
        instructions_raw = offer.get("instructions")
        instructions = (
            instructions_raw
            if isinstance(instructions_raw, str)
            and instructions_raw
            and len(instructions_raw) <= 240
            else None
        )
        item: dict[str, Any] = {
            "work_order_id": str(work_order.get("id", "")),
            "offer_id": offer_id,
            "date": str(offer.get("date", "")),
            "period": str(offer.get("period", "")),
            "options": options,
            "instructions": instructions,
            "paused": bool(offer.get("paused", False)),
            "deferred": bool(offer.get("deferred", False)),
            "booking_status": (
                CONFIRMED_APPOINTMENT_LABEL if is_confirmed else OFFERED_APPOINTMENT_LABEL
            ),
            "can_confirm_appointment": can_confirm,
        }
        if is_confirmed:
            confirmed.append(item)
        else:
            offered.append(item)

    return {"offered": offered, "confirmed": confirmed}, can_confirm_any


def _project_scoped_decision(
    case: Mapping[str, Any],
    measure: str,
    context_revision: int,
) -> dict[str, Any]:
    decisions = case.get("measure_decisions")
    entries = decisions.get(measure) if isinstance(decisions, Mapping) else None
    if not isinstance(entries, Sequence) or isinstance(entries, (str, bytes)):
        return {"status": "Not recorded", "context_revision": context_revision}
    scoped = [
        entry
        for entry in entries
        if isinstance(entry, Mapping) and entry.get("context_revision") == context_revision
    ]
    if not scoped:
        return {"status": "Not recorded", "context_revision": context_revision}
    latest = scoped[-1]
    return {
        "status": str(latest.get("status", "Not recorded")),
        "version": int(latest["version"]) if isinstance(latest.get("version"), int) else 1,
        "answered_by": str(latest.get("answered_by", "")),
        "at": str(latest.get("at", "")),
        "context_revision": context_revision,
    }


def _project_scoped_communications(
    case: Mapping[str, Any],
    representative_ref: str,
) -> dict[str, Any]:
    raw_requests = case.get("service_requests")
    scoped_requests: list[dict[str, Any]] = []
    if isinstance(raw_requests, Sequence) and not isinstance(raw_requests, (str, bytes)):
        for req in raw_requests:
            if not isinstance(req, Mapping):
                continue
            if valid_representative_ref(req.get("representative_ref")) != representative_ref:
                continue
            scoped_requests.append(
                {
                    "id": str(req.get("id", "")),
                    "route": str(req.get("route", "")),
                    "status": str(req.get("status", "")),
                    "next_update": str(req.get("next_update", "")),
                }
            )
    result: dict[str, Any] = {"service_requests": scoped_requests}
    update = case.get("resident_update")
    if scoped_requests and isinstance(update, Mapping):
        result["update_commitment"] = {
            "status": str(update.get("status", "")),
            "due_at": str(update.get("due_at", "")),
        }
    return result


def held_or_expired_view(
    *,
    representative_ref: str,
    state: str,
    reason: str,
    expires_at: str | None,
) -> dict[str, Any]:
    """Build the fail-closed non-disclosing shell for expired, revoked, disputed or held state."""
    notice = EXPIRED_NOTICE if state == "expired" else HELD_NOTICE
    return {
        "banner": _preview.BANNER,
        "viewer": {
            "kind": "representative",
            "representative_ref": representative_ref,
            "state": state,
            "active": False,
        },
        "state": state,
        "active": False,
        "reason": reason,
        "expires_at": expires_at,
        "journey_stages": [],
        "permitted_actions": [],
        "authority_scope": [],
        "notice": notice,
        "renewal_route": renewal_route_payload(
            state=state,
            reason=reason,
            expires_at=expires_at,
        ),
        "help": _preview.HELP,
    }


def project_representative_view(
    case: Mapping[str, Any],
    representative_ref: Any,
    *,
    now: datetime | None = None,
    today_str: str | None = None,
    work_orders: Sequence[Mapping[str, Any]] = (),
    include_case_id: bool = True,
) -> dict[str, Any]:
    """Project ONLY the fields, actions, and journey stages within recorded representative scope."""
    evaluation = evaluate_representative_authority(
        case,
        representative_ref,
        now=now,
        today_str=today_str,
    )
    if not evaluation.active or evaluation.measure is None or evaluation.context_revision is None:
        return held_or_expired_view(
            representative_ref=evaluation.representative_ref,
            state=evaluation.state,
            reason=evaluation.reason,
            expires_at=evaluation.expires_at,
        )

    now_utc = parse_iso_utc(now) if now is not None else utc_now()
    assert now_utc is not None
    check_day = (
        today_str
        if today_str is not None
        else (now_utc.date().isoformat() if now is not None else str(_controls.today()))
    )

    stage_set: set[str] = set()
    actions: list[str] = []
    for task in evaluation.tasks:
        stage_set.update(TASK_JOURNEY_STAGES.get(task, ()))
        for act in TASK_PERMITTED_ACTIONS.get(task, ()):
            if act not in actions:
                actions.append(act)

    journey_stages = [stage for stage in JOURNEY_STAGE_ORDER if stage in stage_set]

    measure_projection: dict[str, Any] = {
        "measure": evaluation.measure,
        "scope": evaluation.scope,
        "design_version": evaluation.design_version,
        "context_revision": evaluation.context_revision,
        "tasks": list(evaluation.tasks),
    }

    if "Receive information" in evaluation.tasks or "Communicate" in evaluation.tasks:
        raw_stage = case.get("stage")
        if (
            isinstance(raw_stage, str)
            and raw_stage in STAGE_ORDER
            and raw_stage in _preview.STAGE_TEXT
        ):
            progress, next_step = _preview.STAGE_TEXT[raw_stage]
            stage_label = raw_stage
        else:
            progress, next_step = _preview.UNKNOWN_PROGRESS, _preview.UNKNOWN_NEXT
            stage_label = "Unknown"
        measure_projection["stage"] = stage_label
        measure_projection["progress"] = progress
        measure_projection["next_step"] = next_step

    if "Works decision" in evaluation.tasks:
        measure_projection["decision"] = _project_scoped_decision(
            case,
            evaluation.measure,
            evaluation.context_revision,
        )

    case_id_str = str(case.get("id", ""))
    appointments_payload: dict[str, list[dict[str, Any]]] | None = None
    if "Attend" in evaluation.tasks:
        appointments_payload, can_confirm = _project_scoped_appointments(
            case_id_str,
            evaluation.measure,
            evaluation.context_revision,
            evaluation.representative_ref,
            work_orders,
            check_day=check_day,
            now_utc=now_utc,
        )
        measure_projection["appointments"] = appointments_payload
        if can_confirm and "confirm_appointment" not in actions:
            actions.append("confirm_appointment")

    record = evaluation.record or {}
    scope_banner = (
        f"You may {', '.join(evaluation.tasks)} for {evaluation.measure} "
        f"({evaluation.scope}, design {evaluation.design_version}) until {evaluation.expires_at}."
    )
    authority_entry: dict[str, Any] = {
        "measure": evaluation.measure,
        "scope": evaluation.scope,
        "design_version": evaluation.design_version,
        "context_revision": evaluation.context_revision,
        "tasks": list(evaluation.tasks),
        "authority_date": str(record.get("authority_date", "")),
        "review_date": str(record.get("review_date", "")),
        "expires_at": evaluation.expires_at,
        "source": str(record.get("source", "")),
        "resident_wishes": str(record.get("resident_wishes", "")),
        "statement": scope_banner,
    }

    view: dict[str, Any] = {
        "banner": _preview.BANNER,
        "viewer": {
            "kind": "representative",
            "representative_ref": evaluation.representative_ref,
            "state": "active",
            "active": True,
        },
        "state": "active",
        "active": True,
        "reason": "active",
        "expires_at": evaluation.expires_at,
        "journey_stages": journey_stages,
        "permitted_actions": actions,
        "authority_scope": [authority_entry],
        "measures": [measure_projection],
        "tasks_not_shown": [
            {"task": task, "reason": TASK_BOUNDARY_NOTES[task]}
            for task in AUTHORITY_TASKS
            if task not in evaluation.tasks
        ],
        "help": _preview.HELP,
    }
    if include_case_id and case_id_str:
        view["case_id"] = case_id_str
    if appointments_payload is not None:
        view["appointments"] = appointments_payload
    if "Communicate" in evaluation.tasks:
        view["communications"] = _project_scoped_communications(
            case,
            evaluation.representative_ref,
        )
    return view


def enforce_representative_action(
    case: Mapping[str, Any],
    representative_ref: Any,
    action: Any,
    *,
    measure: Any = None,
    assistant_topic: Any = None,
    now: datetime | None = None,
    today_str: str | None = None,
    work_orders: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Re-evaluate representative authority and expiry at action time; raise when blocked."""
    view = project_representative_view(
        case,
        representative_ref,
        now=now,
        today_str=today_str,
        work_orders=work_orders,
        include_case_id=False,
    )
    if not view["active"]:
        raise RepresentativeAccessBlockedError(
            state=str(view["state"]),
            reason=str(view["reason"]),
            expires_at=view["expires_at"],
            renewal_route=view["renewal_route"],
        )

    scope_entry = view["authority_scope"][0]
    permitted_actions: list[str] = list(view["permitted_actions"])
    scoped_measure = str(scope_entry["measure"])
    scoped_tasks: list[str] = list(scope_entry["tasks"])

    if not isinstance(action, str) or not action.strip():
        raise RepresentativeScopeDeniedError(
            action=str(action or ""),
            expires_at=view["expires_at"],
            permitted_actions=permitted_actions,
        )
    clean_action = action.strip()

    if measure is not None and (not isinstance(measure, str) or measure.strip() != scoped_measure):
        raise RepresentativeScopeDeniedError(
            action=clean_action,
            expires_at=view["expires_at"],
            permitted_actions=permitted_actions,
        )

    if clean_action not in permitted_actions:
        raise RepresentativeScopeDeniedError(
            action=clean_action,
            expires_at=view["expires_at"],
            permitted_actions=permitted_actions,
        )

    if assistant_topic is not None:
        allowed_topics = allowed_assistant_topics(scoped_tasks)
        if not isinstance(assistant_topic, str) or assistant_topic not in allowed_topics:
            raise RepresentativeScopeDeniedError(
                action=clean_action,
                expires_at=view["expires_at"],
                permitted_actions=permitted_actions,
            )

    return {
        "allowed": True,
        "state": "active",
        "active": True,
        "action": clean_action,
        "measure": scoped_measure,
        "expires_at": view["expires_at"],
        "journey_stages": list(view["journey_stages"]),
        "permitted_actions": permitted_actions,
    }


@dataclass
class RepresentativeSession:
    """Mutable session record tracking immediate transitions from active to expired or held."""

    session_id: str
    case_id: str
    representative_ref: str
    state: str
    reason: str
    expires_at: str | None
    journey_stages: tuple[str, ...]
    permitted_actions: tuple[str, ...]
    updated_at: str

    @property
    def active(self) -> bool:
        return self.state == "active"

    def snapshot(self) -> dict[str, Any]:
        snap: dict[str, Any] = {
            "session_id": self.session_id,
            "representative_ref": self.representative_ref,
            "state": self.state,
            "active": self.active,
            "reason": self.reason,
            "expires_at": self.expires_at,
            "journey_stages": list(self.journey_stages),
            "permitted_actions": list(self.permitted_actions),
            "updated_at": self.updated_at,
        }
        if not self.active:
            snap["renewal_route"] = renewal_route_payload(
                state=self.state,
                reason=self.reason,
                expires_at=self.expires_at,
            )
        return snap


class RepresentativeSessionStore:
    """Thread-safe representative session tracker enforcing mid-session expiry and revocation."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: dict[str, RepresentativeSession] = {}

    def open_session(
        self,
        case: Mapping[str, Any],
        representative_ref: Any,
        *,
        now: datetime | None = None,
        today_str: str | None = None,
        work_orders: Sequence[Mapping[str, Any]] = (),
        session_id: str | None = None,
        include_case_id: bool = False,
    ) -> tuple[RepresentativeSession, dict[str, Any]]:
        now_utc = parse_iso_utc(now) if now is not None else utc_now()
        stamp = format_iso_utc(now_utc if now_utc is not None else utc_now())
        view = project_representative_view(
            case,
            representative_ref,
            now=now,
            today_str=today_str,
            work_orders=work_orders,
            include_case_id=include_case_id,
        )
        sid = (
            session_id if isinstance(session_id, str) and session_id else secrets.token_urlsafe(24)
        )
        session = RepresentativeSession(
            session_id=sid,
            case_id=str(case.get("id", "")),
            representative_ref=str(view["viewer"]["representative_ref"]),
            state=str(view["state"]),
            reason=str(view["reason"]),
            expires_at=view["expires_at"],
            journey_stages=tuple(view["journey_stages"]),
            permitted_actions=tuple(view["permitted_actions"]),
            updated_at=stamp,
        )
        with self._lock:
            self._sessions[sid] = session
        enriched = dict(view)
        enriched["session"] = session.snapshot()
        return session, enriched

    def record_session(self, session: RepresentativeSession) -> None:
        """Persist or replace a tracked representative session under the store lock."""
        with self._lock:
            self._sessions[session.session_id] = session

    def get(self, session_id: str) -> RepresentativeSession | None:
        with self._lock:
            return self._sessions.get(session_id)

    def session_view(
        self,
        session_id: str,
        case: Mapping[str, Any],
        *,
        now: datetime | None = None,
        today_str: str | None = None,
        work_orders: Sequence[Mapping[str, Any]] = (),
        include_case_id: bool = False,
    ) -> dict[str, Any]:
        with self._lock:
            session = self._sessions.get(session_id)
        if session is None or session.case_id != str(case.get("id", "")):
            return held_or_expired_view(
                representative_ref="",
                state="held",
                reason="missing_authority",
                expires_at=None,
            )

        now_utc = parse_iso_utc(now) if now is not None else utc_now()
        stamp = format_iso_utc(now_utc if now_utc is not None else utc_now())
        view = project_representative_view(
            case,
            session.representative_ref,
            now=now,
            today_str=today_str,
            work_orders=work_orders,
            include_case_id=include_case_id,
        )
        resolved_expires = (
            view["expires_at"] if view["expires_at"] is not None else session.expires_at
        )
        with self._lock:
            session.state = str(view["state"])
            session.reason = str(view["reason"])
            session.expires_at = resolved_expires
            session.journey_stages = tuple(view["journey_stages"])
            session.permitted_actions = tuple(view["permitted_actions"])
            session.updated_at = stamp
            snap = session.snapshot()

        enriched = dict(view)
        if enriched["expires_at"] is None and resolved_expires is not None:
            enriched["expires_at"] = resolved_expires
            if "renewal_route" in enriched and isinstance(enriched["renewal_route"], Mapping):
                route = dict(enriched["renewal_route"])
                route["recorded_expires_at"] = resolved_expires
                enriched["renewal_route"] = route
        enriched["session"] = snap
        return enriched

    def session_action(
        self,
        session_id: str,
        case: Mapping[str, Any],
        action: Any,
        *,
        measure: Any = None,
        assistant_topic: Any = None,
        now: datetime | None = None,
        today_str: str | None = None,
        work_orders: Sequence[Mapping[str, Any]] = (),
    ) -> dict[str, Any]:
        current_view = self.session_view(
            session_id,
            case,
            now=now,
            today_str=today_str,
            work_orders=work_orders,
            include_case_id=False,
        )
        if not current_view["active"]:
            raise RepresentativeAccessBlockedError(
                state=str(current_view["state"]),
                reason=str(current_view["reason"]),
                expires_at=current_view["expires_at"],
                renewal_route=current_view["renewal_route"],
            )
        checked = enforce_representative_action(
            case,
            current_view["viewer"]["representative_ref"],
            action,
            measure=measure,
            assistant_topic=assistant_topic,
            now=now,
            today_str=today_str,
            work_orders=work_orders,
        )
        checked["session"] = current_view["session"]
        return checked
