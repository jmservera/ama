"""Server-owned navigation and the bounded IA manifest contract."""

import json
import unittest
from pathlib import Path

from zava_forward.api.workbench import navigation

MANIFEST = Path(__file__).resolve().parents[1] / "checks/workbench-manifest.json"


class WorkbenchNavigation(unittest.TestCase):
    def test_existing_roles_have_exact_manifest_destinations(self) -> None:
        for role in json.loads(MANIFEST.read_text())["roles"]:
            with self.subTest(role=role["role"]):
                links = navigation({"role": role["role"], "name": "Synthetic"})
                self.assertEqual([item["href"] for item in links], role["navigation"])
                self.assertTrue(all(set(item) == {"href", "label", "scope"} for item in links))
                self.assertTrue(all(item["scope"] for item in links))

    def test_unknown_role_has_no_navigation(self) -> None:
        self.assertEqual(navigation({"role": "Unknown"}), [])
        self.assertEqual(navigation({}), [])

    def test_manifest_preserves_all_perspectives_and_defers_missing_evidence(self) -> None:
        manifest = json.loads(MANIFEST.read_text())
        self.assertEqual(len(manifest["profiles"]), 11)
        self.assertEqual(len(manifest["workflows"]), 9)
        self.assertEqual(manifest["widths"], [320, 390, 768, 1024, 1280])
        self.assertIsNone(manifest["default_selection"])
        identities = {item["email"] for item in manifest["roles"]}
        for item in manifest["profiles"] + manifest["workflows"]:
            self.assertIn(item["status"], ("partial", "deferred"))
            if item["status"] == "partial":
                self.assertTrue(item["checks"])
                self.assertTrue(item["endpoint"])
                self.assertIn("fixture", item)
                self.assertTrue(item["deferred"])
                if "identity" in item:
                    self.assertIn(item["identity"], identities)
            else:
                self.assertTrue(item["reason"])

    def test_profile_defaults_match_own_queues_and_declare_empty_reason(self) -> None:
        manifest = json.loads(MANIFEST.read_text())
        roles = {item["email"]: item for item in manifest["roles"]}
        with_default = 0
        for item in manifest["profiles"]:
            if "default" not in item:
                self.assertEqual(item["status"], "deferred", item["perspective"])
                continue
            with_default += 1
            default = item["default"]
            with self.subTest(profile=item["perspective"]):
                self.assertEqual(default["ids"], roles[item["identity"]]["ids"])
                self.assertEqual(default["count"], len(default["ids"]))
                self.assertEqual(default["order"], manifest["default_sort"])
                self.assertEqual(default["selection"], manifest["default_selection"])
                self.assertEqual(
                    default.get("empty_reason"),
                    None if default["ids"] else "no representative scenario supplied",
                )
                self.assertTrue(set(default["ids"]) <= set(manifest["all_case_ids"]))
                self.assertTrue(set(default["ids"]) <= set(item["fixture"]) or not default["ids"])
        self.assertEqual(with_default, 8)

    def test_supported_devices_stay_proposed_and_match_checked_widths(self) -> None:
        manifest = json.loads(MANIFEST.read_text())
        devices = manifest["supported_devices"]
        self.assertEqual(devices["status"], "proposed")
        self.assertEqual(devices["decider"], "owner")
        self.assertEqual(devices["field_mobile"], "undecided")
        self.assertEqual(sorted(item["width"] for item in devices["classes"]), manifest["widths"])
        self.assertIn(320, [item["width"] for item in devices["classes"]])
        proposal = MANIFEST.parents[3] / devices["proposal"]
        self.assertTrue(proposal.is_file())
        text = proposal.read_text()
        self.assertIn("Proposed, not decided", text)
        for width in manifest["widths"]:
            self.assertIn(f"| {width} |", text)


if __name__ == "__main__":
    unittest.main()
