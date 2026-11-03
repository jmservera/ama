"""Staff-mediated contractor job pack and field evidence receipts (#132, slice 1).

Pure, read-only domain rules. Nothing here writes a case, work order or quality
record, grants contractor access, or accepts work. A signed-in staff member
carries the pack to a worker and keys the worker's confirmed evidence in through
the existing quality submission. The PRD has no provider portal, so this is a
staff-mediated design proposal until the owner decides otherwise.
"""

import hashlib
import json
from collections.abc import Iterable, Mapping
from typing import Any

from .quality import checklist_for
from .workflows import MANAGER_ROLES

PACK_FIELDS = ("package", "address", "postcode", "state", "scope", "scope_version")
ACCESS_NOTICE = "Notice needed before the visit"
ACCESS_NONE = "No special notice recorded"
DESIGN_UNKNOWN = "Unknown - design version not recorded"

SUBMITTED = "Submitted by worker - awaiting independent review"
NOT_REVIEWED = "Not reviewed"
ACKNOWLEDGED = "Receipt acknowledged - not accepted"

ESCALATION_KINDS = ("variation", "safety", "access", "scope question", "other")
ESCALATION_OWNER_ROLES = MANAGER_ROLES + ("Building Safety Liaison",)
NO_SHOW_EVENTS = {
    "provider no-show": ("Rebooking needed", "The provider did not attend"),
    "provider cancelled": ("Rebooking needed", "The provider cancelled"),
    "resident cancelled": ("Rebooking needed", "The resident cancelled this visit"),
    "no access": ("No access", "The worker could not get in"),
}


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Enter {label}.")
    return value.strip()


def build_job_pack(order: Mapping[str, Any], case: Mapping[str, Any]) -> dict[str, Any]:
    """Project a work-order view and its case into the fields a worker needs.

    Closed allow-list: scope, design version, a notice flag and one named contact.
    Resident notes, vulnerability reasons and health detail are never read.
    """
    measures = [m.strip() for m in str(order.get("measures") or "").split(",") if m.strip()]
    known = [m for m in measures if not m.startswith("Unknown")]
    pack: dict[str, Any] = {k: order.get(k) for k in PACK_FIELDS}
    pack["order"] = order.get("id")
    pack["order_version"] = order.get("version")
    pack["design_version"] = (case.get("technical") or {}).get("design_version") or DESIGN_UNKNOWN
    pack["access"] = ACCESS_NOTICE if order.get("needs_notice") else ACCESS_NONE
    pack["named_contact"] = order.get("named_contact") or "Unknown - ask the contract manager"
    pack["measures"] = known
    pack["checklists"] = {
        m: {k: checklist_for(m)[k] for k in ("name", "version", "items")} for m in known
    }
    pack["ready"] = (
        bool(known)
        and pack["design_version"] != DESIGN_UNKNOWN
        and order.get("state") == "Appointed"
    )
    pack["not_ready_reason"] = (
        None
        if pack["ready"]
        else ("Scope, design version or a confirmed appointment is missing; do not start work.")
    )
    pack["pack_digest"] = _digest({k: pack[k] for k in sorted(pack) if k != "pack_digest"})
    return pack


def worker_receipt(
    pack: Mapping[str, Any],
    measure: str,
    notes: Mapping[str, str],
    confirmed_by: str,
    confirmed: bool,
    capture_ref: str,
    captured_at: str,
    recorded_by: Mapping[str, str],
    mode: str = "online",
) -> dict[str, Any]:
    """Record the worker's own words against the versioned checklist, never as acceptance."""
    if confirmed is not True:
        raise ValueError("The worker must confirm these notes are their own.")
    if mode not in ("online", "offline"):
        raise ValueError("Capture mode is online or offline.")
    if measure not in pack.get("checklists", {}):
        raise ValueError("Choose one of the measures in this job pack.")
    checklist = pack["checklists"][measure]
    missing = [
        label
        for label in checklist["items"]
        if not isinstance(notes.get(label), str) or not notes[label].strip()
    ]
    if missing:
        raise ValueError("Each check needs the worker's note. Missing: " + "; ".join(missing))
    original = {label: notes[label] for label in checklist["items"]}
    return dict(
        capture_ref=_text(capture_ref, "a capture reference"),
        order=pack["order"],
        measure=measure,
        checklist=checklist["name"],
        checklist_version=checklist["version"],
        pack_digest=pack["pack_digest"],
        design_version=pack["design_version"],
        original_notes=original,
        notes_digest=_digest(original),
        confirmed_by=_text(confirmed_by, "the worker's name"),
        captured_at=_text(captured_at, "when the evidence was captured"),
        recorded_by=dict(recorded_by),
        mode=mode,
        status=SUBMITTED,
        review_state=NOT_REVIEWED,
        accepted=False,
        acknowledgement=None,
    )


