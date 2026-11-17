"""Nomination and self-referral route rules (FR-037, AC-065, RULE-005; issue #130).

Store-independent checks over a nomination record. They gate human review on an acknowledged
route and a named owner, summarise the retained challenge trail, find the dependent decisions a
correction sends back for re-review, and route hazard concerns to the independent hazard intake
(#85). Nothing here accepts, sanctions, changes priority or consent, or touches a hazard clock.
"""

from collections.abc import Iterable, Mapping
from typing import Any

from .challenges import ChallengeRegister, Node

Record = dict[str, Any]

HAZARD_INTAKE: Record = {
    "route": "independent_hazard_intake",
    "issue": "#85",
    "endpoint": "/api/cases/{case_id}/hazard-raise",
    "queue_item_created": False,
    "immediate": True,
}
HAZARD_MESSAGE = (
    "Use the independent hazard intake now (/api/cases/{case_id}/hazard-raise), not the nomination "
    "queue. Existing hazard service owns emergency response and clocks. Nothing was saved here."
)
HAZARD_ROUTING_MESSAGE = HAZARD_MESSAGE
REVIEW_BLOCKED = (
    "Human review cannot start until the referral has a named owner, a staff-recorded "
    "acknowledgement and a staffed non-digital route. Missing: {missing}."
)
NOT_DECIDED = ("acceptance", "sanction", "priority change", "consent or refusal", "hazard clock")
ROUTE_MODES: tuple[str, str] = ("digital", "staff_recorded_non_digital")
ASSISTED_NON_DIGITAL_CHANNELS: dict[str, str] = {
    "phone": "Phone",
    "paper": "Paper",
    "letter": "Letter",
    "in_person": "In person",
    "in person": "In person",
    "trusted_intermediary": "Trusted intermediary",
    "trusted intermediary": "Trusted intermediary",
    "permitted_intermediary": "Trusted intermediary",
    "permitted intermediary": "Trusted intermediary",
}
LEGACY_NON_DIGITAL_LABELS: tuple[str, ...] = (
    "Phone",
    "Paper",
    "Letter",
    "In person",
    "Trusted intermediary",
)
RESTRICTED_VULNERABILITY_KEYS: frozenset[str] = frozenset(
    {
        "internal_vulnerability_note",
        "vulnerability_notes",
        "vulnerability_detail",
        "health_detail",
        "safeguarding_note",
        "safeguarding_detail",
        "vulnerability_reason",
        "priority_support",
        "medical_note",
        "medical_detail",
        "clinical_note",
        "clinical_detail",
        "domestic_abuse_note",
        "internal_risk_notes",
        "support_detail",
        "adjustment_detail",
    }
)
RESTRICTED_VULNERABILITY_PREFIXES: tuple[str, ...] = (
    "vulnerability_",
    "internal_vulnerability",
    "safeguarding_",
    "medical_",
    "clinical_",
    "domestic_abuse",
    "internal_risk",
)


def _is_restricted_vulnerability_key(key: str) -> bool:
    lowered = key.strip().casefold()
    return lowered in RESTRICTED_VULNERABILITY_KEYS or lowered.startswith(
        RESTRICTED_VULNERABILITY_PREFIXES
    )


