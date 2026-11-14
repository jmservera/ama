"""Staff-assisted aftercare intake and joined synthetic evaluator view (FR-049, AC-063, #133).

Stage A source integration around the delivered `AftercareRegister`; it does not recreate the
register lifecycle. An existing staff member records a concern for a household or a representative
(phone, in person, paper or assisted visit), and a durable receipt is returned. The owner,
investigation, remedy and separate closure records are displayed, and a joined view lists observed
synthetic baseline and later means beside the concerns with stated denominators and Unknowns.

Synthetic exercise records only. No new permission or evaluator role is created: access reuses
existing staff role tuples. A synthetic scenario owner is labelled as such and a missing owner is
Unknown. A sensor reading is context and never dismisses a concern; closure never changes a remedy.
The free-text guard is best effort and does not prove that no personal data is present.
"""

import fcntl
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections.abc import Callable, Collection, Mapping, Sequence
from copy import deepcopy
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol, TypeVar, cast

from . import chat_privacy
from .aftercare import (
    ACCESSIBLE_ROUTE,
    CLOSURE_KINDS,
    EVALUATOR_NOTICE,
    NON_DIGITAL_CHANNELS,
    PROTECTION,
    AftercareRegister,
    assert_templates_neutral,
    intake_error_summary,
    intake_errors,
    intake_form,
    neutral_text,
    normalize_support_needed,
)
from .controls import RESIDENT_ROLES, RESIDENT_VIEW_ROLES
from .synthetic import sensor_scenarios as ss
from .workflows import MANAGER_ROLES

_redact = cast(Callable[[str], tuple[str, list[str]]], chat_privacy.redact)
Doc = dict[str, Any]
Record = dict[str, Any]
T = TypeVar("T")

FORMAT = "zf-aftercare-intake/1"
RECORD_ROLES: tuple[str, ...] = tuple(RESIDENT_ROLES)
VIEW_ROLES: tuple[str, ...] = tuple(RESIDENT_VIEW_ROLES)
MANAGER: tuple[str, ...] = tuple(MANAGER_ROLES)
UNKNOWN_OWNER = "Unknown (no owner named)"
OWNER_SUFFIX = " (synthetic scenario owner)"
COHORT_LABEL = "Synthetic handover cohort"
DEFAULT_UPDATE_DAYS = 7
REQUEST_ID = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
STATEMENT_MAX = 1000
BASIS_MAX = 200
CONTEXT_MAX_ITEMS = 10
CONTEXT_VALUE_MAX = 200
CONTEXT_KEY = re.compile(r"[A-Za-z][A-Za-z0-9 _-]{0,39}")
_INVISIBLE = dict.fromkeys([*range(0x200B, 0x2010), 0x2060, 0xFEFF])
EVIDENCE_MAX = 1000
CHANNEL_LABELS = {
    "phone": "By phone",
    "in_person": "In person",
    "paper": "On paper",
    "assisted_visit": "During an assisted visit",
}
SYNTHETIC_NOTICE = (
    "This is a demonstration with synthetic records only. Do not enter real names, contact "
    "details or health information."
)
CLOSURE_NOTE = (
    "Handover and financial closure are recorded separately. They do not change this concern, "
    "its outcome or its remedy."
)
SENSOR_NOTE = (
    "Sensor readings are context only. A normal reading does not close, lower or dismiss a concern."
)
OWNER_NOTE = "A new concern has no named owner. A manager names one afterwards."
ASSISTED_MANUAL_ROUTE = (
    "If this screen is unavailable, write the concern on paper with the "
    "channel, your name and the home reference, and give it to the named owner."
)
HOUSEHOLD_MANUAL_ROUTE = (
    "If you prefer not to use a screen, raise your concern by phone, in person, on paper "
    "or with help at a visit, and a member of staff will record it with you."
)
HOUSEHOLD_UPDATE_NOTE = (
    "We set the first update date within 7 days and a manager names the person looking into "
    "your concern."
)
COMPARISON_UNKNOWN_REASON = (
    "No usable comparison is recorded for this home, so the baseline and outcome are Unknown."
)
COMPARISON_SUFFICIENT_REASON = (
    "Descriptive observed means only. They do not show a cause, assign fault or promise savings."
)
DEFAULT_VALIDATION_MESSAGE = "Some details need fixing before this can be recorded."
STATE_INVALID_MESSAGE = (
    "The saved aftercare record is not valid, so it was left unchanged. "
    "Use the manual route and ask a person to check it."
)
STATE_UNREADABLE_MESSAGE = "The saved aftercare record could not be read, so it was left unchanged."
CONFLICT_REQUEST_MESSAGE = (
    "This request reference was already used for a different concern. Start a new record."
)
NOT_FOUND_MESSAGE = "That concern was not found."
NOT_AVAILABLE_MESSAGE = "That action is not available here."
RECEIPT_ACCESS_DENIED_MESSAGE = (
    "Provide the matching request reference from your receipt to view this concern."
)
FIXED_UNKNOWNS = (
    "Values are synthetic exercise values, not measured homes or real households.",
    "Evaluator role access is not approved yet. This view is open to existing staff roles for "
    "the demonstration only.",
    "The data protection position on outcome data is Unknown.",
    "A home with no usable comparison has an Unknown baseline and outcome.",
)
WINDOWS = {
    "baseline": "Observed means for the 7 days that end 7 days before the measurement date.",
    "early": "Observed means for the first 7 days from the measurement date.",
    "late": "Observed means for the second 7 days from the measurement date.",
}
_PRIVACY_LABELS = {
    "email": "an email address",
    "phone": "a phone number",
    "ni_number": "a national insurance number",
    "postcode": "a postcode",
    "special_category": "health or other sensitive detail",
}
_INTAKE_MESSAGES = (
    "The saved record could not be read.",
    "The record could not be opened. Nothing was saved.",
    "The record is locked. Nothing was saved.",
    "The record could not be saved. Nothing was saved.",
    "Add at least one short descriptive note.",
    "Enter a date as year-month-day, for example 2026-12-01.",
    "Choose today or a later date.",
    "Sign in again so your name can be recorded.",
    "The request reference is missing. Reload the form and try again.",
    "Choose how the household or representative raised this.",
    "This home reference is not in the demonstration set.",
    "Leave the owner blank. A manager names the owner afterwards.",
    "No owner is named for this concern yet, so nobody can act on it. "
    "A manager must name an owner first.",
    "Only the named owner role can act on this concern.",
    "Choose one of the listed owner roles.",
    "This concern already has a named owner.",
    "Choose handover or financial.",
    "Send the details as a JSON object.",
    "This is needed.",
)


