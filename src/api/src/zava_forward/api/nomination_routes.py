"""HTTP boundary helpers and accessible HTML route views for referral and challenge routes."""

from __future__ import annotations

import html
from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from zava_forward.core import nomination_route, projection, resident_decisions

NOMINATION_ROUTE_ACTIONS: frozenset[str] = frozenset(
    {
        "nomination_record",
        "nomination_acknowledge",
        "nomination_correct",
        "challenge_open",
    }
)

NOMINATION_CASE_KEYS: tuple[str, ...] = (
    "nomination_records",
    "affected_challenges",
    "challenge_targets",
    "challenge_guarantees",
    "challenge_assurance",
    "nomination_permissions",
)

_REQUIRED_FIELDS: dict[str, frozenset[str]] = {
    "nomination_record": frozenset(
        {
            "action",
            "case_id",
            "kind",
            "reported_subject_ref",
            "account",
            "source",
            "channel",
            "owner",
            "acknowledgement_ref",
            "next_update",
            "non_digital_route",
            "hazard_concern",
        }
    ),
    "nomination_acknowledge": frozenset(
        {
            "action",
            "case_id",
            "id",
            "expected_version",
            "owner",
            "acknowledgement_ref",
            "non_digital_route",
            "next_update",
        }
    ),
    "nomination_correct": frozenset(
        {
            "action",
            "case_id",
            "id",
            "expected_version",
            "reported_subject_ref",
            "account",
            "source",
            "channel",
            "next_update",
            "challenge_id",
        }
    ),
    "challenge_open": frozenset(
        {
            "action",
            "proposal_id",
            "proposal_version",
            "decision_version",
            "target_kind",
            "channel",
            "source",
            "request",
            "explanation",
            "owner",
            "non_digital_route",
            "next_update",
        }
    ),
}

_OPTIONAL_FIELDS: dict[str, frozenset[str]] = {
    "nomination_record": frozenset({"assisted_channel"}),
    "nomination_acknowledge": frozenset(
        {"hazard_concern", "channel", "assisted_channel", "owner_reassignment_reason"}
    ),
    "nomination_correct": frozenset(
        {"hazard_concern", "raised_by", "representative_ref", "dependencies", "assisted_channel"}
    ),
    "challenge_open": frozenset(
        {"hazard_concern", "raised_by", "representative_ref", "assisted_channel"}
    ),
}


def nomination_routes_visible(user: Mapping[str, Any] | None) -> bool:
    """Return True when the authenticated viewer may inspect referral and challenge routes."""
    if user is None:
        return False
    return bool(projection.appointment_evidence_visible(dict(user)))


