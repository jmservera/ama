"""Versioned deterministic sensor analysis (issue 111, exercise slice).

Pure functions over retained canonical readings: no store, clock, network, task, ranking, hazard,
clock-start, hold or AI access. Every threshold is an exercise value, not a sourced standard. A
review-task candidate exists only for an approved rule; the default policy has no approval, so it
never proposes one. Missing, stale, unconsented or unusable data is INSUFFICIENT/STALE/DECLINED and
carries no priority effect.
"""

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from typing import TypedDict

from .synthetic import sensor_faults
from .synthetic import sensor_scenarios as comparator

ANALYSIS_VERSION = "sensor-analysis-exercise-v1"
COMPARATOR_VERSION = comparator.METHOD_VERSION
SCHEMA_VERSION = sensor_faults.SCHEMA_VERSION
EXERCISE_LABEL = "EXERCISE VALUE: fictional, not sourced"
RULE_ID = "SENSOR-RH-PERSISTENCE-EXERCISE"
TASK_TYPE = "SENSOR_REVIEW_DUE"
TASK_QUEUE = "condition-assessment"
SENSOR_NON_AUTHORITY_ERROR = "SENSOR_NON_AUTHORITY_VIOLATION"
NO_SIGNAL = comparator.NO_SIGNAL
REVIEW = comparator.REVIEW
INSUFFICIENT = comparator.INSUFFICIENT
SUFFICIENT = "SUFFICIENT"
STALE = "STALE"
DECLINED = "DECLINED"
CONSENTS = ("granted", "unknown", "declined")
_LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._-]{0,79}\Z")
_READING_FIELD_SET = frozenset(sensor_faults.READING_FIELDS)
_ROW_BOUND_FIELDS = (
    "sensor_id",
    "observed_at",
    "reading_id",
    "temperature_c",
    "temperature_unit",
    "humidity_pct",
    "humidity_unit",
    "calibrated",
    "source_type",
    "schema_version",
)


class _Unset:
    pass


_UNSET = _Unset()


@dataclass(frozen=True)
class RuleApproval:
    """Named human approval of one rule version; never inferred, never defaulted."""

    rule_id: str
    policy_version: str
    approver_role: str
    approval_reference: str

    def validate(self) -> None:
        for value in (self.rule_id, self.policy_version, self.approver_role):
            if not isinstance(value, str) or not _LABEL.fullmatch(value):
                raise ValueError("INVALID_RULE_APPROVAL")
        if not isinstance(self.approval_reference, str) or not _LABEL.fullmatch(
            self.approval_reference
        ):
            raise ValueError("INVALID_RULE_APPROVAL")


@dataclass(frozen=True)
class AnalysisPolicy:
    version: str = ANALYSIS_VERSION
    humidity_threshold_pct: float = 75.0
    max_staleness_hours: int = 48
    threshold_label: str = EXERCISE_LABEL
    approval: RuleApproval | None = None

    def validate(self) -> None:
        if not isinstance(self.version, str) or not _LABEL.fullmatch(self.version):
            raise ValueError("INVALID_POLICY_VERSION")
        if type(self.max_staleness_hours) is not int or not 1 <= self.max_staleness_hours <= 720:
            raise ValueError("INVALID_STALENESS_LIMIT")
        if not self.threshold_label.startswith(("EXERCISE VALUE", "SOURCED:")):
            raise ValueError("THRESHOLD_LABEL_REQUIRED")
        comparator._threshold(self.humidity_threshold_pct)
        if self.approval is not None:
            self.approval.validate()

    @property
    def rule_approved(self) -> bool:
        return (
            self.approval is not None
            and self.approval.rule_id == RULE_ID
            and self.approval.policy_version == self.version
        )


def _strict_bool(value: object, expected: bool) -> bool:
    return type(value) is bool and value is expected