assert_templates_neutral(
    UNKNOWN_OWNER,
    OWNER_SUFFIX,
    COHORT_LABEL,
    CHANNEL_LABELS,
    SYNTHETIC_NOTICE,
    CLOSURE_NOTE,
    SENSOR_NOTE,
    OWNER_NOTE,
    ASSISTED_MANUAL_ROUTE,
    HOUSEHOLD_MANUAL_ROUTE,
    HOUSEHOLD_UPDATE_NOTE,
    COMPARISON_UNKNOWN_REASON,
    COMPARISON_SUFFICIENT_REASON,
    DEFAULT_VALIDATION_MESSAGE,
    STATE_INVALID_MESSAGE,
    STATE_UNREADABLE_MESSAGE,
    CONFLICT_REQUEST_MESSAGE,
    NOT_FOUND_MESSAGE,
    NOT_AVAILABLE_MESSAGE,
    RECEIPT_ACCESS_DENIED_MESSAGE,
    FIXED_UNKNOWNS,
    WINDOWS,
    _PRIVACY_LABELS,
    _INTAKE_MESSAGES,
)


class StateInvalid(RuntimeError):
    """Stored state is unreadable or inconsistent. It is never overwritten."""


class PersistenceError(RuntimeError):
    """A write could not be completed. Nothing was saved."""


class ValidationError(ValueError):
    def __init__(self, errors: Mapping[str, str], message: str | None = None) -> None:
        self.errors = dict(errors)
        super().__init__(neutral_text(message or DEFAULT_VALIDATION_MESSAGE))


class ConflictError(RuntimeError):
    pass


class StateStore(Protocol):
    """Atomic read-modify-write over one JSON text document."""

    def read(self) -> str | None: ...

    def update(self, mutator: Callable[[str | None], tuple[str, T]]) -> T:
        """Call `mutator(current_text)` once under exclusion and store the text it returns.

        An exception from the mutator leaves the stored text unchanged and propagates.
        """
        ...


class FileStateStore:
    """File-backed store for isolated checks. The shared store must give the same atomic update."""

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)
        self.lock_path = self.path.with_name(self.path.name + ".lock")

    def read(self) -> str | None:
        try:
            return self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise PersistenceError("The saved record could not be read.") from exc

    def update(self, mutator: Callable[[str | None], tuple[str, T]]) -> T:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            lock = open(self.lock_path, "a+")  # noqa: SIM115
        except OSError as exc:
            raise PersistenceError("The record could not be opened. Nothing was saved.") from exc
        with lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX)
            except OSError as exc:
                raise PersistenceError("The record is locked. Nothing was saved.") from exc
            current = self.read()
            text, result = mutator(current)
            try:
                fd, tmp = tempfile.mkstemp(dir=self.path.parent, prefix=self.path.name)
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(text)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(tmp, self.path)
            except OSError as exc:
                raise PersistenceError("The record could not be saved. Nothing was saved.") from exc
            return result


def owner_label(role: str) -> str:
    return neutral_text(f"{role}{OWNER_SUFFIX}")


def _blank() -> Doc:
    return {
        "format": FORMAT,
        "version": 0,
        "register": AftercareRegister().to_state(),
        "receipts": {},
        "requests": {},
        "actions": [],
    }


def _fingerprint(
    raised_by: str,
    basis: str | None,
    home: str,
    kind: str,
    statement: str,
    channel: str | None,
    next_update: str | None,
    *,
    route: str = "staff_recorded",
    support_needed: Sequence[str] = (),
) -> str:
    support = list(support_needed)
    if route == "staff_recorded" and not support:
        payload: list[Any] = [raised_by, basis, home, kind, statement, channel, next_update]
    else:
        payload = [
            route,
            raised_by,
            basis,
            home,
            kind,
            statement,
            channel,
            next_update,
            support,
        ]
    return hashlib.sha256(json.dumps(payload).encode("utf-8")).hexdigest()


def _receipt_fingerprint(r: Mapping[str, Any]) -> str:
    original = r["original"]
    requested_update = original["next_update"] if "next_update" in original else r["next_update"]
    return _fingerprint(
        r["raised_by"],
        original["representative_basis"],
        r["home_ref"],
        r["kind"],
        original["statement"],
        r.get("channel"),
        requested_update,
        route=str(r.get("route", "staff_recorded")),
        support_needed=tuple(r.get("support_needed", ())),
    )


def _register(doc: Doc) -> AftercareRegister:
    return AftercareRegister.from_state(doc["register"])


