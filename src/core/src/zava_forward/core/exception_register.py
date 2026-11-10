"""Read-only exception register for named data stewards and digital operators (FR-029, #135).

It rebuilds the owned exception queue from records the store already keeps and returns it with
the access scope and an honest outage banner. It never corrects a value, replays a run, re-sends
or releases anything, and it stores no recovery action. Named staff come from configuration
because the owner has not yet named the operator and steward roles (open decision on #135).
"""

import json
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from . import import_refusals, taskqueues
from .exception_feeds import (
    feed_failed_ai_runs,
    feed_failed_imports,
    feed_stock_conflicts,
    feed_stranded_tasks,
    feed_unaccepted_handoffs,
)
from .exception_queue import OPERATOR, ROLES, STEWARD, ExceptionQueue

STAFF_ENV = "ZF_EXCEPTION_STAFF"
NOT_CONNECTED = (
    "Failed imports are not connected to this register yet: the importer does not report "
    "rejected batches here. Check the importer by hand."
)
IMPORT_CONNECTED = (
    "Failed imports: {n} refused import file(s) are stored here from the importer's ledger and "
    "{shown} are shown in this view. They are shown only to the configured data steward. "
    "Rejected batches and other failures are not connected, and a refusal not yet transferred "
    "is not shown. Check the importer by hand."
)
NO_HEALTH_CHECK = "No service health check feeds this register, so service state is Unknown."
ROLES_NOT_NAMED = (
    "No data steward or digital operator is named yet. The queue stays empty until the "
    "programme owner names them; nothing is assigned by default."
)
NOTE = "Read-only. Recovery is a recorded human request made elsewhere; nothing is replayed."


def staff_from_env(env: Mapping[str, str]) -> dict[str, tuple[str, ...]]:
    """Parse ZF_EXCEPTION_STAFF, a JSON object of staff email to roles. Bad input names nobody."""
    raw = env.get(STAFF_ENV, "").strip()
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except ValueError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    staff: dict[str, tuple[str, ...]] = {}
    for name, roles in parsed.items():
        if (
            isinstance(name, str)
            and name.strip()
            and isinstance(roles, list)
            and roles
            and all(r in ROLES for r in roles)
        ):
            staff[name.strip().lower()] = tuple(roles)
    return staff


def _owner(staff: Mapping[str, tuple[str, ...]], role: str) -> str | None:
    return next((n for n in sorted(staff) if role in staff[n]), None)


