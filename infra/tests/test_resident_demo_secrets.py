"""Offline tests for the owner-local resident demo secret helper (fake fixtures, fake CLI)."""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import threading
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import credential_arm as CREDENTIAL
import resident_demo_secrets as HELPER
from zava_forward.core import resident_showcase as rs

SUB = "11111111-2222-3333-4444-555555555555"
ROOT = f"/subscriptions/{SUB}/resourceGroups/ama"
VAULT = ROOT + "/providers/Microsoft.KeyVault/vaults/kv-cutovertest-rzsrg"
NOW = datetime(2026, 10, 26, 7, 30, tzinfo=UTC)
EXPIRES = "2026-10-26T11:00:00Z"
VERIFIER = rs.make_verifier("Fake-Fixture-Value-Only-0123456789-xyz", n=2**14)
KEY_BYTES = b"K" * 32
KEY = "S0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0s"
NAMES = ("resident-demo-password-verifier", "resident-demo-session-key")


class FakeCli:
    def __init__(self, body_directory: Path):
        self.subscription: str | None = None
        self.deadline: float | None = None
        self.body_directory = body_directory
        self.calls: list[list[str]] = []
        self.writes: list[tuple[str, dict]] = []
        self.changes = lambda ids: [{"changeType": "Create", "resourceId": i} for i in ids]
        self.rest_error: Exception | None = None
        self.template: dict | None = None
        self.parameter_files_seen = 0

    def call(self, args: list[str]):
        self.calls.append(args)
        template = json.loads(Path(args[args.index("--template-file") + 1]).read_text())
        parameters = json.loads(Path(args[args.index("--parameters") + 1][1:]).read_text())
        self.parameter_files_seen += bool(parameters)
        self.template = template
        ids = [VAULT + "/secrets/" + r["name"].split("/")[1] for r in template["resources"]]
        return {"status": "Succeeded", "changes": self.changes(ids)}

    def rest(self, url: str, *, method: str = "GET", body: dict | None = None):
        if self.rest_error:
            raise self.rest_error
        path = url.split("management.azure.com", 1)[1].split("?")[0]
        if method == "PUT":
            self.writes.append((path, body or {}))
            return {}
        if path.lower() == VAULT.lower():
            return {
                "id": VAULT,
                "properties": {"publicNetworkAccess": "Disabled", "enableRbacAuthorization": True},
            }
        if path.endswith("/secrets"):
            return {}
        if "/deployments/" in path:
            return {"properties": {"provisioningState": "Succeeded"}}
        name = path.rsplit("/", 1)[1]
        expires = int(datetime.fromisoformat(EXPIRES.replace("Z", "+00:00")).timestamp())
        return {
            "id": path,
            "properties": {
                "attributes": {"enabled": True, "exp": expires},
                "secretUri": f"https://kv-cutovertest-rzsrg.vault.azure.net/secrets/{name}",
            },
        }


class HelperCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.profile = self.home / "profile"
        self.profile.mkdir(mode=0o700)
        self.cli = FakeCli(self.profile)
        self.addCleanup(patch.stopall)
        patch.object(HELPER.secrets, "token_bytes", return_value=KEY_BYTES).start()
        patch.object(CREDENTIAL.time, "sleep").start()

    def run_helper(
        self, *extra, apply=False, interactive=True, hidden=VERIFIER, typed=None, expires=EXPIRES
    ):
        argv = [
            "x",
            "--subscription",
            SUB,
            "--expires",
            expires,
            "--tenant-profile",
            str(self.profile),
            *extra,
        ]
        if apply:
            argv.append("--apply")
        out, err = io.StringIO(), io.StringIO()
        answer = typed if typed is not None else HELPER.confirmation(SUB, expires)
        code = HELPER.main(
            argv,
            interactive,
            out,
            err,
            prompt=lambda _: hidden,
            ask=lambda _: answer,
            now=lambda: NOW,
            make_cli=lambda _: self.cli,
        )
        self.output = out.getvalue() + err.getvalue()
        return code

    def assert_no_leak(self):
        for secret in (VERIFIER, KEY, KEY_BYTES.decode()):
            self.assertNotIn(secret, self.output)
            self.assertNotIn(secret, json.dumps(self.cli.calls))
            self.assertNotIn(secret, json.dumps(dict(os.environ)))
        self.assertEqual(list(self.profile.iterdir()), [])

    def private_file(self, text=VERIFIER, mode=0o600):
        path = self.home / "verifier.txt"
        path.write_text(text)
        path.chmod(mode)
        return path