def _validate(doc: object) -> Doc:
    """Cross-check the whole document so a restored store cannot weaken or orphan a record."""
    try:
        if not isinstance(doc, dict) or doc.get("format") != FORMAT:
            raise ValueError("format")
        version = doc.get("version")
        if not isinstance(version, int) or isinstance(version, bool) or version < 0:
            raise ValueError("version")
        reg = AftercareRegister.from_state(doc["register"])
        receipts, requests, actions = doc["receipts"], doc["requests"], doc["actions"]
        if not (
            isinstance(receipts, dict) and isinstance(requests, dict) and isinstance(actions, list)
        ):
            raise ValueError("shape")
        if set(receipts) != set(reg.concerns) or len(requests) != len(receipts):
            raise ValueError("receipts")
        for cid, receipt in receipts.items():
            rec = reg.concerns[cid]
            original = receipt["original"]
            basis = original["representative_basis"]
            owner_known = receipt["owner"]["status"] != "unknown"
            route = rec.get("route")
            rec_support = rec.get("support_needed", [])
            receipt_support = receipt.get("support_needed", [])
            if route == "staff_recorded":
                recorded_by = receipt.get("recorded_by")
                valid_route = (
                    rec.get("channel") in NON_DIGITAL_CHANNELS
                    and rec.get("channel") == receipt.get("channel")
                    and isinstance(recorded_by, dict)
                    and rec.get("recorded_by") == recorded_by.get("name")
                )
            elif route == "digital":
                req_update = original.get("next_update") if "next_update" in original else False
                valid_route = (
                    "channel" not in rec
                    and "recorded_by" not in rec
                    and receipt.get("channel") is None
                    and receipt.get("recorded_by") is None
                    and "next_update" in original
                    and (req_update is None or req_update == receipt["next_update"])
                )
            else:
                valid_route = False
            if (
                receipt["concern_id"] != cid
                or receipt["receipt_id"] != f"RC-{cid}"
                or receipt.get("route") != route
                or not valid_route
                or rec["home_ref"] != receipt["home_ref"]
                or rec["kind"] != receipt["kind"]
                or rec["raised_by"] != receipt["raised_by"]
                or rec_support != receipt_support
                or rec["statement"] != original["statement"].strip()
                or rec.get("representative_basis") != (basis.strip() if basis else None)
                or (owner_known and rec["owner"] != receipt["owner"]["label"])
                or requests[receipt["request_id"]]["concern_id"] != cid
                or requests[receipt["request_id"]]["fingerprint"] != _receipt_fingerprint(receipt)
            ):
                raise ValueError("receipt")
        for action in actions:
            if not all(
                isinstance(action[k], str) for k in ("at", "actor", "role", "action", "ref")
            ):
                raise ValueError("action")
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        raise StateInvalid(neutral_text(STATE_INVALID_MESSAGE)) from exc
    return doc


def _parse(text: str | None) -> Doc:
    if text is None:
        return _blank()
    try:
        return _validate(json.loads(text))
    except json.JSONDecodeError as exc:
        raise StateInvalid(neutral_text(STATE_UNREADABLE_MESSAGE)) from exc


def _guard_kinds(text: str) -> list[str]:
    """Best-effort flagged kinds after folding width, invisible characters and separators."""
    folded = unicodedata.normalize("NFKC", text).translate(_INVISIBLE)
    kinds: list[str] = []
    for candidate in (folded, folded.replace("_", " ").replace("-", " ")):
        for kind in _redact(candidate)[1]:
            if kind not in kinds:
                kinds.append(kind)
    return kinds


def _flagged(kinds: Sequence[str]) -> str:
    found = ", ".join(_PRIVACY_LABELS.get(k, k) for k in kinds)
    return neutral_text(
        f"This looks like it contains {found}. This demonstration holds synthetic "
        "records only, so take it out and describe the concern without it."
    )


def _context_errors(context: object) -> dict[str, str]:
    """Defined synthetic schema for sensor context: short descriptive text, guarded."""
    if not isinstance(context, Mapping) or not context:
        return {"context": neutral_text("Add at least one short descriptive note.")}
    if len(context) > CONTEXT_MAX_ITEMS:
        return {
            "context": neutral_text(f"Keep sensor context to {CONTEXT_MAX_ITEMS} notes or fewer.")
        }
    for position, (key, value) in enumerate(context.items(), start=1):
        if not isinstance(key, str) or not CONTEXT_KEY.fullmatch(key):
            return {
                "context": neutral_text(
                    f"Note {position}: use a short plain label of letters and numbers."
                )
            }
        if not isinstance(value, str) or not value.strip():
            return {"context": neutral_text(f"Note {position}: write a short description.")}
        if len(value) > CONTEXT_VALUE_MAX:
            return {
                "context": neutral_text(
                    f"Note {position} is too long. Keep it under {CONTEXT_VALUE_MAX}."
                )
            }
        kinds = _guard_kinds(key) + [k for k in _guard_kinds(value) if k not in _guard_kinds(key)]
        if kinds:
            return {"context": neutral_text(f"Note {position}: {_flagged(kinds)}")}
    return {}


def _free_text(value: object, field: str, label: str, cap: int, errors: dict[str, str]) -> str:
    if not isinstance(value, str) or not value.strip():
        return ""
    if len(value) > cap:
        errors[field] = neutral_text(f"{label} is too long. Keep it under {cap} characters.")
    else:
        kinds = _guard_kinds(value)
        if kinds:
            errors[field] = _flagged(kinds)
    return value


def _date(value: object, field: str, floor: str, errors: dict[str, str]) -> str:
    try:
        parsed = date.fromisoformat(str(value)).isoformat()
    except ValueError:
        errors[field] = "Enter a date as year-month-day, for example 2026-12-01."
        return ""
    if parsed < floor:
        errors[field] = "Choose today or a later date."
    return parsed


