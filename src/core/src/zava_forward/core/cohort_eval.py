"""Pure cohort and missing-data evaluation record (FR-054, AC-073); no store or clock access.

Constructed cohorts are compared with an approved expected-outcome manifest. Results are reported
per cohort and never averaged. Synthetic results are never fairness evidence (OQ-018).
"""

from __future__ import annotations

import copy
import math
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from typing import Any

from zava_forward.core.rai_release import digest, named, named_human

RECORD_VERSION = "cohort-missing-data-evaluation-v1"
OUTCOMES = ("ranked", "deprioritised", "excluded", "review")
THRESHOLD_KEYS = ("min_sample", "max_error_rate", "max_exclusion_gap", "max_review_burden_gap")
OWNER_KEYS = ("cohorts_owner", "lawful_fields_owner", "thresholds_owner")
OWNER_APPROVAL_APPROVED = "approved"
OWNER_APPROVAL_PENDING = "pending_owner_approval"
OWNER_APPROVAL_UNAPPROVED = "unapproved"
FICTIONAL_OWNER_TOKENS = frozenset(
    {
        "fictional",
        "placeholder",
        "mock",
        "synthetic",
        "example",
        "todo",
        "tbd",
        "unapproved",
        "unknown",
    }
)
DISPOSABLE = {"seeded_defect_unexpected", "threshold_exceeded", "unjustified_exclusion"}
MEASUREMENT_BLOCKERS = {
    "invalid_input",
    "reconciliation",
    "insufficient_sample",
    "unapproved_lawful_analysis_fields",
}
OQ_018_GAP = (
    "OQ-018: representative cohorts, lawful analysis fields, sample sufficiency and thresholds "
    "need owner approval before live use; synthetic results are not fairness evidence."
)
SYNTHETIC_NON_FAIRNESS_NOTICE = (
    "Synthetic cohort evaluation results are constructed offline checks only and are never "
    "fairness evidence or live fairness clearance; live prioritisation requires dated human "
    "owner approval of cohorts, lawful analysis fields and thresholds (OQ-018)."
)
UNAPPROVED_NON_FAIRNESS_NOTICE = (
    "Pending or unapproved cohort evaluation results are not live fairness clearance; live "
    "prioritisation requires dated human owner approval of cohorts, lawful analysis fields and "
    "thresholds, and synthetic results are never fairness evidence (OQ-018)."
)
APPROVED_PROVENANCE_NOTICE = (
    "Dated human owner approval recorded for cohorts, lawful analysis fields and thresholds "
    "(OQ-018); synthetic results remain excluded as fairness evidence."
)


def wilson(errors: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """95% Wilson interval for an error rate, or None when there is no sample."""
    if n <= 0:
        return None
    p = errors / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)


def _rate(count: int, n: int) -> float | None:
    return round(count / n, 4) if n else None


def _finite_number(value: object) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and math.isfinite(value)


def _limit(value: Any) -> bool:
    return _finite_number(value) and 0 <= float(value) <= 1


def _real_human_owner(value: object) -> bool:
    if not named_human(value) or not isinstance(value, str):
        return False
    tokens = {tok for tok in re.split(r"[^a-z0-9]+", value.lower()) if tok}
    return tokens.isdisjoint(FICTIONAL_OWNER_TOKENS)


def _valid_lawful_fields(manifest: Mapping[str, Any]) -> tuple[list[str], bool]:
    if "lawful_analysis_fields" in manifest:
        raw = manifest.get("lawful_analysis_fields")
        if (
            isinstance(raw, Sequence)
            and not isinstance(raw, str | bytes | bytearray)
            and len(raw) > 0
            and all(named(item) for item in raw)
        ):
            return [str(item).strip() for item in raw], True
        return [], False
    cohorts = manifest.get("cohorts")
    if isinstance(cohorts, Mapping) and len(cohorts) > 0 and all(named(k) for k in cohorts):
        return [str(k).strip() for k in cohorts], True
    return [], False


def _valid_approval_stamp(value: object, now: float | None) -> bool:
    if _finite_number(value):
        assert isinstance(value, int | float)
        stamp = float(value)
        if stamp <= 0:
            return False
        if _finite_number(now):
            assert isinstance(now, int | float)
            return stamp <= float(now)
        return True
    if isinstance(value, str):
        text = value.strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}($|[T ])", text):
            return False
        if len(text) == 10:
            try:
                date.fromisoformat(text)
                return True
            except ValueError:
                return False
        iso = text[:-1] + "+00:00" if text.endswith("Z") else text
        try:
            datetime.fromisoformat(iso)
            return True
        except ValueError:
            return False
    return False


