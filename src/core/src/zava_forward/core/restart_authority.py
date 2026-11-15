"""RULE-024 human restart authority validation and distinct-actor separation controls.

Enforces explicit, non-placeholder, non-automated, distinct human restart authority naming and
multi-person separation across guardrail breach pauses and AI operator suspensions (RULE-024,
FR-053, AC-072, AC-078, NFR-014). Error messages never echo raw authority strings or actor PII.
"""

import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

from . import controls

RULE_024 = "RULE-024"
UNAPPOINTED_RESTART_AUTHORITY = "Unavailable: OD-35 authority unappointed"

_EXACT_PLACEHOLDERS: frozenset[str] = frozenset(
    {
        "unknown",
        "unavailable",
        "none",
        "null",
        "n/a",
        "na",
        "tbd",
        "todo",
        "tbc",
        "pending",
        "placeholder",
        "unapproved",
        "unappointed",
        "unassigned",
        "unset",
        "default",
        "self",
        "same operator",
        "same person",
        "-",
        "--",
        "?",
    }
)

_PLACEHOLDER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(?:tbd|todo|tbc|placeholder|unappointed|unassigned|unapproved)\b", re.I),
    re.compile(r"^pending\b", re.I),
    re.compile(r"\bsame\s+(?:operator|person|user|approver)\b", re.I),
    re.compile(
        r"\bself[-\s]+(?:approved|approval|authorised|authorized|designated|signoff|sign-off)\b",
        re.I,
    ),
)

_WORD_SPLIT = re.compile(r"[^a-z0-9]+")

_EXACT_NON_HUMAN: frozenset[str] = frozenset(
    {
        "system",
        "agent",
        "model",
        "workflow",
        "scheduler",
        "pipeline",
        "service",
        "script",
        "timer",
        "webhook",
    }
)

_NON_HUMAN_TOKENS: frozenset[str] = frozenset(
    {
        "ai",
        "bot",
        "automation",
        "automated",
        "automatic",
        "copilot",
        "llm",
        "cron",
        "daemon",
    }
)

_NON_HUMAN_PHRASES: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bai\s+(?:assistant|agent|model|system|service)\b", re.I),
    re.compile(r"\bauto(?:matic|mated)?[-\s]+restart\b", re.I),
    re.compile(r"\b(?:automated|autonomous)\s+(?:system|agent|workflow|process|restart)\b", re.I),
    re.compile(r"\bsystem\s+auto(?:matic|mated)?\b", re.I),
)

_ACTOR_KEYS: tuple[str, ...] = (
    "email",
    "display_email",
    "name",
    "role",
    "code",
    "oid",
    "auth_source",
)


