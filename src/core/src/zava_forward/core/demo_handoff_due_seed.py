"""Demo seed tool: timezone-aware offer and due times for synthetic pending handoffs (Refs #2256).

    ZF_STORE=mssql ... python -m zava_forward.core.demo_handoff_due_seed inspect
    ZF_STORE=mssql ... python -m zava_forward.core.demo_handoff_due_seed apply
    ZF_STORE=mssql ... python -m zava_forward.core.demo_handoff_due_seed revert

The generated demo seed recorded some offers as a wall time without a timezone and no `due_at`.
The workflow code rightly shows those as unknown and never guesses, so the waiting list shows no
due time. This tool fixes the data, not the API. It prints counts only.

Only a pending handoff (offered, received or escalated) whose `offered_at` has no timezone is
touched. The wall time is read as Europe/London, a synthetic-demo assumption (Zava North Homes is
a UK landlord), and rewritten as an offset-aware instant. `due_at` is written only when absent, as
the offer plus a labelled demo window; the approved escalation limit (OD-09) is not involved. Each
changed handoff carries `demo_due_seed` with the original values so `revert` restores it exactly.
Handoff history events are never edited.
"""

import json
import os
import sys
from collections import Counter
from datetime import UTC, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from .workflows import HANDOFF_PENDING

MARK = "demo_due_seed"
ACTION = "demo_handoff_due_seeded"
ZONE_NAME = "Europe/London"
DUE_WINDOW_HOURS = 72


def _naive_wall_time(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip())
    except ValueError:
        return None
    return parsed if parsed.tzinfo is None else None


def plan(case: dict[str, Any]) -> tuple[datetime | None, str]:
    """Return the aware offer time to write, or None with the skip reason."""
    handoff = case.get("handoff")
    if not isinstance(handoff, dict) or handoff.get("state") not in HANDOFF_PENDING:
        return None, "no_pending_handoff"
    if isinstance(handoff.get(MARK), dict):
        return None, "already_seeded"
    wall = _naive_wall_time(handoff.get("offered_at"))
    if wall is None:
        return None, "offer_time_missing_or_already_aware"
    return wall.replace(tzinfo=ZoneInfo(ZONE_NAME)), "ok"


def run(store: Any, *, apply: bool) -> dict[str, Any]:
    skipped: Counter[str] = Counter()
    todo: list[tuple[str, datetime]] = []
    with store.lock:
        for case_id in sorted(store.cases):
            offered, reason = plan(store.cases[case_id])
            if offered is None:
                skipped[reason] += 1
            else:
                todo.append((case_id, offered))
        due_seeded = 0
        for case_id, offered in todo:
            handoff = store.cases[case_id]["handoff"]
            seed_due = not handoff.get("due_at")
            due_seeded += seed_due
            if apply:
                handoff = store._case(case_id)["handoff"]
                handoff[MARK] = {
                    "synthetic": True,
                    "offered_at_was": handoff["offered_at"],
                    "zone": ZONE_NAME,
                    "due_window_hours": DUE_WINDOW_HOURS,
                    "due_seeded": seed_due,
                }
                handoff["offered_at"] = offered.isoformat(timespec="minutes")
                if seed_due:
                    due = (offered + timedelta(hours=DUE_WINDOW_HOURS)).astimezone(UTC)
                    handoff["due_at"] = due.isoformat(timespec="minutes")
        report: dict[str, Any] = {
            "cases": len(store.cases),
            "handoffs_to_write": len(todo),
            "due_at_to_write": due_seeded,
            "skipped": dict(skipped),
            "applied": False,
        }
        if apply and todo:
            store.audit(
                "demo-handoff-due-seed",
                ACTION,
                "-",
                f"handoffs_changed={len(todo)}; due_at_seeded={due_seeded}; "
                "synthetic demo data only",
            )
            store.save()
            report["applied"] = True
    return report


def revert(store: Any) -> dict[str, Any]:
    """Undo this tool's writes by the `demo_due_seed` marker."""
    changed = []
    with store.lock:
        for case_id in sorted(store.cases):
            handoff = store.cases[case_id].get("handoff")
            if isinstance(handoff, dict) and isinstance(handoff.get(MARK), dict):
                changed.append(case_id)
        for case_id in changed:
            handoff = store._case(case_id)["handoff"]
            mark = handoff.pop(MARK)
            handoff["offered_at"] = mark["offered_at_was"]
            if mark.get("due_seeded"):
                handoff["due_at"] = None
        if changed:
            store.audit(
                "demo-handoff-due-seed",
                ACTION + "_reverted",
                "-",
                f"handoffs_reverted={len(changed)}; synthetic demo data only",
            )
            store.save()
    return {"handoffs_reverted": len(changed), "applied": bool(changed)}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or args[0] not in ("inspect", "apply", "revert"):
        print("usage: demo_handoff_due_seed inspect|apply|revert", file=sys.stderr)
        return 2
    if (os.environ.get("ZF_STORE") or "").lower() not in ("sqlite", "mssql"):
        print("ZF_STORE must be sqlite or mssql.", file=sys.stderr)
        return 2
    from .factory import open_store

    store = open_store()  # type: ignore[no-untyped-call]
    result = revert(store) if args[0] == "revert" else run(store, apply=args[0] == "apply")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
