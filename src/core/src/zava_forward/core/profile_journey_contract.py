"""Profile journey contract validator for the eleven perspectives (Refs #134, slice 5).

A walkthrough record states, for each of the five contract elements, the linked record ids it
inspected, the textual state meaning shown, whether it was keyboard operable and the status
announcement text. `validate` returns blockers only and never marks a perspective as accepted:
constructed-fixture records are not user validation or owner approval. `gaps` lists, per
perspective, the elements the coverage register still records as unmet or not observed by the
keyboard probe. Both read only what they are given.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from zava_forward.core import job_pack as jp
from zava_forward.core import journey_trace as jt
from zava_forward.core import perspective_walkthroughs as pw
from zava_forward.core import projection, resident_decisions
from zava_forward.core import resident_preview as rp

ELEMENTS = pw.ELEMENTS
SIX_STAFF_PROFILES: tuple[str, ...] = (
    "Retrofit Programme Manager",
    "Retrofit Coordinator",
    "Resident Liaison Officer",
    "Building Safety Liaison",
    "Quality Inspector",
    "Grants and Evidence Officer",
)
REASON_STAFF_PROFILES: tuple[str, ...] = projection.DEFAULT_REASON_ROLES
REDACTED_STAFF_PROFILES: tuple[str, ...] = (
    "Retrofit Coordinator",
    "Quality Inspector",
    "Grants and Evidence Officer",
)
BANNED_INTERNAL_TERMS: tuple[str, ...] = (
    "gate",
    "gates",
    "hold",
    "holds",
    "provenance",
    "trace",
    "traces",
    "snapshot",
    "snapshots",
    "envelope",
    "envelopes",
)
BOUNDARIES: dict[str, str] = {
    "human_approval": "not-established",
    "resident_approval": "not-established",
    "accessibility_walkthrough": "not-established",
}
NOTICE = (
    "Constructed-fixture contract check, not user validation. A clean result means the record "
    "is complete in shape; it does not mean a perspective journey is accepted."
)
SAME_HOME_NOTICE = (
    "Constructed-fixture connected same-home check across staff profiles, contractor views and "
    "the synthetic resident preview: not user validation. Passing checks confirm code-level "
    "contract invariants only; live perspective walkthroughs (#155) and assistive-technology "
    "sign-off (#151) remain open."
)
# Text that alone would not tell a reader the state (colour or icon only labels).
NON_TEXT = frozenset({"red", "green", "amber", "yellow", "ok", "x", "-", "?"})
JARGON_RE = re.compile(
    r"\b(" + "|".join(re.escape(term) for term in BANNED_INTERNAL_TERMS) + r")\b",
    re.IGNORECASE,
)
CONTRACTOR_FORBIDDEN_KEYS: tuple[str, ...] = (
    "resident",
    "notes",
    "contacts",
    "hazards",
    "safety_clocks",
    "funding",
    "finance",
    "grants",
    "documents",
)


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def validate(walkthrough: Mapping[str, Any]) -> dict[str, Any]:
    """Return blockers for one perspective walkthrough record."""
    pid = _text(walkthrough.get("perspective")) or "?"
    steps = walkthrough.get("steps")
    steps = steps if isinstance(steps, Mapping) else {}
    blockers: list[str] = []
    for el in ELEMENTS:
        step = steps.get(el)
        if not isinstance(step, Mapping):
            blockers.append(f"{pid}.{el}:missing")
            continue
        ids = step.get("record_ids")
        if not isinstance(ids, list) or not [i for i in ids if _text(i)]:
            blockers.append(f"{pid}.{el}:no_linked_records")
        state = _text(step.get("state_text"))
        if not state or state.lower() in NON_TEXT:
            blockers.append(f"{pid}.{el}:state_not_textual")
        if step.get("keyboard_operable") is not True:
            blockers.append(f"{pid}.{el}:not_keyboard_operable")
        if not _text(step.get("announcement")):
            blockers.append(f"{pid}.{el}:no_status_announcement")
    handoff = steps.get("handoff")
    if isinstance(handoff, Mapping) and not _text(handoff.get("owner")):
        blockers.append(f"{pid}.handoff:no_accountable_owner")
    return dict(
        status="blocked" if blockers else "complete_in_shape",
        blockers=blockers,
        accepted=False,
        notice=NOTICE,
    )


def gaps(root: Path) -> dict[str, dict[str, list[str]]]:
    """Per perspective: elements unmet in the register and elements the probe did not observe."""
    reg = pw.check(root)
    if reg["blockers"]:
        raise ValueError(f"walkthrough register blocked: {reg['blockers']}")
    out: dict[str, dict[str, list[str]]] = {}
    for pid, cells in pw.register().items():
        out[pid] = dict(
            unmet=[e for e in ELEMENTS if cells[e]["status"] == "unmet"],
            not_probed=[e for e in ELEMENTS if e not in pw.PROBE_OBSERVED.get(pid, ())],
        )
    return out


_rd: Any = resident_decisions


def _norm_measures(raw: Any) -> list[str]:
    items = _rd.case_measures({"measures": raw})
    return [m.strip() for m in items if isinstance(m, str) and m.strip()]


def _concrete_order_measures(raw: Any) -> list[str]:
    if isinstance(raw, list):
        parts = [_text(item) for item in raw]
    else:
        parts = [part.strip() for part in _text(raw).split(",")]
    return [p for p in parts if p and not p.startswith("Unknown")]


def _contains_secret(payload: Any, secret: str) -> bool:
    needle = secret.lower()
    if isinstance(payload, str):
        return needle in payload.lower()
    if isinstance(payload, Mapping):
        return any(
            _contains_secret(k, secret) or _contains_secret(v, secret) for k, v in payload.items()
        )
    if isinstance(payload, Sequence) and not isinstance(payload, (bytes, bytearray)):
        return any(_contains_secret(item, secret) for item in payload)
    return False


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _seq(value: Any) -> Sequence[Any]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return value
    return ()


def _staff_map(bundle_or_staff: Mapping[str, Any]) -> Mapping[str, Any]:
    if "staff" in bundle_or_staff and isinstance(bundle_or_staff.get("staff"), Mapping):
        return _mapping(bundle_or_staff.get("staff"))
    if "staff_views" in bundle_or_staff and isinstance(bundle_or_staff.get("staff_views"), Mapping):
        return _mapping(bundle_or_staff.get("staff_views"))
    return bundle_or_staff


def _is_bundle(value: Mapping[str, Any]) -> bool:
    return any(
        key in value
        for key in ("staff", "staff_views", "contractor_detail", "resident_view", "case_id")
    )


def _canonical_staff_view(staff: Mapping[str, Any]) -> Mapping[str, Any] | None:
    reasons = set(projection.reason_roles())
    for role in SIX_STAFF_PROFILES:
        view = staff.get(role)
        if role in reasons and isinstance(view, Mapping):
            return view
    for role in SIX_STAFF_PROFILES:
        view = staff.get(role)
        if isinstance(view, Mapping):
            return view
    return None


def check_shared_facts(
    case_id_or_bundle: str | Mapping[str, Any],
    staff_views: Mapping[str, Any] | None = None,
    *,
    resident_view: Mapping[str, Any] | None = None,
    contractor_view: Mapping[str, Any] | None = None,
    contractor_orders: Sequence[Mapping[str, Any]] = (),
    job_pack: Mapping[str, Any] | None = None,
    sibling_ids: Sequence[str] = (),
    sibling_markers: Sequence[str] = (),
) -> list[str]:
    """Verify shared home facts agree across the six staff profiles, contractor and resident."""
    if isinstance(case_id_or_bundle, Mapping):
        bundle = case_id_or_bundle
        expected_id = _text(bundle.get("case_id"))
        staff = _staff_map(bundle)
        rview = resident_view if resident_view is not None else bundle.get("resident_view")
        cdetail = (
            contractor_view if contractor_view is not None else bundle.get("contractor_detail")
        )
        orders: Sequence[Any] = (
            contractor_orders if contractor_orders else _seq(bundle.get("work_orders"))
        )
        pack = job_pack if job_pack is not None else bundle.get("job_pack")
    else:
        expected_id = _text(case_id_or_bundle)
        staff = _mapping(staff_views)
        rview = resident_view
        cdetail = contractor_view
        orders = contractor_orders
        pack = job_pack

    blockers: list[str] = []
    present: list[tuple[str, Mapping[str, Any]]] = []
    for role in SIX_STAFF_PROFILES:
        view = staff.get(role)
        if not isinstance(view, Mapping):
            blockers.append(f"same_home.shared_facts:missing_staff_profile:{role}")
        else:
            present.append((role, view))
    if not present:
        return blockers

    _, first = present[0]
    first_home = _mapping(first.get("home"))
    case_id = expected_id or _text(first.get("id"))
    address = _text(first_home.get("address"))
    postcode = _text(first_home.get("postcode"))
    stage = _text(first.get("stage"))
    closed = bool(first.get("closed"))
    measures = _norm_measures(first.get("measures"))
    if not case_id or not address or not postcode or not stage or not measures:
        blockers.append("same_home.shared_facts:incomplete_baseline_facts")
    if expected_id and _text(first.get("id")) != expected_id:
        blockers.append(f"same_home.shared_facts:staff_mismatch:{present[0][0]}:id")

    for role, view in present[1:]:
        home = _mapping(view.get("home"))
        if _text(view.get("id")) != case_id:
            blockers.append(f"same_home.shared_facts:staff_mismatch:{role}:id")
        if _text(home.get("address")) != address:
            blockers.append(f"same_home.shared_facts:staff_mismatch:{role}:address")
        if _text(home.get("postcode")) != postcode:
            blockers.append(f"same_home.shared_facts:staff_mismatch:{role}:postcode")
        if _text(view.get("stage")) != stage:
            blockers.append(f"same_home.shared_facts:staff_mismatch:{role}:stage")
        if bool(view.get("closed")) != closed:
            blockers.append(f"same_home.shared_facts:staff_mismatch:{role}:closed")
        if _norm_measures(view.get("measures")) != measures:
            blockers.append(f"same_home.shared_facts:staff_mismatch:{role}:measures")

    if isinstance(cdetail, Mapping):
        chome = _mapping(cdetail.get("home"))
        expected_status = "Completed" if closed else stage
        if _text(cdetail.get("id")) != case_id:
            blockers.append("same_home.shared_facts:contractor_mismatch:id")
        if _text(chome.get("address")) != address:
            blockers.append("same_home.shared_facts:contractor_mismatch:address")
        if _text(chome.get("postcode")) != postcode:
            blockers.append("same_home.shared_facts:contractor_mismatch:postcode")
        if _text(cdetail.get("stage")) != stage:
            blockers.append("same_home.shared_facts:contractor_mismatch:stage")
        if _text(cdetail.get("status")) != expected_status:
            blockers.append("same_home.shared_facts:contractor_mismatch:status")
        if _norm_measures(cdetail.get("measures")) != measures:
            blockers.append("same_home.shared_facts:contractor_mismatch:measures")

    for idx, order in enumerate(orders):
        if not isinstance(order, Mapping):
            blockers.append(f"same_home.shared_facts:work_order_invalid:{idx}")
            continue
        if _text(order.get("case_id")) != case_id:
            blockers.append(f"same_home.shared_facts:work_order_mismatch:{idx}:case_id")
        if _text(order.get("address")) != address:
            blockers.append(f"same_home.shared_facts:work_order_mismatch:{idx}:address")
        if _text(order.get("postcode")) != postcode:
            blockers.append(f"same_home.shared_facts:work_order_mismatch:{idx}:postcode")
        order_measures = _concrete_order_measures(order.get("measures"))
        if any(m not in measures for m in order_measures):
            blockers.append(f"same_home.shared_facts:work_order_mismatch:{idx}:measures")

    if isinstance(pack, Mapping):
        if _text(pack.get("address")) != address:
            blockers.append("same_home.shared_facts:job_pack_mismatch:address")
        if _text(pack.get("postcode")) != postcode:
            blockers.append("same_home.shared_facts:job_pack_mismatch:postcode")
        pack_measures = _concrete_order_measures(pack.get("measures"))
        if any(m not in measures for m in pack_measures):
            blockers.append("same_home.shared_facts:job_pack_mismatch:measures")

    if isinstance(rview, Mapping):
        if rview.get("read_only") is not True or _text(rview.get("banner")) != rp.BANNER:
            blockers.append("same_home.shared_facts:resident_preview_boundary_missing")
        if any(key in rview for key in ("id", "case_id", "stage")):
            blockers.append("same_home.shared_facts:resident_internal_field_exposed")
        if "home" in rview:
            rhome = _mapping(rview.get("home"))
            if _text(rhome.get("address")) != address or _text(rhome.get("postcode")) != postcode:
                blockers.append("same_home.shared_facts:resident_mismatch:home")
        if "measures" in rview:
            viewer_kind = _text(_mapping(rview.get("viewer")).get("kind"))
            rmeas = _norm_measures(rview.get("measures"))
            if viewer_kind == "representative":
                if not rmeas or any(m not in measures for m in rmeas):
                    blockers.append("same_home.shared_facts:resident_mismatch:measures")
            elif rmeas != measures:
                blockers.append("same_home.shared_facts:resident_mismatch:measures")
        exp_progress, exp_next = rp.STAGE_TEXT.get(stage, (rp.UNKNOWN_PROGRESS, rp.UNKNOWN_NEXT))
        if "progress" in rview:
            if _text(rview.get("progress")) != exp_progress:
                blockers.append("same_home.shared_facts:resident_mismatch:progress")
            if closed:
                if _text(rview.get("closed")) != "This case is recorded as closed.":
                    blockers.append("same_home.shared_facts:resident_mismatch:closed")
            elif "closed" in rview:
                blockers.append("same_home.shared_facts:resident_mismatch:closed")
        if "next_step" in rview and _text(rview.get("next_step")) != exp_next:
            blockers.append("same_home.shared_facts:resident_mismatch:next_step")

    forbidden_siblings = [_text(s) for s in (*sibling_ids, *sibling_markers) if _text(s)]
    if forbidden_siblings:
        surfaces: list[tuple[str, Any]] = [
            *(("staff:" + role, view) for role, view in present),
            ("contractor_detail", cdetail),
            ("work_orders", list(orders)),
            ("job_pack", pack),
            ("resident_view", rview),
        ]
        for label, surface in surfaces:
            if surface is None:
                continue
            for token in forbidden_siblings:
                if _contains_secret(surface, token):
                    blockers.append(f"same_home.shared_facts:sibling_leak:{label}:{token}")

    return blockers


def check_vulnerability_redaction(
    staff_views_or_bundle: Mapping[str, Any],
    contractor_views: Sequence[Mapping[str, Any]] = (),
    resident_view: Mapping[str, Any] | None = None,
    *,
    vulnerability_reason: str | None = None,
    private_markers: Sequence[str] = (),
    contractor_private_markers: Sequence[str] = (),
) -> list[str]:
    """Verify PR-002 vulnerability reason visibility across staff, contractor and resident views."""
    if _is_bundle(staff_views_or_bundle):
        bundle = staff_views_or_bundle
        staff = _staff_map(bundle)
        rview = resident_view if resident_view is not None else bundle.get("resident_view")
        cviews: list[Mapping[str, Any]] = list(contractor_views)
        if not cviews:
            for item in (
                bundle.get("contractor_summary"),
                bundle.get("contractor_detail"),
                *_seq(bundle.get("work_orders")),
                bundle.get("job_pack"),
            ):
                if isinstance(item, Mapping):
                    cviews.append(item)
    else:
        staff = staff_views_or_bundle
        rview = resident_view
        cviews = [item for item in contractor_views if isinstance(item, Mapping)]

    secret = _text(vulnerability_reason)
    markers = [_text(m) for m in private_markers if _text(m)]
    contractor_markers = [
        _text(m) for m in (*private_markers, *contractor_private_markers) if _text(m)
    ]
    if not secret or secret in ("None", "Unknown"):
        return ["same_home.redaction:missing_vulnerability_fixture"]
    reasons = set(projection.reason_roles())
    blockers: list[str] = []

    roles_to_check = list(SIX_STAFF_PROFILES)
    if "Programme Support Officer" in staff:
        roles_to_check.append("Programme Support Officer")

    for role in roles_to_check:
        view = staff.get(role)
        if not isinstance(view, Mapping):
            continue
        res = _mapping(view.get("resident"))
        shown = _text(res.get("adjustment"))
        if role in reasons:
            if shown != secret:
                blockers.append(f"same_home.redaction:reason_role_missing_adjustment:{role}")
        else:
            if shown != projection.REDACTED:
                blockers.append(f"same_home.redaction:non_reason_role_unredacted:{role}")
            if _contains_secret(view, secret):
                blockers.append(f"same_home.redaction:non_reason_role_leaked_secret:{role}")
            for marker in markers:
                if _contains_secret(view, marker):
                    blockers.append(f"same_home.redaction:non_reason_role_leaked_marker:{role}")

    for idx, cpayload in enumerate(cviews):
        for forbidden in CONTRACTOR_FORBIDDEN_KEYS:
            if forbidden in cpayload:
                blockers.append(f"same_home.redaction:contractor_forbidden_field:{idx}:{forbidden}")
        if _contains_secret(cpayload, projection.REDACTED):
            blockers.append(f"same_home.redaction:contractor_leaked_redacted_marker:{idx}")
        if _contains_secret(cpayload, secret):
            blockers.append(f"same_home.redaction:contractor_leaked_secret:{idx}")
        for marker in contractor_markers:
            if _contains_secret(cpayload, marker):
                blockers.append(f"same_home.redaction:contractor_leaked_marker:{idx}")
        contact = _text(cpayload.get("named_contact"))
        if "access" in cpayload:
            if (
                cpayload.get("access") != jp.ACCESS_NOTICE
                or not contact
                or contact.startswith("Unknown")
            ):
                blockers.append(f"same_home.redaction:job_pack_notice_or_contact_missing:{idx}")
        elif cpayload.get("needs_notice") is not True or not contact:
            blockers.append(f"same_home.redaction:contractor_notice_or_contact_missing:{idx}")

    if isinstance(rview, Mapping):
        for forbidden_text in (projection.REDACTED, "priority_support", "Safeguarding", secret):
            if _contains_secret(rview, forbidden_text):
                blockers.append("same_home.redaction:resident_preview_leaked_private_detail")
                break
        for marker in contractor_markers:
            if _contains_secret(rview, marker):
                blockers.append("same_home.redaction:resident_preview_leaked_marker")

    return blockers


def check_handover_dependencies(
    staff_views_or_bundle: Mapping[str, Any],
    *,
    contractor_view: Mapping[str, Any] | None = None,
    work_orders: Sequence[Mapping[str, Any]] = (),
    job_pack_receipt: Mapping[str, Any] | None = None,
    resident_view: Mapping[str, Any] | None = None,
    audit_trace: Mapping[str, Any] | None = None,
) -> list[str]:
    """Verify safety, resident decision, pending handoff and independent quality boundaries."""
    if _is_bundle(staff_views_or_bundle):
        bundle = staff_views_or_bundle
        staff = _staff_map(bundle)
        cdetail = (
            contractor_view if contractor_view is not None else bundle.get("contractor_detail")
        )
        orders: Sequence[Any] = work_orders if work_orders else _seq(bundle.get("work_orders"))
        receipt = (
            job_pack_receipt
            if job_pack_receipt is not None
            else (bundle.get("job_pack_receipt") or bundle.get("worker_receipt"))
        )
        rview = resident_view if resident_view is not None else bundle.get("resident_view")
        trace = audit_trace if audit_trace is not None else bundle.get("audit_trace")
    else:
        staff = staff_views_or_bundle
        cdetail = contractor_view
        orders = work_orders
        receipt = job_pack_receipt
        rview = resident_view
        trace = audit_trace

    canonical = _canonical_staff_view(staff)
    if canonical is None:
        return ["same_home.handover:missing_staff_views"]
    blockers: list[str] = []

    hazards = _seq(canonical.get("hazards"))
    active_hazards = [h for h in hazards if isinstance(h, Mapping) and not bool(h.get("released"))]
    stock_queries = _seq(canonical.get("stock_reconciliation"))
    unresolved_stock = [
        q
        for q in stock_queries
        if isinstance(q, Mapping) and _text(q.get("status")) not in ("Reconciled", "Withdrawn")
    ]
    work = _mapping(canonical.get("work"))
    gate = _seq(canonical.get("gate"))
    work_blockers = _seq(work.get("blockers"))

    if active_hazards and (bool(canonical.get("closed")) or bool(canonical.get("can_advance"))):
        if not list(gate) and not list(work_blockers):
            blockers.append("same_home.handover:unreleased_hazard_not_blocking")

    handoff = canonical.get("handoff")
    if isinstance(handoff, Mapping):
        hstate = _text(handoff.get("state"))
        work_owner = _text(work.get("owner"))
        from_owner = _text(handoff.get("from_owner"))
        work_handoff = _mapping(work.get("handoff"))
        if hstate in ("Offered", "Received", "Escalated"):
            if (
                not work_owner
                or work_owner.lower() == "unassigned"
                or (from_owner and work_owner != from_owner)
                or handoff.get("confirmed_receiver") is not None
                or _text(work_handoff.get("confirmed_receiver")) not in ("", "Unknown")
                or not _text(handoff.get("chase_owner"))
            ):
                blockers.append("same_home.handover:premature_owner_transfer_on_pending_handoff")

    mdecisions = _seq(canonical.get("measure_decisions"))
    decision_by_measure = {
        _text(item.get("measure")): _text(item.get("status"))
        for item in mdecisions
        if isinstance(item, Mapping) and _text(item.get("measure"))
    }
    overall_decision = _text(_mapping(canonical.get("decision")).get("status"))

    if isinstance(cdetail, Mapping):
        for row in _seq(cdetail.get("resident_readiness")):
            if not isinstance(row, Mapping):
                continue
            mname = _text(row.get("measure"))
            mstatus = decision_by_measure.get(mname, overall_decision)
            if mstatus != "Accepted" and _text(row.get("flag")) == "Proceed":
                blockers.append(
                    f"same_home.handover:contractor_proceed_without_resident_acceptance:{mname}"
                )

    if isinstance(rview, Mapping):
        unavailable = _seq(rview.get("unavailable"))
        has_consent_boundary = any(
            isinstance(item, Mapping) and _text(item.get("feature")) == "Consent and decisions"
            for item in unavailable
        )
        if rview.get("read_only") is not True or not has_consent_boundary:
            blockers.append("same_home.handover:resident_portal_decision_boundary_missing")

    qrecords = _seq(canonical.get("quality"))
    qblockers = _seq(canonical.get("quality_handover_blockers"))
    accepted_measures: set[str] = set()
    for rec in qrecords:
        if not isinstance(rec, Mapping):
            continue
        state = _text(rec.get("state"))
        mname = _text(rec.get("measure"))
        submitted_by = _text(rec.get("submitted_by"))
        accepted_by = _text(rec.get("accepted_by"))
        if (
            state in ("Accepted", "Handed over")
            and accepted_by
            and accepted_by.lower() != submitted_by.lower()
        ):
            accepted_measures.add(mname)
        if state == "Handed over":
            if not accepted_by or accepted_by.lower() == submitted_by.lower():
                blockers.append("same_home.handover:handed_over_without_independent_acceptance")
            if active_hazards:
                blockers.append("same_home.handover:handed_over_with_active_hazard")
            if unresolved_stock:
                blockers.append("same_home.handover:handed_over_with_unresolved_stock_query")
            if list(qblockers):
                blockers.append("same_home.handover:handed_over_with_quality_blockers")
            mstatus = decision_by_measure.get(mname, overall_decision)
            if mstatus != "Accepted":
                blockers.append("same_home.handover:handed_over_without_resident_acceptance")

    if isinstance(receipt, Mapping):
        rmeas = _text(receipt.get("measure"))
        rstatus = _text(receipt.get("status"))
        if receipt.get("accepted") is True or (
            rstatus not in (jp.SUBMITTED, jp.ACKNOWLEDGED) and rmeas not in accepted_measures
        ):
            blockers.append("same_home.handover:worker_receipt_treated_as_acceptance")

    completed_orders = [
        o for o in orders if isinstance(o, Mapping) and _text(o.get("state")) == "Completed"
    ]
    if completed_orders and (
        bool(canonical.get("closed")) or _text(canonical.get("stage")) == "Complete"
    ):
        unaccepted = [
            rec
            for rec in qrecords
            if isinstance(rec, Mapping)
            and (
                _text(rec.get("state")) not in ("Accepted", "Handed over")
                or not _text(rec.get("accepted_by"))
                or _text(rec.get("accepted_by")).lower() == _text(rec.get("submitted_by")).lower()
            )
        ]
        if not list(qrecords) or unaccepted:
            blockers.append(
                "same_home.handover:contractor_completion_closed_without_quality_acceptance"
            )

    if isinstance(trace, Mapping):
        if list(_seq(trace.get("order_findings"))):
            blockers.append("same_home.handover:audit_trace_out_of_order")
        if _text(trace.get("user_validation")) != "not-established":
            blockers.append("same_home.handover:user_validation_overclaimed")
        stage_status = {
            _text(row.get("stage")): _text(row.get("status"))
            for row in _seq(trace.get("stages"))
            if isinstance(row, Mapping)
        }
        if (
            stage_status.get("handover") == "Not recorded"
            and stage_status.get("financial_closure") == "Recorded"
        ):
            blockers.append("same_home.handover:financial_closure_before_handover")

    return blockers


def _check_single_continuity_step(bundle: Mapping[str, Any]) -> list[str]:
    staff = _staff_map(bundle)
    reasons = set(projection.reason_roles())
    blockers: list[str] = []
    owners: dict[str, str] = {}
    reason_actions: dict[str, str] = {}
    non_reason_actions: dict[str, str] = {}
    stage = ""

    for role in SIX_STAFF_PROFILES:
        view = staff.get(role)
        if not isinstance(view, Mapping):
            continue
        if not stage:
            stage = _text(view.get("stage"))
        work = view.get("work")
        if not isinstance(work, Mapping):
            blockers.append(f"same_home.continuity:missing_work_context:{role}")
            continue
        owner = _text(work.get("owner"))
        action = _text(work.get("next_action"))
        wreason = _text(work.get("reason"))
        if not owner or owner.lower() in NON_TEXT:
            blockers.append(f"same_home.continuity:missing_owner:{role}")
        else:
            owners[role] = owner
        if not action or action.lower() in NON_TEXT:
            blockers.append(f"same_home.continuity:missing_next_action:{role}")
            continue
        if role in reasons:
            reason_actions[role] = action
        else:
            non_reason_actions[role] = action
            if wreason and wreason != projection.NOTE_HELD and JARGON_RE.search(wreason):
                blockers.append(f"same_home.continuity:jargon_in_reason:{role}")
        for bitem in _seq(work.get("blockers")):
            if isinstance(bitem, Mapping):
                baction = _text(bitem.get("next_action"))
                if baction and baction != projection.NOTE_HELD and JARGON_RE.search(baction):
                    blockers.append(f"same_home.continuity:jargon_in_blocker_action:{role}")

    if len(set(owners.values())) > 1:
        blockers.append("same_home.continuity:owner_mismatch_across_staff")

    if len(set(reason_actions.values())) > 1:
        blockers.append("same_home.continuity:next_action_mismatch_among_reason_roles")

    canonical_action = next(iter(reason_actions.values()), "")
    if canonical_action:
        for role, action in non_reason_actions.items():
            if action not in (canonical_action, projection.NOTE_HELD):
                blockers.append(f"same_home.continuity:next_action_mismatch:{role}")
        if all(a == canonical_action for a in non_reason_actions.values()) and JARGON_RE.search(
            canonical_action
        ):
            blockers.append("same_home.continuity:jargon_in_next_action")

    canonical = _canonical_staff_view(staff)
    if canonical is not None:
        handoff = canonical.get("handoff")
        work_handoff = _mapping(_mapping(canonical.get("work")).get("handoff"))
        if isinstance(handoff, Mapping):
            hstate = _text(handoff.get("state"))
            to_owner = _text(handoff.get("to_owner"))
            if hstate in ("Offered", "Received", "Escalated"):
                if (
                    handoff.get("confirmed_receiver") is not None
                    or _text(work_handoff.get("confirmed_receiver")) not in ("", "Unknown")
                    or not _text(handoff.get("chase_owner"))
                ):
                    blockers.append("same_home.continuity:pending_handoff_receiver_invalid")
            elif hstate in ("Accepted", "Completed"):
                if not _text(handoff.get("confirmed_receiver")) or (
                    to_owner and _text(handoff.get("confirmed_receiver")) != to_owner
                ):
                    blockers.append("same_home.continuity:accepted_handoff_receiver_missing")

    rview = bundle.get("resident_view")
    if isinstance(rview, Mapping):
        if rview.get("read_only") is not True or _text(rview.get("banner")) != rp.BANNER:
            blockers.append("same_home.continuity:resident_preview_boundary_missing")
        unavailable = _seq(rview.get("unavailable"))
        if not any(
            isinstance(item, Mapping) and _text(item.get("feature")) == "Consent and decisions"
            for item in unavailable
        ):
            blockers.append("same_home.continuity:resident_consent_boundary_missing")
        exp_progress, exp_next = rp.STAGE_TEXT.get(stage, (rp.UNKNOWN_PROGRESS, rp.UNKNOWN_NEXT))
        if "progress" in rview:
            prog = _text(rview.get("progress"))
            if not prog or prog.lower() in NON_TEXT or prog != exp_progress:
                blockers.append("same_home.continuity:resident_progress_invalid")
            elif JARGON_RE.search(prog):
                blockers.append("same_home.continuity:jargon_in_resident_progress")
        if "next_step" in rview:
            nstep = _text(rview.get("next_step"))
            if not nstep or nstep.lower() in NON_TEXT or nstep != exp_next:
                blockers.append("same_home.continuity:resident_next_step_invalid")
            elif JARGON_RE.search(nstep):
                blockers.append("same_home.continuity:jargon_in_resident_next_step")

    return blockers


def check_next_action_continuity(
    transitions_or_bundle: Sequence[Mapping[str, Any]] | Mapping[str, Any],
) -> list[str]:
    """Verify plain-language owner and next-action continuity across same-home transitions."""
    if isinstance(transitions_or_bundle, Mapping):
        return _check_single_continuity_step(transitions_or_bundle)
    steps = list(transitions_or_bundle)
    if not steps:
        return ["same_home.continuity:empty_transitions"]
    blockers: list[str] = []
    for idx, step in enumerate(steps):
        prefix = "" if len(steps) == 1 else f"step_{idx}:"
        blockers.extend(f"{prefix}{b}" for b in _check_single_continuity_step(step))
    return blockers


def project_same_home_bundle(
    store: Any,
    case_id: str,
    *,
    staff_users: Mapping[str, dict[str, Any]],
    contractor_user: dict[str, Any] | None = None,
    resident_grant: rp.Grant | None = None,
    work_order_id: str | None = None,
    job_pack_receipt: Mapping[str, Any] | None = None,
    worker_receipt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a connected same-home projection bundle across roles without mutating store state."""
    staff_views: dict[str, Any] = {}
    first_staff_user: dict[str, Any] | None = None
    for role in (*SIX_STAFF_PROFILES, "Programme Support Officer"):
        user = staff_users.get(role)
        if user is not None:
            if first_staff_user is None and role in SIX_STAFF_PROFILES:
                first_staff_user = user
            staff_views[role] = store.detail(case_id, user)

    csummary: dict[str, Any] | None = None
    cdetail = store.detail(case_id, contractor_user) if contractor_user is not None else None
    if contractor_user is not None:
        rows = store.list_cases(contractor_user)
        csummary = next(
            (r for r in rows if isinstance(r, dict) and r.get("id") == case_id),
            None,
        )
    orders: list[dict[str, Any]] = []
    if contractor_user is not None:
        orders = list(store.list_work_orders(contractor_user, case_id=case_id))
    elif first_staff_user is not None:
        orders = list(store.list_work_orders(first_staff_user, case_id=case_id))

    pack = (
        store.work_order_job_pack(first_staff_user, work_order_id)
        if work_order_id and first_staff_user is not None
        else None
    )
    rview = rp.resident_view(store, resident_grant) if resident_grant is not None else None
    if hasattr(store, "audit_entries"):
        audit_entries: Sequence[Any] = list(store.audit_entries())
    elif isinstance(getattr(store, "data", None), Mapping):
        audit_entries = list(store.data.get("audit", []))
    else:
        audit_entries = ()
    trace = jt.journey_trace(audit_entries, case_id)
    raw_receipt = job_pack_receipt if job_pack_receipt is not None else worker_receipt
    receipt_copy = dict(raw_receipt) if isinstance(raw_receipt, Mapping) else None
    return dict(
        case_id=case_id,
        staff=staff_views,
        staff_views=staff_views,
        contractor_summary=csummary,
        contractor_detail=cdetail,
        work_orders=orders,
        job_pack=pack,
        job_pack_receipt=receipt_copy,
        worker_receipt=receipt_copy,
        resident_view=rview,
        audit_trace=trace,
    )


