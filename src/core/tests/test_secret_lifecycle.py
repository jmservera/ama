"""Deterministic unit tests for Key Vault secret lifecycle verification and signed ledgers."""

from __future__ import annotations

import copy
import datetime as dt
import json
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.secret_lifecycle import (
    GENESIS_HASH,
    SecretExposureError,
    SecretLifecycleError,
    access_review,
    assert_no_secret_material,
    audit_keyvault_data_plane_access,
    check_secrets,
    create_signed_access_review_record,
    default_expected_caller_policy,
    merge_vault_role_assignments,
    parse_time,
    review_status,
    rotation_plan,
    unwrap_arm_list_envelope,
    validate_human_reviewer,
    validate_inventory,
    verify_access_review_ledger,
    verify_staged_entra_rotation,
)

NOW = parse_time("2026-11-15T12:00:00Z")
VAULT = "kv-zava-ama-test"
PRIOR_VER = "11111111111111111111111111111111"
NEXT_VER = "22222222222222222222222222222222"
IDENTITY_ID = (
    "/subscriptions/00000000-0000-0000-0000-000000000001/resourceGroups/ama"
    "/providers/Microsoft.ManagedIdentity/userAssignedIdentities/id-api"
)
OID_API = "aaaaaaaa-0000-4000-8000-000000000001"
OID_TOKEN = "bbbbbbbb-0000-4000-8000-000000000002"
OID_RESIDENT = "cccccccc-0000-4000-8000-000000000003"
OID_AGENTS = "dddddddd-0000-4000-8000-000000000004"
OID_ROGUE = "ffffffff-0000-4000-8000-000000000099"
SIGNING_KEY_A = b"fixture-hmac-key-material-alpha-32b!"
SIGNING_KEY_B = b"fixture-hmac-key-material-bravo-32b!"


def _rotation_fixture(stage: str = "post_switchover") -> dict[str, Any]:
    active_version = NEXT_VER if stage in ("post_switchover", "post_retire") else PRIOR_VER
    probes: list[dict[str, Any]] = []
    if stage in ("dual_secret_overlap", "post_switchover"):
        probes.append(
            {
                "stage": "dual_secret_overlap",
                "totalSamples": 10,
                "errorCount": 0,
                "firstSampleAt": "2026-11-15T09:10:00Z",
                "lastSampleAt": "2026-11-15T09:14:30Z",
                "maxGapSeconds": 30,
                "healthzStatus": 200,
                "anonymousApiStatus": 401,
                "signInRedirectStatus": 302,
            }
        )
    if stage in ("post_switchover", "post_retire"):
        probes.append(
            {
                "stage": "post_switchover",
                "totalSamples": 12,
                "errorCount": 0,
                "firstSampleAt": "2026-11-15T10:15:00Z",
                "lastSampleAt": "2026-11-15T10:20:30Z",
                "maxGapSeconds": 30,
                "healthzStatus": 200,
                "anonymousApiStatus": 401,
                "signInRedirectStatus": 302,
                "authenticatedApiStatus": 200,
                "freshTokenExchangeVerified": True,
            }
        )
    if stage == "post_retire":
        probes.append(
            {
                "stage": "post_retire",
                "totalSamples": 12,
                "errorCount": 0,
                "firstSampleAt": "2026-11-15T11:30:00Z",
                "lastSampleAt": "2026-11-15T11:35:30Z",
                "maxGapSeconds": 30,
                "healthzStatus": 200,
                "anonymousApiStatus": 401,
                "signInRedirectStatus": 302,
                "authenticatedApiStatus": 200,
                "freshTokenExchangeVerified": True,
            }
        )
    if stage == "rollback":
        probes.append(
            {
                "stage": "rollback",
                "totalSamples": 8,
                "errorCount": 0,
                "firstSampleAt": "2026-11-15T10:30:00Z",
                "lastSampleAt": "2026-11-15T10:33:30Z",
                "maxGapSeconds": 30,
                "healthzStatus": 200,
                "anonymousApiStatus": 401,
                "signInRedirectStatus": 302,
                "authenticatedApiStatus": 200,
                "freshTokenExchangeVerified": True,
            }
        )

    cred_entries: list[dict[str, Any]] = [
        {
            "keyId": "key-next-2026-11",
            "startDateTime": "2026-11-15T09:00:00Z",
            "endDateTime": "2027-05-15T09:00:00Z",
        }
    ]
    retired_prior: dict[str, Any] | None = None
    if stage != "post_retire":
        cred_entries.insert(
            0,
            {
                "keyId": "key-prior-2026-05",
                "startDateTime": "2026-05-15T09:00:00Z",
                "endDateTime": "2026-12-15T09:00:00Z",
            },
        )
    else:
        retired_prior = {
            "keyId": "key-prior-2026-05",
            "startDateTime": "2026-05-15T09:00:00Z",
            "endDateTime": "2026-12-15T09:00:00Z",
            "retiredAt": "2026-11-15T11:30:00Z",
        }

    credentials: dict[str, Any] = {
        "priorKeyId": "key-prior-2026-05",
        "nextKeyId": "key-next-2026-11",
        "entries": cred_entries,
    }
    if retired_prior is not None:
        credentials["retiredPriorCredential"] = retired_prior

    return {
        "stage": stage,
        "vaultName": VAULT,
        "secretName": "entra-client-secret",
        "appId": "00000000-1111-2222-3333-444444444444",
        "expectedIdentityId": IDENTITY_ID,
        "browserMode": True,
        "credentials": credentials,
        "secretVersions": {
            "priorVersionId": PRIOR_VER,
            "nextVersionId": NEXT_VER,
            "entries": [
                {
                    "id": (
                        f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret/{PRIOR_VER}"
                    ),
                    "enabled": stage != "post_retire",
                    "created": "2026-05-15T09:00:00Z",
                    "expires": "2026-12-15T09:00:00Z",
                },
                {
                    "id": (
                        f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret/{NEXT_VER}"
                    ),
                    "enabled": stage != "rollback",
                    "created": "2026-11-15T09:05:00Z",
                    "expires": "2027-05-15T09:00:00Z",
                },
            ],
        },
        "containerApp": {
            "clientSecretSettingName": "entra-client-secret",
            **(
                {"switchoverAt": "2026-11-15T10:10:00Z"}
                if stage in ("post_switchover", "post_retire")
                else {}
            ),
            **({"rollbackAt": "2026-11-15T10:25:00Z"} if stage == "rollback" else {}),
            "secrets": [
                {
                    "name": "entra-client-secret",
                    "identity": IDENTITY_ID,
                    "keyVaultUrl": (
                        f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret/{PRIOR_VER}"
                        if stage == "rollback"
                        else f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret"
                    ),
                }
            ],
            "revisions": [
                {
                    "name": "ca-api--rev2",
                    "active": True,
                    "trafficWeight": 100,
                    "runningState": "Running",
                    "replicasReady": 2,
                    "secretVersionId": active_version,
                    "secretName": "entra-client-secret",
                }
            ],
        },
        "healthProbes": probes,
    }


def _inventory_fixture() -> dict[str, Any]:
    return {
        "reviewIntervalDays": 90,
        "secrets": [
            {
                "name": "entra-client-secret",
                "owner": "Identity owner (@jmservera)",
                "rotationIntervalDays": 180,
                "expiryAlertDays": 30,
            },
            {
                "name": "entra-token-store-sas",
                "owner": "Platform operator (@jmservera)",
                "rotationIntervalDays": 1,
                "expiryAlertDays": 7,
            },
            {
                "name": "resident-demo-password-verifier",
                "owner": "Demonstration operator (@jmservera)",
                "rotationIntervalDays": 180,
                "expiryAlertDays": 14,
            },
            {
                "name": "resident-demo-session-key",
                "owner": "Demonstration operator (@jmservera)",
                "rotationIntervalDays": 180,
                "expiryAlertDays": 14,
            },
        ],
    }