def normalize_route_channel(
    channel: object,
    *,
    assisted_channel: object = None,
    allow_intermediary: bool = True,
    label: str = "the supplied channel",
) -> tuple[str, str, str | None]:
    """Validate digital and staff-recorded non-digital route channels fail-closed."""
    if not _non_blank(channel):
        raise ValueError(f"Choose {label}.")
    assert isinstance(channel, str)
    raw = channel.strip()

    resolved_assisted: str | None = None
    if assisted_channel is not None:
        if not isinstance(assisted_channel, str):
            raise ValueError("Choose a supported assisted non-digital intake channel.")
        if assisted_channel.strip():
            mapped = ASSISTED_NON_DIGITAL_CHANNELS.get(assisted_channel.strip().casefold())
            if mapped is None:
                raise ValueError(
                    "Choose a supported assisted non-digital intake channel "
                    "(phone, paper, letter or in person)."
                )
            resolved_assisted = mapped

    if raw in ("digital", "Digital"):
        if resolved_assisted is not None:
            raise ValueError(
                "Assisted non-digital channel applies only to staff-recorded non-digital routes."
            )
        return (raw, "digital", None)

    if raw == "staff_recorded_non_digital":
        if resolved_assisted is None:
            raise ValueError(
                "Choose a supported assisted non-digital intake channel "
                "(phone, paper, letter or in person)."
            )
        medium = resolved_assisted
        if not allow_intermediary and medium == "Trusted intermediary":
            raise ValueError(f"Choose {label} from phone, paper, letter or in-person routes.")
        return ("staff_recorded_non_digital", "staff_recorded_non_digital", medium)

    if raw in LEGACY_NON_DIGITAL_LABELS:
        if not allow_intermediary and raw == "Trusted intermediary":
            raise ValueError(f"Choose {label}.")
        if resolved_assisted is not None and resolved_assisted != raw:
            raise ValueError("Assisted non-digital channel must match the selected channel.")
        return (raw, "staff_recorded_non_digital", raw)

    raise ValueError(f"Choose {label}.")


def scrub_nomination_restricted_fields(value: Any) -> Any:
    """Recursively remove restricted internal vulnerability keys and unpermitted entries."""
    if isinstance(value, Mapping):
        if value.get("permitted") is False:
            return {}
        cleaned: Record = {}
        for key, item in value.items():
            key_str = str(key)
            if _is_restricted_vulnerability_key(key_str):
                continue
            cleaned[key_str] = scrub_nomination_restricted_fields(item)
        return cleaned
    if isinstance(value, list):
        out_list: list[Any] = []
        for elem in value:
            if isinstance(elem, Mapping) and elem.get("permitted") is False:
                continue
            out_list.append(scrub_nomination_restricted_fields(elem))
        return out_list
    if isinstance(value, tuple):
        return tuple(
            scrub_nomination_restricted_fields(elem)
            for elem in value
            if not (isinstance(elem, Mapping) and elem.get("permitted") is False)
        )
    return value


def _human_owner_summary(owner: object) -> str:
    if _named_owner_present(owner) and isinstance(owner, Mapping):
        name = str(owner["name"]).strip()
        role_raw = owner.get("role")
        role = f" ({role_raw.strip()})" if isinstance(role_raw, str) and role_raw.strip() else ""
        return (
            f"{name}{role} — a named person owns every review and follow-up decision; "
            "nothing is decided automatically."
        )
    return (
        "Unassigned — a named human owner is required before review starts; "
        "nothing is decided automatically."
    )


def _route_summary_label(entry: Mapping[str, Any]) -> str:
    route_mode = entry.get("route_mode")
    assisted = entry.get("assisted_channel")
    channel = entry.get("channel")
    if route_mode == "staff_recorded_non_digital" or channel == "staff_recorded_non_digital":
        detail = str(assisted).strip() if _non_blank(assisted) else "Assisted non-digital intake"
        return f"staff-recorded non-digital route ({detail})"
    if route_mode == "digital" or channel in ("digital", "Digital"):
        return "digital route"
    if _non_blank(channel):
        return f"staff-recorded non-digital route ({str(channel).strip()})"
    return "recorded intake route"


