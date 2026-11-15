import ast
import dataclasses
import json
import logging
import tempfile
import traceback
import unittest
from pathlib import Path

from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import device_provision as dp
from zava_forward.core.synthetic import live_provisioning as lp
from zava_forward.core.synthetic import privacy

RAW_KEY_B64 = "K9mP2vX8qL4nR7tY1wZ5bC3dF6gH0jM8pQ2sV4xN6zA="
RAW_CONN_STR = (
    f"HostName=zava-sim-hub.azure-devices.net;DeviceId=SIM-TEST01;SharedAccessKey={RAW_KEY_B64}"
)
RAW_SAS_TOKEN = (
    "SharedAccessSignature "
    "sr=zava-sim-hub.azure-devices.net%2Fdevices%2FSIM-TEST01"
    "&sig=AbCdEfGhIjKlMnOpQrStUvWxYz0123456789%2B%2F%3D%3D&se=1999999999"
)
RAW_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7\n"
    "-----END PRIVATE KEY-----"
)
REGISTER_CSV = (
    "synthetic_home_id,building_form_osm,locality_theme,is_synthetic,monitoring_consent\n"
    "ZNH-HOME-001,terrace,Locality North,true,granted\n"
    "ZNH-HOME-002,semi,Locality North,true,declined\n"
    "ZNH-HOME-003,flat,Locality South,true,granted\n"
    "ZNH-HOME-004,detached,Locality East,true,unknown\n"
)