class DryRunAndApply(HelperCase):
    def test_dry_run_default_sends_no_value_and_writes_nothing(self):
        self.assertEqual(self.run_helper(), 0)
        self.assertEqual((self.cli.writes, self.cli.calls), ([], []))
        self.assertIn("nothing written", self.output)
        self.assert_no_leak()

    def test_apply_writes_exactly_the_two_fixed_secrets_in_one_secure_deployment(self):
        self.assertEqual(self.run_helper(apply=True), 0)
        self.assertEqual(len(self.cli.writes), 1)
        template = self.cli.template
        assert template is not None
        self.assertEqual(
            [r["name"] for r in template["resources"]], [f"kv-cutovertest-rzsrg/{n}" for n in NAMES]
        )
        self.assertTrue(all(p["type"] == "secureString" for p in template["parameters"].values()))
        self.assertNotIn("outputs", template)
        self.assertEqual(self.cli.parameter_files_seen, 1)
        for name in NAMES:
            self.assertIn(f"stored {name}", self.output)
        self.assert_no_leak()
        self.assertIn("/deployments/resident-demo-", self.cli.writes[0][0])

    def test_apply_needs_terminal_and_exact_scoped_confirmation(self):
        self.assertEqual(self.run_helper(apply=True, interactive=False), 1)
        self.assertEqual(self.run_helper(apply=True, typed="yes"), 1)
        self.assertEqual(
            self.run_helper(apply=True, typed=HELPER.confirmation(SUB, "2026-10-26T10:00:00Z")), 1
        )
        self.assertEqual((self.cli.writes, self.cli.calls), ([], []))
        self.assert_no_leak()

    def test_verifier_file_path_is_accepted(self):
        self.assertEqual(
            self.run_helper("--verifier-file", str(self.private_file()), hidden="unused"), 0
        )
        self.assert_no_leak()


