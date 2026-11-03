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

from .synthetic import sensor_scenarios as comparator

ANALYSIS_VERSION = "sensor-analysis-exercise-v1"
EXERCISE_LABEL = "EXERCISE VALUE: fictional, not sourced"
RULE_ID = "SENSOR-RH-PERSISTENCE-EXERCISE"
TASK_TYPE = "SENSOR_REVIEW_DUE"
TASK_QUEUE = "condition-assessment"
NO_SIGNAL = comparator.NO_SIGNAL
REVIEW = comparator.REVIEW
INSUFFICIENT = comparator.INSUFFICIENT
SUFFICIENT = "SUFFICIENT"
STALE = "STALE"
DECLINED = "DECLINED"
CONSENTS = ("granted", "unknown", "declined")
_LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._-]{0,79}\Z")


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


def _stamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def _digest(home_id: str, rows: Sequence[Mapping[str, str]]) -> str:
    canonical = sorted(
        json.dumps(dict(sorted(r.items())), ensure_ascii=True, sort_keys=True) for r in rows
    )
    body = json.dumps([home_id, canonical], ensure_ascii=True)
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
    home_rows = [r for r in rows if r.get("home_id") == home_id]
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


def review_task_candidate(
    signal: Signal, policy: AnalysisPolicy | None = None
) -> ReviewTaskCandidate | None:
    """Propose a human review task only for a sufficient review signal under an approved rule."""
    policy = policy or AnalysisPolicy()
    policy.validate()
    if (
        not policy.rule_approved
        or policy.approval is None
        or signal.sufficiency != SUFFICIENT
        or signal.outcome != REVIEW
        or signal.policy_version != policy.version
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


def as_dict(value: Signal | ReviewTaskCandidate) -> dict[str, object]:
    return asdict(value)