def acknowledge_receipt(
    receipt: Mapping[str, Any], staff: Mapping[str, str], at: str
) -> dict[str, Any]:
    """Confirm receipt only. This never changes review state or accepts work."""
    out = dict(receipt)
    out["acknowledgement"] = dict(
        by=_text(staff.get("name"), "the staff name"),
        email=staff.get("email"),
        code=staff.get("code"),
        at=_text(at, "a time"),
    )
    out["status"] = ACKNOWLEDGED
    return out


def review_blocker(receipt: Mapping[str, Any], reviewer: Mapping[str, str]) -> str | None:
    """Return why this person may not independently review the receipt, or None.

    Independence holds against the worker, the staff member who keyed the notes
    in and whoever acknowledged them; matching is by name, email or code.
    """

    def keys(person: Mapping[str, Any] | None) -> set[str]:
        return {
            str(person[k]).strip().lower()
            for k in ("name", "by", "email", "code")
            if person and person.get(k)
        }

    involved = [
        dict(name=receipt.get("confirmed_by")),
        receipt.get("recorded_by"),
        receipt.get("acknowledgement"),
    ]
    mine = keys(reviewer)
    if not mine:
        return "Review needs a named reviewer."
    if any(mine & keys(p) for p in involved):
        return (
            "Independent review must be by someone who did not do, key in or acknowledge this work."
        )
    return None


def merge_offline(
    held: Iterable[Mapping[str, Any]],
    incoming: Iterable[Mapping[str, Any]],
    current_pack_digest: str,
) -> dict[str, list[dict[str, Any]]]:
    """Reconcile receipts captured offline. Original notes and capture times are kept."""
    seen = {r["capture_ref"] for r in held}
    out: dict[str, list[dict[str, Any]]] = dict(new=[], duplicate=[], held_for_review=[])
    for receipt in incoming:
        item = dict(receipt)
        if item["capture_ref"] in seen:
            out["duplicate"].append(item)
        elif item["pack_digest"] != current_pack_digest:
            item["hold_reason"] = (
                "Scope, design or order changed after capture; the worker re-confirms."
            )
            out["held_for_review"].append(item)
        else:
            seen.add(item["capture_ref"])
            out["new"].append(item)
    return out


def visit_recovery(event: str) -> dict[str, Any]:
    """Map a missed or cancelled visit to a rebooking outcome. Never a resident refusal."""
    if event not in NO_SHOW_EVENTS:
        raise ValueError("Choose one of: " + ", ".join(NO_SHOW_EVENTS) + ".")
    outcome, cause = NO_SHOW_EVENTS[event]
    return dict(
        event=event,
        outcome=outcome,
        cause=cause,
        resident_refusal=False,
        resident_effect="No change to the resident's choices, consent or priority.",
        next_step="Contract manager offers a new appointment; the resident confirms it.",
        owner_role=MANAGER_ROLES[0],
    )


def escalation(
    kind: str, summary: str, raised_by: str, order: str, owner_name: str, owner_role: str
) -> dict[str, Any]:
    """Route a variation or concern to a named owner. It is never a contract instruction."""
    if kind not in ESCALATION_KINDS:
        raise ValueError("Choose one of: " + ", ".join(ESCALATION_KINDS) + ".")
    if owner_role not in ESCALATION_OWNER_ROLES:
        raise ValueError("Choose a contract manager or the building safety liaison as owner.")
    return dict(
        kind=kind,
        summary=_text(summary, "what needs deciding")[:500],
        raised_by=_text(raised_by, "who is raising this"),
        order=_text(order, "the work order"),
        owner=dict(name=_text(owner_name, "the named owner"), role=owner_role),
        status="Raised - awaiting owner",
        contract_instruction=False,
        note="The work order does not change until the contract manager issues a new version.",
    )