def nomination_explanation(
    record: Mapping[str, Any],
    *,
    follow_up: Mapping[str, Any] | None = None,
    recommendations: Iterable[Mapping[str, Any]] = (),
    can_view_intake: bool = True,
    can_view_reason: bool = True,
) -> Record:
    """Build deterministic, permitted plain-language explanation without restricted fields."""
    owner_text = _human_owner_summary(record.get("owner"))

    ai_labels: list[str] = []
    rule_ids: list[str] = []
    policy_versions: list[str] = []
    for rec in recommendations:
        if not isinstance(rec, Mapping) or rec.get("kind") == "ai_task":
            continue
        rec_id_raw = rec.get("id") or rec.get("proposal_id")
        if not _non_blank(rec_id_raw):
            continue
        rec_id = str(rec_id_raw).strip()
        ai_meta = rec.get("ai_details")
        src = rec.get("source") or (ai_meta.get("source") if isinstance(ai_meta, Mapping) else None)
        model = rec.get("model") or (ai_meta.get("model") if isinstance(ai_meta, Mapping) else None)
        pol = rec.get("policy_version") or (
            ai_meta.get("policy_version") if isinstance(ai_meta, Mapping) else None
        )
        if _non_blank(pol):
            pol_label = f"{rec_id} (policy {str(pol).strip()})"
            if pol_label not in policy_versions:
                policy_versions.append(pol_label)
        if src == "ai":
            lbl = f"{rec_id} (model {str(model).strip()})" if _non_blank(model) else rec_id
            if lbl not in ai_labels:
                ai_labels.append(lbl)
        elif rec_id not in rule_ids:
            rule_ids.append(rec_id)

    if ai_labels:
        ai_text = (
            "No AI was used to record, acknowledge, correct or review this referral. "
            f"Separate AI priority suggestion {', '.join(ai_labels)} included this home using "
            "recorded workflow fields only; AI does not decide eligibility, infer health or "
            "support needs, or approve or reject referrals."
        )
    elif rule_ids:
        ai_text = (
            "No AI was involved in this referral or in priority suggestion "
            f"{', '.join(rule_ids)}. Every identity, eligibility and follow-up decision is "
            "made by a named person."
        )
    else:
        ai_text = (
            "No AI was involved in recording, acknowledging, correcting or reviewing this "
            "referral. Every identity, eligibility and follow-up decision is made by a named "
            "person."
        )

    raw_orig = record.get("original")
    original: Mapping[str, Any] = raw_orig if isinstance(raw_orig, Mapping) else {}
    kind = str(record.get("kind")).strip() if _non_blank(record.get("kind")) else "Referral"
    sources: list[str] = [f"{kind} recorded via {_route_summary_label(original)}"]
    if can_view_intake and can_view_reason:
        if original.get("permitted") is not False and _non_blank(original.get("source")):
            sources.append(f"Supplied intake source: {str(original['source']).strip()}")
        raw_ack = record.get("acknowledgement")
        if isinstance(raw_ack, Mapping) and _non_blank(raw_ack.get("reference")):
            sources.append(
                f"Acknowledgement reference ({_route_summary_label(raw_ack)}): "
                f"{str(raw_ack['reference']).strip()}"
            )
        raw_corrs = record.get("corrections")
        if isinstance(raw_corrs, Iterable) and not isinstance(raw_corrs, (str, bytes)):
            corr_list = [
                c for c in raw_corrs if isinstance(c, Mapping) and c.get("permitted") is not False
            ]
            if corr_list and _non_blank(corr_list[-1].get("source")):
                latest_corr = corr_list[-1]
                sources.append(
                    f"Latest correction source (v{latest_corr.get('version')}, "
                    f"{_route_summary_label(latest_corr)}): {str(latest_corr['source']).strip()}"
                )
        raw_revs = record.get("reviews")
        if isinstance(raw_revs, Iterable) and not isinstance(raw_revs, (str, bytes)):
            rev_list = [
                rv
                for rv in raw_revs
                if isinstance(rv, Mapping) and rv.get("permitted") is not False
            ]
            if rev_list and _non_blank(rev_list[-1].get("evidence_ref")):
                sources.append(
                    f"Human review evidence reference: {str(rev_list[-1]['evidence_ref']).strip()}"
                )
    for pol_entry in policy_versions:
        sources.append(f"Case priority suggestion reference: {pol_entry}")
    if not (can_view_intake and can_view_reason):
        sources = [s for s in sources if s.startswith("Case priority suggestion reference:")]

    policy_reasons: list[str] = [
        "Staffed nomination and self-referral route (FR-037): priority and support never rely "
        "solely on pre-recorded household flags.",
        "Protected challenge and safety rule (RULE-005): raising or correcting a referral never "
        "delays repairs, building safety action, or access to formal complaints and the Housing "
        "Ombudsman.",
    ]
    raw_corrs_check = record.get("corrections")
    has_corrections = bool(isinstance(raw_corrs_check, list) and len(raw_corrs_check) > 0)
    if has_corrections:
        policy_reasons.append(
            "Supplied correction re-review rule (FR-043): competing evidence stays alongside the "
            "original account and sends earlier reviews back for human re-review without automatic "
            "acceptance or sanction."
        )
    if can_view_intake and can_view_reason:
        raw_revs_check = record.get("reviews")
        if isinstance(raw_revs_check, list) and raw_revs_check:
            last_rev = raw_revs_check[-1]
            if (
                isinstance(last_rev, Mapping)
                and last_rev.get("permitted") is not False
                and _non_blank(last_rev.get("outcome"))
            ):
                policy_reasons.append(
                    f"Recorded human review outcome (v{last_rev.get('record_version')}): "
                    f"{str(last_rev['outcome']).strip()}."
                )

    uncertainty_parts: list[str] = []
    for field_key, field_label in (
        ("identity_status", "Identity status"),
        ("support_needs", "Support needs"),
        ("risk_flags", "Risk flags"),
    ):
        val = record.get(field_key)
        if not _non_blank(val) or str(val).strip() == "Unknown":
            uncertainty_parts.append(f"{field_label}: Unknown")
    ack_map = record.get("acknowledgement")
    delivery = ack_map.get("delivery") if isinstance(ack_map, Mapping) else None
    if delivery != "Verified":
        uncertainty_parts.append("Acknowledgement delivery: Not verified by this system")
    missing = missing_before_review(record)
    if missing:
        uncertainty_parts.append(f"Missing before human review: {', '.join(missing)}")
    re_review_flag = (
        bool(follow_up.get("re_review_pending"))
        if isinstance(follow_up, Mapping)
        else has_corrections
    )
    if re_review_flag:
        uncertainty_parts.append(
            "Earlier review is marked for human re-review following supplied correction"
        )
    uncertainty_parts.append(
        "Unknown items remain recorded as Unknown and are never treated as None."
    )

    return {
        "permitted": True,
        "ai_involved": bool(ai_labels),
        "human_decision_owner": owner_text,
        "ai_involvement_explanation": ai_text,
        "sources": sources,
        "policy_reasons": policy_reasons,
        "uncertainty_note": "; ".join(uncertainty_parts),
    }