def validate_same_home_walk(
    bundle_or_transitions: Mapping[str, Any] | Sequence[Mapping[str, Any]],
    *,
    case_id: str | None = None,
    vulnerability_reason: str | None = None,
    raw_adjustment: str = "",
    private_markers: Sequence[str] = (),
    contractor_private_markers: Sequence[str] = (),
    sibling_ids: Sequence[str] = (),
    sibling_markers: Sequence[str] = (),
    transitions: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate connected same-home invariants across one bundle or an ordered transition walk."""
    if isinstance(bundle_or_transitions, Mapping):
        steps = [bundle_or_transitions, *(transitions or ())]
    else:
        steps = list(bundle_or_transitions)
    if not steps:
        return dict(
            ok=False,
            status="blocked",
            blockers=["same_home.walk:empty_transitions"],
            accepted=False,
            boundaries=dict(BOUNDARIES),
            notice=SAME_HOME_NOTICE,
        )

    secret = _text(vulnerability_reason) or _text(raw_adjustment)
    blockers: list[str] = []
    anchor_id = _text(case_id)
    anchor_address = ""
    anchor_postcode = ""

    for idx, step in enumerate(steps):
        prefix = "" if len(steps) == 1 else f"step_{idx}:"
        step_case = anchor_id or _text(step.get("case_id"))
        step_with_id = (
            dict(step, case_id=step_case) if step_case and not _text(step.get("case_id")) else step
        )
        step_blockers = [
            *check_shared_facts(
                step_with_id,
                sibling_ids=sibling_ids,
                sibling_markers=sibling_markers,
            ),
            *check_handover_dependencies(step_with_id),
            *_check_single_continuity_step(step_with_id),
        ]
        if secret:
            step_blockers.extend(
                check_vulnerability_redaction(
                    step_with_id,
                    vulnerability_reason=secret,
                    private_markers=private_markers,
                    contractor_private_markers=contractor_private_markers,
                )
            )
        blockers.extend(f"{prefix}{b}" for b in step_blockers)

        canonical = _canonical_staff_view(_staff_map(step_with_id))
        if canonical is not None:
            cid = _text(canonical.get("id"))
            home = _mapping(canonical.get("home"))
            addr = _text(home.get("address"))
            post = _text(home.get("postcode"))
            if idx == 0:
                anchor_id = anchor_id or cid
                anchor_address, anchor_postcode = addr, post
            elif (cid, addr, post) != (anchor_id, anchor_address, anchor_postcode):
                blockers.append(f"step_{idx}:same_home.walk:home_identity_changed")

    return dict(
        ok=not blockers,
        status="blocked" if blockers else "complete_in_shape",
        blockers=blockers,
        accepted=False,
        boundaries=dict(BOUNDARIES),
        notice=SAME_HOME_NOTICE,
    )