def _date_key_gaps(approval: Mapping[str, Any], now: float | None) -> list[tuple[str, str]]:
    gaps: list[tuple[str, str]] = []
    has_expires = "expires" in approval
    has_stamp = "approved_at" in approval or "approved_on" in approval
    if has_expires:
        expires = approval.get("expires")
        if not _finite_number(now) or not _finite_number(expires):
            gaps.append(
                ("live_approval_expired", "live approval is missing, expired or unverifiable")
            )
        else:
            assert isinstance(now, int | float)
            assert isinstance(expires, int | float)
            if float(expires) <= float(now):
                gaps.append(
                    ("live_approval_expired", "live approval is missing, expired or unverifiable")
                )
    if has_stamp:
        stamps_ok = all(
            _valid_approval_stamp(approval.get(k), now)
            for k in ("approved_at", "approved_on")
            if k in approval
        )
        if not stamps_ok:
            gaps.append(
                ("live_approval_undated", "live owner approval needs a valid approval date")
            )
    if not has_expires and not has_stamp:
        gaps.append(("live_approval_undated", "live owner approval needs a dated approval record"))
    return gaps


def _has_invalid_or_expired_date(approval: Mapping[str, Any], now: float | None) -> bool:
    if any(
        not _valid_approval_stamp(approval.get(k), now)
        for k in ("approved_at", "approved_on")
        if k in approval
    ):
        return True
    if "expires" in approval:
        expires = approval.get("expires")
        if not _finite_number(expires):
            return True
        if _finite_number(now):
            assert isinstance(expires, int | float)
            assert isinstance(now, int | float)
            if float(expires) <= float(now):
                return True
    return False


def manifest_digest(manifest: Mapping[str, Any]) -> str:
    """Digest of the manifest content an owner approves, excluding the approval block itself."""
    return digest({k: v for k, v in manifest.items() if k != "approval"})


def approve(manifest: dict[str, Any], approval: Mapping[str, Any]) -> dict[str, Any]:
    """Record named owner approval bound to the manifest content; a later change voids it."""
    manifest["approval"] = {**approval, "manifest_digest": manifest_digest(manifest)}
    return manifest


def _approval_bound(manifest: Mapping[str, Any]) -> bool:
    approval = manifest.get("approval")
    return isinstance(approval, Mapping) and approval.get("manifest_digest") == manifest_digest(
        manifest
    )


def _thresholds_approved(manifest: Mapping[str, Any]) -> bool:
    approval = manifest.get("approval")
    thresholds = manifest.get("thresholds")
    if not (
        isinstance(approval, Mapping)
        and all(named(approval.get(k)) for k in OWNER_KEYS)
        and _approval_bound(manifest)
        and isinstance(thresholds, Mapping)
    ):
        return False
    sample = thresholds.get("min_sample")
    return (
        isinstance(sample, int)
        and not isinstance(sample, bool)
        and sample > 0
        and all(_limit(thresholds.get(k)) for k in THRESHOLD_KEYS[1:])
    )


def _owner_approval_status(
    manifest: Mapping[str, Any], fields_valid: bool, now: float | None
) -> str:
    synthetic = manifest.get("synthetic") is not False
    approval = manifest.get("approval")
    if not isinstance(approval, Mapping) or not _thresholds_approved(manifest) or not fields_valid:
        return OWNER_APPROVAL_UNAPPROVED
    if not all(named_human(approval.get(k)) for k in OWNER_KEYS):
        return OWNER_APPROVAL_UNAPPROVED
    if _has_invalid_or_expired_date(approval, now):
        return OWNER_APPROVAL_UNAPPROVED
    if (
        not synthetic
        and all(_real_human_owner(approval.get(k)) for k in OWNER_KEYS)
        and not _date_key_gaps(approval, now)
    ):
        return OWNER_APPROVAL_APPROVED
    return OWNER_APPROVAL_PENDING


