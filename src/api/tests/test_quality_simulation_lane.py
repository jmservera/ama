"""E4 regressions for issue 1288: the public synthetic simulation lane (CANDIDATE design).

A real Ai client, a real loopback TLS peer, a counting meter and a counted credential are the
production transport composition; nothing here mocks the sealed boundary. Synthetic public data
only; no live model call, no Azure, no private data."""

import json
import os
import re
import shutil
import sqlite3
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

from zava_forward.core import ai_consumption, simulation_lane
from zava_forward.core.assistants import Assistants

import test_assistants as ta
import test_quality_sensors_c7 as c7
import test_quality_sensors_e2 as e2
from zava_forward.api.server import App

SENSOR_KEY = re.compile(rb"sensor:SENS-SYN-PUB1:LIVE-SENS-SYN-PUB1-[0-9TZ]+")


def counted_reply(body: bytes) -> bytes:
    reply = json.loads(valid_reply(body))
    reply["usage"] = {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120}
    return json.dumps(reply).encode()


def valid_reply(body: bytes) -> bytes:
    key = SENSOR_KEY.search(body)
    assert key is not None
    output = {
        "summary": "Public simulation summary.",
        "findings": [{"text": "Fixture reading cited.", "citations": [key.group().decode()]}],
        "unknowns": [],
    }
    return json.dumps(
        {
            "model": "test-model",
            "choices": [{"message": {"content": json.dumps(output)}}],
            "usage": {},
        }
    ).encode()


