"""Pure cohort and missing-data evaluation record (FR-054, AC-073); no store or clock access.

Constructed cohorts are compared with an approved expected-outcome manifest. Results are reported
per cohort and never averaged. Synthetic results are never fairness evidence (OQ-018).
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

from zava_forward.core.rai_release import digest, named

RECORD_VERSION = "cohort-missing-data-evaluation-v1"
OUTCOMES = ("ranked", "deprioritised", "excluded", "review")
THRESHOLD_KEYS = ("min_sample", "max_error_rate", "max_exclusion_gap", "max_review_burden_gap")
DISPOSABLE = {"seeded_defect_unexpected", "threshold_exceeded", "unjustified_exclusion"}
OQ_018_GAP = (
    "OQ-018: representative cohorts, lawful analysis fields, sample sufficiency and thresholds "
    "need owner approval before live use; synthetic results are not fairness evidence."
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


def _limit(value: Any) -> bool:
    return (
        isinstance(value, int | float)
        and not isinstance(value, bool)
        and math.isfinite(value)
        and 0 <= value <= 1
    )


def _thresholds_approved(manifest: Mapping[str, Any]) -> bool:
    approval = manifest.get("approval")
    thresholds = manifest.get("thresholds")
    if not (
        isinstance(approval, Mapping)
        and named(approval.get("cohorts_owner"))
        and named(approval.get("thresholds_owner"))
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


def _cohort_row(cases: Sequence[Mapping[str, Any]], min_sample: int) -> dict[str, Any]:
    missing = sum(1 for c in cases if c["actual"] is None)
    cases = [c for c in cases if c["actual"] is not None]
    n = len(cases)
    errors = sum(1 for c in cases if c["actual"] != c["expected"])
    excluded = sum(1 for c in cases if c["actual"] == "excluded")
    deprioritised = sum(1 for c in cases if c["actual"] == "deprioritised")
    review = sum(1 for c in cases if c["actual"] == "review")
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
) -> dict[str, Any]:
    """Build the versioned evaluation record for one task or policy version."""
    blockers: list[dict[str, str]] = []

    def block(code: str, detail: str) -> None:
        blockers.append({"code": code, "detail": detail})

    cases = list(manifest.get("cases", []))
    declared: Mapping[str, Sequence[str]] = manifest.get("cohorts", {})
    thresholds: Mapping[str, Any] = manifest.get("thresholds", {})
    justified = set(manifest.get("justified_reasons", []))
    obs_ids = [o.get("id") for o in observed]
    case_ids = [c["id"] for c in cases]
    for label, ids in (("observed", obs_ids), ("manifest", case_ids)):
        for dup in sorted({str(i) for i in ids if ids.count(i) > 1}):
            block("invalid_input", f"duplicate {label} case id {dup}")
    seen = {o.get("id"): o for o in observed}
    manifest_ids = set(case_ids)

    for extra in sorted(str(i) for i in set(seen) - manifest_ids):
        block("reconciliation", f"observed case {extra} is not in the manifest")
    for miss in sorted(manifest_ids - set(seen)):
        block("reconciliation", f"manifest case {miss} has no observed outcome")

    joined: list[dict[str, Any]] = []
    for c in cases:
        obs = seen.get(c["id"], {})
        actual = obs.get("outcome") if obs else None
        if obs and actual not in OUTCOMES:
            block("invalid_input", f"observed case {c['id']} has missing or unsupported outcome")
            actual = None
        defect = (
            actual in ("excluded", "deprioritised")
            and actual != c["expected"]
            and obs.get("reason") not in justified
        )
        joined.append({**c, "actual": actual, "defect": defect})

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

    if not _thresholds_approved(manifest):
        block("unapproved_thresholds", "cohorts or thresholds lack named owner approval (OQ-018)")

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
    body = {
        "record_version": RECORD_VERSION,
        "task_id": manifest.get("task_id"),
        "policy_or_model_version": manifest.get("subject_version"),
        "synthetic": bool(manifest.get("synthetic", True)),
        "fairness_evidence": False
        if manifest.get("synthetic", True)
        else bool(_thresholds_approved(manifest)),
        "missing_data_treatment": manifest.get("missing_data_treatment"),
        "input_digests": {"manifest": digest(manifest), "observed": digest(list(observed))},
        "thresholds": dict(thresholds),
        "approval": dict(manifest.get("approval") or {}),
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