def _live_gaps(manifest: Mapping[str, Any], now: float | None) -> list[tuple[str, str]]:
    gaps: list[tuple[str, str]] = []
    if manifest.get("synthetic") is not False:
        gaps.append(
            ("constructed_thresholds_live", "constructed thresholds support offline tests only")
        )
    _, fields_valid = _valid_lawful_fields(manifest)
    if not fields_valid:
        gaps.append(
            (
                "unapproved_lawful_analysis_fields",
                "lawful analysis fields must be non-empty owner-approved field names",
            )
        )
    approval = manifest.get("approval")
    approval = approval if isinstance(approval, Mapping) else {}
    if not all(_real_human_owner(approval.get(k)) for k in OWNER_KEYS):
        gaps.append(("live_approval_not_named_human", "live thresholds need named-human owners"))
    gaps.extend(_date_key_gaps(approval, now))
    return gaps


def _cohort_row(cases: Sequence[Mapping[str, Any]], min_sample: int) -> dict[str, Any]:
    missing = sum(1 for c in cases if c["actual"] is None)
    cases = [c for c in cases if c["actual"] is not None]
    n = len(cases)
    errors = sum(1 for c in cases if c["actual"] != c.get("expected"))
    excluded = sum(1 for c in cases if c["actual"] == "excluded")
    deprioritised = sum(1 for c in cases if c["actual"] == "deprioritised")
    review = sum(1 for c in cases if c["review"])
    return {
        "n": n,
        "missing": missing,
        "errors": errors,
        "excluded": excluded,
        "deprioritised": deprioritised,
        "review": review,
        "defects": sum(1 for c in cases if c["defect"]),
        "error_rate": _rate(errors, n),
        "exclusion_rate": _rate(excluded + deprioritised, n),
        "review_burden": _rate(review, n),
        "_raw": {
            "error_rate": errors / n if n else None,
            "exclusion_rate": (excluded + deprioritised) / n if n else None,
            "review_burden": review / n if n else None,
        },
        "error_interval": wilson(errors, n),
        "sufficient": n >= min_sample > 0,
    }


def _gap(rows: Mapping[str, Mapping[str, Any]], key: str) -> float | None:
    values = [r["_raw"][key] for r in rows.values() if r["sufficient"] and r[key] is not None]
    return max(values) - min(values) if len(values) >= 2 else None