def challenge_explanation(
    item: Mapping[str, Any],
    *,
    can_view_intake: bool = True,
    can_view_reason: bool = True,
) -> Record:
    """Build deterministic, permitted plain-language explanation for a challenge or target."""
    owner_raw = item.get("owner")
    decision_raw = item.get("human_decision")
    resolved_by = decision_raw.get("resolved_by") if isinstance(decision_raw, Mapping) else None
    if _named_owner_present(owner_raw):
        owner_text = _human_owner_summary(owner_raw)
    elif _non_blank(resolved_by):
        owner_text = (
            f"{str(resolved_by).strip()} — a named person owns the recorded suggestion review; "
            "any challenge is assigned to a named reviewer and nothing is decided automatically."
        )
    else:
        owner_text = (
            "Named human reviewer required — priority suggestions and challenges are always "
            "decided by a named person, never automatically."
        )

    ai_meta = item.get("ai_details")
    src = (
        ai_meta.get("source")
        if isinstance(ai_meta, Mapping) and _non_blank(ai_meta.get("source"))
        else item.get("source")
    )
    model = (
        ai_meta.get("model")
        if isinstance(ai_meta, Mapping) and _non_blank(ai_meta.get("model"))
        else item.get("model")
    )
    pid = str(item.get("proposal_id")).strip() if _non_blank(item.get("proposal_id")) else "record"
    if src == "ai":
        model_note = f" (model {str(model).strip()})" if _non_blank(model) else ""
        ai_text = (
            f"AI was involved in generating priority suggestion {pid}{model_note} from recorded "
            "workflow fields only. AI does not decide challenges, infer health or support needs, "
            "or change priority; a named person reviews and decides every step."
        )
    else:
        basis = str(src).strip() if src in ("workflow", "manual", "fallback") else "workflow rules"
        ai_text = (
            f"No AI was used to generate priority suggestion {pid} (basis: {basis}). "
            "A named person reviews and decides every challenge and correction."
        )

    pol_ver = item.get("policy_version") or (
        ai_meta.get("policy_version") if isinstance(ai_meta, Mapping) else None
    )
    src_ver = item.get("source_version")
    if src_ver is None and isinstance(ai_meta, Mapping):
        sv_map = ai_meta.get("source_versions")
        if isinstance(sv_map, Mapping) and len(sv_map) == 1:
            src_ver = next(iter(sv_map.values()))

    sources: list[str] = [f"Priority suggestion reference: {pid}"]
    if _non_blank(src_ver) or isinstance(src_ver, int):
        sources.append(f"Recorded case source version: {src_ver}")
    if _non_blank(pol_ver):
        sources.append(f"Priority policy version: {str(pol_ver).strip()}")
    if _non_blank(item.get("channel")) or _non_blank(item.get("route_mode")):
        sources.append(f"Challenge intake route: {_route_summary_label(item)}")
    if can_view_intake and can_view_reason:
        supplied_src = item.get("source")
        if (
            item.get("permitted") is not False
            and _non_blank(supplied_src)
            and supplied_src not in ("ai", "workflow", "manual", "fallback")
        ):
            sources.append(f"Supplied challenge reference: {str(supplied_src).strip()}")
        res = item.get("resolution")
        if isinstance(res, Mapping) and _non_blank(res.get("reference")):
            sources.append(f"Human resolution reference: {str(res['reference']).strip()}")

    policy_reasons: list[str] = [
        "Right to plain-language explanation and challenge (FR-041 / AC-065): affected residents "
        "and confirmed representatives receive clear reasons, AI involvement details, and a named "
        "human reviewer.",
        "Protected non-retaliation rule (RULE-005): challenging a priority suggestion never slows "
        "repairs, safety duties, or access to formal complaints and the Housing Ombudsman.",
    ]
    if _non_blank(pol_ver):
        policy_reasons.append(f"Priority ranking policy version applied: {str(pol_ver).strip()}.")
    if (
        can_view_intake
        and can_view_reason
        and item.get("permitted") is not False
        and _non_blank(item.get("explanation"))
    ):
        policy_reasons.append(
            f"Recorded plain-language explanation: {str(item['explanation']).strip()}"
        )

    uncertainty_parts: list[str] = []
    if not (_non_blank(src_ver) or isinstance(src_ver, int)):
        uncertainty_parts.append("Case source version: Unknown")
    if not _non_blank(pol_ver):
        uncertainty_parts.append("Priority policy version: Unknown")
    status = item.get("status")
    if status == "Open":
        uncertainty_parts.append("Challenge outcome: Pending human review")
    elif status is None and isinstance(decision_raw, Mapping) and not decision_raw.get("status"):
        uncertainty_parts.append("Suggestion disposition: Pending human review")
    if item.get("stale") or item.get("review_stale"):
        uncertainty_parts.append(
            "Recorded correction affects this suggestion; human re-review is required"
        )
    uncertainty_parts.append(
        "Unverified or missing items stay marked Unknown until a named person checks them."
    )

    return {
        "permitted": True,
        "ai_involved": src == "ai",
        "human_decision_owner": owner_text,
        "ai_involvement_explanation": ai_text,
        "sources": sources,
        "policy_reasons": policy_reasons,
        "uncertainty_note": "; ".join(uncertainty_parts),
    }


