"""Deployed run-control verifier tests (issue #189)."""

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any

from zava_forward.core.synthetic import run_live_check
from zava_forward.core.synthetic.run_live_check import verify_live_run_controls

HUB: dict[str, Any] = {
    "name": "iot-x",
    "sku": {"name": "B1", "capacity": 1},
    "tags": {"owner": "Juan Manuel Servera"},
}


def _budget(email: str = "ops@contoso.org") -> dict[str, Any]:
    note = {"enabled": True, "operator": "GreaterThan", "contactEmails": [email]}
    return {
        "name": "budget-iot-x",
        "amount": "25.0",
        "timeGrain": "Monthly",
        "notifications": {
            "actual80": {**note, "threshold": "80.0"},
            "forecast100": {**note, "threshold": "100.0"},
        },
    }


def _failed(hub: dict[str, Any], budgets: list[dict[str, Any]], **kw: Any) -> set[str]:
    return {c.name for c in verify_live_run_controls(hub, budgets, **kw) if not c.passed}


class LiveRunControlTests(unittest.TestCase):
    def test_all_pass(self) -> None:
        self.assertEqual(_failed(HUB, [_budget()], expected_sku="B1", expected_capacity=1), set())

    def test_budget_selected_by_hub_scope_not_name(self) -> None:
        hub = {
            **HUB,
            "id": "/subscriptions/s/resourceGroups/ama/providers/Microsoft.Devices/IotHubs/iot-x",
        }
        scoped = {**_budget(), "name": "other-name"}
        scoped["filter"] = {
            "dimensions": {"name": "ResourceId", "operator": "In", "values": [hub["id"].upper()]}
        }
        self.assertEqual(_failed(hub, [scoped]), set())
        elsewhere = {
            **scoped,
            "filter": {"dimensions": {"name": "ResourceId", "operator": "In", "values": ["/x"]}},
        }
        self.assertIn("budget_cap", _failed(hub, [elsewhere]))

    def test_noreply_and_invalid_recipients_fail_only_reachability(self) -> None:
        for email in ("1+u@users.noreply.github.com", "a@example.invalid", "nobody"):
            self.assertEqual(_failed(HUB, [_budget(email)]), {"recipient_reachable"})

    def test_contact_group_counts_as_reachable(self) -> None:
        b = _budget("a@example.invalid")
        for n in b["notifications"].values():
            n["contactEmails"] = []
            n["contactGroups"] = ["/subscriptions/s/ag"]
        self.assertEqual(_failed(HUB, [b]), set())

    def test_owner_tier_and_budget_failures(self) -> None:
        hub = copy.deepcopy(HUB)
        hub["tags"]["owner"] = "TBD"
        self.assertIn("owner_tag", _failed(hub, [_budget()]))
        self.assertIn("hub_tier", _failed(HUB, [_budget()], expected_sku="S1"))
        self.assertTrue({"budget_cap", "alert_actual", "alert_forecast"} <= _failed(HUB, []))

    def test_disabled_forecast_alert_fails(self) -> None:
        b = _budget()
        b["notifications"]["forecast100"]["enabled"] = False
        self.assertEqual(_failed(HUB, [b]), {"alert_forecast"})

    def test_cli_exit_codes_and_no_address_echo(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            hub, bud = Path(d) / "h.json", Path(d) / "b.json"
            hub.write_text(json.dumps(HUB))
            bud.write_text(json.dumps([_budget("1+u@users.noreply.github.com")]))
            out = io.StringIO()
            with redirect_stdout(out):
                code = run_live_check.main(["--hub", str(hub), "--budgets", str(bud)])
            self.assertEqual(code, 3)
            self.assertNotIn("noreply", out.getvalue())
            bud.write_text("{}")
            with redirect_stderr(io.StringIO()):
                self.assertEqual(run_live_check.main(["--hub", str(hub), "--budgets", str(bud)]), 2)


if __name__ == "__main__":
    unittest.main()