def _role_matrix_fixture() -> dict[str, Any]:
    return {
        "builtInRoles": {
            "role-kv-user": "Key Vault Secrets User",
            "role-kv-officer": "Key Vault Secrets Officer",
            "role-queue": "Storage Queue Data Contributor",
        },
        "assignments": [
            {
                "identity": "api",
                "resource": "keyvault",
                "scope": "Key Vault",
                "roleId": "role-kv-user",
            },
            {
                "identity": "token-maintenance",
                "resource": "keyvault",
                "scope": "Secret entra-token-store-sas only",
                "roleId": "role-kv-officer",
            },
            {
                "identity": "resident-demo",
                "resource": "keyvault",
                "scope": "Secret resident-demo-password-verifier only",
                "roleId": "role-kv-user",
            },
            {
                "identity": "resident-demo",
                "resource": "keyvault",
                "scope": "Secret resident-demo-session-key only",
                "roleId": "role-kv-user",
            },
            {
                "identity": "agents",
                "resource": "storage",
                "scope": "Storage account, queue service",
                "roleId": "role-queue",
            },
            {
                "identity": "orchestrator",
                "resource": "storage",
                "scope": "Storage account, queue service",
                "roleId": "role-queue",
            },
            {
                "identity": "import",
                "resource": "storage",
                "scope": "Storage account, queue service",
                "roleId": "role-queue",
            },
        ],
    }


def _principal_map_fixture() -> dict[str, str]:
    return {
        "api": OID_API,
        "token-maintenance": OID_TOKEN,
        "resident-demo": OID_RESIDENT,
        "agents": OID_AGENTS,
    }


class SecretGuardTests(unittest.TestCase):
    def test_rejects_forbidden_keys_and_patterns_without_echoing_canary(self) -> None:
        canary = "CANARY_SUPER_SECRET_DO_NOT_ECHO_98765"
        for bad in (
            {"nested": {"clientSecret": canary}},
            {"nested": {"value": canary}},
            {"uri": f"https://acct.blob.core.windows.net/c?sv=2024-01-01&sig={canary}"},
            {"header": f"Bearer {canary}"},
            {"jwt": f"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.{canary}"},
        ):
            with self.assertRaises(SecretExposureError) as ctx:
                assert_no_secret_material(bad)
            self.assertNotIn(canary, str(ctx.exception))

    def test_allows_hex_digests_and_unwraps_top_level_arm_list_envelope(self) -> None:
        wrapped = {
            "value": [{"name": "entra-client-secret", "version": PRIOR_VER, "digest": "a" * 64}]
        }
        rows = unwrap_arm_list_envelope(wrapped)
        self.assertEqual(len(rows), 1)
        with self.assertRaises(SecretExposureError):
            unwrap_arm_list_envelope({"value": [{"name": "ok", "value": "leaked-secret"}]})

    def test_rejects_non_finite_floats_and_paginated_arm_envelopes(self) -> None:
        for bad_num in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(SecretLifecycleError):
                assert_no_secret_material({"metric": bad_num})
        for link_key in ("nextLink", "@odata.nextLink"):
            with self.assertRaises(SecretLifecycleError):
                unwrap_arm_list_envelope(
                    {"value": [{"name": "ok"}], link_key: "https://management.azure.com/page2"}
                )
            with self.assertRaises(SecretExposureError):
                unwrap_arm_list_envelope(
                    {"value": [{"name": "ok"}], link_key: "Bearer SECRET_PAGE_TOKEN_999"}
                )


