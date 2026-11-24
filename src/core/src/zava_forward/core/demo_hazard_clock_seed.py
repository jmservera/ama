"""Demo seed tool: awareness time and response target for synthetic open hazards (Refs #2255).

    ZF_STORE=mssql ... python -m zava_forward.core.demo_hazard_clock_seed inspect
    ZF_STORE=mssql ... python -m zava_forward.core.demo_hazard_clock_seed apply
    ZF_STORE=mssql ... python -m zava_forward.core.demo_hazard_clock_seed revert

The generated demo seed recorded open hazards with no `aware_at` and no `response_due_at`. The
hazard service rightly shows those as unknown and never guesses, so the safety queue shows no
running clock. This tool fixes the data, not the service, which stays the timing authority. It
prints counts only.

Only an open hazard (not released, not responded) with neither field is touched. `aware_at` is
the run time minus a cycled demo offset, so some clocks run inside the target and some past it;
`response_due_at` is awareness plus the operational 7-day hazard investigation reference. Both are
synthetic-demo assumptions, not a recorded regulatory deadline. Each changed hazard carries
`demo_clock_seed` so `revert` removes exactly what was written.
"""

import json
import os
import sys
from collections import Counter
from datetime import UTC, datetime, timedelta
from typing import Any

MARK = "demo_clock_seed"
ACTION = "demo_hazard_clock_seeded"
OFFSET_HOURS = (6, 30, 80, 200)
WINDOW_HOURS = 168


def plan(hazard: Any) -> str:
    """Return "ok" when the hazard should be seeded, otherwise the skip reason."""
    if not isinstance(hazard, dict):
        return "not_a_hazard"
    if isinstance(hazard.get(MARK), dict):
        return "already_seeded"
    if hazard.get("released") is True or hazard.get("responded_at"):
        return "not_open"
    if hazard.get("aware_at") or hazard.get("response_due_at"):
        return "timing_already_recorded"
    return "ok"


def _targets(store: Any) -> list[tuple[str, int]]:
    found: list[tuple[str, int]] = []
    for case_id in sorted(store.cases):
        hazards = store.cases[case_id].get("hazards")
        if isinstance(hazards, list):
            found.extend((case_id, i) for i, h in enumerate(hazards) if plan(h) == "ok")
    return found


def run(store: Any, *, apply: bool, now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(UTC)
    skipped: Counter[str] = Counter()
    with store.lock:
        for case in store.cases.values():
            hazards = case.get("hazards")
            if isinstance(hazards, list):
                skipped.update(r for r in map(plan, hazards) if r != "ok")
        todo = _targets(store)
        if apply:
            for number, (case_id, index) in enumerate(todo):
                hazard = store._case(case_id)["hazards"][index]
                aware = now - timedelta(hours=OFFSET_HOURS[number % len(OFFSET_HOURS)])
                due = aware + timedelta(hours=WINDOW_HOURS)
                hazard["aware_at"] = aware.isoformat(timespec="minutes")
                hazard["response_due_at"] = due.isoformat(timespec="minutes")
                hazard[MARK] = {"synthetic": True, "window_hours": WINDOW_HOURS}
        report: dict[str, Any] = {
            "cases": len(store.cases),
            "hazards_to_write": len(todo),
            "skipped": dict(skipped),
            "applied": False,
        }
        if apply and todo:
            store.audit(
                "demo-hazard-clock-seed",
                ACTION,
                "-",
                f"hazards_changed={len(todo)}; synthetic demo data only",
            )
            store.save()
            report["applied"] = True
    return report


def revert(store: Any) -> dict[str, Any]:
    """Undo this tool's writes by the `demo_clock_seed` marker."""
    changed: list[tuple[str, int]] = []
    with store.lock:
        for case_id in sorted(store.cases):
            hazards = store.cases[case_id].get("hazards")
            if isinstance(hazards, list):
                changed.extend(
                    (case_id, i)
                    for i, h in enumerate(hazards)
                    if isinstance(h, dict) and isinstance(h.get(MARK), dict)
                )
        for case_id, index in changed:
            hazard = store._case(case_id)["hazards"][index]
            for key in (MARK, "aware_at", "response_due_at"):
                hazard.pop(key, None)
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
    if len(args) != 1 or args[0] not in ("inspect", "apply", "revert"):
        print("usage: demo_hazard_clock_seed inspect|apply|revert", file=sys.stderr)
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
