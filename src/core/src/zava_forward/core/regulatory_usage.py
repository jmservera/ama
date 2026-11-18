"""Content-free accounting for the closed, model-free regulatory paths."""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from datetime import UTC, datetime
from typing import Any, cast

from zava_forward.core import chatthreads as _chatthreads
from zava_forward.core import projection as _projection
from zava_forward.core.regulatory_privacy import (
    cost_record,
    is_trusted_proxy_user,
    metering_record,
    require_regulatory_role,
    retention_alignment,
)

_user_key = cast(Callable[[dict[str, Any]], str], _chatthreads.user_key)
_STAFF_ROLES: tuple[str, ...] = tuple(_projection.STAFF_ROLES)
_SAFE_ID_SUB = re.compile(r"[^A-Za-z0-9._:-]+")

SCHEMA = "regulatory-usage-v1"
MAX_POSITIONS = 1000
MAX_BYTES = 256 * 1024
TASKS = {
    "regulatory-home-chat": ("answer", "refused", "conflict"),
    "regulatory-check": ("clear", "attention", "breach risk", "unknown", "not applicable"),
}


def offline_usage(task: str, version: str, outcome: str, at: str) -> dict[str, Any]:
    if task not in TASKS or outcome not in TASKS[task]:
        raise ValueError("Unsupported offline regulatory task or outcome.")
    parsed = datetime.fromisoformat(at)
    if parsed.tzinfo is None:
        raise ValueError("Usage needs a timezone-aware recorded time.")
    return dict(
        schema=SCHEMA,
        task=task,
        task_version=version,
        model="none",
        outcome=outcome,
        period=parsed.astimezone(UTC).date().isoformat(),
        period_basis="UTC day",
        model_calls=0,
        input_tokens=0,
        output_tokens=0,
        cached_tokens=0,
        retries=0,
        model_call_limit_per_role_period=0,
        limit_basis="Inference disabled for every role; not a paid budget approval.",
    )


SURFACES = {"regulatory-home-chat": "chat", "regulatory-check": "check"}


def usage_metering(usage: dict[str, Any], record_id: str) -> dict[str, Any]:
    """Project offline usage onto the closed metering schema: ids, counts and versions only."""
    return metering_record(
        dict(
            surface=SURFACES[usage["task"]],
            record_id=record_id,
            model_id=usage["model"],
            prompt_version=usage["task_version"],
            input_tokens=usage["input_tokens"],
            output_tokens=usage["output_tokens"],
            cached_tokens=usage["cached_tokens"],
            retry_count=usage["retries"],
            occurred_at=usage["period"] + "T00:00:00+00:00",
        )
    )


def _validate_stored_usage(
    usage: Any, expected_task: str, expected_version: str | None = None
) -> dict[str, Any]:
    if not isinstance(usage, dict):
        raise ValueError("Stored regulatory usage is invalid; audit review required.")
    version = (
        expected_version if expected_version is not None else str(usage.get("task_version") or "")
    )
    try:
        expected = offline_usage(
            expected_task,
            version,
            str(usage.get("outcome") or ""),
            str(usage.get("period") or "") + "T00:00:00+00:00",
        )
    except ValueError:
        raise ValueError("Stored regulatory usage is invalid; audit review required.") from None
    if usage != expected or any(
        type(usage[key]) is not type(value) for key, value in expected.items()
    ):
        raise ValueError("Stored regulatory usage is invalid; audit review required.")
    return expected


def check_usage_metering(check: Mapping[str, Any]) -> dict[str, Any]:
    """Project a reg_check body onto closed content-free check metering."""
    usage = _validate_stored_usage(check.get("usage"), "regulatory-check")
    card_id = str(check.get("card_id") or "")
    card_version = check.get("card_version")
    if type(card_version) is not int or card_version < 1:
        raise ValueError("reg_check card_version must be a positive integer.")
    occurred_at = str(check.get("at") or "")
    return metering_record(
        dict(
            surface="check",
            record_id=str(check.get("id") or ""),
            model_id=usage["model"],
            prompt_version=usage["task_version"],
            rule_card_version=f"{card_id}:v{card_version}",
            input_tokens=usage["input_tokens"],
            output_tokens=usage["output_tokens"],
            cached_tokens=usage["cached_tokens"],
            retry_count=usage["retries"],
            occurred_at=occurred_at,
        )
    )


