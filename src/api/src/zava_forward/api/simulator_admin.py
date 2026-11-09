"""Administrator start, status and stop surface for the finite simulator run control (issue 189).

It edits only the existing `live-sim-control-v1` document through `live_control`'s own guards and
`live_simulator.check_capacity`; the simulator and receiver jobs still read that file every slot.
It starts no job, calls no Azure API and changes no permission or resource. The control has no
budget-alert field, so no alert is ever reported as configured or verified here.
"""

import hashlib
import json
import os
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from zava_forward.core import identity
from zava_forward.core.synthetic.sensor_stream import StreamError, accountable_text

from . import live_control
from .live_simulator import Limits, check_capacity

PREFIX = "/api/admin/simulator-control"
ENV = "ZF_SIM_CONTROL_FILE"
TEXT_LIMIT = 160
MANUAL_ROUTE = (
    "Manual route: an operator with write access to the control file share can run "
    "python -m zava_forward.api.live_control start, stop or status. Without a valid, enabled, "
    "unexpired control the simulator sends nothing."
)
ALERT_DETAIL = (
    "The run control has no budget alert field. No budget alert is recorded or verified live "
    "(#146); the approval reference is not evidence that an alert exists."
)
MESSAGES = {
    "ADMIN_REQUIRED": "Only an application administrator can use simulator run control.",
    "CONTROL_NOT_CONFIGURED": (
        "No run control file is configured for this service. Use the manual route."
    ),
    "VIEW_ONLY": (
        "Administrator access shows every option but changes nothing; a staff role is needed "
        "to act."
    ),
    "CONFIRMATION_REQUIRED": "Tick the confirmation box before you continue.",
    "BODY_INVALID": "The request was not complete. Check every field and try again.",
    "STALE_CONTROL": (
        "The run control changed since this screen loaded. Refresh and check it first."
    ),
    "ALREADY_RUNNING": "A run is already permitted. Stop it before you start a different one.",
    "NOTHING_TO_STOP": (
        "There is no readable run control to stop. A missing or invalid control already blocks "
        "sending."
    ),
    "CONTROL_INVALID": (
        "The owner, approval reference, expiry or home list is not valid. Fix it and try again."
    ),
    "CONTROL_WINDOW_INVALID": "The expiry must be in the future and at most 14 days away.",
    "B1_QUOTA_HEADROOM": "This cohort would exceed the daily message budget. Choose fewer homes.",
    "RATE_TOO_LOW_FOR_HOMES": "This cohort cannot finish inside one slot. Choose fewer homes.",
    "NO_HOMES": "Name at least one home.",
    "CONTROL_BUSY": "Another change is in progress. Wait a moment, refresh and try again.",
    "CONTROL_UNAVAILABLE": "The run control file cannot be written here. Use the manual route.",
    "WRITE_FAILED": "The change could not be saved and nothing was changed. Use the manual route.",
    "WRITE_NOT_VERIFIED": (
        "The saved file could not be confirmed. Check it with the manual route before relying on "
        "it."
    ),
    "NOT_FOUND": "Not found.",
}
STATUS_FOR = {
    "ADMIN_REQUIRED": 403,
    "VIEW_ONLY": 403,
    "CONTROL_NOT_CONFIGURED": 503,
    "STALE_CONTROL": 409,
    "ALREADY_RUNNING": 409,
    "NOTHING_TO_STOP": 409,
    "CONTROL_BUSY": 409,
    "CONTROL_UNAVAILABLE": 503,
    "WRITE_FAILED": 503,
    "WRITE_NOT_VERIFIED": 503,
    "NOT_FOUND": 404,
}
START_FIELDS = frozenset(
    {"owner", "approval_reference", "expires_at", "homes", "expected_revision", "confirm"}
)
STOP_FIELDS = frozenset({"expected_revision", "confirm"})


