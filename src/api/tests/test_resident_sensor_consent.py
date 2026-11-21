"""Issue 2192: the resident sensor consent checkbox backend, fail-closed and owner-only."""

import unittest

from resident_demo_fixture import Client, DemoTestCase, make_row
from zava_forward.api.resident_demo import sensor_consent as sc


class FakePort:
    def __init__(self) -> None:
        self.states = {"ZF-1": "granted"}
        self.fail = False
        self.calls: list[tuple[str, bool]] = []

    def state(self, home_id: str) -> str:
        if self.fail:
            raise ValueError("down")
        return self.states.get(home_id, "unknown")

    def set(self, home_id: str, granted: bool) -> str:
        if self.fail:
            raise ValueError("down")
        self.calls.append((home_id, granted))
        self.states[home_id] = "granted" if granted else "declined"
        return self.states[home_id]


class SensorConsentTests(DemoTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.port = FakePort()
        self.app.sensor_consent = self.port
        self.reader.rows["C-1"] = make_row("C-1", "one@example.com", sensor_home_id="ZF-1")

    def signed_in(self) -> Client:
        client = self.client()
        self.assertEqual(client.login("one@example.com"), 200)
        return client

    def test_view_carries_the_card_and_withdrawal_then_grant_round_trips(self) -> None:
        client = self.signed_in()
        card = client.call("GET", "/demo/view")[1]["sensor_consent"]
        self.assertEqual((card["available"], card["state"]), (True, "granted"))
        status, body, _ = client.call("POST", "/demo/sensor-consent", {"granted": False})
        self.assertEqual((status, body["sensor_consent"]["state"]), (200, "declined"))
        self.assertIn("cannot see", body["sensor_consent"]["status"])
        status, body, _ = client.call("POST", "/demo/sensor-consent", {"granted": True})
        self.assertEqual(body["sensor_consent"]["state"], "granted")
        self.assertEqual(self.port.calls, [("ZF-1", False), ("ZF-1", True)])

    def test_unavailable_without_a_writer_or_when_the_store_fails(self) -> None:
        client = self.signed_in()
        self.port.fail = True
        self.assertFalse(client.call("GET", "/demo/view")[1]["sensor_consent"]["available"])
        status, body, _ = client.call("POST", "/demo/sensor-consent", {"granted": False})
        self.assertEqual((status, body["error"]), (503, sc.ERROR_TEXT))
        self.app.sensor_consent = None
        status, _, _ = client.call("POST", "/demo/sensor-consent", {"granted": False})
        self.assertEqual(status, 503)

    def test_refuses_bad_bodies_missing_csrf_and_residents_without_a_sensor_home(self) -> None:
        client = self.signed_in()
        for bad in ({"granted": "yes"}, {"granted": True, "home": "ZF-2"}, {}):
            self.assertEqual(client.call("POST", "/demo/sensor-consent", bad)[0], 400)
        self.assertEqual(self.port.calls, [])
        other = self.client()
        self.assertEqual(other.login("two@example.com"), 200)
        self.assertEqual(other.call("POST", "/demo/sensor-consent", {"granted": False})[0], 403)
        self.assertEqual(self.port.calls, [])
        anonymous = self.client()
        anonymous.prime()
        self.assertEqual(anonymous.call("POST", "/demo/sensor-consent", {"granted": False})[0], 401)

    def test_get_is_not_allowed(self) -> None:
        self.assertEqual(self.client().call("GET", "/demo/sensor-consent")[0], 405)


if __name__ == "__main__":
    unittest.main()
