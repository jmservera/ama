"""Exact #90 HTTP controls using only temporary fictional source bytes."""

import copy
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any

from building_fixture import fixture, hold
from dataset import (
    DATA,
    RESIDENT_BINDINGS,
    supplied_appointment_fixture,
    supplied_contract_fixture,
    supplied_resident_fixture,
)
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

from zava_forward.api import server


class ProcurementApiFixture(unittest.TestCase):
    sql = True

    def make_store(self, path: Path) -> Any:
        factory: Any = SqlStore if self.sql else Store
        return (
            factory(str(path), str(path.with_suffix(".sqlite"))) if self.sql else factory(str(path))
        )

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        for case in data["cases"]:
            supplied_resident_fixture(case)
        data["cases"][1]["contractor"]["name"] = "Other Ltd"
        data["staff"].extend(
            [
                dict(
                    code=code,
                    name=name,
                    email=email,
                    role="Contractor",
                    contractor=contractor,
                )
                for code, name, email, contractor in (
                    ("CON-1", "Kim Fiction", "kim@example.test", "Test Ltd"),
                    ("CON-2", "Kai Fiction", "kai@example.test", "Other Ltd"),
                )
            ]
        )
        data["staff"].append(
            dict(
                code="QI-02", name="Quil Other", email="quil@example.test", role="Quality Inspector"
            )
        )
        self.manager = data["staff"][1]
        self.path.write_text(json.dumps(data))
        self.store = self.make_store(self.path)
        if hasattr(self.store, "db"):
            self.addCleanup(self.store.db.close)
        self.pid = self.store.create_package(
            self.manager, "Synthetic package", "2026-01-01", "2099-12-31", "Loft", "SYN", "SYN-1"
        )
        self.details = supplied_contract_fixture(self.store, self.pid, self.manager)
        self.other_details = supplied_contract_fixture(
            self.store, self.pid, self.manager, "Other Ltd"
        )
        app_factory: Any = server.App
        handler_factory: Any = server.make_handler
        self.app = app_factory(self.store, "synthetic-password")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler_factory(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(self, path: str, body: object = None, actor: str = "pam") -> tuple[int, Any]:
        if actor not in self.cookies:
            request = urllib.request.Request(
                self.base + "/api/login",
                json.dumps(
                    dict(email=f"{actor}@example.test", password="synthetic-password")
                ).encode(),
            )
            with urllib.request.urlopen(request) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        request = urllib.request.Request(
            self.base + path,
            None if body is None else json.dumps(body).encode(),
            headers={"Cookie": self.cookies[actor]},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def capacity(self, contractor: str = "Test Ltd") -> dict[str, Any]:
        return dict(
            contractor=contractor,
            offered=9,
            committed=1,
            evidence="SYN accepted commitment",
            details=self.details if contractor == "Test Ltd" else self.other_details,
        )

    def issue(self, cid: str = "ZF-1") -> dict[str, Any]:
        return dict(package=self.pid, case_id=cid, resident_bindings=RESIDENT_BINDINGS)


class ProcurementApi(ProcurementApiFixture):
    def test_package_creation_requires_contract_version(self) -> None:
        body = dict(
            name="SYN new package",
            period_from="2026-01-01",
            period_to="2099-12-31",
            scope="Loft",
            contract_ref="SYN",
        )
        before = copy.deepcopy(self.store.data["procurement"])
        audit = list(self.store.audit_entries())
        for payload in (body, dict(body, contract_version=""), dict(body, contract_version=" \t ")):
            with self.subTest(payload=payload):
                code, result = self.call("/api/packages", payload)
                self.assertEqual(code, 400)
                self.assertIn("contract or call-off version", result["error"])
                self.assertEqual(self.store.data["procurement"], before)
                self.assertEqual(list(self.store.audit_entries()), audit)
        code, result = self.call("/api/packages", dict(body, contract_version=" SYN-1 "))
        self.assertEqual(code, 200)
        self.assertEqual(result["packages"][-1]["contract_version"], "SYN-1")

    def test_capacity_http_exact_threshold_and_source_inputs(self) -> None:
        path = f"/api/packages/{self.pid}/capacity"
        self.assertEqual(self.call(path, dict(self.capacity(), details=None))[0], 400)
        self.assertEqual(self.call(path, self.capacity())[0], 200)
        self.assertEqual(self.call("/api/workorders", self.issue())[0], 200)
        self.assertEqual(self.call("/api/workorders", self.issue("ZF-3"))[0], 400)
        self.assertEqual(
            self.call(
                "/api/workorders/WO-0001/appointment", dict(outcome="Booked", date="2100-01-01")
            )[0],
            400,
        )
        self.assertEqual(self.call("/api/cases/ZF-3/advance", {})[0], 400)

    def test_contractors_own_orders_only_and_all_writes_denied(self) -> None:
        path = f"/api/packages/{self.pid}/capacity"
        for contractor, cid in (("Test Ltd", "ZF-1"), ("Other Ltd", "ZF-2")):
            self.assertEqual(self.call(path, self.capacity(contractor))[0], 200)
            self.assertEqual(self.call("/api/workorders", self.issue(cid))[0], 200)
        for actor, own, foreign in (("kim", "ZF-1", "ZF-2"), ("kai", "ZF-2", "ZF-1")):
            code, rows = self.call("/api/workorders", actor=actor)
            self.assertEqual(code, 200)
            self.assertEqual([row["case_id"] for row in rows], [own])
            self.assertEqual(self.call(f"/api/workorders?case={foreign}", actor=actor), (200, []))
            self.assertEqual(self.call("/api/packages", actor=actor)[0], 403)
            for route, body in [
                ("/api/workorders", self.issue()),
                ("/api/packages", dict(name="SYN")),
                (path, self.capacity()),
                (f"/api/packages/{self.pid}/rescope", dict(scope="SYN", reason="SYN")),
            ] + [
                (f"/api/workorders/WO-0001/{action}", {})
                for action in ("reissue", "appointment", "complete", "correct", "withdraw")
            ]:
                self.assertEqual(self.call(route, body, actor)[0], 403, (actor, route))
            with self.assertRaises(PermissionError):
                self.store.list_packages(self.store.staff[f"{actor}@example.test"])

    def test_lifecycle_http_has_issuer_for_every_change(self) -> None:
        self.assertEqual(self.call(f"/api/packages/{self.pid}/capacity", self.capacity())[0], 200)
        self.assertEqual(self.call("/api/workorders", self.issue("ZF-3"))[0], 200)
        route = "/api/workorders/WO-0001/"
        for action, body in (
            ("appointment", dict(outcome="Booked", date="2099-01-01")),
            ("appointment", dict(outcome="No access")),
            ("appointment", dict(outcome="Booked", date="2099-01-02")),
            ("reissue", dict(scope="Loft", reason="SYN", resident_bindings=RESIDENT_BINDINGS)),
            ("complete", dict(note="SYN")),
            ("correct", dict(reason="SYN", resident_bindings=RESIDENT_BINDINGS)),
            ("withdraw", dict(reason="SYN")),
        ):
            if action == "appointment" and body["outcome"] == "Booked":
                supplied_appointment_fixture(self.store, self.manager, "WO-0001", body["date"])
            self.assertEqual(self.call(route + action, body)[0], 200, action)
        versions = self.call("/api/workorders")[1][0]["versions"]
        self.assertEqual([row["version"] for row in versions], list(range(1, 9)))
        self.assertTrue(all(row["issuer_email"] == self.manager["email"] for row in versions))
        self.assertEqual(versions[0]["appointments"], [])
        self.assertTrue(self.store.verify_audit())

    def test_appointment_controls_http_provenance_denials_and_committed_response(self) -> None:
        from unittest.mock import patch

        self.call(f"/api/packages/{self.pid}/capacity", self.capacity())
        self.call("/api/workorders", self.issue())
        route = "/api/workorders/WO-0001/appointment-control"
        code, result = self.call("/api/workorders")
        self.assertEqual(result[0]["appointment_control"]["status"], "Unknown")
        ref = supplied_appointment_fixture(self.store, self.manager, "WO-0001", confirmations=False)
        self.assertEqual(
            self.call(route, dict(action="confirm", event_ref="FORGED", status="Committed"))[0], 400
        )
        for actor in ("kim", "kai"):
            self.assertEqual(self.call(route, dict(action="confirm"), actor)[0], 403)
        for kind, person in (
            ("resident", "Pat Test"),
            ("staff", self.manager["name"]),
            ("capacity", "SYN supplier"),
        ):
            body = dict(
                action="confirm",
                event_ref="HTTP-" + kind,
                offer_id=ref,
                kind=kind,
                person=person,
                source="SYN recorded source",
                channel="Phone, manual",
            )
            if kind == "capacity":
                with patch.object(
                    self.store, "list_packages", side_effect=OSError("SYN projection")
                ):
                    code, result = self.call(route, body)
                self.assertEqual((code, result["outcome"]), (409, "committed"))
                # Retry reconciles the already consumed reference, not a new confirmation.
            code, result = self.call(route, body)
            self.assertEqual(code, 200)
            self.assertEqual(
                result["work_orders"][0]["appointment_control"]["status"],
                "Committed" if kind == "capacity" else "Offer",
            )
        self.assertEqual(len(self.store._work_order("WO-0001")["appointment_events"]), 4)

    def test_human_home_case_closure_http_evidence_denials_reset_and_committed_retry(self) -> None:
        from unittest.mock import patch

        self.call(f"/api/packages/{self.pid}/capacity", self.capacity())
        self.call("/api/workorders", self.issue())
        route = "/api/workorders/WO-0001/appointment-control"
        supplied_appointment_fixture(self.store, self.manager, "WO-0001")
        state = self.call("/api/workorders")[1][0]["appointment_control"]
        update = self.store.detail("ZF-1")["resident_update"]
        body = dict(
            action="close_case",
            event_ref="HTTP-HUMAN-CLOSE",
            case_id="ZF-1",
            expected_case_version=state["case_version"],
            confirmed=True,
            source="SYN supplied human closure",
            source_version="SYN-1",
            reason="SYN human decision",
        )
        for actor in ("kim", "kai"):
            self.assertEqual(self.call(route, body, actor)[0], 403)
        for delta in (
            {"source": ""},
            {"reason": ""},
            {"source_version": ""},
            {"confirmed": False},
            {"case_id": "ZF-2"},
            {"at": "2000-01-01"},
        ):
            self.assertEqual(self.call(route, dict(body, **delta))[0], 400)
        self.assertEqual(self.call(route, dict(body, expected_case_version="stale"))[0], 409)
        self.assertFalse(self.store.detail("ZF-1")["closed"])
        with patch.object(
            self.store, "list_packages", side_effect=OSError("SYN closure projection")
        ):
            code, result = self.call(route, body)
        self.assertEqual((code, result["outcome"]), (409, "committed"))
        code, result = self.call(route, body)
        self.assertEqual(code, 200)
        state = result["work_orders"][0]["appointment_control"]
        self.assertTrue(state["case_closed"])
        self.assertEqual(state["eligible_no_access"], 0)
        self.assertEqual(len(state["closure_history"]), 1)
        self.assertEqual(state["closure_history"][0]["actor"]["email"], self.manager["email"])
        self.assertEqual(self.store.detail("ZF-1")["resident_update"], update)
        self.assertEqual(
            self.call(
                route,
                dict(body, event_ref="CLOSE-AGAIN", expected_case_version=state["case_version"]),
            )[0],
            400,
        )
        self.store.reopen_case(
            self.manager,
            "ZF-1",
            "SYN human reopen",
            metadata=dict(source="SYN review", next_action="Human review"),
        )
        self.assertEqual(self.call(route, body)[0], 200)
        self.assertFalse(self.store.detail("ZF-1")["closed"])
        self.assertEqual(len(self.store.cases["ZF-1"]["home_case_closures"]), 1)
        self.assertTrue(self.store.verify_audit())

    def test_response_only_encoder_failure_is_truthful_for_confirmation_and_closure(self) -> None:
        from unittest.mock import patch

        self.call(f"/api/packages/{self.pid}/capacity", self.capacity())
        self.call("/api/workorders", self.issue())
        route = "/api/workorders/WO-0001/appointment-control"
        ref = supplied_appointment_fixture(self.store, self.manager, "WO-0001", confirmations=False)
        state = self.call("/api/workorders")[1][0]["appointment_control"]
        encode = json.dumps

        def fault(obj: Any, *args: Any, **kwargs: Any) -> str:
            if (
                isinstance(obj, dict)
                and obj.get("work_orders")
                and "appointment_control" in obj["work_orders"][0]
            ):
                raise ValueError("SYN response-only encoder failure")
            return encode(obj, *args, **kwargs)

        bodies = [
            dict(
                action="confirm",
                event_ref="SERIAL-CONFIRM",
                offer_id=ref,
                kind="resident",
                person="Pat Test",
                source="SYN human",
                channel="Phone",
            ),
            dict(
                action="close_case",
                event_ref="SERIAL-CLOSE",
                case_id="ZF-1",
                expected_case_version=state["case_version"],
                confirmed=True,
                source="SYN human",
                source_version="SYN-1",
                reason="SYN human decision",
            ),
        ]
        for body in bodies:
            with patch.object(json, "dumps", side_effect=fault):
                code, result = self.call(route, body)
            self.assertEqual((code, result.get("outcome")), (409, "committed"))
            self.assertIn("Reload", result["error"])
            self.assertEqual(
                sum(
                    e["ref"] == body["event_ref"]
                    for e in self.store._work_order("WO-0001")["appointment_events"]
                ),
                1,
            )
            self.assertEqual(self.call(route, body)[0], 200)
            self.assertEqual(
                sum(
                    e["ref"] == body["event_ref"]
                    for e in self.store._work_order("WO-0001")["appointment_events"]
                ),
                1,
            )
        self.assertEqual(len(self.store.cases["ZF-1"]["home_case_closures"]), 1)

    def test_bundle_competence_http_requires_bounded_text_and_exact_scope(self) -> None:
        self.call(f"/api/packages/{self.pid}/capacity", self.capacity())
        self.call("/api/workorders", self.issue())
        supplied_appointment_fixture(self.store, self.manager, "WO-0001", confirmations=False)
        w = self.store._work_order("WO-0001")
        body = dict(
            w["appointment_events"][0]["body"],
            event_ref="BUNDLE",
            bundle=True,
            bundle_agreed=True,
            expected_offer_id=w["appointment_offer"]["id"],
        )
        route = "/api/workorders/WO-0001/appointment-control"
        bad_values: tuple[Any, ...] = ("", " \t ", None, 42, True, [], {}, "x" * 501)
        for bad in bad_values:
            with self.subTest(bad=bad):
                self.assertEqual(
                    self.call(
                        route,
                        dict(
                            body,
                            competence=dict(scope=self.store._appointment_binding(w), source=bad),
                        ),
                    )[0],
                    400,
                )
        self.assertEqual(
            self.call(route, dict(body, competence=dict(scope={}, source="SYN")))[0], 400
        )
        self.assertEqual(
            self.call(
                route,
                dict(
                    body,
                    competence=dict(
                        scope=self.store._appointment_binding(w), source="SYN exact competence"
                    ),
                ),
            )[0],
            200,
        )

    def test_withdrawal_http_ends_current_appointment_for_staff_and_provider(self) -> None:
        self.call(f"/api/packages/{self.pid}/capacity", self.capacity())
        self.call("/api/workorders", self.issue())
        supplied_appointment_fixture(self.store, self.manager, "WO-0001")
        self.assertEqual(self.call("/api/workorders/WO-0001/withdraw", dict(reason="SYN"))[0], 200)
        for actor in ("pam", "kim"):
            self.assertEqual(
                self.call("/api/workorders", actor=actor)[1][0]["appointment_control"]["status"],
                "Ended",
            )
        for route, body in (
            ("/api/workorders/WO-0001/appointment", dict(outcome="Booked", date="2099-01-01")),
            ("/api/workorders/WO-0001/complete", dict(note="SYN")),
            ("/api/cases/ZF-1/advance", {}),
        ):
            self.assertEqual(self.call(route, body)[0], 400)

    def test_appointment_http_serialized_canaries_follow_existing_roles(self) -> None:
        self.call(f"/api/packages/{self.pid}/capacity", self.capacity())
        self.call("/api/workorders", self.issue())
        wid = "WO-0001"
        route = f"/api/workorders/{wid}/appointment-control"
        ref = supplied_appointment_fixture(self.store, self.manager, wid, confirmations=False)
        self.assertEqual(
            self.call(
                route,
                dict(
                    action="authority",
                    event_ref="PRIVATE-GRANT",
                    offer_id=ref,
                    representative_ref="SYN-REP",
                    person="SYN Helper",
                    source="PRIVATE-AUTHORITY",
                    valid_from="2026-01-01",
                    valid_to="2099-12-31",
                    revoked=False,
                ),
            )[0],
            200,
        )
        for kind, person in (
            ("resident", "SYN Helper"),
            ("staff", self.manager["name"]),
            ("capacity", "SYN supplier"),
        ):
            self.assertEqual(
                self.call(
                    route,
                    dict(
                        action="confirm",
                        event_ref="PRIVATE-" + kind,
                        offer_id=ref,
                        kind=kind,
                        person=person,
                        source="PRIVATE-CONFIRMATION",
                        channel="Phone",
                        representative_ref="SYN-REP" if kind == "resident" else None,
                    ),
                )[0],
                200,
            )
        self.assertEqual(
            self.call(
                route,
                dict(action="configure", event_ref="PRIVATE-RULE", threshold=0, basis="SYN human"),
            )[0],
            200,
        )
        self.assertEqual(
            self.call(
                route,
                dict(
                    action="outcome",
                    event_ref="PRIVATE-OUTCOME",
                    offer_id=ref,
                    cause="Resident",
                    owner="SYN human",
                    source="SYN checked",
                    verified=True,
                    no_access=True,
                    preference_breach=False,
                    abortive=False,
                ),
            )[0],
            200,
        )
        self.assertEqual(
            self.call(
                route,
                dict(
                    action="investigation",
                    event_ref="PRIVATE-INVESTIGATION",
                    checks={
                        key: "PRIVATE-CIRCUMSTANCES"
                        for key in (
                            "confirmation",
                            "notice",
                            "attendance",
                            "adjustments",
                            "contact",
                            "circumstances",
                        )
                    },
                    corrective_action="PRIVATE-CIRCUMSTANCES",
                    next_update="SYN human",
                    disposition="SYN task reviewed",
                ),
            )[0],
            200,
        )
        state = self.call("/api/workorders")[1][0]["appointment_control"]
        self.assertEqual(
            self.call(
                route,
                dict(
                    action="close_case",
                    event_ref="PRIVATE-CLOSE",
                    case_id="ZF-1",
                    expected_case_version=state["case_version"],
                    confirmed=True,
                    source="PRIVATE-CLOSURE-SOURCE",
                    source_version="SYN-1",
                    reason="PRIVATE-CLOSURE",
                ),
            )[0],
            200,
        )
        markers = (
            "PRIVATE-AUTHORITY",
            "PRIVATE-CONFIRMATION",
            "PRIVATE-CIRCUMSTANCES",
            "PRIVATE-CLOSURE",
            "SYN agreed morning only",
        )
        privileged = json.dumps(self.call("/api/workorders")[1])
        self.assertTrue(all(marker in privileged for marker in markers))
        for actor in ("quil", "kim"):
            code, rows = self.call("/api/workorders", actor=actor)
            self.assertEqual(code, 200)
            payload = json.dumps(rows)
            for marker in markers:
                self.assertNotIn(marker, payload)
                self.assertNotIn(marker, json.dumps(list(self.store.audit_entries())))
            self.assertIn("Knock and wait", payload)
            self.assertIn("2099-01-01", payload)
            summary = self.store.appointment_summary(
                self.store._work_order(wid), self.store.staff[f"{actor}@example.test"]
            )
            self.assertNotIn("closure_history", summary)
        from unittest.mock import patch

        with patch.dict("os.environ", {"ZF_REASON_ROLES": ""}):
            payload = json.dumps(self.call("/api/workorders")[1])
            self.assertFalse(any(marker in payload for marker in markers))
        with self.assertRaises(PermissionError):
            self.store.appointment_summary(
                self.store._work_order(wid),
                dict(self.store.staff["quil@example.test"], name="Forged"),
            )


class JsonProcurementApi(ProcurementApi):
    sql = False


class ConsultationApi(ProcurementApiFixture):
    def decision(self, status: str = "unknown", version: int = 0) -> dict[str, Any]:
        return dict(
            status=status,
            expected_version=version,
            decided_by="Fictional human adviser; Legal authority unverified",
            reason="SYN supplied human decision, not approval",
            **{
                key: self.details[key]
                for key in ("source_case_id", "document_id", "source_version")
            },
        )

    def test_supplied_decisions_do_not_hold_unrelated_service_orders(self) -> None:
        route = f"/api/packages/{self.pid}/consultation"
        self.assertEqual(self.call(f"/api/packages/{self.pid}/capacity", self.capacity())[0], 200)
        for version, status in enumerate(("unknown", "applies", "complete", "not_applicable")):
            code, result = self.call(route, self.decision(status, version))
            self.assertEqual(code, 200)
            row = result["packages"][0]
            self.assertEqual(row["consultation_status"], "unknown")
            self.assertEqual(row["consultation_history"][-1]["status"], status)
            self.assertEqual(row["consultation_authority"], "Unverified")
            with self.assertRaisesRegex(ValueError, "Consultation status is unknown"):
                self.store.require_consultation_clear(self.store._package(self.pid))
        self.assertEqual(self.call("/api/workorders", self.issue("ZF-3"))[0], 200)
        self.assertEqual(len(self.call("/api/workorders")[1]), 1)
        for action in ("let", "renew"):
            code, _ = self.call(f"/api/packages/{self.pid}/{action}", {})
            self.assertEqual(code, 404)

    def test_consultation_route_rejects_actor_and_claimed_authority(self) -> None:
        route = f"/api/packages/{self.pid}/consultation"
        for actor in ("sam", "kim"):
            self.assertEqual(self.call(route, self.decision(), actor)[0], 403)
        for extra in (
            dict(authority_status="Approved"),
            dict(recorded_by=self.manager),
            dict(bulk=True),
        ):
            self.assertEqual(self.call(route, dict(self.decision(), **extra))[0], 400)
        self.assertEqual(self.store.list_packages(self.manager)[0]["consultation_history"], [])

    def test_explicit_held_scope_is_not_released_by_a_supplied_decision(self) -> None:
        self.assertEqual(self.call(f"/api/packages/{self.pid}/capacity", self.capacity())[0], 200)
        self.assertEqual(
            self.call(f"/api/packages/{self.pid}/consultation", self.decision("complete"))[0],
            200,
        )
        with self.store.lock:
            building = fixture()["buildings"][0]
            building["works"], building["costs"] = [], []
            building["holds"] = [
                dict(
                    hold(),
                    label="SYN consultation-dependent work awaiting human review",
                    status="Unknown",
                    case_ids=["ZF-3"],
                    package_ids=[self.pid],
                )
            ]
            self.store.data["buildings"] = [building]
            self.store._case("ZF-3")["building_id"] = building["id"]
            self.store.save()
        before = copy.deepcopy(self.store.data["procurement"])
        audit = list(self.store.audit_entries())
        code, result = self.call("/api/workorders", self.issue("ZF-3"))
        self.assertEqual(code, 409)
        self.assertIn("consultation-dependent", " ".join(result["reasons"]))
        self.assertEqual(self.store.data["procurement"], before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertEqual(self.call("/api/workorders", self.issue("ZF-1"))[0], 200)

    def test_consultation_version_conflict_and_source_failure(self) -> None:
        route = f"/api/packages/{self.pid}/consultation"
        self.assertEqual(self.call(route, dict(self.decision(), source_version="missing"))[0], 400)
        self.assertEqual(self.call(route, self.decision())[0], 200)
        self.assertEqual(self.call(route, self.decision("complete"))[0], 409)
        row = self.store.list_packages(self.manager)[0]
        self.assertEqual(len(row["consultation_history"]), 1)
        self.assertEqual(
            row["consultation_history"][0]["recorded_by"]["email"], self.manager["email"]
        )


class JsonConsultationApi(ConsultationApi):
    sql = False
