"""Local HTTP proof of scoped alerts, trusted owner actions and independent safety routes."""

from __future__ import annotations

import base64
import copy
import json
import threading
import unittest
import urllib.error
import urllib.request
import uuid
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

import test_rule_engine as engine_fixture
from dataset import DATA
from zava_forward.core import rule_engine
from zava_forward.core.lawstore import LawStore
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api import auth
from zava_forward.api.server import App, make_handler

TENANT = "11111111-2222-3333-4444-555555555555"


class RuleAlertApi(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = engine_fixture.EngineTests(methodName="runTest")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        data = copy.deepcopy(DATA)
        for email, code, role in (
            ("owner@example.test", "SYN-OWNER", "Building Safety Liaison"),
            ("other@example.test", "SYN-OTHER", "Building Safety Liaison"),
            ("quality@example.test", "SYN-QA", "Quality Inspector"),
            ("contractor@example.test", "SYN-CON", "Contractor"),
        ):
            data["staff"].append(
                dict(email=email, code=code, name=code, oid=code, role=role, contractor="Test Ltd")
            )
        self.path = Path(self.fixture.tmp.name) / "synthetic.json"
        self.path.write_text(json.dumps(data))
        self.store: Any = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.provider: Any = auth.TrustedProxyProvider(
            self.store, {"ZF_ENTRA_TENANT_ID": TENANT, "ZF_TRUSTED_PROXY": "1"}
        )
        self.app: Any = App(self.store, provider=self.provider, law=self.fixture.law)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(
        self, actor: str, path: str, body: object = None, *, owner_capability: bool = True
    ) -> tuple[int, Any]:
        person = self.store.staff[f"{actor}@example.test"]
        mapped = next(k for k, v in auth.DEFAULT_ROLE_MAP.items() if v == person["role"])
        claims = [
            dict(typ="tid", val=TENANT),
            dict(typ="oid", val=str(uuid.uuid5(uuid.NAMESPACE_DNS, person["code"]))),
            dict(typ="roles", val=mapped),
        ]
        if owner_capability:
            claims.append(dict(typ="roles", val="ZavaForward.RuleOwner"))
        principal = base64.b64encode(json.dumps(dict(auth_typ="aad", claims=claims)).encode())
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"X-MS-CLIENT-PRINCIPAL": principal.decode(), "X-ZF-CSRF": "1"},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def report(self, *, case_id: str = "ZF-1") -> tuple[int, Any]:
        return self.call(
            "owner",
            f"/api/cases/{case_id}/hazard-raise",
            dict(
                category="Damp and mould",
                priority="Emergency",
                source="SYN-REPORT",
                aware_at="2026-01-01T10:00:00Z",
            ),
        )

    def alert(self) -> dict[str, Any]:
        code, data = self.call("owner", "/api/law/alerts?case=ZF-1")
        self.assertEqual(code, 200, data)
        return dict(data["homes"][0]["alerts"][0])

    def test_post_change_scoped_reads_owner_ack_outcome_and_spoof_denial(self) -> None:
        code, detail = self.report()
        self.assertEqual((code, detail["rule_checks"]["status"]), (200, "evaluated"))
        self.assertEqual(detail["hazards"][0]["hold"]["status"], "Active")
        a = self.alert()
        self.assertEqual(a["result"], "breach risk")
        self.assertEqual(a["trigger"], "data_change")
        self.assertEqual(a["usage"]["model_calls"], 0)
        self.assertEqual(a["usage"]["outcome"], a["result"])
        self.assertEqual(a["usage"]["model_call_limit_per_role_period"], 0)
        for actor, expected in (
            ("owner", 200),
            ("other", 200),
            ("quality", 200),
            ("contractor", 401),
        ):
            code, data = self.call(actor, "/api/law/alerts?case=ZF-1")
            self.assertEqual(code, expected)
            if actor == "quality":
                self.assertEqual(data["homes"], [])
        route = f"/api/law/alerts/{a['id']}/"
        self.assertEqual(self.call("other", route + "acknowledge", {"note": "SYN"})[0], 403)
        self.assertEqual(
            self.call("owner", route + "acknowledge", {"note": "SYN"}, owner_capability=False)[0],
            403,
        )
        for forged in ({"actor": "owner"}, {"at": "2026-01-01"}, {"role": "rule_owner"}):
            self.assertEqual(
                self.call("owner", route + "acknowledge", {"note": "SYN"} | forged)[0], 400
            )
        # Named decision owners are roster emails; an Entra identity fails closed (documented
        # limit).
        self.assertEqual(self.call("owner", route + "outcome", {"note": "SYN"})[0], 403)
        self.assertEqual(self.call("owner", route + "acknowledge", {"note": "SYN"})[0], 403)
        self.assertEqual(
            self.call("owner", "/api/law/alerts/guessed/acknowledge", {"note": "SYN"})[0], 403
        )
        self.assertEqual(self.store.detail("ZF-1")["hazards"][0]["hold"]["status"], "Active")
        self.assertEqual(self.store.detail("ZF-1")["contacts"], [])

    def test_check_inputs_clock_and_actor_are_not_client_controlled(self) -> None:
        bodies: tuple[dict[str, object], ...] = (
            {"now": "2026-01-01"},
            {"aware_at": "forged"},
            {"suppress": True},
            {"trigger": "schedule"},
            {"facts": {}},
        )
        for body in bodies:
            self.assertEqual(self.call("owner", "/api/law/checks/ZF-1", body)[0], 400)
        self.assertEqual(self.call("contractor", "/api/law/checks/ZF-1", {})[0], 401)
        code, data = self.call("quality", "/api/law/checks/ZF-1", {})
        self.assertEqual((code, data["checks"]), (200, []))
        self.assertEqual(self.call("owner", "/api/law/checks/guessed", {})[0], 404)

    def test_engine_down_does_not_block_emergency_or_hazard_referral(self) -> None:
        with patch.object(self.app, "rule_engine", side_effect=RuntimeError("SYN outage")):
            with self.assertLogs("zava_forward.api.server", level="ERROR"):
                code, detail = self.report()
            self.assertEqual((code, detail["rule_checks"]["status"]), (200, "unknown"))
            self.assertIn("human emergency", detail["rule_checks"]["safe_route"])
            with self.assertLogs("zava_forward.api.server", level="ERROR"):
                code, _ = self.call(
                    "owner",
                    "/api/cases/ZF-1/hazard-refer",
                    dict(index=0, to="other@example.test", job="SYN-JOB", evidence="SYN-SENT"),
                )
            self.assertEqual(code, 200)
            with self.assertLogs("zava_forward.api.server", level="ERROR"):
                code, data = self.call("owner", "/api/law/alerts")
            self.assertEqual((code, data["status"]), (503, "unknown"))
        self.assertTrue(self.store.detail("ZF-1")["hazards"][0]["job"])
        self.app.law = None
        with self.assertLogs("zava_forward.api.server", level="ERROR"):
            code, detail = self.report(case_id="ZF-2")
        self.assertEqual((code, detail["rule_checks"]["status"]), (200, "unknown"))
        self.assertIn("human emergency", detail["rule_checks"]["safe_route"])
        for route, body in (
            ("/api/law/alerts", None),
            ("/api/law/checks/ZF-2", {}),
        ):
            code, data = self.call("owner", route, body)
            self.assertEqual((code, data["status"]), (503, "unknown"))
            self.assertIn("law store is not loaded", data["error"])
            self.assertIn("human emergency", data["safe_route"])
        self.assertTrue(self.store.detail("ZF-2")["hazards"])

    def test_empty_law_store_returns_unknown_checks_and_freshness_without_alerts(self) -> None:
        empty = LawStore(
            str(Path(self.fixture.tmp.name) / "empty-law.sqlite"),
            Path(self.fixture.tmp.name) / "empty-blobs",
        )
        self.addCleanup(empty.close)
        self.app.law = empty
        self.app.engine = None
        self.assertEqual(empty.sources(), {"sources": [], "gaps": []})
        code, cards = self.call("owner", "/api/law/cards")
        self.assertEqual(code, 200, cards)
        self.assertEqual(len(cards["cards"]), 2)
        for card in cards["cards"]:
            self.assertEqual(card["source_freshness"]["status"], "unknown")
            self.assertEqual(card["state"], "draft")
            self.assertIsNone(card["approved_by"])
            code, history = self.call("owner", "/api/law/cards/" + card["card_id"])
            self.assertEqual(code, 200, history)
            self.assertEqual(history["versions"], [card])
            self.assertIsNone(history["active_version"])
        code, checkpoint = self.call("owner", "/api/law/checks/ZF-1", {})
        self.assertEqual(code, 200, checkpoint)
        self.assertEqual(
            [check["card_id"] for check in checkpoint["checks"]], ["hazard-awareness-clock"]
        )
        self.assertTrue(all(check["result"] == "unknown" for check in checkpoint["checks"]))
        self.assertEqual(empty.sql.all("SELECT * FROM reg_alert"), [])
        code, alerts = self.call("owner", "/api/law/alerts")
        self.assertEqual((code, alerts["homes"]), (200, []))

    def test_checkpoint_failure_keeps_safety_saved_and_schedule_recovers(self) -> None:
        engine: Any = self.app.rule_engine()
        original = engine.sql.run

        def fail(sql: str, args: object = ()) -> None:
            if sql.startswith("INSERT INTO reg_checkpoint"):
                raise RuntimeError("SYN checkpoint outage")
            original(sql, args)

        with patch.object(engine.sql, "run", side_effect=fail):
            with self.assertLogs("zava_forward.api.server", level="ERROR"):
                code, detail = self.report()
        self.assertEqual((code, detail["rule_checks"]["status"]), (200, "unknown"))
        self.assertEqual(self.fixture.law.sql.all("SELECT COUNT(*) n FROM reg_check")[0]["n"], 0)
        result = engine.run(self.store, "ZF-1", "schedule")
        self.assertTrue(result["checks"])
        self.assertEqual(self.alert()["trigger"], "schedule")

    def test_workflow_transition_trigger_and_bounded_scheduled_entrypoint(self) -> None:
        code, detail = self.call(
            "owner",
            "/api/cases/ZF-2/return",
            dict(
                to_stage="Contacting resident",
                reason="Synthetic evidence return",
                source="SYN-REVIEW",
                next_action="Human evidence review",
            ),
        )
        self.assertEqual(code, 200, detail)
        self.assertEqual(detail["rule_checks"]["status"], "evaluated")
        bodies = self.fixture.law.sql.all("SELECT body FROM reg_checkpoint")
        self.assertTrue(
            any(json.loads(b["body"])["checks"][0]["trigger"] == "step_transition" for b in bodies)
        )
        with (
            patch("sys.argv", ["rule_engine", "--limit", "2"]),
            patch("zava_forward.core.factory.open_store", return_value=self.store),
            patch("zava_forward.core.lawstore.LawStore.from_env", return_value=self.fixture.law),
            patch("builtins.print") as output,
        ):
            rule_engine.main()
        page = json.loads(output.call_args.args[0])
        self.assertEqual((page["processed"], page["next_after"]), (2, "ZF-2"))


if __name__ == "__main__":
    unittest.main()