class Refusals(HelperCase):
    def test_expiry_is_mandatory_future_and_not_past_the_authority_limit(self):
        for bad in (
            "",
            "2026-10-26T12:00:01Z",
            "2026-10-26T07:00:00Z",
            "2026-10-26T11:00:00",
            "tomorrow",
            "2027-01-01T00:00:00Z",
        ):
            self.assertEqual(self.run_helper(apply=True, expires=bad), 1, bad)
        self.assertEqual((self.cli.writes, self.cli.calls), ([], []))
        self.assertEqual(self.run_helper(expires="2026-10-26T12:00:00Z"), 0)

    def test_expiry_is_rechecked_immediately_before_the_write(self):
        clock = iter([NOW, datetime(2026, 10, 26, 13, 0, tzinfo=UTC)])
        out, err = io.StringIO(), io.StringIO()
        code = HELPER.main(
            [
                "x",
                "--subscription",
                SUB,
                "--expires",
                EXPIRES,
                "--tenant-profile",
                str(self.profile),
                "--apply",
            ],
            True,
            out,
            err,
            prompt=lambda _: VERIFIER,
            ask=lambda _: HELPER.confirmation(SUB, EXPIRES),
            now=lambda: next(clock),
            make_cli=lambda _: self.cli,
        )
        self.assertEqual(code, 1)
        self.assertEqual(self.cli.writes, [])

    def test_verifier_file_must_be_private_regular_unlinked_and_small(self):
        good = self.private_file()
        link = self.home / "link.txt"
        link.symlink_to(good)
        loose = self.home / "loose.txt"
        loose.write_text(VERIFIER)
        loose.chmod(0o644)
        big = self.home / "big.txt"
        big.write_text("x" * 2000)
        big.chmod(0o600)
        for path in (link, loose, big, self.home, self.home / "missing.txt"):
            self.assertEqual(self.run_helper("--verifier-file", str(path)), 1, path)
            self.assertNotIn(VERIFIER, self.output)
        repo_file = Path(HELPER.setup.REPO) / "pyproject-like-private.txt"
        self.assertEqual(self.run_helper("--verifier-file", str(repo_file)), 1)
        self.assertEqual(self.cli.calls, [])

    def test_fifo_verifier_file_is_refused_without_blocking(self):
        fifo = self.home / "verifier.fifo"
        os.mkfifo(fifo, 0o600)
        done: list[int] = []
        worker = threading.Thread(
            target=lambda: done.append(self.run_helper("--verifier-file", str(fifo))), daemon=True
        )
        worker.start()
        worker.join(5)
        self.assertFalse(worker.is_alive(), "helper blocked on a FIFO")
        self.assertEqual(done, [1])
        self.assertEqual(self.cli.calls, [])

    def test_malformed_or_plain_password_values_are_refused_without_echo(self):
        for bad in ("", "Plain-Looking-Password-123!", "scrypt$1$1$1$a$b"):
            self.assertEqual(self.run_helper(hidden=bad), 1)
            if bad:
                self.assertNotIn(bad, self.output)
        self.assertEqual(self.cli.calls, [])

    def test_bad_subscription_and_unknown_arguments_do_not_echo_values(self):
        self.assertEqual(
            HELPER.main(
                ["x", "--subscription", "nope", "--expires", EXPIRES],
                True,
                io.StringIO(),
                io.StringIO(),
            ),
            1,
        )
        err = io.StringIO()
        self.assertEqual(HELPER.main(["x", "Leaked-Secret-On-Argv"], True, io.StringIO(), err), 2)
        self.assertNotIn("Leaked-Secret-On-Argv", err.getvalue())

    def test_whatif_must_prove_exactly_the_two_new_secrets(self):
        def first(ids):
            return [{"changeType": "Create", "resourceId": ids[0]}]

        def modify(ids):
            return [{"changeType": "Modify", "resourceId": i} for i in ids]

        def outside(ids):
            return [
                *({"changeType": "Create", "resourceId": i} for i in ids),
                {"changeType": "Create", "resourceId": "/subscriptions/x/resourceGroups/other/a"},
            ]

        def extra(ids):
            return [
                {"changeType": "Create", "resourceId": ids[0]},
                {"changeType": "Create", "resourceId": ids[0]},
            ]

        for mutate in (first, modify, outside, extra):
            self.cli.changes = mutate
            self.assertEqual(self.run_helper(apply=True), 1)
            self.assertEqual(self.cli.writes, [])
            self.assert_no_leak()

    def test_service_failure_is_sanitized_and_never_silent_success(self):
        self.cli.rest_error = RuntimeError(f"service said {VERIFIER} {KEY}")
        self.assertEqual(self.run_helper(apply=True), 1)
        self.assertNotIn(VERIFIER, self.output)
        self.assertNotIn(KEY, self.output)
        self.assertIn("Failed", self.output)

    def test_vault_and_scope_are_fixed(self):
        self.assertEqual(CREDENTIAL.RESIDENT_VAULT, "kv-cutovertest-rzsrg")
        self.cli.subscription = "99999999-2222-3333-4444-555555555555"
        app = {"id": ROOT + "/providers/x/y"}
        with self.assertRaises(CREDENTIAL.CredentialError):
            CREDENTIAL.store_resident_demo(self.cli, app, VERIFIER, KEY, EXPIRES)
        self.assertEqual(self.cli.writes, [])


class EmployeePathUnchanged(HelperCase):
    def test_entra_store_still_refuses_resident_names_and_accepts_its_own(self):
        self.cli.subscription = SUB
        app = {"id": ROOT + "/providers/x/y"}
        for name in NAMES:
            with self.assertRaises(CREDENTIAL.CredentialError):
                CREDENTIAL.store(self.cli, app, "kv-cutovertest-rzsrg", name, "v", EXPIRES)
        entra = "entra-" + "a" * 32 + "-" + "b" * 12
        self.assertIn(
            entra, CREDENTIAL.store(self.cli, app, "kv-cutovertest-rzsrg", entra, "v", EXPIRES)
        )
        self.assertEqual(list(self.cli.template["parameters"]), ["credential"])

    def test_pair_values_must_differ_and_exist(self):
        self.cli.subscription = SUB
        app = {"id": ROOT + "/providers/x/y"}
        for pair in (("", KEY), (VERIFIER, ""), (KEY, KEY)):
            with self.assertRaises(CREDENTIAL.CredentialError):
                CREDENTIAL.store_resident_demo(self.cli, app, *pair, EXPIRES)


if __name__ == "__main__":
    unittest.main()
