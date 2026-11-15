"""Whole-system data protection register, model-dispatch gate and rights clock (#121).

Reference-only: recorded references are not verified DPO or Legal approval, no legal conclusion or
retention period is set here, and nothing is stored, sent or deleted. Constructed fixtures are the
only data permitted to reach a model until qualified owners record the approvals.
"""

from __future__ import annotations

import calendar
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
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
        "Append-only SQL ledger, digests in Blob with an unlocked immutability policy",
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


MODE_ENV = "ZF_DATA_PROCESSING"
APPROVED_DERIVATIVE = "reviewed_redacted"
CONSTRUCTED_DERIVATIVE = "synthetic_safe"
_AUTOMATED_APPROVERS = frozenset(
    {"ai", "model", "assistant", "system", "auto", "automated", "bot", "llm"}
)


def actual_mode(env: Any = None) -> bool:
    mapping = os.environ if env is None else env
    return str(mapping.get(MODE_ENV) or "constructed").strip().lower() != "constructed"


def validate_necessity_exception(
    exception: Any,
    *,
    task: str = "read_document",
    case_id: str | None = None,
    doc_id: str | None = None,
    actual: bool = False,
    as_of: str | date | datetime | None = None,
) -> dict[str, Any]:
    """Verify whether a human-authorized text-only derivative may be sent to an external model."""
    if not isinstance(exception, Mapping):
        return dict(
            permitted=False,
            reason="Scoped necessity exception must be a recorded object",
            exception=None,
        )

    def _clean_str(key: str, label: str, limit: int) -> tuple[str | None, str | None]:
        val = exception.get(key)
        if not isinstance(val, str) or not val.strip():
            return None, f"Scoped necessity exception requires {label}"
        text = val.strip()
        if len(text) > limit:
            return None, f"Scoped necessity exception {label} exceeds {limit} characters"
        return text, None

    ref_key = "reference" if "reference" in exception else "id"
    reference, err = _clean_str(ref_key, "a reference", 120)
    if err or reference is None:
        return dict(permitted=False, reason=err or "Invalid reference", exception=None)
    if actual and reference.upper().startswith("SYNTH-"):
        return dict(
            permitted=False,
            reason="Synthetic necessity exception reference is not valid for actual processing",
            exception=None,
        )
    approved_by, err = _clean_str("approved_by", "a named human approver", 120)
    if err or approved_by is None:
        return dict(permitted=False, reason=err or "Invalid approver", exception=None)
    approver_tokens = {tok for tok in re.split(r"[^a-z0-9]+", approved_by.casefold()) if tok}
    if approved_by.casefold() in _AUTOMATED_APPROVERS or bool(
        approver_tokens & _AUTOMATED_APPROVERS
    ):
        return dict(
            permitted=False,
            reason="Scoped necessity exception requires a named human approver",
            exception=None,
        )
    reason, err = _clean_str("reason", "a necessity reason", 300)
    if err or reason is None:
        return dict(permitted=False, reason=err or "Invalid reason", exception=None)

    raw_scope = exception.get("task") if "task" in exception else exception.get("scope")
    if not isinstance(raw_scope, str) or not raw_scope.strip() or len(raw_scope.strip()) > 80:
        return dict(
            permitted=False,
            reason=f"Scoped necessity exception must specify task {task}",
            exception=None,
        )
    scope_task = raw_scope.strip()
    if scope_task.casefold() in {"*", "all", "any"} or scope_task != task:
        return dict(
            permitted=False,
            reason=f"Scoped necessity exception scope does not match {task}",
            exception=None,
        )

    cleaned: dict[str, str] = dict(
        reference=reference,
        approved_by=approved_by,
        reason=reason,
        task=scope_task,
    )

    raw_case = exception.get("case_id")
    if case_id is not None:
        if not isinstance(raw_case, str) or raw_case.strip() != case_id:
            return dict(
                permitted=False,
                reason="Scoped necessity exception does not match this case",
                exception=None,
            )
        cleaned["case_id"] = raw_case.strip()
    elif raw_case is not None:
        if not isinstance(raw_case, str) or not (1 <= len(raw_case.strip()) <= 80):
            return dict(
                permitted=False,
                reason="Scoped necessity exception case_id is invalid",
                exception=None,
            )
        cleaned["case_id"] = raw_case.strip()

    raw_doc = exception.get("doc_id")
    if doc_id is not None:
        if not isinstance(raw_doc, str) or raw_doc.strip() != doc_id:
            return dict(
                permitted=False,
                reason="Scoped necessity exception does not match this document",
                exception=None,
            )
        cleaned["doc_id"] = raw_doc.strip()
    elif raw_doc is not None:
        if not isinstance(raw_doc, str) or not (1 <= len(raw_doc.strip()) <= 80):
            return dict(
                permitted=False,
                reason="Scoped necessity exception doc_id is invalid",
                exception=None,
            )
        cleaned["doc_id"] = raw_doc.strip()

    raw_exp = exception.get("expires_at")
    if raw_exp is not None and raw_exp != "":
        if not isinstance(raw_exp, str) or len(raw_exp.strip()) < 10 or len(raw_exp.strip()) > 40:
            return dict(
                permitted=False,
                reason="Scoped necessity exception expires_at must be an ISO date",
                exception=None,
            )
        try:
            exp_date = date.fromisoformat(raw_exp.strip()[:10])
            if isinstance(as_of, datetime):
                ref_date = as_of.date()
            elif isinstance(as_of, date):
                ref_date = as_of
            elif isinstance(as_of, str) and as_of.strip():
                ref_date = date.fromisoformat(as_of.strip()[:10])
            else:
                ref_date = datetime.now(UTC).date()
        except ValueError:
            return dict(
                permitted=False,
                reason="Scoped necessity exception expires_at must be an ISO date",
                exception=None,
            )
        if exp_date < ref_date:
            return dict(
                permitted=False,
                reason="Scoped necessity exception has expired",
                exception=None,
            )
        cleaned["expires_at"] = raw_exp.strip()

    return dict(
        permitted=True,
        reason="Scoped necessity exception recorded; human approval is not verified by this check",
        exception=cleaned,
    )