def _clean(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _contains_boundary_term(haystack_cf: str, term_cf: str) -> bool:
    pattern = rf"(?<![a-z0-9]){re.escape(term_cf)}(?![a-z0-9])"
    return re.search(pattern, haystack_cf) is not None


def actor_snapshot(user: Mapping[str, Any]) -> dict[str, str]:
    """Return a normalized non-empty identity snapshot for audit and separation checks."""
    snap: dict[str, str] = {}
    for key in _ACTOR_KEYS:
        val = _clean(user.get(key))
        if val:
            snap[key] = val
    return snap


def reject_automatic_restart(body: Mapping[str, Any]) -> None:
    """Refuse any automatic restart flag per RULE-024."""
    for key in ("automatic", "auto_restart"):
        flag = body.get(key)
        if flag is not None and flag is not False:
            raise PermissionError(
                "RULE-024 forbids automatic restart after a guardrail breach "
                "or operator suspension."
            )


def actors_for_store(store: Any, user: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    """Return user plus any roster rows sharing user's immutable oid for fail-closed separation."""
    out: list[Mapping[str, Any]] = [user]
    oid = _clean(user.get("oid"))
    if not oid:
        return tuple(out)
    rows: list[Any] = []
    if hasattr(store, "db") and hasattr(store, "dblock"):
        with store.dblock:
            rows = [json.loads(r[0]) for r in store.db.execute("SELECT body FROM staff").fetchall()]
    elif hasattr(store, "staff") and isinstance(store.staff, Mapping):
        rows = list(store.staff.values())
    for row in rows:
        if isinstance(row, Mapping) and _clean(row.get("oid")).casefold() == oid.casefold():
            out.append(row)
    return tuple(out)


def _matches_actor_designation(text_cf: str, actor: Mapping[str, Any] | str | None) -> bool:
    if actor is None:
        return False
    if isinstance(actor, str):
        ident_cf = _clean(actor).casefold()
        if not ident_cf:
            return False
        if text_cf == ident_cf:
            return True
        if "@" in ident_cf and ident_cf in text_cf:
            return True
        return len(ident_cf) >= 3 and _contains_boundary_term(text_cf, ident_cf)
    bound = actor.get("bound")
    if isinstance(bound, Mapping) and _matches_actor_designation(text_cf, bound):
        return True
    for key in ("email", "display_email", "oid"):
        ident_cf = _clean(actor.get(key)).casefold()
        if not ident_cf:
            continue
        if text_cf == ident_cf or ident_cf in text_cf:
            return True
    for key in ("code", "name"):
        ident_cf = _clean(actor.get(key)).casefold()
        if not ident_cf:
            continue
        if text_cf == ident_cf:
            return True
        if len(ident_cf) >= 3 and _contains_boundary_term(text_cf, ident_cf):
            return True
    return False


def validate_restart_authority(
    value: object,
    *,
    label: str = "the restart authority (OD-35)",
    limit: int = 200,
    allow_unappointed_default: bool = False,
    disallowed_actors: Sequence[Mapping[str, Any] | str | None] = (),
    authority_error: type[Exception] = ValueError,
) -> str:
    """Validate a RULE-024 human restart authority designation without echoing raw input."""
    text = _clean(value)
    if not text or len(text) > limit:
        raise ValueError(f"Enter {label} (up to {limit} characters).")
    if controls.MEMORY_REF.search(text):
        raise ValueError(
            f"Do not cite chat memory as {label}; "
            "record an accountable human authority under RULE-024."
        )
    if allow_unappointed_default and text == UNAPPOINTED_RESTART_AUTHORITY:
        return UNAPPOINTED_RESTART_AUTHORITY

    text_cf = text.casefold()
    if (
        text_cf in _EXACT_PLACEHOLDERS
        or text_cf.startswith("unavailable")
        or any(pattern.search(text) for pattern in _PLACEHOLDER_PATTERNS)
    ):
        raise authority_error(
            f"RULE-024 requires an appointed human designation for {label}; "
            "placeholder or unappointed values cannot authorise restart."
        )

    words = {tok for tok in _WORD_SPLIT.split(text_cf) if tok}
    if (
        text_cf in _EXACT_NON_HUMAN
        or (words & _NON_HUMAN_TOKENS)
        or any(pattern.search(text) for pattern in _NON_HUMAN_PHRASES)
    ):
        raise authority_error(
            f"RULE-024 requires a named human authority for {label}; "
            "automated or AI designations cannot authorise restart."
        )

    for actor in disallowed_actors:
        if _matches_actor_designation(text_cf, actor):
            raise PermissionError(
                "RULE-024 requires a distinct human restart authority; "
                "an operator who recorded or proposed the incident cannot self-designate."
            )
    return text


def _actor_emails(actor: Mapping[str, Any]) -> set[str]:
    emails = {
        _clean(actor.get("email")).casefold(),
        _clean(actor.get("display_email")).casefold(),
    }
    bound = actor.get("bound")
    if isinstance(bound, Mapping):
        emails.add(_clean(bound.get("email")).casefold())
    emails.discard("")
    return emails


def _same_actor(user: Mapping[str, Any], prior: Mapping[str, Any] | str | None) -> bool:
    if prior is None:
        return False
    user_emails = _actor_emails(user)
    user_name = _clean(user.get("name")).casefold()
    user_code = _clean(user.get("code")).casefold()
    user_oid = _clean(user.get("oid")).casefold()
    bound = user.get("bound")
    bound_code = _clean(bound.get("code")).casefold() if isinstance(bound, Mapping) else ""
    if isinstance(prior, str):
        ident = _clean(prior).casefold()
        if not ident:
            return False
        tokens = set(user_emails) | {
            val for val in (user_name, user_code, bound_code, user_oid) if val
        }
        return ident in tokens
    if user_emails & _actor_emails(prior):
        return True
    prior_bound = prior.get("bound")
    prior_codes = {
        _clean(prior.get("code")).casefold(),
        _clean(prior_bound.get("code")).casefold() if isinstance(prior_bound, Mapping) else "",
    } - {""}
    user_codes = {val for val in (user_code, bound_code) if val}
    if user_codes & prior_codes:
        return True
    for user_val, key in (
        (user_oid, "oid"),
        (user_name, "name"),
    ):
        prior_val = _clean(prior.get(key)).casefold()
        if user_val and prior_val and user_val == prior_val:
            return True
    return False


def ensure_distinct_restart_actor(
    user: Mapping[str, Any],
    *prior_actors: Mapping[str, Any] | str | None,
    prior_role_description: str,
) -> None:
    """Refuse self-approval when user matches any prior actor by email, OID, code, or name."""
    for prior in prior_actors:
        if _same_actor(user, prior):
            raise PermissionError(
                f"RULE-024 requires a distinct human authority: the person who "
                f"{prior_role_description} cannot adjudicate or authorise restart."
            )
