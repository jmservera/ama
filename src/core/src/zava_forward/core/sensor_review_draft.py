"""Default-off, case-local sensor review drafts (Refs #111).

A draft is an unapproved, manual-review-only record of an existing `ReviewTaskCandidate`. It is
not a task: it creates no work, owner, handoff, queue entry, model call, ranking, hold, hazard
clock or consent change. No rule is approved here; the served policy carries no approval, so the
served write path refuses until a separately approved policy source exists (out of scope).
Constructed approvals belong only to tests through the private synthetic seam.
"""

import hashlib
import json
import os
import re
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from .sensor_analysis import (
    REVIEW,
    SUFFICIENT,
    AnalysisPolicy,
    ReviewTaskCandidate,
    Signal,
    as_dict,
    review_task_candidate,
)
from .sensor_analysis_store import analyse_retained
from .sensor_consumer import ConsumerError, SensorConsumer
from .sqlstore import CommittedReloadError, SqlStore
from .store import Store
from .synthetic.sensor_scenarios import Window

# JSON-shaped payloads: stored drafts, projections and route results have no fixed schema type.
Json = dict[str, Any]
User = Mapping[str, object]
DraftStore = Store | SqlStore

FLAG = "ZF_SENSOR_REVIEW_DRAFTS"
CASE_KEY = "sensor_review_drafts"
SCHEMA = "sensor-review-draft-v1"
STATE = "PROPOSED_UNAPPROVED"
DRAFT_ROLES = ("Quality Inspector", "Retrofit Programme Manager")
MAX_DRAFTS = 20
MANUAL_ROUTE = "manual-sensor-review"
LABEL = (
    "Proposed for a person to review. Not an approved task. Exercise rule, not a sourced standard."
)
APPROVAL_NOTE = "An approval reference was supplied but is not verified here."
WITHHELD_NOTE = "Monitoring consent is not granted now; saved drafts are withheld."
_STAMP = re.compile(r"\d{4}-\d{2}-\d{2}T00:00:00Z")
_VIEW_CANDIDATE = (
    "task_key",
    "task_type",
    "queue",
    "home_id",
    "rule_id",
    "approval_reference",
    "policy_version",
    "analysis_version",
    "input_digest",
    "summary",
    "resident_report_unaffected",
    "changes_ranking",
    "starts_clock",
    "releases_hold",
    "diagnoses_hazard",
)
_VIEW_LINEAGE = (
    "window_start",
    "window_end",
    "as_of",
    "threshold_label",
    "sufficiency",
    "outcome",
    "expected",
    "valid",
    "coverage",
    "longest_high_hours",
    "high_nights",
)


class DraftAuditError(RuntimeError):
    """The draft was committed but its audit entry could not be written (JSON store)."""

    def __init__(self, draft: Json) -> None:
        super().__init__(
            "The draft was saved, but its audit record could not be written. "
            "Do not enter it again. Tell the programme manager."
        )
        self.draft = draft


def enabled(env: Mapping[str, str] | None = None) -> bool:
    return (os.environ if env is None else env).get(FLAG) == "1"


def server_policy() -> AnalysisPolicy:
    """The policy the served routes use: no approval, so every served request is refused."""
    return AnalysisPolicy()


def _sql(store: DraftStore) -> bool:
    return hasattr(store, "dblock")


def _role_gate(user: User) -> None:
    if (user or {}).get("role") not in DRAFT_ROLES:
        raise PermissionError(
            "Your role does not include sensor review drafts. Use the manual route."
        )


def _current_staff(store: DraftStore, user: User) -> Json | None:
    email = str(user.get("email") or "").lower()
    if not isinstance(store, SqlStore):
        staff: Json | None = store.staff.get(email)
        return staff
    db = store.assistant_connection()
    try:
        row = db.execute("SELECT body FROM staff WHERE email=?", (email,)).fetchone()
    finally:
        db.close()
    loaded = json.loads(row[0]) if row else None
    return loaded if isinstance(loaded, dict) else None


def _scope(current: Json, field: str) -> list[str] | None:
    values = current.get(field)
    if values is None:
        return None
    if (
        not isinstance(values, list)
        or len(values) > 1000
        or any(not isinstance(x, str) or not 1 <= len(x) <= 128 for x in values)
    ):
        raise PermissionError("Current staff scope is malformed; resolve it manually.")
    return [str(x) for x in values]


