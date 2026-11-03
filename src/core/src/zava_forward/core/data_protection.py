"""Whole-system data protection register, model-dispatch gate and rights clock (#121).

Reference-only: recorded references are not verified DPO or Legal approval, no legal conclusion or
retention period is set here, and nothing is stored, sent or deleted. Constructed fixtures are the
only data permitted to reach a model until qualified owners record the approvals.
"""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import datetime
from typing import Any

OWNER_ROLES = "DPO and Legal (named owners not yet recorded; issue #121 dependency)"
MANUAL_PATH = "Handle the item manually; a named human decides. No model is used."
GATES = ("LAWFUL_BASIS", "ART9", "RETENTION", "ERASURE", "TRANSFER", "NECESSITY")


@dataclass(frozen=True)
class DataClass:
    id: str
    name: str
    kind: str  # constructed | actual
    purpose: str
    audience: str
    storage: str
    special_category: bool = False
    model_bound: bool = False
    needs_derivative: bool = False
    provider_copy: str = "None known; provider terms are unverified"


DATA_CLASSES = (
    DataClass(
        "fixture_resident",
        "Constructed resident fixtures",
        "constructed",
        "Offline development and demonstration",
        "Developers and demonstration users",
        "Fixture files and demo SQL; entirely constructed",
        model_bound=True,
    ),
    DataClass(
        "staff_identity",
        "Staff identities and role assignments",
        "actual",
        "Access control and attribution of actions",
        "Administrators and auditors",
        "Entra ID claims, SQL actor columns",
    ),
    DataClass(
        "tenant_identity",
        "Actual tenant or representative identities",
        "actual",
        "Future case management under the tenancy contract",
        "Case staff",
        "Not collected by the demonstrator",
        special_category=True,
        model_bound=True,
    ),
    DataClass(
        "review_record",
        "Reviewer identity and review decisions",
        "actual",
        "Evidence of named human approval",
        "Approvers and auditors",
        "SQL review and approval rows, audit ledger",
    ),
    DataClass(
        "raw_document",
        "Uploaded document and image bytes",
        "actual",
        "Evidence storage for a case",
        "Case staff",
        "Blob storage with scan tags",
        special_category=True,
        model_bound=True,
        needs_derivative=True,
    ),
    DataClass(
        "prompt_output",
        "Prompts, outputs and citations",
        "actual",
        "Bounded assistant answers with sources",
        "Signed-in staff",
        "Not stored by Zava except chat threads; provider copy unknown",
        model_bound=True,
        provider_copy="Provider abuse-monitoring and retention terms unknown",
    ),
    DataClass(
        "audit_ledger",
        "Audit ledger entries",
        "actual",
        "Tamper-evident record of actions",
        "Auditors",
        "Append-only SQL ledger, digests in locked Blob",
    ),
    DataClass(
        "telemetry",
        "Diagnostics, telemetry and token counts",
        "actual",
        "Operation and metering without content",
        "Operators",
        "Process output, Azure Monitor",
    ),
)
BY_ID = {c.id: c for c in DATA_CLASSES}

# field -> (type, max length); mirrors regulatory_privacy.QUERY_FIELDS
_TEXT = (str, 80)
TASKS: dict[str, dict[str, Any]] = {
    "rule_lookup": dict(
        purpose="Find a rule card or provision",
        audience="Authorised staff",
        necessity="Source identifiers locate the provision; no resident data is needed",
        prohibited="Names, addresses, health, safeguarding, free text about a person",
        fields=dict(
            card_id=_TEXT,
            card_version=_TEXT,
            provision_id=_TEXT,
            source_id=_TEXT,
            version=_TEXT,
            as_of=(str, 10),
        ),
    ),
    "check_explain": dict(
        purpose="Explain a regulatory check outcome",
        audience="Authorised staff",
        necessity="Check kind and outcome explain the result; case is an opaque id",
        prohibited="Resident names, contact details, special-category data",
        fields=dict(
            card_id=_TEXT,
            card_version=_TEXT,
            check_kind=_TEXT,
            outcome=_TEXT,
            as_of=(str, 10),
            case_id=_TEXT,
        ),
    ),
    "alert_triage": dict(
        purpose="Summarise a regulatory alert",
        audience="Authorised staff",
        necessity="Alert and source identifiers are sufficient",
        prohibited="Any resident data",
        fields=dict(alert_id=_TEXT, source_id=_TEXT, version=_TEXT, status=_TEXT, as_of=(str, 10)),
    ),
}
SPECIAL_FIELDS = frozenset(
    {"health", "disability", "ethnicity", "religion", "safeguarding", "vulnerability", "notes"}
)


def _ref(env: Any, class_id: str, gate: str) -> str:
    return str(env.get(f"DP_{class_id.upper()}_{gate}_REF") or "").strip()