def filter_explanation_for_viewer(
    explanation: Mapping[str, Any] | None,
    *,
    can_view_intake: bool,
    can_view_reason: bool,
) -> Record | None:
    """Filter an explanation payload according to role and reason-view rights fail-closed."""
    if explanation is None or not can_view_intake or explanation.get("permitted") is False:
        return None
    scrubbed = scrub_nomination_restricted_fields(explanation)
    if not isinstance(scrubbed, dict):
        return None
    if can_view_reason:
        return scrubbed
    raw_sources = scrubbed.get("sources")
    safe_sources = (
        [
            str(s)
            for s in raw_sources
            if isinstance(s, str)
            and (
                s.startswith("Priority suggestion reference:")
                or s.startswith("Case priority suggestion reference:")
                or s.startswith("Priority policy version:")
            )
        ]
        if isinstance(raw_sources, list)
        else []
    )
    raw_reasons = scrubbed.get("policy_reasons")
    safe_reasons = (
        [
            str(r)
            for r in raw_reasons
            if isinstance(r, str)
            and not r.startswith("Recorded human review outcome")
            and not r.startswith("Recorded plain-language explanation:")
        ]
        if isinstance(raw_reasons, list)
        else []
    )
    return {
        "permitted": True,
        "ai_involved": bool(scrubbed.get("ai_involved")),
        "human_decision_owner": (
            "Named human reviewer required — every referral and challenge decision is owned by a "
            "named person; nothing is decided automatically."
        ),
        "ai_involvement_explanation": str(scrubbed.get("ai_involvement_explanation") or ""),
        "sources": safe_sources,
        "policy_reasons": safe_reasons,
        "uncertainty_note": str(scrubbed.get("uncertainty_note") or ""),
    }


