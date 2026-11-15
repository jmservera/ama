"""Secret inventory, expiry/rotation checks, access review, CLI ledger and Bicep wiring."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "secret_lifecycle", ROOT / "scripts" / "secret_lifecycle.py"
)
assert SPEC is not None and SPEC.loader is not None
LIFE: Any = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LIFE)
NOW = LIFE.parse_time("2026-10-15T00:00:00Z")
INVENTORY: dict[str, Any] = json.loads((ROOT / "secret-inventory.json").read_text(encoding="utf-8"))
ROLE_MATRIX: dict[str, Any] = json.loads(
    (ROOT / "role-assignments.json").read_text(encoding="utf-8")
)


class InventoryTests(unittest.TestCase):
    def test_inventory_complete_and_covers_container_apps_secrets(self) -> None:
        self.assertEqual(LIFE.validate_inventory(INVENTORY), [])
        names = {entry["name"] for entry in INVENTORY["secrets"]}
        apps = (ROOT / "modules" / "containerapps.bicep").read_text(encoding="utf-8")
        for name in names - {"resident-demo-password-verifier", "resident-demo-session-key"}:
            if name == "entra-client-secret":
                self.assertIn("param entraClientSecretName string = 'entra-client-secret'", apps)
                self.assertIn(
                    "name: entraClientSecretName, keyVaultUrl: "
                    "'${keyVaultUri}/secrets/${entraClientSecretName}'",
                    apps,
                )
            else:
                self.assertIn(f"/secrets/{name}'", apps)

    def test_inventory_covers_every_vault_secret_and_names_owners(self) -> None:
        names = {entry["name"] for entry in INVENTORY["secrets"]}
        resident = (ROOT / "resident-demo.bicep").read_text(encoding="utf-8")
        for var in ("verifierSecret", "sessionSecret"):
            declared = re.search(rf"var {var} = '([^']+)'", resident)
            self.assertIsNotNone(declared)
            assert declared is not None
            self.assertIn(declared.group(1), names)
        for entry in INVENTORY["secrets"]:
            self.assertNotIn("open item", entry["owner"])
            self.assertNotIn("Platform operator (named", entry["owner"])

    def test_missing_owner_is_reported(self) -> None:
        bad = {"secrets": [{"name": "x", "rotationIntervalDays": 1, "expiryAlertDays": 1}]}
        self.assertEqual(LIFE.validate_inventory(bad), ["x: missing owner"])


class CheckTests(unittest.TestCase):
    def secret(
        self, name: str, expires: str | None, updated: str = "2026-10-01T00:00:00Z"
    ) -> dict[str, Any]:
        return {
            "name": name,
            "attributes": {"enabled": True, "expires": expires, "updated": updated},
        }

    def kinds(self, listed: list[dict[str, Any]]) -> set[tuple[str, str]]:
        return {(n, k) for n, k, _ in LIFE.check_secrets(INVENTORY, listed, NOW)}

    def test_healthy_secrets_have_no_findings(self) -> None:
        listed = [
            self.secret("entra-client-secret", "2027-04-01T00:00:00Z"),
            self.secret("entra-token-store-sas", "2026-10-30T00:00:00Z", "2026-10-14T12:00:00Z"),
            self.secret(
                "resident-demo-password-verifier",
                "2026-11-30T00:00:00Z",
                "2026-10-10T00:00:00Z",
            ),
            self.secret(
                "resident-demo-session-key", "2026-11-30T00:00:00Z", "2026-10-10T00:00:00Z"
            ),
        ]
        self.assertEqual(self.kinds(listed), set())

    def test_expiring_expired_overdue_and_missing(self) -> None:
        listed = [
            self.secret("entra-client-secret", "2026-10-30T00:00:00Z", "2026-01-01T00:00:00Z")
        ]
        kinds = self.kinds(listed)
        self.assertIn(("entra-client-secret", "expiring"), kinds)
        self.assertIn(("entra-client-secret", "rotation-overdue"), kinds)
        self.assertIn(("entra-token-store-sas", "missing"), kinds)
        expired = self.kinds([self.secret("entra-client-secret", "2026-10-01T00:00:00Z")])
        self.assertIn(("entra-client-secret", "expired"), expired)

    def test_no_expiry_is_a_finding(self) -> None:
        self.assertIn(
            ("entra-client-secret", "no-expiry"),
            self.kinds([self.secret("entra-client-secret", None)]),
        )


class ReviewAndRotationTests(unittest.TestCase):
    def test_review_record_is_pending_and_dated(self) -> None:
        record = LIFE.access_review(
            INVENTORY,
            [
                {
                    "principalId": "p1",
                    "principalType": "ServicePrincipal",
                    "roleDefinitionName": "Key Vault Secrets User",
                    "scope": "/v",
                },
                {
                    "principalId": "p2",
                    "principalType": "User",
                    "roleDefinitionName": "Contributor",
                    "scope": "/v",
                },
            ],
            "Reviewer",
            NOW,
        )
        self.assertEqual(record["nextReviewDue"], "2027-01-13")
        self.assertEqual([r["decision"] for r in record["assignments"]], ["pending", "pending"])
        self.assertTrue(record["assignments"][1]["access"].startswith("unclassified"))

    def test_rotation_deletes_old_credential_only_after_verification(self) -> None:
        plan = LIFE.rotation_plan("kv", "app")
        text = "\n".join(plan)
        self.assertIn("--append", plan[0])
        self.assertLess(text.index("confirm /app"), text.index("credential delete"))


class NoDowntimeRotationTests(unittest.TestCase):
    def test_documented_order_never_loses_sign_in(self) -> None:
        timeline = LIFE.rotation_timeline(LIFE.SAFE_ORDER)
        self.assertTrue(all(row["signInOk"] for row in timeline))
        self.assertEqual(timeline[-1]["valid"], ["new"])
        self.assertEqual(timeline[-1]["presented"], "new")

    def test_plan_matches_modelled_order(self) -> None:
        text = "\n".join(LIFE.rotation_plan("kv", "app"))
        positions = [
            text.index(k)
            for k in (
                "--append",
                "new version of entra-client-secret",
                "refresh",
                "confirm /app",
                "credential delete",
            )
        ]
        self.assertEqual(positions, sorted(positions))

    def test_deleting_old_credential_first_causes_outage(self) -> None:
        timeline = LIFE.rotation_timeline(("delete_old", "append", "store", "refresh"))
        self.assertFalse(timeline[0]["signInOk"])

    def test_deleting_before_app_refresh_causes_outage(self) -> None:
        timeline = LIFE.rotation_timeline(("append", "store", "delete_old", "refresh"))
        self.assertFalse(timeline[2]["signInOk"])

    def test_cli_simulation_succeeds(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = LIFE.main(["rotation-simulate"])
        self.assertEqual(rc, 0)


class ReviewStatusTests(unittest.TestCase):
    def record(
        self,
        decision: str = "keep",
        due: str = "2027-01-13",
        reviewer: str = "Reviewer",
    ) -> dict[str, Any]:
        return {
            "reviewer": reviewer,
            "nextReviewDue": due,
            "assignments": [{"principalId": "p1", "decision": decision}],
        }

    def test_complete_current_record_passes(self) -> None:
        self.assertEqual(LIFE.review_status(self.record(), NOW), [])

    def test_pending_decision_fails(self) -> None:
        self.assertTrue(LIFE.review_status(self.record("pending"), NOW))

    def test_overdue_and_unsigned_fail(self) -> None:
        problems = LIFE.review_status(self.record(due="2026-10-01", reviewer=""), NOW)
        self.assertEqual(len(problems), 2)

    def test_whitespace_reviewer_fails(self) -> None:
        problems = LIFE.review_status(self.record(reviewer="   "), NOW)
        self.assertEqual(problems, ["no reviewer recorded"])

    def test_generated_record_is_not_complete_until_decided(self) -> None:
        record = LIFE.access_review(
            INVENTORY,
            [{"principalId": "p1", "roleDefinitionName": "Key Vault Secrets User"}],
            "R",
            NOW,
        )
        self.assertTrue(LIFE.review_status(record, NOW))
        record["assignments"][0]["decision"] = "keep"
        self.assertEqual(LIFE.review_status(record, NOW), [])


class BicepWiringTests(unittest.TestCase):
    def test_diagnostics_and_alerts(self) -> None:
        kv = (ROOT / "modules" / "keyvault.bicep").read_text(encoding="utf-8")
        self.assertIn("categoryGroup: 'allLogs'", kv)
        self.assertIn("workspaceId: workspaceId", kv)
        self.assertIn("SecretNearExpiryEventGridNotification", kv)
        self.assertIn("SecretExpiredEventGridNotification", kv)
        main = (ROOT / "main.bicep").read_text(encoding="utf-8")
        self.assertIn("actionGroupId: monitoring.outputs.actionGroupId", main)


class StagedRotationAndLedgerCliTests(unittest.TestCase):
    def _run_cli(self, argv: list[str]) -> tuple[int, str, str]:
        out = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = int(LIFE.main(argv))
        return rc, out.getvalue(), err.getvalue()

    def _rotation_payload(self, *, switched: bool = True) -> dict[str, Any]:
        prior_ver = "11111111111111111111111111111111"
        next_ver = "22222222222222222222222222222222"
        id_arm = (
            "/subscriptions/00000000-0000-0000-0000-000000000001/resourceGroups/ama"
            "/providers/Microsoft.ManagedIdentity/userAssignedIdentities/id-api"
        )
        return {
            "stage": "post_switchover",
            "vaultName": "kv-ama-demo",
            "secretName": "entra-client-secret",
            "appId": "00000000-1111-2222-3333-444444444444",
            "expectedIdentityId": id_arm,
            "browserMode": True,
            "credentials": {
                "priorKeyId": "cred-old",
                "nextKeyId": "cred-new",
                "entries": [
                    {
                        "keyId": "cred-old",
                        "startDateTime": "2026-06-01T00:00:00Z",
                        "endDateTime": "2026-12-01T00:00:00Z",
                    },
                    {
                        "keyId": "cred-new",
                        "startDateTime": "2026-10-15T00:00:00Z",
                        "endDateTime": "2027-04-15T00:00:00Z",
                    },
                ],
            },
            "secretVersions": {
                "priorVersionId": prior_ver,
                "nextVersionId": next_ver,
                "entries": [
                    {
                        "id": (
                            "https://kv-ama-demo.vault.azure.net/secrets/"
                            f"entra-client-secret/{prior_ver}"
                        ),
                        "enabled": True,
                        "created": "2026-06-01T00:00:00Z",
                        "expires": "2026-12-01T00:00:00Z",
                    },
                    {
                        "id": (
                            "https://kv-ama-demo.vault.azure.net/secrets/"
                            f"entra-client-secret/{next_ver}"
                        ),
                        "enabled": True,
                        "created": "2026-10-15T00:05:00Z",
                        "expires": "2027-04-15T00:00:00Z",
                    },
                ],
            },
            "containerApp": {
                "clientSecretSettingName": "entra-client-secret",
                "switchoverAt": "2026-10-15T01:30:00Z",
                "secrets": [
                    {
                        "name": "entra-client-secret",
                        "identity": id_arm,
                        "keyVaultUrl": (
                            "https://kv-ama-demo.vault.azure.net/secrets/entra-client-secret"
                        ),
                    }
                ],
                "revisions": [
                    {
                        "name": "ca-api--0002",
                        "active": True,
                        "trafficWeight": 100,
                        "runningState": "Running",
                        "replicasReady": 1,
                        "secretVersionId": next_ver if switched else prior_ver,
                        "secretName": "entra-client-secret",
                    }
                ],
            },
            "healthProbes": [
                {
                    "stage": "dual_secret_overlap",
                    "totalSamples": 5,
                    "errorCount": 0,
                    "firstSampleAt": "2026-10-15T01:00:00Z",
                    "lastSampleAt": "2026-10-15T01:02:00Z",
                    "maxGapSeconds": 30,
                    "healthzStatus": 200,
                    "anonymousApiStatus": 401,
                    "signInRedirectStatus": 302,
                },
                {
                    "stage": "post_switchover",
                    "totalSamples": 5,
                    "errorCount": 0,
                    "firstSampleAt": "2026-10-15T02:00:00Z",
                    "lastSampleAt": "2026-10-15T02:02:00Z",
                    "maxGapSeconds": 30,
                    "healthzStatus": 200,
                    "anonymousApiStatus": 401,
                    "signInRedirectStatus": 302,
                    "authenticatedApiStatus": 200,
                    "freshTokenExchangeVerified": True,
                },
            ],
        }

    def test_role_matrix_aligns_with_default_expected_caller_policy(self) -> None:
        principal_map = {
            "api": "10000000-0000-4000-8000-000000000001",
            "token-maintenance": "10000000-0000-4000-8000-000000000002",
            "agents": "10000000-0000-4000-8000-000000000003",
            "orchestrator": "10000000-0000-4000-8000-000000000004",
            "import": "10000000-0000-4000-8000-000000000005",
        }
        policy = LIFE.default_expected_caller_policy(ROLE_MATRIX, principal_map)
        self.assertEqual(policy[principal_map["api"]]["allowedOperations"], ["SecretGet"])
        self.assertEqual(
            policy[principal_map["token-maintenance"]]["allowedOperations"],
            ["SecretGet", "SecretSet"],
        )
        for forbidden_name in ("agents", "orchestrator", "import"):
            self.assertTrue(policy[principal_map[forbidden_name]]["forbidden"])

    def test_rotation_verify_cli_passes_fails_and_refuses_secret_leak(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            ev_ok = tmp_dir / "ev-ok.json"
            receipt_out = tmp_dir / "receipt.json"
            ev_ok.write_text(json.dumps(self._rotation_payload(switched=True)), encoding="utf-8")
            rc, out, err = self._run_cli(
                [
                    "rotation-verify",
                    "--evidence",
                    str(ev_ok),
                    "--now",
                    "2026-10-16T00:00:00Z",
                    "--out",
                    str(receipt_out),
                ]
            )
            self.assertEqual(rc, 0, err)
            receipt = json.loads(receipt_out.read_text(encoding="utf-8"))
            self.assertTrue(receipt["safeToRetirePriorCredential"])
            self.assertEqual(json.loads(out)["evidenceDigest"], receipt["evidenceDigest"])

            ev_unswitched = tmp_dir / "ev-bad.json"
            ev_unswitched.write_text(
                json.dumps(self._rotation_payload(switched=False)), encoding="utf-8"
            )
            rc_bad, out_bad, _ = self._run_cli(
                [
                    "rotation-verify",
                    "--evidence",
                    str(ev_unswitched),
                    "--now",
                    "2026-10-16T00:00:00Z",
                ]
            )
            self.assertEqual(rc_bad, 1)
            self.assertFalse(json.loads(out_bad)["safeToRetirePriorCredential"])

            ev_leak = self._rotation_payload(switched=True)
            ev_leak["value"] = "CANARY_SECRET_CLI_999"
            ev_leak_path = tmp_dir / "ev-leak.json"
            ev_leak_path.write_text(json.dumps(ev_leak), encoding="utf-8")
            rc_leak, out_leak, err_leak = self._run_cli(
                ["rotation-verify", "--evidence", str(ev_leak_path)]
            )
            self.assertEqual(rc_leak, 2)
            self.assertNotIn("CANARY_SECRET_CLI_999", out_leak + err_leak)

    def test_access_audit_review_sign_and_ledger_verify_cli_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            oid_api = "20000000-0000-4000-8000-000000000001"
            oid_token = "20000000-0000-4000-8000-000000000002"
            principals_path = tmp_dir / "principals.json"
            principals_path.write_text(
                json.dumps({"api": oid_api, "token-maintenance": oid_token}), encoding="utf-8"
            )
            vault_scope = (
                "/subscriptions/s/resourceGroups/ama"
                "/providers/Microsoft.KeyVault/vaults/kv-ama-demo"
            )
            assignments_path = tmp_dir / "assignments.json"
            assignments_path.write_text(
                json.dumps(
                    {
                        "value": [
                            {
                                "principalId": oid_api,
                                "principalType": "ServicePrincipal",
                                "roleDefinitionName": "Key Vault Secrets User",
                                "scope": vault_scope,
                            },
                            {
                                "principalId": oid_token,
                                "principalType": "ServicePrincipal",
                                "roleDefinitionName": "Key Vault Secrets Officer",
                                "scope": f"{vault_scope}/secrets/entra-token-store-sas",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            diagnostics_path = tmp_dir / "diagnostics.json"
            diagnostics_path.write_text(
                json.dumps(
                    {
                        "value": [
                            {
                                "OperationName": "SecretGet",
                                "identity_claim_oid_g": oid_api,
                                "httpStatusCode_d": 200,
                                "id_s": "https://kv-ama-demo.vault.azure.net/secrets/entra-client-secret/v1",
                                "TimeGenerated": "2026-10-14T10:00:00Z",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            audit_q3 = tmp_dir / "audit-q3.json"
            rc_audit, _, err_audit = self._run_cli(
                [
                    "access-audit",
                    "--vault-name",
                    "kv-ama-demo",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--role-matrix",
                    str(ROOT / "role-assignments.json"),
                    "--expected-principals",
                    str(principals_path),
                    "--assignments",
                    str(assignments_path),
                    "--diagnostics",
                    str(diagnostics_path),
                    "--now",
                    "2026-10-15T00:00:00Z",
                    "--out",
                    str(audit_q3),
                ]
            )
            self.assertEqual(rc_audit, 0, err_audit)
            audit_payload = json.loads(audit_q3.read_text(encoding="utf-8"))
            self.assertEqual(audit_payload["anomalies"], [])

            decisions_path = tmp_dir / "decisions.json"
            decisions_path.write_text(
                json.dumps(
                    {
                        "assignments": {
                            row["assignmentId"]: {
                                "decision": "keep",
                                "rationale": "Verified active workload managed identity",
                            }
                            for row in audit_payload["rbacAssignments"]
                        },
                        "anomalies": {},
                    }
                ),
                encoding="utf-8",
            )
            key_file = tmp_dir / "signing.key"
            key_str = "cli-hmac-signing-key-material-32bytes!!"
            key_file.write_text(key_str, encoding="utf-8")
            os.chmod(key_file, 0o600)

            keys_file = tmp_dir / "verify-keys.json"
            keys_file.write_text(json.dumps({"ops-q3": key_str}), encoding="utf-8")
            os.chmod(keys_file, 0o600)

            ledger_path = tmp_dir / "access-reviews.jsonl"
            rc_sign1, _, err_sign1 = self._run_cli(
                [
                    "review-sign",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--audit",
                    str(audit_q3),
                    "--decisions",
                    str(decisions_path),
                    "--reviewer",
                    "Jose Miguel Servera (@jmservera)",
                    "--key-file",
                    str(key_file),
                    "--key-id",
                    "ops-q3",
                    "--ledger",
                    str(ledger_path),
                    "--now",
                    "2026-10-15T00:00:00Z",
                ]
            )
            self.assertEqual(rc_sign1, 0, err_sign1)

            audit_q4 = tmp_dir / "audit-q4.json"
            self._run_cli(
                [
                    "access-audit",
                    "--vault-name",
                    "kv-ama-demo",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--role-matrix",
                    str(ROOT / "role-assignments.json"),
                    "--expected-principals",
                    str(principals_path),
                    "--assignments",
                    str(assignments_path),
                    "--diagnostics",
                    str(diagnostics_path),
                    "--now",
                    "2027-01-10T00:00:00Z",
                    "--out",
                    str(audit_q4),
                ]
            )
            rc_sign2, _, err_sign2 = self._run_cli(
                [
                    "review-sign",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--audit",
                    str(audit_q4),
                    "--decisions",
                    str(decisions_path),
                    "--reviewer",
                    "Jose Miguel Servera (@jmservera)",
                    "--key-file",
                    str(key_file),
                    "--key-id",
                    "ops-q3",
                    "--ledger",
                    str(ledger_path),
                    "--now",
                    "2027-01-10T00:00:00Z",
                ]
            )
            self.assertEqual(rc_sign2, 0, err_sign2)

            rc_ver, out_ver, err_ver = self._run_cli(
                [
                    "ledger-verify",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--ledger",
                    str(ledger_path),
                    "--keys-file",
                    str(keys_file),
                    "--vault-name",
                    "kv-ama-demo",
                    "--now",
                    "2027-02-01T00:00:00Z",
                ]
            )
            self.assertEqual(rc_ver, 0, err_ver)
            verified = json.loads(out_ver)
            self.assertTrue(verified["intact"])
            self.assertEqual(verified["entryCount"], 2)

    def test_key_file_hygiene_rejects_group_readable_symlink_and_in_repo_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            ledger = tmp_dir / "empty.jsonl"
            ledger.write_text("", encoding="utf-8")

            open_keys = tmp_dir / "open-keys.json"
            open_keys.write_text(
                json.dumps({"k1": "0123456789abcdef0123456789abcdef"}), encoding="utf-8"
            )
            os.chmod(open_keys, 0o644)
            rc_mode, _, err_mode = self._run_cli(
                ["ledger-verify", "--ledger", str(ledger), "--keys-file", str(open_keys)]
            )
            self.assertEqual(rc_mode, 2)
            self.assertIn("0600", err_mode)

            os.chmod(open_keys, 0o600)
            link_keys = tmp_dir / "link-keys.json"
            link_keys.symlink_to(open_keys)
            rc_link, _, err_link = self._run_cli(
                ["ledger-verify", "--ledger", str(ledger), "--keys-file", str(link_keys)]
            )
            self.assertEqual(rc_link, 2)
            self.assertIn("symbolic link", err_link)

            repo_probe = ROOT / "secret-inventory.json"
            rc_repo, _, err_repo = self._run_cli(
                ["ledger-verify", "--ledger", str(ledger), "--keys-file", str(repo_probe)]
            )
            self.assertEqual(rc_repo, 2)
            self.assertIn("outside the Git repository", err_repo)

    def test_review_sign_rejects_json_array_ledger_and_preserves_missing_newline_jsonl(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            oid_api = "30000000-0000-4000-8000-000000000001"
            principals_path = tmp_dir / "principals.json"
            principals_path.write_text(json.dumps({"api": oid_api}), encoding="utf-8")
            vault_scope = (
                "/subscriptions/s/resourceGroups/ama"
                "/providers/Microsoft.KeyVault/vaults/kv-ama-demo"
            )
            assignments_path = tmp_dir / "assignments.json"
            assignments_path.write_text(
                json.dumps(
                    [
                        {
                            "principalId": oid_api,
                            "principalType": "ServicePrincipal",
                            "roleDefinitionName": "Key Vault Secrets User",
                            "scope": vault_scope,
                        }
                    ]
                ),
                encoding="utf-8",
            )
            diagnostics_path = tmp_dir / "diagnostics.json"
            diagnostics_path.write_text(json.dumps([]), encoding="utf-8")
            audit_q3 = tmp_dir / "audit-q3.json"
            self._run_cli(
                [
                    "access-audit",
                    "--vault-name",
                    "kv-ama-demo",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--role-matrix",
                    str(ROOT / "role-assignments.json"),
                    "--expected-principals",
                    str(principals_path),
                    "--assignments",
                    str(assignments_path),
                    "--diagnostics",
                    str(diagnostics_path),
                    "--now",
                    "2026-10-15T00:00:00Z",
                    "--out",
                    str(audit_q3),
                ]
            )
            audit_payload = json.loads(audit_q3.read_text(encoding="utf-8"))
            decisions_path = tmp_dir / "decisions.json"
            decisions_path.write_text(
                json.dumps(
                    {
                        "assignments": {
                            row["assignmentId"]: {"decision": "keep", "rationale": "Active API"}
                            for row in audit_payload["rbacAssignments"]
                        },
                        "anomalies": {},
                    }
                ),
                encoding="utf-8",
            )
            key_file = tmp_dir / "signing.key"
            key_str = "cli-hmac-signing-key-material-32bytes!!"
            key_file.write_text(key_str, encoding="utf-8")
            os.chmod(key_file, 0o600)

            array_ledger = tmp_dir / "readonly-array.json"
            array_ledger.write_text("[]\n", encoding="utf-8")
            rc_arr, _, err_arr = self._run_cli(
                [
                    "review-sign",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--audit",
                    str(audit_q3),
                    "--decisions",
                    str(decisions_path),
                    "--reviewer",
                    "Jose Miguel Servera (@jmservera)",
                    "--key-file",
                    str(key_file),
                    "--key-id",
                    "ops-q3",
                    "--ledger",
                    str(array_ledger),
                    "--now",
                    "2026-10-15T00:00:00Z",
                ]
            )
            self.assertEqual(rc_arr, 2)
            self.assertIn("JSONL", err_arr)
            self.assertEqual(array_ledger.read_text(encoding="utf-8"), "[]\n")

            jsonl_ledger = tmp_dir / "no-trailing-nl.jsonl"
            rc_s1, out_s1, _ = self._run_cli(
                [
                    "review-sign",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--audit",
                    str(audit_q3),
                    "--decisions",
                    str(decisions_path),
                    "--reviewer",
                    "Jose Miguel Servera (@jmservera)",
                    "--key-file",
                    str(key_file),
                    "--key-id",
                    "ops-q3",
                    "--now",
                    "2026-10-15T00:00:00Z",
                ]
            )
            self.assertEqual(rc_s1, 0)
            jsonl_ledger.write_text(
                json.dumps(json.loads(out_s1), sort_keys=True, separators=(",", ":")),
                encoding="utf-8",
            )

            audit_q4 = tmp_dir / "audit-q4.json"
            self._run_cli(
                [
                    "access-audit",
                    "--vault-name",
                    "kv-ama-demo",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--role-matrix",
                    str(ROOT / "role-assignments.json"),
                    "--expected-principals",
                    str(principals_path),
                    "--assignments",
                    str(assignments_path),
                    "--diagnostics",
                    str(diagnostics_path),
                    "--now",
                    "2026-11-15T00:00:00Z",
                    "--out",
                    str(audit_q4),
                ]
            )
            rc_s2, _, err_s2 = self._run_cli(
                [
                    "review-sign",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--audit",
                    str(audit_q4),
                    "--decisions",
                    str(decisions_path),
                    "--reviewer",
                    "Jose Miguel Servera (@jmservera)",
                    "--key-file",
                    str(key_file),
                    "--key-id",
                    "ops-q3",
                    "--ledger",
                    str(jsonl_ledger),
                    "--now",
                    "2026-11-15T00:00:00Z",
                ]
            )
            self.assertEqual(rc_s2, 0, err_s2)
            self.assertEqual(len(LIFE.load_ledger_entries(jsonl_ledger)), 2)

    def test_cli_signing_flags_browser_gate_and_runbook_command_safety(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("tr -d '\\r\\n'", readme)
        self.assertIn("--output none", readme)
        self.assertNotIn("tolower(", readme)
        self.assertIn("--include-inherited", readme)
        self.assertIn("rbac-merge", readme)
        self.assertIn("--signing-key-file", readme)
        self.assertIn("--signing-key-env", readme)
        self.assertIn("canonical SHA-256 integrity checksum", readme)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            rot_key = tmp_dir / "rot.key"
            key_material = "rotation-hmac-key-material-32bytes-ok!!"
            rot_key.write_text(key_material, encoding="utf-8")
            os.chmod(rot_key, 0o600)

            sw_payload = self._rotation_payload(switched=True)
            sw_path = tmp_dir / "sw.json"
            sw_receipt_path = tmp_dir / "sw-receipt.json"
            sw_path.write_text(json.dumps(sw_payload), encoding="utf-8")

            rc_both, _, err_both = self._run_cli(
                [
                    "rotation-verify",
                    "--evidence",
                    str(sw_path),
                    "--signing-key-file",
                    str(rot_key),
                    "--signing-key-env",
                    "ZF_TEST_ROT_KEY",
                    "--now",
                    "2026-10-16T00:00:00Z",
                ]
            )
            self.assertEqual(rc_both, 2)
            self.assertIn("at most one", err_both)

            rc_sw, _, err_sw = self._run_cli(
                [
                    "rotation-verify",
                    "--evidence",
                    str(sw_path),
                    "--signing-key-file",
                    str(rot_key),
                    "--now",
                    "2026-10-16T00:00:00Z",
                    "--out",
                    str(sw_receipt_path),
                ]
            )
            self.assertEqual(rc_sw, 0, err_sw)
            sw_receipt = json.loads(sw_receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(sw_receipt["signatureAlgorithm"], "HMAC-SHA256")

            retire_payload = self._rotation_payload(switched=True)
            retire_payload["stage"] = "post_retire"
            retire_payload["credentials"]["entries"] = [retire_payload["credentials"]["entries"][1]]
            retire_payload["credentials"]["priorRetiredAt"] = "2026-10-16T00:25:00Z"
            retire_payload["secretVersions"]["entries"][0]["enabled"] = False
            retire_payload["healthProbes"].append(
                {
                    "stage": "post_retire",
                    "totalSamples": 5,
                    "errorCount": 0,
                    "firstSampleAt": "2026-10-16T00:30:00Z",
                    "lastSampleAt": "2026-10-16T00:32:00Z",
                    "maxGapSeconds": 30,
                    "healthzStatus": 200,
                    "anonymousApiStatus": 401,
                    "signInRedirectStatus": 302,
                    "authenticatedApiStatus": 200,
                    "freshTokenExchangeVerified": True,
                }
            )
            retire_payload["priorSwitchoverReceipt"] = sw_receipt
            retire_path = tmp_dir / "retire.json"
            retire_path.write_text(json.dumps(retire_payload), encoding="utf-8")

            rc_no_key, _, _ = self._run_cli(
                ["rotation-verify", "--evidence", str(retire_path), "--now", "2026-10-16T01:00:00Z"]
            )
            self.assertEqual(rc_no_key, 1)

            old_env = os.environ.get("ZF_TEST_ROT_KEY")
            os.environ["ZF_TEST_ROT_KEY"] = key_material
            try:
                rc_env_ok, out_env_ok, err_env_ok = self._run_cli(
                    [
                        "rotation-verify",
                        "--evidence",
                        str(retire_path),
                        "--signing-key-env",
                        "ZF_TEST_ROT_KEY",
                        "--now",
                        "2026-10-16T01:00:00Z",
                    ]
                )
            finally:
                if old_env is None:
                    os.environ.pop("ZF_TEST_ROT_KEY", None)
                else:
                    os.environ["ZF_TEST_ROT_KEY"] = old_env
            self.assertEqual(rc_env_ok, 0, err_env_ok)
            self.assertTrue(json.loads(out_env_ok)["postRetireVerified"])

            non_browser = self._rotation_payload(switched=True)
            non_browser["browserMode"] = False
            del non_browser["healthProbes"][0]["signInRedirectStatus"]
            del non_browser["healthProbes"][1]["signInRedirectStatus"]
            del non_browser["healthProbes"][1]["authenticatedApiStatus"]
            del non_browser["healthProbes"][1]["freshTokenExchangeVerified"]
            nb_path = tmp_dir / "nb.json"
            nb_path.write_text(json.dumps(non_browser), encoding="utf-8")

            rc_nb_blocked, _, _ = self._run_cli(
                ["rotation-verify", "--evidence", str(nb_path), "--now", "2026-10-16T00:00:00Z"]
            )
            self.assertEqual(rc_nb_blocked, 1)

            rc_nb_allowed, _, err_nb_allowed = self._run_cli(
                [
                    "rotation-verify",
                    "--evidence",
                    str(nb_path),
                    "--allow-non-browser-mode",
                    "--now",
                    "2026-10-16T00:00:00Z",
                ]
            )
            self.assertEqual(rc_nb_allowed, 0, err_nb_allowed)

    def test_rbac_merge_cli_preserves_root_and_mg_ancestors_and_feeds_access_audit(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            oid_api = "40000000-0000-4000-8000-000000000001"
            oid_token = "40000000-0000-4000-8000-000000000002"
            oid_mg_admin = "40000000-0000-4000-8000-000000000099"
            vid = (
                "/subscriptions/s/resourceGroups/ama"
                "/providers/Microsoft.KeyVault/vaults/kv-ama-demo"
            )
            inh_path = tmp_dir / "roles-inh.json"
            all_path = tmp_dir / "roles-all.json"
            merged_path = tmp_dir / "roles.json"
            inh_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "asgn-root",
                            "principalId": oid_api,
                            "principalType": "ServicePrincipal",
                            "roleDefinitionName": "Owner",
                            "scope": "/",
                        },
                        {
                            "id": "asgn-mg",
                            "principalId": oid_mg_admin,
                            "principalType": "Group",
                            "roleDefinitionName": "Key Vault Administrator",
                            "scope": "/providers/Microsoft.Management/managementGroups/mg-root",
                        },
                        {
                            "id": "asgn-vault",
                            "principalId": oid_api,
                            "principalType": "ServicePrincipal",
                            "roleDefinitionName": "Key Vault Secrets User",
                            "scope": vid,
                        },
                    ]
                ),
                encoding="utf-8",
            )
            all_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "asgn-vault",
                            "principalId": oid_api,
                            "principalType": "ServicePrincipal",
                            "roleDefinitionName": "Key Vault Secrets User",
                            "scope": vid,
                        },
                        {
                            "id": "asgn-child",
                            "principalId": oid_token,
                            "principalType": "ServicePrincipal",
                            "roleDefinitionName": "Key Vault Secrets Officer",
                            "scope": f"{vid}/secrets/entra-token-store-sas",
                        },
                    ]
                ),
                encoding="utf-8",
            )
            rc_merge, _, err_merge = self._run_cli(
                [
                    "rbac-merge",
                    "--vault-id",
                    vid,
                    "--inherited",
                    str(inh_path),
                    "--all",
                    str(all_path),
                    "--out",
                    str(merged_path),
                ]
            )
            self.assertEqual(rc_merge, 0, err_merge)
            merged_rows = json.loads(merged_path.read_text(encoding="utf-8"))
            self.assertEqual(len(merged_rows), 4)

            principals_path = tmp_dir / "principals.json"
            principals_path.write_text(
                json.dumps({"api": oid_api, "token-maintenance": oid_token}),
                encoding="utf-8",
            )
            diag_path = tmp_dir / "diag.json"
            diag_path.write_text("[]\n", encoding="utf-8")
            rc_audit, out_audit, err_audit = self._run_cli(
                [
                    "access-audit",
                    "--vault-name",
                    "kv-ama-demo",
                    "--inventory",
                    str(ROOT / "secret-inventory.json"),
                    "--role-matrix",
                    str(ROOT / "role-assignments.json"),
                    "--expected-principals",
                    str(principals_path),
                    "--assignments",
                    str(merged_path),
                    "--diagnostics",
                    str(diag_path),
                    "--now",
                    "2026-10-15T00:00:00Z",
                ]
            )
            self.assertEqual(rc_audit, 0, err_audit)
            audit_data = json.loads(out_audit)
            self.assertEqual(len(audit_data["rbacAssignments"]), 4)
            self.assertTrue(
                any(
                    a["principalId"] == oid_mg_admin and a["kind"] == "unmapped_rbac_principal"
                    for a in audit_data["anomalies"]
                )
            )

    def test_cli_rejects_nan_infinity_json_constants_and_sanitizes_signing_key_env(self) -> None:
        canary = "UNLABELLED_CLI_CANARY_secret_987"
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            nan_ev = tmp_dir / "nan-ev.json"
            nan_ev.write_text('{"stage": "post_switchover", "metric": NaN}\n', encoding="utf-8")
            rc_ev, _, err_ev = self._run_cli(["rotation-verify", "--evidence", str(nan_ev)])
            self.assertEqual(rc_ev, 2)
            self.assertIn("non-standard numeric constant", err_ev)

            nan_arr = tmp_dir / "nan-arr.json"
            nan_arr.write_text('[{"vaultName": "kv-ama-demo", "x": Infinity}]\n', encoding="utf-8")
            with self.assertRaises(LIFE.SecretLifecycleError):
                LIFE.load_ledger_entries(nan_arr)

            nan_jsonl = tmp_dir / "nan.jsonl"
            nan_jsonl.write_text('{"vaultName": "kv-ama-demo", "x": -Infinity}\n', encoding="utf-8")
            with self.assertRaises(LIFE.SecretLifecycleError):
                LIFE.load_ledger_entries(nan_jsonl)

            bad_keys = tmp_dir / "bad-keys.json"
            bad_keys.write_text('{"ops-q4": NaN}\n', encoding="utf-8")
            os.chmod(bad_keys, 0o600)
            empty_ledger = tmp_dir / "empty.jsonl"
            empty_ledger.write_text("", encoding="utf-8")
            rc_keys, _, _ = self._run_cli(
                ["ledger-verify", "--ledger", str(empty_ledger), "--keys-file", str(bad_keys)]
            )
            self.assertEqual(rc_keys, 2)

            ok_ev = tmp_dir / "ok-ev.json"
            ok_ev.write_text(json.dumps(self._rotation_payload(switched=True)), encoding="utf-8")
            rc_bad_env, _, err_bad_env = self._run_cli(
                [
                    "rotation-verify",
                    "--evidence",
                    str(ok_ev),
                    "--signing-key-env",
                    f"NOT-AN-ENV={canary}",
                    "--now",
                    "2026-10-16T00:00:00Z",
                ]
            )
            self.assertEqual(rc_bad_env, 2)
            self.assertNotIn(canary, err_bad_env)

            unset_var = f"ZF_UNSET_{canary}"
            os.environ.pop(unset_var, None)
            rc_unset, _, err_unset = self._run_cli(
                [
                    "rotation-verify",
                    "--evidence",
                    str(ok_ev),
                    "--signing-key-env",
                    unset_var,
                    "--now",
                    "2026-10-16T00:00:00Z",
                ]
            )
            self.assertEqual(rc_unset, 2)
            self.assertNotIn(canary, err_unset)

    def test_readme_rotation_step1_matches_rotation_plan_and_pinned_rollback_cli(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        plan_lines = LIFE.rotation_plan("kv-ama-demo", "00000000-1111-2222-3333-444444444444")
        self.assertTrue(any("--years 1" in line for line in plan_lines))
        self.assertIn("--years 1", readme)
        self.assertNotIn("--end-date <iso>", readme)
        self.assertIn("SecretDisabled", readme)
        self.assertIn("firstSampleAt >= retiredAt", readme)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            rb = self._rotation_payload(switched=False)
            rb["stage"] = "rollback"
            rb["secretVersions"]["entries"][1]["enabled"] = False
            del rb["containerApp"]["switchoverAt"]
            rb["containerApp"]["rollbackAt"] = "2026-10-15T02:10:00Z"
            rb["healthProbes"] = [
                {
                    "stage": "rollback",
                    "totalSamples": 5,
                    "errorCount": 0,
                    "firstSampleAt": "2026-10-15T02:15:00Z",
                    "lastSampleAt": "2026-10-15T02:17:00Z",
                    "maxGapSeconds": 30,
                    "healthzStatus": 200,
                    "anonymousApiStatus": 401,
                    "signInRedirectStatus": 302,
                    "authenticatedApiStatus": 200,
                    "freshTokenExchangeVerified": True,
                }
            ]
            vless_path = tmp_dir / "rb-vless.json"
            vless_path.write_text(json.dumps(rb), encoding="utf-8")
            rc_vl, out_vl, _ = self._run_cli(
                ["rotation-verify", "--evidence", str(vless_path), "--now", "2026-10-15T03:00:00Z"]
            )
            self.assertEqual(rc_vl, 1)
            self.assertFalse(json.loads(out_vl)["rollbackVerified"])

            prior_ver = rb["secretVersions"]["priorVersionId"]
            rb["containerApp"]["secrets"][0]["keyVaultUrl"] = (
                f"https://kv-ama-demo.vault.azure.net/secrets/entra-client-secret/{prior_ver}"
            )
            pinned_path = tmp_dir / "rb-pinned.json"
            pinned_path.write_text(json.dumps(rb), encoding="utf-8")
            rc_pin, out_pin, _ = self._run_cli(
                ["rotation-verify", "--evidence", str(pinned_path), "--now", "2026-10-15T03:00:00Z"]
            )
            self.assertEqual(rc_pin, 1)
            self.assertTrue(json.loads(out_pin)["rollbackVerified"])


if __name__ == "__main__":
    unittest.main()
