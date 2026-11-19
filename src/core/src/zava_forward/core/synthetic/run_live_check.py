"""Check a deployed IoT hub and its budgets against the simulator run-control contract (issue #189).

Input is JSON captured with `az iot hub show` and `az consumption budget list`; no Azure call is
made here. Recipient addresses are never echoed, only classified.
"""

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .run_governance import governed_text

UNREACHABLE_DOMAINS = frozenset(
    {
        "users.noreply.github.com",
        "noreply.github.com",
        "example.invalid",
        "example.com",
        "localhost",
    }
)


@dataclass(frozen=True)
class LiveCheck:
    name: str
    passed: bool
    detail: str


def _domain_class(address: object) -> str:
    if not isinstance(address, str) or "@" not in address:
        return "invalid"
    domain = address.rsplit("@", 1)[1].strip().lower()
    return "unreachable" if domain in UNREACHABLE_DOMAINS or not domain else "reachable"


def _threshold(notification: Mapping[str, Any]) -> float | None:
    try:
        return float(notification.get("threshold", ""))
    except (TypeError, ValueError):
        return None


def _enabled(notifications: object) -> dict[str, Mapping[str, Any]]:
    if not isinstance(notifications, Mapping):
        return {}
    return {
        str(key): value
        for key, value in notifications.items()
        if isinstance(value, Mapping)
        and value.get("enabled") is True
        and value.get("operator") == "GreaterThan"
        and _threshold(value) is not None
    }


def _scoped_to(hub: Mapping[str, Any], budget: Mapping[str, Any]) -> bool:
    flt = budget.get("filter")
    dims = flt.get("dimensions") if isinstance(flt, Mapping) else None
    hub_id = hub.get("id")
    if not isinstance(dims, Mapping) or not isinstance(hub_id, str) or not hub_id:
        return False
    values = dims.get("values")
    return (
        str(dims.get("name", "")).lower() == "resourceid"
        and str(dims.get("operator", "")).lower() == "in"
        and isinstance(values, list)
        and hub_id.lower() in {str(v).lower() for v in values}
    )


def _select_budget(
    hub: Mapping[str, Any], budgets: Sequence[Mapping[str, Any]]
) -> Mapping[str, Any] | None:
    """The budget scoped to the hub resource, else the one named `budget-<hub name>`."""
    for budget in budgets:
        if _scoped_to(hub, budget):
            return budget
    named = [b for b in budgets if b.get("name") == f"budget-{hub.get('name', '')}"]
    return named[0] if named else None


def verify_live_run_controls(
    hub: Mapping[str, Any],
    budgets: Sequence[Mapping[str, Any]],
    *,
    expected_sku: str | None = None,
    expected_capacity: int | None = None,
) -> tuple[LiveCheck, ...]:
    """Return one result per check; the budget is the hub-scoped one, else `budget-<hub name>`."""
    checks: list[LiveCheck] = []
    tags = hub.get("tags")
    owner = tags.get("owner") if isinstance(tags, Mapping) else None
    checks.append(
        LiveCheck(
            "owner_tag",
            governed_text(owner),
            "hub owner tag is a named owner" if governed_text(owner) else "hub owner tag missing",
        )
    )

    sku = hub.get("sku")
    sku_name = sku.get("name") if isinstance(sku, Mapping) else None
    capacity = sku.get("capacity") if isinstance(sku, Mapping) else None
    tier_ok = isinstance(sku_name, str) and isinstance(capacity, int) and capacity >= 1
    if tier_ok and expected_sku is not None:
        tier_ok = sku_name == expected_sku
    if tier_ok and expected_capacity is not None:
        tier_ok = capacity == expected_capacity
    checks.append(LiveCheck("hub_tier", tier_ok, f"sku {sku_name} capacity {capacity}"))

    budget = _select_budget(hub, budgets)
    try:
        amount = float(budget["amount"]) if budget is not None else 0.0
    except (KeyError, TypeError, ValueError):
        amount = 0.0
    cap_ok = budget is not None and budget.get("timeGrain") == "Monthly" and amount > 0
    checks.append(
        LiveCheck("budget_cap", cap_ok, f"monthly amount {amount}" if cap_ok else "no hub budget")
    )

    live = _enabled(budget.get("notifications")) if budget is not None else {}
    actual = [n for k, n in live.items() if "forecast" not in k.lower()]
    forecast = [n for k, n in live.items() if "forecast" in k.lower()]
    actual_t = min((_threshold(n) or 0.0 for n in actual), default=0.0)
    forecast_t = min((_threshold(n) or 0.0 for n in forecast), default=0.0)
    checks.append(
        LiveCheck(
            "alert_actual",
            0 < actual_t <= 100,
            f"enabled actual threshold {actual_t}" if actual else "no enabled actual alert",
        )
    )
    checks.append(
        LiveCheck(
            "alert_forecast",
            forecast_t >= actual_t > 0,
            f"enabled forecast threshold {forecast_t}" if forecast else "no enabled forecast alert",
        )
    )

    classes: list[str] = []
    for notification in live.values():
        contacts = list(notification.get("contactEmails") or [])
        reachable = bool(notification.get("contactGroups") or notification.get("contactRoles"))
        classes.extend(_domain_class(c) for c in contacts)
        if reachable:
            classes.append("reachable")
        if not contacts and not reachable:
            classes.append("none")
    recipient_ok = bool(classes) and all(c == "reachable" for c in classes)
    counts = {c: classes.count(c) for c in sorted(set(classes))}
    checks.append(LiveCheck("recipient_reachable", recipient_ok, f"recipient classes {counts}"))
    return tuple(checks)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify deployed run controls from az JSON")
    parser.add_argument("--hub", type=Path, required=True)
    parser.add_argument("--budgets", type=Path, required=True)
    parser.add_argument("--expected-sku")
    parser.add_argument("--expected-capacity", type=int)
    args = parser.parse_args(argv)
    try:
        hub = json.loads(args.hub.read_text(encoding="utf-8"))
        budgets = json.loads(args.budgets.read_text(encoding="utf-8"))
        if not isinstance(hub, dict) or not isinstance(budgets, list):
            raise TypeError("shape")
    except (OSError, ValueError, TypeError):
        print("refused: LIVE_INPUT_INVALID", file=sys.stderr)
        return 2
    checks = verify_live_run_controls(
        hub, budgets, expected_sku=args.expected_sku, expected_capacity=args.expected_capacity
    )
    print(
        json.dumps(
            {
                "ok": all(c.passed for c in checks),
                "checks": [
                    {"name": c.name, "passed": c.passed, "detail": c.detail} for c in checks
                ],
            },
            indent=2,
        )
    )
    return 0 if all(c.passed for c in checks) else 3


if __name__ == "__main__":
    sys.exit(main())
