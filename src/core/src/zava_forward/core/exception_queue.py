"""Owned exception queue for the data steward and digital operator (FR-012, FR-029, AC-040).

A store-independent register of identity and source conflicts, failed imports, failed AI or
integration runs and stranded tasks. It only records and routes: it never corrects a value,
replays a run or releases anything. Recovery is a named human request with a reason, and every
action is appended to an audit log. Role names are engineering placeholders until the owner names
the operator and steward roles.
"""

from collections.abc import Callable, Iterable, Mapping
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

Record = dict[str, Any]

STEWARD = "data_steward"
OPERATOR = "digital_operator"
ROLES = (STEWARD, OPERATOR)
CONFLICT_KINDS = ("identity_conflict", "source_conflict")
FAILURE_KINDS = ("failed_import", "failed_ai_run", "failed_integration", "stranded_task")
OWNER_ROLE = {
    "identity_conflict": STEWARD,
    "source_conflict": STEWARD,
    "failed_import": STEWARD,
    "failed_ai_run": OPERATOR,
    "failed_integration": OPERATOR,
    "stranded_task": OPERATOR,
}
RUNBOOK = {
    "identity_conflict": "Compare both records with the owner; record the chosen value and why.",
    "source_conflict": "Compare both source values with the owner; record the choice and why.",
    "failed_import": "Fix rows in the supplied workbook copy, then ask for a new preview.",
    "failed_ai_run": "Check the run record, then ask a human to re-run from the task screen.",
    "failed_integration": "Check the integration status, then ask a human to re-send.",
    "stranded_task": "Confirm the task and its owner, then reassign or close it by hand.",
}
UNKNOWN = "Unknown"
NO_AUTOMATION = (
    "Recovery is a recorded human request. Nothing is replayed or released automatically."
)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required.")
    return value.strip()


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class ExceptionQueue:
    """Items, a named-person role register and an append-only audit log."""

    def __init__(self, staff: Mapping[str, Iterable[str]], clock: Callable[[], str] = _now) -> None:
        self._staff: dict[str, tuple[str, ...]] = {}
        for name, roles in staff.items():
            held = tuple(roles)
            if any(r not in ROLES for r in held):
                raise ValueError("Roles must be data_steward or digital_operator.")
            self._staff[_text(name, "Staff name")] = held
        self._clock = clock
        self.items: dict[str, Record] = {}
        self.audit: list[Record] = []
        self.outages: dict[str, Record] = {}

    def _log(self, actor: str, action: str, item: str | None, detail: str = "") -> None:
        self.audit.append(
            {"at": self._clock(), "actor": actor, "action": action, "item": item, "detail": detail}
        )

    def _roles(self, actor: str) -> tuple[str, ...]:
        if actor not in self._staff:
            self._log(str(actor), "denied", None, "Not a named staff member.")
            raise PermissionError("Only named staff can use the exception queue.")
        if not self._staff[actor]:
            self._log(actor, "denied", None, "No operator or steward role.")
            raise PermissionError("Only a data steward or digital operator can use the queue.")
        return self._staff[actor]

    def _owner(self, kind: str, owner: str) -> str:
        name = _text(owner, "Resolution owner")
        if OWNER_ROLE[kind] not in self._staff.get(name, ()):
            raise ValueError(f"Owner must be a named {OWNER_ROLE[kind]}.")
        return name

    def _add(self, kind: str, owner: str, summary: str, original: object, extra: Record) -> Record:
        seq = len(self.items) + 1
        while f"EX-{seq:03d}" in self.items:
            seq += 1
        item_id = f"EX-{seq:03d}"
        rec: Record = {
            "id": item_id,
            "kind": kind,
            "owner": self._owner(kind, owner),
            "owner_role": OWNER_ROLE[kind],
            "summary": _text(summary, "Summary"),
            "status": "open",
            "original_source": deepcopy(original),
            "eligibility": UNKNOWN,
            "runbook": RUNBOOK[kind],
            "recovery": None,
            **extra,
        }
        self.items[item_id] = rec
        self._log(rec["owner"], "raised", item_id, kind)
        return deepcopy(rec)

    def raise_conflict(
        self,
        kind: str,
        owner: str,
        summary: str,
        values: Iterable[Mapping[str, str]],
        original_source: object,
    ) -> Record:
        """Record two or more different values, each with its source, date and version."""
        if kind not in CONFLICT_KINDS:
            raise ValueError("Kind must be identity_conflict or source_conflict.")
        shown = [
            {k: _text(v.get(k), f"Value {k}") for k in ("value", "source", "date", "version")}
            for v in values
        ]
        if len({v["value"] for v in shown}) < 2:
            raise ValueError("A conflict needs at least two different values.")
        return self._add(kind, owner, summary, original_source, {"values": shown})

    def raise_failure(
        self, kind: str, owner: str, summary: str, original_source: object, error: str
    ) -> Record:
        """Record a failed import, failed AI or integration run, or stranded task."""
        if kind not in FAILURE_KINDS:
            raise ValueError(
                "Kind must be a failed_import, failed_ai_run, failed_integration or stranded_task."
            )
        return self._add(kind, owner, summary, original_source, {"error": _text(error, "Error")})

    def queue(self, actor: str) -> list[Record]:
        """Items in the actor's role scope. Viewing is audited."""
        roles = self._roles(actor)
        self._log(actor, "viewed_queue", None, ",".join(roles))
        return [deepcopy(i) for i in self.items.values() if i["owner_role"] in roles]

    def conflict_view(self, actor: str, item_id: str) -> Record:
        item = self._item(actor, item_id)
        if "values" not in item:
            raise ValueError("This item is not a conflict.")
        self._log(actor, "viewed_conflict", item_id)
        return {
            "id": item_id,
            "values": deepcopy(item["values"]),
            "resolution_owner": item["owner"],
            "eligibility": item["eligibility"],
            "original_source": deepcopy(item["original_source"]),
        }

    def _item(self, actor: str, item_id: str) -> Record:
        roles = self._roles(actor)
        item = self.items.get(item_id)
        if item is None or item["owner_role"] not in roles:
            self._log(actor, "denied", item_id, "Outside role scope or unknown item.")
            raise PermissionError("This item is outside your role scope.")
        return item

    def request_recovery(self, actor: str, item_id: str, action: str, reason: str) -> Record:
        """Record a human recovery request. It never replays, corrects or releases."""
        item = self._item(actor, item_id)
        if item["status"] == "closed":
            raise ValueError("This item is already closed.")
        if action not in ("hold", "request_rerun", "resolve_by_owner"):
            raise ValueError("Action must be hold, request_rerun or resolve_by_owner.")
        why = _text(reason, "Reason")
        if action == "resolve_by_owner" and actor != item["owner"]:
            self._log(actor, "denied", item_id, "Only the named owner resolves.")
            raise PermissionError("Only the named resolution owner can resolve this item.")
        item["status"] = {
            "hold": "held",
            "request_rerun": "rerun_requested",
            "resolve_by_owner": "closed",
        }[action]
        item["recovery"] = {
            "action": action,
            "by": actor,
            "reason": why,
            "replayed": False,
            "released": False,
            "note": NO_AUTOMATION,
        }
        self._log(actor, action, item_id, why)
        return deepcopy(item)

    def set_outage(self, actor: str, component: str, note: str) -> None:
        if OPERATOR not in self._roles(actor):
            raise PermissionError("Only a digital operator records an outage.")
        self.outages[_text(component, "Component")] = {
            "since": self._clock(),
            "note": _text(note, "Note"),
            "recovered": False,
        }
        self._log(actor, "outage_set", None, component)

    def clear_outage(self, actor: str, component: str, evidence: str) -> None:
        if OPERATOR not in self._roles(actor):
            raise PermissionError("Only a digital operator clears an outage.")
        if component not in self.outages:
            raise KeyError(component)
        self.outages[component].update(recovered=True, evidence=_text(evidence, "Evidence"))
        self._log(actor, "outage_cleared", None, component)

    def outage_banner(self, last_checked: str | None = None) -> Record:
        """Honest staff status: an unknown check is Unknown, never healthy."""
        down = {k: dict(v) for k, v in self.outages.items() if not v["recovered"]}
        if down:
            state, text = "outage", "Some services are down: " + ", ".join(sorted(down)) + "."
        elif last_checked is None:
            state, text = (
                "unknown",
                "Service state has not been checked. Do not assume it is healthy.",
            )
        else:
            state, text = "no_known_outage", f"No outage recorded at last check ({last_checked})."
        return {"state": state, "text": text, "components": down, "last_checked": last_checked}

    def access_report(self) -> Record:
        """Visible roles and who may see which queue, plus the access audit."""
        return {
            "roles": {name: list(roles) for name, roles in self._staff.items()},
            "scope": dict(OWNER_ROLE),
            "audit": deepcopy(self.audit),
        }