def _gate(store: DraftStore, user: User, case_id: str, env: Mapping[str, str] | None) -> bool:
    """Role, then flag, then current staff and case scope. Returns False when disabled."""
    _role_gate(user)
    if not enabled(env):
        return False
    current = _current_staff(store, user)
    if (
        not current
        or current.get("role") != user.get("role")
        or current.get("disabled")
        or current.get("active") is False
    ):
        raise PermissionError("Current staff role has changed or been revoked.")
    ids, areas = _scope(current, "case_ids"), _scope(current, "areas")
    if ids is not None and case_id not in ids:
        raise PermissionError("Case is outside your current scope.")
    with store.lock:
        case = store.cases.get(case_id)
    if areas is not None and (case is None or case.get("home", {}).get("area") not in areas):
        raise PermissionError("Case is outside your current scope.")
    if case is None:
        raise KeyError(case_id)
    return True


def _consent_granted(store: DraftStore, case_id: str) -> bool:
    try:
        return SensorConsumer(store).home_consent(case_id) == "granted"
    except ConsumerError:
        return False


def _digest(record: Json) -> str:
    body = {k: v for k, v in record.items() if k != "draft_digest"}
    raw = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def _view(record: object) -> Json:
    """Allowlisted projection; a draft that fails its digest is withheld except for its key."""
    if not isinstance(record, dict) or record.get("draft_digest") != _digest(record):
        key = record.get("task_key") if isinstance(record, dict) else None
        return {"state": "INTEGRITY_MISMATCH", "task_key": key if isinstance(key, str) else None}
    cand, lineage = record.get("candidate") or {}, record.get("lineage") or {}
    by = record.get("created_by") or {}
    return {
        "state": record["state"],
        "label": LABEL,
        "task_key": record["task_key"],
        "candidate": {k: cand.get(k) for k in _VIEW_CANDIDATE},
        "lineage": {k: lineage.get(k) for k in _VIEW_LINEAGE},
        "approval_verified": False,
        "approval_note": APPROVAL_NOTE,
        "manual_review_only": True,
        "created_by": {"name": by.get("name"), "role": by.get("role")},
        "created_at": record["created_at"],
        "digest_prefix": str(record["draft_digest"])[:12],
        "manual_route": MANUAL_ROUTE,
    }


def read_drafts(
    store: DraftStore, user: User, case_id: str, *, env: Mapping[str, str] | None = None
) -> Json:
    if not _gate(store, user, case_id, env):
        return {"state": "disabled"}
    if not _consent_granted(store, case_id):
        return {
            "state": "consent-withheld",
            "case_id": case_id,
            "drafts": [],
            "note": WITHHELD_NOTE,
        }
    with store.lock:
        stored = list((store.cases[case_id].get(CASE_KEY) or [])[:MAX_DRAFTS])
    return {"state": "ok", "case_id": case_id, "drafts": [_view(r) for r in reversed(stored)]}


def _refusal(code: str, signal: Signal | None = None) -> Json:
    return {
        "created": False,
        "refusal": code,
        "reasons": list(signal.reasons) if signal else [],
        "manual_route": MANUAL_ROUTE,
    }


def _propose(
    store: DraftStore, user: User, case_id: str, signal: Signal, policy: AnalysisPolicy, at: str
) -> Json:
    if signal.home_id != case_id:
        return _refusal("SIGNAL_HOME_MISMATCH", signal)
    if signal.sufficiency != SUFFICIENT:
        return _refusal(f"SIGNAL_{signal.sufficiency}", signal)
    if signal.outcome != REVIEW:
        return _refusal("NO_REVIEW_SIGNAL", signal)
    if signal.window_end > signal.as_of:
        return _refusal("FUTURE_READINGS", signal)
    candidate = review_task_candidate(signal, policy)
    if candidate is None:
        return _refusal("NO_APPROVED_RULE", signal)
    return _persist(store, user, case_id, signal, candidate, at)