def build_route_action_payload(
    action: str,
    body: Mapping[str, Any],
    *,
    user: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate role, field permissions, and dual-route channel arguments before write dispatch."""
    if action not in NOMINATION_ROUTE_ACTIONS:
        raise ValueError(f"Unsupported referral or challenge route action: {action!r}.")
    if not nomination_routes_visible(user):
        raise PermissionError(
            "Referral and challenge route writes need current resident-workflow and "
            "recorded-reason rights."
        )
    allowed_keys = _REQUIRED_FIELDS[action] | _OPTIONAL_FIELDS[action]
    extra_keys = sorted(set(body) - allowed_keys)
    if extra_keys:
        raise ValueError(
            "Supply only permitted route fields. Server-derived and unpermitted fields are not "
            f"accepted: {', '.join(extra_keys)}."
        )
    missing_keys = sorted(_REQUIRED_FIELDS[action] - set(body))
    if missing_keys:
        raise ValueError(f"Supply every required route field: {', '.join(missing_keys)}.")
    if (
        action == "nomination_acknowledge"
        and user.get("role") not in resident_decisions.MANAGERS
        and body.get("owner_reassignment_reason") not in (None, "")
    ):
        raise PermissionError(
            "Only a resident-workflow manager can record an owner reassignment reason."
        )
    payload = deepcopy(dict(body))
    if "channel" in payload:
        nomination_route.normalize_route_channel(
            payload["channel"],
            assisted_channel=payload.get("assisted_channel"),
            allow_intermediary=(action != "challenge_open"),
            label=(
                "the supplied challenge channel"
                if action == "challenge_open"
                else "the acknowledgement channel"
                if action == "nomination_acknowledge"
                else "the supplied channel"
            ),
        )
    elif payload.get("assisted_channel") not in (None, ""):
        raise ValueError(
            "Assisted non-digital channel applies only when channel is staff_recorded_non_digital."
        )
    return payload


def _filter_explanation_node(
    node: dict[str, Any],
    *,
    can_view_intake: bool,
    can_view_reason: bool,
) -> None:
    raw = node.get("plain_language_explanation")
    if isinstance(raw, Mapping):
        filtered = nomination_route.filter_explanation_for_viewer(
            raw,
            can_view_intake=can_view_intake,
            can_view_reason=can_view_reason,
        )
        if filtered is None:
            node.pop("plain_language_explanation", None)
        else:
            node["plain_language_explanation"] = filtered


def project_case_nomination_routes(
    detail: dict[str, Any],
    *,
    user: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Scrub restricted vulnerability fields and enforce viewer visibility on route payloads."""
    out = dict(detail)
    if user is not None and not nomination_routes_visible(user):
        for key in NOMINATION_CASE_KEYS:
            out.pop(key, None)
        return out
    can_view_intake = True
    can_view_reason = True if user is None else bool(projection.can_see_reason(dict(user)))
    for list_key in ("nomination_records", "affected_challenges", "challenge_targets"):
        items = out.get(list_key)
        if not isinstance(items, list):
            continue
        scrubbed = nomination_route.scrub_nomination_restricted_fields(items)
        for item in scrubbed:
            if not isinstance(item, dict):
                continue
            _filter_explanation_node(
                item,
                can_view_intake=can_view_intake,
                can_view_reason=can_view_reason,
            )
            follow_up = item.get("follow_up")
            if isinstance(follow_up, dict):
                _filter_explanation_node(
                    follow_up,
                    can_view_intake=can_view_intake,
                    can_view_reason=can_view_reason,
                )
        out[list_key] = scrubbed
    return out


def _esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _render_explanation_block(expl: Mapping[str, Any] | None, heading: str) -> str:
    if not isinstance(expl, Mapping) or expl.get("permitted") is not True:
        return ""
    sources = [str(s) for s in expl.get("sources") or () if isinstance(s, str) and s.strip()]
    reasons = [str(r) for r in expl.get("policy_reasons") or () if isinstance(r, str) and r.strip()]
    source_items = "".join(f"<li>{_esc(item)}</li>" for item in sources) or "<li>Unknown</li>"
    reason_items = "".join(f"<li>{_esc(item)}</li>" for item in reasons) or "<li>Unknown</li>"
    return (
        '<section class="plain-language-explanation" '
        f'aria-label="{_esc(heading)}">'
        f"<h4>{_esc(heading)}</h4>"
        "<dl>"
        f"<dt>Human decision owner</dt><dd>{_esc(expl.get('human_decision_owner'))}</dd>"
        f"<dt>AI involvement</dt><dd>{_esc(expl.get('ai_involvement_explanation'))}</dd>"
        f"<dt>Uncertainty and unverified items</dt><dd>{_esc(expl.get('uncertainty_note'))}</dd>"
        "</dl>"
        f"<h5>Sources recorded</h5><ul>{source_items}</ul>"
        f"<h5>Policy reasons</h5><ul>{reason_items}</ul>"
        "</section>"
    )


def _render_owner_options(
    owners: list[Mapping[str, Any]],
    selected_email: str | None = None,
) -> str:
    opts = ['<option value="">Select named owner</option>']
    for person in owners:
        email = str(person.get("email") or "")
        if not email:
            continue
        label = f"{person.get('name') or email} ({person.get('role') or 'Staff'})"
        sel = " selected" if selected_email and email == selected_email else ""
        opts.append(f'<option value="{_esc(email)}"{sel}>{_esc(label)}</option>')
    return "".join(opts)


def render_accessible_nomination_route_html(
    detail: Mapping[str, Any],
    *,
    user: Mapping[str, Any],
) -> str:
    """Render an accessible, keyboard-operable HTML view for digital and non-digital routes."""
    if not nomination_routes_visible(user):
        raise PermissionError(
            "Your role does not include referral, acknowledgement, and challenge routes."
        )
    projected = project_case_nomination_routes(deepcopy(dict(detail)), user=user)
    case_id = str(projected.get("id") or "")
    perms = projected.get("nomination_permissions")
    perm_map: Mapping[str, Any] = perms if isinstance(perms, Mapping) else {}
    can_write = bool(perm_map.get("can_write"))
    can_reassign = bool(perm_map.get("can_reassign_owner"))
    ack_ids = set(perm_map.get("acknowledgeable_nomination_ids") or ())
    corr_ids = set(perm_map.get("correctable_nomination_ids") or ())
    staff_owners = [p for p in (perm_map.get("staff_owners") or ()) if isinstance(p, Mapping)]
    rep_refs = [
        str(r)
        for r in (perm_map.get("representative_authorities") or ())
        if isinstance(r, str) and r.strip()
    ]
    records = [r for r in (projected.get("nomination_records") or ()) if isinstance(r, Mapping)]
    targets = [t for t in (projected.get("challenge_targets") or ()) if isinstance(t, Mapping)]
    challenges = [
        ch for ch in (projected.get("affected_challenges") or ()) if isinstance(ch, Mapping)
    ]

    nomination_blocks: list[str] = []
    for rec in records:
        rec_id = str(rec.get("id") or "")
        version = int(rec.get("version") or 1)
        owner_raw = rec.get("owner")
        owner: Mapping[str, Any] = owner_raw if isinstance(owner_raw, Mapping) else {}
        owner_email = str(owner.get("email") or user.get("email") or "")
        expl_raw = rec.get("plain_language_explanation")
        expl = expl_raw if isinstance(expl_raw, Mapping) else None
        forms_html = ""
        if can_write and rec_id in ack_ids:
            ack_key = f"nomination-ack-{_esc(rec_id)}"
            reassign_field = (
                f'<label for="{ack_key}-owner_reassignment_reason">'
                "Owner reassignment reason (optional)</label>"
                f'<input id="{ack_key}-owner_reassignment_reason" '
                'name="owner_reassignment_reason" type="text" maxlength="500" '
                f'aria-describedby="{ack_key}-feedback">'
                if can_reassign
                else ""
            )
            forms_html += (
                f"<details><summary>Record acknowledgement for {_esc(rec_id)}</summary>"
                f'<form id="{ack_key}" method="post" '
                f'action="/api/cases/{_esc(case_id)}/resident" novalidate>'
                '<input type="hidden" name="action" value="nomination_acknowledge">'
                f'<input type="hidden" name="case_id" value="{_esc(case_id)}">'
                f'<input type="hidden" name="id" value="{_esc(rec_id)}">'
                f'<input type="hidden" name="expected_version" value="{version}">'
                f'<label for="{ack_key}-channel">Intake route</label>'
                f'<select id="{ack_key}-channel" name="channel" '
                f'aria-describedby="{ack_key}-feedback">'
                '<option value="digital">Digital route</option>'
                '<option value="staff_recorded_non_digital">'
                "Staff-recorded non-digital route</option>"
                "</select>"
                f'<label for="{ack_key}-assisted_channel">'
                "Assisted non-digital medium (when staff-recorded non-digital)</label>"
                f'<select id="{ack_key}-assisted_channel" name="assisted_channel" '
                f'aria-describedby="{ack_key}-feedback">'
                '<option value="">Not applicable (digital)</option>'
                '<option value="phone">Phone</option>'
                '<option value="paper">Paper</option>'
                '<option value="letter">Letter</option>'
                '<option value="in_person">In person</option>'
                '<option value="trusted_intermediary">Trusted intermediary</option>'
                "</select>"
                f'<label for="{ack_key}-owner">Named follow-up owner</label>'
                f'<select id="{ack_key}-owner" name="owner" '
                f'aria-describedby="{ack_key}-feedback">'
                f"{_render_owner_options(staff_owners, owner_email)}"
                "</select>"
                f"{reassign_field}"
                f'<label for="{ack_key}-acknowledgement_ref">'
                "Acknowledgement evidence reference</label>"
                f'<input id="{ack_key}-acknowledgement_ref" name="acknowledgement_ref" '
                f'type="text" maxlength="500" aria-describedby="{ack_key}-feedback">'
                f'<label for="{ack_key}-non_digital_route">'
                "Staffed phone, paper, letter or in-person contact route</label>"
                f'<input id="{ack_key}-non_digital_route" name="non_digital_route" '
                f'type="text" maxlength="500" value="{_esc(rec.get("non_digital_route"))}" '
                f'aria-describedby="{ack_key}-feedback">'
                f'<label for="{ack_key}-next_update">Next update date</label>'
                f'<input id="{ack_key}-next_update" name="next_update" type="date" '
                f'value="{_esc(rec.get("next_update"))}" aria-describedby="{ack_key}-feedback">'
                f'<p id="{ack_key}-feedback" role="status" aria-live="polite" tabindex="-1"></p>'
                '<button type="submit">Record acknowledgement</button>'
                "</form></details>"
            )
        if can_write and rec_id in corr_ids:
            corr_key = f"nomination-correct-{_esc(rec_id)}"
            rep_opts = "".join(
                f'<option value="{_esc(ref)}">{_esc(ref)}</option>' for ref in rep_refs
            )
            forms_html += (
                f"<details><summary>Record correction for {_esc(rec_id)}</summary>"
                f'<form id="{corr_key}" method="post" '
                f'action="/api/cases/{_esc(case_id)}/resident" novalidate>'
                '<input type="hidden" name="action" value="nomination_correct">'
                f'<input type="hidden" name="case_id" value="{_esc(case_id)}">'
                f'<input type="hidden" name="id" value="{_esc(rec_id)}">'
                f'<input type="hidden" name="expected_version" value="{version}">'
                f'<label for="{corr_key}-channel">Correction intake route</label>'
                f'<select id="{corr_key}-channel" name="channel" '
                f'aria-describedby="{corr_key}-feedback">'
                '<option value="digital">Digital route</option>'
                '<option value="staff_recorded_non_digital">'
                "Staff-recorded non-digital route</option>"
                "</select>"
                f'<label for="{corr_key}-assisted_channel">'
                "Assisted non-digital medium (when staff-recorded non-digital)</label>"
                f'<select id="{corr_key}-assisted_channel" name="assisted_channel" '
                f'aria-describedby="{corr_key}-feedback">'
                '<option value="">Not applicable (digital)</option>'
                '<option value="phone">Phone</option>'
                '<option value="paper">Paper</option>'
                '<option value="letter">Letter</option>'
                '<option value="in_person">In person</option>'
                '<option value="trusted_intermediary">Trusted intermediary</option>'
                "</select>"
                f'<label for="{corr_key}-raised_by">Who supplied the correction</label>'
                f'<select id="{corr_key}-raised_by" name="raised_by" '
                f'aria-describedby="{corr_key}-feedback">'
                '<option value="Resident">Resident</option>'
                '<option value="Officer">Officer</option>'
                + ('<option value="Representative">Representative</option>' if rep_refs else "")
                + "</select>"
                f'<label for="{corr_key}-representative_ref">'
                "Confirmed representative reference (when raised by representative)</label>"
                f'<select id="{corr_key}-representative_ref" name="representative_ref" '
                f'aria-describedby="{corr_key}-feedback">'
                '<option value="">Not applicable</option>'
                f"{rep_opts}"
                "</select>"
                f'<label for="{corr_key}-reported_subject_ref">'
                "Corrected unverified subject reference</label>"
                f'<input id="{corr_key}-reported_subject_ref" name="reported_subject_ref" '
                f'type="text" maxlength="100" aria-describedby="{corr_key}-feedback">'
                f'<label for="{corr_key}-account">Competing corrected account</label>'
                f'<textarea id="{corr_key}-account" name="account" maxlength="4000" '
                f'aria-describedby="{corr_key}-feedback"></textarea>'
                f'<label for="{corr_key}-source">Correction evidence reference</label>'
                f'<input id="{corr_key}-source" name="source" type="text" maxlength="500" '
                f'aria-describedby="{corr_key}-feedback">'
                f'<label for="{corr_key}-next_update">Next update date</label>'
                f'<input id="{corr_key}-next_update" name="next_update" type="date" '
                f'aria-describedby="{corr_key}-feedback">'
                f'<p id="{corr_key}-feedback" role="status" aria-live="polite" tabindex="-1"></p>'
                '<button type="submit">Record competing correction</button>'
                "</form></details>"
            )
        nomination_blocks.append(
            f'<article id="nomination-{_esc(rec_id)}">'
            f"<h3>{_esc(rec.get('kind') or 'Referral')} {_esc(rec_id)} (version {version})</h3>"
            f"{_render_explanation_block(expl, f'How decisions and AI apply to {rec_id}')}"
            f"{forms_html}"
            "</article>"
        )

    challenge_target_blocks = [
        f'<article id="target-{_esc(t.get("proposal_id"))}">'
        f"<h3>Suggestion {_esc(t.get('proposal_id'))}</h3>"
        + _render_explanation_block(
            t.get("plain_language_explanation")
            if isinstance(t.get("plain_language_explanation"), Mapping)
            else None,
            f"How AI and policy rules apply to suggestion {t.get('proposal_id')}",
        )
        + "</article>"
        for t in targets
    ]

    challenge_record_blocks = [
        f'<article id="challenge-{_esc(ch.get("id"))}">'
        f"<h3>Challenge {_esc(ch.get('id'))} ({_esc(ch.get('status'))})</h3>"
        + _render_explanation_block(
            ch.get("plain_language_explanation")
            if isinstance(ch.get("plain_language_explanation"), Mapping)
            else None,
            f"How AI and human ownership apply to challenge {ch.get('id')}",
        )
        + "</article>"
        for ch in challenges
    ]

    challenge_form_html = ""
    if can_write and targets:
        ch_key = "challenge-open-route"
        target_opts = "".join(
            f'<option value="{_esc(t.get("proposal_id"))}" '
            f'data-proposal-version="{_esc(t.get("proposal_version"))}" '
            f'data-decision-version="{_esc(t.get("decision_version"))}">'
            f"{_esc(t.get('proposal_id'))}</option>"
            for t in targets
        )
        rep_opts = "".join(f'<option value="{_esc(ref)}">{_esc(ref)}</option>' for ref in rep_refs)
        challenge_form_html = (
            f"<details><summary>Record supplied challenge</summary>"
            f'<form id="{ch_key}" method="post" '
            f'action="/api/cases/{_esc(case_id)}/resident" novalidate>'
            '<input type="hidden" name="action" value="challenge_open">'
            f'<label for="{ch_key}-proposal_id">Suggestion reference</label>'
            f'<select id="{ch_key}-proposal_id" name="proposal_id" '
            f'aria-describedby="{ch_key}-feedback">{target_opts}</select>'
            f'<label for="{ch_key}-target_kind">Challenged information</label>'
            f'<select id="{ch_key}-target_kind" name="target_kind" '
            f'aria-describedby="{ch_key}-feedback">'
            '<option value="proposal">proposal</option>'
            '<option value="source">source</option>'
            '<option value="policy">policy</option>'
            "</select>"
            f'<label for="{ch_key}-channel">Challenge intake route</label>'
            f'<select id="{ch_key}-channel" name="channel" '
            f'aria-describedby="{ch_key}-feedback">'
            '<option value="digital">Digital route</option>'
            '<option value="staff_recorded_non_digital">'
            "Staff-recorded non-digital route</option>"
            "</select>"
            f'<label for="{ch_key}-assisted_channel">'
            "Assisted non-digital medium (when staff-recorded non-digital)</label>"
            f'<select id="{ch_key}-assisted_channel" name="assisted_channel" '
            f'aria-describedby="{ch_key}-feedback">'
            '<option value="">Not applicable (digital)</option>'
            '<option value="phone">Phone</option>'
            '<option value="paper">Paper</option>'
            '<option value="letter">Letter</option>'
            '<option value="in_person">In person</option>'
            "</select>"
            f'<label for="{ch_key}-raised_by">Who raised the challenge</label>'
            f'<select id="{ch_key}-raised_by" name="raised_by" '
            f'aria-describedby="{ch_key}-feedback">'
            '<option value="Resident">Resident</option>'
            '<option value="Officer">Officer</option>'
            + ('<option value="Representative">Representative</option>' if rep_refs else "")
            + "</select>"
            f'<label for="{ch_key}-representative_ref">'
            "Confirmed representative reference (when raised by representative)</label>"
            f'<select id="{ch_key}-representative_ref" name="representative_ref" '
            f'aria-describedby="{ch_key}-feedback">'
            '<option value="">Not applicable</option>'
            f"{rep_opts}"
            "</select>"
            f'<label for="{ch_key}-source">Challenge evidence reference</label>'
            f'<input id="{ch_key}-source" name="source" type="text" maxlength="300" '
            f'aria-describedby="{ch_key}-feedback">'
            f'<label for="{ch_key}-request">Supplied challenge request</label>'
            f'<input id="{ch_key}-request" name="request" type="text" maxlength="300" '
            f'aria-describedby="{ch_key}-feedback">'
            f'<label for="{ch_key}-explanation">Permitted plain-language explanation</label>'
            f'<input id="{ch_key}-explanation" name="explanation" type="text" maxlength="300" '
            f'aria-describedby="{ch_key}-feedback">'
            f'<label for="{ch_key}-owner">Named challenge owner</label>'
            f'<select id="{ch_key}-owner" name="owner" aria-describedby="{ch_key}-feedback">'
            f"{_render_owner_options(staff_owners, str(user.get('email') or ''))}"
            "</select>"
            f'<label for="{ch_key}-non_digital_route">'
            "Accessible phone, paper, letter or in-person route</label>"
            f'<input id="{ch_key}-non_digital_route" name="non_digital_route" type="text" '
            f'maxlength="300" aria-describedby="{ch_key}-feedback">'
            f'<label for="{ch_key}-next_update">Challenge next update date</label>'
            f'<input id="{ch_key}-next_update" name="next_update" type="date" '
            f'aria-describedby="{ch_key}-feedback">'
            f'<p id="{ch_key}-feedback" role="status" aria-live="polite" tabindex="-1"></p>'
            '<button type="submit">Record supplied challenge</button>'
            "</form></details>"
        )

    return (
        "<!doctype html>"
        '<html lang="en-GB"><head><meta charset="utf-8">'
        f"<title>Referral and challenge routes for {_esc(case_id)}</title></head>"
        "<body><main>"
        f"<h1>Referral, acknowledgement, and challenge routes ({_esc(case_id)})</h1>"
        "<p>Urgent hazards use the hazard reporting route immediately and are never queued here. "
        "A named person owns every review and response.</p>"
        '<section id="nominations-html" aria-labelledby="nominations-html-title">'
        '<h2 id="nominations-html-title">Referrals and self-referrals</h2>'
        + ("".join(nomination_blocks) or "<p>No referrals recorded.</p>")
        + "</section>"
        '<section id="challenges-html" aria-labelledby="challenges-html-title">'
        '<h2 id="challenges-html-title">Priority suggestions and challenges</h2>'
        + "".join(challenge_target_blocks)
        + challenge_form_html
        + ("".join(challenge_record_blocks) or "<p>No challenges recorded.</p>")
        + "</section>"
        '</main><script src="/nomination-routes.js" defer></script></body></html>'
    )
