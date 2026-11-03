"""Retrofit Flow Evidence Assistant readiness gate and read-only boundary (issue 125).

Pure, deterministic and read-only: no store, network, model or clock access. It encodes the
discovery brief's "Readiness Before Writing the Agent" list and "Authority and Safety Boundary" so a
design hypothesis cannot be connected to company data until a human supplies evidence for every
item, and so any tool request outside an explicit read-only allowlist is denied. It never connects
anything and never decides that readiness is approved; that stays with the named accountable
discovery owner. Manual analysis and export remain possible without any model.
"""

import re
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

BOUNDARY_VERSION = "discovery-assistant-boundary-v1"
READY_FOR_OWNER_DECISION = "READY_FOR_OWNER_DECISION"
NOT_READY = "NOT_READY"

READINESS_ITEMS: tuple[tuple[str, str], ...] = (
    ("accountable-owner", "Nominated the accountable discovery owner"),
    ("baseline-population", "Agreed the baseline population and accepted-handover endpoint"),
    ("lifecycle-dictionary", "Validated the current-state lifecycle and event dictionary"),
    ("source-identifier-map", "Produced the source-to-field and identifier map"),
    (
        "access-privacy-controls",
        "Approved lawful access, data minimisation, retention and security",
    ),
    ("delay-attribution-handling", "Defined delay, exception and disputed-attribution handling"),
    ("calculation-tests", "Established deterministic calculation and reconciliation tests"),
    ("human-reviewers", "Defined human reviewers and acceptance criteria"),
    ("non-agent-comparator", "Selected a non-agent comparator"),
    ("manual-path", "Confirmed manual analysis and export remain possible"),
)
ITEM_KEYS = tuple(key for key, _ in READINESS_ITEMS)

# Read-only capabilities named in the brief's Proposed Tools; anything else is denied by default.
ALLOWED_TOOLS: tuple[str, ...] = (
    "query_approved_analytical_store",
    "calculate_lifecycle_durations",
    "retrieve_source_record_lineage",
    "generate_evidence_document",
    "capture_human_review",
    "export_analysis_evidence",
)
# Capture of human review writes only to the assistant's own evidence log, never to a source system.
OWN_EVIDENCE_LOG_ONLY = frozenset({"capture_human_review", "generate_evidence_document"})
DENIED_AREAS: tuple[str, ...] = (
    "write_source_system",
    "progress_lifecycle_state",
    "infer_consent",
    "diagnose_hazard",
    "release_safety_hold",
    "approve_pas2035_output",
    "contact_resident",
    "schedule_appointment",
    "allocate_work",
    "award_contract",
    "commit_supplier_capacity",
    "accept_quality",
    "release_payment",
    "determine_grant_eligibility",
    "submit_claim",
    "rank_properties",
)

_REFERENCE = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._:/#-]{2,119}\Z")
_PLACEHOLDERS = frozenset({"tbc", "tbd", "todo", "n/a", "none", "pending", "unknown"})
MANUAL_PATH = (
    "Manual analysis, conventional reporting and export remain available; "
    "nothing here needs a model."
)


@dataclass(frozen=True)
class ReadinessEvidence:
    """A human-supplied pointer to evidence for one readiness item; never inferred."""

    item: str
    evidence_reference: str
    confirmed_by_role: str


@dataclass(frozen=True)
class ReadinessReport:
    boundary_version: str
    status: str
    satisfied: tuple[str, ...]
    missing: tuple[str, ...]
    invalid: tuple[str, ...]
    connection_to_company_data_permitted: bool = False
    approved_solution: bool = False
    manual_path: str = MANUAL_PATH
    next_step: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)


def _valid(value: object) -> bool:
    return (
        isinstance(value, str)
        and _REFERENCE.fullmatch(value) is not None
        and value.strip().lower() not in _PLACEHOLDERS
    )


def assess_readiness(evidence: Iterable[ReadinessEvidence]) -> ReadinessReport:
    """Report which readiness items have named evidence; never grants a connection.

    Even when every item has evidence, the result is only READY_FOR_OWNER_DECISION: the accountable
    discovery owner decides on connection, and this code never connects or describes the assistant
    as an approved solution.
    """
    seen: dict[str, ReadinessEvidence] = {}
    invalid: list[str] = []
    for entry in evidence:
        if entry.item not in ITEM_KEYS:
            invalid.append(f"unknown-item:{entry.item[:40]}")
        elif entry.item in seen:
            invalid.append(f"duplicate:{entry.item}")
        elif not (_valid(entry.evidence_reference) and _valid(entry.confirmed_by_role)):
            invalid.append(f"unusable-evidence:{entry.item}")
        else:
            seen[entry.item] = entry
    satisfied = tuple(k for k in ITEM_KEYS if k in seen)
    missing = tuple(k for k in ITEM_KEYS if k not in seen)
    ready = not missing and not invalid
    return ReadinessReport(
        boundary_version=BOUNDARY_VERSION,
        status=READY_FOR_OWNER_DECISION if ready else NOT_READY,
        satisfied=satisfied,
        missing=missing,
        invalid=tuple(invalid),
        next_step=(
            "Accountable discovery owner decides whether to approve a read-only connection."
            if ready
            else "Supply named evidence for each missing item; do not connect company data."
        ),
        notes=("Readiness evidence is a pointer supplied by a human, not verified by this code.",),
    )


@dataclass(frozen=True)
class ToolDecision:
    tool: str
    allowed: bool
    reason: str
    writes_to_source_system: bool = False


def authorise_tool(name: str) -> ToolDecision:
    """Default-deny: only the named read-only tools pass; anything else is refused."""
    if name in DENIED_AREAS:
        return ToolDecision(name, False, "DENIED_BY_AUTHORITY_BOUNDARY")
    if name not in ALLOWED_TOOLS:
        return ToolDecision(name, False, "NOT_ON_READ_ONLY_ALLOWLIST")
    reason = (
        "ALLOWED_OWN_EVIDENCE_LOG_ONLY" if name in OWN_EVIDENCE_LOG_ONLY else "ALLOWED_READ_ONLY"
    )
    return ToolDecision(name, True, reason)


class ToolDenied(PermissionError):
    pass


class ReadOnlyToolbox:
    """Dispatches only allowlisted tools and only once the readiness report is ready for decision.

    Callers pass tool callables; unlisted names never run, and no source-system writer can be
    registered because denied names are rejected at construction.
    """

    def __init__(self, tools: Mapping[str, Callable[..., Any]], readiness: ReadinessReport) -> None:
        if readiness.status != READY_FOR_OWNER_DECISION:
            raise ToolDenied("READINESS_NOT_SATISFIED")
        for name in tools:
            if not authorise_tool(name).allowed:
                raise ToolDenied(f"{name}: {authorise_tool(name).reason}")
        self._tools = dict(tools)
        self.denials: list[ToolDecision] = []

    def call(self, name: str, *args: Any, **kwargs: Any) -> Any:
        decision = authorise_tool(name)
        if not decision.allowed or name not in self._tools:
            self.denials.append(
                decision if not decision.allowed else ToolDecision(name, False, "NOT_REGISTERED")
            )
            raise ToolDenied(f"{name}: {self.denials[-1].reason}")
        return self._tools[name](*args, **kwargs)