class AftercareService:
    """Existing-staff assisted intake, receipts and views over one atomic state document."""

    def __init__(
        self,
        store: StateStore,
        *,
        homes: Collection[str] | None = None,
        cohort: Collection[str] | None = None,
        scenarios: Sequence[Mapping[str, Any]] | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self.store = store
        self.scenarios: tuple[Mapping[str, Any], ...] = tuple(
            ss.retrofit_exercise_scenarios() if scenarios is None else scenarios
        )
        scenario_homes = [self._home_of(s) for s in self.scenarios]
        self.cohort: tuple[str, ...] = tuple(
            sorted(set(scenario_homes if cohort is None else cohort))
        )
        self.homes: frozenset[str] | None = None if homes is None else frozenset(homes)
        self._now = now or (lambda: datetime.now(UTC))

    @staticmethod
    def _home_of(scenario: Mapping[str, Any]) -> str:
        return str(scenario["rows"][0]["home_id"])

    def _today(self) -> str:
        return self._now().astimezone(UTC).date().isoformat()

    def _load(self) -> Doc:
        return _parse(self.store.read())

    def _txn(self, fn: Callable[[Doc], T], writes: Callable[[T], bool] = lambda _: True) -> T:
        def mutator(text: str | None) -> tuple[str, T]:
            doc = _parse(text)
            result = fn(doc)
            if text is not None and not writes(result):
                return text, result
            doc["version"] += 1
            return json.dumps(doc, sort_keys=True), result

        return self.store.update(mutator)

    @staticmethod
    def _staff(user: Mapping[str, Any] | None, roles: tuple[str, ...], what: str) -> Record:
        if not isinstance(user, Mapping) or user.get("role") not in roles:
            raise PermissionError(
                neutral_text(f"Your role cannot {what}. Ask a colleague who can.")
            )
        name = user.get("name")
        if not isinstance(name, str) or not name.strip():
            raise PermissionError(neutral_text("Sign in again so your name can be recorded."))
        return {"name": name.strip(), "role": str(user["role"])}

    def _log(self, doc: Doc, actor: Record, action: str, ref: str) -> None:
        doc["actions"].append(
            {
                "at": self._now().astimezone(UTC).isoformat(timespec="seconds"),
                "actor": actor["name"],
                "role": actor["role"],
                "action": action,
                "ref": ref,
            }
        )

    def household_form(self) -> Record:
        """Accessible self-service digital concern form for a household or representative."""
        form = intake_form()
        return {
            **form,
            "assisted": False,
            "owner_note": neutral_text(OWNER_NOTE),
            "next_update_note": neutral_text(HOUSEHOLD_UPDATE_NOTE),
            "homes": None if self.homes is None else sorted(self.homes),
            "synthetic_notice": neutral_text(SYNTHETIC_NOTICE),
            "manual_route": neutral_text(HOUSEHOLD_MANUAL_ROUTE),
        }

    def form(self, user: Mapping[str, Any] | None) -> Record:
        self._staff(user, RECORD_ROLES, "record a concern")
        form = intake_form()
        staff_fields: list[Record] = [
            {
                "name": "channel",
                "label": "How was this raised with you?",
                "required": True,
                "options": [{"value": c, "label": CHANNEL_LABELS[c]} for c in NON_DIGITAL_CHANNELS],
            },
            {"name": "next_update", "label": "Date of the next update", "required": True},
        ]
        for field in staff_fields:
            neutral_text(field["label"])
        return {
            **form,
            "assisted": True,
            "staff_fields": staff_fields,
            "owner_note": neutral_text(OWNER_NOTE),
            "owner_choices": [{"value": r, "label": owner_label(r)} for r in VIEW_ROLES],
            "homes": None if self.homes is None else sorted(self.homes),
            "synthetic_notice": neutral_text(SYNTHETIC_NOTICE),
            "manual_route": neutral_text(ASSISTED_MANUAL_ROUTE),
        }

    def submit_household_concern(self, values: Mapping[str, Any]) -> tuple[Record, bool]:
        """Submit a self-service accessible digital concern from a household or representative."""
        errors = self._household_errors(values)
        errors.update(intake_errors(values))
        if errors:
            raise ValidationError(errors, intake_error_summary(errors))
        raised_by = str(values["raised_by"])
        raw_basis = values.get("representative_basis")
        basis = str(raw_basis) if raised_by == "representative" and raw_basis is not None else None
        home = str(values["home_ref"]).strip()
        statement = str(values["statement"])
        support = normalize_support_needed(values.get("support_needed"))
        raw_update = values.get("next_update")
        requested_update = (
            None
            if raw_update is None or (isinstance(raw_update, str) and not raw_update.strip())
            else date.fromisoformat(str(raw_update)).isoformat()
        )
        request_id = str(values["request_id"])
        fingerprint = _fingerprint(
            raised_by,
            basis,
            home,
            str(values["kind"]),
            statement,
            None,
            requested_update,
            route="digital",
            support_needed=support,
        )

        def work(doc: Doc) -> tuple[Record, bool]:
            seen = doc["requests"].get(request_id)
            if seen is not None:
                if seen["fingerprint"] != fingerprint:
                    raise ConflictError(neutral_text(CONFLICT_REQUEST_MESSAGE))
                return deepcopy(doc["receipts"][seen["concern_id"]]), True
            today = self._today()
            if requested_update is not None:
                if requested_update < today:
                    raise ValidationError({"next_update": "Choose today or a later date."})
                effective_update = requested_update
            else:
                effective_update = (
                    date.fromisoformat(today) + timedelta(days=DEFAULT_UPDATE_DAYS)
                ).isoformat()
            reg = _register(doc)
            rec = reg.raise_concern(
                "digital",
                raised_by,
                home,
                str(values["kind"]),
                statement,
                UNKNOWN_OWNER,
                effective_update,
                representative_basis=basis,
                support_needed=support,
            )
            cid = str(rec["id"])
            receipt = self._receipt(
                rec,
                None,
                request_id,
                statement,
                basis,
                route="digital",
                requested_next_update=requested_update,
            )
            doc["register"] = reg.to_state()
            doc["receipts"][cid] = receipt
            doc["requests"][request_id] = {"fingerprint": fingerprint, "concern_id": cid}
            self._log(
                doc,
                {"name": raised_by, "role": "household_route"},
                "household_concern_submitted",
                cid,
            )
            return deepcopy(receipt), False

        return self._txn(work, writes=lambda outcome: not outcome[1])

    def household_receipt(self, cid: str, request_id: str) -> Record:
        """Read-only status and receipt for the raising household or representative."""
        doc = self._load()
        reg = _register(doc)
        if cid not in reg.concerns or cid not in doc["receipts"]:
            raise KeyError(cid)
        receipt = doc["receipts"][cid]
        if not isinstance(request_id, str) or receipt.get("request_id") != request_id:
            raise PermissionError(neutral_text(RECEIPT_ACCESS_DENIED_MESSAGE))
        view = reg.view(cid)
        unresolved = {r["id"] for r in reg.unresolved()}
        owner = str(view["owner"])
        return {
            "id": cid,
            "receipt_id": receipt["receipt_id"],
            "request_id": receipt["request_id"],
            "received_at": receipt["received_at"],
            "route": view["route"],
            "channel": view.get("channel"),
            "raised_by": view["raised_by"],
            "representative_basis": receipt["original"]["representative_basis"],
            "home_ref": view["home_ref"],
            "kind": view["kind"],
            "statement": receipt["original"]["statement"],
            "support_needed": list(view.get("support_needed", [])),
            "owner": {
                "label": owner,
                "status": "unknown" if owner == UNKNOWN_OWNER else "synthetic_scenario_owner",
            },
            "investigation": view["investigation"],
            "outcome": view["outcome"],
            "remedy": view["remedy"],
            "next_update": view["next_update"],
            "unresolved": cid in unresolved,
            "what_happens_next": receipt["what_happens_next"],
            "accessible_route": ACCESSIBLE_ROUTE,
            "protection": PROTECTION,
            "synthetic_notice": SYNTHETIC_NOTICE,
        }

    def record_concern(
        self, user: Mapping[str, Any] | None, values: Mapping[str, Any]
    ) -> tuple[Record, bool]:
        """Record an assisted concern. Returns the receipt and whether it was a replay."""
        actor = self._staff(user, RECORD_ROLES, "record a concern")
        errors = self._assisted_errors(actor, values)
        errors.update(intake_errors(values))
        if errors:
            raise ValidationError(errors, intake_error_summary(errors))
        raw_basis = values.get("representative_basis")
        basis = raw_basis if values["raised_by"] == "representative" else None
        home = str(values["home_ref"]).strip()
        statement = str(values["statement"])
        channel = str(values["channel"])
        support = normalize_support_needed(values.get("support_needed"))
        next_update = date.fromisoformat(str(values["next_update"])).isoformat()
        request_id = str(values["request_id"])
        fingerprint = _fingerprint(
            str(values["raised_by"]),
            basis,
            home,
            str(values["kind"]),
            statement,
            channel,
            next_update,
            route="staff_recorded",
            support_needed=support,
        )

        def work(doc: Doc) -> tuple[Record, bool]:
            seen = doc["requests"].get(request_id)
            if seen is not None:
                if seen["fingerprint"] != fingerprint:
                    raise ConflictError(neutral_text(CONFLICT_REQUEST_MESSAGE))
                return deepcopy(doc["receipts"][seen["concern_id"]]), True
            if next_update < self._today():
                raise ValidationError({"next_update": "Choose today or a later date."})
            reg = _register(doc)
            rec = reg.raise_concern(
                "staff_recorded",
                str(values["raised_by"]),
                home,
                str(values["kind"]),
                statement,
                UNKNOWN_OWNER,
                next_update,
                representative_basis=basis,
                recorded_by=actor["name"],
                channel=channel,
                support_needed=support,
            )
            cid = str(rec["id"])
            receipt = self._receipt(rec, actor, request_id, statement, basis)
            doc["register"] = reg.to_state()
            doc["receipts"][cid] = receipt
            doc["requests"][request_id] = {"fingerprint": fingerprint, "concern_id": cid}
            self._log(doc, actor, "concern_recorded", cid)
            return deepcopy(receipt), False

        return self._txn(work, writes=lambda outcome: not outcome[1])

    def _household_errors(self, values: Mapping[str, Any]) -> dict[str, str]:
        errors: dict[str, str] = {}
        if not isinstance(values.get("request_id"), str) or not REQUEST_ID.match(
            values["request_id"]
        ):
            errors["request_id"] = (
                "The request reference is missing. Reload the form and try again."
            )
        home = values.get("home_ref")
        if self.homes is not None and isinstance(home, str) and home.strip() not in self.homes:
            errors["home_ref"] = "This home reference is not in the demonstration set."
        if values.get("owner_role"):
            errors["owner_role"] = "Leave the owner blank. A manager names the owner afterwards."
        raw_update = values.get("next_update")
        if raw_update is not None and (not isinstance(raw_update, str) or raw_update.strip()):
            _date(raw_update, "next_update", "0001-01-01", errors)
        for field, label, cap in (
            ("statement", "The statement", STATEMENT_MAX),
            ("representative_basis", "The authority statement", BASIS_MAX),
        ):
            _free_text(values.get(field), field, label, cap, errors)
        return errors

    def _assisted_errors(self, actor: Record, values: Mapping[str, Any]) -> dict[str, str]:
        errors: dict[str, str] = {}
        if not isinstance(values.get("request_id"), str) or not REQUEST_ID.match(
            values["request_id"]
        ):
            errors["request_id"] = (
                "The request reference is missing. Reload the form and try again."
            )
        if values.get("channel") not in NON_DIGITAL_CHANNELS:
            errors["channel"] = "Choose how the household or representative raised this."
        home = values.get("home_ref")
        if self.homes is not None and isinstance(home, str) and home.strip() not in self.homes:
            errors["home_ref"] = "This home reference is not in the demonstration set."
        if values.get("owner_role"):
            errors["owner_role"] = "Leave the owner blank. A manager names the owner afterwards."
        _date(values.get("next_update"), "next_update", "0001-01-01", errors)
        for field, label, cap in (
            ("statement", "The statement", STATEMENT_MAX),
            ("representative_basis", "The authority statement", BASIS_MAX),
        ):
            _free_text(values.get(field), field, label, cap, errors)
        return errors

    def _receipt(
        self,
        rec: Record,
        actor: Record | None,
        request_id: str,
        statement: str,
        basis: str | None,
        *,
        route: str = "staff_recorded",
        requested_next_update: str | None = None,
    ) -> Record:
        unknown = rec["owner"] == UNKNOWN_OWNER
        if unknown:
            owner_text = "No owner is named yet. Your concern stays open and visible until a "
            owner_text += "manager names one."
        else:
            owner_text = f"{rec['owner']} will look into it."
        next_steps = (
            f"{owner_text} The next update is due on {rec['next_update']}. A normal sensor "
            "reading does not close it. You can still raise it by phone, in person or on paper."
        )
        original: Record = {"statement": statement, "representative_basis": basis}
        if route == "digital":
            original["next_update"] = requested_next_update
        return {
            "receipt_id": f"RC-{rec['id']}",
            "concern_id": rec["id"],
            "request_id": request_id,
            "received_at": self._now().astimezone(UTC).isoformat(timespec="seconds"),
            "recorded_by": (
                {"name": actor["name"], "role": actor["role"]} if actor is not None else None
            ),
            "route": route,
            "channel": rec.get("channel"),
            "raised_by": rec["raised_by"],
            "home_ref": rec["home_ref"],
            "kind": rec["kind"],
            "support_needed": list(rec.get("support_needed", [])),
            "original": original,
            "owner": {
                "label": rec["owner"],
                "status": "unknown" if unknown else "synthetic_scenario_owner",
            },
            "next_update": rec["next_update"],
            "investigation": rec["investigation"],
            "what_happens_next": neutral_text(next_steps),
            "protection": PROTECTION,
            "accessible_route": ACCESSIBLE_ROUTE,
            "synthetic_notice": SYNTHETIC_NOTICE,
        }

    def _display(self, doc: Doc, cid: str, reg: AftercareRegister) -> Record:
        rec = reg.concerns[cid]
        receipt = doc["receipts"][cid]
        unresolved = {r["id"] for r in reg.unresolved()}
        overdue = {r["id"] for r in reg.overdue(self._today())}
        owner = rec["owner"]
        return {
            "id": cid,
            "receipt_id": receipt["receipt_id"],
            "home_ref": rec["home_ref"],
            "kind": rec["kind"],
            "raised_by": rec["raised_by"],
            "representative_basis": receipt["original"]["representative_basis"],
            "route": rec["route"],
            "channel": rec.get("channel"),
            "recorded_by": rec.get("recorded_by"),
            "support_needed": list(rec.get("support_needed", [])),
            "statement": receipt["original"]["statement"],
            "owner": {
                "label": owner,
                "status": "unknown" if owner == UNKNOWN_OWNER else "synthetic_scenario_owner",
            },
            "investigation": rec["investigation"],
            "outcome": rec["outcome"],
            "remedy": rec["remedy"],
            "next_update": rec["next_update"],
            "unresolved": cid in unresolved,
            "overdue": cid in overdue,
            "closures": [
                {**c, "note": CLOSURE_NOTE}
                for c in reg.closures
                if c["home_ref"] == rec["home_ref"]
            ],
            "sensor_context": rec["sensor_context"],
            "sensor_note": SENSOR_NOTE,
            "dismissed_by_sensor": False,
            "history": rec["history"],
            "accessible_route": ACCESSIBLE_ROUTE,
            "protection": PROTECTION,
        }

    def concerns(self, user: Mapping[str, Any] | None, home_ref: str | None = None) -> Record:
        self._staff(user, VIEW_ROLES, "see aftercare concerns")
        doc = self._load()
        reg = _register(doc)
        items = [
            self._display(doc, cid, reg)
            for cid, rec in reg.concerns.items()
            if home_ref is None or rec["home_ref"] == home_ref
        ]
        return {"items": items, "count": len(items), "synthetic_notice": SYNTHETIC_NOTICE}

    def concern(self, user: Mapping[str, Any] | None, cid: str) -> Record:
        self._staff(user, VIEW_ROLES, "see aftercare concerns")
        doc = self._load()
        reg = _register(doc)
        if cid not in reg.concerns:
            raise KeyError(cid)
        return self._display(doc, cid, reg)

    def _owner_action(
        self, user: Mapping[str, Any] | None, cid: str, what: str, act: Callable[..., Any]
    ) -> Record:
        actor = self._staff(user, VIEW_ROLES, what)

        def work(doc: Doc) -> Record:
            reg = _register(doc)
            if cid not in reg.concerns:
                raise KeyError(cid)
            owner = reg.concerns[cid]["owner"]
            if owner == UNKNOWN_OWNER:
                raise PermissionError(
                    "No owner is named for this concern yet, so nobody can act on it. "
                    "A manager must name an owner first."
                )
            if owner != owner_label(actor["role"]):
                raise PermissionError("Only the named owner role can act on this concern.")
            act(reg, owner)
            doc["register"] = reg.to_state()
            self._log(doc, actor, what, cid)
            return self._display(doc, cid, reg)

        return self._txn(work)

    def start_investigation(
        self, user: Mapping[str, Any] | None, cid: str, next_update: str
    ) -> Record:
        errors: dict[str, str] = {}
        day = _date(next_update, "next_update", self._today(), errors)
        if errors:
            raise ValidationError(errors)
        return self._owner_action(
            user, cid, "start_investigation", lambda reg, o: reg.start_investigation(cid, o, day)
        )

    def record_outcome(
        self, user: Mapping[str, Any] | None, cid: str, outcome: str, basis: str, evidence: str
    ) -> Record:
        errors: dict[str, str] = {}
        _free_text(evidence, "evidence", "The evidence", EVIDENCE_MAX, errors)
        if errors:
            raise ValidationError(errors)
        return self._owner_action(
            user,
            cid,
            "record_outcome",
            lambda reg, o: reg.record_outcome(cid, o, outcome, basis, evidence),
        )

    def set_remedy(
        self, user: Mapping[str, Any] | None, cid: str, status: str, evidence: str | None = None
    ) -> Record:
        errors: dict[str, str] = {}
        _free_text(evidence, "evidence", "The evidence", EVIDENCE_MAX, errors)
        if errors:
            raise ValidationError(errors)
        return self._owner_action(
            user, cid, "set_remedy", lambda reg, o: reg.set_remedy(cid, o, status, evidence)
        )

    def assign_owner(self, user: Mapping[str, Any] | None, cid: str, owner_role: str) -> Record:
        actor = self._staff(user, MANAGER, "name an owner")
        if owner_role not in VIEW_ROLES:
            raise ValidationError({"owner_role": "Choose one of the listed owner roles."})

        def work(doc: Doc) -> Record:
            reg = _register(doc)
            if cid not in reg.concerns:
                raise KeyError(cid)
            rec = reg.concerns[cid]
            if rec["owner"] != UNKNOWN_OWNER:
                raise ConflictError("This concern already has a named owner.")
            rec["owner"] = owner_label(owner_role)
            rec["history"].append({"event": "owner_assigned"})
            doc["register"] = reg.to_state()
            self._log(doc, actor, "assign_owner", cid)
            return self._display(doc, cid, reg)

        return self._txn(work)

    def add_sensor_context(
        self, user: Mapping[str, Any] | None, cid: str, context: Mapping[str, str]
    ) -> Record:
        actor = self._staff(user, VIEW_ROLES, "add sensor context")
        errors = _context_errors(context)
        if errors:
            raise ValidationError(errors)

        def work(doc: Doc) -> Record:
            reg = _register(doc)
            if cid not in reg.concerns:
                raise KeyError(cid)
            merged = {**(reg.concerns[cid]["sensor_context"] or {}), **context}
            if len(merged) > CONTEXT_MAX_ITEMS:
                raise ValidationError(
                    {
                        "context": neutral_text(
                            f"A concern can hold {CONTEXT_MAX_ITEMS} sensor notes at most."
                        )
                    }
                )
            reg.add_sensor_context(cid, context)
            doc["register"] = reg.to_state()
            self._log(doc, actor, "add_sensor_context", cid)
            return self._display(doc, cid, reg)

        return self._txn(work)

    def record_closure(
        self, user: Mapping[str, Any] | None, home_ref: str, kind: str, closed_on: str
    ) -> Record:
        actor = self._staff(user, MANAGER, "record a closure")
        errors: dict[str, str] = {}
        if kind not in CLOSURE_KINDS:
            errors["kind"] = "Choose handover or financial."
        if self.homes is not None and home_ref.strip() not in self.homes:
            errors["home_ref"] = "This home reference is not in the demonstration set."
        _date(closed_on, "closed_on", "0001-01-01", errors)
        if errors:
            raise ValidationError(errors)

        def work(doc: Doc) -> Record:
            reg = _register(doc)
            item = reg.record_closure(home_ref, kind, closed_on, actor["role"])
            doc["register"] = reg.to_state()
            self._log(doc, actor, f"closure_{kind}", home_ref.strip())
            return {**item, "note": CLOSURE_NOTE}

        return self._txn(work)

    def evaluator_view(self, user: Mapping[str, Any] | None) -> Record:
        self._staff(user, VIEW_ROLES, "see the evaluator view")
        doc = self._load()
        reg = _register(doc)
        by_home = {self._home_of(s): s for s in self.scenarios}
        overdue = {r["id"] for r in reg.overdue(self._today())}
        unresolved = {r["id"] for r in reg.unresolved()}
        rows: list[Record] = []
        comparable: list[str] = []
        for home in self.cohort:
            comparison = self._comparison(by_home.get(home))
            if comparison["status"] == "sufficient":
                comparable.append(home)
            items = [c for c in reg.concerns.values() if c["home_ref"] == home]
            rows.append(
                {
                    "home_ref": home,
                    "case_id": by_home[home]["case_id"] if home in by_home else None,
                    "comparison": comparison,
                    "concerns": [
                        {
                            "id": c["id"],
                            "kind": c["kind"],
                            "owner": c["owner"],
                            "investigation": c["investigation"],
                            "outcome": (c["outcome"] or {}).get("outcome", "no_outcome_yet"),
                            "remedy": c["remedy"]["status"],
                            "unresolved": c["id"] in unresolved,
                            "overdue": c["id"] in overdue,
                        }
                        for c in items
                    ],
                    "unresolved_count": sum(1 for c in items if c["id"] in unresolved),
                    "closures": [c for c in reg.closures if c["home_ref"] == home],
                }
            )
        summary = reg.evaluator_view(self.cohort, baseline_homes=comparable)
        total = len(self.cohort)
        return {
            "cohort_label": neutral_text(COHORT_LABEL),
            "rows": rows,
            "windows": dict(WINDOWS),
            "totals": {
                "homes_in_cohort": total,
                "homes_with_usable_comparison": {"count": len(comparable), "denominator": total},
                "households_raising_concern": summary["households_raising_concern"],
                "concerns_raised": summary["concerns_raised"],
                "concerns_unresolved": summary["concerns_unresolved"],
                "concerns_outside_stated_scope": summary["concerns_outside_stated_scope"],
                "unresolved_with_handover_or_financial_closure": summary[
                    "unresolved_with_handover_or_financial_closure"
                ],
            },
            "register_summary": summary,
            "unknowns": [*summary["unknowns"], *FIXED_UNKNOWNS],
            "notice": neutral_text(EVALUATOR_NOTICE),
            "sensor_note": SENSOR_NOTE,
            "synthetic_notice": SYNTHETIC_NOTICE,
        }

    @staticmethod
    def _comparison(scenario: Mapping[str, Any] | None) -> Record:
        unknown: Record = {
            "status": "unknown",
            "baseline": None,
            "early": None,
            "late": None,
            "deltas": None,
            "reason": neutral_text(COMPARISON_UNKNOWN_REASON),
        }
        if scenario is None:
            return unknown
        try:
            at = datetime.fromisoformat(str(scenario["measure_at"]).replace("Z", "+00:00"))
            result: dict[str, Any] = dict(ss.retrofit_comparison(scenario["rows"], at))
        except (ValueError, KeyError, TypeError):
            return unknown
        if result["status"] != "SUFFICIENT":
            return unknown
        means: dict[str, Any] = {}
        for name, window in result["windows"].items():
            means[name] = {
                "temperature_c": window["mean_temperature_c"],
                "humidity_pct": window["mean_humidity_pct"],
            }
        return {
            "status": "sufficient",
            "baseline": means["baseline"],
            "early": means["early"],
            "late": means["late"],
            "deltas": result["deltas"],
            "reason": neutral_text(COMPARISON_SUFFICIENT_REASON),
        }

    def handle(
        self,
        method: str,
        path: str,
        user: Mapping[str, Any] | None,
        body: object = None,
        query: Mapping[str, str] | None = None,
    ) -> tuple[int, Record]:
        """Pure route contract: returns (status, payload). Hooks only delegate to this."""
        try:
            return self._route(method.upper(), path, user, body, query or {})
        except ValidationError as exc:
            return 400, {"error": neutral_text(str(exc)), "errors": exc.errors}
        except PermissionError as exc:
            return 403, {"error": neutral_text(str(exc))}
        except KeyError:
            return 404, {"error": neutral_text(NOT_FOUND_MESSAGE)}
        except ConflictError as exc:
            return 409, {"error": neutral_text(str(exc))}
        except ValueError as exc:
            return 400, {"error": neutral_text(str(exc)), "errors": {}}
        except (StateInvalid, PersistenceError) as exc:
            return 503, {"error": neutral_text(str(exc))}

    def _route(
        self,
        method: str,
        path: str,
        user: Mapping[str, Any] | None,
        body: object,
        query: Mapping[str, str],
    ) -> tuple[int, Record]:
        base = "/api/aftercare"
        parts = [p for p in path.removeprefix(base).split("/") if p]
        if not path.startswith(base) or path[len(base) :][:1] not in ("", "/"):
            raise KeyError(path)
        data: Mapping[str, Any] = {}
        if method == "POST":
            if not isinstance(body, Mapping):
                raise ValueError("Send the details as a JSON object.")
            data = body

        def text(key: str) -> str:
            value = data.get(key)
            if not isinstance(value, str):
                raise ValidationError({key: "This is needed."})
            return value

        if parts == ["form"] and method == "GET":
            return 200, self.form(user)
        if parts == ["household-form"] and method == "GET":
            return 200, self.household_form()
        if parts == ["evaluator"] and method == "GET":
            return 200, self.evaluator_view(user)
        if parts == ["household-concerns"] and method == "POST":
            receipt, replayed = self.submit_household_concern(data)
            return (200 if replayed else 201), {"receipt": receipt, "replayed": replayed}
        if len(parts) == 2 and parts[0] == "household-concerns" and method == "GET":
            return 200, self.household_receipt(parts[1], query.get("request_id", ""))
        if parts == ["concerns"]:
            if method == "GET":
                return 200, self.concerns(user, query.get("home_ref"))
            if method == "POST":
                receipt, replayed = self.record_concern(user, data)
                return (200 if replayed else 201), {"receipt": receipt, "replayed": replayed}
        if len(parts) == 2 and parts[0] == "concerns" and method == "GET":
            return 200, self.concern(user, parts[1])
        if len(parts) == 3 and parts[0] == "concerns" and method == "POST":
            cid, action = parts[1], parts[2]
            if action == "investigation":
                return 200, self.start_investigation(user, cid, text("next_update"))
            if action == "outcome":
                return 200, self.record_outcome(
                    user, cid, text("outcome"), text("basis"), text("evidence")
                )
            if action == "remedy":
                evidence = data.get("evidence")
                return 200, self.set_remedy(
                    user, cid, text("status"), evidence if isinstance(evidence, str) else None
                )
            if action == "owner":
                return 200, self.assign_owner(user, cid, text("owner_role"))
            if action == "sensor-context":
                context = data.get("context")
                if not isinstance(context, Mapping):
                    raise ValidationError({"context": "This is needed."})
                return 200, self.add_sensor_context(user, cid, context)
        if parts == ["closures"] and method == "POST":
            return 201, self.record_closure(user, text("home_ref"), text("kind"), text("closed_on"))
        known = {
            "form",
            "household-form",
            "evaluator",
            "concerns",
            "household-concerns",
            "closures",
        }
        if parts and parts[0] in known:
            return 405, {"error": neutral_text(NOT_AVAILABLE_MESSAGE)}
        raise KeyError(path)
