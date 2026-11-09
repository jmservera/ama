"""Staff-mediated synthetic field-evidence intake (#132).

Existing authenticated staff key a worker's confirmed notes into the existing
quality submission, record a distinct receipt acknowledgement and inspect the
independent-review handoff. Pure orchestration over job_pack.py and
submit_quality; there is no provider portal, permission, contract instruction,
resident consent or acceptance authority here.
"""

import os
import re
from copy import deepcopy
from typing import Any, NoReturn

from . import job_pack, projection, quality, resident_decisions, workflows
from .quality import SUBMITTED

REF = re.compile(r"[A-Za-z0-9._-]{8,64}")
DIGEST = re.compile(r"[0-9a-f]{64}")
NOTE_LIMIT = 200
WORKER_LIMIT = 80
SOURCE = "Installer"
UNKNOWN = "Unknown - not configured"
UNKNOWN_ORDER = "Choose one of the work orders."


def _norm(value: Any) -> str:
    return str(quality._norm(value))  # type: ignore[no-untyped-call]


def _identity(user: Any) -> Any:
    return quality._identity(user)  # type: ignore[no-untyped-call]


def _now() -> str:
    return str(workflows._now())  # type: ignore[no-untyped-call]


class IntakeError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


def _fail(status: int, message: str) -> NoReturn:
    raise IntakeError(status, message)


def _staff_only(store: Any, user: Any) -> None:
    if projection.is_contractor(user):
        raise PermissionError("Job pack intake is for staff. Ask the contract manager.")


def _pack(store: Any, user: Any, wid: str) -> dict[str, Any]:
    try:
        pack: dict[str, Any] = store.work_order_job_pack(user, wid)
        return pack
    except ValueError as error:
        if str(error) == UNKNOWN_ORDER:
            raise IntakeError(404, UNKNOWN_ORDER) from None
        raise


def _find(store: Any, wid: str) -> tuple[dict[str, Any], dict[str, Any]]:
    w = store._work_order(wid)
    c = store.cases.get(w["case_id"])
    if not c:
        raise ValueError("Choose one of the work orders.")
    return w, c


def _records(c: dict[str, Any], wid: str) -> list[tuple[int, dict[str, Any]]]:
    return [
        (i, r)
        for i, r in enumerate(c.get("quality") or [])
        if isinstance(r.get("field_receipt"), dict) and r["field_receipt"].get("order") == wid
    ]


def _notes(value: Any, items: list[str]) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError("Enter the worker's notes for each check.")
    out = {}
    for label in items:
        note = value.get(label)
        if not isinstance(note, str) or not note.strip():
            raise ValueError(f"Each check needs the worker's note. Missing: {label}")
        if len(note.strip()) > NOTE_LIMIT:
            raise ValueError(
                f"Keep each note to {NOTE_LIMIT} characters so it is stored whole: {label}"
            )
        out[label] = note.strip()
    return out