class StagedEntraRotationTests(unittest.TestCase):
    def test_valid_dual_overlap_and_post_switchover_progression(self) -> None:
        overlap = verify_staged_entra_rotation(_rotation_fixture("dual_secret_overlap"), now=NOW)
        self.assertTrue(overlap["ok"])
        self.assertFalse(overlap["safeToRetirePriorCredential"])
        self.assertGreaterEqual(overlap["overlapMinutes"], 60)

        switched = verify_staged_entra_rotation(_rotation_fixture("post_switchover"), now=NOW)
        self.assertTrue(switched["ok"])
        self.assertTrue(switched["zeroDowntimeVerified"])
        self.assertTrue(switched["versionSwitchoverVerified"])
        self.assertTrue(switched["safeToRetirePriorCredential"])
        self.assertEqual(switched["problems"], [])

    def test_supports_staged_two_name_secret_switchover(self) -> None:
        ev = _rotation_fixture("post_switchover")
        ev["priorSecretName"] = "entra-client-secret"
        ev["secretName"] = "entra-client-secret-2026-11"
        ev["secretVersions"]["entries"][1]["id"] = (
            f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret-2026-11/{NEXT_VER}"
        )
        ev["containerApp"]["secrets"][0]["keyVaultUrl"] = (
            f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret-2026-11"
        )
        ev["containerApp"]["revisions"][0]["secretName"] = "entra-client-secret-2026-11"
        receipt = verify_staged_entra_rotation(ev, now=NOW)
        self.assertTrue(receipt["ok"], receipt["problems"])
        self.assertTrue(receipt["safeToRetirePriorCredential"])

    def test_rejects_overlap_shorter_than_minimum_window(self) -> None:
        ev = _rotation_fixture("post_switchover")
        ev["credentials"]["entries"][0]["endDateTime"] = "2026-11-15T12:05:00Z"
        ev["credentials"]["entries"][1]["startDateTime"] = "2026-11-15T11:45:00Z"
        receipt = verify_staged_entra_rotation(ev, now=NOW, min_overlap_minutes=60)
        self.assertFalse(receipt["ok"])
        self.assertFalse(receipt["safeToRetirePriorCredential"])
        self.assertTrue(any("dual-secret overlap" in p for p in receipt["problems"]))

    def test_rejects_active_revision_still_serving_prior_version(self) -> None:
        ev = _rotation_fixture("post_switchover")
        ev["containerApp"]["revisions"][0]["secretVersionId"] = PRIOR_VER
        receipt = verify_staged_entra_rotation(ev, now=NOW)
        self.assertFalse(receipt["ok"])
        self.assertFalse(receipt["versionSwitchoverVerified"])
        self.assertFalse(receipt["safeToRetirePriorCredential"])

    def test_rejects_missing_authenticated_probe_or_auth_regression_after_switchover(self) -> None:
        missing_auth = _rotation_fixture("post_switchover")
        del missing_auth["healthProbes"][1]["authenticatedApiStatus"]
        r1 = verify_staged_entra_rotation(missing_auth, now=NOW)
        self.assertFalse(r1["ok"])
        self.assertTrue(any("authenticated session probe" in p for p in r1["problems"]))

        anon_bypass = _rotation_fixture("post_switchover")
        anon_bypass["healthProbes"][1]["anonymousApiStatus"] = 200
        r2 = verify_staged_entra_rotation(anon_bypass, now=NOW)
        self.assertFalse(r2["ok"])
        self.assertFalse(r2["zeroDowntimeVerified"])

    def test_rollback_stage_verifies_prior_restore_and_blocks_retirement(self) -> None:
        ev = _rotation_fixture("rollback")
        receipt = verify_staged_entra_rotation(ev, now=NOW)
        self.assertFalse(receipt["ok"])
        self.assertTrue(receipt["rollbackVerified"])
        self.assertFalse(receipt["safeToRetirePriorCredential"])
        self.assertTrue(any("rollback hold active" in p for p in receipt["problems"]))

    def test_post_retire_requires_retired_prior_and_verifiable_overlap_proof(self) -> None:
        ev = _rotation_fixture("post_retire")
        receipt = verify_staged_entra_rotation(ev, now=NOW)
        self.assertTrue(receipt["ok"], receipt["problems"])
        self.assertTrue(receipt["postRetireVerified"])
        self.assertFalse(receipt["safeToRetirePriorCredential"])

        no_proof = copy.deepcopy(ev)
        del no_proof["credentials"]["retiredPriorCredential"]
        failed = verify_staged_entra_rotation(no_proof, now=NOW)
        self.assertFalse(failed["ok"])
        self.assertTrue(any("retiredPriorCredential" in p for p in failed["problems"]))

    def test_rejects_secret_exposure_in_rotation_evidence(self) -> None:
        ev = _rotation_fixture("post_switchover")
        ev["credentials"]["secretText"] = "DO_NOT_LOG_RAW_ENTRA_SECRET"
        with self.assertRaises(SecretExposureError) as ctx:
            verify_staged_entra_rotation(ev, now=NOW)
        self.assertNotIn("DO_NOT_LOG_RAW_ENTRA_SECRET", str(ctx.exception))

    def test_rejects_premature_elapsed_overlap_missing_fresh_exchange_and_bad_uris(self) -> None:
        premature = _rotation_fixture("post_switchover")
        premature["credentials"]["entries"][1]["startDateTime"] = "2026-11-15T11:59:59Z"
        r_premature = verify_staged_entra_rotation(premature, now=NOW, min_overlap_minutes=60)
        self.assertFalse(r_premature["ok"])
        self.assertFalse(r_premature["safeToRetirePriorCredential"])
        self.assertTrue(any("elapsed dual-secret overlap" in p for p in r_premature["problems"]))

        cached_only = _rotation_fixture("post_switchover")
        cached_only["healthProbes"][1]["freshTokenExchangeVerified"] = False
        r_cached = verify_staged_entra_rotation(cached_only, now=NOW)
        self.assertFalse(r_cached["ok"])
        self.assertFalse(r_cached["safeToRetirePriorCredential"])
        self.assertTrue(any("freshTokenExchangeVerified" in p for p in r_cached["problems"]))

        missing_uri = _rotation_fixture("post_switchover")
        del missing_uri["secretVersions"]["entries"][1]["id"]
        missing_uri["secretVersions"]["entries"][1]["version"] = NEXT_VER
        r_no_uri = verify_staged_entra_rotation(missing_uri, now=NOW)
        self.assertFalse(r_no_uri["ok"])
        self.assertFalse(r_no_uri["versionSwitchoverVerified"])

        masked_secret = _rotation_fixture("post_switchover")
        masked_secret["secretVersions"]["entries"][1]["id"] = (
            f"https://{VAULT}.vault.azure.net/secrets/entra-token-store-sas/{NEXT_VER}"
        )
        masked_secret["secretVersions"]["entries"][1]["secretName"] = "entra-client-secret"
        r_masked = verify_staged_entra_rotation(masked_secret, now=NOW)
        self.assertFalse(r_masked["ok"])
        self.assertFalse(r_masked["versionSwitchoverVerified"])

    def test_post_retire_rejects_future_retired_at_and_unbound_prior_receipt(self) -> None:
        future_retire = _rotation_fixture("post_retire")
        future_retire["credentials"]["retiredPriorCredential"]["retiredAt"] = "2026-11-15T18:00:00Z"
        r_future = verify_staged_entra_rotation(future_retire, now=NOW)
        self.assertFalse(r_future["ok"])
        self.assertFalse(r_future["postRetireVerified"])

        valid_switchover = verify_staged_entra_rotation(
            _rotation_fixture("post_switchover"),
            now=NOW,
            signing_key=SIGNING_KEY_A,
        )
        self.assertTrue(valid_switchover["safeToRetirePriorCredential"])
        self.assertEqual(valid_switchover["signatureAlgorithm"], "HMAC-SHA256")

        bound_retire = _rotation_fixture("post_retire")
        del bound_retire["credentials"]["retiredPriorCredential"]
        bound_retire["credentials"]["priorRetiredAt"] = "2026-11-15T11:30:00Z"
        bound_retire["priorSwitchoverReceipt"] = copy.deepcopy(valid_switchover)
        r_bound = verify_staged_entra_rotation(
            bound_retire,
            now=NOW,
            signing_key=SIGNING_KEY_A,
        )
        self.assertTrue(r_bound["ok"], r_bound["problems"])
        self.assertTrue(r_bound["postRetireVerified"])

        cross_rotation = copy.deepcopy(bound_retire)
        cross_rotation["priorSwitchoverReceipt"]["nextKeyId"] = "key-from-older-rotation"
        r_cross = verify_staged_entra_rotation(
            cross_rotation,
            now=NOW,
            signing_key=SIGNING_KEY_A,
        )
        self.assertFalse(r_cross["ok"])
        self.assertFalse(r_cross["postRetireVerified"])

    def test_seals_browser_mode_strict_enabled_uri_redaction_rollback_and_hmac_receipt(
        self,
    ) -> None:
        downgraded = _rotation_fixture("post_switchover")
        downgraded["browserMode"] = False
        del downgraded["healthProbes"][0]["signInRedirectStatus"]
        del downgraded["healthProbes"][1]["signInRedirectStatus"]
        del downgraded["healthProbes"][1]["authenticatedApiStatus"]
        del downgraded["healthProbes"][1]["freshTokenExchangeVerified"]
        r_denied = verify_staged_entra_rotation(downgraded, now=NOW)
        self.assertFalse(r_denied["ok"])
        self.assertFalse(r_denied["zeroDowntimeVerified"])
        self.assertTrue(any("browserMode=false" in p for p in r_denied["problems"]))

        r_explicit_api_only = verify_staged_entra_rotation(
            downgraded, now=NOW, require_browser_mode=False
        )
        self.assertTrue(r_explicit_api_only["ok"], r_explicit_api_only["problems"])

        str_enabled_cred = _rotation_fixture("post_switchover")
        str_enabled_cred["credentials"]["entries"][1]["enabled"] = "false"
        r_str_cred = verify_staged_entra_rotation(str_enabled_cred, now=NOW)
        self.assertFalse(r_str_cred["ok"])
        self.assertTrue(any("enabled must be a boolean" in p for p in r_str_cred["problems"]))

        conflict_ver = _rotation_fixture("post_retire")
        conflict_ver["secretVersions"]["entries"][0]["enabled"] = False
        conflict_ver["secretVersions"]["entries"][0]["attributes"] = {"enabled": True}
        r_conflict_ver = verify_staged_entra_rotation(conflict_ver, now=NOW)
        self.assertFalse(r_conflict_ver["ok"])
        self.assertTrue(any("conflicts" in p for p in r_conflict_ver["problems"]))

        uri_canary = "CANARY_RAW_URI_SEGMENT_DO_NOT_ECHO_42"
        bad_uris = _rotation_fixture("dual_secret_overlap")
        bad_uris["secretVersions"]["entries"][0]["id"] = f"https://evil.example/{uri_canary}"
        bad_uris["containerApp"]["secrets"][0]["keyVaultUrl"] = (
            f"https://{VAULT}.vault.azure.net/secrets/{uri_canary}"
        )
        bad_uris["containerApp"]["revisions"][0]["secretVersionId"] = uri_canary
        r_redacted = verify_staged_entra_rotation(bad_uris, now=NOW)
        self.assertFalse(r_redacted["ok"])
        joined_problems = " | ".join(r_redacted["problems"])
        self.assertNotIn(uri_canary, joined_problems)

        broken_rb = _rotation_fixture("rollback")
        broken_rb["vaultName"] = "bad!"
        r_broken_rb = verify_staged_entra_rotation(broken_rb, now=NOW)
        self.assertFalse(r_broken_rb["rollbackVerified"])

        signed_sw = verify_staged_entra_rotation(
            _rotation_fixture("post_switchover"),
            now=NOW,
            signing_key=SIGNING_KEY_A,
        )
        retire_ev = _rotation_fixture("post_retire")
        del retire_ev["credentials"]["retiredPriorCredential"]
        retire_ev["credentials"]["priorRetiredAt"] = "2026-11-15T11:30:00Z"
        retire_ev["priorSwitchoverReceipt"] = copy.deepcopy(signed_sw)

        r_no_key = verify_staged_entra_rotation(retire_ev, now=NOW)
        self.assertFalse(r_no_key["ok"])
        r_wrong_key = verify_staged_entra_rotation(retire_ev, now=NOW, signing_key=SIGNING_KEY_B)
        self.assertFalse(r_wrong_key["ok"])

        forged_receipt = copy.deepcopy(retire_ev)
        forged_receipt["priorSwitchoverReceipt"]["overlapMinutes"] = 999.0
        r_forged = verify_staged_entra_rotation(forged_receipt, now=NOW, signing_key=SIGNING_KEY_A)
        self.assertFalse(r_forged["ok"])

    def test_rollback_requires_disabled_next_version_on_versionless_url_and_fresh_exchange(
        self,
    ) -> None:
        pinned_default = _rotation_fixture("rollback")
        r_pinned_default = verify_staged_entra_rotation(pinned_default, now=NOW)
        self.assertTrue(r_pinned_default["rollbackVerified"], r_pinned_default["problems"])
        self.assertFalse(r_pinned_default["ok"])
        self.assertFalse(r_pinned_default["safeToRetirePriorCredential"])

        versionless_inplace = _rotation_fixture("rollback")
        versionless_inplace["containerApp"]["secrets"][0]["keyVaultUrl"] = (
            f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret"
        )
        r_vless = verify_staged_entra_rotation(versionless_inplace, now=NOW)
        self.assertFalse(r_vless["rollbackVerified"])
        self.assertTrue(any("SecretDisabled" in p for p in r_vless["problems"]))

        two_name_rb = _rotation_fixture("rollback")
        two_name_rb["priorSecretName"] = "entra-client-secret-2026-05"
        two_name_rb["secretVersions"]["entries"][0]["id"] = (
            f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret-2026-05/{PRIOR_VER}"
        )
        two_name_rb["containerApp"]["secrets"][0]["keyVaultUrl"] = (
            f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret-2026-05"
        )
        two_name_rb["containerApp"]["revisions"][0]["secretName"] = "entra-client-secret-2026-05"
        r_two_name = verify_staged_entra_rotation(two_name_rb, now=NOW)
        self.assertTrue(r_two_name["rollbackVerified"], r_two_name["problems"])

        two_name_newer_disabled = copy.deepcopy(two_name_rb)
        two_name_newer_disabled["secretVersions"]["entries"].append(
            {
                "id": (
                    f"https://{VAULT}.vault.azure.net/secrets/"
                    "entra-client-secret-2026-05/33333333333333333333333333333333"
                ),
                "enabled": False,
                "created": "2026-11-15T10:00:00Z",
                "expires": "2027-05-15T09:00:00Z",
            }
        )
        r_two_name_bad = verify_staged_entra_rotation(two_name_newer_disabled, now=NOW)
        self.assertFalse(r_two_name_bad["rollbackVerified"])

        stale_cookie = _rotation_fixture("rollback")
        stale_cookie["healthProbes"][0]["freshTokenExchangeVerified"] = False
        r_stale = verify_staged_entra_rotation(stale_cookie, now=NOW)
        self.assertFalse(r_stale["rollbackVerified"])

    def test_enforces_kv_newest_version_resolution_and_bad_created_metadata(self) -> None:
        older_next = _rotation_fixture("post_switchover")
        older_next["secretVersions"]["entries"][1]["created"] = "2026-01-01T00:00:00Z"
        r_older = verify_staged_entra_rotation(older_next, now=NOW)
        self.assertFalse(r_older["ok"])
        self.assertFalse(r_older["versionSwitchoverVerified"])

        superseded_next = _rotation_fixture("post_switchover")
        superseded_next["secretVersions"]["entries"].append(
            {
                "id": (
                    f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret/"
                    "33333333333333333333333333333333"
                ),
                "enabled": False,
                "created": "2026-11-15T09:30:00Z",
                "expires": "2027-05-15T09:00:00Z",
            }
        )
        r_sup = verify_staged_entra_rotation(superseded_next, now=NOW)
        self.assertFalse(r_sup["ok"])
        self.assertFalse(r_sup["versionSwitchoverVerified"])

        for bad_created in (True, 0, -5, 10**20, "2026-11-15T18:00:00Z"):
            bad_ev = _rotation_fixture("post_switchover")
            bad_ev["secretVersions"]["entries"][1]["created"] = bad_created
            r_bad = verify_staged_entra_rotation(bad_ev, now=NOW)
            self.assertFalse(r_bad["ok"])
            self.assertFalse(r_bad["versionSwitchoverVerified"])

        conflict_created = _rotation_fixture("post_switchover")
        conflict_created["secretVersions"]["entries"][1]["attributes"] = {
            "created": "2026-11-15T09:06:00Z"
        }
        self.assertFalse(verify_staged_entra_rotation(conflict_created, now=NOW)["ok"])

    def test_enforces_event_bound_probe_windows_switchover_receipt_binding_and_rollback_floor(
        self,
    ) -> None:
        early_dso = _rotation_fixture("dual_secret_overlap")
        early_dso["healthProbes"][0]["firstSampleAt"] = "2026-11-15T09:02:00Z"
        early_dso["healthProbes"][0]["lastSampleAt"] = "2026-11-15T09:04:00Z"
        r_dso = verify_staged_entra_rotation(early_dso, now=NOW)
        self.assertFalse(r_dso["ok"])
        self.assertFalse(r_dso["zeroDowntimeVerified"])

        early_sw_at = _rotation_fixture("post_switchover")
        early_sw_at["containerApp"]["switchoverAt"] = "2026-11-15T09:30:00Z"
        self.assertFalse(verify_staged_entra_rotation(early_sw_at, now=NOW)["ok"])

        early_psw_probe = _rotation_fixture("post_switchover")
        early_psw_probe["healthProbes"][1]["firstSampleAt"] = "2026-11-15T10:05:00Z"
        early_psw_probe["healthProbes"][1]["lastSampleAt"] = "2026-11-15T10:07:00Z"
        self.assertFalse(verify_staged_entra_rotation(early_psw_probe, now=NOW)["ok"])

        straddling_retire = _rotation_fixture("post_retire")
        straddling_retire["healthProbes"][1]["firstSampleAt"] = "2026-11-15T11:29:59Z"
        self.assertFalse(verify_staged_entra_rotation(straddling_retire, now=NOW)["ok"])

        signed_sw = verify_staged_entra_rotation(
            _rotation_fixture("post_switchover"), now=NOW, signing_key=SIGNING_KEY_A
        )
        mismatched_sw = _rotation_fixture("post_retire")
        del mismatched_sw["credentials"]["retiredPriorCredential"]
        mismatched_sw["credentials"]["priorRetiredAt"] = "2026-11-15T11:30:00Z"
        mismatched_sw["containerApp"]["switchoverAt"] = "2026-11-15T10:12:00Z"
        mismatched_sw["priorSwitchoverReceipt"] = copy.deepcopy(signed_sw)
        self.assertFalse(
            verify_staged_entra_rotation(mismatched_sw, now=NOW, signing_key=SIGNING_KEY_A)["ok"]
        )

        early_rb = _rotation_fixture("rollback")
        early_rb["healthProbes"][0]["firstSampleAt"] = "2026-11-15T10:20:00Z"
        early_rb["healthProbes"][0]["lastSampleAt"] = "2026-11-15T10:22:00Z"
        self.assertFalse(verify_staged_entra_rotation(early_rb, now=NOW)["rollbackVerified"])

    def test_probe_batches_enforce_sample_count_span_gap_feasibility_and_post_retire_ordering(
        self,
    ) -> None:
        one_sample = _rotation_fixture("dual_secret_overlap")
        one_sample["healthProbes"][0]["totalSamples"] = 1
        self.assertFalse(verify_staged_entra_rotation(one_sample, now=NOW)["ok"])

        bool_sample = _rotation_fixture("dual_secret_overlap")
        bool_sample["healthProbes"][0]["totalSamples"] = True
        self.assertFalse(verify_staged_entra_rotation(bool_sample, now=NOW)["ok"])

        short_span = _rotation_fixture("dual_secret_overlap")
        short_span["healthProbes"][0]["lastSampleAt"] = "2026-11-15T09:10:15Z"
        self.assertFalse(verify_staged_entra_rotation(short_span, now=NOW)["ok"])

        wide_gap = _rotation_fixture("dual_secret_overlap")
        wide_gap["healthProbes"][0]["maxGapSeconds"] = 120
        self.assertFalse(verify_staged_entra_rotation(wide_gap, now=NOW)["ok"])

        impossible_math = _rotation_fixture("dual_secret_overlap")
        impossible_math["healthProbes"][0]["totalSamples"] = 3
        impossible_math["healthProbes"][0]["maxGapSeconds"] = 30
        self.assertFalse(verify_staged_entra_rotation(impossible_math, now=NOW)["ok"])

        naive_ts = _rotation_fixture("dual_secret_overlap")
        naive_ts["healthProbes"][0]["firstSampleAt"] = "2026-11-15T09:10:00"
        r_naive = verify_staged_entra_rotation(naive_ts, now=NOW)
        self.assertFalse(r_naive["ok"])
        self.assertTrue(any("firstSampleAt" in p for p in r_naive["problems"]))

        out_of_order = _rotation_fixture("post_switchover")
        out_of_order["healthProbes"][1]["firstSampleAt"] = "2026-11-15T09:12:00Z"
        out_of_order["healthProbes"][1]["lastSampleAt"] = "2026-11-15T09:14:00Z"
        self.assertFalse(verify_staged_entra_rotation(out_of_order, now=NOW)["ok"])

        stale_retire = _rotation_fixture("post_retire")
        stale_retire["healthProbes"][1]["firstSampleAt"] = "2026-11-15T11:20:00Z"
        stale_retire["healthProbes"][1]["lastSampleAt"] = "2026-11-15T11:30:00Z"
        r_stale_retire = verify_staged_entra_rotation(stale_retire, now=NOW)
        self.assertFalse(r_stale_retire["ok"])
        self.assertTrue(any("retiredAt" in p for p in r_stale_retire["problems"]))

    def test_rotation_plan_streams_secret_without_stdout_exposure(self) -> None:
        plan = rotation_plan(VAULT, "app-123")
        self.assertIn("--append", plan[0])
        self.assertIn("--query password -o tsv", plan[0])
        self.assertIn("tr -d", plan[0])
        self.assertIn("--file /dev/stdin", plan[0])
        self.assertIn("--output none", plan[0])


class AccessAuditAndLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = _inventory_fixture()
        self.policy = default_expected_caller_policy(
            _role_matrix_fixture(), _principal_map_fixture()
        )
        self.window_start = NOW - dt.timedelta(days=90)
        self.vault_scope = (
            f"/subscriptions/sub/resourceGroups/ama/providers/Microsoft.KeyVault/vaults/{VAULT}"
        )
        self.assignments = [
            {
                "principalId": OID_API,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets User",
                "scope": self.vault_scope,
            },
            {
                "principalId": OID_TOKEN,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets Officer",
                "scope": f"{self.vault_scope}/secrets/entra-token-store-sas",
            },
        ]

    def test_clean_expected_traffic_and_event_grid_notifications_have_zero_anomalies(self) -> None:
        diagnostics = [
            {
                "OperationName": "SecretGet",
                "identity_claim_oid_g": OID_API,
                "httpStatusCode_d": 200,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret/{NEXT_VER}",
                "TimeGenerated": "2026-11-10T10:00:00Z",
            },
            {
                "OperationName": "SecretSet",
                "identity_claim_oid_g": OID_TOKEN,
                "httpStatusCode_d": 200,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-token-store-sas/abcd",
                "TimeGenerated": "2026-11-11T01:00:00Z",
            },
            {
                "OperationName": "SecretNearExpiryEventGridNotification",
                "httpStatusCode_d": 200,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-token-store-sas",
                "TimeGenerated": "2026-11-12T00:00:00Z",
            },
        ]
        audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=diagnostics,
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        self.assertEqual(audit["anomalies"], [])
        self.assertEqual(audit["systemNotificationCount"], 1)
        self.assertEqual(len(audit["callerSummaries"]), 2)

    def test_flags_unexpected_forbidden_out_of_scope_anonymous_and_denied_callers(self) -> None:
        diagnostics = [
            {
                "OperationName": "SecretGet",
                "identity_claim_oid_g": OID_ROGUE,
                "httpStatusCode_d": 200,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret",
                "TimeGenerated": "2026-11-10T10:00:00Z",
            },
            {
                "OperationName": "SecretGet",
                "identity_claim_oid_g": OID_AGENTS,
                "httpStatusCode_d": 403,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret",
                "TimeGenerated": "2026-11-10T11:00:00Z",
            },
            {
                "OperationName": "SecretSet",
                "identity_claim_oid_g": OID_API,
                "httpStatusCode_d": 200,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/resident-demo-session-key",
                "TimeGenerated": "2026-11-10T12:00:00Z",
            },
            {
                "OperationName": "SecretGet",
                "httpStatusCode_d": 401,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret",
                "TimeGenerated": "2026-11-10T13:00:00Z",
            },
        ]
        assignments = [
            *self.assignments,
            {
                "principalId": OID_ROGUE,
                "principalType": "User",
                "roleDefinitionName": "Key Vault Secrets User",
                "scope": self.vault_scope,
            },
        ]
        audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=assignments,
            diagnostics=diagnostics,
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        kinds = {item["kind"] for item in audit["anomalies"]}
        self.assertIn("unmapped_rbac_principal", kinds)
        self.assertIn("unexpected_caller", kinds)
        self.assertIn("forbidden_workload_caller", kinds)
        self.assertIn("denied_access_activity", kinds)
        self.assertIn("unexpected_operation", kinds)
        self.assertIn("out_of_scope_secret", kinds)
        callers = {row["principalId"] for row in audit["callerSummaries"]}
        self.assertIn("<anonymous>", callers)

    def test_denied_401_threshold_distinguishes_single_challenge_from_repeated_failures(
        self,
    ) -> None:
        one_401 = [
            {
                "OperationName": "SecretGet",
                "identity_claim_oid_g": OID_API,
                "httpStatusCode_d": 401,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret",
                "TimeGenerated": "2026-11-10T10:00:00Z",
            }
        ]
        calm = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=one_401,
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
            denied_401_threshold=3,
        )
        self.assertEqual(calm["anomalies"], [])

        burst = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=one_401 * 3,
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
            denied_401_threshold=3,
        )
        self.assertEqual([a["kind"] for a in burst["anomalies"]], ["denied_access_activity"])

    def test_reviewer_validation_rejects_placeholders_and_automation(self) -> None:
        self.assertEqual(validate_human_reviewer("Jane Doe (@janedoe)"), "Jane Doe (@janedoe)")
        for bad in ("", "   ", "TBD", "open item", "github-actions[bot]", "copilot"):
            with self.assertRaises(SecretLifecycleError):
                validate_human_reviewer(bad)

    def test_signed_review_enforces_exact_assignment_and_anomaly_coverage(self) -> None:
        audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[
                {
                    "OperationName": "SecretGet",
                    "identity_claim_oid_g": OID_ROGUE,
                    "httpStatusCode_d": 403,
                    "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret",
                    "TimeGenerated": "2026-11-10T10:00:00Z",
                }
            ],
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        asgn_decisions = {
            row["assignmentId"]: {"decision": "keep", "rationale": "Active workload identity"}
            for row in audit["rbacAssignments"]
        }
        with self.assertRaises(SecretLifecycleError):
            create_signed_access_review_record(
                audit=audit,
                decisions={"assignments": asgn_decisions, "anomalies": {}},
                reviewer="Alex Morgan (@amorgan)",
                reviewed_at=NOW,
                review_interval_days=90,
                signing_key=SIGNING_KEY_A,
                key_id="ops-2026-q4",
            )

        anom_decisions = {
            row["anomalyId"]: {
                "disposition": "revoked",
                "rationale": "Confirmed blocked probe; IP rule verified",
            }
            for row in audit["anomalies"]
        }
        signed = create_signed_access_review_record(
            audit=audit,
            decisions={"assignments": asgn_decisions, "anomalies": anom_decisions},
            reviewer="Alex Morgan (@amorgan)",
            reviewed_at=NOW,
            review_interval_days=90,
            signing_key=SIGNING_KEY_A,
            key_id="ops-2026-q4",
        )
        self.assertEqual(signed["prevHash"], GENESIS_HASH)
        self.assertEqual(signed["auditDigest"], audit["auditDigest"])

    def test_hash_chained_ledger_verifies_key_rotation_and_detects_tampering_or_overdue_gap(
        self,
    ) -> None:
        t1 = parse_time("2026-08-20T12:00:00Z")
        t2 = parse_time("2026-11-10T12:00:00Z")
        audit1 = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=t1 - dt.timedelta(days=90),
            window_end=t1,
        )
        decisions = {
            "assignments": {
                row["assignmentId"]: {"decision": "keep", "rationale": "Required runtime role"}
                for row in audit1["rbacAssignments"]
            },
            "anomalies": {},
        }
        e1 = create_signed_access_review_record(
            audit=audit1,
            decisions=decisions,
            reviewer="Alex Morgan (@amorgan)",
            reviewed_at=t1,
            review_interval_days=90,
            signing_key=SIGNING_KEY_A,
            key_id="ops-2026-q3",
        )
        audit2 = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=t1,
            window_end=t2,
        )
        e2 = create_signed_access_review_record(
            audit=audit2,
            decisions=decisions,
            reviewer="Sam Taylor (@staylor)",
            reviewed_at=t2,
            review_interval_days=90,
            signing_key=SIGNING_KEY_B,
            key_id="ops-2026-q4",
            prev_entry=e1,
        )
        keys = {"ops-2026-q3": SIGNING_KEY_A, "ops-2026-q4": SIGNING_KEY_B}
        ok = verify_access_review_ledger(
            [e1, e2], keys, now=NOW, max_interval_days=90, expected_vault_name=VAULT
        )
        self.assertTrue(ok["intact"], ok["problems"])
        self.assertEqual(ok["entryCount"], 2)

        tampered = [copy.deepcopy(e1), copy.deepcopy(e2)]
        tampered[0]["reviewer"] = "Mallory (@mallory)"
        bad_tamper = verify_access_review_ledger(tampered, keys, now=NOW, max_interval_days=90)
        self.assertFalse(bad_tamper["intact"])
        self.assertTrue(any("entryHash mismatch" in p for p in bad_tamper["problems"]))

        wrong_vault = verify_access_review_ledger(
            [e1, e2], keys, now=NOW, max_interval_days=90, expected_vault_name="kv-other"
        )
        self.assertFalse(wrong_vault["intact"])

        overdue = verify_access_review_ledger(
            [e1, e2], keys, now=parse_time("2027-03-01T00:00:00Z"), max_interval_days=90
        )
        self.assertFalse(overdue["intact"])
        self.assertTrue(any("overdue" in p for p in overdue["problems"]))

        t_late = parse_time("2026-12-05T12:00:00Z")
        audit_late = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=t1,
            window_end=t_late,
            max_window_days=120,
        )
        e_late = create_signed_access_review_record(
            audit=audit_late,
            decisions=decisions,
            reviewer="Sam Taylor (@staylor)",
            reviewed_at=t_late,
            review_interval_days=90,
            signing_key=SIGNING_KEY_B,
            key_id="ops-2026-q4",
            prev_entry=e1,
        )
        gap_fail = verify_access_review_ledger([e1, e_late], keys, now=t_late, max_interval_days=90)
        self.assertFalse(gap_fail["intact"])
        self.assertTrue(any("schedule gap" in p for p in gap_fail["problems"]))

    def test_verify_ledger_raises_secret_exposure_error_on_embedded_secret(self) -> None:
        with self.assertRaises(SecretExposureError):
            verify_access_review_ledger(
                [{"vaultName": VAULT, "password": "raw-secret-never-store"}],
                {"ops-2026-q4": SIGNING_KEY_A},
                now=NOW,
            )

    def test_scalar_secret_guards_on_reviewer_and_rotation_plan(self) -> None:
        canary = "Bearer SECRET_CANARY_SCALAR_TOKEN_777"
        with self.assertRaises(SecretExposureError) as c1:
            validate_human_reviewer(canary)
        self.assertNotIn("SECRET_CANARY_SCALAR_TOKEN_777", str(c1.exception))
        with self.assertRaises(SecretExposureError):
            access_review(self.inventory, self.assignments, canary, NOW)
        with self.assertRaises(SecretExposureError):
            rotation_plan(canary, "app-id")
        with self.assertRaises(SecretExposureError):
            rotation_plan(VAULT, canary)

    def test_flags_excess_rbac_privilege_and_deduplicates_wrong_vault_diagnostics(self) -> None:
        overprivileged_assignments = [
            {
                "principalId": OID_API,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets Officer",
                "scope": self.vault_scope,
            },
            {
                "principalId": OID_API,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets Officer",
                "scope": self.vault_scope,
            },
        ]
        mixed_diagnostics = [
            {
                "OperationName": "SecretNearExpiryEventGridNotification",
                "httpStatusCode_d": 200,
                "id_s": "https://kv-foreign-other.vault.azure.net/secrets/entra-client-secret",
                "TimeGenerated": "2026-11-12T00:00:00Z",
            },
            {
                "OperationName": "SecretGet",
                "identity_claim_oid_g": OID_ROGUE,
                "httpStatusCode_d": 200,
                "id_s": "https://kv-foreign-other.vault.azure.net/secrets/secret-one",
                "TimeGenerated": "2026-11-12T01:00:00Z",
            },
            {
                "OperationName": "SecretGet",
                "identity_claim_oid_g": OID_ROGUE,
                "httpStatusCode_d": 200,
                "id_s": "https://kv-foreign-other.vault.azure.net/secrets/secret-two",
                "TimeGenerated": "2026-11-12T02:00:00Z",
            },
            {
                "OperationName": "SecretGet",
                "identity_claim_oid_g": OID_API,
                "httpStatusCode_d": 200,
                "TimeGenerated": "2026-11-12T03:00:00Z",
            },
        ]
        audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=overprivileged_assignments,
            diagnostics=mixed_diagnostics,
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        self.assertEqual(len(audit["rbacAssignments"]), 1)
        self.assertEqual(audit["systemNotificationCount"], 0)
        kinds = [item["kind"] for item in audit["anomalies"]]
        self.assertIn("excess_rbac_privilege", kinds)
        self.assertIn("wrong_vault_diagnostic", kinds)
        anom_ids = [item["anomalyId"] for item in audit["anomalies"]]
        self.assertEqual(len(anom_ids), len(set(anom_ids)))

        decisions = {
            "assignments": {
                row["assignmentId"]: {
                    "decision": "remove",
                    "rationale": "Downgrade API identity back to Key Vault Secrets User",
                }
                for row in audit["rbacAssignments"]
            },
            "anomalies": {
                row["anomalyId"]: {
                    "disposition": "remediated",
                    "rationale": "Scoped KQL export to target vault and removed excess role",
                }
                for row in audit["anomalies"]
            },
        }
        signed = create_signed_access_review_record(
            audit=audit,
            decisions=decisions,
            reviewer="Alex Morgan (@amorgan)",
            reviewed_at=NOW,
            review_interval_days=90,
            signing_key=SIGNING_KEY_A,
            key_id="ops-2026-q4",
        )
        self.assertEqual(signed["auditDigest"], audit["auditDigest"])

    def test_rejects_tampered_audit_digest_and_forged_review_timestamps_or_due_dates(self) -> None:
        audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[
                {
                    "OperationName": "SecretGet",
                    "identity_claim_oid_g": OID_ROGUE,
                    "httpStatusCode_d": 403,
                    "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret",
                    "TimeGenerated": "2026-11-10T10:00:00Z",
                }
            ],
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        tampered_audit = copy.deepcopy(audit)
        tampered_audit["anomalies"] = []
        base_decisions = {
            "assignments": {
                row["assignmentId"]: {"decision": "keep", "rationale": "Required runtime role"}
                for row in tampered_audit["rbacAssignments"]
            },
            "anomalies": {},
        }
        with self.assertRaises(SecretLifecycleError):
            create_signed_access_review_record(
                audit=tampered_audit,
                decisions=base_decisions,
                reviewer="Alex Morgan (@amorgan)",
                reviewed_at=NOW,
                review_interval_days=90,
                signing_key=SIGNING_KEY_A,
                key_id="ops-2026-q4",
            )

        clean_audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        with self.assertRaises(SecretLifecycleError):
            create_signed_access_review_record(
                audit=clean_audit,
                decisions=base_decisions,
                reviewer="Alex Morgan (@amorgan)",
                reviewed_at=NOW + dt.timedelta(days=95),
                review_interval_days=90,
                signing_key=SIGNING_KEY_A,
                key_id="ops-2026-q4",
            )

        future_reviewed = NOW + dt.timedelta(days=2)
        future_audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=future_reviewed - dt.timedelta(days=90),
            window_end=future_reviewed,
        )
        future_entry = create_signed_access_review_record(
            audit=future_audit,
            decisions=base_decisions,
            reviewer="Alex Morgan (@amorgan)",
            reviewed_at=future_reviewed,
            review_interval_days=90,
            signing_key=SIGNING_KEY_A,
            key_id="ops-2026-q4",
        )
        res_future = verify_access_review_ledger(
            [future_entry], {"ops-2026-q4": SIGNING_KEY_A}, now=NOW, max_interval_days=90
        )
        self.assertFalse(res_future["intact"])
        self.assertTrue(any("in the future" in p for p in res_future["problems"]))

        valid_entry = create_signed_access_review_record(
            audit=clean_audit,
            decisions=base_decisions,
            reviewer="Alex Morgan (@amorgan)",
            reviewed_at=NOW,
            review_interval_days=90,
            signing_key=SIGNING_KEY_A,
            key_id="ops-2026-q4",
        )
        forged_due = copy.deepcopy(valid_entry)
        forged_due["nextReviewDue"] = "2099-01-01"
        forged_due["reviewIntervalDays"] = True
        res_forged = verify_access_review_ledger(
            [forged_due], {"ops-2026-q4": SIGNING_KEY_A}, now=NOW, max_interval_days=90
        )
        self.assertFalse(res_forged["intact"])
        self.assertTrue(any("reviewIntervalDays" in p for p in res_forged["problems"]))

    def test_enforces_child_secret_rbac_scope_window_continuity_and_eod_due_date(self) -> None:
        bad_matrix = _role_matrix_fixture()
        bad_matrix["assignments"][0]["scope"] = "Unexpected Scope String"
        with self.assertRaises(SecretLifecycleError):
            default_expected_caller_policy(bad_matrix, _principal_map_fixture())

        mixed_case_assignments = [
            {
                "principalId": OID_API,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets User",
                "scope": (
                    f"/SUBSCRIPTIONS/sub/RESOURCEGROUPS/ama"
                    f"/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/{VAULT.upper()}/"
                ),
            },
            {
                "principalId": OID_TOKEN,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets Officer",
                "scope": (
                    f"/subscriptions/sub/resourceGroups/ama"
                    f"/providers/Microsoft.KeyVault/vaults/{VAULT}/SECRETS/ENTRA-TOKEN-STORE-SAS"
                ),
            },
        ]
        mixed_case_diag = [
            {
                "OperationName": "SecretSet",
                "identity_claim_oid_g": OID_TOKEN,
                "httpStatusCode_d": 200,
                "id_s": f"https://{VAULT}.vault.azure.net/secrets/ENTRA-TOKEN-STORE-SAS/v1",
                "TimeGenerated": "2026-11-11T01:00:00Z",
            }
        ]
        clean_mixed = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=mixed_case_assignments,
            diagnostics=mixed_case_diag,
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        self.assertEqual(clean_mixed["anomalies"], [])
        self.assertEqual(clean_mixed["callerSummaries"][0]["secrets"], ["ENTRA-TOKEN-STORE-SAS"])

        broad_and_foreign = [
            {
                "principalId": OID_TOKEN,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets Officer",
                "scope": self.vault_scope,
            },
            {
                "principalId": OID_API,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets User",
                "scope": "/subscriptions/sub/resourceGroups/ama",
            },
            {
                "principalId": OID_API,
                "principalType": "ServicePrincipal",
                "roleDefinitionName": "Key Vault Secrets User",
                "scope": (
                    "/subscriptions/sub/resourceGroups/ama"
                    "/providers/Microsoft.KeyVault/vaults/kv-foreign-other"
                ),
            },
        ]
        scoped_audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=broad_and_foreign,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        anom_by_kind = [a["kind"] for a in scoped_audit["anomalies"]]
        self.assertEqual(anom_by_kind.count("excess_rbac_privilege"), 2)
        self.assertIn("wrong_vault_rbac_scope", anom_by_kind)

        tiny_audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=NOW - dt.timedelta(seconds=1),
            window_end=NOW,
        )
        decisions = {
            "assignments": {
                row["assignmentId"]: {"decision": "keep", "rationale": "Active runtime role"}
                for row in tiny_audit["rbacAssignments"]
            },
            "anomalies": {},
        }
        with self.assertRaises(SecretLifecycleError):
            create_signed_access_review_record(
                audit=tiny_audit,
                decisions=decisions,
                reviewer="Alex Morgan (@amorgan)",
                reviewed_at=NOW,
                review_interval_days=90,
                signing_key=SIGNING_KEY_A,
                key_id="ops-2026-q4",
            )

        t1 = parse_time("2026-08-17T12:00:00Z")
        a1 = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=t1 - dt.timedelta(days=90),
            window_end=t1,
        )
        e1 = create_signed_access_review_record(
            audit=a1,
            decisions=decisions,
            reviewer="Alex Morgan (@amorgan)",
            reviewed_at=t1,
            review_interval_days=90,
            signing_key=SIGNING_KEY_A,
            key_id="ops-2026-q3",
        )

        gapped_audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[],
            expected_callers=self.policy,
            window_start=t1 + dt.timedelta(days=5),
            window_end=NOW,
        )
        with self.assertRaises(SecretLifecycleError):
            create_signed_access_review_record(
                audit=gapped_audit,
                decisions=decisions,
                reviewer="Alex Morgan (@amorgan)",
                reviewed_at=NOW,
                review_interval_days=90,
                signing_key=SIGNING_KEY_A,
                key_id="ops-2026-q4",
                prev_entry=e1,
            )

        same_day_due = parse_time(f"{e1['nextReviewDue']}T18:00:00Z")
        same_day_res = verify_access_review_ledger(
            [e1], {"ops-2026-q3": SIGNING_KEY_A}, now=same_day_due, max_interval_days=90
        )
        self.assertTrue(same_day_res["intact"], same_day_res["problems"])
        self.assertFalse(same_day_res["overdue"])

        after_due = parse_time(f"{e1['nextReviewDue']}T00:00:00Z") + dt.timedelta(days=1)
        after_due_res = verify_access_review_ledger(
            [e1], {"ops-2026-q3": SIGNING_KEY_A}, now=after_due, max_interval_days=90
        )
        self.assertFalse(after_due_res["intact"])
        self.assertTrue(after_due_res["overdue"])

    def test_merge_vault_role_assignments_preserves_root_mg_ancestors_and_child_secrets(
        self,
    ) -> None:
        vid = f"/subscriptions/sub/resourceGroups/ama/providers/Microsoft.KeyVault/vaults/{VAULT}"
        inherited = {
            "value": [
                {
                    "id": "r-root",
                    "principalId": OID_ROGUE,
                    "roleDefinitionName": "Key Vault Secrets Officer",
                    "scope": "/",
                },
                {
                    "id": "r-mg",
                    "principalId": OID_ROGUE,
                    "roleDefinitionName": "Key Vault Administrator",
                    "scope": "/providers/Microsoft.Management/managementGroups/mg-zava",
                },
                {
                    "id": "r-sub",
                    "principalId": OID_API,
                    "roleDefinitionName": "Owner",
                    "scope": "/subscriptions/sub",
                },
                {
                    "id": "r-rg",
                    "principalId": OID_API,
                    "roleDefinitionName": "Owner",
                    "scope": "/subscriptions/sub/resourceGroups/ama",
                },
                {
                    "id": "r-vault",
                    "principalId": OID_API,
                    "roleDefinitionName": "Key Vault Secrets User",
                    "scope": vid,
                },
            ]
        }
        all_rows = [
            {
                "id": "R-VAULT",
                "principalId": OID_API,
                "roleDefinitionName": "Key Vault Secrets User",
                "scope": vid,
            },
            {
                "id": "r-child-sas",
                "principalId": OID_TOKEN,
                "roleDefinitionName": "Key Vault Secrets Officer",
                "scope": f"{vid}/SECRETS/entra-token-store-sas",
            },
            {
                "id": "r-key-ignored",
                "principalId": OID_ROGUE,
                "roleDefinitionName": "Key Vault Crypto User",
                "scope": f"{vid}/keys/signing-key",
            },
            {
                "id": "r-sibling-vault",
                "principalId": OID_ROGUE,
                "roleDefinitionName": "Key Vault Secrets Officer",
                "scope": f"{vid}-dr/secrets/entra-token-store-sas",
            },
            {
                "id": "r-other-rg-same-name",
                "principalId": OID_ROGUE,
                "roleDefinitionName": "Key Vault Secrets Officer",
                "scope": (
                    f"/subscriptions/sub/resourceGroups/other-rg"
                    f"/providers/Microsoft.KeyVault/vaults/{VAULT}/secrets/entra-token-store-sas"
                ),
            },
        ]
        merged = merge_vault_role_assignments(inherited, all_rows, vault_resource_id=vid)
        self.assertEqual(
            [row["id"] for row in merged],
            ["r-root", "r-mg", "r-sub", "r-rg", "r-vault", "r-child-sas"],
        )

        with self.assertRaises(SecretLifecycleError):
            merge_vault_role_assignments(
                [
                    {
                        "id": "r-wrong-sub",
                        "principalId": OID_API,
                        "roleDefinitionName": "Owner",
                        "scope": "/subscriptions/other-sub",
                    }
                ],
                [],
                vault_resource_id=vid,
            )

    def test_sanitizes_unlabelled_canary_across_all_problem_and_error_paths(self) -> None:
        canary = "UNLABELLED_CANARY_XYZZY_999"
        rot = _rotation_fixture("post_switchover")
        rot["stage"] = canary
        rot["credentials"]["priorKeyId"] = f"bad!{canary}"
        rot["credentials"]["nextKeyId"] = f"next!{canary}"
        rot["healthProbes"][0]["stage"] = canary
        rot["healthProbes"][0]["maxGapSeconds"] = canary
        rot["healthProbes"][0]["healthzStatus"] = canary
        rot["healthProbes"][0]["anonymousApiStatus"] = canary
        rot["healthProbes"][0]["signInRedirectStatus"] = canary
        rot["healthProbes"][1]["authenticatedApiStatus"] = canary
        rot_res = verify_staged_entra_rotation(rot, now=NOW)
        self.assertFalse(rot_res["ok"])
        self.assertNotIn(canary, " | ".join(rot_res["problems"]))

        rev_probs = review_status(
            {
                "reviewer": "Jane Doe (@janedoe)",
                "assignments": [{"principalId": f"bad!{canary}", "decision": canary}],
                "nextReviewDue": canary,
            },
            NOW,
        )
        self.assertNotIn(canary, " | ".join(rev_probs))

        vid = f"/subscriptions/sub/resourceGroups/ama/providers/Microsoft.KeyVault/vaults/{VAULT}"
        with self.assertRaises(SecretLifecycleError) as m_ctx:
            merge_vault_role_assignments(
                [{"id": "r1", "principalId": OID_API, "scope": f"/bad/{canary}"}],
                [],
                vault_resource_id=vid,
            )
        self.assertNotIn(canary, str(m_ctx.exception))

        for bad_code in (True, "NaN", "Infinity"):
            with self.assertRaises(SecretLifecycleError):
                audit_keyvault_data_plane_access(
                    vault_name=VAULT,
                    inventory=self.inventory,
                    assignments=self.assignments,
                    diagnostics=[
                        {
                            "OperationName": "SecretGet",
                            "identity_claim_oid_g": OID_API,
                            "httpStatusCode_d": bad_code,
                            "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret",
                            "TimeGenerated": "2026-11-10T10:00:00Z",
                        }
                    ],
                    expected_callers=self.policy,
                    window_start=self.window_start,
                    window_end=NOW,
                )

        audit = audit_keyvault_data_plane_access(
            vault_name=VAULT,
            inventory=self.inventory,
            assignments=self.assignments,
            diagnostics=[
                {
                    "OperationName": "SecretGet",
                    "identity_claim_oid_g": OID_ROGUE,
                    "httpStatusCode_d": 403,
                    "id_s": f"https://{VAULT}.vault.azure.net/secrets/entra-client-secret",
                    "TimeGenerated": "2026-11-10T10:00:00Z",
                }
            ],
            expected_callers=self.policy,
            window_start=self.window_start,
            window_end=NOW,
        )
        with self.assertRaises(SecretLifecycleError) as s_dec:
            create_signed_access_review_record(
                audit=audit,
                decisions={
                    "assignments": {
                        r["assignmentId"]: {"decision": canary, "rationale": "x"}
                        for r in audit["rbacAssignments"]
                    },
                    "anomalies": {
                        a["anomalyId"]: {"disposition": "remediated", "rationale": "x"}
                        for a in audit["anomalies"]
                    },
                },
                reviewer="Jane Doe (@janedoe)",
                reviewed_at=NOW,
                review_interval_days=90,
                signing_key=SIGNING_KEY_A,
                key_id="ops-q4",
            )
        self.assertNotIn(canary, str(s_dec.exception))

        valid_entry = create_signed_access_review_record(
            audit=audit,
            decisions={
                "assignments": {
                    r["assignmentId"]: {"decision": "keep", "rationale": "x"}
                    for r in audit["rbacAssignments"]
                },
                "anomalies": {
                    a["anomalyId"]: {"disposition": "remediated", "rationale": "x"}
                    for a in audit["anomalies"]
                },
            },
            reviewer="Jane Doe (@janedoe)",
            reviewed_at=NOW,
            review_interval_days=90,
            signing_key=SIGNING_KEY_A,
            key_id="ops-q4",
        )
        tampered = copy.deepcopy(valid_entry)
        tampered["signingKeyId"] = f"bad!{canary}"
        tampered["nextReviewDue"] = "2099-01-01"
        tampered["assignments"][0]["decision"] = canary
        tampered["anomalyDispositions"][0]["disposition"] = canary
        led_res = verify_access_review_ledger(
            [tampered],
            {f"bad!{canary}": b"short"},
            now=NOW,
            expected_vault_name=f"bad!{canary}",
        )
        self.assertFalse(led_res["intact"])
        self.assertNotIn(canary, " | ".join(led_res["problems"]))


