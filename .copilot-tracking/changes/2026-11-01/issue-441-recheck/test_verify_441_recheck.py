"""Focused contracts for the issue 441 recheck verifier."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "verify_recheck", Path(__file__).with_name("verify-441-recheck.py")
)
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


class CustodyTests(unittest.TestCase):
    def run_custody(self, content, recorded):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_bytes(content)
            custody = root / "custody.json"
            custody.write_text(
                json.dumps({"base": "x", "files": {"a.md": {"sha256": recorded}}})
            )
            with patch.object(v, "CUSTODY", custody), patch.object(v, "DRAFT", root):
                return v.check_custody()

    def test_matching_hash_passes(self):
        digest = hashlib.sha256(b"abc").hexdigest()
        self.assertTrue(self.run_custody(b"abc", digest)["ok"])

    def test_mismatched_hash_fails(self):
        result = self.run_custody(b"abc", "0" * 64)
        self.assertFalse(result["ok"])
        self.assertEqual(result["mismatch"], ["a.md"])


class DefinitionTests(unittest.TestCase):
    def test_only_shall_rows_count_and_duplicates_detected(self):
        text = (
            "| FR-001 | The system shall x |\n"
            "| FR-001 | The system shall y |\n"
            "| FR-002 | matrix row |\n"
        )
        found = v.definitions(text, r"^\| (FR-\d{3}) \|")
        self.assertEqual(found, ["FR-001", "FR-001"])
        self.assertEqual(sorted({x for x in found if found.count(x) > 1}), ["FR-001"])


class PolicyTests(unittest.TestCase):
    def policy(self, brd_text, prd_text):
        with tempfile.TemporaryDirectory() as tmp:
            brd, prd = Path(tmp, "b.md"), Path(tmp, "p.md")
            brd.write_text(brd_text)
            prd.write_text(prd_text)
            with patch.object(v, "BRD", brd), patch.object(v, "PRD", prd):
                return v.check_policy()

    def test_passing_policy(self):
        brd = (
            "| FR-044 | named per-output human review is required; "
            "explicitly enabled under RULE-028 |\n"
            "| RULE-028 | OD-53 named per-message human approval is required |\n"
            "OD-52 OD-53 OD-54 OD-55\n"
        )
        self.assertTrue(self.policy(brd, "per-message OD-52 OD-53 OD-54 OD-55")["ok"])

    def test_missing_gate_fails(self):
        brd = "| FR-044 | review |\n| RULE-028 | none |\n"
        self.assertFalse(self.policy(brd, "")["ok"])


class AdrAndFreshnessTests(unittest.TestCase):
    def test_adr_branch_change_fails(self):
        with patch.object(v, "git", return_value="docs/adrs/0007-x.md\n"):
            self.assertFalse(v.check_adr()["no_adr_change_on_branch"])

    def test_dirty_documents_fail_freshness(self):
        def fake(*args):
            if args[0] == "rev-parse":
                return "abc\n"
            if args[0] == "merge-base":
                return ""
            if args[0] == "status":
                return " M docs/prds/x.md\n"
            return ""

        with patch.object(v, "git", side_effect=fake):
            result = v.check_freshness()
        self.assertFalse(result["ok"])
        self.assertTrue(result["descends_from_origin_main"])


if __name__ == "__main__":
    unittest.main()
