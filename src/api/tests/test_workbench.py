"""Server-owned navigation and the bounded IA manifest contract."""

import json
import unittest
from pathlib import Path
from typing import Any

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
        self.assertEqual(manifest["widths"], [320, 360, 390, 768, 1024, 1280])
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

    def test_owner_decided_device_widths_match_checked_widths(self) -> None:
        manifest = json.loads(MANIFEST.read_text())
        devices = manifest["supported_devices"]
        self.assertEqual(devices["status"], "decided")
        self.assertEqual(devices["decider"], "owner")
        self.assertEqual(devices["decided_on"], "2026-11-13")
        supported = {
            item["class"]: item["width"]
            for item in devices["classes"]
            if item["class"] in ("desktop", "tablet", "mobile")
        }
        self.assertEqual(supported, {"desktop": 1280, "tablet": 768, "mobile": 360})
        self.assertTrue({1280, 768, 360, 320} <= set(manifest["widths"]))
        self.assertEqual(
            sorted(item["width"] for item in devices["classes"]), sorted(manifest["widths"])
        )
        proposal = MANIFEST.parents[3] / devices["proposal"]
        text = proposal.read_text()
        self.assertIn("Decided by the owner on 2026-11-13", text)
        for width in manifest["widths"]:
            self.assertIn(f"| {width} |", text)

    def test_ac043_manifest_declares_slice_coverage_and_unavailable(self) -> None:
        manifest = json.loads(MANIFEST.read_text())
        self.assertTrue(manifest["version"])
        self.assertTrue(manifest["active_slice"].startswith("Shared IA engineering only"))
        self.assertIn("not complete", manifest["active_slice"])
        self.assertIn("Full AC-034/043 acceptance", manifest["unavailable"])
        self.assertTrue(manifest["unknowns"])
        profiles = {item["perspective"]: item for item in manifest["profiles"]}
        workflows = {item["name"]: item for item in manifest["workflows"]}
        self.assertEqual(
            set(profiles),
            {
                "Asset and investment",
                "Programme coordinator",
                "Retrofit case team",
                "Retrofit Assessor, designer and Coordinator",
                "Housing and Resident Engagement",
                "Repairs and Building Safety",
                "Procurement and contract manager",
                "Provider / contractor contact",
                "Quality and assurance",
                "Finance and Grants",
                "Digital operator and auditor",
            },
        )
        self.assertEqual(len(manifest["profiles"]), 11)
        self.assertEqual(len(workflows), 9)
        self.assertEqual(len(manifest["workflows"]), 9)
        routes = {link for role in manifest["roles"] for link in role["navigation"]}
        routes |= {f"#/case/{case_id}" for case_id in manifest["all_case_ids"]}
        for item in [*profiles.values(), *workflows.values()]:
            if item["status"] != "partial":
                self.assertTrue(item["reason"])
                continue
            self.assertIn(item["endpoint"], routes)
            self.assertTrue(set(item["fixture"]) <= set(manifest["all_case_ids"]))
            self.assertTrue(item["checks"])
            self.assertTrue(item["deferred"])
        for item in workflows.values():
            if item["status"] == "partial":
                self.assertTrue(item["fixture"])

    def test_ac034_scope_reset_checks_follow_default_manifest(self) -> None:
        manifest = json.loads(MANIFEST.read_text())
        self.assertIsNone(manifest["default_selection"])
        self.assertEqual(manifest["default_sort"], "urgent")
        reset_profiles = []
        for item in manifest["profiles"]:
            if item["status"] != "partial":
                self.assertNotIn("default", item)
                continue
            default = item["default"]
            self.assertTrue(item["checks"], item["perspective"])
            if not default["ids"]:
                self.assertEqual(default["count"], 0, item["perspective"])
                self.assertEqual(
                    default["empty_reason"],
                    "no representative scenario supplied",
                    item["perspective"],
                )
            if "reset" in item["checks"]:
                reset_profiles.append(item["perspective"])
                self.assertIn("scope", item["checks"])
                self.assertTrue(default["ids"])
        self.assertEqual(reset_profiles, ["Housing and Resident Engagement"])

    def test_every_role_navigation_omits_the_role_simulator(self) -> None:
        manifest = json.loads(MANIFEST.read_text())
        self.assertEqual(len(manifest["roles"]), 8)
        self.assertFalse(self.simulator_links(manifest["roles"]))
        injected = [{"code": "X", "navigation": ["#/", "#/simulator"]}]
        self.assertEqual(self.simulator_links(injected), ["X"])

    @staticmethod
    def simulator_links(roles: list[dict[str, Any]]) -> list[str]:
        return [
            role["code"]
            for role in roles
            if any("simulator" in link for link in role["navigation"])
        ]


if __name__ == "__main__":
    unittest.main()
