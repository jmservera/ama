"""Local loopback app exercise; synthetic source/home/owner data, zero provider calls."""

from __future__ import annotations

import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch

from regulatory_fixture import ENV, NOW, PID, QUOTE, Fixture
from zava_forward.core import rule_engine, rulecards
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.regulatory_chat import RegulatoryChat
from zava_forward.core.source_monitor import SourceMonitor

from zava_forward.api.server import App, make_handler


class RegulatoryApi(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.f = Fixture(temp.name, sql=True)
        self.addCleanup(self.f.close)
        self.app: Any = App(self.f.store, "synthetic-local", law=self.f.law)
        self.app.chat = ChatIsolation(self.f.store, env=ENV)
        self.app.regulatory = RegulatoryChat(
            self.app.chat,
            self.f.law,
            self.app.regulatory.render,
            self.app.regulatory.classify,
            self.app.regulatory.refuse,
            env=ENV,
            clock=lambda: NOW,
        )
        self.outbound = patch.object(
            self.f.store.ai, "evidence", side_effect=AssertionError("No offline provider calls")
        )
        self.outbound.start()
        self.addCleanup(self.outbound.stop)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.worker = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.worker.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}
        for email in ("sam@example.test", "exercise-owner@example.test", "pam@example.test"):
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(dict(email=email, password="synthetic-local")).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[email] = response.headers["Set-Cookie"].split(";")[0]

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.worker.join(timeout=5)

    def call(self, path: str, body: Any = None, email: str = "sam@example.test") -> tuple[int, Any]:
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies[email]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                text = response.read().decode()
                return response.status, json.loads(text) if text.startswith(("{", "[")) else text
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def start(self) -> str:
        code, data = self.call("/api/chat/regulatory/threads", dict(case_id="ZF-1"))
        self.assertEqual(code, 200, data)
        return str(data["id"])

    def test_local_app_full_turn_resume_doubt_and_owner_inbox(self) -> None:
        self.assertTrue(self.worker.is_alive())
        self.assertEqual(self.call("/healthz")[0], 200)
        self.assertEqual(self.call("/api/cases/ZF-1")[0], 200)
        tid = self.start()
        route = f"/api/chat/regulatory/threads/{tid}"
        code, reply = self.call(route + "/ask", dict(content="What are the hazard sources?"))
        self.assertEqual((code, reply["kind"]), (200, "answer"), reply)
        self.assertEqual(reply["citations"][0]["id"], PID)
        history = self.call(route)[1]
        self.assertEqual(
            json.loads(history["messages"][1]["content"])["citations"], reply["citations"]
        )
        code, receipt = self.call(route + "/doubt", dict(turn=reply["turn"]))
        self.assertEqual((code, receipt["status"]), (200, "sent-to-exercise-inbox"))
        self.assertEqual(self.call(route + "/doubt", dict(turn=reply["turn"]))[1], receipt)
        code, inbox = self.call("/api/chat/regulatory/inbox", email="exercise-owner@example.test")
        self.assertEqual(code, 200, inbox)
        self.assertEqual(len(inbox["threads"]), 1)
        self.assertEqual(len(inbox["threads"][0]["messages"]), 2)
        self.assertEqual(self.call("/api/chat/regulatory/inbox")[0], 403)
        self.assertEqual(self.call(route, email="exercise-owner@example.test")[0], 404)
        self.assertEqual(self.call("/api/chat/threads/" + receipt["inbox_thread"])[0], 404)
        # Source content is absent from audit metadata.
        self.assertNotIn("Synthetic hazard reports", json.dumps(self.f.store.data.get("audit", [])))

    def test_denied_disabled_missing_owner_forgery_and_generic_bypass(self) -> None:
        self.app.regulatory.env = {}
        self.assertEqual(self.call("/api/chat/regulatory/status")[0], 403)
        self.assertEqual(self.call("/api/chat/regulatory/threads", dict(case_id="ZF-1"))[0], 403)
        self.app.regulatory.env = ENV
        tid = self.start()
        route = f"/api/chat/regulatory/threads/{tid}"
        extras: tuple[dict[str, Any], ...] = (
            dict(owner="forged"),
            dict(facts={}),
            dict(model="live"),
        )
        for extra in extras:
            self.assertEqual(self.call(route + "/ask", dict(content="hazard") | extra)[0], 400)
        self.assertEqual(self.call(f"/api/chat/threads/{tid}/ask", dict(content="hazard"))[0], 400)
        reply = self.call(route + "/ask", dict(content="hazard sources"))[1]
        self.assertEqual(
            self.call(route + "/doubt", dict(turn=reply["turn"], owner="forged"))[0], 400
        )
        self.assertEqual(self.call(route, email="pam@example.test")[0], 404)
        # Persist the revocation; SqlStore re-reads the staff register.
        self.f.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?",
            (json.dumps(dict(self.f.owner, name="Not the exercise owner")), self.f.owner["email"]),
        )
        with self.f.store.lock:
            pass
        code, error = self.call(route + "/doubt", dict(turn=reply["turn"]))
        self.assertEqual(code, 400, error)
        self.assertIn("no turn was sent", error["error"])

    def test_role_change_blocks_direct_and_generic_history(self) -> None:
        tid = self.start()
        route = f"/api/chat/regulatory/threads/{tid}"
        self.assertEqual(self.call(route + "/ask", dict(content="hazard sources"))[0], 200)
        self.f.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?",
            (json.dumps(dict(self.f.user, role="Quality Inspector")), self.f.user["email"]),
        )
        with self.f.store.lock:
            pass
        self.assertEqual(self.call(route)[0], 403)
        self.assertEqual(self.call("/api/chat/threads/" + tid)[0], 403)

    def test_panel_wiring_uses_real_routes_and_safe_dom(self) -> None:
        web = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
        text = (web / "chat.js").read_text()
        for required in (
            "regulatoryChatPanel(id)",
            "/api/chat/regulatory/threads",
            "/doubt",
            "Juan Manuel Servera",
            'role: "log"',
            '"aria-live": "polite"',
            "synthetic-demo",
            'type: "submit"',
            'role: "status"',
        ):
            self.assertIn(required, text)
        self.assertNotIn("innerHTML", text)
        self.assertIn("chatCasePanel(id)", (web / "app.js").read_text())

    def test_stale_card_labels_agree_on_http_history_and_chat_without_suppression(self) -> None:
        monitor = SourceMonitor(self.f.law)
        monitor.configure(
            "synthetic",
            cadence_days=1,
            likelihood="High",
            rationale="Synthetic daily fixture",
            impact=dict(requirements=[], journeys=[], tests=[], communications=[]),
            actor="Juan Manuel Servera",
            role=rulecards.OWNER,
        )
        monitor.observe(
            "synthetic",
            today="2026-10-09",
            content=QUOTE.encode(),
            metadata={},
            provenance="Constructed unchanged fixture",
            method="local-fixture",
        )
        engine = rule_engine.RuleEngine(self.f.law)
        engine.run(self.f.store, "ZF-1", "schedule", now=NOW)
        before = self.f.law.sql.all("SELECT body FROM reg_alert ORDER BY id")
        self.assertTrue(before)
        code, collection = self.call("/api/law/cards")
        self.assertEqual(code, 200, collection)
        card = next(c for c in collection["cards"] if c["card_id"] == "synthetic-hazard")
        self.assertEqual(card["source_freshness"]["status"], "out_of_cadence")
        code, history = self.call("/api/law/cards/synthetic-hazard")
        self.assertEqual(code, 200, history)
        self.assertEqual(history["versions"][0]["source_freshness"], card["source_freshness"])
        tid = self.start()
        code, reply = self.call(
            f"/api/chat/regulatory/threads/{tid}/ask", dict(content="What are the hazard sources?")
        )
        self.assertEqual((code, reply["kind"]), (200, "answer"), reply)
        self.assertEqual(reply["cards"][0]["source_freshness"]["status"], "out_of_cadence")
        self.assertEqual(before, self.f.law.sql.all("SELECT body FROM reg_alert ORDER BY id"))
        self.assertEqual(self.f.law.rules.is_active("synthetic-hazard", "2026-10-16"), 1)


if __name__ == "__main__":
    unittest.main()
