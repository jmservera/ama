"""Behaviour tests for tools/check-repo-secrets.py (Issue #138)."""

import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "check_repo_secrets", Path(__file__).with_name("check-repo-secrets.py")
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)

# Built by concatenation so this file never contains a secret-shaped literal.
POSITIVES = {
    "private-key": "-----BEGIN " + "RSA PRIVATE KEY-----",
    "aws-access-key-id": "AKIA" + "ABCDEFGHIJKLMNOP",
    "github-token": "gh" + "p_" + "a" * 36,
    "azure-storage-key": "Account" + "Key=" + "A" * 24 + "==",
    "sas-signature": "https://x.blob.example/c?sv=1&" + "sig=" + "a" * 40,
    "jwt": "eyJ" + "a" * 20 + ".eyJ" + "b" * 20 + "." + "c" * 12,
    "connection-string-password": "Server=x;Pass" + "word=Hunter2Hunter2;",
}


class SecretScanTests(unittest.TestCase):
    def test_every_rule_detects_its_constructed_positive(self):
        self.assertEqual(set(POSITIVES), set(checker.RULES))
        for rule, value in POSITIVES.items():
            with self.subTest(rule=rule):
                found = checker.scan_text("docs/x.md", f"before\n{value}\n")
                self.assertEqual(found, [("docs/x.md", 2, rule)])

    def test_placeholders_and_expressions_are_not_flagged(self):
        text = "Password=${{ secrets.X }};\npassword=<redacted>;\nclient-id: ${{ vars.ID }}\n"
        self.assertEqual(checker.scan_text("a.yml", text), [])

    def test_allowlist_is_exact_to_path_and_rule(self):
        path, rule = sorted(checker.ALLOWLIST)[0]
        self.assertEqual(checker.scan_text(path, POSITIVES[rule]), [])
        self.assertTrue(checker.scan_text("elsewhere.py", POSITIVES[rule]))

    def test_tracked_repository_has_no_findings(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(checker.scan_repo(root), [])


if __name__ == "__main__":
    unittest.main()
