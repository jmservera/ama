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