_AUTHORITY_FALSE_FLAGS = ("diagnoses_hazard", "starts_clock", "releases_hold", "changes_ranking")
_AUTHORITY_TRUE_FLAGS = ("resident_report_unaffected",)
_AUTHORITY_STR_VALUES = (("priority_effect", "NONE"),)


@dataclass(frozen=True)
class Signal:
    home_id: str
    analysis_version: str
    policy_version: str
    threshold_label: str
    window_start: str
    window_end: str
    as_of: str
    sufficiency: str
    outcome: str
    reasons: tuple[str, ...]
    expected: int
    valid: int
    coverage: float
    longest_high_hours: int
    high_nights: int
    input_digest: str
    priority_effect: str = "NONE"
    diagnoses_hazard: bool = False

    def __post_init__(self) -> None:
        if self.priority_effect != "NONE" or not _strict_bool(self.diagnoses_hazard, False):
            raise ValueError(SENSOR_NON_AUTHORITY_ERROR)


@dataclass(frozen=True)
class ReviewTaskCandidate:
    """A proposal for a human condition-review task; nothing here creates or ranks a task."""

    task_key: str
    task_type: str
    queue: str
    home_id: str
    status: str
    rule_id: str
    approval_reference: str
    policy_version: str
    analysis_version: str
    input_digest: str
    summary: str
    resident_report_unaffected: bool = True
    changes_ranking: bool = False
    starts_clock: bool = False
    releases_hold: bool = False
    diagnoses_hazard: bool = False

    def __post_init__(self) -> None:
        if (
            self.task_type != TASK_TYPE
            or self.queue != TASK_QUEUE
            or self.status != "PROPOSED"
            or not _strict_bool(self.resident_report_unaffected, True)
            or any(not _strict_bool(getattr(self, f), False) for f in _AUTHORITY_FALSE_FLAGS)
        ):
            raise ValueError(SENSOR_NON_AUTHORITY_ERROR)


def enforce_sensor_non_authority(value: object) -> None:
    """Fail closed if a sensor value object, receipt, or serialized payload claims authority."""
    if isinstance(value, (Signal, ReviewTaskCandidate)):
        value.__post_init__()
        return
    if not isinstance(value, Mapping):
        if all(hasattr(value, f) for f in _AUTHORITY_FALSE_FLAGS):
            if any(not _strict_bool(getattr(value, f), False) for f in _AUTHORITY_FALSE_FLAGS):
                raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
            for str_field, expected in _AUTHORITY_STR_VALUES:
                if hasattr(value, str_field) and getattr(value, str_field) != expected:
                    raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
            for true_field in _AUTHORITY_TRUE_FLAGS:
                if hasattr(value, true_field) and not _strict_bool(
                    getattr(value, true_field), True
                ):
                    raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
            return
        raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
    is_candidate = any(k in value for k in ("task_type", "queue", "resident_report_unaffected"))
    is_signal = "priority_effect" in value and "diagnoses_hazard" in value
    has_all_flags = all(f in value for f in _AUTHORITY_FALSE_FLAGS)
    if not (is_candidate or is_signal or has_all_flags):
        raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
    if is_candidate and (
        value.get("task_type") != TASK_TYPE
        or value.get("queue") != TASK_QUEUE
        or ("status" in value and value.get("status") != "PROPOSED")
        or not _strict_bool(value.get("resident_report_unaffected"), True)
        or any(not _strict_bool(value.get(f), False) for f in _AUTHORITY_FALSE_FLAGS)
    ):
        raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
    if is_signal and (
        value.get("priority_effect") != "NONE"
        or not _strict_bool(value.get("diagnoses_hazard"), False)
    ):
        raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
    for flag in _AUTHORITY_FALSE_FLAGS:
        if flag in value and not _strict_bool(value.get(flag), False):
            raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
    if "priority_effect" in value and value.get("priority_effect") != "NONE":
        raise ValueError(SENSOR_NON_AUTHORITY_ERROR)
    if "resident_report_unaffected" in value and not _strict_bool(
        value.get("resident_report_unaffected"), True
    ):
        raise ValueError(SENSOR_NON_AUTHORITY_ERROR)