@unittest.skipUnless(e2.OPENSSL, "needs the openssl CLI to build a loopback certificate")
class Lane(c7.Base):
    meter: e2.CountingMeter
    tokens: list[int]

    def tls_ai(
        self, before: Callable[[], object] | None = None, trickle: bool = True
    ) -> tuple[e2.TlsPeer, Any]:
        boundary: Any = self
        peer, ai = e2.Boundary.tls_ai(boundary, before, trickle)
        return peer, ai

    def provision(self, name: str) -> tuple[str, str]:
        store, key = os.path.join(self.dir, f"{name}.sqlite"), os.path.join(self.dir, f"{name}.key")
        simulation_lane.provision(store, key, working=(self.working,))
        return store, key

    def setUp(self) -> None:
        self.dir = tempfile.mkdtemp(prefix="zf-sim-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.working = os.path.join(self.dir, "working-placeholder.sqlite")
        store, key = self.provision("lane")
        patcher = patch.dict(
            os.environ, {simulation_lane.STORE_ENV: store, simulation_lane.KEY_ENV: key}
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        super().setUp()
        lane = self.app.simulation
        assert lane is not None
        self.lane: simulation_lane.Lane = lane
        self.addCleanup(self.lane.close)

    def attempt(self, seal: Any, system: str, prompt: str, max_tokens: int = 600) -> dict[str, Any]:
        with ai_consumption.captured_readings(True), ai_consumption.sealed_simulation(seal):
            envelope: dict[str, Any] = self.ai.evidence(system, prompt, max_tokens, 20)
        return envelope

    def start(self) -> tuple[e2.TlsPeer, dict[str, Any]]:
        peer, self.ai = self.tls_ai()
        peer.reply = valid_reply
        self.ai.simulation_verifier = self.lane.verify
        self.lane.observe()
        return peer, self.lane.compose()

    def nothing_left(self, peer: e2.TlsPeer, accepts: int = 0) -> None:
        self.assertEqual((peer.accepts, peer.bytes > 0), (accepts, bool(accepts)))
        self.assertEqual((self.meter.reserved, self.meter.checked), (accepts, accepts))
        self.assertEqual(len(self.tokens), accepts)

    def test_the_sealed_request_sends_exactly_the_composed_public_payload(self) -> None:
        peer, composed = self.start()
        working_before = self.domain()
        status, state = self.request("/api/assistants/simulation/quality")
        self.assertEqual((status, state["status"]), (200, "ready"))
        shown = {
            (r["reading_id"], r["temperature_c"], r["humidity_pct"])
            for r in state["view"]["readings"]
        }
        status, result = self.request("/api/assistants/simulation/quality/request", {})
        self.assertEqual(
            (status, result["status"], result["state"]), (200, "proposal", "unapproved-proposal")
        )
        self.assertEqual(len(peer.bodies), 1)
        sent = peer.bodies[0]
        self.assertEqual(
            sent, composed["body"]
        )  # the production transport carried the sealed bytes
        self.assertEqual({tuple(r) for r in result["readings"]}, shown)
        for reading_id, temperature, humidity in shown:
            self.assertIn(reading_id.encode(), sent)
            self.assertIn(f'\\"temperature_c\\":\\"{temperature}\\"'.encode(), sent)
            self.assertIn(f'\\"humidity_pct\\":\\"{humidity}\\"'.encode(), sent)
        self.assertIn(b"1 Fixture Row", sent)
        private = self.store._case("ZF-1")
        self.assertNotIn(private["home"]["address"].encode(), sent)
        self.assertNotIn(b"ZF-1", sent)
        self.assertEqual((self.meter.reserved, self.meter.checked, len(self.tokens)), (1, 1, 1))
        self.assertEqual(self.domain(), working_before)  # no controlled-domain mutation
        last = self.lane.last_proposal()
        assert last is not None
        self.assertEqual(last["state"], "unapproved-proposal")
        self.assertIn("synthetic", result["label"].lower())

    def test_every_refusal_happens_before_meter_token_or_socket(self) -> None:
        peer, composed = self.start()
        system, prompt, body = composed["system"], composed["prompt"], composed["body"]
        good = self.lane.mint(body)
        other_store, other_key = self.provision("other")
        other = simulation_lane.Lane.open(
            {simulation_lane.STORE_ENV: other_store, simulation_lane.KEY_ENV: other_key}
        )
        self.addCleanup(other.close)
        cross = other.mint(body)
        cases: dict[str, tuple[Any, str, str]] = {
            "forged-mac": (dict(good, mac="0" * 64), prompt, "signature"),
            "altered-body": (good, prompt + " ", "payload-mismatch"),
            "other-namespace": (dict(good, ns="public"), prompt, "signature"),
            "other-store-claim": (dict(good, store=other.store_id), prompt, "signature"),
            "cross-store-seal": (cross, prompt, "signature"),
            "unsigned-digest": ({"digest": good["digest"]}, prompt, "malformed"),
            "boolean": (True, prompt, "malformed"),
            "free-text-claim": (dict(good, ns="synthetic public simulation"), prompt, "signature"),
        }
        for name, (seal, text, code) in cases.items():
            with self.subTest(name):
                envelope = self.attempt(seal, system, text)
                self.assertEqual(
                    (envelope["outcome"], envelope["reason"]), ("simulation-refused", code)
                )
                self.nothing_left(peer)
        with self.subTest("private working-store payload under a fixture seal"):
            private = json.dumps(self.store._case("ZF-1"))
            envelope = self.attempt(good, system, private)
            self.assertEqual(envelope["reason"], "payload-mismatch")
            self.nothing_left(peer)
        with self.subTest("expired"):
            expired = self.lane.mint(body)
            self.lane.clock = lambda: time.time() + 10_000
            self.assertEqual(self.attempt(expired, system, prompt)["reason"], "expired")
            self.lane.clock = time.time
            self.nothing_left(peer)
        with self.subTest("no verifier installed"):
            self.ai.simulation_verifier = None
            self.assertEqual(self.attempt(good, system, prompt)["reason"], "verifier-unavailable")
            self.nothing_left(peer)
        with self.subTest("captured readings without a seal stay refused (private route off)"):
            self.ai.simulation_verifier = self.lane.verify
            with ai_consumption.captured_readings(True):
                envelope = self.ai.evidence(system, prompt, 600, 20)
            self.assertEqual(envelope["outcome"], "suspended-before-dispatch")
            self.nothing_left(peer)

    def test_a_seal_is_single_use(self) -> None:
        peer, composed = self.start()
        seal = self.lane.mint(composed["body"])
        first = self.attempt(seal, composed["system"], composed["prompt"])
        self.assertEqual(first["outcome"], "returned")
        again = self.attempt(seal, composed["system"], composed["prompt"])
        self.assertEqual((again["outcome"], again["reason"]), ("simulation-refused", "replayed"))
        self.nothing_left(peer, accepts=1)

    def test_existing_guards_still_apply(self) -> None:
        peer, _ = self.start()
        with patch.object(Assistants, "suspended", return_value="Release suspended."):
            result = self.request("/api/assistants/simulation/quality/request", {})[1]
        self.assertEqual((result["status"], result["reason"]), ("held", "Release suspended."))
        self.nothing_left(peer)
        meter, self.ai.consumption = self.ai.consumption, None
        result = self.request("/api/assistants/simulation/quality/request", {})[1]
        self.ai.consumption = meter
        self.assertEqual(
            (result["status"], result["reason"]), ("not-sent", "financial-meter-unavailable")
        )
        self.nothing_left(peer)
        with patch.object(Assistants, "dispatch_hold", return_value="Suspended."):
            result = self.request("/api/assistants/simulation/quality/request", {})[1]
        self.assertEqual(result["status"], "held")
        self.assertIsNone(self.lane.last_proposal())  # output discarded after a late hold

    def test_an_unconfigured_lane_is_unavailable_and_sends_nothing(self) -> None:
        peer, _ = self.start()
        self.app.simulation, self.app.simulation_reason = None, "not-configured"
        self.assertEqual(
            self.request("/api/assistants/simulation/quality")[1]["status"], "unavailable"
        )
        status, result = self.request("/api/assistants/simulation/quality/request", {})
        self.assertEqual((status, result["status"]), (200, "unavailable"))
        self.assertIn("manual route", result["manual_route"])
        self.nothing_left(peer)

    def test_the_store_and_key_must_be_separate_and_safe(self) -> None:
        store, key = self.provision("again")
        for name, settings, code in (
            ("unset", {}, "not-configured"),
            ("missing store", {"store": store + "x", "key": key}, "store-unavailable"),
            ("same file", {"store": key, "key": key}, "store-not-separate"),
            ("working database", {"store": self.store.db_path, "key": key}, "store-not-simulation"),
        ):
            with self.subTest(name):
                values = {
                    simulation_lane.STORE_ENV: settings.get("store", ""),
                    simulation_lane.KEY_ENV: settings.get("key", ""),
                }
                with self.assertRaises(simulation_lane.Unavailable) as caught:
                    simulation_lane.Lane.open(values, working=(self.store.db_path + "-other",))
                self.assertEqual(caught.exception.code, code)
        with self.assertRaises(simulation_lane.Unavailable) as caught:
            simulation_lane.Lane.open(
                {simulation_lane.STORE_ENV: self.store.db_path, simulation_lane.KEY_ENV: key},
                working=(self.store.db_path,),
            )
        self.assertEqual(caught.exception.code, "store-not-separate")
        os.chmod(key, 0o644)
        with self.assertRaises(simulation_lane.Unavailable) as caught:
            simulation_lane.Lane.open(
                {simulation_lane.STORE_ENV: store, simulation_lane.KEY_ENV: key}
            )
        self.assertEqual(caught.exception.code, "key-unsafe")
        with self.assertRaises(simulation_lane.Unavailable):
            simulation_lane.provision(self.store.db_path + "-new", self.store.db_path + "-new")

    def test_only_quality_roles_may_use_the_routes(self) -> None:
        for role, expected in (("Contractor", 403), ("Retrofit Programme Manager", 200)):
            self.user = self.people[role]
            self.assertEqual(self.request("/api/assistants/simulation/quality")[0], expected)
            self.assertEqual(
                self.request("/api/assistants/simulation/quality/observe", {})[0], expected
            )

    def authority(self, **settings: Any) -> Assistants:
        """A real Assistants over the working store with its own operator authority settings."""
        service = Assistants(self.store, ta.config(**settings))
        self.addCleanup(service.stop)
        self.app.assistants = service
        self.ai.consumption = (
            self.meter
        )  # the service installs its own ledger; keep the counting meter
        return service

    def post(self) -> dict[str, Any]:
        status, result = self.request("/api/assistants/simulation/quality/request", {})
        self.assertEqual(status, 200)
        result_dict: dict[str, Any] = result
        return result_dict

    def allowance(self) -> tuple[int, int]:
        with self.service.transaction() as db:
            row = db.execute(
                "SELECT SUM(used_calls),SUM(reserved_tokens) FROM assistant_allowance"
            ).fetchone()
        return int(row[0] or 0), int(row[1] or 0)

    def active_attempts(self) -> int:
        with self.service.transaction() as db:
            now = self.service.now(db)
            return int(
                db.execute(
                    "SELECT COUNT(*) FROM assistant_attempts WHERE active_until>?", (now,)
                ).fetchone()[0]
            )

    def test_missing_invalid_expired_and_schema_error_authority_declines_before_the_model(
        self,
    ) -> None:
        peer, _ = self.start()
        cases: dict[str, dict[str, Any]] = {
            "missing authority": dict(authority=""),
            "invalid allowance": dict(call_allowance=0),
            "token allowance below one reservation": dict(token_allowance=1000),
            "expired authority": dict(expires="2000-01-01T00:00:00Z"),
        }
        for name, settings in cases.items():
            with self.subTest(name):
                self.authority(**settings)
                result = self.post()
                self.assertEqual(result["status"], "held")
                self.assertTrue(result["reason"])
                self.assertEqual(self.allowance(), (0, 0))
                self.nothing_left(peer)
        with self.subTest("schema error"):
            self.authority().schema_error = (
                "Assistant schema unavailable; operator migration required."
            )
            result = self.post()
            self.assertEqual(
                (result["status"], result["reason"][:16]), ("held", "Assistant schema")
            )
            self.nothing_left(peer)
        self.assertIsNone(self.lane.last_proposal())

    def test_the_durable_allowance_bounds_calls_and_keeps_uncertain_tokens_reserved(self) -> None:
        peer, _ = self.start()
        service = self.authority(call_allowance=1)
        self.assertEqual(self.post()["status"], "proposal")
        exhausted = self.post()
        self.assertEqual(exhausted["status"], "held")
        self.assertIn("allowance exhausted", exhausted["reason"])
        self.nothing_left(peer, accepts=1)
        used, reserved = self.allowance()
        self.assertEqual(
            (used, reserved), (1, service.limits.reservation)
        )  # usage unknown: liability kept
        self.assertEqual(self.active_attempts(), 0)

        self.authority(token_allowance=13000)
        self.assertEqual(
            self.post()["status"], "held"
        )  # the earlier liability leaves no second reservation
        self.nothing_left(peer, accepts=1)

    def test_known_usage_settles_the_reservation_and_the_slots_are_released(self) -> None:
        peer, _ = self.start()
        peer.reply = counted_reply
        service = self.authority(active_calls=1)
        self.assertEqual(self.post()["status"], "proposal")
        self.assertEqual(self.allowance(), (1, 120))
        self.assertEqual(self.active_attempts(), 0)
        self.assertTrue(service.call_slots.acquire(blocking=False))
        service.call_slots.release()
        self.assertEqual(self.post()["status"], "proposal")
        self.nothing_left(peer, accepts=2)

    def test_parallel_posts_cannot_exceed_the_physical_and_durable_call_slots(self) -> None:
        peer, _ = self.start()
        entered, release, calls = threading.Event(), threading.Event(), []

        def hold_first() -> None:
            calls.append(1)
            if len(calls) == 1:
                entered.set()
                release.wait(15)

        self.meter.before = hold_first
        service = self.authority(active_calls=1)
        first: list[dict[str, Any]] = []
        thread = threading.Thread(target=lambda: first.append(self.post()))
        thread.start()
        self.assertTrue(entered.wait(15))
        results = [self.post() for _ in range(3)]
        self.assertEqual([r["status"] for r in results], ["held"] * 3)
        self.assertEqual((self.meter.reserved, peer.accepts, self.allowance()[0]), (1, 0, 1))
        release.set()
        thread.join(30)
        self.assertEqual(first[0]["status"], "proposal")
        self.assertEqual(self.post()["status"], "proposal")
        self.assertEqual((self.meter.reserved, peer.accepts, self.allowance()[0]), (2, 2, 2))
        self.assertEqual(self.active_attempts(), 0)
        self.assertTrue(service.call_slots.acquire(blocking=False))

    def test_a_failed_provider_call_releases_the_physical_slot_but_keeps_the_durable_one(
        self,
    ) -> None:
        peer, _ = self.start()
        service = self.authority(active_calls=1)
        unreachable = dict(
            outcome="provider-unavailable", usage=None, reason="provider-unavailable"
        )
        with patch.object(self.ai, "evidence", return_value=unreachable):
            failed = self.post()
        self.assertEqual(
            (failed["status"], failed["reason"]), ("model-failed", "provider-unavailable")
        )
        self.assertEqual(self.allowance()[0], 1)
        self.assertTrue(service.call_slots.acquire(blocking=False))  # physical slot freed
        service.call_slots.release()
        again = self.post()  # uncertain outcome keeps its durable slot to lease expiry
        self.assertEqual((again["status"], "active-call slot" in again["reason"]), ("held", True))
        self.assertEqual(peer.accepts, 0)

    def test_reduced_authority_bounds_the_sealed_body_and_oversized_input_is_declined(self) -> None:
        peer, _ = self.start()
        self.authority(output_tokens=100)
        self.assertEqual(self.post()["status"], "proposal")
        self.assertEqual(json.loads(peer.bodies[0])["max_tokens"], 100)
        self.authority(input_chars=1000)
        refused = self.post()
        self.assertEqual(refused["status"], "held")
        self.nothing_left(peer, accepts=1)

    def test_a_ticket_settles_once_and_a_second_end_cannot_release_another_slot(self) -> None:
        self.start()
        service = self.authority(active_calls=2)
        ticket = service.begin_call(simulation_lane.CAPABILITY, 500, "a" * 64)
        self.assertIsNone(ticket.reason)
        other = service.begin_call(simulation_lane.CAPABILITY, 500, "b" * 64)
        self.assertIsNone(other.reason)
        refused = service.begin_call(simulation_lane.CAPABILITY, 500, "c" * 64)
        self.assertIn("active-call slot", refused.reason or "")
        envelope = dict(
            outcome="returned", usage=dict(prompt_tokens=1, completion_tokens=1, total_tokens=2)
        )
        ticket.end(envelope)
        ticket.end(envelope)
        self.assertEqual(self.allowance()[1], service.limits.reservation + 2)
        replacement = service.begin_call(simulation_lane.CAPABILITY, 500, "d" * 64)
        self.assertIsNone(replacement.reason)  # exactly one slot came back
        self.assertIsNotNone(service.begin_call(simulation_lane.CAPABILITY, 500, "9" * 64).reason)
        other.end(envelope)
        replacement.end(envelope)
        again = service.begin_call(simulation_lane.CAPABILITY, 500, "e" * 64)
        self.assertIsNone(again.reason)
        again.end(envelope)

    def test_a_pre_dispatch_failure_releases_the_slot_and_never_sends(self) -> None:
        peer, _ = self.start()
        service = self.authority(active_calls=1)
        with patch.object(
            simulation_lane.Lane, "mint", side_effect=sqlite3.OperationalError("seal store")
        ):
            with self.assertRaises(sqlite3.OperationalError):
                self.lane.request(self.ai, self.admission(service))
        self.nothing_left(peer)
        self.assertTrue(service.call_slots.acquire(blocking=False))
        service.call_slots.release()

    def admission(self, service: Assistants) -> "simulation_lane.Admission":
        return self.app.simulation_admission(service)

    def test_an_unavailable_authority_store_declines_with_the_manual_route(self) -> None:
        peer, _ = self.start()
        service = self.authority()
        with patch.object(
            type(service), "transaction", side_effect=sqlite3.OperationalError("down")
        ):
            ticket = service.begin_call(simulation_lane.CAPABILITY, 500, "f" * 64)
        self.assertIn("manual", ticket.reason or "")
        self.assertTrue(service.call_slots.acquire(blocking=False))
        service.call_slots.release()
        self.nothing_left(peer)

    def test_an_unreadable_key_or_invalid_simulation_meta_leaves_the_app_working(self) -> None:
        store, key = self.provision("fragile")
        real_open = open

        def refuse_key(file: Any, *args: Any, **kwargs: Any) -> Any:
            if file == key:
                raise PermissionError(13, "Permission denied", key)
            return real_open(file, *args, **kwargs)

        built: list[Any] = []
        real_store = simulation_lane.SqlStore

        def watch(*args: Any, **kwargs: Any) -> Any:
            built.append(real_store(*args, **kwargs))
            return built[-1]

        with patch.dict(
            os.environ, {simulation_lane.STORE_ENV: store, simulation_lane.KEY_ENV: key}
        ):
            with patch("builtins.open", refuse_key):
                app = App(self.store, provider=self.app.provider)
            self.assertEqual((app.simulation, app.simulation_reason), (None, "key-unreadable"))
            db = sqlite3.connect(store)
            db.execute("DROP TABLE sim_meta")
            db.execute("CREATE TABLE sim_meta (wrong TEXT)")
            db.commit()
            db.close()
            with patch.object(simulation_lane, "SqlStore", watch):
                app = App(self.store, provider=self.app.provider)
        self.assertEqual((app.simulation, app.simulation_reason), (None, "store-not-simulation"))
        self.assertEqual(len(built), 1)
        with self.assertRaises(sqlite3.ProgrammingError):
            built[0].db.execute("SELECT 1")  # the partial store was closed
        self.assertEqual(app.simulation_state(self.pm)["status"], "unavailable")
        self.assertEqual(self.request("/api/assistants")[0], 200)  # ordinary routes still work

    def test_a_store_that_cannot_be_opened_is_unavailable_not_a_crash(self) -> None:
        store, key = self.provision("unopenable")
        with patch.object(
            simulation_lane.sqlite3, "connect", side_effect=sqlite3.OperationalError("locked")
        ):
            with self.assertRaises(simulation_lane.Unavailable) as caught:
                simulation_lane.Lane.open(
                    {simulation_lane.STORE_ENV: store, simulation_lane.KEY_ENV: key}
                )
        self.assertEqual(caught.exception.code, "store-not-simulation")

    def test_the_stored_proposal_separates_supplied_from_cited_readings(self) -> None:
        self.start()
        self.assertEqual(self.post()["status"], "proposal")
        last = self.lane.last_proposal()
        assert last is not None
        supplied = {r[0] for r in last["readings"]}
        self.assertEqual(len(supplied), simulation_lane.SLOTS)
        self.assertEqual(len(last["cited"]), 1)
        self.assertTrue({r[0] for r in last["cited"]} <= supplied)
        self.lane.observe()
        self.lane.clock = lambda: time.time() + 3600
        self.lane.observe()
        self.lane.clock = time.time
        rotated = self.lane.last_proposal()
        assert rotated is not None
        self.assertEqual(rotated["readings"], last["readings"])  # historic IDs and values survive
        self.assertEqual(rotated["cited"], last["cited"])


if __name__ == "__main__":
    unittest.main()