class Refusal(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _reply(code: str) -> tuple[int, dict[str, Any]]:
    return STATUS_FOR.get(code, 400), {
        "error": MESSAGES.get(code, MESSAGES["BODY_INVALID"]),
        "code": code,
    }


def _path(env: Mapping[str, str]) -> Path | None:
    value = (env.get(ENV) or "").strip()
    return Path(value) if value else None


def _snapshot(path: Path) -> tuple[str, live_control.Control | None, str]:
    """Return (revision, control, availability) from one read of the file bytes."""
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return "absent", None, "unavailable"
    except OSError:
        return "unreadable", None, "unavailable"
    revision = hashlib.sha256(raw).hexdigest()
    try:
        return revision, live_control.parse(json.loads(raw.decode("utf-8"))), "configured"
    except (ValueError, StreamError):
        return revision, None, "invalid"


def _status(path: Path | None, now: datetime, read_only: bool = False) -> dict[str, Any]:
    base: dict[str, Any] = {
        "availability": "not_configured",
        "state": None,
        "activity": "unverified",
        "revision": "absent",
        "writable": False,
        "read_only": read_only,
        "manual_route": MANUAL_ROUTE,
        "budget_alert": {"status": "not_recorded", "live_verified": False, "detail": ALERT_DETAIL},
        "owner": None,
        "approval_reference": None,
        "time_limit": None,
        "cohort_size": None,
        "capacity": None,
    }
    if path is None:
        return base
    revision, control, availability = _snapshot(path)
    base |= {
        "availability": availability,
        "revision": revision,
        "writable": not read_only and os.access(path.parent, os.W_OK),
    }
    if control is None:
        return base
    try:
        capacity: dict[str, Any] = dict(check_capacity(len(control.homes), Limits()))
    except StreamError as error:
        capacity = {"refused": str(error)}
    base |= {
        "state": live_control.decide(control, now),
        "owner": {"value": control.owner, "status": "declared_unverified"},
        "approval_reference": {
            "value": control.approval_reference,
            "status": "declared_unverified",
        },
        "time_limit": {
            "expires_at": control.expires_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "max_days": live_control.MAX_WINDOW.days,
            "remaining_seconds": max(0, int((control.expires_at - now).total_seconds())),
        },
        "cohort_size": len(control.homes),
        "capacity": capacity,
    }
    return base


def _verify(path: Path, expected: live_control.Control) -> None:
    _, control, _ = _snapshot(path)
    if control != expected:
        raise Refusal("WRITE_NOT_VERIFIED")


def _write(path: Path, control: live_control.Control) -> None:
    try:
        live_control.write(path, control)
    except OSError:
        raise Refusal("WRITE_FAILED") from None
    _verify(path, control)


def _checked(body: Mapping[str, Any], fields: frozenset[str]) -> None:
    if set(body) != fields or type(body.get("expected_revision")) is not str:
        raise Refusal("BODY_INVALID")
    if body.get("confirm") is not True:
        raise Refusal("CONFIRMATION_REQUIRED")


def _clean(value: Any) -> str:
    """Owner and approval text must be plain, bounded, non-placeholder strings."""
    if not accountable_text(value) or identity.display(value, TEXT_LIMIT) != value.strip():
        raise Refusal("CONTROL_INVALID")
    return str(value).strip()


def _audit(store: Any, user: Mapping[str, Any], action: str, detail: str) -> bool:
    try:
        store.audit(user["email"], action, "-", detail)
    except Exception:
        return False
    return True


def _start(
    store: Any, user: Mapping[str, Any], body: Mapping[str, Any], path: Path, now: datetime
) -> dict[str, Any]:
    _checked(body, START_FIELDS)
    owner, approval = _clean(body["owner"]), _clean(body["approval_reference"])
    try:
        with live_control.locked(path):
            revision, current, _ = _snapshot(path)
            if body["expected_revision"] != revision:
                raise Refusal("STALE_CONTROL")
            if current is not None and live_control.decide(current, now) == live_control.SEND:
                raise Refusal("ALREADY_RUNNING")
            control = live_control.parse(
                {
                    "version": live_control.VERSION,
                    "enabled": True,
                    "expires_at": body["expires_at"],
                    "approval_reference": approval,
                    "owner": owner,
                    "homes": body["homes"],
                }
            )
            live_control.check_window(control, now)
            check_capacity(len(control.homes), Limits())
            _write(path, control)
    except StreamError as error:
        raise Refusal(str(error)) from None
    audited = _audit(
        store,
        user,
        "sim_control_start",
        f"Finite simulator run permitted for {len(control.homes)} homes until "
        f"{control.expires_at:%Y-%m-%dT%H:%M:%SZ}.",
    )
    return {"ok": True, "changed": True, "audit_recorded": audited, "status": _status(path, now)}


def _stop(
    store: Any, user: Mapping[str, Any], body: Mapping[str, Any], path: Path, now: datetime
) -> dict[str, Any]:
    _checked(body, STOP_FIELDS)
    try:
        with live_control.locked(path):
            revision, current, _ = _snapshot(path)
            if body["expected_revision"] != revision:
                raise Refusal("STALE_CONTROL")
            if current is None:
                raise Refusal("NOTHING_TO_STOP")
            if not current.enabled:
                return {
                    "ok": True,
                    "changed": False,
                    "audit_recorded": None,
                    "status": _status(path, now),
                }
            _write(
                path,
                live_control.Control(
                    False,
                    current.expires_at,
                    current.approval_reference,
                    current.owner,
                    current.homes,
                ),
            )
    except StreamError as error:
        raise Refusal(str(error)) from None
    audited = _audit(
        store, user, "sim_control_stop", "Finite simulator run stopped by an administrator."
    )
    return {"ok": True, "changed": True, "audit_recorded": audited, "status": _status(path, now)}


def handles(path: str) -> bool:
    return path == PREFIX or path.startswith(PREFIX + "/")


def handle(
    store: Any,
    user: Mapping[str, Any],
    method: str,
    path: str,
    body: Mapping[str, Any] | None = None,
    env: Mapping[str, str] | None = None,
    now: datetime | None = None,
) -> tuple[int, dict[str, Any]]:
    """Serve one request under PREFIX; authorize first and disclose nothing on refusal."""
    if not (
        isinstance(user, Mapping)
        and user.get("app_admin") is True
        and identity.verified(dict(user)) is not None
    ):
        return _reply("ADMIN_REQUIRED")
    read_only = bool(user.get("view_only"))
    if method != "GET" and read_only:
        return _reply("VIEW_ONLY")
    environment = os.environ if env is None else env
    moment = now or datetime.now(UTC)
    target = _path(environment)
    try:
        if method == "GET" and path == PREFIX:
            return 200, _status(target, moment, read_only)
        action = {PREFIX + "/start": _start, PREFIX + "/stop": _stop}.get(path)
        if method != "POST" or action is None:
            return _reply("NOT_FOUND")
        if target is None:
            return _reply("CONTROL_NOT_CONFIGURED")
        return 200, action(store, user, body or {}, target, moment)
    except Refusal as refusal:
        return _reply(refusal.code)
