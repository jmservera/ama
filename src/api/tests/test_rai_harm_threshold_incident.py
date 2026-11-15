"""Issue #146 RAI harm monitoring: breaches create an owned incident that suspends the task.

Seeded critical harm and approved threshold breaches reach the SQL-backed suspension through the
HTTP API. Constructed thresholds stay offline; live thresholds need a named human approver.
Every actor, event and threshold is constructed.
"""

import json
import threading
import unittest
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import ThreadingHTTPServer
from typing import Any

from zava_forward.core import monitoring_coverage as mc

from test_assistants import Base
from zava_forward.api.auth import PasswordProvider
from zava_forward.api.server import App, make_handler

CAP = "stock-prioritisation"
OTHER = "assessment-preparation"
OWNER = "Safety and Assurance appointee"
APPROVER = "Named Assurance Lead"
PASSWORD = "synthetic-only-password"
WINDOW = dict(window_start="2026-11-05T00:00:00Z", window_end="2026-11-06T00:00:00Z")


def constructed_threshold(limit: float = 0.0, min_sample: int = 1) -> dict[str, Any]:
    return dict(limit=limit, min_sample=min_sample, constructed=True)


def live_threshold(approved_by: Any, limit: float = 0.1, min_sample: int = 20) -> dict[str, Any]:
    return dict(limit=limit, min_sample=min_sample, approved_by=approved_by)


def seeded_events(count: int) -> int:
    events = [dict(event_id=f"harm-{n}", observed_at="2026-11-05T10:00:00Z") for n in range(count)]
    counted: dict[str, Any] = mc.reconcile_events(events, **WINDOW)
    return int(counted["count"])


def verdict(events: int, denominator: int, threshold: dict[str, Any] | None) -> dict[str, Any]:
    result: dict[str, Any] = mc.evaluate_indicator(
        events=events,
        denominator=denominator,
        window_complete=True,
        threshold=threshold,
        incident_owner=OWNER,
    )
    return result


def incident_body(result: dict[str, Any], scope: str = CAP) -> dict[str, Any]:
    """Map a live breach verdict to the suspension request; offline verdicts never qualify."""
    if result["status"] != mc.BREACH or result["offline_only"]:
        raise AssertionError("only a live, approved breach may open an incident")
    return dict(
        scope=scope,
        reason="Approved harm threshold breached",
        incident_owner=result["incident_owner"],
        containment="Stop affected proposals",
        comms_owner=result["incident_owner"],
        comms_audience="Synthetic staff",
        evidence="synthetic:harm-threshold-146",
        resident_impact="Constructed resident could receive an unsupported claim",
        remediation="Correct prompt and rerun negative controls",
        synthetic=True,
        trigger="guardrail breach",
    )


