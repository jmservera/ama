from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "deployed_hardening.py"
spec = importlib.util.spec_from_file_location("deployed_hardening", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

HARDENED_STATUS = """Uid:\t10001\t10001\t10001\t10001
CapInh:\t0000000000000000
CapPrm:\t0000000000000000
CapEff:\t0000000000000000
CapBnd:\t00000000a80425fb
CapAmb:\t0000000000000000
NoNewPrivs:\t1
"""
RW_MOUNTS = "overlay / overlay rw,relatime,redirect_dir=on 0 0\n/dev/sda2 /tmp ext4 rw 0 0\n"


def app(name: str, env: list[dict[str, str]]) -> dict[str, object]:
    return {"name": name, "properties": {"template": {"containers": [{"env": env}]}}}


class SpecTests(unittest.TestCase):
    def test_only_enforced_passes(self) -> None:
        on = app("a", [{"name": "ZF_CONTAINER_HARDENING", "value": "enforced"}])
        off = app("b", [{"name": "ZF_CONTAINER_HARDENING", "value": "off"}])
        missing = app("c", [{"name": "OTHER", "value": "enforced"}])
        self.assertTrue(module.audit_specs([on])["all_enforced"])
        report = module.audit_specs([on, off, missing])
        self.assertFalse(report["all_enforced"])
        self.assertEqual([r["enforced"] for r in report["containers"]], [True, False, False])

    def test_empty_input_fails(self) -> None:
        self.assertFalse(module.audit_specs([])["all_enforced"])


class StatusTests(unittest.TestCase):
    def test_live_receipt_passes_and_reports_read_write_root(self) -> None:
        report = module.audit_status(HARDENED_STATUS, RW_MOUNTS)
        self.assertTrue(report["all_passed"])
        self.assertEqual(report["cap_bounding_set"], "00000000a80425fb")
        self.assertFalse(report["root_filesystem"]["read_only"])
        self.assertIn("rw", report["root_filesystem"]["options"])

    def test_each_weakness_fails(self) -> None:
        cases = {
            "non_root": HARDENED_STATUS.replace("10001\t10001\t10001\t10001", "0\t0\t0\t0"),
            "no_new_privs": HARDENED_STATUS.replace("NoNewPrivs:\t1", "NoNewPrivs:\t0"),
            "CapInh_empty": HARDENED_STATUS.replace(
                "CapInh:\t0000000000000000", "CapInh:\t00000000a80425fb"
            ),
            "CapEff_empty": HARDENED_STATUS.replace(
                "CapEff:\t0000000000000000", "CapEff:\t0000000000000001"
            ),
        }
        for check, text in cases.items():
            with self.subTest(check=check):
                report = module.audit_status(text)
                self.assertFalse(report["all_passed"])
                self.assertFalse(report["checks"][check])

    def test_missing_fields_fail_closed(self) -> None:
        self.assertFalse(module.audit_status("")["all_passed"])

    def test_read_only_root_is_detected(self) -> None:
        report = module.audit_status(HARDENED_STATUS, "overlay / overlay ro,relatime 0 0\n")
        self.assertTrue(report["root_filesystem"]["read_only"])


class CliTests(unittest.TestCase):
    def test_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp, "status.txt")
            good.write_text(HARDENED_STATUS, encoding="utf-8")
            bad = Path(tmp, "bad.txt")
            bad.write_text(HARDENED_STATUS.replace("NoNewPrivs:\t1", "NoNewPrivs:\t0"))
            specs = Path(tmp, "specs.json")
            specs.write_text(json.dumps([app("a", [])]), encoding="utf-8")
            self.assertEqual(module.main(["status", str(good)]), 0)
            self.assertEqual(module.main(["status", str(bad)]), 1)
            self.assertEqual(module.main(["specs", str(specs)]), 1)


if __name__ == "__main__":
    unittest.main()