class ExceptionRegisterMixin:
    cases: dict[str, Any]
    data: dict[str, Any]
    lock: Any

    def exception_register(
        self,
        user: Mapping[str, str],
        staff: Mapping[str, tuple[str, ...]],
        as_of: str | None = None,
    ) -> dict[str, Any]:
        """The viewer's exception queue, access report and outage banner. Viewing is audited."""
        from .workflows import MANAGER_ROLES, handoff_ageing, handoff_view

        email = str(user.get("email", "")).lower()
        if not staff:
            if user.get("role") not in MANAGER_ROLES:
                self._audit_register(
                    email, "denied", "Exception register: no steward or operator named."
                )
                raise PermissionError("Only a named data steward or digital operator can see this.")
            self._audit_register(email, "viewed_exception_register", "state=roles_not_named")
            with self.lock:
                stored = self._stored_refusals()
            return {
                "state": "roles_not_named",
                "items": [],
                "unrouted": [ROLES_NOT_NAMED],
                "sources": self._exception_sources(stored, 0),
                "banner": ExceptionQueue({}).outage_banner(None),
                "access": {"roles": {}, "scope": {}},
                "note": NOTE,
            }
        if email not in staff:
            self._audit_register(
                email, "denied", "Exception register: not a named steward or operator."
            )
            raise PermissionError("Only a named data steward or digital operator can see this.")

        as_of = as_of or datetime.now(UTC).isoformat(timespec="seconds")
        queue = ExceptionQueue(staff)
        steward, operator = _owner(staff, STEWARD), _owner(staff, OPERATOR)
        unrouted: list[str] = []
        with self.lock:
            cases = list(self.cases.values())
            refused = self._import_refusals(unrouted)
            stored = self._stored_refusals()
            if steward:
                self._route_refusals(queue, refused, steward, unrouted)
                for case in cases:
                    try:
                        feed_stock_conflicts(queue, [case], steward)
                    except (KeyError, TypeError, ValueError, AttributeError):
                        unrouted.append(
                            f"Case {self._case_label(case)}: stock query could not be read, so "
                            "its conflicts are not routed. Open the case."
                        )
            else:
                unrouted.append("No named data steward: conflicts are not routed.")
                if refused:
                    unrouted.append(
                        f"No named data steward: {len(refused)} refused import file(s) "
                        "are not routed."
                    )
            if operator:
                for rec in self.data.get("recommendations", []):
                    try:
                        feed_failed_ai_runs(queue, [rec], operator)
                    except (KeyError, TypeError, ValueError, AttributeError):
                        unrouted.append(
                            f"Recommendation {self._case_label(rec)}: record could not be read, "
                            "so a failed AI run is not routed."
                        )
                for case in cases:
                    if case.get("closed"):
                        continue
                    try:
                        overdue = taskqueues.overdue_tasks(
                            case,
                            as_of=as_of,
                            handoff=handoff_view(case),  # type: ignore[no-untyped-call]
                        )
                        row = handoff_ageing(case, as_of)  # type: ignore[no-untyped-call]
                        feed_stranded_tasks(queue, overdue, operator)
                        if row:
                            feed_unaccepted_handoffs(queue, [row], operator)
                    except (KeyError, TypeError, ValueError, AttributeError):
                        unrouted.append(
                            f"Case {self._case_label(case)}: task or handoff record could "
                            "not be read, so stranded work is not checked. Open the case."
                        )
            else:
                unrouted.append("No named digital operator: failed runs and tasks are not routed.")
        items = queue.queue(email)
        shown = sum(1 for item in items if item.get("kind") == "failed_import")
        report = queue.access_report(email)
        with self.lock:
            self._audit_register(email, "viewed_exception_register", f"items={len(items)}")
        return {
            "state": "ok",
            "items": items,
            "unrouted": unrouted,
            "sources": self._exception_sources(stored, shown),
            "banner": queue.outage_banner(None),
            "access": {
                "roles": {email: list(report["roles"].get(email, []))},
                "scope": report["scope"],
            },
            "note": NOTE,
        }

    def _audit_register(self, email: str, action: str, detail: str) -> None:
        self.audit(email, action, "-", detail)  # type: ignore[attr-defined]

    @staticmethod
    def _case_label(record: Any) -> str:
        return str(record.get("id", "Unknown")) if isinstance(record, Mapping) else "Unknown"

    def _import_refusals(self, unrouted: list[str]) -> list[dict[str, str]]:
        try:
            return import_refusals.load(self.data) or []
        except ValueError:
            unrouted.append(
                "Transferred import refusals could not be read, so refused import files are not "
                "routed. Check the importer by hand."
            )
            return []

    @staticmethod
    def _route_refusals(
        queue: ExceptionQueue,
        refused: list[dict[str, str]],
        steward: str,
        unrouted: list[str],
    ) -> None:
        shown = [
            {**r, "reason": f"{r['reason']} Refused at {r['at']}."}
            for r in sorted(refused, key=lambda r: (r["at"], import_refusals.ref_of(r)))
        ]
        try:
            feed_failed_imports(queue, [], steward, shown)
        except ValueError:
            unrouted.append(
                f"{len(refused)} refused import file(s) could not be routed. "
                "Check the importer by hand."
            )

    def _stored_refusals(self) -> int | None:
        """Stored refusal count; None when none were transferred or the document is damaged."""
        try:
            refused = import_refusals.load(self.data)
        except ValueError:
            return None
        return None if refused is None else len(refused)

    @staticmethod
    def _exception_sources(stored: int | None, shown: int) -> list[str]:
        if stored is None:
            return [NOT_CONNECTED, NO_HEALTH_CHECK]
        return [IMPORT_CONNECTED.format(n=stored, shown=shown), NO_HEALTH_CHECK]