def evaluate(
    manifest: Mapping[str, Any],
    observed: Sequence[Mapping[str, Any]],
    disposition: Mapping[str, Any] | None = None,
    *,
    live: bool = False,
    now: float | None = None,
) -> dict[str, Any]:
    """Build the versioned evaluation record for one task or policy version.

    Offline use (the default) accepts constructed thresholds. With `live=True` the thresholds must
    come from a non-synthetic manifest whose owners are named humans and whose approval carries an
    unexpired `expires` epoch later than the caller-supplied `now`.
    """
    blockers: list[dict[str, str]] = []

    def block(code: str, detail: str) -> None:
        blockers.append({"code": code, "detail": detail})

    cases = list(manifest.get("cases", []))
    declared: Mapping[str, Sequence[str]] = manifest.get("cohorts", {})
    thresholds: Mapping[str, Any] = manifest.get("thresholds", {})
    approval = manifest.get("approval")
    justified = set(manifest.get("justified_reasons", []))
    obs_ids = [o.get("id") for o in observed]
    case_ids = [c.get("id") for c in cases]

    def valid_id(value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())

    for label, ids in (("observed", obs_ids), ("manifest", case_ids)):
        if not all(valid_id(i) for i in ids):
            block("invalid_input", f"{label} case id is missing or not a non-empty string")
    obs_ids = [i for i in obs_ids if valid_id(i)]
    case_ids = [i for i in case_ids if valid_id(i)]
    for label, ids in (("observed", obs_ids), ("manifest", case_ids)):
        freq = Counter(ids)
        for dup in sorted(str(i) for i, count in freq.items() if count > 1):
            block("invalid_input", f"duplicate {label} case id {dup}")
    for field in ("task_id", "subject_version", "missing_data_treatment"):
        value = manifest.get(field)
        if not (isinstance(value, str) and value.strip()):
            block("invalid_input", f"manifest {field} is missing")
    for c in cases:
        if c.get("expected") not in OUTCOMES:
            block(
                "invalid_input", f"manifest case {c.get('id')} has missing or unsupported expected"
            )
    seen = {o.get("id"): o for o in observed if valid_id(o.get("id"))}
    manifest_ids = set(case_ids)

    for extra in sorted(str(i) for i in set(seen) - manifest_ids):
        block("reconciliation", f"observed case {extra} is not in the manifest")
    for miss in sorted(manifest_ids - set(seen)):
        block("reconciliation", f"manifest case {miss} has no observed outcome")

    joined: list[dict[str, Any]] = []
    for c in cases:
        obs = seen.get(c.get("id"), {}) if valid_id(c.get("id")) else {}
        actual = obs.get("outcome") if obs else None
        if obs and actual not in OUTCOMES:
            block("invalid_input", f"observed case {c['id']} has missing or unsupported outcome")
            actual = None
        defect = (
            actual in ("excluded", "deprioritised")
            and actual != c.get("expected")
            and obs.get("reason") not in justified
        )
        cohort_map = c.get("cohorts")
        if not isinstance(cohort_map, Mapping):
            block("invalid_input", f"manifest case {c.get('id')} has no cohorts mapping")
            cohort_map = {}
        needs_review = actual == "review" or (
            obs.get("review_required") is True and actual is not None
        )
        joined.append(
            {**c, "cohorts": cohort_map, "actual": actual, "defect": defect, "review": needs_review}
        )

    min_sample = int(thresholds.get("min_sample", 0)) if _thresholds_approved(manifest) else 0
    dimensions: dict[str, Any] = {}
    if not declared or not cases or any(not labels for labels in declared.values()):
        block("insufficient_sample", "no cohort dimensions, labels or cases to evaluate")
    for dim, labels in declared.items():
        rows = {
            label: _cohort_row([c for c in joined if c["cohorts"].get(dim) == label], min_sample)
            for label in labels
        }
        total = sum(r["n"] + r["missing"] for r in rows.values())
        in_dim = sum(1 for c in joined if c["cohorts"].get(dim) in labels)
        if total != in_dim or total != len(joined):
            block(
                "reconciliation", f"{dim}: cohort counts {total} do not reconcile to {len(joined)}"
            )
        gaps = {
            "exclusion": _gap(rows, "exclusion_rate"),
            "review_burden": _gap(rows, "review_burden"),
        }
        raw = {label: row.pop("_raw") for label, row in rows.items()}
        dimensions[dim] = {
            "cohorts": rows,
            "gaps": {k: None if v is None else round(v, 4) for k, v in gaps.items()},
        }
        for label, row in rows.items():
            if not row["sufficient"]:
                block("insufficient_sample", f"{dim}/{label}: n={row['n']} below minimum sample")
            elif _thresholds_approved(manifest):
                if raw[label]["error_rate"] > thresholds["max_error_rate"]:
                    block("threshold_exceeded", f"{dim}/{label}: error rate {row['error_rate']}")
        if _thresholds_approved(manifest):
            for name, limit in (
                ("exclusion", "max_exclusion_gap"),
                ("review_burden", "max_review_burden_gap"),
            ):
                value = gaps[name]
                if value is not None and value > thresholds[limit]:
                    block(
                        "threshold_exceeded",
                        f"{dim}: {name} gap {value} exceeds {thresholds[limit]}",
                    )

    detected = sorted(c["id"] for c in joined if c["defect"])
    seeded = sorted(manifest.get("seeded_defects", []))
    for missed in sorted(set(seeded) - set(detected)):
        block("seeded_defect_undetected", f"seeded defect {missed} was not detected")
    for extra in sorted(set(detected) - set(seeded)):
        block("seeded_defect_unexpected", f"unexpected defect {extra}")
    for case_id in detected:
        block(
            "unjustified_exclusion", f"{case_id} excluded or deprioritised without approved reason"
        )

    lawful_fields, fields_valid = _valid_lawful_fields(manifest)
    if "lawful_analysis_fields" in manifest and not fields_valid:
        block(
            "unapproved_lawful_analysis_fields",
            "lawful analysis fields must be non-empty owner-approved field names",
        )

    if not _thresholds_approved(manifest):
        block(
            "unapproved_thresholds",
            "cohorts, lawful fields or thresholds lack named owner approval bound to this "
            "manifest digest (OQ-018)",
        )

    if live:
        for code, detail in _live_gaps(manifest, now):
            block(code, detail)

    human = bool(
        disposition
        and named(disposition.get("by"))
        and named(disposition.get("rationale"))
        and disposition.get("decision") in ("accept", "reject")
    )
    open_blockers = [
        b
        for b in blockers
        if not (
            human
            and disposition
            and disposition["decision"] == "accept"
            and b["code"] in DISPOSABLE
        )
    ]
    if human and disposition and disposition["decision"] == "reject":
        open_blockers.append({"code": "rejected", "detail": "human reviewer rejected activation"})
        blockers.append(open_blockers[-1])
    activation_allowed = not open_blockers
    synthetic = manifest.get("synthetic") is not False
    owner_approval_status = _owner_approval_status(manifest, fields_valid, now)
    lawful_analysis_fields_approved = owner_approval_status == OWNER_APPROVAL_APPROVED
    live_activation_allowed = bool(
        activation_allowed
        and owner_approval_status == OWNER_APPROVAL_APPROVED
        and lawful_analysis_fields_approved
        and not _live_gaps(manifest, now)
    )
    provenance_notice = (
        SYNTHETIC_NON_FAIRNESS_NOTICE
        if synthetic
        else (
            APPROVED_PROVENANCE_NOTICE
            if owner_approval_status == OWNER_APPROVAL_APPROVED
            else UNAPPROVED_NON_FAIRNESS_NOTICE
        )
    )
    body = {
        "record_version": RECORD_VERSION,
        "task_id": manifest.get("task_id"),
        "policy_or_model_version": manifest.get("subject_version"),
        "synthetic": synthetic,
        "synthetic_not_fairness_evidence": True,
        "non_fairness_provenance_notice": provenance_notice,
        "owner_approval_status": owner_approval_status,
        "lawful_analysis_fields": lawful_fields,
        "lawful_analysis_fields_approved": lawful_analysis_fields_approved,
        "live_activation_allowed": live_activation_allowed,
        "fairness_evidence": bool(
            not synthetic
            and _thresholds_approved(manifest)
            and fields_valid
            and not any(b["code"] in MEASUREMENT_BLOCKERS for b in blockers)
            and (not live or owner_approval_status == OWNER_APPROVAL_APPROVED)
        ),
        "missing_data_treatment": manifest.get("missing_data_treatment"),
        "input_digests": {"manifest": digest(manifest), "observed": digest(list(observed))},
        "thresholds": dict(thresholds) if isinstance(thresholds, Mapping) else {},
        "approval": dict(approval) if isinstance(approval, Mapping) else {},
        "total_cases": len(joined),
        "dimensions": dimensions,
        "seeded_defects": seeded,
        "detected_defects": detected,
        "blockers": blockers,
        "disposition": dict(disposition) if human and disposition else None,
        "status": "ready"
        if not blockers
        else ("dispositioned" if activation_allowed else "blocked"),
        "activation_allowed": activation_allowed,
        "authority_gap": OQ_018_GAP,
    }
    return {**body, "record_hash": digest(body)}


