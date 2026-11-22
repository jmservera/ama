"""One-off private tool: give synthetic demo hazards an awareness time (Refs #2255).

Run it only inside the private network (the demo SQL server has public access Disabled), for
example in the demo API replica, with the app's own `ZF_STORE=mssql` and `ZF_SQL_*` settings. It
prints counts only: no hazard text, names or e-mail addresses.

  inspect [N]   report how many open hazards lack `aware_at` and what the backfill would do.
  revert        undo every change this tool made, found by its `demo_clock_seed` marker.
  apply [N]     write `aware_at` on those hazards through the normal store save and audit path.

The queue clock reads time against the dataset `as_of` snapshot, so that is the reference "now"
(the wall clock only when the store has none); an anchor after it is skipped.

Only an open, non-safeguarding hazard with no `aware_at` is touched. The awareness time comes
from the hazard's own `recorded_at` instant, else its `noticed` date at 09:00 UTC; an anchor in
the future or missing is skipped. That keeps the record honest but, for old demo data, leaves every
clock overdue. N (default 0) picks N hazards spread evenly across the sorted list to be re-dated
so the clock is running: `aware_at` becomes 40 percent of the existing reference window before
the reference time and `noticed` follows its date. The original `noticed` is kept in the marker.

The response target is the existing reference window from awareness, written as `response_due_at`
only when it is absent, because the queue text shows a target window only from that field. No
other service time (`responded_at`, resident update times) is written, so the hazard service
still owns every real response and update. Each changed hazard carries `demo_clock_seed` so the synthetic origin stays
visible.
"""

import json
import os
import sys
from collections import Counter
from datetime import UTC, datetime, timedelta
from typing import Any

MARK = "demo_clock_seed"
ACTION = "demo_hazard_clock_seeded"
WINDOW_HOURS = {"EMERGENCY": 24, "ROUTINE": 336}
RUNNING_SHARE = 0.4


def _instant(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip())
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _stamp(moment: datetime) -> str:
    return moment.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def window_hours(hazard: dict[str, Any]) -> int:
    """The reference window the existing queue clock applies to this hazard."""
    priority = str(hazard.get("priority") or "").upper()
    if priority == "SIGNIFICANT" and hazard.get("accepted_at"):
        return 336
    return WINDOW_HOURS.get(priority, 168)


def anchor(hazard: dict[str, Any]) -> datetime | None:
    """The existing record time to reuse as awareness, or None."""
    recorded = _instant(hazard.get("recorded_at"))
    if recorded is not None:
        return recorded
    noticed = hazard.get("noticed")
    if isinstance(noticed, str) and len(noticed) == 10:
        return _instant(noticed + "T09:00:00Z")
    return None


def plan(case: dict[str, Any], now: datetime) -> tuple[list[tuple[int, datetime]], Counter[str]]:
    """Return (hazard index, awareness) candidates and a skip-reason tally for one case."""
    found: list[tuple[int, datetime]] = []
    skipped: Counter[str] = Counter()
    for index, hazard in enumerate(case.get("hazards") or []):
        if not isinstance(hazard, dict) or hazard.get("released"):
            skipped["released_or_invalid"] += 1
        elif "safeguard" in str(hazard.get("category") or "").lower():
            skipped["safeguarding"] += 1
        elif hazard.get("aware_at"):
            skipped["already_has_aware_at"] += 1
        else:
            moment = anchor(hazard)
            if moment is None or moment > now:
                skipped["no_usable_anchor"] += 1
            else:
                found.append((index, moment))
    return found, skipped