def required_gates(c: DataClass) -> tuple[str, ...]:
    gates = ["LAWFUL_BASIS", "RETENTION", "ERASURE"]
    if c.special_category:
        gates.append("ART9")
    if c.model_bound:
        gates.append("TRANSFER")
    if c.needs_derivative:
        gates.append("NECESSITY")
    return tuple(g for g in GATES if g in gates)


def register_report(env: Any) -> dict[str, Any]:
    """Per class: which approvals are recorded. Never echoes values or claims approval."""
    rows = []
    for c in DATA_CLASSES:
        need = required_gates(c)
        refs = {g: _ref(env, c.id, g) for g in need}
        missing = [g for g, r in refs.items() if not r]
        synthetic = [g for g, r in refs.items() if r.startswith("SYNTH-")]
        rows.append(
            dict(
                id=c.id,
                name=c.name,
                kind=c.kind,
                purpose=c.purpose,
                audience=c.audience,
                storage=c.storage,
                special_category=c.special_category,
                provider_copy=c.provider_copy,
                required=list(need),
                missing=missing,
                synthetic=synthetic,
                references_recorded=c.kind == "actual" and not missing and not synthetic,
                retention="Unknown until Legal sets a period"
                if "RETENTION" in missing
                else "Reference recorded; period held by owner",
            )
        )
    return dict(
        label="synthetic-demo",
        owners=OWNER_ROLES,
        dpo_reviewed=False,
        classes=rows,
        statement=(
            "Recorded references are not verified DPO or Legal approval. "
            "Local deletion is not provider erasure."
        ),
    )


def model_dispatch(class_id: str, env: Any, derivative: str | None = None) -> dict[str, Any]:
    """Deny model dispatch for actual data until required references exist and none is synthetic."""
    c = BY_ID.get(class_id)
    if c is None:
        return dict(permitted=False, reason="Unknown data class", manual_path=MANUAL_PATH)
    if c.kind == "constructed":
        return dict(
            permitted=True,
            reason="Entirely constructed fixture; no actual processing",
            manual_path=MANUAL_PATH,
        )
    if not c.model_bound:
        return dict(
            permitted=False, reason="This class is never sent to a model", manual_path=MANUAL_PATH
        )
    need = required_gates(c)
    bad = [g for g in need if not _ref(env, c.id, g) or _ref(env, c.id, g).startswith("SYNTH-")]
    if bad:
        return dict(
            permitted=False,
            reason="Approvals not recorded: " + ", ".join(bad),
            manual_path=MANUAL_PATH,
        )
    if c.needs_derivative and derivative != "reviewed_redacted":
        return dict(
            permitted=False,
            reason="Intact material is not sent; use a reviewed, redacted derivative",
            manual_path=MANUAL_PATH,
        )
    return dict(
        permitted=True,
        reason="References recorded; human approval is not verified by this check",
        manual_path=MANUAL_PATH,
    )


def validate_task_payload(task: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Keep only declared fields of the declared type and length; report names, never values."""
    spec = TASKS.get(task)
    if spec is None:
        return dict(permitted=False, fields={}, dropped=[], rejected=[], manual_path=MANUAL_PATH)
    kept: dict[str, Any] = {}
    rejected = []
    for name, (kind, limit) in spec["fields"].items():
        if name not in payload:
            continue
        value = payload[name]
        if isinstance(value, kind) and len(value) <= limit:
            kept[name] = value
        else:
            rejected.append(name)
    return dict(
        permitted=True,
        fields=kept,
        rejected=sorted(rejected),
        dropped=sorted(k for k in payload if k not in spec["fields"]),
        special_category_dropped=sorted(k for k in payload if k in SPECIAL_FIELDS),
        purpose=spec["purpose"],
        audience=spec["audience"],
        manual_path=MANUAL_PATH,
    )


def due_date(received: datetime) -> datetime:
    """One calendar month after receipt, clamped to month end. Extensions are a DPO decision."""
    if received.tzinfo is None:
        raise ValueError("Rights request time needs a timezone.")
    month = received.month % 12 + 1
    year = received.year + (received.month == 12)
    day = min(received.day, calendar.monthrange(year, month)[1])
    return received.replace(year=year, month=month, day=day)


def rights_status(requests: list[dict[str, Any]], now: datetime) -> dict[str, Any]:
    """Classify rights requests: rows hold id, kind, received_at (ISO), optional answered_at."""
    rows = []
    for r in requests:
        due = due_date(datetime.fromisoformat(r["received_at"]))
        answered = r.get("answered_at")
        late = datetime.fromisoformat(answered) > due if answered else now > due
        state = (
            "answered_late"
            if answered and late
            else "answered"
            if answered
            else "overdue"
            if late
            else "open"
        )
        rows.append(dict(id=r["id"], kind=r["kind"], due=due.isoformat(), state=state))
    return dict(
        label="synthetic-demo",
        requests=rows,
        overdue=[r["id"] for r in rows if r["state"] == "overdue"],
        note="In-memory classification only: no rights log is persisted or answered here.",
    )
