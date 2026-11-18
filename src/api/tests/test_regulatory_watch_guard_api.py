"""HTTP integration proofs for Issue #208 regulatory output guard and watch API."""

from __future__ import annotations

import csv
import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from typing import Any
from unittest.mock import patch

from regulatory_fixture import ENV, NOW, PID, QUOTE, Fixture
from zava_forward.core import assistants, lawstore
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.regulatory_chat import RegulatoryChat

from zava_forward.api.server import App, make_handler


class RegulatoryWatchGuardApiTest(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.f = Fixture(temp.name, sql=True)
        self.addCleanup(self.f.close)
        self.f.store.staff["kim@example.test"] = dict(
            code="CON-01",
            name="Kim Builder",
            email="kim@example.test",
            role="Contractor",
            firm="Test Ltd",
        )
        app_cls: Any = App
        handler_factory: Any = make_handler
        self.app: Any = app_cls(self.f.store, "synthetic-local", law=self.f.law)
        self.app.chat = ChatIsolation(self.f.store, env=ENV)
        self.app.regulatory = RegulatoryChat(
            self.app.chat,
            self.f.law,
            self.app.regulatory.render,
            self.app.regulatory.classify,
            self.app.regulatory.refuse,
            env=ENV,
            clock=lambda: NOW,
            guard_telemetry=self.app.guard_telemetry,
        )
        self.outbound = patch.object(
            self.f.store.ai, "evidence", side_effect=AssertionError("No offline provider calls")
        )
        self.outbound.start()
        self.addCleanup(self.outbound.stop)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler_factory(self.app))
        self.worker = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.worker.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.cookies: dict[str, str] = {}
        for email in (
            "sam@example.test",
            "exercise-owner@example.test",
            "pam@example.test",
            "kim@example.test",
        ):
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

    def call(
        self, path: str, body: Any = None, *, email: str = "sam@example.test"
    ) -> tuple[int, Any]:
        request = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies[email], "X-ZF-CSRF": "1"},
        )
        try:
            with urllib.request.urlopen(request) as response:
                text = response.read().decode()
                return response.status, json.loads(text) if text.startswith(("{", "[")) else text
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def start_reg_thread(self) -> str:
        code, data = self.call("/api/chat/regulatory/threads", dict(case_id="ZF-1"))
        self.assertEqual(code, 200, data)
        return str(data["id"])

    def test_watch_role_gate_bad_date_unloaded_503_and_legitimate_cited_pass(self) -> None:
        # Contractor gets 403 on /api/law/watch and does not receive guard telemetry on /api/me.
        self.assertEqual(self.call("/api/law/watch", email="kim@example.test")[0], 403)
        _, contractor_me = self.call("/api/me", email="kim@example.test")
        self.assertNotIn("regulatory_output_guard", contractor_me)

        # Malformed as_of query returns 400.
        self.assertEqual(self.call("/api/law/watch?as_of=not-a-date")[0], 400)

        # Legitimate cited source with source date, retrieval date, provision, and active human
        # rule activation passes cleanly with zero model calls.
        code, watch = self.call("/api/law/watch?as_of=2026-10-16")
        self.assertEqual(code, 200, watch)
        self.assertIs(watch["output_guard"]["checked"], True)
        self.assertIs(watch["output_guard"]["passed"], True)
        self.assertEqual(watch["output_guard"]["action"], "passed")
        self.assertEqual(watch["output_guard"]["telemetry"]["model_calls"], 0)
        self.assertIs(watch["output_guard"]["telemetry"]["deterministic"], True)
        self.assertEqual(len(watch["sources"]), 1)
        src_entry = watch["sources"][0]
        self.assertEqual(src_entry["source_id"], "synthetic")
        self.assertEqual(src_entry["effective"], "2026-01-01")
        self.assertEqual(src_entry["retrieved"], "2026-10-16")
        self.assertIs(src_entry["human_rule_activated"], True)
        self.assertIs(src_entry["output_guard"]["passed"], True)

        # Unloaded law store still denies contractor with 403 first and gives 503 to staff.
        self.app.law = None
        self.assertEqual(self.call("/api/law/watch", email="kim@example.test")[0], 403)
        self.assertEqual(self.call("/api/law/watch")[0], 503)

    def test_watch_blocks_and_rewrites_duty_satisfied_legal_advice_and_future_law(self) -> None:
        # Insert an append-only consultation source and review item carrying all three prohibited
        # claim classes so /api/law/watch deterministically flags and rewrites each one.
        with self.f.law.transaction():
            self.f.law.sql.run(
                "INSERT INTO reg_source VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    "synthetic-consult",
                    "Synthetic Consultation: statutory duty is satisfied for all homes.",
                    "https://example.test/consult",
                    "consultation",
                    "England",
                    "Juan Manuel Servera",
                    "High",
                    "daily",
                    "none",
                ),
            )
            self.f.law.sql.run(
                "INSERT INTO reg_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "synthetic-consult",
                    1,
                    "consultation",
                    "2027-04-01",
                    "2026-10-16",
                    "2026-10-16",
                    "reviewed",
                    lawstore.sha256(b"Draft consultation provision."),
                    "none",
                    "ok",
                    "full",
                    None,
                ),
            )
            self.f.law.sql.run(
                "INSERT INTO reg_provision VALUES (?,?,?,?,?,?,?)",
                (
                    "synthetic-consult@v1#0001",
                    "synthetic-consult",
                    1,
                    1,
                    "Phase 2 consultation",
                    "Draft consultation provision.",
                    lawstore.sha256(b"Draft consultation provision."),
                ),
            )
            self.f.law.sql.run(
                "INSERT INTO rule_card_review "
                "(id, card_id, source_id, source_version, detected, status, note, affected, "
                "prior_version, source_effective) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    1,
                    "synthetic-hazard",
                    "synthetic-consult",
                    1,
                    "2026-10-16",
                    "open",
                    "Legal advice: you are legally exempt from inspection, and consultation "
                    "phase 2 applies now as an active operational rule.",
                    json.dumps({"rules": ["synthetic-hazard"]}),
                    1,
                    "2027-04-01",
                ),
            )

        code, watch = self.call("/api/law/watch?as_of=2026-10-16")
        self.assertEqual(code, 200, watch)
        guard = watch["output_guard"]
        self.assertIs(guard["passed"], False)
        self.assertEqual(guard["action"], "rewritten")
        for expected_cat in ("duty_satisfied", "legal_advice", "future_law_applied_as_active"):
            self.assertIn(expected_cat, guard["violations"])
            self.assertGreaterEqual(guard["telemetry"]["by_category"][expected_cat], 1)

        serialized = json.dumps(watch)
        self.assertNotIn("statutory duty is satisfied", serialized.lower())
        self.assertNotIn("you are legally exempt", serialized.lower())
        self.assertNotIn("applies now as an active operational rule", serialized.lower())
        self.assertIn("Advisory review item only", serialized)

    def test_sources_json_and_csv_share_guard_and_rulecards_distinguish_draft_vs_active(
        self,
    ) -> None:
        # Insert a future_phase source whose title embeds an unsafe duty-satisfaction claim.
        with self.f.law.transaction():
            self.f.law.sql.run(
                "INSERT INTO reg_source VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    "future-regs",
                    "Future Phase Regs — complies with the Act and duty is satisfied.",
                    "https://example.test/future",
                    "legislation",
                    "England",
                    "Juan Manuel Servera",
                    "High",
                    "weekly",
                    "none",
                ),
            )
            self.f.law.sql.run(
                "INSERT INTO reg_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "future-regs",
                    1,
                    "future_phase",
                    "2028-01-01",
                    "2026-10-16",
                    "2026-10-16",
                    "reviewed",
                    lawstore.sha256(b"Future phase text."),
                    "none",
                    "ok",
                    "full",
                    None,
                ),
            )
            self.f.law.sql.run(
                "INSERT INTO reg_provision VALUES (?,?,?,?,?,?,?)",
                (
                    "future-regs@v1#0001",
                    "future-regs",
                    1,
                    1,
                    "Future phase duty",
                    "Future phase text.",
                    lawstore.sha256(b"Future phase text."),
                ),
            )

        code, listing = self.call("/api/law/sources")
        self.assertEqual(code, 200, listing)
        self.assertIs(listing["output_guard"]["passed"], False)
        self.assertNotIn("duty is satisfied", json.dumps(listing).lower())

        csv_code, csv_text = self.call("/api/law/sources.csv")
        self.assertEqual(csv_code, 200)
        rows = list(csv.DictReader(io.StringIO(csv_text)))
        self.assertTrue(any("Advisory review item only" in r["title"] for r in rows))
        self.assertNotIn("duty is satisfied", csv_text.lower())

        # Draft card citing future-regs@v1#0001 with neutral prose passes cleanly (PC-003).
        self.f.card(
            "draft-future-card",
            approve=False,
            safe="Escalate to Compliance review before any operational change.",
            pid="future-regs@v1#0001",
        )
        code, draft_hist = self.call("/api/law/cards/draft-future-card")
        self.assertEqual(code, 200, draft_hist)
        self.assertIsNone(draft_hist["active_version"])
        self.assertIs(draft_hist["output_guard"]["passed"], True)

        # Activated card on future_phase source is flagged as future_law_applied_as_active.
        self.f.card(
            "misactivated-future-card",
            approve=True,
            safe="Apply future threshold immediately to active cases.",
            pid="future-regs@v1#0001",
        )
        code, active_cards = self.call("/api/law/cards")
        self.assertEqual(code, 200, active_cards)
        mis_card = next(
            c for c in active_cards["cards"] if c["card_id"] == "misactivated-future-card"
        )
        self.assertIs(active_cards["output_guard"]["passed"], False)
        self.assertIn("future_law_applied_as_active", active_cards["output_guard"]["violations"])
        self.assertIn("Advisory review item only", mis_card["safe_default"])

    def test_rule_checks_and_alerts_guard_unsafe_prose(self) -> None:
        # Clean check & alert pass first.
        code, clean_cp = self.call("/api/law/checks/ZF-1", {}, email="exercise-owner@example.test")
        self.assertEqual(code, 200, clean_cp)
        self.assertIs(clean_cp["output_guard"]["passed"], True)

        # Create an active card on in_force source whose safe_default gives legal advice.
        self.f.card(
            "unsafe-advice-card",
            approve=True,
            safe="Legal advice: you are legally required to close the case and duty is satisfied.",
            pid=PID,
        )
        code, cp = self.call("/api/law/checks/ZF-1", {}, email="exercise-owner@example.test")
        self.assertEqual(code, 200, cp)
        self.assertIs(cp["output_guard"]["passed"], False)
        self.assertIn("legal_advice", cp["output_guard"]["violations"])
        self.assertIn("duty_satisfied", cp["output_guard"]["violations"])
        self.assertNotIn("you are legally required", json.dumps(cp).lower())

        code, alerts = self.call("/api/law/alerts?case=ZF-1", email="exercise-owner@example.test")
        self.assertEqual(code, 200, alerts)
        self.assertIs(alerts["output_guard"]["passed"], False)
        self.assertNotIn("duty is satisfied", json.dumps(alerts).lower())

    def test_chat_plain_language_preserves_violation_flag_and_demotes_future_law(self) -> None:
        tid = self.start_reg_thread()
        ask_route = f"/api/chat/regulatory/threads/{tid}/ask"

        # 1. Legitimate active cited answer passes cleanly.
        code, ok_reply = self.call(
            ask_route, dict(content="What are the hazard sources?", plain_language=True)
        )
        self.assertEqual((code, ok_reply["kind"]), (200, "answer"))
        self.assertIs(ok_reply["output_guard"]["passed"], True)

        # 2. Rogue renderer claiming duty satisfaction with plain_language=True keeps passed=False
        # (PC-001: plain_language.apply must not clobber upstream violation status).
        orig_render = self.app.regulatory.render

        def rogue_render(bundle: dict[str, Any]) -> dict[str, Any]:
            base = dict(orig_render(bundle))
            base["reply"] = f'"{QUOTE}" Therefore the statutory duty is satisfied.'
            base["output_guard"] = {
                "checked": True,
                "passed": False,
                "action": "rewritten",
                "violations": ["duty_satisfied"],
                "reasons": ["statutory_duty_is_satisfied"],
                "guard_version": "regulatory-non-advice-guard-v1",
            }
            return base

        self.app.regulatory.render = rogue_render
        try:
            before_checked = self.app.guard_telemetry.snapshot()["checked_total"]
            code, guarded_reply = self.call(
                ask_route, dict(content="What are the hazard sources?", plain_language=True)
            )
        finally:
            self.app.regulatory.render = orig_render

        self.assertEqual(code, 200, guarded_reply)
        self.assertIs(guarded_reply["plain_language"], True)
        self.assertIs(guarded_reply["output_guard"]["passed"], False)
        self.assertIn("duty_satisfied", guarded_reply["output_guard"]["violations"])
        self.assertNotIn("duty is satisfied", guarded_reply["reply"].lower())
        after_checked = self.app.guard_telemetry.snapshot()["checked_total"]
        # Single turn check + plain_summary check = 2 checks (no double-counting inside ask).
        self.assertEqual(after_checked - before_checked, 2)

        # 3a. Retiring the human-approved rule card causes bundle retrieval itself to refuse
        # cleanly rather than serving unactivated law.
        self.f.law.rules.retire("synthetic-hazard", 1, "exercise-owner@example.test", "rule_owner")
        code, unactivated_reply = self.call(
            ask_route, dict(content="What are the hazard sources?", plain_language=True)
        )
        self.assertEqual((code, unactivated_reply["kind"]), (200, "refused"))
        self.assertIs(unactivated_reply["output_guard"]["passed"], True)
        self.assertIs(unactivated_reply["requires_human"], True)

        # 3b. Even if a renderer attempts to return kind="answer" on an unactivated/future-phase
        # source bundle, _guard_turn_reply + plain_language.apply flags future_law_applied_as_active
        # and demotes the reply to refused.
        def unactivated_answer_render(bundle: dict[str, Any]) -> dict[str, Any]:
            return {
                "kind": "answer",
                "reply": f'[synthetic@v1#0001] "{QUOTE}"',
                "citations": ["synthetic@v1#0001"],
                "sections": {
                    "what_sources_say": [f'[synthetic@v1#0001] "{QUOTE}"'],
                    "recorded_home_facts": [],
                    "unknown_or_missing": [],
                },
                "requires_human": False,
                "as_of": bundle["as_of"],
            }

        orig_bundle = self.app.regulatory.bundle

        def future_bundle(user: dict[str, Any], cid: str, q: str) -> dict[str, Any]:
            snap = dict(orig_bundle(user, cid, q))
            snap["refusal"] = None
            snap["sources"] = [
                {
                    "id": "synthetic@v1#0001",
                    "text": QUOTE,
                    "status": "future_phase",
                    "version": 1,
                    "effective": "2027-06-01",
                    "retrieved": "2026-10-16",
                }
            ]
            snap["cards"] = []
            return snap

        with (
            patch.object(self.app.regulatory, "bundle", side_effect=future_bundle),
            patch.object(self.app.regulatory, "render", side_effect=unactivated_answer_render),
            patch.object(self.app.regulatory, "enforce_ship_gate", False),
        ):
            code, future_reply = self.call(
                ask_route, dict(content="What are the hazard sources?", plain_language=True)
            )

        self.assertEqual((code, future_reply["kind"]), (200, "refused"))
        self.assertIs(future_reply["output_guard"]["passed"], False)
        self.assertIn(
            "future_law_applied_as_active",
            future_reply["output_guard"]["violations"],
        )
        self.assertIs(future_reply["requires_human"], True)

    def test_workbench_status_surfaces_expose_shared_telemetry_including_rejections(self) -> None:
        # Trigger assistant rejection on unsafe legal-advice and duty-satisfied proposal output.
        with self.assertRaises(ValueError):
            assistants.validate_output(
                {
                    "summary": "This constitutes legal advice and confirms the duty is satisfied.",
                    "findings": [{"text": "Recorded EPC band is D.", "citations": ["case:ZF-1"]}],
                    "unknowns": [],
                },
                {"citations": {"case:ZF-1": "epc=D"}, "unknowns": []},
                4000,
                guard_telemetry=self.app.guard_telemetry,
            )

        _, reg_status = self.call("/api/chat/regulatory/status")
        _, chat_status = self.call("/api/chat/status")
        _, me_payload = self.call("/api/me")
        _, watch_payload = self.call("/api/law/watch")

        for surface_telemetry in (
            reg_status["output_guard"],
            chat_status["output_guard"],
            me_payload["regulatory_output_guard"],
            watch_payload["output_guard"]["telemetry"],
        ):
            self.assertEqual(surface_telemetry["guard_version"], "regulatory-non-advice-guard-v1")
            self.assertIs(surface_telemetry["deterministic"], True)
            self.assertEqual(surface_telemetry["model_calls"], 0)
            self.assertGreaterEqual(surface_telemetry["rejected_total"], 1)
            self.assertGreaterEqual(surface_telemetry["by_category"]["legal_advice"], 1)
            self.assertGreaterEqual(surface_telemetry["by_category"]["duty_satisfied"], 1)


if __name__ == "__main__":
    unittest.main()