def _non_blank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _named_owner_present(owner: object) -> bool:
    if not isinstance(owner, Mapping):
        return False
    name = owner.get("name")
    if not isinstance(name, str) or not name.strip():
        return False
    role = owner.get("role")
    if (
        isinstance(role, str)
        and role.strip()
        and name.strip().casefold() == role.strip().casefold()
    ):
        return False
    return True


def missing_before_review(record: Mapping[str, Any]) -> list[str]:
    """Route prerequisites a record still lacks; an empty list means review may start."""
    owner = record.get("owner")
    ack = record.get("acknowledgement")
    return [
        label
        for label, ready in (
            ("named owner", _named_owner_present(owner)),
            (
                "staff-recorded acknowledgement",
                isinstance(ack, Mapping) and _non_blank(ack.get("reference")),
            ),
            ("staffed non-digital route", _non_blank(record.get("non_digital_route"))),
        )
        if not ready
    ]


def require_ready_for_review(record: Mapping[str, Any]) -> None:
    missing = missing_before_review(record)
    if missing:
        raise ValueError(REVIEW_BLOCKED.format(missing=", ".join(missing)))


def hazard_routing(hazard_concern: object, *, case_id: str | None = None) -> Record | None:
    """The hazard-intake route when any hazard or emergency concern is flagged; else None.

    Only an explicit False is a clear answer: unknown or missing is routed, never ignored.
    """
    if hazard_concern is False:
        return None
    clean_case = case_id.strip() if isinstance(case_id, str) and case_id.strip() else None
    action = (
        f"/api/cases/{clean_case}/hazard-raise"
        if clean_case is not None
        else str(HAZARD_INTAKE["endpoint"])
    )
    return {**HAZARD_INTAKE, "action": action, "message": HAZARD_MESSAGE}


class HazardRouted(ValueError):
    """Emergency or hazard concern refused here and routed to the independent hazard intake."""

    route: Record = dict(HAZARD_INTAKE)

    def __init__(self, message: str = HAZARD_MESSAGE, *, case_id: str | None = None) -> None:
        super().__init__(message)
        routed = hazard_routing(True, case_id=case_id)
        assert routed is not None
        self.route = routed


def _reviewer_name(entry: object) -> str | None:
    if not isinstance(entry, Mapping):
        return None
    name = entry.get("name")
    return name if isinstance(name, str) and name.strip() else None


def _reviewer_code(entry: object) -> str | None:
    if not isinstance(entry, Mapping):
        return None
    code = entry.get("code")
    return code if isinstance(code, str) and code.strip() else None