@dataclass(frozen=True)
class VersionProvenance:
    """Explicit version, policy, approval, window, and digest provenance; carries no raw data."""

    home_id: str
    analysis_version: str
    comparator_version: str
    schema_version: str
    policy_version: str
    policy_digest: str
    threshold_label: str
    humidity_threshold_pct: float
    max_staleness_hours: int
    rule_id: str
    rule_approved: bool
    approver_role: str | None
    approval_reference: str | None
    window_start: str
    window_end: str
    as_of: str
    input_digest: str
    output_digest: str


class ProvenanceDict(TypedDict):
    home_id: str
    analysis_version: str
    comparator_version: str
    schema_version: str
    policy_version: str
    policy_digest: str
    threshold_label: str
    humidity_threshold_pct: float
    max_staleness_hours: int
    rule_id: str
    rule_approved: bool
    approver_role: str | None
    approval_reference: str | None
    window_start: str
    window_end: str
    as_of: str
    input_digest: str
    output_digest: str


class SignalDict(TypedDict):
    home_id: str
    analysis_version: str
    policy_version: str
    threshold_label: str
    window_start: str
    window_end: str
    as_of: str
    sufficiency: str
    outcome: str
    reasons: tuple[str, ...]
    expected: int
    valid: int
    coverage: float
    longest_high_hours: int
    high_nights: int
    input_digest: str
    priority_effect: str
    diagnoses_hazard: bool


class ReviewTaskDict(TypedDict):
    task_key: str
    task_type: str
    queue: str
    home_id: str
    status: str
    rule_id: str
    approval_reference: str
    policy_version: str
    analysis_version: str
    input_digest: str
    summary: str
    resident_report_unaffected: bool
    changes_ranking: bool
    starts_clock: bool
    releases_hold: bool
    diagnoses_hazard: bool


class ReproducedReviewTask(TypedDict):
    provenance: ProvenanceDict
    signal: SignalDict
    review_task: ReviewTaskDict | None


class ReproducedSensorAnalysis(TypedDict):
    analysis_version: str
    policy_version: str
    input_digest: str
    output_digest: str
    provenance: ProvenanceDict
    signal: SignalDict
    review_task: ReviewTaskDict | None


def _stamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def _canonical_row(row: Mapping[str, str]) -> str:
    return json.dumps(
        {str(k): v for k, v in sorted(row.items(), key=lambda item: str(item[0]))},
        ensure_ascii=True,
        sort_keys=True,
        default=str,
    )


def _exact_row_key(row: Mapping[str, str]) -> tuple[str, str, str, str]:
    home_val: object = row.get("home_id")
    home_type = "str" if isinstance(home_val, str) else type(home_val).__qualname__
    return (home_type, str(row.get("home_id", "")), _canonical_row(row), _schema_marker(row))


