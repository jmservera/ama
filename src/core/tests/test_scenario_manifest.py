"""Offline iteration coverage and public-fixture provenance for #103."""

import ast
import copy
import json
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core.synthetic.scenario_manifest import validate_manifest

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "docs/reference/research/retrofit-synthetic-data"


class ScenarioManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads((PACK / "scenario-manifest.json").read_text())

    def test_current_iteration_is_complete_and_honest(self) -> None:
        before = copy.deepcopy(self.manifest)
        validate_manifest(self.manifest, ROOT)
        self.assertEqual(self.manifest, before)
        self.assertEqual(self.manifest["version"], "0.2.1")
        self.assertTrue(
            all(
                entry["status"] == "unavailable"
                for key in ("profiles", "workflows")
                for entry in self.manifest[key]
            )
        )
        self.assertEqual(self.manifest["fixture_contract"]["case_ids"], ["ZF-4", "ZF-1", "ZF-5"])

    def test_profile_inventory_reuses_existing_chat_perspectives(self) -> None:
        tree = ast.parse((ROOT / "src/agents/tests/chat_fixture.py").read_text())
        assignment = next(
            node
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "PERSPECTIVES" for t in node.targets)
        )
        perspectives = ast.literal_eval(assignment.value)
        self.assertEqual(
            [entry["id"] for entry in self.manifest["profiles"]],
            [entry[0] for entry in perspectives],
        )
        prd = (ROOT / "docs/prds/zava-forward-retrofit-programme-demonstrator.md").read_text()
        for entry in self.manifest["profiles"]:
            self.assertIn("| " + entry["perspective"] + " |", prd)
        for entry in self.manifest["workflows"]:
            self.assertIn(entry["name"], prd)

    def reject(self, manifest: dict[str, Any]) -> None:
        with self.assertRaises(ValueError):
            validate_manifest(manifest, ROOT)

    def test_missing_duplicate_and_unknown_inventory_entries_fail(self) -> None:
        for key in ("profiles", "workflows"):
            for mutation in ("missing", "duplicate", "unknown"):
                with self.subTest(key=key, mutation=mutation):
                    manifest = copy.deepcopy(self.manifest)
                    if mutation == "missing":
                        manifest[key].pop()
                    elif mutation == "duplicate":
                        manifest[key][-1] = manifest[key][0]
                    else:
                        manifest[key][-1]["id"] = "invented"
                    self.reject(manifest)

    def test_unsupported_statuses_and_missing_paths_fail(self) -> None:
        for key in ("profiles", "workflows"):
            for field, value in (
                ("status", "partial"),
                ("status", "represented"),
                ("status", "deferred"),
                ("reason", ""),
                ("path", []),
                ("safe_endpoint", ""),
                ("evidence_index", 99),
            ):
                with self.subTest(key=key, field=field, value=value):
                    manifest = copy.deepcopy(self.manifest)
                    manifest[key][0][field] = value
                    self.reject(manifest)

    def test_fixture_drift_and_false_privacy_claims_fail(self) -> None:
        for field, value in (
            ("is_synthetic", False),
            ("contains_real_data", True),
            ("version", ""),
            ("iteration", ""),
            ("active_slice", ""),
            ("applicable_checks", []),
        ):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest[field] = value
                self.reject(manifest)
        for fixture_field, fixture_value in (
            ("version", "stale"),
            ("case_ids", ["PRIVATE-1"]),
            ("default_selection", "ZF-1"),
            ("default_sort", "name"),
            ("role_defaults", []),
        ):
            with self.subTest(fixture_field=fixture_field):
                manifest = copy.deepcopy(self.manifest)
                manifest["fixture_contract"][fixture_field] = fixture_value
                self.reject(manifest)
        for field, value in (
            ("path", "../private.json"),
            ("path", "/tmp/private.json"),
            ("path", "support/cohort.md"),
            ("sha256", "0" * 64),
        ):
            with self.subTest(source_field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest["sources"][0][field] = value
                if field == "path":
                    with patch.object(
                        Path, "read_bytes", side_effect=AssertionError("Unapproved source read")
                    ):
                        self.reject(manifest)
                else:
                    self.reject(manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["sources"].pop()
        self.reject(manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["profile_defaults"]["asset-investment"] = {"ids": [], "count": 0}
        self.reject(manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["fixture_references"][0] = "support/cohort.md"
        self.reject(manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["evaluation_registry"] = "new-registry.json"
        self.reject(manifest)

    def test_malformed_metadata_fails_with_actionable_errors(self) -> None:
        for key in ("sources", "profiles", "workflows", "inventory"):
            with self.subTest(key=key):
                manifest = copy.deepcopy(self.manifest)
                manifest[key] = None
                self.reject(manifest)
        for key in ("sources", "profiles", "workflows"):
            for row in (None, {}, {"id": "unknown"}):
                with self.subTest(key=key, row=row):
                    manifest = copy.deepcopy(self.manifest)
                    manifest[key][0] = row
                    self.reject(manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["profiles"][0]["resident"] = {"name": "Unreviewed supplied person"}
        self.reject(manifest)

    def test_false_inventory_approval_or_stale_binding_fails(self) -> None:
        for field, value in (
            ("version", "stale"),
            ("review_date", "2026-10-01"),
            ("owner_review", "approved"),
            ("reviewed_rows", ["SN-11"]),
        ):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest["inventory"][field] = value
                self.reject(manifest)

    def test_journey_coverage_cannot_grant_source_authority(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest.pop("inventory_authority")
        with self.assertRaisesRegex(ValueError, "authority"):
            validate_manifest(manifest, ROOT)
        for field, value in (
            ("roles", "confirmed-company-roles"),
            ("journeys", "approved-operational-journeys"),
            ("customer_approval", "approved"),
            ("owner_approval", "approved"),
            ("source", "unrecorded-approval"),
        ):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest["inventory_authority"][field] = value
                with self.assertRaisesRegex(ValueError, "authority"):
                    validate_manifest(manifest, ROOT)