class HarmThresholdIncident(Base):
    @contextmanager
    def api(self) -> Iterator[tuple[str, dict[str, str]]]:
        inspector = self.people["Quality Inspector"]
        password_provider: Any = PasswordProvider
        app_factory: Any = App
        provider = password_provider(self.store, PASSWORD)
        cookie = provider.login(inspector["email"], PASSWORD)
        app = app_factory(self.store, provider=provider)
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            yield (
                f"http://127.0.0.1:{server.server_port}",
                {
                    "Content-Type": "application/json",
                    "X-ZF-CSRF": "1",
                    "Cookie": f"zf_session={cookie}",
                },
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(10)
            app.assistants.stop()

    def post(
        self, base: str, headers: dict[str, str], path: str, body: dict[str, Any]
    ) -> tuple[int, Any]:
        request = urllib.request.Request(
            base + path, data=json.dumps(body).encode(), headers=headers
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            payload = json.load(error)
            error.close()
            return error.code, payload

    def held(self, scope: str) -> Any:
        with self.service.transaction() as db:
            return self.service.suspended(db, scope)

    def assert_no_incident(self) -> None:
        self.assertEqual(self.store.continuity_view(self.pm)["suspensions"], [])
        self.assertFalse(self.held(CAP))

    def test_seeded_critical_harm_creates_owned_incident_and_blocks_dispatch(self) -> None:
        count = seeded_events(1)
        result = verdict(count, count, live_threshold(APPROVER, limit=0.0, min_sample=1))
        self.assertEqual(result["status"], mc.BREACH)
        self.assertFalse(result["offline_only"])
        self.assertEqual(result["incident_owner"], OWNER)
        ready: Any = self.run_ready
        verify: Any = self.verify
        ready(CAP)
        pending = self.service.invoke(self.pm, CAP, "ZF-2")
        independent = verify(ready(OTHER))
        with self.api() as (base, headers):
            status, created = self.post(
                base, headers, "/api/continuity/suspend", incident_body(result)
            )
            self.assertEqual(status, 200)
            self.assertRegex(created["id"], r"SUS-[0-9]+")
            calls = self.provider.calls
        queued = self.service.invoke(self.pm, CAP, "ZF-1")
        self.assertFalse(self.service.execute(queued["id"]))
        self.assertFalse(self.service.execute(pending["id"]))
        self.assertEqual(self.provider.calls, calls)
        record = self.store.continuity_view(self.pm)["suspensions"][0]
        self.assertEqual(
            (record["status"], record["scope"], record["scope_kind"], record["trigger"]),
            ("Suspended", CAP, "task", "guardrail breach"),
        )
        self.assertEqual(record["incident_owner"], OWNER)
        self.assertEqual(record["communication"]["owner"], OWNER)
        self.assertTrue(record["actual_hold"])
        self.assertIn(pending["id"], {row["id"] for row in record["affected_assistant_tasks"]})
        self.assertIn("use the manual route", str(self.held(CAP)))
        self.assertIn("use the manual route", str(self.store.continuity_block(CAP)))
        self.assertFalse(self.held(OTHER))
        self.assertTrue(self.service.detail(self.pm, independent["id"])["actionable"])
        self.store.log_call(self.pm, "ZF-1", "Spoke", "Synthetic manual route")
        self.assertIn("Synthetic manual route", json.dumps(self.store.cases["ZF-1"]))
        reopened = self.other()
        with reopened.transaction() as db:
            self.assertTrue(reopened.suspended(db, CAP))
        self.assertEqual(
            reopened.store.continuity_view(self.pm)["suspensions"][0]["id"], record["id"]
        )

    def test_approved_threshold_breach_needs_a_named_incident_owner(self) -> None:
        events, denominator = seeded_events(10), 50
        threshold = live_threshold(APPROVER)
        ownerless = mc.evaluate_indicator(
            events=events,
            denominator=denominator,
            window_complete=True,
            threshold=threshold,
            incident_owner="",
        )
        self.assertEqual(ownerless["status"], mc.BREACH)
        self.assertIsNone(ownerless["incident_owner"])
        with self.api() as (base, headers):
            body = dict(incident_body(verdict(events, denominator, threshold)), incident_owner="")
            status, refused = self.post(base, headers, "/api/continuity/suspend", body)
            self.assertEqual(status, 400)
            self.assertIn("incident owner", refused["error"])
            self.assert_no_incident()
            within = verdict(2, denominator, threshold)
            self.assertEqual(within["status"], mc.WITHIN)
            self.assertNotIn("incident_required", within)
            status, created = self.post(
                base,
                headers,
                "/api/continuity/suspend",
                incident_body(verdict(events, denominator, threshold)),
            )
        self.assertEqual(status, 200)
        self.assertRegex(created["id"], r"SUS-[0-9]+")
        self.assertTrue(self.held(CAP))
        self.assertFalse(self.held(OTHER))

    def test_constructed_thresholds_are_offline_only_and_open_no_live_incident(self) -> None:
        count = seeded_events(1)
        offline = verdict(count, count, constructed_threshold())
        self.assertEqual(offline["status"], mc.BREACH)
        self.assertTrue(offline["offline_only"])
        self.assertTrue(offline["incident_required"])
        with self.assertRaises(AssertionError):
            incident_body(offline)
        self.assert_no_incident()
        ratified = verdict(count, count, dict(constructed_threshold(), approved_by=APPROVER))
        self.assertTrue(ratified["offline_only"])
        self.assertFalse(verdict(count, count, live_threshold(APPROVER, 0.0, 1))["offline_only"])

    def test_live_threshold_without_named_human_approval_is_blocked(self) -> None:
        count = seeded_events(10)
        for approver in (None, "", "   ", "Unavailable"):
            with self.subTest(approver=approver):
                result = verdict(count, 50, live_threshold(approver))
                self.assertEqual(result["status"], mc.BLOCKED)
                self.assertEqual(result["reason"], "live threshold needs named human approval")
                self.assertFalse(result.get("incident_required"))
                with self.assertRaises(AssertionError):
                    incident_body(result)
        invalid = verdict(count, 50, dict(constructed=False, limit=2, min_sample=1))
        self.assertEqual(invalid["status"], mc.BLOCKED)
        self.assertEqual(verdict(count, 50, None)["status"], mc.BLOCKED)
        self.assert_no_incident()

    def test_suspension_requires_an_authorised_role_and_is_not_repeated(self) -> None:
        result = verdict(1, 1, live_threshold(APPROVER, 0.0, 1))
        body = incident_body(result)
        with self.assertRaises(PermissionError):
            self.store.suspend(
                dict(email="resident@example.test", role="Resident"),
                body,
            )
        self.assert_no_incident()
        with self.api() as (base, headers):
            self.assertEqual(self.post(base, headers, "/api/continuity/suspend", body)[0], 200)
            status, repeat = self.post(base, headers, "/api/continuity/suspend", body)
        self.assertEqual(status, 400)
        self.assertIn("already suspended", repeat["error"])
        self.assertEqual(len(self.store.continuity_view(self.pm)["suspensions"]), 1)


if __name__ == "__main__":
    unittest.main()