def run(
    store: Any, *, apply: bool, running: int = 0, now: datetime | None = None
) -> dict[str, Any]:
    now = now or _instant(getattr(store, "as_of", None)) or datetime.now(UTC)
    skipped: Counter[str] = Counter()
    todo: list[tuple[str, int, datetime]] = []
    with store.lock:
        for case_id in sorted(store.cases):
            found, case_skips = plan(store.cases[case_id], now)
            skipped.update(case_skips)
            todo += [(case_id, index, moment) for index, moment in found]
        redate = set(range(0, len(todo), max(1, len(todo) // running))) if running else set()
        redate = set(sorted(redate)[:running])
        outcome: Counter[str] = Counter()
        cases_changed = {case_id for case_id, _, _ in todo}
        for position, (case_id, index, moment) in enumerate(todo):
            case = store._case(case_id) if apply else store.cases[case_id]
            hazard = case["hazards"][index]
            basis = "recorded_at_or_noticed"
            if position in redate:
                moment = (now - timedelta(hours=window_hours(hazard) * RUNNING_SHARE)).replace(
                    minute=0, second=0, microsecond=0
                )
                basis = "demo_running_share"
            hours = int((now - moment).total_seconds() // 3600)
            outcome["running" if hours < window_hours(hazard) else "overdue"] += 1
            if apply:
                if basis == "demo_running_share":
                    hazard[MARK] = {
                        "synthetic": True,
                        "basis": basis,
                        "noticed_was": hazard.get("noticed"),
                    }
                    hazard["noticed"] = _stamp(moment)[:10]
                else:
                    hazard[MARK] = {"synthetic": True, "basis": basis}
                hazard["aware_at"] = _stamp(moment)
                if not hazard.get("response_due_at"):
                    due = moment + timedelta(hours=window_hours(hazard))
                    hazard["response_due_at"] = _stamp(due)
                    hazard[MARK]["response_due_seeded"] = True
        report: dict[str, Any] = {
            "cases": len(store.cases),
            "cases_with_writes": len(cases_changed),
            "hazards_to_write": len(todo),
            "projected": dict(outcome),
            "skipped": dict(skipped),
            "applied": False,
        }
        if apply and todo:
            store.audit(
                "demo-hazard-clock-seed",
                ACTION,
                "-",
                f"hazards_changed={len(todo)}; cases_changed={len(cases_changed)}; "
                f"running_redated={len(redate)}; synthetic demo data only",
            )
            store.save()
            report["applied"] = True
    return report


def revert(store: Any) -> dict[str, Any]:
    """Undo this tool's writes: drop `aware_at` and the marker, restore a re-dated `noticed`."""
    changed: list[tuple[str, int]] = []
    with store.lock:
        for case_id in sorted(store.cases):
            for index, hazard in enumerate(store.cases[case_id].get("hazards") or []):
                if isinstance(hazard, dict) and isinstance(hazard.get(MARK), dict):
                    changed.append((case_id, index))
        for case_id, index in changed:
            hazard = store._case(case_id)["hazards"][index]
            mark = hazard.pop(MARK)
            hazard.pop("aware_at", None)
            if mark.get("response_due_seeded"):
                hazard.pop("response_due_at", None)
            if mark.get("noticed_was") is not None:
                hazard["noticed"] = mark["noticed_was"]
        if changed:
            store.audit(
                "demo-hazard-clock-seed",
                ACTION + "_reverted",
                "-",
                f"hazards_reverted={len(changed)}; synthetic demo data only",
            )
            store.save()
    return {"hazards_reverted": len(changed), "applied": bool(changed)}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if (
        not 1 <= len(args) <= 2
        or args[0] not in ("inspect", "apply", "revert")
        or (len(args) == 2 and not args[1].isdigit())
    ):
        print("usage: seed_demo_hazard_clock.py inspect|apply [N]|revert", file=sys.stderr)
        return 2
    if (os.environ.get("ZF_STORE") or "").lower() not in ("sqlite", "mssql"):
        print("ZF_STORE must be sqlite or mssql.", file=sys.stderr)
        return 2
    from zava_forward.core.factory import open_store

    store = open_store()
    if args[0] == "revert":
        result = revert(store)
    else:
        result = run(store, apply=args[0] == "apply", running=int(args[1]) if len(args) > 1 else 0)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