def _apply_price_schedule(
    metered: Mapping[str, Any], price_schedule: Mapping[str, Any] | None
) -> dict[str, Any]:
    base: dict[str, Any] = {
        k: metered[k]
        for k in (
            "surface",
            "record_id",
            "model_id",
            "prompt_version",
            "rule_card_version",
            "input_tokens",
            "output_tokens",
            "cached_tokens",
            "retry_count",
            "occurred_at",
        )
        if k in metered
    }
    if price_schedule is None:
        base.update(
            price_version="unpriced",
            currency=None,
            cost_minor_units=None,
            cost="Unknown",
        )
        return cost_record(base)
    pver = str(price_schedule.get("price_version") or "")
    currency = str(price_schedule.get("currency") or "")
    in_rate = price_schedule.get("input_minor_per_1k")
    out_rate = price_schedule.get("output_minor_per_1k")
    if type(in_rate) is not int or type(out_rate) is not int or in_rate < 0 or out_rate < 0:
        raise ValueError("Price schedule rates must be non-negative integers.")
    in_tok = int(metered["input_tokens"])
    out_tok = int(metered["output_tokens"])
    minor = (in_tok * in_rate + out_tok * out_rate) // 1000
    base.update(
        price_version=pver,
        currency=currency,
        cost_minor_units=minor,
        cost="calculated",
    )
    return cost_record(base)