def _persist(
    store: DraftStore,
    user: User,
    case_id: str,
    signal: Signal,
    candidate: ReviewTaskCandidate,
    at: str,
) -> Json:
    sql = _sql(store)
    with store.lock:
        case = store._case(case_id)
        existing = list(case.get(CASE_KEY) or [])
        for record in existing:
            if isinstance(record, dict) and record.get("task_key") == candidate.task_key:
                return {"created": False, "existing": True, "draft": _view(record)}
        if len(existing) >= MAX_DRAFTS:
            return _refusal("DRAFT_LIMIT_REACHED", signal)
        sig = as_dict(signal)
        record = {
            "schema": SCHEMA,
            "state": STATE,
            "manual_review_only": True,
            "approval_verified": False,
            "activation": None,
            "task_key": candidate.task_key,
            "candidate": as_dict(candidate),
            "lineage": {k: sig[k] for k in _VIEW_LINEAGE},
            "created_by": {"name": user.get("name"), "role": user.get("role")},
            "created_at": at,
        }
        record["draft_digest"] = _digest(record)
        had_key = CASE_KEY in case
        pending = getattr(getattr(store, "local", None), "pending", None)
        mark = len(pending) if pending is not None else 0
        case[CASE_KEY] = [*existing, record]
        committed = False
        try:
            if sql:
                store.audit(
                    user["email"], "sensor_review_draft_proposed", case_id, candidate.task_key
                )
                try:
                    store.save()
                except CommittedReloadError:
                    committed = True
                    raise
                committed = True
            else:
                store.save()
                committed = True
                try:
                    store.audit(
                        user["email"], "sensor_review_draft_proposed", case_id, candidate.task_key
                    )
                except OSError as error:
                    raise DraftAuditError(_view(record)) from error
        finally:
            if not committed:
                if had_key:
                    case[CASE_KEY] = existing
                else:
                    case.pop(CASE_KEY, None)
                if pending is not None:
                    del pending[mark:]
        return {"created": True, "existing": False, "draft": _view(record)}


def _record_draft_synthetic(
    store: DraftStore,
    user: User,
    case_id: str,
    signal: Signal,
    policy: AnalysisPolicy,
    *,
    env: Mapping[str, str] | None = None,
    at: str | None = None,
) -> Json:
    """Test seam only: accepts a caller-built signal and policy. No served route reaches it."""
    if not _gate(store, user, case_id, env):
        raise PermissionError("Sensor review drafts are not enabled.")
    return _propose(store, user, case_id, signal, policy, at or _now())


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def draft_from_retained(
    store: DraftStore,
    user: User,
    case_id: str,
    window: Window,
    as_of: datetime,
    *,
    env: Mapping[str, str] | None = None,
    at: str | None = None,
) -> Json:
    if not _gate(store, user, case_id, env):
        raise PermissionError("Sensor review drafts are not enabled.")
    return _from_retained(store, user, case_id, window, as_of, at)


def _from_retained(
    store: DraftStore,
    user: User,
    case_id: str,
    window: Window,
    as_of: datetime,
    at: str | None,
) -> Json:
    try:
        consumer = SensorConsumer(store)
        signal = analyse_retained(consumer, case_id, window, as_of, server_policy())
    except ConsumerError:
        return _refusal("RETAINED_READINGS_UNAVAILABLE")
    return _propose(store, user, case_id, signal, server_policy(), at or _now())


def _parse_window(body: object) -> Window:
    if not isinstance(body, dict) or set(body) != {"window_start", "window_end"}:
        raise ValueError("Send exactly window_start and window_end.")
    stamps: list[datetime] = []
    for key in ("window_start", "window_end"):
        value = body[key]
        if not isinstance(value, str) or not _STAMP.fullmatch(value):
            raise ValueError("Give each window time as a UTC midnight, like 2024-10-01T00:00:00Z.")
        stamps.append(datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC))
    return Window(*stamps)


def draft_from_request(
    store: DraftStore,
    user: User,
    case_id: str,
    body: object,
    *,
    env: Mapping[str, str] | None = None,
    now: datetime | None = None,
) -> Json:
    """Served write: authorize, then validate the window, then analyse with the server policy."""
    if not _gate(store, user, case_id, env):
        raise PermissionError("Sensor review drafts are not enabled.")
    window = _parse_window(body)
    return _from_retained(store, user, case_id, window, now or datetime.now(UTC), None)
