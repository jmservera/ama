"""E4 regressions for issue 1288: the public synthetic simulation lane (CANDIDATE design).

A real Ai client, a real loopback TLS peer, a counting meter and a counted credential are the
production transport composition; nothing here mocks the sealed boundary. Synthetic public data
only; no live model call, no Azure, no private data."""

import json
import os
import re
import shutil
import tempfile
import time
import unittest
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

from zava_forward.core import ai_consumption, simulation_lane

import test_quality_sensors_c7 as c7
import test_quality_sensors_e2 as e2

SENSOR_KEY = re.compile(rb"sensor:SENS-SYN-PUB1:LIVE-SENS-SYN-PUB1-[0-9TZ]+")


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
        with patch.object(
            type(self.app.assistants), "dispatch_hold", return_value="Release suspended."
        ):
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
        calls: list[int] = []

        def late(*_: object) -> str | None:
            calls.append(1)
            return None if len(calls) == 1 else "Suspended."

        with patch.object(type(self.app.assistants), "dispatch_hold", late):
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


if __name__ == "__main__":
    unittest.main()
