"""Read-only exception register for named data stewards and digital operators (FR-029, #135).

It rebuilds the owned exception queue from records the store already keeps and returns it with
the access scope and an honest outage banner. It never corrects a value, replays a run, re-sends
or releases anything, and it stores no recovery action. Named staff come from configuration
because the owner has not yet named the operator and steward roles (open decision on #135).
"""

import json
from collections.abc import Mapping
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

from . import continuity, import_refusals, taskqueues
from .exception_feeds import (
    feed_failed_ai_runs,
    feed_failed_imports,
    feed_stock_conflicts,
    feed_stranded_tasks,
    feed_unaccepted_handoffs,
)
from .exception_queue import (
    ALLOWED_ACTIONS,
    NO_AUTOMATION,
    OPERATOR,
    ROLES,
    STEWARD,
    ExceptionQueue,
)

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
IMPORT_WITH_BATCHES_CONNECTED = (
    "Failed imports: {refusals} refused import file(s) and {batches} rejected import batch(es) "
    "are stored here and {shown} are shown in this view. They are shown only to the configured "
    "data steward. Unsynced external failures are not shown. Check the importer by hand."
)
NO_HEALTH_CHECK = "No service health check feeds this register, so service state is Unknown."
OUTAGE_RECORDED_NO_PROBE = (
    "Service outages: {n} active suspension or outage record(s) feed the banner above; "
    "no automated live service health check is connected."
)
ROLES_NOT_NAMED = (
    "No data steward or digital operator is named yet. The queue stays empty until the "
    "programme owner names them; nothing is assigned by default."
)
NOTE = (
    "Viewing changes nothing. Recovery is a recorded, audited human request; nothing is "
    "replayed, corrected, re-sent or released automatically."
)
RECOVERY_AUDIT = "exception_recovery_requested"
RECOVERY_STATUS = {
    "hold": "held",
    "request_rerun": "rerun_requested",
    "resolve_by_owner": "closed",
}


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
        from .workflows import MANAGER_ROLES

        email = str(user.get("email", "")).lower()
        if not staff:
            if user.get("role") not in MANAGER_ROLES:
                self._audit_register(
                    email, "denied", "Exception register: no steward or operator named."
                )
                raise PermissionError("Only a named data steward or digital operator can see this.")
            self._audit_register(email, "viewed_exception_register", "state=roles_not_named")
            unrouted_empty = [ROLES_NOT_NAMED]
            empty_queue = ExceptionQueue({})
            with self.lock:
                stored = self._stored_refusals()
                _, stored_batches = self._rejected_batches(unrouted_empty)
                active_outages = self._apply_detected_outages(empty_queue)
            return {
                "state": "roles_not_named",
                "items": [],
                "unrouted": unrouted_empty,
                "sources": self._exception_sources(stored, 0, stored_batches, active_outages),
                "banner": empty_queue.outage_banner(None),
                "access": {
                    "roles": {},
                    "viewer_roles": [],
                    "allowed_kinds": [],
                    "scope": {},
                },
                "note": NOTE,
            }
        if email not in staff:
            self._audit_register(
                email, "denied", "Exception register: not a named steward or operator."
            )
            raise PermissionError("Only a named data steward or digital operator can see this.")

        queue, unrouted, stored, stored_batches, active_outages = self._build_exception_queue(
            staff, as_of
        )
        items = self._with_recoveries(queue.queue(email))
        shown = sum(1 for item in items if item.get("kind") == "failed_import")
        report = queue.access_report(email)
        viewer_roles = list(report["roles"].get(email, []))
        allowed_kinds = [k for k, r in report["scope"].items() if r in viewer_roles]
        with self.lock:
            self._audit_register(email, "viewed_exception_register", f"items={len(items)}")
        return {
            "state": "ok",
            "items": items,
            "unrouted": unrouted,
            "sources": self._exception_sources(stored, shown, stored_batches, active_outages),
            "banner": queue.outage_banner(None),
            "access": {
                "roles": {email: viewer_roles},
                "viewer_roles": list(viewer_roles),
                "allowed_kinds": allowed_kinds,
                "scope": report["scope"],
            },
            "note": NOTE,
        }

    def _build_exception_queue(
        self, staff: Mapping[str, tuple[str, ...]], as_of: str | None
    ) -> tuple[ExceptionQueue, list[str], int | None, int | None, int]:
        from .workflows import handoff_ageing, handoff_view

        as_of = as_of or datetime.now(UTC).isoformat(timespec="seconds")
        queue = ExceptionQueue(staff)
        steward, operator = _owner(staff, STEWARD), _owner(staff, OPERATOR)
        unrouted: list[str] = []
        with self.lock:
            active_outages = self._apply_detected_outages(queue)
            cases = list(self.cases.values())
            refused = self._import_refusals(unrouted)
            stored = self._stored_refusals()
            rejected_batches, stored_batches = self._rejected_batches(unrouted)
            if steward:
                self._route_refusals(queue, refused, steward, unrouted)
                self._route_batches(queue, rejected_batches, steward, unrouted)
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
                if rejected_batches:
                    unrouted.append(
                        f"No named data steward: {len(rejected_batches)} rejected import "
                        "batch(es) are not routed."
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
                policy = self.data.get("handoff_policy")
                staff_rows = self.data.get("staff")
                for case in cases:
                    if case.get("closed"):
                        continue
                    try:
                        overdue = taskqueues.overdue_tasks(
                            case,
                            as_of=as_of,
                            handoff=handoff_view(  # type: ignore[no-untyped-call]
                                case, as_of=as_of, policy=policy, staff=staff_rows
                            ),
                        )
                        row = handoff_ageing(  # type: ignore[no-untyped-call]
                            case, as_of, policy=policy
                        )
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
        return queue, unrouted, stored, stored_batches, active_outages

    @staticmethod
    def recovery_key(item: Mapping[str, Any]) -> str | None:
        """Stable key for an item across rebuilds; None when its feed gave it no ref."""
        ref = item.get("ref")
        return f"{item['kind']}:{ref}" if ref else None

    def _recovery_requests(self) -> dict[str, list[dict[str, Any]]]:
        """Ordered recorded requests per item key, read from the tamper-evident audit ledger."""
        history: dict[str, list[dict[str, Any]]] = {}
        audit_entries = getattr(self, "audit_entries", None)
        for entry in audit_entries() if callable(audit_entries) else ():
            if entry.get("action") != RECOVERY_AUDIT:
                continue
            try:
                detail = json.loads(entry["detail"])
                key = str(entry["case"])
                history.setdefault(key, []).append(
                    {
                        "action": str(detail["action"]),
                        "reason": str(detail["reason"]),
                        "by": str(entry["who"]),
                        "at": str(entry["at"]),
                        "replayed": False,
                        "released": False,
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue
        return history

    def _with_recoveries(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        requests = self._recovery_requests()
        decorated: list[dict[str, Any]] = []
        for raw in items:
            item = deepcopy(raw)
            key = self.recovery_key(item)
            item["recovery_key"] = key
            allowed = ALLOWED_ACTIONS[item["kind"]]
            trail = [
                dict(r) for r in (requests.get(key, []) if key else []) if r["action"] in allowed
            ]
            item["audit_trail"] = trail
            if trail:
                latest = trail[-1]
                item["status"] = RECOVERY_STATUS[latest["action"]]
                item["recovery"] = {
                    **latest,
                    "automatic_replay": False,
                    "automatic_release": False,
                    "note": NO_AUTOMATION,
                    "audit_trail": deepcopy(trail),
                }
            decorated.append(item)
        return decorated

    def request_exception_recovery(
        self,
        user: Mapping[str, str],
        staff: Mapping[str, tuple[str, ...]],
        key: object,
        action: object,
        reason: object,
    ) -> dict[str, Any]:
        """Record one human recovery request for an item in the actor's scope.

        It writes only an audit entry. It never replays, corrects, re-sends or releases, and
        the original source and unresolved eligibility on the item stay as they were.
        """
        email = str(user.get("email", "")).lower()
        if email not in staff:
            self._audit_register(email, "denied", "Exception recovery: not named staff.")
            raise PermissionError("Only a named data steward or digital operator can do this.")
        if not isinstance(key, str) or not isinstance(action, str):
            raise ValueError("An item and an action are required.")
        why = reason.strip() if isinstance(reason, str) else ""
        if not why or len(why) > 400:
            raise ValueError("A reason of up to 400 characters is required.")
        queue, _, _, _, _ = self._build_exception_queue(staff, None)
        scoped = self._with_recoveries(queue.queue(email))
        item = next((i for i in scoped if i["recovery_key"] == key), None)
        if item is None:
            self._audit_register(email, "denied", f"Exception recovery: {key[:80]} out of scope.")
            raise PermissionError("This item is outside your role scope or no longer exists.")
        if item["status"] == "closed":
            raise ValueError("This item is already closed.")
        if action not in ALLOWED_ACTIONS[item["kind"]]:
            raise ValueError(
                "Action for this item must be one of: " + ", ".join(ALLOWED_ACTIONS[item["kind"]])
            )
        if action == "resolve_by_owner" and email != item["owner"]:
            self._audit_register(email, "denied", f"Exception recovery: {key[:80]} not owner.")
            raise PermissionError("Only the named resolution owner can resolve this item.")
        detail = json.dumps({"action": action, "reason": why}, sort_keys=True)
        self.audit(email, RECOVERY_AUDIT, key, detail)  # type: ignore[attr-defined]
        return self._with_recoveries([item])[0]

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

    @staticmethod
    def _route_batches(
        queue: ExceptionQueue,
        rejected: list[Mapping[str, Any]],
        steward: str,
        unrouted: list[str],
    ) -> None:
        for batch in rejected:
            try:
                feed_failed_imports(queue, [batch], steward)
            except (KeyError, TypeError, ValueError, AttributeError):
                label = str(batch.get("batch_id") or "Unknown")
                unrouted.append(
                    f"Rejected import batch {label} could not be routed. "
                    "Check the importer by hand."
                )

    def _rejected_batches(self, unrouted: list[str]) -> tuple[list[Mapping[str, Any]], int | None]:
        """Read-only projection of rejected importer batches without mutating store data."""
        raw_top = self.data.get("import_batches")
        doc = self.data.get(import_refusals.KEY)
        raw_doc = doc.get("rejected_batches") if isinstance(doc, Mapping) else None
        if raw_top is None and raw_doc is None:
            return [], None
        valid_source = False
        seen: set[str] = set()
        rejected: list[Mapping[str, Any]] = []
        for raw in (raw_top, raw_doc):
            if raw is None:
                continue
            if not isinstance(raw, list):
                unrouted.append(
                    "Rejected import batches could not be read, so rejected batches are not "
                    "routed. Check the importer by hand."
                )
                continue
            valid_source = True
            for entry in raw:
                if not isinstance(entry, Mapping):
                    unrouted.append(
                        "A rejected import batch entry could not be read, so it is not routed. "
                        "Check the importer by hand."
                    )
                    continue
                if entry.get("status") != "rejected":
                    continue
                batch_key = str(entry.get("batch_id") or f"idx:{len(rejected)}")
                if batch_key not in seen:
                    seen.add(batch_key)
                    rejected.append(entry)
        if not valid_source:
            return [], None
        return rejected, len(rejected)

    def _apply_detected_outages(self, queue: ExceptionQueue) -> int:
        """Project active AI continuity suspensions and recorded service outages onto queue."""
        invalid_note = (
            "AI continuity history could not be verified; AI serving is treated as suspended."
        )
        cont = self.data.get("continuity")
        if cont is not None:
            if not isinstance(cont, Mapping):
                queue.record_detected_outage("ai-continuity", invalid_note)
            else:
                doc = {
                    "epoch": cont.get("epoch", 0),
                    "suspensions": cont.get("suspensions", []),
                    "changes": cont.get("changes", []),
                }
                if not continuity.history_valid(doc):  # type: ignore[no-untyped-call]
                    queue.record_detected_outage("ai-continuity", invalid_note)
                else:
                    for susp in doc["suspensions"]:
                        if not isinstance(susp, Mapping):
                            continue
                        if susp.get("status") == "Suspended" or susp.get("actual_hold", True):
                            scope = str(susp.get("scope") or "all")
                            comp = "ai-tasks (all)" if scope == "all" else f"ai-task:{scope}"
                            inc = susp.get("incident_owner")
                            if isinstance(inc, str) and inc.strip():
                                inc_name = inc.strip()
                            elif isinstance(inc, Mapping) and inc.get("name"):
                                inc_name = str(inc["name"])
                            else:
                                inc_name = "incident owner"
                            reason_txt = str(
                                susp.get("reason")
                                or "AI assistance suspended; manual work continues."
                            )
                            since_raw = susp.get("at") or susp.get("restarted_at")
                            since = (
                                str(since_raw)
                                if isinstance(since_raw, str) and since_raw.strip()
                                else None
                            )
                            queue.record_detected_outage(
                                comp,
                                f"Suspended (incident owner: {inc_name}): {reason_txt}",
                                since=since,
                            )
        raw_outages = self.data.get("service_outages")
        if isinstance(raw_outages, Mapping):
            for comp_name, info in raw_outages.items():
                if isinstance(info, Mapping) and not info.get("recovered"):
                    since_raw = info.get("since")
                    since = (
                        str(since_raw) if isinstance(since_raw, str) and since_raw.strip() else None
                    )
                    try:
                        queue.record_detected_outage(
                            str(comp_name),
                            str(info.get("note") or "Service outage recorded."),
                            since=since,
                        )
                    except ValueError:
                        continue
        elif isinstance(raw_outages, list):
            for info in raw_outages:
                if isinstance(info, Mapping) and not info.get("recovered"):
                    comp_raw = info.get("component") or info.get("name")
                    if not isinstance(comp_raw, str) or not comp_raw.strip():
                        continue
                    since_raw = info.get("since")
                    since = (
                        str(since_raw) if isinstance(since_raw, str) and since_raw.strip() else None
                    )
                    try:
                        queue.record_detected_outage(
                            comp_raw,
                            str(info.get("note") or "Service outage recorded."),
                            since=since,
                        )
                    except ValueError:
                        continue
        return len(queue.outage_banner(None)["components"])

    def _stored_refusals(self) -> int | None:
        """Stored refusal count; None when none were transferred or the document is damaged."""
        try:
            refused = import_refusals.load(self.data)
        except ValueError:
            return None
        return None if refused is None else len(refused)

    @staticmethod
    def _exception_sources(
        stored: int | None,
        shown: int,
        stored_batches: int | None = None,
        active_outages: int = 0,
    ) -> list[str]:
        health = (
            OUTAGE_RECORDED_NO_PROBE.format(n=active_outages)
            if active_outages > 0
            else NO_HEALTH_CHECK
        )
        if stored_batches is not None:
            return [
                IMPORT_WITH_BATCHES_CONNECTED.format(
                    refusals=stored or 0, batches=stored_batches, shown=shown
                ),
                health,
            ]
        if stored is None:
            return [NOT_CONNECTED, health]
        return [IMPORT_CONNECTED.format(n=stored, shown=shown), health]