def model_dispatch(
    class_id: str,
    env: Any,
    derivative: str | None = None,
    *,
    necessity_exception: Any = None,
    task: str = "read_document",
    case_id: str | None = None,
    doc_id: str | None = None,
    as_of: str | date | datetime | None = None,
) -> dict[str, Any]:
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
    if c.needs_derivative and derivative != APPROVED_DERIVATIVE:
        if derivative == CONSTRUCTED_DERIVATIVE:
            return dict(
                permitted=False,
                reason=(
                    "Synthetic derivative marker is not valid for actual processing; "
                    "use a reviewed, redacted derivative"
                ),
                manual_path=MANUAL_PATH,
            )
        if necessity_exception is not None:
            exc = validate_necessity_exception(
                necessity_exception,
                task=task,
                case_id=case_id,
                doc_id=doc_id,
                actual=True,
                as_of=as_of,
            )
            if exc["permitted"]:
                return dict(
                    permitted=True,
                    reason=exc["reason"],
                    manual_path=MANUAL_PATH,
                )
            return dict(permitted=False, reason=exc["reason"], manual_path=MANUAL_PATH)
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


def dispatch_hold(
    class_id: str,
    env: Any,
    derivative: str | None = None,
    *,
    necessity_exception: Any = None,
    task: str = "read_document",
    case_id: str | None = None,
    doc_id: str | None = None,
    as_of: str | date | datetime | None = None,
) -> str | None:
    """Reason a model call must not happen, or None. Unset or "constructed" means constructed only.

    Any other value is treated as actual processing, so a typo fails closed.
    """
    if not actual_mode(env):
        return None
    d = model_dispatch(
        class_id,
        env,
        derivative,
        necessity_exception=necessity_exception,
        task=task,
        case_id=case_id,
        doc_id=doc_id,
        as_of=as_of,
    )
    if d["permitted"]:
        return None
    return f"{d['reason']}. {d['manual_path']}"


def document_model_hold(
    doc: Mapping[str, Any] | None = None,
    env: Any = None,
    *,
    case_id: str | None = None,
    doc_id: str | None = None,
    derivative: str | None = None,
    necessity_exception: Any = None,
    resident_consent: str | None = None,
    as_of: str | date | datetime | None = None,
) -> str | None:
    """Reason document AI processing must not run, or None when permitted."""
    mapping = os.environ if env is None else env
    if resident_consent is not None:
        if str(resident_consent).strip().lower() not in ("given", "granted"):
            return f"Resident AI data-use consent is not granted. {MANUAL_PATH}"
    doc_map = doc if isinstance(doc, Mapping) else {}
    resolved_doc_id = (
        doc_id if doc_id is not None else (str(doc_map["id"]) if doc_map.get("id") else None)
    )
    has_explicit_derivative = (
        derivative is not None or "ai_derivative" in doc_map or "derivative" in doc_map
    )
    raw_deriv = (
        derivative
        if derivative is not None
        else (
            doc_map.get("ai_derivative")
            if "ai_derivative" in doc_map
            else doc_map.get("derivative")
        )
    )
    deriv = str(raw_deriv).strip() if isinstance(raw_deriv, str) and raw_deriv.strip() else None
    exc_obj = (
        necessity_exception
        if necessity_exception is not None
        else doc_map.get("necessity_exception")
    )
    requires_deriv = bool(doc_map.get("requires_derivative"))
    is_uploaded_doc = isinstance(doc, Mapping) and doc.get("generated") is False
    is_actual = actual_mode(mapping)
    if is_actual:
        return dispatch_hold(
            "raw_document",
            mapping,
            deriv,
            necessity_exception=exc_obj,
            task="read_document",
            case_id=case_id,
            doc_id=resolved_doc_id,
            as_of=as_of,
        )
    if is_uploaded_doc or has_explicit_derivative or requires_deriv or exc_obj is not None:
        if deriv in {APPROVED_DERIVATIVE, CONSTRUCTED_DERIVATIVE}:
            return None
        if exc_obj is not None:
            exc = validate_necessity_exception(
                exc_obj,
                task="read_document",
                case_id=case_id,
                doc_id=resolved_doc_id,
                actual=False,
                as_of=as_of,
            )
            if exc["permitted"]:
                return None
            return f"{exc['reason']}. {MANUAL_PATH}"
        return (
            "Intact material is not sent; use a reviewed, redacted derivative or "
            f"a scoped necessity exception. {MANUAL_PATH}"
        )
    return None


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
        late = (
            datetime.fromisoformat(answered).date() > due.date()
            if answered
            else now.date() > due.date()
        )
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
