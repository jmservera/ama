import logging
import threading
import traceback
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
        if device_id in self.devices:
            raise RuntimeError(SECRET)
        self.devices[device_id] = run_id

    def run_of(self, device_id: str) -> str | None:
        return self.devices.get(device_id)

    def delete(self, device_id: str, run_id: str) -> None:
        if self.devices.get(device_id) == run_id:
            del self.devices[device_id]

    def list_run(self, run_id: str) -> Sequence[str]:
        return [d for d, r in self.devices.items() if r == run_id]


class FakeStore:
    def __init__(self) -> None:
        self.secrets: dict[str, str] = {}
        self.owners: dict[str, str] = {}
        self.counter = 0

    def issue(self, device_id: str, run_id: str) -> str:
        self.counter += 1
        reference = f"kv://zava-sim/{device_id.lower()}/{self.counter}"
        self.secrets[reference] = SECRET
        self.owners[reference] = run_id
        return reference

    def run_references(self, run_id: str) -> Sequence[str]:
        return [r for r, o in self.owners.items() if o == run_id and r in self.secrets]

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
        self.assertEqual([r for r in store.secrets], [])

    def test_teardown_removes_all_run_identities_and_only_those(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        done = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        di.teardown(done, registry, store)
        self.assertEqual(registry.list_run("run-001"), [])
        self.assertEqual([r for r in store.secrets], [])
        self.assertEqual(registry.devices, {"SYN-OTHER": "other-run"})

    def test_teardown_fails_loudly_when_identity_remains(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        done = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        registry.delete = lambda device_id, run_id: None  # type: ignore[method-assign]
        with self.assertRaisesRegex(di.DeviceIdentityError, "TEARDOWN_INCOMPLETE:5"):
            di.teardown(done, registry, store)

    def test_rollback_spares_preexisting_device(self) -> None:
        rows = sensors()
        existing = "SYN-" + str(rows[2]["sensor_id"])
        registry, store = FakeRegistry(), FakeStore()
        registry.devices[existing] = "other-run"
        with self.assertRaises(di.DeviceIdentityError):
            di.provision(di.plan("run-001", "owner-role", rows), registry, store)
        self.assertEqual(registry.devices, {"SYN-OTHER": "other-run", existing: "other-run"})
        self.assertEqual([r for r in store.secrets], [])

    def test_rollback_covers_device_whose_credential_issue_failed(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        original = store.issue
        calls: list[str] = []

        def flaky(device_id: str, run_id: str) -> str:
            calls.append(device_id)
            if len(calls) == 3:
                raise RuntimeError(SECRET)
            return original(device_id, run_id)

        store.issue = flaky  # type: ignore[method-assign]
        with self.assertRaisesRegex(di.DeviceIdentityError, "ROLLED_BACK"):
            di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        self.assertEqual(registry.list_run("run-001"), [])
        self.assertEqual([r for r in store.secrets], [])

    def test_rollback_revokes_credential_stored_before_issue_raised(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        original = store.issue

        def stores_then_raises(device_id: str, run_id: str) -> str:
            original(device_id, run_id)
            raise RuntimeError(SECRET)

        store.issue = stores_then_raises  # type: ignore[method-assign]
        with self.assertRaisesRegex(di.DeviceIdentityError, "ROLLED_BACK"):
            di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        self.assertEqual([r for r in store.secrets], [])

    def test_rollback_covers_registry_write_then_raise(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        original = registry.create

        def writes_then_raises(device_id: str, run_id: str) -> None:
            original(device_id, run_id)
            if len(registry.list_run(run_id)) == 3:
                raise RuntimeError(SECRET)

        registry.create = writes_then_raises  # type: ignore[method-assign]
        with self.assertRaisesRegex(di.DeviceIdentityError, "ROLLED_BACK"):
            di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        self.assertEqual(registry.devices, {"SYN-OTHER": "other-run"})
        self.assertEqual([r for r in store.secrets], [])

    def test_same_run_retry_is_rejected_without_mutation(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        manifest = di.plan("run-001", "owner-role", sensors())
        di.provision(manifest, registry, store)
        before = (dict(registry.devices), dict(store.secrets))
        with self.assertRaisesRegex(di.DeviceIdentityError, "RUN_ALREADY_ACTIVE"):
            di.provision(manifest, registry, store)
        self.assertEqual((registry.devices, store.secrets), before)

    def test_same_run_teardown_waits_for_provision_in_flight(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        manifest = di.plan("run-001", "owner-role", sensors())
        real_issue = store.issue
        paused = threading.Event()
        torn_down = threading.Event()

        def run_teardown() -> None:
            di.teardown(manifest, registry, store)
            torn_down.set()

        worker = threading.Thread(target=run_teardown)

        def issue(device_id: str, run_id: str) -> str:
            if not paused.is_set():
                paused.set()
                worker.start()
                self.assertFalse(torn_down.wait(timeout=0.2))
            return real_issue(device_id, run_id)

        store.issue = issue  # type: ignore[method-assign]
        done = di.provision(manifest, registry, store)
        worker.join(timeout=5)
        self.assertTrue(torn_down.is_set())
        self.assertEqual(len(done.identities), len(manifest.identities))
        self.assertEqual(registry.list_run("run-001"), [])
        self.assertEqual(store.references(), [])

    def test_overlapping_provision_cannot_roll_back_completed_attempt(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        manifest = di.plan("run-001", "owner-role", sensors())
        real_create = registry.create
        outcomes: list[str] = []
        started = threading.Event()

        def attempt() -> None:
            try:
                di.provision(manifest, registry, store)
            except di.DeviceIdentityError as error:
                outcomes.append(str(error))

        second = threading.Thread(target=attempt)

        def create(device_id: str, run_id: str) -> None:
            if not started.is_set():
                started.set()
                second.start()
                second.join(timeout=0.2)
            real_create(device_id, run_id)

        registry.create = create  # type: ignore[method-assign]
        first = di.provision(manifest, registry, store)
        second.join(timeout=5)
        self.assertEqual(outcomes, ["RUN_ALREADY_ACTIVE"])
        self.assertEqual(len(registry.list_run("run-001")), len(first.identities))
        self.assertEqual(len(store.run_references("run-001")), len(first.identities))

    def test_unknown_creation_ownership_reports_incomplete_rollback(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        real_create, real_run_of = registry.create, registry.run_of
        failing = {"on": False}

        def writes_then_raises(device_id: str, run_id: str) -> None:
            real_create(device_id, run_id)
            if len(registry.list_run(run_id)) == 3:
                failing["on"] = True
                raise RuntimeError(SECRET)

        def run_of(device_id: str) -> str | None:
            if failing["on"] and device_id == f"SYN-{sensors()[2]['sensor_id']}":
                raise RuntimeError(SECRET)
            return real_run_of(device_id)

        registry.create = writes_then_raises  # type: ignore[method-assign]
        registry.run_of = run_of  # type: ignore[method-assign]
        with self.assertRaises(di.DeviceIdentityError) as ctx:
            di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        self.assertEqual(str(ctx.exception), "PROVISION_ROLLBACK_INCOMPLETE")
        self.assertNotIn(SECRET, str(ctx.exception))
        self.assertEqual(len(registry.list_run("run-001")), 1)
        self.assertEqual(len(store.run_references("run-001")), 0)

    def test_active_run_check_failures_are_sanitised_without_mutation(self) -> None:
        for broken in ("registry", "store"):
            registry, store = FakeRegistry(), FakeStore()

            def boom(_run_id: str) -> Sequence[str]:
                raise RuntimeError(SECRET)

            if broken == "registry":
                registry.list_run = boom  # type: ignore[method-assign,assignment]
            else:
                store.run_references = boom  # type: ignore[method-assign,assignment]
            with self.assertRaises(di.DeviceIdentityError) as ctx:
                di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
            self.assertEqual(str(ctx.exception), "ACTIVE_RUN_CHECK_FAILED")
            self.assertIsNone(ctx.exception.__cause__)
            self.assertTrue(ctx.exception.__suppress_context__)
            self.assertEqual(registry.devices, {"SYN-OTHER": "other-run"})
            self.assertEqual(store.secrets, {})

    def test_overlapping_teardown_cannot_revoke_newer_run_credential(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        old = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        real_delete = registry.delete
        newer: list[di.Manifest] = []

        def delete_then_reprovision(device_id: str, run_id: str) -> None:
            real_delete(device_id, run_id)
            if not newer and not registry.list_run("run-001"):
                newer.append(
                    di.provision(di.plan("run-002", "owner-role", sensors()), registry, store)
                )

        registry.delete = delete_then_reprovision  # type: ignore[method-assign]
        di.teardown(old, registry, store)
        self.assertEqual(len(store.run_references("run-002")), 5)
        self.assertEqual(store.run_references("run-001"), [])

    def test_partial_manifest_teardown_is_refused_before_mutation(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        partial = di.plan("run-001", "owner-role", sensors(1))
        with self.assertRaisesRegex(di.DeviceIdentityError, "MANIFEST_INCOMPLETE"):
            di.teardown(partial, registry, store)
        for refs in ([], [i.credential_ref for i in partial.identities]):
            with self.assertRaisesRegex(di.DeviceIdentityError, "MANIFEST_INCOMPLETE"):
                di.teardown(partial, registry, store, refs=refs)
        self.assertEqual(len(registry.list_run("run-001")), 5)
        self.assertEqual(len(store.run_references("run-001")), 5)

    def test_teardown_inside_except_does_not_chain_caller_secret(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        partial = di.plan("run-001", "owner-role", sensors(1))
        captured: list[di.DeviceIdentityError] = []
        try:
            raise RuntimeError(SECRET)
        except RuntimeError:
            try:
                di.teardown(partial, registry, store)
            except di.DeviceIdentityError as error:
                captured.append(error)
        self.assertEqual(len(captured), 1)
        self.assertNotIn(SECRET, "".join(traceback.format_exception(captured[0])))

    def test_plan_inside_except_does_not_chain_caller_secret(self) -> None:
        captured: list[di.DeviceIdentityError] = []
        try:
            raise RuntimeError(SECRET)
        except RuntimeError:
            try:
                di.plan("X", "owner-role", sensors())
            except di.DeviceIdentityError as error:
                captured.append(error)
        self.assertEqual(len(captured), 1)
        self.assertEqual(str(captured[0]), "INVALID_MANIFEST")
        self.assertNotIn(SECRET, "".join(traceback.format_exception(captured[0])))

    def test_credential_issued_during_cleanup_is_reported(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        done = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        original = store.revoke

        def revoke_and_reissue(reference: str) -> None:
            original(reference)
            store.issue("SYN-LATE", "run-001")

        store.revoke = revoke_and_reissue  # type: ignore[method-assign]
        with self.assertRaises(di.DeviceIdentityError) as ctx:
            di.teardown(done, registry, store)
        self.assertEqual(str(ctx.exception), "TEARDOWN_CREDENTIALS_REMAIN")

    def test_device_added_during_revocation_is_reported(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        done = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        original = store.revoke

        def revoke_and_add_device(reference: str) -> None:
            original(reference)
            registry.devices["SYN-LATE"] = "run-001"

        store.revoke = revoke_and_add_device  # type: ignore[method-assign]
        with self.assertRaises(di.DeviceIdentityError) as ctx:
            di.teardown(done, registry, store)
        self.assertEqual(str(ctx.exception), "TEARDOWN_INCOMPLETE:1")

    def test_provision_inside_except_does_not_chain_caller_secret(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        manifest = di.plan("run-001", "owner-role", sensors())
        di.provision(manifest, registry, store)
        invalid = di.Manifest("run-001", "owner-role", ())
        for target in (manifest, invalid):
            captured: list[di.DeviceIdentityError] = []
            try:
                raise RuntimeError(SECRET)
            except RuntimeError:
                try:
                    di.provision(target, registry, store)
                except di.DeviceIdentityError as error:
                    captured.append(error)
            self.assertEqual(len(captured), 1)
            self.assertNotIn(SECRET, "".join(traceback.format_exception(captured[0])))

    def test_explicit_foreign_reference_is_not_revoked(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        one = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        registry.devices["SYN-OTHER"] = "run-002"
        foreign = store.issue("SYN-OTHER", "run-002")
        di.teardown(one, registry, store, refs=[foreign])
        self.assertEqual(store.run_references("run-002"), [foreign])
        self.assertEqual(registry.list_run("run-002"), ["SYN-OTHER"])

    def test_stale_manifest_cannot_delete_newer_run(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        stale = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        di.teardown(stale, registry, store)
        di.provision(di.plan("run-002", "owner-role", sensors()), registry, store)
        with self.assertRaisesRegex(di.DeviceIdentityError, "OWNERSHIP_MISMATCH"):
            di.teardown(stale, registry, store)
        self.assertEqual(len(registry.list_run("run-002")), 5)
        self.assertEqual(len([r for r in store.secrets]), 5)

    def test_teardown_errors_are_secret_free_and_cleanup_continues(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        done = di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        real_delete = registry.delete

        def boom(device_id: str, run_id: str) -> None:
            real_delete(device_id, run_id)
            raise RuntimeError(SECRET)

        registry.delete = boom  # type: ignore[method-assign]
        with self.assertRaises(di.DeviceIdentityError) as ctx:
            di.teardown(done, registry, store)
        text = "".join(traceback.format_exception(ctx.exception))
        self.assertNotIn(SECRET, text)
        self.assertEqual([r for r in store.secrets], [])

    def test_rollback_cleanup_failure_does_not_chain_secret(self) -> None:
        registry, store = FakeRegistry(fail_after=3), FakeStore()

        def boom(reference: str) -> None:
            raise RuntimeError(SECRET)

        store.revoke = boom  # type: ignore[method-assign]
        with self.assertRaises(di.DeviceIdentityError) as ctx:
            di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)
        self.assertNotIn(SECRET, "".join(traceback.format_exception(ctx.exception)))

    def test_incomplete_credential_cleanup_is_reported_for_rollback_refs(self) -> None:
        registry, store = FakeRegistry(fail_after=3), FakeStore()
        store.revoke = lambda reference: None  # type: ignore[method-assign]
        with self.assertRaisesRegex(di.DeviceIdentityError, "CREDENTIALS_REMAIN"):
            di.provision(di.plan("run-001", "owner-role", sensors()), registry, store)


if __name__ == "__main__":
    unittest.main()
