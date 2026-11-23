import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from test_device_identity import FakeRegistry, FakeStore, sensors
from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import device_provision as dp
from zava_forward.core.synthetic import live_provisioning as lp

REGISTER = (
    "synthetic_home_id,building_form_osm,locality_theme,is_synthetic,monitoring_consent\n"
    "home-a,terrace,Locality A,true,granted\n"
    "home-b,terrace,Locality A,true,declined\n"
    "home-c,terrace,Locality A,true,granted\n"
)


def manifest(owner: str = "Named Owner") -> di.Manifest:
    return di.plan("run-185", owner, sensors(3))


class DeviceProvisionTests(unittest.TestCase):
    def cli(self, *extra: str) -> tuple[int, str, str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register.csv"
            path.write_text(REGISTER, encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = dp.main(["--register", str(path), "--run-id", "run-185", *extra])
        return code, out.getvalue(), err.getvalue()

    def test_default_is_dry_run_and_skips_declined_homes(self) -> None:
        code, out, _ = self.cli("--homes", "3", "--owner", "Named Owner")
        body = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(body["mode"], "dry-run")
        self.assertEqual(body["device_count"], 2)
        for device in body["devices"]:
            self.assertTrue(device["device_id"].startswith("SYN-"))
        self.assertEqual({d["home_id"] for d in body["devices"]}, {"home-a", "home-c"})
        self.assertIn("none created", body["credentials"])
        self.assertIn("dry run", body["credentials"])

    def test_apply_refused_without_adapters_or_owner(self) -> None:
        code, out, err = self.cli("--homes", "3", "--owner", "Named Owner", "--apply")
        self.assertEqual((code, out), (2, ""))
        self.assertIn("LIVE_ADAPTERS_NOT_CONFIGURED", err)
        code, _, err = self.cli("--homes", "3", "--apply")
        self.assertEqual(code, 2)
        self.assertIn("CREDENTIAL_OWNER_NOT_NAMED", err)

    def test_cycle_leaves_no_identity_and_prints_no_credential(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        body = dp.run(manifest(), "cycle", True, registry, store)
        receipt = body["teardown_receipt"]
        assert isinstance(receipt, dict)
        self.assertEqual(receipt["removed_count"], 3)
        self.assertTrue(receipt["verified_zero_residual"])
        self.assertEqual(list(registry.list_run("run-185")), [])
        self.assertEqual(list(store.run_references("run-185")), [])
        self.assertIn("none remain", str(body["credentials"]))

    def test_hub_host_cycle_uses_hub_adapters_and_reports_residual(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        closed: list[bool] = []

        def adapters(m: di.Manifest, host: str) -> tuple[FakeRegistry, FakeStore, object]:
            self.assertEqual(host, "hub-demo.azure-devices.net")
            return registry, store, lambda: closed.append(True)

        original = dp.hub_adapters
        dp.hub_adapters = adapters  # type: ignore[assignment]
        try:
            code, out, _ = self.cli(
                "--homes", "3", "--owner", "Named Owner", "--action", "cycle", "--apply",
                "--hub-host", "hub-demo.azure-devices.net",
            )  # fmt: skip
        finally:
            dp.hub_adapters = original
        body = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(body["residual_in_hub"], 0)
        self.assertEqual(body["device_count"], 2)
        self.assertEqual(closed, [True])

    def test_vault_url_selects_durable_store_and_report_has_no_key(self) -> None:
        registry = FakeRegistry()
        seen: list[tuple[str, str | None]] = []

        def adapters(
            m: di.Manifest, host: str, vault: str | None = None
        ) -> tuple[FakeRegistry, FakeStore, object]:
            seen.append((host, vault))
            return registry, FakeStore(), lambda: None

        original = dp.hub_adapters
        dp.hub_adapters = adapters  # type: ignore[assignment]
        try:
            code, out, _ = self.cli(
                "--homes", "3", "--owner", "Named Owner", "--action", "cycle", "--apply",
                "--hub-host", "hub-demo.azure-devices.net",
                "--vault-url", "https://kv-demo.vault.azure.net",
            )  # fmt: skip
        finally:
            dp.hub_adapters = original
        self.assertEqual(code, 0)
        self.assertEqual(seen, [("hub-demo.azure-devices.net", "https://kv-demo.vault.azure.net")])
        self.assertEqual(json.loads(out)["residual_in_hub"], 0)

    def test_vault_url_needs_hub_and_must_be_a_key_vault_url(self) -> None:
        code, _, err = self.cli(
            "--homes", "3", "--owner", "Named Owner",
            "--vault-url", "https://kv-demo.vault.azure.net",
        )  # fmt: skip
        self.assertEqual((code, err.strip()), (2, "refused: VAULT_REQUIRES_HUB"))
        with self.assertRaises(dp.ProvisionError) as ctx:
            dp.hub_adapters(manifest(), "hub-demo.azure-devices.net", "https://evil.example/kv")
        self.assertEqual(str(ctx.exception), "INVALID_VAULT_URL")

    def test_vault_backend_failure_is_a_fixed_code_refusal(self) -> None:
        def adapters(m: di.Manifest, host: str, vault: str | None = None) -> object:
            raise lp.LiveProvisioningError("CREDENTIAL_BACKEND_FAILED")

        original = dp.hub_adapters
        dp.hub_adapters = adapters  # type: ignore[assignment]
        try:
            code, _, err = self.cli(
                "--homes", "3", "--owner", "Named Owner", "--apply",
                "--hub-host", "hub-demo.azure-devices.net",
                "--vault-url", "https://kv-demo.vault.azure.net",
            )  # fmt: skip
        finally:
            dp.hub_adapters = original
        self.assertEqual((code, err.strip()), (2, "refused: CREDENTIAL_BACKEND_FAILED"))

    def test_hub_host_rejects_invalid_host_without_detail(self) -> None:
        code, _, err = self.cli(
            "--homes", "3", "--owner", "Named Owner", "--apply", "--hub-host", "bad host"
        )
        self.assertEqual(code, 2)
        self.assertNotIn("bad host", err)

    def test_invalid_input_is_refused_without_detail(self) -> None:
        code, _, err = self.cli("--homes", "9")
        self.assertEqual(code, 2)
        self.assertEqual(err.strip(), "refused: INVALID_INPUT")

    def test_dry_run_touches_no_adapter(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        body = dp.run(manifest(), "teardown", False, registry, store)
        self.assertEqual(body["mode"], "dry-run")
        self.assertEqual(registry.devices, {"SYN-OTHER": "other-run"})
        self.assertEqual(store.references(), [])

    def test_applied_run_with_fakes_provisions_then_tears_down(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        body = dp.run(manifest(), "provision", True, registry, store)
        self.assertEqual(body["mode"], "applied")
        self.assertEqual(len(store.references()), 3)
        self.assertNotIn("PRIVATE-KEY-MATERIAL", json.dumps(body))
        issued = di.Manifest(
            "run-185",
            "Named Owner",
            tuple(
                di.DeviceIdentity(i.device_id, i.sensor_id, i.home_id, ref)
                for i, ref in zip(manifest().identities, store.references(), strict=True)
            ),
        )
        dp.run(issued, "teardown", True, registry, store)
        self.assertEqual(store.references(), [])
        self.assertEqual(registry.list_run("run-185"), [])

    def test_applied_provision_report_says_credentials_stored(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        body = dp.run(manifest(), "provision", True, registry, store)
        self.assertEqual(len(store.references()), 3)
        text = str(body["credentials"])
        self.assertIn("stored", text)
        self.assertNotIn("none created", text)
        self.assertNotIn("PRIVATE-KEY-MATERIAL", json.dumps(body))

    def test_applied_teardown_with_original_manifest_reports_revoked(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        original = manifest()
        dp.run(original, "provision", True, registry, store)
        body = dp.run(original, "teardown", True, registry, store)
        self.assertEqual(store.references(), [])
        self.assertEqual(registry.list_run("run-185"), [])
        text = str(body["credentials"])
        self.assertIn("revoked", text)
        self.assertNotIn("none created", text)

    def test_dry_run_with_adapters_writes_nothing_and_says_so(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        for action in dp.ACTIONS:
            body = dp.run(manifest(), action, False, registry, store)
            self.assertIn("dry run", str(body["credentials"]))
        self.assertEqual(store.references(), [])
        self.assertEqual(registry.devices, {"SYN-OTHER": "other-run"})

    def test_placeholder_owners_are_not_named(self) -> None:
        for owner in ("", " ", "TBD", "unassigned", "<owner>"):
            self.assertFalse(dp.owner_named(owner), owner)
        self.assertTrue(dp.owner_named("Named Owner"))

    def test_report_and_teardown_include_approach_and_zero_residual_receipt(self) -> None:
        registry, store = FakeRegistry(), FakeStore()
        target = di.plan("run-185", dp.CREDENTIAL_OWNER_ROLE, sensors(2))
        provisioned = dp.run(target, "provision", True, registry, store)
        self.assertEqual(provisioned["approach"], dp.DEVICE_IDENTITY_APPROACH)
        self.assertEqual(provisioned["credential_owner"], dp.CREDENTIAL_OWNER_ROLE)
        torn_down = dp.run(target, "teardown", True, registry, store)
        self.assertEqual(torn_down["approach"], dp.DEVICE_IDENTITY_APPROACH)
        receipt = torn_down["teardown_receipt"]
        assert isinstance(receipt, dict)
        self.assertIs(receipt["verified_zero_residual"], True)
        self.assertEqual(receipt["residual_simulated_count"], 0)
        self.assertEqual(receipt["removed_count"], 2)

    def test_report_refuses_secret_bearing_credential_owner(self) -> None:
        raw_key = "".join(("K9mP2vX8qL4nR7tY1wZ5bC", "3dF6gH0jM8pQ2sV4xN6zA="))
        owner_with_secret = "".join(("Owner SharedAccess", "Key=", raw_key))
        secret_manifest = di.plan("run-185", owner_with_secret, sensors(1))
        with self.assertRaisesRegex(dp.ProvisionError, "^CREDENTIAL_OWNER_SECRET_MATERIAL$"):
            dp.report(secret_manifest, "provision", "dry-run")

    def test_invalid_action_is_refused(self) -> None:
        with self.assertRaises(dp.ProvisionError):
            dp.run(manifest(), "delete-all", False)


if __name__ == "__main__":
    unittest.main()
