"""Pure monitoring-coverage checks (issue 146); no store, clock, network or Azure access.

The register states which alerts are installed, disabled candidates or explicit gaps, each with a
proposed owner role and runbook anchor. Roles are routing proposals, not appointments. Indicator
evaluation never reports green: missing samples, thresholds or approvals are insufficient or
blocked, and constructed thresholds are offline-only.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from zava_forward.core.rai_release import named

INSTALLED = "installed"
CANDIDATE = "candidate-disabled"
GAP = "gap"
DIGITAL = "Digital service owner"
FINANCE = "Finance budget owner"
TASK_OWNER = "Competent task owner"


@dataclass(frozen=True)
class AlertEntry:
    anchor: str
    status: str
    owner_role: str
    criterion: str
    source_file: str | None = None
    source_marker: str | None = None


def _a(anchor: str, status: str, owner: str, criterion: str, *source: str) -> AlertEntry:
    return AlertEntry(anchor, status, owner, criterion, *(source or (None, None)))


ALERTS: tuple[AlertEntry, ...] = (
    _a("foundry-client-errors", INSTALLED, DIGITAL, "chat", "main.bicep", "-foundry-throttle"),
    _a("sql-cpu", INSTALLED, DIGITAL, "availability", "main.bicep", "-sql-cpu"),
    _a("api-errors", INSTALLED, DIGITAL, "errors", "main.bicep", "-api-5xx"),
    _a("api-restarts", INSTALLED, DIGITAL, "availability", "main.bicep", "-api-restarts"),
    _a(
        "ledger-digest-mismatch",
        INSTALLED,
        DIGITAL,
        "ledger",
        "main.bicep",
        "ledger-digest-mismatch",
    ),
    _a(
        "ledger-verify-missing",
        INSTALLED,
        DIGITAL,
        "ledger",
        "main.bicep",
        "ledger-verify-missing",
    ),
    _a("vault-expiry", INSTALLED, DIGITAL, "secrets", "modules/keyvault.bicep", "secret-expiry"),
    _a("vault-denied", INSTALLED, DIGITAL, "secrets", "modules/keyvault.bicep", "denied-access"),
    _a("budget-actual80", INSTALLED, FINANCE, "budget", "main.bicep", "actual80"),
    _a("budget-forecast100", INSTALLED, FINANCE, "budget", "main.bicep", "forecast100"),
    _a("iot-budget-actual80", INSTALLED, FINANCE, "budget", "modules/iothub.bicep", "actual80"),
    _a(
        "iot-budget-forecast100",
        INSTALLED,
        FINANCE,
        "budget",
        "modules/iothub.bicep",
        "forecast100",
    ),
    _a(
        "job-orchestrator",
        CANDIDATE,
        DIGITAL,
        "jobs",
        "modules/operationalMonitoring.bicep",
        "'job-orchestrator'",
    ),
    _a(
        "job-ledger",
        CANDIDATE,
        DIGITAL,
        "jobs",
        "modules/operationalMonitoring.bicep",
        "'job-ledger'",
    ),
    _a(
        "job-import",
        CANDIDATE,
        DIGITAL,
        "jobs",
        "modules/operationalMonitoring.bicep",
        "'job-import'",
    ),
    _a("job-auth", CANDIDATE, DIGITAL, "jobs", "modules/operationalMonitoring.bicep", "'job-auth'"),
    _a(
        "iot-ingress-throttle",
        CANDIDATE,
        DIGITAL,
        "ingestion",
        "modules/operationalMonitoring.bicep",
        "iot-ingress-throttle",
    ),
    _a(
        "iot-routing-dropped",
        CANDIDATE,
        DIGITAL,
        "ingestion",
        "modules/operationalMonitoring.bicep",
        "iot-routing-dropped",
    ),
    _a(
        "iot-routing-invalid",
        CANDIDATE,
        DIGITAL,
        "ingestion",
        "modules/operationalMonitoring.bicep",
        "iot-routing-invalid",
    ),
    _a(
        "iot-routing-orphaned",
        CANDIDATE,
        DIGITAL,
        "ingestion",
        "modules/operationalMonitoring.bicep",
        "iot-routing-orphaned",
    ),
    _a("agent-tasks-poison", GAP, DIGITAL, "poison"),
    _a("import-jobs-poison", GAP, DIGITAL, "poison"),
    _a("ai-limits", GAP, TASK_OWNER, "ai-limits"),
    _a("rai-harm", GAP, TASK_OWNER, "harm"),
)
REQUIRED_CRITERIA = ("jobs", "poison", "ledger", "ingestion", "ai-limits", "harm", "budget")


def runbook_anchors(runbook_text: str) -> set[str]:
    """GitHub-style heading anchors of a Markdown document."""
    found = re.findall(r"^#{2,6}\s+(.+?)\s*$", runbook_text, flags=re.MULTILINE)
    return {re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-") for h in found}


def coverage_gaps(
    runbook_text: str,
    infra_sources: Mapping[str, str],
    register: Sequence[AlertEntry] = ALERTS,
) -> list[str]:
    """Return human-readable problems; an empty list means the register is self-consistent."""
    problems: list[str] = []
    anchors = runbook_anchors(runbook_text)
    seen: set[str] = set()
    for entry in register:
        if entry.anchor in seen:
            problems.append(f"{entry.anchor}: duplicate register entry")
        seen.add(entry.anchor)
        if not named(entry.owner_role):
            problems.append(f"{entry.anchor}: no owner role")
        if entry.anchor not in anchors:
            problems.append(f"{entry.anchor}: no runbook heading")
        if entry.status not in (INSTALLED, CANDIDATE, GAP):
            problems.append(f"{entry.anchor}: unknown status {entry.status!r}")
        elif entry.status in (INSTALLED, CANDIDATE):
            text = infra_sources.get(entry.source_file or "")
            if text is None or not entry.source_marker or entry.source_marker not in text:
                problems.append(f"{entry.anchor}: not found in {entry.source_file}")
        elif entry.source_file:
            problems.append(f"{entry.anchor}: gap must not claim a source")
    covered = {e.criterion for e in register}
    problems.extend(
        f"criterion {c}: no register entry" for c in REQUIRED_CRITERIA if c not in covered
    )
    return problems


INSUFFICIENT = "insufficient"
BLOCKED = "blocked"
WITHIN = "within-threshold"
BREACH = "breach"


def _count(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def evaluate_indicator(
    *,
    events: Any,
    denominator: Any,
    window_complete: bool,
    threshold: Mapping[str, Any] | None,
    incident_owner: str | None,
) -> dict[str, Any]:
    """Classify one harm, quality or AI-limit indicator; there is deliberately no green state.

    `threshold` holds `limit` (rate 0..1), `min_sample`, and either `approved_by` (a named human,
    live use) or `constructed: True` (offline tests only). A breach needs a named incident owner.
    """
    constructed = bool(threshold and threshold.get("constructed") is True)
    result: dict[str, Any] = {"status": BLOCKED, "reason": "", "offline_only": constructed}
    limit = threshold.get("limit") if threshold else None
    min_sample = threshold.get("min_sample") if threshold else None
    if not (
        isinstance(limit, int | float)
        and not isinstance(limit, bool)
        and 0 <= limit <= 1
        and math.isfinite(limit)
        and _count(min_sample)
    ):
        result["reason"] = "threshold missing or invalid"
        return result
    assert threshold is not None
    if not constructed and not named(threshold.get("approved_by")):
        result["reason"] = "live threshold needs named human approval"
        return result
    if not (_count(events) and _count(denominator)) or events > denominator:
        result["reason"] = "invalid counts"
        return result
    if not window_complete:
        result.update(status=INSUFFICIENT, reason="observation window incomplete")
        return result
    if denominator == 0 or denominator < int(min_sample or 0):
        result.update(status=INSUFFICIENT, reason="sample below minimum")
        return result
    rate = events / denominator
    result["rate"] = round(rate, 4)
    if rate <= limit:
        result.update(status=WITHIN, reason="not proof of safety")
        return result
    result["status"] = BREACH
    result["incident_required"] = True
    result["incident_owner"] = incident_owner if named(incident_owner) else None
    result["reason"] = "threshold breached" if result["incident_owner"] else "breach without owner"
    return result


HARM_INDICATORS = (
    "unsupported_claims",
    "critical_misses",
    "stale_review_attempts",
    "challenges",
    "cohort_errors",
    "review_effort",
)
DECLARED = "declared"


def check_monitoring_declaration(
    declaration: Mapping[str, Any] | None, *, task_enabled: bool
) -> dict[str, Any]:
    """Check one task or serving release declaration; it never reports a green or approved state.

    Each indicator in `HARM_INDICATORS` needs either `applicable: False` with a `reason`, or a
    `denominator`, `window` and a threshold that is constructed (offline only) or approved by a
    named human. The release needs named monitoring and incident owners and a response. Ownership
    and the manual-route status are exposed even when the task is disabled or the declaration is
    blocked, so a switched-off task still shows who monitors it.
    """
    record: Mapping[str, Any] = declaration or {}
    manual = record.get("manual_route_status")
    result: dict[str, Any] = {
        "status": BLOCKED,
        "task_enabled": task_enabled,
        "monitoring_owner": record.get("monitoring_owner")
        if named(record.get("monitoring_owner"))
        else None,
        "incident_owner": record.get("incident_owner")
        if named(record.get("incident_owner"))
        else None,
        "manual_route_status": manual if named(manual) else None,
        "missing": [],
        "offline_only": False,
    }
    missing: list[str] = result["missing"]
    for key in ("monitoring_owner", "incident_owner", "response"):
        if not named(record.get(key)):
            missing.append(key)
    if not task_enabled and result["manual_route_status"] is None:
        missing.append("manual_route_status")
    indicators = record.get("indicators")
    entries: Mapping[str, Any] = indicators if isinstance(indicators, Mapping) else {}
    for name in HARM_INDICATORS:
        entry = entries.get(name)
        if not isinstance(entry, Mapping):
            missing.append(f"indicator:{name}")
        elif entry.get("applicable") is False:
            if not named(entry.get("reason")):
                missing.append(f"indicator:{name}:reason")
        elif not _count(entry.get("denominator")) or not entry.get("denominator"):
            missing.append(f"indicator:{name}:denominator")
        elif not named(entry.get("window")):
            missing.append(f"indicator:{name}:window")
        else:
            threshold = entry.get("threshold")
            check = evaluate_indicator(
                events=0,
                denominator=entry["denominator"],
                window_complete=True,
                threshold=threshold if isinstance(threshold, Mapping) else None,
                incident_owner=None,
            )
            if check["status"] == BLOCKED:
                missing.append(f"indicator:{name}:threshold")
            elif check["offline_only"]:
                result["offline_only"] = True
    if not missing:
        result["status"] = DECLARED
    return result


AI_DIMENSIONS = ("calls", "tokens", "cost")
UNKNOWN = "unknown"
COUNTED = "counted"


def _aware(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else None


def evaluate_ai_limits(
    *,
    usage: Mapping[str, Any],
    limits: Mapping[str, Any] | None,
    expires_at: Any,
    as_of: Any,
    approved_by: Any = None,
    constructed: bool = False,
    price_source: Any = None,
    owner: Any = None,
) -> dict[str, Any]:
    """Classify one capability/period against finite call, token, cost and expiry limits.

    There is no green state and no invented price: cost without a named `price_source` is
    unknown, and absent usage is insufficient, never zero. Live limits need a named approver;
    `constructed` limits are offline tests only. A breach names the alert owner and the
    `ai-limits` runbook anchor, and carries no suspension authority.
    """
    result: dict[str, Any] = {
        "status": BLOCKED,
        "reason": "",
        "offline_only": constructed,
        "dimensions": {},
        "runbook": "ai-limits",
        "owner": owner if named(owner) else None,
    }
    if not constructed and not named(approved_by):
        result["reason"] = "live limits need named human approval"
        return result
    expiry, now = _aware(expires_at), _aware(as_of)
    if now is None or not limits:
        result["reason"] = "limits or as-of time missing or invalid"
        return result
    dims: dict[str, str] = {}
    for name in AI_DIMENSIONS:
        limit, used = limits.get(name), usage.get(name)
        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            dims[name] = BLOCKED
        elif name == "cost" and not named(price_source):
            dims[name] = UNKNOWN
        elif not isinstance(used, int) or isinstance(used, bool) or used < 0:
            dims[name] = INSUFFICIENT
        else:
            dims[name] = BREACH if used > limit else WITHIN
    if expiry is None:
        dims["expiry"] = BLOCKED
    else:
        dims["expiry"] = BREACH if now >= expiry else WITHIN
    result["dimensions"] = dims
    states = set(dims.values())
    if BREACH in states:
        result["status"] = BREACH
        result["incident_required"] = True
        result["reason"] = "limit breached" if result["owner"] else "breach without owner"
    elif BLOCKED in states:
        result["reason"] = "limit or expiry missing or invalid"
    elif states & {INSUFFICIENT, UNKNOWN}:
        result.update(status=INSUFFICIENT, reason="usage or price source missing")
    else:
        result.update(status=WITHIN, reason="not proof of value or safety")
    return result


def reconcile_events(
    events: Sequence[Mapping[str, Any]], *, window_start: Any, window_end: Any
) -> dict[str, Any]:
    """Count distinct events in a half-open window so replays after a restart do not double count.

    Events need a bounded `event_id` token and an aware ISO `observed_at`; others are counted as
    invalid, and an invalid window yields no count.
    """
    start, end = _aware(window_start), _aware(window_end)
    out: dict[str, Any] = {"count": None, "duplicates": 0, "outside_window": 0, "invalid": 0}
    if start is None or end is None or end <= start:
        out["status"] = BLOCKED
        return out
    seen: set[str] = set()
    for event in events:
        event_id, at = event.get("event_id"), _aware(event.get("observed_at"))
        if not isinstance(event_id, str) or _TOKEN.fullmatch(event_id) is None or at is None:
            out["invalid"] += 1
        elif event_id in seen:
            out["duplicates"] += 1
        elif not start <= at < end:
            out["outside_window"] += 1
        else:
            seen.add(event_id)
    out["count"] = len(seen)
    out["status"] = BLOCKED if out["invalid"] else COUNTED if seen else INSUFFICIENT
    return out


ALLOWED_FIELDS = frozenset(
    {
        "alert",
        "severity",
        "task",
        "release",
        "window_start",
        "window_end",
        "count",
        "denominator",
        "status",
        "owner_role",
        "offline_only",
    }
)
_SENSITIVE = re.compile(
    r"[\w.+-]+@[\w-]+\.[\w.]+|eyJ[\w-]{8,}\.[\w-]+|bearer\s+\S+|\b\d{1,3}(?:\.\d{1,3}){3}\b",
    re.IGNORECASE,
)
_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,63}")
_TIMESTAMP = re.compile(
    r"\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})?)?"
)
_STATUSES = frozenset({INSTALLED, CANDIDATE, GAP, INSUFFICIENT, BLOCKED, WITHIN, BREACH})
_SEVERITIES = frozenset({"0", "1", "2", "3", "4", "info", "low", "medium", "high", "critical"})
MAX_COUNT = 10**9
MAX_TEXT = 64


def _parses(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _valid(key: str, value: Any) -> bool:
    if key in ("count", "denominator"):
        return _count(value) and value <= MAX_COUNT
    if key == "offline_only":
        return isinstance(value, bool)
    if not isinstance(value, str) or len(value) > MAX_TEXT or _SENSITIVE.search(value):
        return False
    if key == "alert":
        return value in {e.anchor for e in ALERTS}
    if key == "owner_role":
        return value in {e.owner_role for e in ALERTS}
    if key == "status":
        return value in _STATUSES
    if key == "severity":
        return value.lower() in _SEVERITIES
    if key in ("window_start", "window_end"):
        return _TIMESTAMP.fullmatch(value) is not None and _parses(value)
    return _TOKEN.fullmatch(value) is not None


def sanitize_diagnostic(event: Mapping[str, Any]) -> dict[str, Any]:
    """Keep only allowlisted fields whose values match a field-specific aggregate schema.

    Free text, identities, tokens and unregistered values are dropped, not truncated.
    """
    return {k: v for k, v in event.items() if k in ALLOWED_FIELDS and _valid(k, v)}