def chat_cost_record(
    usage: dict[str, Any],
    record_id: str,
    *,
    occurred_at: str | None = None,
    price_schedule: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a closed-schema chat cost record (OD-51 cost='Unknown' when unpriced)."""
    metered = dict(usage_metering(usage, record_id))
    if occurred_at is not None:
        metered["occurred_at"] = occurred_at
        metered = metering_record({k: v for k, v in metered.items() if k != "retention_class"})
    return _apply_price_schedule(metered, price_schedule)


def check_cost_record(
    check: Mapping[str, Any],
    *,
    price_schedule: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a closed-schema check cost record (OD-51 cost='Unknown' when unpriced)."""
    metered = check_usage_metering(check)
    return _apply_price_schedule(metered, price_schedule)


def _check_visible_to_user(check: Mapping[str, Any], user: Mapping[str, Any]) -> bool:
    role = str(user.get("role") or "")
    audience = check.get("audience")
    if isinstance(audience, (list, tuple, set, frozenset)) and role in audience:
        return True
    email = str(user.get("email") or "").strip().lower()
    owner = str(check.get("decision_owner") or "").strip().lower()
    return bool(email and owner and email == owner)


def summarize_checks(
    checks: Iterable[Mapping[str, Any]], user: Mapping[str, Any], day: str
) -> dict[str, Any]:
    """Summarize role-scoped reg_check usage outcomes for one UTC day without raw content."""
    if bool(user.get("view_only")) or user.get("role") not in _STAFF_ROLES:
        raise PermissionError("Only scoped staff can summarize check usage.")
    outcomes: Counter[str] = Counter()
    for check in checks:
        if not _check_visible_to_user(check, user):
            continue
        check_usage_metering(check)
        usage = cast(dict[str, Any], check["usage"])
        if usage["period"] == day:
            outcomes[str(usage["outcome"])] += 1
    return dict(
        schema=SCHEMA,
        surface="check",
        role=str(user["role"]),
        period=day,
        period_basis="UTC day",
        recorded_checks=sum(outcomes.values()),
        outcomes={name: outcomes[name] for name in TASKS["regulatory-check"]},
        model_calls=0,
        model_call_limit_per_role_period=0,
        economics=economics(),
    )


def economics() -> dict[str, Any]:
    return dict(
        cost="Unknown",
        ai_cost_per_accepted_check="Unknown",
        missing_inputs=[
            "Owner-agreed accepted-check definition and human acceptance count",
            "Dated versioned price source",
            "Attributable billing and shared-service allocation",
            "Measured human review effort",
        ],
        execution=dict(
            model_calls=0,
            input_tokens=0,
            output_tokens=0,
            model_call_limit=0,
            token_limit=0,
            paid_budget_limit=0,
            paid_authority="none",
            paid_authority_expires_at=None,
            reason="Offline only; no model dispatch or spend authority exists.",
        ),
    )


def summarize(details: Iterable[str], role: str, day: str, *, truncated: bool) -> dict[str, Any]:
    outcomes: Counter[str] = Counter()
    unmetered = 0
    for text in details:
        record = json.loads(text)
        if record.get("role") != role:
            continue
        usage = record.get("usage")
        if usage is None:
            unmetered += 1
            continue
        expected = offline_usage(
            "regulatory-home-chat",
            "regulatory-chat-v1",
            usage.get("outcome"),
            usage.get("period", "") + "T00:00:00+00:00",
        )
        if usage != expected or any(
            type(usage[key]) is not type(value) for key, value in expected.items()
        ):
            raise ValueError("Stored regulatory usage is invalid; audit review required.")
        try:
            usage_metering(usage, "audit-event")
        except ValueError:
            raise ValueError("Stored regulatory usage is invalid; audit review required.") from None
        if usage["period"] == day:
            outcomes[usage["outcome"]] += 1
    return dict(
        schema=SCHEMA,
        role=role,
        period=day,
        period_basis="UTC day",
        coverage="bounded_partial" if truncated else "recorded_audit_only",
        coverage_note=(
            "Recorded audit events only, not exact turn totals. Historical unmetered "
            "events and post-save JSON audit failures cannot be reconstructed."
        ),
        max_audit_positions=MAX_POSITIONS,
        max_json_bytes=MAX_BYTES,
        recorded_turns=sum(outcomes.values()),
        outcomes={name: outcomes[name] for name in TASKS["regulatory-home-chat"]},
        unmetered_events_in_window=unmetered,
        model_calls=0,
        model_call_limit_per_role_period=0,
        economics=economics(),
    )


def _audit_usage_access(store: Any, who: str, action: str, payload: dict[str, Any]) -> None:
    if store is None:
        return
    audit_fn = cast(Callable[[str, str, str, str], None], store.audit)
    audit_fn(who, action, "-", json.dumps(payload, sort_keys=True))


def _normalise_iso_time(raw: object, fallback_day: str) -> str:
    if isinstance(raw, str) and raw.strip():
        candidate = raw.strip()
        if candidate.endswith("Z"):
            candidate = candidate[:-1] + "+00:00"
        parsed = datetime.fromisoformat(candidate)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        utc_val = parsed.astimezone(UTC)
        if utc_val.date().isoformat() == fallback_day:
            return utc_val.isoformat()
    return f"{fallback_day}T00:00:00+00:00"


def _read_chat_turn_audit(
    store: Any, actor_key: str, role: str
) -> tuple[list[tuple[str, str, dict[str, Any]]], bool]:
    entries: list[tuple[str, str, dict[str, Any]]] = []
    if hasattr(store, "assistant_connection"):
        with store.dblock:
            latest_row = store.db.execute("SELECT MAX(seq) FROM audit").fetchone()
            latest = int(latest_row[0] or 0) if latest_row else 0
            rows = store.db.execute(
                "SELECT seq, CASE WHEN who=? AND action=? THEN detail ELSE NULL END, "
                "CASE WHEN who=? AND action=? THEN at ELSE NULL END "
                "FROM audit WHERE seq>? AND seq<=? ORDER BY seq",
                (
                    actor_key,
                    "chat.regulatory.turn",
                    actor_key,
                    "chat.regulatory.turn",
                    max(0, latest - MAX_POSITIONS),
                    latest,
                ),
            ).fetchall()
        truncated = latest > MAX_POSITIONS
        for seq, detail_text, at_text in rows:
            if detail_text is None:
                continue
            parsed = cast(dict[str, Any], json.loads(str(detail_text)))
            if parsed.get("role") != role or parsed.get("usage") is None:
                continue
            usage = _validate_stored_usage(
                parsed["usage"], "regulatory-home-chat", "regulatory-chat-v1"
            )
            occurred_at = _normalise_iso_time(at_text, str(usage["period"]))
            entries.append((f"chat-seq-{int(seq)}", occurred_at, usage))
        return entries, truncated
    try:
        stream = open(store.audit_path, "rb")
    except FileNotFoundError:
        raw_lines: list[bytes] = []
        truncated = False
    else:
        with stream:
            size = stream.seek(0, 2)
            start = max(0, size - MAX_BYTES)
            stream.seek(start)
            raw_lines = stream.read(size - start).splitlines()
        if start:
            raw_lines = raw_lines[1:]
        truncated = bool(start) or len(raw_lines) > MAX_POSITIONS
        raw_lines = raw_lines[-MAX_POSITIONS:]
    for idx, line in enumerate(raw_lines, 1):
        event = cast(dict[str, Any], json.loads(line))
        if event.get("who") != actor_key or event.get("action") != "chat.regulatory.turn":
            continue
        parsed = cast(dict[str, Any], json.loads(str(event["detail"])))
        if parsed.get("role") != role or parsed.get("usage") is None:
            continue
        usage = _validate_stored_usage(
            parsed["usage"], "regulatory-home-chat", "regulatory-chat-v1"
        )
        raw_time = event.get("at") or event.get("ts")
        occurred_at = _normalise_iso_time(raw_time, str(usage["period"]))
        thread_part = _SAFE_ID_SUB.sub("-", str(parsed.get("thread") or "t"))[:32]
        turn_part = int(parsed.get("turn") or parsed.get("messages") or idx)
        entries.append((f"turn-{thread_part}-{turn_part}"[:64], occurred_at, usage))
    return entries, truncated


def governed_metering_and_cost(
    store: Any,
    user: dict[str, Any],
    *,
    law: Any = None,
    surface: str = "all",
    env: Any = None,
    as_of: datetime | None = None,
    retention_days: int | None = None,
    price_schedule: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Read identifier/count/version-only chat and check metering and cost under shared controls."""
    if surface not in ("all", "chat", "check"):
        raise ValueError("surface must be 'all', 'chat' or 'check'.")
    now = datetime.now(UTC) if as_of is None else as_of
    if now.tzinfo is None:
        raise ValueError("Metering review needs a timezone-aware clock.")
    actor = str(user.get("email") or user.get("code") or "anonymous").strip().lower() or "anonymous"
    role = str(user.get("role") or "")
    try:
        if bool(user.get("view_only")):
            raise PermissionError("View-only administrators cannot read regulatory metering.")
        if role not in _STAFF_ROLES:
            raise PermissionError("Only scoped staff roles can read regulatory metering.")
        if is_trusted_proxy_user(user):
            if surface in ("all", "chat"):
                user = require_regulatory_role(user, "chat", require_entra=False)
            else:
                try:
                    user = require_regulatory_role(user, "chat", require_entra=False)
                except PermissionError:
                    user = require_regulatory_role(user, "approve", require_entra=False)
    except PermissionError as exc:
        _audit_usage_access(
            store,
            actor,
            "regulatory.metering.denied",
            dict(
                surface=surface,
                role=role,
                reason="role_or_capability_denied",
                label="synthetic-demo",
            ),
        )
        raise exc
    actor_key = _user_key(user)
    retention = retention_alignment(env, now, retention_days=retention_days)
    cutoff = (
        datetime.fromisoformat(str(retention["cutoff"]))
        if retention["cutoff"] is not None
        else None
    )
    metering_rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    filtered = 0
    truncated = False
    chat_count = 0
    check_count = 0
    if surface in ("all", "chat") and store is not None:
        turns, truncated = _read_chat_turn_audit(store, actor_key, role)
        for rec_id, occurred_at, usage in turns:
            if cutoff is not None and datetime.fromisoformat(occurred_at) < cutoff:
                filtered += 1
                continue
            metered = dict(usage_metering(usage, rec_id))
            metered["occurred_at"] = occurred_at
            validated_metered = metering_record(
                {k: v for k, v in metered.items() if k != "retention_class"}
            )
            metering_rows.append(validated_metered)
            cost_rows.append(
                chat_cost_record(
                    usage,
                    rec_id,
                    occurred_at=occurred_at,
                    price_schedule=price_schedule,
                )
            )
            chat_count += 1
    if surface in ("all", "check") and law is not None:
        with law.sql.lock:
            raw_checks = law.sql.all("SELECT id, at, body FROM reg_check ORDER BY check_seq, id")
        for row in raw_checks:
            parsed_body = cast(dict[str, Any], json.loads(str(row["body"])))
            raw_at = str(row["at"] or "")
            check_day = raw_at[:10] if len(raw_at) >= 10 else now.astimezone(UTC).date().isoformat()
            minimal_check = dict(
                id=row["id"],
                at=_normalise_iso_time(row["at"], check_day),
                card_id=parsed_body.get("card_id"),
                card_version=parsed_body.get("card_version"),
                audience=parsed_body.get("audience"),
                decision_owner=parsed_body.get("decision_owner"),
                usage=parsed_body.get("usage"),
            )
            if not _check_visible_to_user(minimal_check, user):
                continue
            if cutoff is not None and datetime.fromisoformat(str(minimal_check["at"])) < cutoff:
                filtered += 1
                continue
            metering_rows.append(check_usage_metering(minimal_check))
            cost_rows.append(check_cost_record(minimal_check, price_schedule=price_schedule))
            check_count += 1
    _audit_usage_access(
        store,
        actor_key,
        "regulatory.metering.read",
        dict(
            surface=surface,
            role=role,
            chat_records=chat_count,
            check_records=check_count,
            retention_filtered=filtered,
            retention_status=retention["status"],
            label="synthetic-demo",
        ),
    )
    return dict(
        label="synthetic-demo",
        surface=surface,
        role=role,
        dpo_reviewed=False,
        retention=retention,
        metering=metering_rows,
        cost=cost_rows,
        retention_filtered_count=filtered,
        truncated=truncated,
        economics=economics(),
    )