def export_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Verify hash integrity and OQ-018 pre-live/non-fairness invariants before export."""
    if not isinstance(record, Mapping) or record.get("record_version") != RECORD_VERSION:
        raise ValueError("cohort evaluation export requires a valid v1 evaluation record")
    record_hash = record.get("record_hash")
    body = copy.deepcopy({k: v for k, v in record.items() if k != "record_hash"})
    if not isinstance(record_hash, str) or digest(body) != record_hash:
        raise ValueError("cohort evaluation record_hash mismatch")
    if body.get("synthetic_not_fairness_evidence") is not True:
        raise ValueError("cohort evaluation export requires synthetic_not_fairness_evidence=True")
    notice = body.get("non_fairness_provenance_notice")
    if not named(notice) or "OQ-018" not in str(notice):
        raise ValueError("cohort evaluation export requires OQ-018 non_fairness_provenance_notice")
    approval_status = body.get("owner_approval_status")
    if approval_status not in (
        OWNER_APPROVAL_APPROVED,
        OWNER_APPROVAL_PENDING,
        OWNER_APPROVAL_UNAPPROVED,
    ):
        raise ValueError("cohort evaluation export requires explicit owner_approval_status")
    fields_approved = body.get("lawful_analysis_fields_approved")
    if not isinstance(fields_approved, bool):
        raise ValueError("cohort evaluation export requires bool lawful_analysis_fields_approved")
    synthetic = body.get("synthetic") is not False
    if synthetic and (
        body.get("fairness_evidence") is True
        or approval_status == OWNER_APPROVAL_APPROVED
        or fields_approved
        or body.get("live_activation_allowed") is True
    ):
        raise ValueError(
            "synthetic cohort evaluation cannot claim live approval or fairness evidence"
        )
    if (approval_status != OWNER_APPROVAL_APPROVED or not fields_approved) and body.get(
        "live_activation_allowed"
    ) is True:
        raise ValueError("unapproved cohort evaluation cannot allow live activation")
    return {**body, "record_hash": record_hash}
