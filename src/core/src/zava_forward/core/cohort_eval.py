"""Pure cohort and missing-data evaluation record (FR-054, AC-073); no store or clock access.

Constructed cohorts are compared with an approved expected-outcome manifest. Results are reported
per cohort and never averaged. Synthetic results are never fairness evidence (OQ-018).
"""

from __future__ import annotations

import copy
import math
import re
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from datetime import date, datetime
from typing import Any

from zava_forward.core import ranking
from zava_forward.core.rai_release import digest, named, named_human

_policy_hash: Callable[[Mapping[str, Any]], str] = ranking.policy_hash
_rule_order_hash: Callable[[Mapping[str, Any]], str] = ranking.rule_order_hash
_signoff_problems: Callable[[Mapping[str, Any]], list[str]] = ranking.signoff_problems
_rank_with_policy: Callable[
    [Sequence[Mapping[str, Any]], Mapping[str, Any]], list[dict[str, Any]]
] = ranking.rank

RECORD_VERSION = "cohort-missing-data-evaluation-v1"
OUTCOMES = ("ranked", "deprioritised", "excluded", "review", "abstained")
THRESHOLD_KEYS = ("min_sample", "max_error_rate", "max_exclusion_gap", "max_review_burden_gap")
OPTIONAL_THRESHOLD_KEYS = ("max_abstention_rate", "max_abstention_gap")
APPROVAL_ENVELOPE_KEYS = frozenset(
    {"approval", "protected_characteristic_approval", "context_dimension_approvals"}
)
OWNER_KEYS = ("cohorts_owner", "lawful_fields_owner", "thresholds_owner")
OWNER_APPROVAL_APPROVED = "approved"
OWNER_APPROVAL_PENDING = "pending_owner_approval"
OWNER_APPROVAL_UNAPPROVED = "unapproved"
UNAPPROVED_PLACEHOLDER_TOKENS = frozenset(
    {"unapproved", "unknown", "todo", "tbd", "tbc", "unassigned"}
)
FICTIONAL_OWNER_TOKENS = frozenset(
    {
        "fictional",
        "placeholder",
        "mock",
        "synthetic",
        "example",
        "todo",
        "tbd",
        "tbc",
        "unassigned",
        "unapproved",
        "unknown",
    }
)
PROTECTED_CHARACTERISTIC_FIELDS = frozenset(
    {
        "age",
        "disability",
        "gender_reassignment",
        "marriage_civil_partnership",
        "marriage_and_civil_partnership",
        "marital_status",
        "pregnancy",
        "maternity",
        "pregnancy_maternity",
        "pregnancy_and_maternity",
        "race",
        "ethnicity",
        "ethnic_origin",
        "nationality",
        "national_origin",
        "religion",
        "belief",
        "religion_or_belief",
        "sex",
        "gender",
        "sexual_orientation",
        "health",
    }
)
PROHIBITED_INFERENCE_KEYS = (
    frozenset(
        {
            "vulnerability",
            "vulnerable",
            "refusal",
            "refused",
            "non_engagement",
            "non_cooperative",
        }
    )
    | PROTECTED_CHARACTERISTIC_FIELDS
)
OPTIONAL_CONTEXT_DIMENSIONS = ("geography", "archetype")
GENERATED_ORIGINS = frozenset({"generated", "constructed", "synthetic"})
PROVISIONING_KEYS = frozenset(
    {
        "device_id",
        "sensor_device_id",
        "syn_device_id",
        "provision_device",
        "provision_sensor",
        "provisioned_device",
        "device_binding",
        "iot_hub_connection",
        "mqtt_endpoint",
        "serial_number",
        "mac_address",
        "hardware_id",
    }
)
INVENTED_SENSOR_THRESHOLD_KEYS = frozenset(
    {
        "dew_point_threshold",
        "dew_point_threshold_c",
        "hazard_threshold",
        "mould_hazard_threshold",
        "damp_hazard_threshold",
        "rh_hazard_threshold",
        "humidity_hazard_threshold",
        "hazard_rh_threshold",
        "condensation_threshold",
    }
)
LOWERED_SERVICE_VALUES = frozenset(
    {
        "reduced",
        "lowered",
        "degraded",
        "deprioritised",
        "withheld",
        "excluded",
        "none",
        "suspended",
        "basic_only",
    }
)
DISPOSABLE = {"seeded_defect_unexpected", "threshold_exceeded", "unjustified_exclusion"}
MEASUREMENT_BLOCKERS = {
    "invalid_input",
    "reconciliation",
    "insufficient_sample",
    "unapproved_lawful_analysis_fields",
    "unapproved_protected_characteristic",
    "unapproved_context_dimension",
    "unapproved_ranking_policy",
    "invalid_ranking_policy_hash",
    "missing_non_ai_comparison",
    "non_ai_comparison_invalid",
    "ai_regression_vs_non_ai",
    "service_lowered",
    "prohibited_inference",
    "sensor_fixture_provisions_device",
    "sensor_fixture_invents_threshold",
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


def _valid_offline_human_owner(value: object) -> bool:
    if not named_human(value) or not isinstance(value, str):
        return False
    norm = value.strip().casefold()
    if norm == "to be named":
        return False
    tokens = {tok for tok in re.split(r"[^a-z0-9]+", norm) if tok}
    return tokens.isdisjoint(UNAPPROVED_PLACEHOLDER_TOKENS)


def _real_human_owner(value: object) -> bool:
    if not _valid_offline_human_owner(value) or not isinstance(value, str):
        return False
    tokens = {tok for tok in re.split(r"[^a-z0-9]+", value.lower()) if tok}
    return tokens.isdisjoint(FICTIONAL_OWNER_TOKENS)


def _is_generated_cohort(manifest: Mapping[str, Any]) -> bool:
    if manifest.get("synthetic") is not False or bool(manifest.get("generated")):
        return True
    origin = str(manifest.get("cohort_origin", "")).strip().casefold()
    return origin in GENERATED_ORIGINS


def collect_protected_fields(value: Any) -> set[str]:
    """Return any UK Equality Act protected-characteristic field names referenced in `value`."""
    found: set[str] = set()
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = str(raw_key).strip().casefold()
            if key in PROTECTED_CHARACTERISTIC_FIELDS:
                found.add(key)
            if key not in APPROVAL_ENVELOPE_KEYS:
                found.update(collect_protected_fields(item))
    elif isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        for item in value:
            if isinstance(item, str):
                norm = item.strip().casefold()
                if norm in PROTECTED_CHARACTERISTIC_FIELDS:
                    found.add(norm)
            else:
                found.update(collect_protected_fields(item))
    return found


def scan_sensor_fixture_violations(value: Any) -> set[str]:
    """Detect device-provisioning fields/SYN- IDs or invented hazard/dew-point thresholds."""
    problems: set[str] = set()
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = str(raw_key).strip().casefold()
            if key in APPROVAL_ENVELOPE_KEYS:
                continue
            if key in PROVISIONING_KEYS and item not in (None, False, "", [], {}):
                problems.add("sensor_fixture_provisions_device")
            if (
                ("sensor" in key or "device" in key)
                and isinstance(item, str)
                and item.strip().upper().startswith("SYN-")
            ):
                problems.add("sensor_fixture_provisions_device")
            if key in INVENTED_SENSOR_THRESHOLD_KEYS and item is not None:
                problems.add("sensor_fixture_invents_threshold")
            problems.update(scan_sensor_fixture_violations(item))
    elif isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        for item in value:
            problems.update(scan_sensor_fixture_violations(item))
    return problems


def is_lowered_service(entry: Mapping[str, Any]) -> bool:
    """Return True when an observed/task output lowers service or priority."""
    if entry.get("service_lowered") is True or entry.get("priority_lowered") is True:
        return True
    level = entry.get("service_level")
    return isinstance(level, str) and level.strip().casefold() in LOWERED_SERVICE_VALUES


def has_prohibited_inference(entry: Mapping[str, Any]) -> bool:
    """Return True if output infers vulnerability, refusal, or protected traits."""
    for direct in (
        "inferred_vulnerability",
        "inferred_refusal",
        "inferred_protected_characteristic",
    ):
        if entry.get(direct) not in (None, False, ""):
            return True
    for container_key in ("inferences", "inferred", "inferred_attributes"):
        container = entry.get(container_key)
        if isinstance(container, Mapping):
            for raw_k, val in container.items():
                if val in (None, False, ""):
                    continue
                if str(raw_k).strip().casefold() in PROHIBITED_INFERENCE_KEYS:
                    return True
        elif isinstance(container, Sequence) and not isinstance(container, str | bytes | bytearray):
            for item in container:
                if isinstance(item, str) and item.strip().casefold() in PROHIBITED_INFERENCE_KEYS:
                    return True
    return False


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
    """Digest of the manifest content an owner approves, excluding approval envelopes."""
    return digest({k: v for k, v in manifest.items() if k not in APPROVAL_ENVELOPE_KEYS})


def approve(manifest: dict[str, Any], approval: Mapping[str, Any]) -> dict[str, Any]:
    """Record named owner approval bound to the manifest content; a later change voids it."""
    manifest["approval"] = {**approval, "manifest_digest": manifest_digest(manifest)}
    return manifest


def approve_protected_characteristics(
    manifest: dict[str, Any], approval: Mapping[str, Any]
) -> dict[str, Any]:
    """Bind lawful minimum-necessary DPO approval for protected-characteristic fields."""
    manifest["protected_characteristic_approval"] = {
        **approval,
        "manifest_digest": manifest_digest(manifest),
    }
    return manifest


def approve_context_dimensions(
    manifest: dict[str, Any], approvals: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    """Bind relevance approvals for optional context dimensions (geography, archetype)."""
    digest_val = manifest_digest(manifest)
    manifest["context_dimension_approvals"] = {
        dim: {**entry, "manifest_digest": digest_val} for dim, entry in approvals.items()
    }
    return manifest


def _approval_bound(manifest: Mapping[str, Any]) -> bool:
    approval = manifest.get("approval")
    return isinstance(approval, Mapping) and approval.get("manifest_digest") == manifest_digest(
        manifest
    )


def _thresholds_approved(manifest: Mapping[str, Any], now: float | None = None) -> bool:
    approval = manifest.get("approval")
    thresholds = manifest.get("thresholds")
    if not (
        isinstance(approval, Mapping)
        and all(_valid_offline_human_owner(approval.get(k)) for k in OWNER_KEYS)
        and _approval_bound(manifest)
        and not _has_invalid_or_expired_date(approval, now)
        and isinstance(thresholds, Mapping)
    ):
        return False
    sample = thresholds.get("min_sample")
    return (
        isinstance(sample, int)
        and not isinstance(sample, bool)
        and sample > 0
        and all(_limit(thresholds.get(k)) for k in THRESHOLD_KEYS[1:])
        and all(_limit(thresholds.get(k)) for k in OPTIONAL_THRESHOLD_KEYS if k in thresholds)
    )


def _owner_approval_status(
    manifest: Mapping[str, Any], fields_valid: bool, now: float | None
) -> str:
    generated = _is_generated_cohort(manifest)
    approval = manifest.get("approval")
    if (
        not isinstance(approval, Mapping)
        or not _thresholds_approved(manifest, now)
        or not fields_valid
    ):
        return OWNER_APPROVAL_UNAPPROVED
    if not all(named_human(approval.get(k)) for k in OWNER_KEYS):
        return OWNER_APPROVAL_UNAPPROVED
    if _has_invalid_or_expired_date(approval, now):
        return OWNER_APPROVAL_UNAPPROVED
    if (
        not generated
        and all(_real_human_owner(approval.get(k)) for k in OWNER_KEYS)
        and not _date_key_gaps(approval, now)
    ):
        return OWNER_APPROVAL_APPROVED
    return OWNER_APPROVAL_PENDING


def _live_gaps(manifest: Mapping[str, Any], now: float | None) -> list[tuple[str, str]]:
    gaps: list[tuple[str, str]] = []
    if _is_generated_cohort(manifest):
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
    eligible = len(cases)
    missing = sum(1 for c in cases if c["actual"] is None)
    present = [c for c in cases if c["actual"] is not None]
    n = len(present)
    abstained = sum(1 for c in present if c["abstained"])
    errors = sum(1 for c in present if c["failed"])
    excluded = sum(1 for c in present if c["actual"] == "excluded")
    deprioritised = sum(1 for c in present if c["actual"] == "deprioritised")
    review = sum(1 for c in present if c["review"])
    return {
        "n": n,
        "eligible": eligible,
        "tested": n,
        "abstained": abstained,
        "failed": errors,
        "missing": missing,
        "errors": errors,
        "excluded": excluded,
        "deprioritised": deprioritised,
        "review": review,
        "defects": sum(1 for c in present if c["defect"]),
        "error_rate": _rate(errors, n),
        "abstention_rate": _rate(abstained, n),
        "exclusion_rate": _rate(excluded + deprioritised, n),
        "review_burden": _rate(review, n),
        "_raw": {
            "error_rate": errors / n if n else None,
            "abstention_rate": abstained / n if n else None,
            "exclusion_rate": (excluded + deprioritised) / n if n else None,
            "review_burden": review / n if n else None,
        },
        "error_interval": wilson(errors, n),
        "sufficient": n >= min_sample > 0,
    }


def _gap(rows: Mapping[str, Mapping[str, Any]], key: str) -> float | None:
    values = [r["_raw"][key] for r in rows.values() if r["sufficient"] and r[key] is not None]
    return max(values) - min(values) if len(values) >= 2 else None


def _verify_ranking_policy(
    raw_policy: Any,
) -> tuple[dict[str, Any], list[tuple[str, str]]]:
    problems: list[tuple[str, str]] = []
    if not isinstance(raw_policy, Mapping):
        problems.append(
            ("unapproved_ranking_policy", "ranking or AI task requires a signed ranking_policy")
        )
        return {
            "policy_id": None,
            "version": None,
            "owner": None,
            "content_hash": None,
            "rule_order_hash": None,
            "signed": False,
            "signoff_problems": ["missing ranking_policy"],
        }, problems
    required = ("policy_id", "version", "owner", "rules", "stage_order", "content_hash")
    missing_keys = [k for k in required if k not in raw_policy]
    content_hash_ok = False
    rule_hash: str | None = None
    rules_valid = False
    if not missing_keys and isinstance(raw_policy.get("rules"), Sequence):
        try:
            computed = _policy_hash(raw_policy)
            content_hash_ok = computed == raw_policy.get("content_hash")
            rule_hash = _rule_order_hash(raw_policy)
            _rank_with_policy([], raw_policy)
            rules_valid = True
        except (KeyError, TypeError, ValueError):
            rules_valid = False
    if missing_keys or not content_hash_ok or not rules_valid:
        problems.append(
            (
                "invalid_ranking_policy_hash",
                "ranking_policy is incomplete, has invalid rules or fails content_hash check",
            )
        )
    signoff_issues = list(_signoff_problems(raw_policy)) if rules_valid else ["invalid policy"]
    owner_val = raw_policy.get("owner")
    if not _valid_offline_human_owner(owner_val) and "No named policy owner." not in signoff_issues:
        signoff_issues.append("Policy owner is not a named human.")
    signed = content_hash_ok and rules_valid and not signoff_issues
    if not signed:
        problems.append(
            (
                "unapproved_ranking_policy",
                "ranking_policy lacks named-human rule-order sign-off: "
                + "; ".join(signoff_issues),
            )
        )
    return {
        "policy_id": raw_policy.get("policy_id"),
        "version": raw_policy.get("version"),
        "owner": owner_val,
        "content_hash": raw_policy.get("content_hash"),
        "rule_order_hash": rule_hash,
        "signed": signed,
        "signoff_problems": signoff_issues,
    }, problems


def _case_has_missing_sensor_or_non_response(
    case: Mapping[str, Any],
    cohort_map: Mapping[str, Any],
    input_case: Mapping[str, Any],
) -> bool:
    if cohort_map.get("sensor_completeness") in {
        "declined",
        "missing",
        "partial",
        "absent",
        "none",
    }:
        return True
    if cohort_map.get("source_completeness") in {"missing", "partial", "stale"}:
        return True
    if cohort_map.get("appointment_history") in {
        "no_response",
        "missed",
        "prior_no_access",
        "unconfirmed",
        "resident_rescheduled",
    }:
        return True
    for src in (case, input_case):
        if "sensor_data" in src and src.get("sensor_data") in {None, "declined", "missing"}:
            return True
        if src.get("appointment_history") in {
            "no_response",
            "prior_no_access",
            "unconfirmed",
            "resident_rescheduled",
        }:
            return True
    return False


def evaluate(
    manifest: Mapping[str, Any],
    observed: Sequence[Mapping[str, Any]],
    disposition: Mapping[str, Any] | None = None,
    *,
    live: bool = False,
    now: float | None = None,
    ranking_policy: Mapping[str, Any] | None = None,
    non_ai_observed: Sequence[Mapping[str, Any]] | None = None,
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
    declared_raw = manifest.get("cohorts", {})
    declared: Mapping[str, Sequence[str]] = (
        declared_raw if isinstance(declared_raw, Mapping) else {}
    )
    thresholds_raw = manifest.get("thresholds", {})
    thresholds: Mapping[str, Any] = thresholds_raw if isinstance(thresholds_raw, Mapping) else {}
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

    raw_inputs = manifest.get("inputs", [])
    input_by_id: dict[str, Mapping[str, Any]] = {}
    if isinstance(raw_inputs, Sequence) and not isinstance(raw_inputs, str | bytes | bytearray):
        for item in raw_inputs:
            if isinstance(item, Mapping) and valid_id(item.get("id")):
                input_by_id[str(item["id"])] = item

    for sensor_code in sorted(
        scan_sensor_fixture_violations(manifest) | scan_sensor_fixture_violations(list(observed))
    ):
        block(
            sensor_code,
            (
                "sensor completeness fixtures must not provision devices "
                "or invent hazard/dew-point thresholds"
            ),
        )

    joined: list[dict[str, Any]] = []
    service_lowered_ids: list[str] = []
    prohibited_inference_ids: list[str] = []
    for c in cases:
        cid = str(c.get("id"))
        obs = seen.get(c.get("id"), {}) if valid_id(c.get("id")) else {}
        actual = obs.get("outcome") if obs else None
        if obs and actual not in OUTCOMES:
            block("invalid_input", f"observed case {c['id']} has missing or unsupported outcome")
            actual = None
        cohort_map = c.get("cohorts")
        if not isinstance(cohort_map, Mapping):
            block("invalid_input", f"manifest case {c.get('id')} has no cohorts mapping")
            cohort_map = {}
        abstained_flag = actual == "abstained" or (
            actual is not None and obs.get("abstained") is True
        )
        protected_missing = _case_has_missing_sensor_or_non_response(
            c, cohort_map, input_by_id.get(cid, {})
        )
        lowered_service = (
            bool(obs)
            and is_lowered_service(obs)
            and (protected_missing or obs.get("reason") not in justified)
        )
        prohibited_inf = bool(obs) and has_prohibited_inference(obs)
        if lowered_service:
            service_lowered_ids.append(cid)
        if prohibited_inf:
            prohibited_inference_ids.append(cid)
        unjustified_drop = (
            actual in ("excluded", "deprioritised")
            and actual != c.get("expected")
            and obs.get("reason") not in justified
        )
        unjustified_abstain = (
            abstained_flag
            and c.get("expected") != "abstained"
            and obs.get("reason") not in justified
            and obs.get("fallback_to_non_ai") is not True
        )
        defect = unjustified_drop or unjustified_abstain or lowered_service
        case_failed = actual is not None and (
            actual != c.get("expected") or lowered_service or prohibited_inf
        )
        needs_review = (
            actual == "review"
            or (abstained_flag and obs.get("review_required") is not False)
            or (obs.get("review_required") is True and actual is not None)
        )
        joined.append(
            {
                **c,
                "cohorts": cohort_map,
                "actual": actual,
                "abstained": abstained_flag,
                "failed": case_failed,
                "defect": defect,
                "review": needs_review,
            }
        )

    for cid in sorted(service_lowered_ids):
        block(
            "service_lowered",
            f"{cid} lowered service or priority on missing/declined sensor or non-response",
        )
    for cid in sorted(prohibited_inference_ids):
        block(
            "prohibited_inference",
            f"{cid} inferred vulnerability, refusal or protected characteristics",
        )

    thresholds_ok = _thresholds_approved(manifest, now)
    min_sample = int(thresholds.get("min_sample", 0)) if thresholds_ok else 0
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
        gaps: dict[str, float | None] = {
            "exclusion": _gap(rows, "exclusion_rate"),
            "review_burden": _gap(rows, "review_burden"),
            "abstention": _gap(rows, "abstention_rate"),
        }
        raw = {label: row.pop("_raw") for label, row in rows.items()}
        dimensions[dim] = {
            "cohorts": rows,
            "gaps": {k: None if v is None else round(v, 4) for k, v in gaps.items()},
        }
        for label, row in rows.items():
            if not row["sufficient"]:
                block("insufficient_sample", f"{dim}/{label}: n={row['n']} below minimum sample")
            elif thresholds_ok:
                if raw[label]["error_rate"] > thresholds["max_error_rate"]:
                    block("threshold_exceeded", f"{dim}/{label}: error rate {row['error_rate']}")
                if (
                    "max_abstention_rate" in thresholds
                    and raw[label]["abstention_rate"] > thresholds["max_abstention_rate"]
                ):
                    block(
                        "threshold_exceeded",
                        f"{dim}/{label}: abstention rate {row['abstention_rate']}",
                    )
        if thresholds_ok:
            gap_limits: list[tuple[str, str]] = [
                ("exclusion", "max_exclusion_gap"),
                ("review_burden", "max_review_burden_gap"),
            ]
            if "max_abstention_gap" in thresholds:
                gap_limits.append(("abstention", "max_abstention_gap"))
            for name, limit in gap_limits:
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

    used_protected = (
        collect_protected_fields(declared)
        | collect_protected_fields(lawful_fields)
        | collect_protected_fields(cases)
        | collect_protected_fields(raw_inputs)
    )
    if used_protected:
        pca = manifest.get("protected_characteristic_approval")
        approved_fields_raw = pca.get("approved_fields") if isinstance(pca, Mapping) else None
        approved_protected = (
            {str(item).strip().casefold() for item in approved_fields_raw if named(item)}
            if isinstance(approved_fields_raw, Sequence)
            and not isinstance(approved_fields_raw, str | bytes | bytearray)
            else set()
        )
        pca_ok = bool(
            isinstance(pca, Mapping)
            and pca.get("manifest_digest") == manifest_digest(manifest)
            and _real_human_owner(pca.get("dpo_owner") or pca.get("approved_by"))
            and named(pca.get("lawful_basis"))
            and named(pca.get("minimum_necessary_justification"))
            and _valid_approval_stamp(pca.get("approved_at"), now)
            and not _has_invalid_or_expired_date(pca, now)
            and used_protected <= approved_protected
        )
        if not pca_ok:
            block(
                "unapproved_protected_characteristic",
                "protected-characteristic fields require bound DPO minimum-necessary approval: "
                + ", ".join(sorted(used_protected)),
            )

    used_context_dims = [d for d in OPTIONAL_CONTEXT_DIMENSIONS if d in declared]
    if used_context_dims:
        cda = manifest.get("context_dimension_approvals")
        m_dig = manifest_digest(manifest)
        for dim in used_context_dims:
            entry = cda.get(dim) if isinstance(cda, Mapping) else None
            ctx_ok = bool(
                isinstance(entry, Mapping)
                and entry.get("manifest_digest") == m_dig
                and _valid_offline_human_owner(entry.get("approved_by"))
                and entry.get("relevant") is True
                and named(entry.get("rationale"))
                and not _has_invalid_or_expired_date(entry, now)
            )
            if not ctx_ok:
                block(
                    "unapproved_context_dimension",
                    f"{dim} cohort dimension requires bound relevance approval",
                )

    task_kind = str(manifest.get("task_kind", "")).strip().casefold()
    raw_policy = ranking_policy if ranking_policy is not None else manifest.get("ranking_policy")
    raw_non_ai = non_ai_observed if non_ai_observed is not None else manifest.get("non_ai_baseline")
    policy_summary: dict[str, Any] | None = None
    if (
        task_kind in {"ai_task", "ranking", "prioritisation"}
        or raw_policy is not None
        or raw_non_ai is not None
    ):
        policy_summary, policy_problems = _verify_ranking_policy(raw_policy)
        for p_code, p_detail in policy_problems:
            block(p_code, p_detail)

    non_ai_comparison: dict[str, Any] | None = None
    if task_kind == "ai_task" or raw_non_ai is not None:
        if not isinstance(raw_non_ai, Sequence) or isinstance(raw_non_ai, str | bytes | bytearray):
            block(
                "missing_non_ai_comparison",
                "AI task evaluation requires a transparent non-AI baseline comparison",
            )
        else:
            base_ids = [b.get("id") for b in raw_non_ai if isinstance(b, Mapping)]
            if (
                len(base_ids) != len(raw_non_ai)
                or not all(valid_id(i) for i in base_ids)
                or len(set(base_ids)) != len(base_ids)
                or set(base_ids) != manifest_ids
                or any(b.get("outcome") not in OUTCOMES for b in raw_non_ai)
            ):
                block(
                    "non_ai_comparison_invalid",
                    "non_ai_observed baseline does not reconcile cleanly with manifest cases",
                )
            else:
                base_by_id = {str(b["id"]): b for b in raw_non_ai}
                regressed_cases: list[str] = []
                for c in joined:
                    cid = str(c["id"])
                    b_obs = base_by_id[cid]
                    b_out = b_obs.get("outcome")
                    ai_bad = c["actual"] in ("excluded", "deprioritised") and (
                        seen.get(cid, {}).get("reason") not in justified
                    )
                    base_bad = b_out in ("excluded", "deprioritised") and (
                        b_obs.get("reason") not in justified
                    )
                    ai_err = c["failed"]
                    base_err = b_out != c.get("expected")
                    if (ai_bad and not base_bad) or (ai_err and not base_err):
                        regressed_cases.append(cid)
                subgroup_regressions: list[str] = []
                for dim, labels in declared.items():
                    for label in labels:
                        sub_cases = [c for c in joined if c["cohorts"].get(dim) == label]
                        ai_excl = sum(
                            1 for c in sub_cases if c["actual"] in ("excluded", "deprioritised")
                        )
                        base_excl = sum(
                            1
                            for c in sub_cases
                            if base_by_id[str(c["id"])].get("outcome")
                            in ("excluded", "deprioritised")
                        )
                        if ai_excl > base_excl:
                            subgroup_regressions.append(f"{dim}/{label}")
                regression_detected = bool(regressed_cases or subgroup_regressions)
                if regression_detected:
                    block(
                        "ai_regression_vs_non_ai",
                        "AI task regressed relative to transparent non-AI baseline on: "
                        + ", ".join(regressed_cases or subgroup_regressions),
                    )
                non_ai_comparison = {
                    "compared_cases": len(joined),
                    "regressed_cases": regressed_cases,
                    "regressed_subgroups": subgroup_regressions,
                    "regression_detected": regression_detected,
                }

    if not thresholds_ok:
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
        and _valid_offline_human_owner(disposition.get("by"))
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
    generated_cohort = _is_generated_cohort(manifest)
    owner_approval_status = _owner_approval_status(manifest, fields_valid, now)
    lawful_analysis_fields_approved = owner_approval_status == OWNER_APPROVAL_APPROVED
    live_activation_allowed = bool(
        activation_allowed
        and not generated_cohort
        and owner_approval_status == OWNER_APPROVAL_APPROVED
        and lawful_analysis_fields_approved
        and not _live_gaps(manifest, now)
    )
    provenance_notice = (
        SYNTHETIC_NON_FAIRNESS_NOTICE
        if generated_cohort
        else (
            APPROVED_PROVENANCE_NOTICE
            if owner_approval_status == OWNER_APPROVAL_APPROVED
            else UNAPPROVED_NON_FAIRNESS_NOTICE
        )
    )
    input_digests: dict[str, str] = {
        "manifest": digest(manifest),
        "observed": digest(list(observed)),
    }
    if ranking_policy is not None:
        input_digests["ranking_policy"] = digest(ranking_policy)
    if non_ai_observed is not None:
        input_digests["non_ai_observed"] = digest(list(non_ai_observed))
    tested_count = sum(1 for c in joined if c["actual"] is not None)
    missing_count = sum(1 for c in joined if c["actual"] is None)
    abstained_count = sum(1 for c in joined if c["actual"] is not None and c["abstained"])
    failed_count = sum(1 for c in joined if c["actual"] is not None and c["failed"])
    body = {
        "record_version": RECORD_VERSION,
        "task_id": manifest.get("task_id"),
        "policy_or_model_version": manifest.get("subject_version"),
        "synthetic": synthetic,
        "generated_cohort": generated_cohort,
        "population_fairness_established": False,
        "aggregation_rule": "per_cohort_unaveraged",
        "synthetic_not_fairness_evidence": True,
        "non_fairness_provenance_notice": provenance_notice,
        "owner_approval_status": owner_approval_status,
        "lawful_analysis_fields": lawful_fields,
        "lawful_analysis_fields_approved": lawful_analysis_fields_approved,
        "live_activation_allowed": live_activation_allowed,
        "fairness_evidence": bool(
            not generated_cohort
            and thresholds_ok
            and fields_valid
            and owner_approval_status != OWNER_APPROVAL_UNAPPROVED
            and not blockers
            and (not live or owner_approval_status == OWNER_APPROVAL_APPROVED)
        ),
        "missing_data_treatment": manifest.get("missing_data_treatment"),
        "cohort_definitions": {
            "cohort_version": manifest.get("cohort_version", "v1"),
            "cohorts": {k: list(v) for k, v in declared.items()},
            "justified_reasons": sorted(str(x) for x in justified),
            "missing_data_treatment": manifest.get("missing_data_treatment"),
        },
        "version_definitions": {
            "record_version": RECORD_VERSION,
            "manifest_digest": manifest_digest(manifest),
            "cohort_version": manifest.get("cohort_version", "v1"),
            "subject_version": manifest.get("subject_version"),
            "policy_version": (
                policy_summary["version"]
                if policy_summary is not None
                else manifest.get("policy_version")
            ),
            "ranking_policy_id": (
                policy_summary["policy_id"] if policy_summary is not None else None
            ),
            "ranking_policy_hash": (
                policy_summary["content_hash"] if policy_summary is not None else None
            ),
            "ranking_rule_order_hash": (
                policy_summary["rule_order_hash"] if policy_summary is not None else None
            ),
            "prompt_version": manifest.get("prompt_version"),
            "model_version": manifest.get("model_version"),
        },
        "ranking_policy": policy_summary,
        "non_ai_comparison": non_ai_comparison,
        "input_digests": input_digests,
        "thresholds": dict(thresholds) if isinstance(thresholds, Mapping) else {},
        "approval": dict(approval) if isinstance(approval, Mapping) else {},
        "total_cases": len(joined),
        "counts": {
            "eligible": len(joined),
            "tested": tested_count,
            "abstained": abstained_count,
            "failed": failed_count,
            "missing": missing_count,
        },
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
    if body.get("population_fairness_established") is not False:
        raise ValueError("cohort evaluation export cannot claim population_fairness_established")
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
    generated = body.get("synthetic") is not False or bool(body.get("generated_cohort"))
    if generated and (
        body.get("fairness_evidence") is True
        or approval_status == OWNER_APPROVAL_APPROVED
        or fields_approved
        or body.get("live_activation_allowed") is True
    ):
        raise ValueError(
            "synthetic or generated cohort evaluation cannot claim "
            "live approval or fairness evidence"
        )
    if body.get("blockers") and body.get("fairness_evidence") is True:
        raise ValueError("cohort evaluation with recorded blockers cannot claim fairness_evidence")
    if (approval_status != OWNER_APPROVAL_APPROVED or not fields_approved) and body.get(
        "live_activation_allowed"
    ) is True:
        raise ValueError("unapproved cohort evaluation cannot allow live activation")
    return {**body, "record_hash": record_hash}
