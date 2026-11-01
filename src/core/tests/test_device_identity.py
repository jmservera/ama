import logging
import unittest
from collections.abc import Sequence

from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import sensor_stock

SECRET = "PRIVATE-KEY-MATERIAL"


class FakeRegistry:
    def __init__(self, fail_after: int | None = None) -> None:
        self.devices: dict[str, str] = {"SYN-OTHER": "other-run"}
        self.fail_after = fail_after

    def create(self, device_id: str, run_id: str) -> None:
        if self.fail_after is not None and len(self.devices) > self.fail_after:
            raise RuntimeError(SECRET)
        self.devices[device_id] = run_id

    def delete(self, device_id: str) -> None:
        self.devices.pop(device_id, None)

    def list_run(self, run_id: str) -> Sequence[str]:
        return [d for d, r in self.devices.items() if r == run_id]


class FakeStore:
    def __init__(self) -> None:
        self.secrets: dict[str, str] = {}

    def issue(self, device_id: str) -> str:
        reference = f"kv://zava-sim/{device_id.lower()}"
        self.secrets[reference] = SECRET
        return reference

    def revoke(self, reference: str) -> None:
        self.secrets.pop(reference, None)

    def references(self) -> Sequence[str]:
        return list(self.secrets)


def sensors(n: int = 5) -> list[dict[str, object]]:
    rows = [
        dict(
            synthetic_home_id=f"opaque-home-{i:03d}",
            building_form_osm="terrace",
            locality_theme="Locality A",
            is_synthetic="true",
            monitoring_consent="granted",
        )
        for i in range(n)
    ]
    return sensor_stock.select(rows, n).sensors(7)


class DeviceIdentityTests(unittest.TestCase):
    def test_each_home_maps_to_one_device_and_sensor(self) -> None:
        manifest = di.plan("run-001", "owner-role", sensors())
        self.assertEqual(len(manifest.identities), 5)
        self.assertEqual(len({i.device_id for i in manifest.identities}), 5)
        self.assertEqual(len({i.home_id for i in manifest.identities}), 5)
        self.assertTrue(all(i.device_id == "SYN-" + i.sensor_id for i in manifest.identities))

    def test_duplicate_home_rejected(self) -> None:
        rows = sensors(2)
        with self.assertRaisesRegex(di.DeviceIdentityError, "ONE_TO_ONE"):
            di.plan("run-001", "owner-role", [rows[0], rows[0]])

    def test_sensor_not_derived_from_home_rejected(self) -> None:
        bad = [{**sensors(1)[0], "home_id": "another-home"}]
        with self.assertRaisesRegex(di.DeviceIdentityError, "INVALID_DEVICE_IDENTITY"):
            di.plan("run-001", "owner-role", bad)

    def test_owner_and_run_required(self) -> None:
        with self.assertRaisesRegex(di.DeviceIdentityError, "INVALID_MANIFEST"):
            di.plan("run-001", " ", sensors())
        with self.assertRaisesRegex(di.DeviceIdentityError, "INVALID_MANIFEST"):
            di.plan("X", "owner-role", sensors())

    def test_provision_returns_references_only_and_logs_no_secret(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        with self.assertNoLogs(level=logging.DEBUG):
            done = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        self.assertEqual(len(registry.list_run("run-001")), 5)
        self.assertTrue(all(i.credential_ref.startswith("kv://") for i in done.identities))
        self.assertNotIn(SECRET, repr(done))
        self.assertNotIn("kv://", repr(done))

    def test_failure_rolls_back_without_leaking_secret(self) -> None:
        registry, store = FakeRegistry(fail_after=3), FakeStore()
        with self.assertRaises(di.DeviceIdentityError) as ctx:
            di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        self.assertNotIn(SECRET, str(ctx.exception))
        self.assertIsNone(ctx.exception.__cause__)
        self.assertEqual(registry.list_run("run-001"), [])
        self.assertEqual(store.references(), [])

    def test_teardown_removes_all_run_identities_and_only_those(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        done = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        di.teardown(done, registry, store)
        self.assertEqual(registry.list_run("run-001"), [])
        self.assertEqual(store.references(), [])
        self.assertEqual(registry.devices, {"SYN-OTHER": "other-run"})

    def test_teardown_fails_loudly_when_identity_remains(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        done = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        registry.delete = lambda device_id: None  # type: ignore[method-assign]
        with self.assertRaisesRegex(di.DeviceIdentityError, "TEARDOWN_INCOMPLETE:5"):
            di.teardown(done, registry, store)


if __name__ == "__main__":
    unittest.main()
