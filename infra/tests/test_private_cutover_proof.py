"""Offline safety and exact-outcome contracts for the in-VNet proof runner."""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

SPEC = importlib.util.spec_from_file_location(
    "private_cutover_proof", Path(__file__).parents[1] / "scripts/private-cutover-proof.py"
)
proof = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(proof)


class PrivateProofTests(unittest.TestCase):
    def test_unknown_database_is_rejected_before_application_queries(self):
        db = MagicMock()
        db.execute.return_value.fetchall.return_value = [("cases",)]
        with self.assertRaisesRegex(RuntimeError, "Unrecognized database"):
            proof.preflight(db, {"cases"})
        self.assertEqual(db.execute.call_count, 1)
        self.assertIn("sys.tables", db.execute.call_args.args[0])

    def test_preflight_empty_owned_and_wrong_sentinel(self):
        db = MagicMock()
        db.execute.return_value.fetchall.return_value = []
        self.assertFalse(proof.preflight(db, {"cases"}))
        db.execute.return_value.fetchall.return_value = [("cases",), (proof.SENTINEL,)]
        db.execute.return_value.fetchone.return_value = (proof.PROOF,)
        self.assertTrue(proof.preflight(db, {"cases"}))
        db.execute.return_value.fetchone.return_value = ("different-proof",)
        with self.assertRaises(RuntimeError):
            proof.preflight(db, {"cases"})

    def test_api_assistant_startup_tables_are_known_but_unknown_tables_still_fail(self):
        allowed = proof.allowed_tables()
        self.assertIn("assistant_tasks", allowed)
        self.assertIn("assistant_releases", allowed)
        db = MagicMock()
        db.execute.return_value.fetchall.return_value = [
            (table,) for table in allowed | {proof.SENTINEL}
        ]
        db.execute.return_value.fetchone.return_value = (proof.PROOF,)
        self.assertTrue(proof.preflight(db, allowed))
        db.reset_mock()
        db.execute.return_value.fetchall.return_value.append(("unexpected_private_table",))
        with self.assertRaises(RuntimeError):
            proof.preflight(db, allowed)
        self.assertEqual(db.execute.call_count, 1)

    def test_private_dns_rejects_vm_and_public_networks(self):
        for address in ("172.16.0.1", "20.0.0.1", "127.0.0.1"):
            with patch.object(
                proof.socket, "getaddrinfo", return_value=[(0, 0, 0, "", (address, 443))]
            ):
                with self.assertRaises(ValueError):
                    proof.private_dns("example.test")
        with patch.object(
            proof.socket, "getaddrinfo", return_value=[(0, 0, 0, "", ("10.40.4.5", 443))]
        ):
            self.assertEqual(proof.private_dns("example.test"), ["10.40.4.5"])

    def test_grant_sid_idempotence_and_input_rejection(self):
        db = MagicMock()
        client = "00112233-4455-6677-8899-aabbccddeeff"
        db.execute.return_value.fetchone.return_value = ("0x33221100554477668899aabbccddeeff",)
        for _ in range(2):
            proof.grant(db, "id-cutover-test-api", client, ("db_datareader",))
        self.assertIn("IF NOT EXISTS", db.execute.call_args_list[0].args[0])
        self.assertIn(
            "SID=0x33221100554477668899aabbccddeeff", db.execute.call_args_list[0].args[0]
        )
        for name in ("arbitrary", "id-cutover-test-api']; DROP TABLE staff;--"):
            with self.assertRaises(ValueError):
                proof.grant(db, name, client, ())
        db.execute.return_value.fetchone.return_value = ("0x00",)
        with self.assertRaisesRegex(RuntimeError, "SID mismatch"):
            proof.grant(db, "id-cutover-test-api", client, ())

    def test_fixture_is_nonempty_unbound_and_survives_seedless_reopen(self):
        from zava_forward.core.sqlstore import SqlStore

        fixture = proof.fixture()
        self.assertEqual(fixture["staff"], [])
        self.assertEqual(len(fixture["cases"]), 1)
        with tempfile.TemporaryDirectory() as directory:
            seed, db = Path(directory) / "seed.json", str(Path(directory) / "state.sqlite")
            seed.write_text(json.dumps(fixture))
            first = SqlStore(str(seed), db)
            first.db.close()
            seed.unlink()
            reopened = SqlStore(str(seed), db)
            try:
                self.assertEqual(reopened.cases[proof.CASE_ID]["reason"], proof.PROOF)
                self.assertFalse(reopened.staff)
            finally:
                reopened.db.close()

    def test_owned_partial_initialization_retains_a_seed_for_safe_retry(self):
        from zava_forward.core import mssqlstore

        def store(seed, **kwargs):
            self.assertTrue(Path(seed).exists())
            result = MagicMock()
            result.cases = {proof.CASE_ID: {"reason": proof.PROOF}}
            result.staff = {}
            return result

        with (
            patch.dict(
                "os.environ",
                {
                    "ZF_SQL_SERVER": "sql.example.test",
                    "ZF_SQL_DATABASE": "proof",
                    "ZF_SQL_CLIENT_ID": "explicit-identity",
                    "PROOF_API_CLIENT_ID": "00112233-4455-6677-8899-aabbccddeeff",
                    "PROOF_IMPORT_CLIENT_ID": "00112233-4455-6677-8899-aabbccddeeff",
                },
            ),
            patch.object(proof, "private_dns"),
            patch.object(proof, "preflight", return_value=True),
            patch.object(proof, "grant"),
            patch.object(proof, "emit"),
            patch.object(mssqlstore, "_Conn"),
            patch.object(mssqlstore, "MssqlStore", side_effect=store),
        ):
            proof.sql_probe(True)

    def test_smoke_requires_exact_codes_and_checks_forged_headers(self):
        with (
            patch.object(proof, "private_dns", return_value=["10.40.0.1"]),
            patch.object(proof, "http_status", side_effect=[200, 401, 401, 401]) as status,
            patch.object(proof, "emit"),
        ):
            proof.smoke("https://test.internal.example.azurecontainerapps.io")
            self.assertIn("X-MS-CLIENT-PRINCIPAL", status.call_args.args[1])
        with (
            patch.object(proof, "private_dns"),
            patch.object(proof, "http_status", return_value=302),
            patch.object(proof, "emit"),
        ):
            with self.assertRaises(RuntimeError):
                proof.smoke("https://test.internal.example.azurecontainerapps.io")

    def test_smoke_rejects_arbitrary_origins_before_request(self):
        for url in (
            "http://test.azurecontainerapps.io",
            "https://example.com",
            "https://test.azurecontainerapps.io/api",
            "https://user@test.azurecontainerapps.io",
        ):
            with self.subTest(url=url), patch.object(proof, "http_status") as status:
                with self.assertRaises(ValueError):
                    proof.smoke(url)
                status.assert_not_called()

    def test_error_output_does_not_include_raw_exception(self):
        with (
            patch.object(sys, "argv", ["proof", "verify"]),
            patch.object(proof, "sql_probe", side_effect=RuntimeError("secret-token")),
            patch.object(proof, "emit") as emit,
        ):
            self.assertEqual(proof.main(), 1)
            self.assertNotIn("secret-token", str(emit.call_args))


if __name__ == "__main__":
    unittest.main()