def challenge_trail(
    record: Mapping[str, Any],
    challenges: Iterable[Mapping[str, Any]] = (),
) -> Record:
    """Read-only retained trail: original account, competing evidence, reviewer and outcome."""
    raw_original = record.get("original")
    original: Mapping[str, Any] = raw_original if isinstance(raw_original, Mapping) else {}
    raw_corrections = record.get("corrections")
    corrections: Iterable[Any] = (
        raw_corrections
        if isinstance(raw_corrections, Iterable) and not isinstance(raw_corrections, (str, bytes))
        else ()
    )
    raw_reviews = record.get("reviews")
    reviews: Iterable[Any] = (
        raw_reviews
        if isinstance(raw_reviews, Iterable) and not isinstance(raw_reviews, (str, bytes))
        else ()
    )
    by_id: dict[str, Mapping[str, Any]] = {
        str(ch["id"]): ch
        for ch in challenges
        if isinstance(ch, Mapping) and _non_blank(ch.get("id"))
    }
    competing: list[Record] = []
    for item in corrections:
        if not isinstance(item, Mapping):
            continue
        linked = item.get("challenge")
        cid_raw = linked.get("id") if isinstance(linked, Mapping) else None
        cid = str(cid_raw) if _non_blank(cid_raw) else None
        live = by_id.get(cid) if cid is not None else None
        effective = live if live is not None else (linked if isinstance(linked, Mapping) else None)
        res_raw = effective.get("resolution") if isinstance(effective, Mapping) else None
        resolution: Record | None = None
        if isinstance(res_raw, Mapping):
            resolution = {
                "outcome": res_raw.get("outcome"),
                "reviewer": _reviewer_name(res_raw.get("recorded_by")),
                "reference": res_raw.get("reference"),
            }
        cr_raw = item.get("challenged_review")
        challenged_review: Record | None = None
        if isinstance(cr_raw, Mapping):
            challenged_review = {
                "record_version": cr_raw.get("record_version"),
                "reviewer": _reviewer_name(cr_raw.get("reviewer")),
                "outcome": cr_raw.get("outcome"),
            }
        competing.append(
            {
                "version": item.get("version"),
                "reported_subject_ref": item.get("reported_subject_ref"),
                "account": item.get("account"),
                "source": item.get("source"),
                "channel": item.get("channel"),
                "route_mode": item.get("route_mode"),
                "assisted_channel": item.get("assisted_channel"),
                "raised_by": item.get("raised_by"),
                "representative_ref": item.get("representative_ref"),
                "challenge_id": cid,
                "challenge_status": (
                    effective.get("status") if isinstance(effective, Mapping) else None
                ),
                "challenge_resolution": resolution,
                "challenged_review": challenged_review,
            }
        )
    review_items: list[Record] = []
    for rev in reviews:
        if not isinstance(rev, Mapping):
            continue
        versions_raw = rev.get("competing_evidence_versions")
        ev_versions = (
            list(versions_raw)
            if isinstance(versions_raw, Iterable) and not isinstance(versions_raw, (str, bytes))
            else []
        )
        review_items.append(
            {
                "record_version": rev.get("record_version"),
                "reviewer": _reviewer_name(rev.get("reviewer")),
                "reviewer_code": _reviewer_code(rev.get("reviewer")),
                "outcome": rev.get("outcome"),
                "rationale": rev.get("rationale"),
                "evidence_ref": rev.get("evidence_ref"),
                "competing_evidence_versions": ev_versions,
                "stale_from_version": rev.get("stale_from_version"),
            }
        )
    return {
        "original_account": original.get("account"),
        "original": {
            "reported_subject_ref": original.get("reported_subject_ref"),
            "account": original.get("account"),
            "source": original.get("source"),
            "channel": original.get("channel"),
            "route_mode": original.get("route_mode"),
            "assisted_channel": original.get("assisted_channel"),
        },
        "competing_evidence": competing,
        "reviews": review_items,
        "not_decided": list(NOT_DECIDED),
    }


