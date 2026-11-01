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