class LiveProvisioningTests(unittest.TestCase):
    def test_manifest_records_dps_symmetric_sas_approach_and_credential_owner(self) -> None:
        manifest = lp.plan_simulated_provisioning(
            "run-185-plan",
            ("ZNH-HOME-001", "ZNH-HOME-002", "ZNH-HOME-003"),
        )
        self.assertIs(lp.ProvisioningPlan, lp.ProvisioningManifest)
        self.assertIs(lp.TeardownReceipt, di.TeardownReceipt)
        self.assertEqual(
            manifest.approach,
            "per-device symmetric SAS / DPS enrollment group",
        )
        self.assertEqual(
            manifest.identity_approach,
            "per-device symmetric SAS / DPS enrollment group",
        )
        self.assertEqual(
            manifest.credential_owner,
            "Platform Engineering / IoT Operations Owner",
        )
        self.assertEqual(len(manifest.identities), 3)
        self.assertTrue(all(i.device_id.startswith("SIM-") for i in manifest.identities))
        self.assertEqual(
            len({i.device_id for i in manifest.identities}),
            len({i.home_id for i in manifest.identities}),
        )
        exported = manifest.as_dict()
        self.assertEqual(
            exported["approach"],
            "per-device symmetric SAS / DPS enrollment group",
        )
        self.assertEqual(
            exported["identity_approach"],
            "per-device symmetric SAS / DPS enrollment group",
        )
        self.assertEqual(
            exported["credential_owner"],
            "Platform Engineering / IoT Operations Owner",
        )
        self.assertEqual(exported["enrollment_mode"], "dps_enrollment_group")
        self.assertEqual(exported["credential_type"], "per_device_symmetric_sas")
        self.assertEqual(privacy.emission_issues(exported), [])

    def test_plan_simulated_register_selects_only_consenting_homes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            reg_path = Path(tmp) / "register.csv"
            reg_path.write_text(REGISTER_CSV, encoding="utf-8")
            manifest = lp.plan_simulated_register(reg_path, homes=4, run_id="run-185-reg")
            self.assertEqual(len(manifest.identities), 2)
            self.assertEqual(
                {i.home_id for i in manifest.identities},
                {"ZNH-HOME-001", "ZNH-HOME-003"},
            )
            self.assertTrue(all(i.device_id.startswith("SIM-") for i in manifest.identities))

            declined_only = Path(tmp) / "declined.csv"
            declined_only.write_text(
                "synthetic_home_id,building_form_osm,locality_theme,"
                "is_synthetic,monitoring_consent\n"
                "ZNH-HOME-002,semi,Locality North,true,declined\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(lp.LiveProvisioningError, "^NO_MONITORED_HOMES$"):
                lp.plan_simulated_register(declined_only, homes=1, run_id="run-185-empty")

    def test_manifest_refuses_unnamed_personal_secret_or_unsupported_approach(self) -> None:
        for bad_owner in ("", "   ", "TBD", "unassigned", "<owner>"):
            with self.assertRaisesRegex(lp.LiveProvisioningError, "^CREDENTIAL_OWNER_NOT_NAMED$"):
                lp.plan_simulated_provisioning(
                    "run-185-bad", ("ZNH-HOME-001",), credential_owner=bad_owner
                )
        with self.assertRaisesRegex(lp.LiveProvisioningError, "^CREDENTIAL_OWNER_PERSONAL_DATA$"):
            lp.plan_simulated_provisioning(
                "run-185-pii",
                ("ZNH-HOME-001",),
                credential_owner="iot-owner@zavanorth.example.org",
            )
        with self.assertRaisesRegex(lp.LiveProvisioningError, "^CREDENTIAL_OWNER_SECRET_MATERIAL$"):
            lp.plan_simulated_provisioning(
                "run-185-sec",
                ("ZNH-HOME-001",),
                credential_owner=f"Owner SharedAccessKey={RAW_KEY_B64}",
            )
        with self.assertRaisesRegex(
            lp.LiveProvisioningError, "^UNSUPPORTED_PROVISIONING_APPROACH$"
        ):
            lp.plan_simulated_provisioning(
                "run-185-app",
                ("ZNH-HOME-001",),
                approach="hardcoded-shared-hub-connection-string",
            )

    def test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens(
        self,
    ) -> None:
        synthetic_dir = Path(lp.__file__).resolve().parent
        for module_name in ("live_provisioning.py", "device_identity.py", "device_provision.py"):
            source = (synthetic_dir / module_name).read_text(encoding="utf-8")
            tree = ast.parse(source, filename=module_name)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    self.assertFalse(
                        lp.contains_raw_secret(node.value),
                        f"Unexpected secret-shaped string literal in {module_name}",
                    )

    def test_vault_issuance_and_rotation_hide_runtime_derived_keys_and_preserve_safe_uris(
        self,
    ) -> None:
        registry = lp.SimulatedDeviceRegistry()
        store = lp.SymmetricSasCredentialStore()
        audit_log: list[lp.ProvisioningAuditRecord] = []
        manifest = lp.plan_simulated_provisioning("run-185-vault", ("ZNH-HOME-001", "ZNH-HOME-003"))
        with self.assertLogs(lp.LOG.name, level=logging.INFO) as captured_logs:
            summary = lp.provision_simulated_devices(manifest, registry, store, audit_log=audit_log)
            active_keys = [entry.derived_key_b64 for entry in store._vault.values()]
            self.assertEqual(len(active_keys), 2)
            rotated = lp.rotate_simulated_credentials(
                summary.manifest, registry, store, audit_log=audit_log
            )
            rotated_keys = [entry.derived_key_b64 for entry in store._vault.values()]
            self.assertEqual(len(rotated_keys), 2)
            self.assertFalse(set(active_keys) & set(rotated_keys))

        serialized = json.dumps(
            {
                "store_repr": repr(store),
                "manifest_repr": repr(rotated.manifest),
                "summary": rotated.as_dict(),
                "audit": [a.as_dict() for a in audit_log],
                "logs": captured_logs.output,
            }
        )
        for runtime_secret in [*active_keys, *rotated_keys]:
            self.assertNotIn(runtime_secret, serialized)

        for safe_uri in (
            rotated.manifest.identities[0].credential_ref,
            "kv://zavasim/syn0123456789abcdef01/1",
        ):
            self.assertEqual(lp.redact_provisioning_secrets(safe_uri), safe_uri)

        receipt = lp.teardown_simulated_identities(
            registry, store, manifest=rotated.manifest, audit_log=audit_log
        )
        self.assertTrue(receipt.verified_zero_residual)
        self.assertEqual(store.active_count(), 0)
        self.assertEqual(store._vault, {})

    def test_outputs_and_audit_records_redact_keys_connection_strings_and_sas_tokens(
        self,
    ) -> None:
        registry = lp.SimulatedDeviceRegistry()
        store = lp.SymmetricSasCredentialStore()
        audit_log: list[lp.ProvisioningAuditRecord] = []
        manifest = lp.plan_simulated_provisioning("run-185-redact", ("ZNH-HOME-001",))
        noisy_note = (
            f"conn={RAW_CONN_STR} sas={RAW_SAS_TOKEN} "
            f"PrimaryKey={RAW_KEY_B64} standalone={RAW_KEY_B64} pem={RAW_PEM}"
        )
        summary = lp.provision_simulated_devices(
            manifest, registry, store, note=noisy_note, audit_log=audit_log
        )
        rotated = lp.rotate_simulated_credentials(
            summary.manifest, registry, store, note=noisy_note, audit_log=audit_log
        )
        receipt = lp.teardown_simulated_identities(
            registry, store, manifest=rotated.manifest, note=noisy_note, audit_log=audit_log
        )

        combined = json.dumps(
            {
                "summary": summary.as_dict(),
                "rotated": rotated.as_dict(),
                "receipt": receipt.as_dict(),
                "audit": [record.as_dict() for record in audit_log],
            }
        )
        for secret_fragment in (
            RAW_KEY_B64,
            "zava-sim-hub.azure-devices.net;DeviceId=SIM-TEST01;SharedAccessKey=",
            "SharedAccessSignature sr=",
            "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789",
            "BEGIN PRIVATE KEY",
        ):
            self.assertNotIn(secret_fragment, combined)
        self.assertIn(lp.REDACTED, combined)
        self.assertEqual(privacy.emission_issues(summary.as_dict()), [])
        self.assertEqual(privacy.emission_issues(audit_log[0].as_dict()), [])

    def test_logger_filter_redacts_percent_formatted_split_extra_and_exception_secrets(
        self,
    ) -> None:
        captured_records: list[logging.LogRecord] = []

        class CaptureHandler(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                captured_records.append(record)

        handler = CaptureHandler(level=logging.INFO)
        lp.LOG.addHandler(handler)
        try:
            with self.assertLogs(lp.LOG.name, level=logging.INFO) as logs:
                lp.LOG.error("Direct format SharedAccessKey=%s", RAW_KEY_B64)
                lp.LOG.warning("Split format %s=%s", "SharedAccessKey", RAW_KEY_B64)
                lp.LOG.info(
                    "Structured extras",
                    extra={"conn": RAW_CONN_STR, "sas_tuple": (RAW_SAS_TOKEN, "safe-tag")},
                )
                try:
                    raise RuntimeError(f"SDK failure {RAW_CONN_STR} {RAW_SAS_TOKEN}")
                except RuntimeError:
                    lp.LOG.exception("Exception log with %s", RAW_KEY_B64)
        finally:
            lp.LOG.removeHandler(handler)

        joined_logs = "\n".join(logs.output)
        for secret_fragment in (
            RAW_KEY_B64,
            "SharedAccessSignature sr=",
            "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789",
            "DeviceId=SIM-TEST01;SharedAccessKey=",
        ):
            self.assertNotIn(secret_fragment, joined_logs)
        for record in captured_records:
            record_dump = json.dumps(
                {
                    "msg": str(record.msg),
                    "exc_text": record.exc_text,
                    "conn": getattr(record, "conn", None),
                    "sas_tuple": getattr(record, "sas_tuple", None),
                }
            )
            self.assertNotIn(RAW_KEY_B64, record_dump)
            self.assertNotIn("SharedAccessSignature sr=", record_dump)
            self.assertIsNone(record.exc_info)

    def test_adapter_failure_rolls_back_atomically_and_suppresses_secret_traceback(
        self,
    ) -> None:
        registry = lp.SimulatedDeviceRegistry()
        store = lp.SymmetricSasCredentialStore()
        audit_log: list[lp.ProvisioningAuditRecord] = []
        manifest = lp.plan_simulated_provisioning(
            "run-185-fail", ("ZNH-HOME-001", "ZNH-HOME-002", "ZNH-HOME-003")
        )
        original_issue = store.issue
        calls = {"count": 0}

        def failing_issue(device_id: str, run_id: str) -> str:
            calls["count"] += 1
            if calls["count"] == 2:
                raise RuntimeError(f"Vault write error {RAW_CONN_STR}")
            return original_issue(device_id, run_id)

        store.issue = failing_issue  # type: ignore[method-assign]
        caught: list[lp.LiveProvisioningError] = []
        try:
            raise ValueError(f"Caller context {RAW_SAS_TOKEN}")
        except ValueError:
            try:
                lp.provision_simulated_devices(
                    manifest, registry, store, note=RAW_KEY_B64, audit_log=audit_log
                )
            except lp.LiveProvisioningError as err:
                caught.append(err)

        self.assertEqual(len(caught), 1)
        self.assertEqual(str(caught[0]), "PROVISION_FAILED_ROLLED_BACK")
        rendered_tb = "".join(traceback.format_exception(caught[0]))
        self.assertNotIn(RAW_KEY_B64, rendered_tb)
        self.assertNotIn("SharedAccessSignature", rendered_tb)
        self.assertEqual(registry.list_simulated(), ())
        self.assertEqual(store.active_count(), 0)
        self.assertEqual(len(audit_log), 1)
        self.assertEqual(audit_log[0].outcome, "rolled_back")
        self.assertNotIn(RAW_KEY_B64, json.dumps(audit_log[0].as_dict()))

    def test_teardown_simulated_identities_removes_run_and_returns_verifiable_receipt(
        self,
    ) -> None:
        registry = lp.SimulatedDeviceRegistry()
        registry.seed_non_simulated("PROD-BOILER-01", owner_tag="prod-fleet")
        store = lp.SymmetricSasCredentialStore()

        run_a = lp.provision_simulated_devices(
            lp.plan_simulated_provisioning("run-185-a", ("ZNH-HOME-001", "ZNH-HOME-002")),
            registry,
            store,
        )
        run_b = lp.provision_simulated_devices(
            lp.plan_simulated_provisioning("run-185-b", ("ZNH-HOME-003",)),
            registry,
            store,
        )

        receipt = lp.teardown_simulated_identities(registry, store, manifest=run_a.manifest)
        self.assertTrue(receipt.verified_zero_residual)
        self.assertEqual(receipt.removed_count, 2)
        self.assertEqual(receipt.revoked_credential_count, 2)
        self.assertEqual(receipt.residual_simulated_count, 0)
        self.assertEqual(receipt.residual_simulated_identities, ())
        self.assertEqual(receipt.residual_credential_count, 0)
        self.assertEqual(receipt.approach, lp.DEVICE_IDENTITY_APPROACH)
        self.assertEqual(receipt.credential_owner, lp.CREDENTIAL_OWNER_ROLE)
        self.assertTrue(receipt.verify())
        self.assertFalse(dataclasses.replace(receipt, removed_count=99).verify())
        self.assertEqual(privacy.emission_issues(receipt.as_dict()), [])

        self.assertEqual(registry.list_simulated("run-185-a"), ())
        self.assertEqual(len(registry.list_simulated("run-185-b")), 1)
        self.assertEqual(registry.run_of("PROD-BOILER-01"), "prod-fleet")
        self.assertEqual(len(store.run_references(run_b.manifest.run_id)), 1)

    def test_deprovision_simulated_devices_sweeps_all_runs_preserving_non_simulated(
        self,
    ) -> None:
        self.assertIs(dp.deprovision_simulated_devices, lp.deprovision_simulated_devices)
        self.assertIs(dp.teardown_simulated_identities, lp.teardown_simulated_identities)
        registry = lp.SimulatedDeviceRegistry(
            {"PROD-HUB-01": "production", "REAL-GW-02": "field-trial"}
        )
        store = lp.SymmetricSasCredentialStore()
        lp.provision_simulated_devices(
            lp.plan_simulated_provisioning("run-185-s1", ("ZNH-HOME-001", "ZNH-HOME-002")),
            registry,
            store,
        )
        lp.provision_simulated_devices(
            lp.plan_simulated_provisioning("run-185-s2", ("ZNH-HOME-003",)),
            registry,
            store,
        )
        self.assertEqual(len(registry.list_simulated()), 3)

        receipt = lp.deprovision_simulated_devices(registry, store)
        self.assertIsNone(receipt.run_id)
        self.assertTrue(receipt.verified_zero_residual)
        self.assertEqual(receipt.removed_count, 3)
        self.assertEqual(receipt.revoked_credential_count, 3)
        self.assertEqual(receipt.residual_simulated_count, 0)
        self.assertEqual(receipt.residual_simulated_identities, ())
        self.assertTrue(receipt.verify())
        self.assertEqual(registry.list_simulated(), ())
        self.assertEqual(store.active_count(), 0)
        self.assertEqual(
            registry.list_all(),
            {"PROD-HUB-01": "production", "REAL-GW-02": "field-trial"},
        )

    def test_teardown_fails_closed_when_residual_simulated_identity_or_credential_remains(
        self,
    ) -> None:
        registry = lp.SimulatedDeviceRegistry()
        store = lp.SymmetricSasCredentialStore()
        summary = lp.provision_simulated_devices(
            lp.plan_simulated_provisioning("run-185-stuck", ("ZNH-HOME-001",)),
            registry,
            store,
        )
        audit_log: list[lp.ProvisioningAuditRecord] = []
        original_delete = registry.delete
        registry.delete = lambda device_id, run_id: None  # type: ignore[method-assign]
        with self.assertRaisesRegex(
            lp.LiveProvisioningError, "^TEARDOWN_RESIDUAL_SIMULATED_IDENTITIES:1$"
        ):
            lp.teardown_simulated_identities(
                registry, store, manifest=summary.manifest, audit_log=audit_log
            )
        self.assertEqual(audit_log[-1].outcome, "failed")

        registry.delete = original_delete  # type: ignore[method-assign]
        registry_two = lp.SimulatedDeviceRegistry()
        store_two = lp.SymmetricSasCredentialStore()
        summary_two = lp.provision_simulated_devices(
            lp.plan_simulated_provisioning("run-185-cred", ("ZNH-HOME-002",)),
            registry_two,
            store_two,
        )
        store_two.revoke = lambda reference: None  # type: ignore[method-assign]
        with self.assertRaisesRegex(lp.LiveProvisioningError, "^TEARDOWN_CREDENTIALS_REMAIN$"):
            lp.teardown_simulated_identities(
                registry_two, store_two, manifest=summary_two.manifest, audit_log=audit_log
            )

    def test_idempotent_reteardown_confirms_zero_residual_without_error(self) -> None:
        registry = lp.SimulatedDeviceRegistry()
        store = lp.SymmetricSasCredentialStore()
        summary = lp.provision_simulated_devices(
            lp.plan_simulated_provisioning("run-185-idem", ("ZNH-HOME-001",)),
            registry,
            store,
        )
        first = lp.teardown_simulated_identities(registry, store, manifest=summary.manifest)
        second = lp.teardown_simulated_identities(registry, store, manifest=summary.manifest)
        self.assertEqual(first.removed_count, 1)
        self.assertEqual(second.removed_count, 0)
        self.assertTrue(second.verified_zero_residual)
        self.assertEqual(second.residual_simulated_count, 0)
        self.assertTrue(second.verify())


if __name__ == "__main__":
    unittest.main()