INVENTORY_PATH = Path(__file__).resolve().parents[3] / "infra" / "secret-inventory.json"
CHECK_NOW = parse_time("2026-11-15T12:00:00Z")


def _inventory(interval: int = 30, alert: int = 7) -> dict[str, Any]:
    return {
        "secrets": [
            {
                "name": "s1",
                "owner": "owner",
                "rotationIntervalDays": interval,
                "expiryAlertDays": alert,
            }
        ]
    }


def _listed(
    expires: str | None, updated: str = "2026-11-10T12:00:00Z", enabled: bool = True
) -> list[dict[str, Any]]:
    attrs: dict[str, Any] = {"enabled": enabled, "updated": updated}
    if expires is not None:
        attrs["expires"] = expires
    return [{"name": "s1", "attributes": attrs}]


def _kinds(findings: list[tuple[str, str, str]]) -> list[str]:
    return [kind for _, kind, _ in findings]


class CheckSecretsTests(unittest.TestCase):
    def test_repository_inventory_names_owner_interval_and_alert(self) -> None:
        inventory: dict[str, Any] = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
        self.assertEqual(validate_inventory(inventory), [])
        self.assertGreaterEqual(len(inventory["secrets"]), 1)
        for entry in inventory["secrets"]:
            self.assertTrue(entry["owner"])
            self.assertGreater(entry["rotationIntervalDays"], 0)
            self.assertGreater(entry["expiryAlertDays"], 0)

    def test_expiry_alert_window_boundary(self) -> None:
        inv = _inventory(alert=7)
        inside = check_secrets(inv, _listed("2026-11-22T12:00:00Z"), CHECK_NOW)
        self.assertEqual(_kinds(inside), ["expiring"])
        outside = check_secrets(inv, _listed("2026-11-23T12:00:00Z"), CHECK_NOW)
        self.assertEqual(outside, [])

    def test_expired_and_missing_expiry_are_findings(self) -> None:
        inv = _inventory()
        self.assertEqual(
            _kinds(check_secrets(inv, _listed("2026-11-01T12:00:00Z"), CHECK_NOW)), ["expired"]
        )
        self.assertEqual(_kinds(check_secrets(inv, _listed(None), CHECK_NOW)), ["no-expiry"])

    def test_rotation_interval_boundary(self) -> None:
        inv = _inventory(interval=30)
        due = check_secrets(inv, _listed("2027-06-01T00:00:00Z", "2026-10-16T12:00:00Z"), CHECK_NOW)
        self.assertEqual(due, [])
        overdue = check_secrets(
            inv, _listed("2027-06-01T00:00:00Z", "2026-10-15T11:00:00Z"), CHECK_NOW
        )
        self.assertEqual(_kinds(overdue), ["rotation-overdue"])

    def test_disabled_missing_and_uninventoried_secrets(self) -> None:
        inv = _inventory()
        disabled = check_secrets(inv, _listed("2027-06-01T00:00:00Z", enabled=False), CHECK_NOW)
        self.assertEqual(_kinds(disabled), ["disabled"])
        extra = [*_listed("2027-06-01T00:00:00Z"), {"name": "stray", "attributes": {}}]
        self.assertEqual(_kinds(check_secrets(inv, extra, CHECK_NOW)), ["uninventoried"])
        self.assertEqual(_kinds(check_secrets(inv, [], CHECK_NOW)), ["missing"])

    def test_inventory_without_owner_is_reported(self) -> None:
        bad = {"secrets": [{"name": "x", "rotationIntervalDays": 1, "expiryAlertDays": 1}]}
        self.assertEqual(validate_inventory(bad), ["x: missing owner"])


if __name__ == "__main__":
    unittest.main()