def parse_node(raw: object, label: str = "decision node") -> Node:
    """Validate and normalize a (kind, id, version) decision node fail-closed."""
    parts: tuple[object, object, object] | None = None
    if isinstance(raw, Mapping):
        if set(raw) != {"kind", "id", "version"}:
            raise ValueError(f"Supply a valid {label} (kind, id, version).")
        parts = (raw["kind"], raw["id"], raw["version"])
    elif isinstance(raw, (list, tuple)) and len(raw) == 3:
        parts = (raw[0], raw[1], raw[2])
    if parts is None:
        raise ValueError(f"Supply a valid {label} (kind, id, version).")
    raw_kind, raw_id, raw_ver = parts
    if not _non_blank(raw_kind) or not _non_blank(raw_id):
        raise ValueError(f"Supply a valid {label} (kind, id, version).")
    assert isinstance(raw_kind, str) and isinstance(raw_id, str)
    kind = raw_kind.strip()
    ident = raw_id.strip()
    if isinstance(raw_ver, int) and not isinstance(raw_ver, bool) and raw_ver >= 1:
        ver = f"v{raw_ver}" if kind == "nomination" else str(raw_ver)
    elif isinstance(raw_ver, str) and raw_ver.strip():
        clean_ver = raw_ver.strip()
        if kind == "nomination" and clean_ver.isdigit() and int(clean_ver) >= 1:
            ver = f"v{int(clean_ver)}"
        else:
            ver = clean_ver
    else:
        raise ValueError(f"Supply a valid {label} (kind, id, version).")
    return (kind, ident, ver)


def parse_dependencies(raw: object) -> dict[Node, list[Node]]:
    """Validate a JSON-friendly dependency graph into ChallengeRegister Node edges."""
    result: dict[Node, list[Node]] = {}
    if isinstance(raw, Mapping):
        for raw_target, raw_sources in raw.items():
            target = parse_node(raw_target, "dependent decision")
            if not isinstance(raw_sources, (list, tuple)) or not raw_sources:
                raise ValueError("Supply at least one upstream node in depends_on.")
            sources = [parse_node(src, "upstream decision") for src in raw_sources]
            result[target] = sources
        return result
    if isinstance(raw, (list, tuple)):
        for entry in raw:
            if not isinstance(entry, Mapping) or set(entry) != {"decision", "depends_on"}:
                raise ValueError("Each dependency entry needs decision and depends_on.")
            target = parse_node(entry["decision"], "dependent decision")
            raw_sources = entry["depends_on"]
            if not isinstance(raw_sources, (list, tuple)) or not raw_sources:
                raise ValueError("Supply at least one upstream node in depends_on.")
            sources = [parse_node(src, "upstream decision") for src in raw_sources]
            if target in result:
                for src in sources:
                    if src not in result[target]:
                        result[target].append(src)
            else:
                result[target] = sources
        return result
    raise ValueError("Supply dependencies as a list of {decision, depends_on} entries.")


def _nomination_version_cutoff(corrected: Node) -> int | None:
    if corrected[0] != "nomination":
        return None
    ver = corrected[2].strip()
    if ver.startswith(("v", "V")):
        ver = ver[1:]
    if ver.isdigit() and int(ver) >= 1:
        return int(ver)
    return None


def re_review_set(
    corrected: Node,
    dependencies: Mapping[Node, Iterable[Node]],
    record: Mapping[str, Any],
) -> Record:
    """Dependent decisions a correction sends back for human re-review, and nothing else.

    Unrelated nodes are untouched. The review of each record version at or before the corrected
    nomination version is listed for re-review. Acceptance and sanction stay off.
    """
    register = ChallengeRegister(dependencies=dependencies)
    cutoff = _nomination_version_cutoff(corrected)
    raw_reviews = record.get("reviews")
    reviews: Iterable[Any] = (
        raw_reviews
        if isinstance(raw_reviews, Iterable) and not isinstance(raw_reviews, (str, bytes))
        else ()
    )
    versions: list[int] = []
    for rev in reviews:
        if not isinstance(rev, Mapping):
            continue
        rv = rev.get("record_version")
        if isinstance(rv, int) and not isinstance(rv, bool) and (cutoff is None or rv <= cutoff):
            versions.append(rv)
    return {
        "corrected": corrected,
        "dependents": register.dependents(corrected),
        "review_versions": versions,
        "dependent_review_versions": list(versions),
        "required": True,
        "automatic_acceptance": False,
        "automatic_sanction": False,
        "priority_changed": False,
        "consent_changed": False,
    }