def _dedupe_exact_rows(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    seen: dict[tuple[str, str, str, str], Mapping[str, str]] = {}
    for row in rows:
        key = _exact_row_key(row)
        if key not in seen:
            seen[key] = row
    return list(seen.values())


def _by_observation(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    """Canonical set order so the result is a function of the reading set, not arrival or replay."""
    return sorted(
        _dedupe_exact_rows(rows),
        key=lambda r: (str(r.get("observed_at", "")), _exact_row_key(r)),
    )


_METRICS = (("temperature_c", "temperature_unit"), ("humidity_pct", "humidity_unit"))


def reading_tuples(rows: Sequence[Mapping[str, str]]) -> list[tuple[str, str, str, str, str]]:
    """Canonical (sensor_id, metric, timestamp, value, unit) tuples, sorted independent of order."""
    unique = _dedupe_exact_rows(rows)
    return sorted(
        (
            str(row.get("sensor_id", "")),
            metric,
            str(row.get("observed_at", "")),
            str(row.get(metric, "")),
            str(row.get(unit, "")),
        )
        for row in unique
        for metric, unit in _METRICS
    )


def _norm_float(value: float) -> float:
    out = float(value)
    return 0.0 if out == 0.0 else out


def _schema_marker(row: Mapping[str, str]) -> str:
    raw: Mapping[str, object] = row
    if set(raw) == _READING_FIELD_SET and all(isinstance(v, str) for v in raw.values()):
        return "1"
    items = sorted(
        (str(k), "str" if isinstance(v, str) else type(v).__qualname__, str(v))
        for k, v in raw.items()
        if k != "home_id"
    )
    return "0:" + hashlib.sha256(json.dumps(items, ensure_ascii=True).encode("ascii")).hexdigest()


def _row_digest_tuples(rows: Sequence[Mapping[str, str]]) -> list[tuple[str, ...]]:
    """Per-row canonical tuples binding metrics, units, identity, quality, and schema validity."""
    return sorted(
        tuple(str(row.get(f, "")) for f in _ROW_BOUND_FIELDS) + (_schema_marker(row),)
        for row in rows
    )


def _digest(home_id: str, rows: Sequence[Mapping[str, str]]) -> str:
    body = json.dumps([home_id, _row_digest_tuples(rows)], ensure_ascii=True)
    return hashlib.sha256(body.encode("ascii")).hexdigest()


def _latest(rows: Sequence[Mapping[str, str]], window: comparator.Window) -> datetime | None:
    latest: datetime | None = None
    for row in rows:
        try:
            at = comparator._time(str(row["observed_at"]))
        except (KeyError, ValueError):
            continue
        if window.start <= at < window.end and (latest is None or at > latest):
            latest = at
    return latest


def derive_signal(
    home_id: str,
    rows: Sequence[Mapping[str, str]],
    window: comparator.Window,
    as_of: datetime,
    consent: str,
    policy: AnalysisPolicy | None = None,
) -> Signal:
    """Derive one labelled signal. Reads rows only; as_of is supplied, never the wall clock."""
    policy = policy or AnalysisPolicy()
    policy.validate()
    if consent not in CONSENTS:
        raise ValueError("INVALID_CONSENT")
    if not isinstance(as_of, datetime) or as_of.utcoffset() != timedelta(0):
        raise ValueError("AS_OF_UTC_REQUIRED")
    as_of = as_of.astimezone(UTC).replace(microsecond=0)
    home_rows = _by_observation([r for r in rows if r.get("home_id") == home_id])
    digest = _digest(home_id, home_rows)

    def signal(
        sufficiency: str,
        outcome: str,
        reasons: Sequence[str],
        metrics: comparator.Analysis | None = None,
    ) -> Signal:
        return Signal(
            home_id=home_id,
            analysis_version=ANALYSIS_VERSION,
            policy_version=policy.version,
            threshold_label=policy.threshold_label,
            window_start=_stamp(window.start),
            window_end=_stamp(window.end),
            as_of=_stamp(as_of),
            sufficiency=sufficiency,
            outcome=outcome,
            reasons=tuple(sorted(reasons)),
            expected=window.expected,
            valid=metrics.valid if metrics else 0,
            coverage=metrics.coverage if metrics else 0.0,
            longest_high_hours=metrics.longest_high_hours if metrics else 0,
            high_nights=metrics.high_nights if metrics else 0,
            input_digest=digest,
        )

    if consent == "declined":
        return signal(DECLINED, INSUFFICIENT, ["MONITORING_DECLINED"])
    if consent != "granted":
        return signal(INSUFFICIENT, INSUFFICIENT, ["CONSENT_NOT_CONFIRMED"])
    latest = _latest(home_rows, window)
    if latest is None:
        return signal(STALE, INSUFFICIENT, ["NO_READINGS_IN_WINDOW"])
    if as_of - latest > timedelta(hours=policy.max_staleness_hours):
        return signal(STALE, INSUFFICIENT, ["LATEST_READING_STALE"])
    metrics = comparator.analyse(
        home_rows, window, humidity_threshold=policy.humidity_threshold_pct
    )
    if metrics.status == INSUFFICIENT:
        return signal(INSUFFICIENT, INSUFFICIENT, metrics.reasons, metrics)
    return signal(SUFFICIENT, metrics.status, [], metrics)


def _valid_home_id(value: object) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("SINGLE_HOME_REQUIRED")
    return value


def _home_and_window(
    retained_readings: Sequence[Mapping[str, str]],
    window: comparator.Window | None,
    home_id: str | None = None,
) -> tuple[str, comparator.Window]:
    explicit_home = _valid_home_id(home_id) if home_id is not None else None
    row_homes = {_valid_home_id(r.get("home_id")) for r in retained_readings}
    if explicit_home is not None:
        if row_homes and row_homes != {explicit_home}:
            raise ValueError("SINGLE_HOME_REQUIRED")
        resolved_home = explicit_home
    else:
        if len(row_homes) != 1:
            raise ValueError("SINGLE_HOME_REQUIRED")
        (resolved_home,) = row_homes
    if window is None:
        times = []
        for r in retained_readings:
            try:
                times.append(comparator._time(str(r["observed_at"])))
            except (KeyError, ValueError):
                continue
        if not times:
            raise ValueError("NO_VALID_OBSERVATIONS")
        start = min(times).replace(hour=0, minute=0, second=0, microsecond=0)
        days = (max(times) - start).days + 1
        window = comparator.Window(start, start + timedelta(days=days))
    return resolved_home, window


def policy_digest(policy: AnalysisPolicy) -> str:
    """Canonical SHA-256 digest of policy parameters and effective rule-approval state."""
    policy.validate()
    approved = (
        {
            "rule_id": policy.approval.rule_id,
            "policy_version": policy.approval.policy_version,
            "approver_role": policy.approval.approver_role,
            "approval_reference": policy.approval.approval_reference,
        }
        if policy.rule_approved and policy.approval is not None
        else None
    )
    body = json.dumps(
        {
            "policy_version": policy.version,
            "humidity_threshold_pct": _norm_float(policy.humidity_threshold_pct),
            "max_staleness_hours": policy.max_staleness_hours,
            "threshold_label": policy.threshold_label,
            "rule_id": RULE_ID,
            "rule_approved": policy.rule_approved,
            "approval": approved,
        },
        ensure_ascii=True,
        sort_keys=True,
    )
    return hashlib.sha256(body.encode("ascii")).hexdigest()


def output_digest(signal: Signal, candidate: ReviewTaskCandidate | None = None) -> str:
    """Canonical SHA-256 digest committing to the derived signal and review-task decision."""
    body = json.dumps(
        {
            "signal": asdict(signal),
            "review_task": asdict(candidate) if candidate is not None else None,
        },
        ensure_ascii=True,
        sort_keys=True,
    )
    return hashlib.sha256(body.encode("ascii")).hexdigest()


def review_task_candidate(
    signal: Signal, policy: AnalysisPolicy | None = None
) -> ReviewTaskCandidate | None:
    """Propose a human review task only for a sufficient review signal under an approved rule."""
    enforce_sensor_non_authority(signal)
    policy = policy or AnalysisPolicy()
    policy.validate()
    if (
        not policy.rule_approved
        or policy.approval is None
        or signal.sufficiency != SUFFICIENT
        or signal.outcome != REVIEW
        or signal.analysis_version != ANALYSIS_VERSION
        or signal.policy_version != policy.version
        or signal.threshold_label != policy.threshold_label
    ):
        return None
    key = hashlib.sha256(
        "|".join(
            (
                TASK_TYPE,
                signal.home_id,
                signal.window_start,
                signal.window_end,
                signal.policy_version,
                signal.input_digest,
            )
        ).encode("ascii", "replace")
    ).hexdigest()
    return ReviewTaskCandidate(
        task_key=key,
        task_type=TASK_TYPE,
        queue=TASK_QUEUE,
        home_id=signal.home_id,
        status="PROPOSED",
        rule_id=policy.approval.rule_id,
        approval_reference=policy.approval.approval_reference,
        policy_version=signal.policy_version,
        analysis_version=signal.analysis_version,
        input_digest=signal.input_digest,
        summary=(
            "Humidity stayed high in this period. A person should check the home. "
            "This is not a finding of damp or mould."
        ),
    )


def version_provenance(
    signal: Signal,
    policy: AnalysisPolicy | None = None,
    candidate: ReviewTaskCandidate | None | _Unset = _UNSET,
) -> VersionProvenance:
    """Build explicit version, policy, approval, window, and digest provenance for a signal."""
    enforce_sensor_non_authority(signal)
    if not isinstance(candidate, _Unset) and candidate is not None:
        enforce_sensor_non_authority(candidate)
    effective = policy or AnalysisPolicy()
    effective.validate()
    if (
        signal.analysis_version != ANALYSIS_VERSION
        or signal.policy_version != effective.version
        or signal.threshold_label != effective.threshold_label
    ):
        raise ValueError("SIGNAL_POLICY_MISMATCH")
    expected = review_task_candidate(signal, effective)
    if isinstance(candidate, _Unset):
        resolved = expected
    else:
        if candidate != expected:
            raise ValueError("CANDIDATE_MISMATCH")
        resolved = candidate
    approval = effective.approval if effective.rule_approved else None
    return VersionProvenance(
        home_id=signal.home_id,
        analysis_version=signal.analysis_version,
        comparator_version=COMPARATOR_VERSION,
        schema_version=SCHEMA_VERSION,
        policy_version=signal.policy_version,
        policy_digest=policy_digest(effective),
        threshold_label=signal.threshold_label,
        humidity_threshold_pct=_norm_float(effective.humidity_threshold_pct),
        max_staleness_hours=effective.max_staleness_hours,
        rule_id=RULE_ID,
        rule_approved=effective.rule_approved,
        approver_role=approval.approver_role if approval is not None else None,
        approval_reference=approval.approval_reference if approval is not None else None,
        window_start=signal.window_start,
        window_end=signal.window_end,
        as_of=signal.as_of,
        input_digest=signal.input_digest,
        output_digest=output_digest(signal, resolved),
    )


def _provenance_dict(value: VersionProvenance) -> ProvenanceDict:
    return {
        "home_id": value.home_id,
        "analysis_version": value.analysis_version,
        "comparator_version": value.comparator_version,
        "schema_version": value.schema_version,
        "policy_version": value.policy_version,
        "policy_digest": value.policy_digest,
        "threshold_label": value.threshold_label,
        "humidity_threshold_pct": value.humidity_threshold_pct,
        "max_staleness_hours": value.max_staleness_hours,
        "rule_id": value.rule_id,
        "rule_approved": value.rule_approved,
        "approver_role": value.approver_role,
        "approval_reference": value.approval_reference,
        "window_start": value.window_start,
        "window_end": value.window_end,
        "as_of": value.as_of,
        "input_digest": value.input_digest,
        "output_digest": value.output_digest,
    }


def _signal_dict(value: Signal) -> SignalDict:
    return {
        "home_id": value.home_id,
        "analysis_version": value.analysis_version,
        "policy_version": value.policy_version,
        "threshold_label": value.threshold_label,
        "window_start": value.window_start,
        "window_end": value.window_end,
        "as_of": value.as_of,
        "sufficiency": value.sufficiency,
        "outcome": value.outcome,
        "reasons": value.reasons,
        "expected": value.expected,
        "valid": value.valid,
        "coverage": value.coverage,
        "longest_high_hours": value.longest_high_hours,
        "high_nights": value.high_nights,
        "input_digest": value.input_digest,
        "priority_effect": value.priority_effect,
        "diagnoses_hazard": value.diagnoses_hazard,
    }


def _review_task_dict(value: ReviewTaskCandidate) -> ReviewTaskDict:
    return {
        "task_key": value.task_key,
        "task_type": value.task_type,
        "queue": value.queue,
        "home_id": value.home_id,
        "status": value.status,
        "rule_id": value.rule_id,
        "approval_reference": value.approval_reference,
        "policy_version": value.policy_version,
        "analysis_version": value.analysis_version,
        "input_digest": value.input_digest,
        "summary": value.summary,
        "resident_report_unaffected": value.resident_report_unaffected,
        "changes_ranking": value.changes_ranking,
        "starts_clock": value.starts_clock,
        "releases_hold": value.releases_hold,
        "diagnoses_hazard": value.diagnoses_hazard,
    }


def format_reproduced_review_task(
    provenance: VersionProvenance,
    signal: Signal,
    candidate: ReviewTaskCandidate | None,
) -> ReproducedReviewTask:
    """Format canonical serialized provenance, signal, and optional review-task candidate."""
    return {
        "provenance": _provenance_dict(provenance),
        "signal": _signal_dict(signal),
        "review_task": _review_task_dict(candidate) if candidate is not None else None,
    }


def reproduce_sensor_analysis(
    retained_readings: Sequence[Mapping[str, str]],
    thresholds: AnalysisPolicy | None = None,
    *,
    home_id: str | None = None,
    window: comparator.Window | None = None,
    as_of: datetime | None = None,
    consent: str = "granted",
) -> ReproducedSensorAnalysis:
    """Pure: re-derive the versioned output of one home from retained readings alone.

    The window defaults to the whole UTC days spanned by the readings and as_of to the window end,
    so the result depends only on the reading set, never on arrival order or the wall clock.
    """
    effective = thresholds or AnalysisPolicy()
    effective.validate()
    resolved_home, resolved_window = _home_and_window(retained_readings, window, home_id)
    signal = derive_signal(
        resolved_home,
        retained_readings,
        resolved_window,
        as_of or resolved_window.end,
        consent,
        effective,
    )
    candidate = review_task_candidate(signal, effective)
    provenance = version_provenance(signal, effective, candidate)
    return {
        "analysis_version": signal.analysis_version,
        "policy_version": signal.policy_version,
        "input_digest": signal.input_digest,
        "output_digest": provenance.output_digest,
        "provenance": _provenance_dict(provenance),
        "signal": _signal_dict(signal),
        "review_task": _review_task_dict(candidate) if candidate is not None else None,
    }


def reproduce_review_task(
    retained_readings: Sequence[Mapping[str, str]],
    policy: AnalysisPolicy | None = None,
    *,
    home_id: str | None = None,
    window: comparator.Window | None = None,
    as_of: datetime | None = None,
    consent: str = "granted",
) -> ReproducedReviewTask:
    """Pure: re-derive signal and review-task candidate with explicit version provenance."""
    effective = policy or AnalysisPolicy()
    effective.validate()
    resolved_home, resolved_window = _home_and_window(retained_readings, window, home_id)
    signal = derive_signal(
        resolved_home,
        retained_readings,
        resolved_window,
        as_of or resolved_window.end,
        consent,
        effective,
    )
    candidate = review_task_candidate(signal, effective)
    provenance = version_provenance(signal, effective, candidate)
    return format_reproduced_review_task(provenance, signal, candidate)


def as_dict(value: Signal | ReviewTaskCandidate | VersionProvenance) -> dict[str, object]:
    return asdict(value)
