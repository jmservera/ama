"""Durable SAS credential store: persistence, restart recovery, revocation and no leakage (#185)."""

import json
import logging
import unittest
from types import SimpleNamespace
from typing import Any

from zava_forward.core.synthetic import live_provisioning as lp


class FakeBackend:
    def __init__(self) -> None:
        self.secrets: dict[str, tuple[str, str, str]] = {}
        self.fail = False

    def put(self, reference: str, value: str, run_id: str, device_id: str) -> None:
        if self.fail:
            raise RuntimeError(f"vault down while storing {value}")
        self.secrets[reference] = (value, run_id, device_id)

    def delete(self, reference: str) -> None:
        if self.fail:
            raise RuntimeError("vault down")
        self.secrets.pop(reference, None)

    def list_entries(self) -> list[tuple[str, str, str]]:
        return [(ref, run, dev) for ref, (_, run, dev) in self.secrets.items()]


class FakeKeyVaultClient:
    def __init__(self) -> None:
        self.items: dict[str, tuple[str, dict[str, str]]] = {}

    def set_secret(self, name: str, value: str, tags: dict[str, str]) -> None:
        self.items[name] = (value, tags)

    def begin_delete_secret(self, name: str) -> Any:
        self.items.pop(name, None)
        return SimpleNamespace(wait=lambda: None)

    def list_properties_of_secrets(self) -> list[Any]:
        return [SimpleNamespace(name=n, tags=t) for n, (_, t) in self.items.items()]


class DurableStoreTests(unittest.TestCase):
    def test_provision_stores_keys_and_a_restarted_store_tears_down(self) -> None:
        backend = FakeBackend()
        registry = lp.SimulatedDeviceRegistry()
        manifest = lp.plan_simulated_provisioning(
            "run-185-durable", ("ZNH-HOME-001", "ZNH-HOME-003")
        )
        with self.assertLogs(lp.LOG.name, level=logging.INFO) as captured:
            summary = lp.provision_simulated_devices(
                manifest, registry, lp.DurableSasCredentialStore(backend)
            )
        self.assertEqual(len(backend.secrets), 2)
        keys = [value for value, _, _ in backend.secrets.values()]
        serialized = json.dumps({"s": summary.as_dict(), "logs": captured.output})
        for key in keys:
            self.assertNotIn(key, serialized)

        restarted = lp.DurableSasCredentialStore(backend)
        self.assertEqual(restarted.active_count(), 2)
        receipt = lp.teardown_simulated_identities(registry, restarted, manifest=summary.manifest)
        self.assertTrue(receipt.verified_zero_residual)
        self.assertEqual(backend.secrets, {})

    def test_restart_does_not_reuse_reference_numbers(self) -> None:
        backend = FakeBackend()
        first = lp.DurableSasCredentialStore(backend).issue("SIM-A", "run-185-seq")
        second = lp.DurableSasCredentialStore(backend).issue("SIM-A", "run-185-seq")
        self.assertNotEqual(first, second)

    def test_backend_failure_is_fixed_code_without_secret_and_leaves_nothing(self) -> None:
        backend = FakeBackend()
        store = lp.DurableSasCredentialStore(backend)
        backend.fail = True
        with self.assertRaises(lp.LiveProvisioningError) as ctx:
            store.issue("SIM-A", "run-185-fail")
        self.assertIn("CREDENTIAL_BACKEND_FAILED", str(ctx.exception))
        self.assertNotIn("vault down", str(ctx.exception))
        self.assertIsNone(ctx.exception.__cause__)
        self.assertEqual(store.active_count(), 0)

    def test_failed_revoke_keeps_the_reference_visible(self) -> None:
        backend = FakeBackend()
        store = lp.DurableSasCredentialStore(backend)
        reference = store.issue("SIM-A", "run-185-rev")
        backend.fail = True
        with self.assertRaises(lp.LiveProvisioningError):
            store.revoke(reference)
        self.assertTrue(store.has_reference(reference))
        backend.fail = False
        store.revoke(reference)
        self.assertEqual((store.active_count(), backend.secrets), (0, {}))

    def test_key_vault_backend_round_trip_with_tags_only_for_own_secrets(self) -> None:
        client = FakeKeyVaultClient()
        client.items["unrelated"] = ("x", {})
        backend = lp.KeyVaultSecretBackend(client)
        store = lp.DurableSasCredentialStore(backend)
        reference = store.issue("SIM-A", "run-185-kv")
        (name,) = [n for n in client.items if n.startswith("zfsas-")]
        self.assertNotIn("SIM-A", name)
        self.assertEqual(backend.list_entries(), ((reference, "run-185-kv", "SIM-A"),))
        store.revoke(reference)
        self.assertEqual(list(client.items), ["unrelated"])
        self.assertNotIn("zfsas", repr(backend))


if __name__ == "__main__":
    unittest.main()