def _worker(value: Any, store: Any, user: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Enter the worker's name.")
    name = value.strip()
    if len(name) > WORKER_LIMIT:
        raise ValueError(f"Keep the worker's name to {WORKER_LIMIT} characters.")
    staff = {_norm(user.get(k)) for k in ("name", "email", "code")} - {""}
    if _norm(name) in staff or "@" in name:
        raise ValueError(
            "The worker must be the person who did the work, not the staff member keying it in."
        )
    return name


def escalation_destination() -> dict[str, Any]:
    owner, role, contact = (
        os.environ.get(f"ZF_STAFF_INTAKE_ESCALATION_{k}", "").strip()
        for k in ("OWNER", "ROLE", "CONTACT")
    )
    return dict(
        owner=owner or UNKNOWN,
        role=role or UNKNOWN,
        contact=contact or UNKNOWN,
        configured=bool(owner and role and contact),
        contract_instruction=False,
        note=(
            "A concern raised here does not change the work order. "
            "Only the contract manager issues a new version."
        ),
    )


def _view_receipt(idx: int, rec: dict[str, Any], user: Any) -> dict[str, Any]:
    fr = rec["field_receipt"]
    ack = fr.get("acknowledgement")
    blocker = job_pack.review_blocker(_review_view(rec), _identity(user))
    me = {_norm(user.get(k)) for k in ("name", "email", "code")} - {""}
    if blocker is None and not rec.get("resident_binding"):
        blocker = (
            "This evidence was recorded without a resident scope binding, so it cannot be "
            "accepted. Ask the contract manager how to replace it."
        )
    if blocker is None and any(
        me & {_norm(p.get(k)) for k in ("name", "email", "code")}
        for p in rec.get("participants", [])
    ):
        blocker = (
            "Independent review must be by someone who did not do, key in, "
            "correct or acknowledge this work."
        )
    return dict(
        record=idx,
        capture_ref=fr["capture_ref"],
        measure=rec["measure"],
        checklist=rec["checklist"],
        checklist_version=rec["checklist_version"],
        evidence_version=rec.get("evidence_version"),
        pack_digest=fr["pack_digest"],
        design_version=fr["design_version"],
        original_notes=deepcopy(fr["original_notes"]),
        corrections=deepcopy(fr.get("corrections", [])),
        confirmed_by=fr["confirmed_by"],
        recorded_by=rec["recorded_by"],
        captured_at=fr["captured_at"],
        recorded_at=rec["recorded_at"],
        mode=fr["mode"],
        quality_state=rec["state"],
        status=fr["status"],
        accepted=rec["state"] in ("Accepted", "Handed over"),
        acknowledgement=(dict(by=ack["by"], at=ack["at"]) if ack else None),
        review=dict(
            state=job_pack.NOT_REVIEWED if rec["state"] == SUBMITTED else rec["state"],
            independent_required=True,
            you_may_review=blocker is None,
            blocker=blocker,
            history=[
                dict(at=h.get("at"), by=h.get("by"), to=h.get("to_state"), note=h.get("note"))
                for h in rec.get("history", [])
            ],
        ),
    )


def _review_view(rec: dict[str, Any]) -> dict[str, Any]:
    fr = rec["field_receipt"]
    out = dict(fr)
    out["recorded_by"] = dict(name=rec.get("recorded_by"), code=rec.get("recorded_by_code"))
    return out


def view(store: Any, user: Any, wid: str) -> dict[str, Any]:
    _staff_only(store, user)
    with store.lock:
        pack = _pack(store, user, wid)
        _, c = _find(store, wid)
        return dict(
            pack=pack,
            receipts=[_view_receipt(i, r, user) for i, r in _records(c, wid)],
            recovery=[job_pack.visit_recovery(e) for e in job_pack.NO_SHOW_EVENTS],
            escalation=escalation_destination(),
            boundaries=dict(
                contract_instruction=False,
                acceptance=(
                    "Acceptance needs independent review by a named quality role. "
                    "This screen never accepts work."
                ),
                consent="This does not record or replace resident consent.",
            ),
        )


def _replay(
    store: Any, user: Any, c: dict[str, Any], wid: str, ref: str, body: dict[str, Any]
) -> dict[str, Any] | None:
    """A retry of stored evidence is matched on the stored receipt, not on today's pack."""
    for idx, rec in _records(c, wid):
        fr = rec["field_receipt"]
        if fr["capture_ref"] != ref:
            continue
        if body.get("confirmed") is not True:
            raise ValueError("The worker must confirm these notes are their own.")
        notes = _notes(body.get("notes"), list(fr["original_notes"]))
        worker = _worker(body.get("confirmed_by"), store, user)
        if (
            body.get("measure") != rec["measure"]
            or notes != fr["original_notes"]
            or _norm(worker) != _norm(fr["confirmed_by"])
        ):
            _fail(409, "That capture reference was already used for different evidence.")
        return dict(outcome="duplicate", receipt=_view_receipt(idx, rec, user))
    return None


def _binding(c: dict[str, Any], w: dict[str, Any], measure: str) -> int:
    """The work order's bound resident scope revision, valid only while it is still current."""
    bound = {
        b.get("measure"): b.get("context_revision")
        for b in w["versions"][-1].get("resident_bindings") or []
        if isinstance(b, dict)
    }
    context: dict[str, Any] | None = resident_decisions.current_context(  # type: ignore[no-untyped-call]
        c, measure
    )
    revision = bound.get(measure)
    if context is None or type(revision) is not int or revision != context["revision"]:
        _fail(
            409,
            "The resident scope for this measure is not confirmed or has changed. "
            "Ask the contract manager to reissue the work order with the current scope.",
        )
    return revision


def capture(store: Any, user: Any, wid: str, body: dict[str, Any]) -> dict[str, Any]:
    _staff_only(store, user)
    if not isinstance(body, dict):
        raise ValueError("Send the capture as a JSON object.")
    with store.lock:
        pack = _pack(store, user, wid)
        w, c = _find(store, wid)
        ref = body.get("capture_ref")
        if not isinstance(ref, str) or not REF.fullmatch(ref):
            raise ValueError(
                "The capture reference is 8 to 64 letters, digits, dots, dashes or underscores."
            )
        replay = _replay(store, user, c, wid, ref, body)
        if replay:
            return replay
        measure = body.get("measure")
        if not isinstance(measure, str) or measure not in pack["checklists"]:
            raise ValueError("Choose one of the measures in this job pack.")
        notes = _notes(body.get("notes"), pack["checklists"][measure]["items"])
        worker = _worker(body.get("confirmed_by"), store, user)
        mode = body.get("mode", "online")
        captured_at = body.get("captured_at") if mode == "offline" else None
        captured_at = (
            captured_at if isinstance(captured_at, str) and captured_at.strip() else _now()
        )
        receipt = job_pack.worker_receipt(
            pack,
            measure,
            notes,
            worker,
            body.get("confirmed") is True,
            ref,
            captured_at,
            _identity(user),
            mode,
        )
        digest = body.get("pack_digest")
        if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            raise ValueError(
                "Send the job pack reference the worker's notes were written against. "
                "Reload the job pack if you do not have it."
            )
        if digest != pack["pack_digest"]:
            _fail(
                409,
                "The job pack changed after this was captured. "
                "Reload it and have the worker re-confirm.",
            )
        if not pack["ready"]:
            raise ValueError(pack["not_ready_reason"])
        revision = _binding(c, w, measure)
        store.submit_quality(
            user,
            w["case_id"],
            measure,
            worker,
            SOURCE,
            notes,
            context_revision=revision,
            field_receipt=dict(receipt, pack_digest=digest),
        )
        return dict(outcome="recorded", receipt=_view_one(c, wid, ref, user))


def _view_one(c: dict[str, Any], wid: str, ref: str, user: Any) -> dict[str, Any]:
    for i, r in _records(c, wid):
        if r["field_receipt"]["capture_ref"] == ref:
            return _view_receipt(i, r, user)
    raise ValueError("Choose one of this order's receipts.")


def _locate(c: dict[str, Any], wid: str, record: Any) -> tuple[int, dict[str, Any]]:
    try:
        idx = int(record)
        rec = c["quality"][idx]
    except (TypeError, ValueError, IndexError, KeyError):
        raise ValueError("Choose one of this order's receipts.") from None
    if (
        idx < 0
        or not isinstance(rec.get("field_receipt"), dict)
        or rec["field_receipt"].get("order") != wid
    ):
        raise ValueError("Choose one of this order's receipts.")
    return idx, rec


def correct(store: Any, user: Any, wid: str, body: dict[str, Any]) -> dict[str, Any]:
    _staff_only(store, user)
    if not isinstance(body, dict):
        raise ValueError("Send the correction as a JSON object.")
    _pack(store, user, wid)
    w, _ = _find(store, wid)
    with store._quality_operation(user, w["case_id"]) as (c, actor):
        idx, rec = _locate(c, wid, body.get("record"))
        fr = rec["field_receipt"]
        if rec["state"] != SUBMITTED or fr.get("acknowledgement"):
            _fail(
                409,
                "This receipt is acknowledged or already reviewed. Raise a new capture instead.",
            )
        if body.get("confirmed") is not True:
            raise ValueError("The worker must confirm this correction is their own.")
        label = body.get("label")
        if not isinstance(label, str) or label not in fr["original_notes"]:
            raise ValueError("Choose one of the checks on this checklist.")
        note = _notes({label: body.get("note")}, [label])[label]
        worker = _worker(body.get("confirmed_by"), store, actor)
        if _norm(worker) != _norm(fr["confirmed_by"]):
            raise ValueError(
                "A correction is confirmed by the same worker who gave the original notes."
            )
        fr.setdefault("corrections", []).append(
            dict(
                label=label, note=note, confirmed_by=worker, recorded_by=_identity(actor), at=_now()
            )
        )
        for item in rec["items"]:
            if item.get("label") == label:
                item["evidence"] = note
        rec.setdefault("participants", []).append(_identity(actor))
        store._quality_event(
            c, rec, actor, SUBMITTED, SUBMITTED, f"Worker correction recorded for: {label}"
        )
        store.audit(
            actor["email"],
            "field_receipt_corrected",
            w["case_id"],
            f"{wid} {rec['measure']} {label}",
        )
        store.save()
        return dict(outcome="corrected", receipt=_view_receipt(idx, rec, actor))


def acknowledge(store: Any, user: Any, wid: str, body: dict[str, Any]) -> dict[str, Any]:
    _staff_only(store, user)
    if not isinstance(body, dict):
        raise ValueError("Send the acknowledgement as a JSON object.")
    _pack(store, user, wid)
    w, _ = _find(store, wid)
    with store._quality_operation(user, w["case_id"]) as (c, actor):
        idx, rec = _locate(c, wid, body.get("record"))
        fr = rec["field_receipt"]
        if fr.get("acknowledgement"):
            _fail(409, "This receipt is already acknowledged.")
        if rec["state"] != SUBMITTED:
            _fail(409, "This receipt has moved on and can no longer be acknowledged.")
        me = {_norm(actor.get(k)) for k in ("name", "email", "code")} - {""}
        if _norm(fr["confirmed_by"]) in me:
            raise PermissionError("The worker cannot acknowledge their own evidence.")
        at = _now()
        merged = job_pack.acknowledge_receipt(fr, _identity(actor), at)
        fr["acknowledgement"] = merged["acknowledgement"]
        fr["status"] = merged["status"]
        rec.setdefault("participants", []).append(_identity(actor))
        store._quality_event(
            c, rec, actor, SUBMITTED, SUBMITTED, "Receipt acknowledged; not accepted"
        )
        store.audit(
            actor["email"], "field_receipt_acknowledged", w["case_id"], f"{wid} {rec['measure']}"
        )
        store.save()
        return dict(outcome="acknowledged", receipt=_view_receipt(idx, rec, actor))


ACTIONS = {"field-capture": capture, "field-correct": correct, "field-acknowledge": acknowledge}


def handle(
    store: Any, user: Any, method: str, parts: list[str], body: Any = None
) -> tuple[int, dict[str, Any]]:
    """parts is the path after /api/workorders/, e.g. [id, 'field-intake']."""
    try:
        if len(parts) != 2:
            return 404, dict(error="Choose one of the work orders.")
        wid, action = parts
        if method == "GET" and action == "field-intake":
            return 200, view(store, user, wid)
        if method == "POST" and action in ACTIONS:
            return 200, ACTIONS[action](store, user, wid, body)
        return 404, dict(error="Choose one of the available actions.")
    except IntakeError as error:
        return error.status, dict(error=str(error))
    except PermissionError as error:
        return 403, dict(error=str(error))
    except ValueError as error:
        return 400, dict(error=str(error))
