"""Offline provenance/privacy regressions using public data and fresh small fixtures only."""

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic import privacy, scale_fixture, sensor_backfill, sensor_stock

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / privacy.PACK
REGISTER = json.loads((PACK / "provenance-register.json").read_text())
SAMPLES = {
    "email": "jo.smith@example.com",
    "uk_phone": "07700 900123",
    "ni_number": "AB 12 34 56 C",
    "uk_postcode": "NE5 2QS",
}


def rehash(out: Path) -> None:
    manifest = json.loads((out / "manifest.json").read_text())
    manifest["file_sha256"] = {
        name: hashlib.sha256((out / name).read_bytes()).hexdigest()
        for name in manifest["file_sha256"]
    }
    (out / "manifest.json").write_text(json.dumps(manifest))


class ProvenanceRegisterTests(unittest.TestCase):
    def test_every_dataset_has_current_visibility_and_dictionary_entry(self) -> None:
        dictionary = (PACK / REGISTER["dictionary"]).read_text()
        headings = {
            re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-")
            for h in re.findall(r"^#+ (.+)$", dictionary, re.M)
        }
        ids = [d["id"] for d in REGISTER["datasets"]]
        self.assertEqual(len(ids), len(set(ids)))
        source_ids = {source["id"] for source in REGISTER["sources"]}
        for dataset in REGISTER["datasets"]:
            self.assertIn(dataset["visibility"], {"public", "private"})
            path, _, anchor = dataset["data_dictionary"].partition("#")
            self.assertEqual(path, REGISTER["dictionary"])
            if anchor:
                self.assertIn(anchor, headings, dataset["id"])
            self.assertLessEqual(set(dataset["sources"]), source_ids)
        self.assertTrue(
            {
                "DS-SENSOR",
                "DS-SCALE-FIXTURE",
                "DS-STOCK-FABRIC",
                "DS-CHAT-RUNTIME",
                "DS-CHAT-MEMORY-FIXTURE",
                "DS-CHAT-GOLDEN",
                "DS-REGULATORY-EVALS",
                "DS-DOC-CONTROL-FIXTURES",
            }
            <= set(ids)
        )
        sensor = next(d for d in REGISTER["datasets"] if d["id"] == "DS-SENSOR")
        self.assertIn("generator-and-small-fixture-tests-delivered", sensor["generation_status"])

    def test_all_public_payloads_pass_production_checker(self) -> None:
        self.assertEqual(privacy.public_issues(ROOT), [])

    def test_source_audit_reports_exactly_the_unmet_historic_sources(self) -> None:
        issues = privacy.source_issues(REGISTER["sources"])
        expected = {
            f"{sid}:missing_or_invalid_retrieval_date"
            for sid in ("SRC-CENSUS-TS054", "SRC-IMD-2025", "SRC-ONS-BOUNDARIES")
        } | {"SRC-ONS-BOUNDARIES:provisional_attribution"}
        self.assertEqual(sorted(issues), sorted(expected))
        valid = [
            {
                "id": "SYN-SOURCE",
                "licence": "Test licence",
                "attribution": "Test source",
                "url": "https://example.test/source",
                "retrieval_date": "2026-10-16",
            }
        ]
        self.assertEqual(privacy.source_issues(valid), [])
        for field in ("licence", "attribution", "url", "retrieval_date"):
            with self.subTest(field=field):
                self.assertTrue(privacy.source_issues([{**valid[0], field: None}]))
        for field in ("licence", "attribution"):
            with self.subTest(provisional=field):
                self.assertIn(
                    f"SYN-SOURCE:provisional_{field}",
                    privacy.source_issues([{**valid[0], field: "wording to confirm"}]),
                )

    def test_private_and_public_separation_without_reading_private_data(self) -> None:
        for dataset in REGISTER["datasets"]:
            location = dataset["location"]
            if dataset["visibility"] == "private":
                self.assertTrue(location.startswith(("support/", "ZF_DATA", "serving database")))
            else:
                self.assertTrue(
                    location.startswith("docs/") or re.match(r"src/[^/]+/evals/", location)
                )
        for path in (
            "src/core/data/synthetic-probe.json",
            "support/synthetic-data/probe/answer-key/probe.json",
        ):
            result = subprocess.run(
                ["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT, check=False
            )
            self.assertEqual(result.returncode, 0, path)


class PrivacyMutationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=ROOT / "src/core")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "zava_forward.core.synthetic.privacy", *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_public_cli_and_source_audit_are_independent(self) -> None:
        clean = self.cli("--public-root", str(ROOT))
        self.assertEqual(clean.returncode, 0, clean.stderr)
        blocked = self.cli("--public-root", str(ROOT), "--sources")
        self.assertEqual(blocked.returncode, 1)
        self.assertIn("SRC-CENSUS-TS054:missing_or_invalid_retrieval_date", blocked.stdout)

    def test_patterns_labels_and_sanitized_cli_on_rehashed_sensor_snapshots(self) -> None:
        for kind, sample in {**SAMPLES, "missing": None, "false": False}.items():
            with self.subTest(kind=kind):
                out = self.root / kind
                sensor_backfill.write(out, homes=2, days=1, cadence=360)
                self.assertEqual(privacy.snapshot_issues(out, "sensor"), [])
                path = out / "sensors.csv"
                with path.open(newline="") as handle:
                    reader = csv.DictReader(handle)
                    fields = reader.fieldnames
                    rows = list(reader)
                if kind in SAMPLES:
                    rows[0]["fault_profile"] = str(sample)
                    expected = kind
                else:
                    rows[0]["source_type"] = "" if sample is None else "false"
                    expected = "missing_synthetic_label"
                with path.open("w", newline="") as handle:
                    writer = csv.DictWriter(handle, fields)
                    writer.writeheader()
                    writer.writerows(rows)
                rehash(out)
                issues = privacy.snapshot_issues(out, "sensor")
                self.assertIn(f"sensors.csv:row-1:{expected}", issues)
                self.assertFalse(any("hash" in issue for issue in issues), issues)
                result = self.cli("--snapshot", str(out), "--kind", "sensor")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(expected, result.stdout)
                if isinstance(sample, str):
                    self.assertNotIn(sample, result.stdout + result.stderr)

    def test_scalar_shapes_labels_and_pattern_variants(self) -> None:
        self.assertEqual(privacy.record_issues("unlabelled"), ["record_not_object"])
        for value in (None, False, 1, "yes", ""):
            self.assertIn("missing_synthetic_label", privacy.record_issues({"is_synthetic": value}))
        for value in (True, "true", "True"):
            self.assertEqual(privacy.record_issues({"is_synthetic": value}), [])
        for sample in ("+44 7700 900123", "+44 (0)7700 900123", "020 7123 4567"):
            self.assertIn("uk_phone", privacy.pattern_issues(sample))
        self.assertIn("ni_number", privacy.pattern_issues("ab123456c"))
        self.assertIn("uk_postcode", privacy.pattern_issues("ne5 2qs"))
        self.assertIn("email", privacy.pattern_issues({SAMPLES["email"]: ""}))
        self.assertIn("missing_synthetic_label", privacy.record_issues({}, "contains_real_data"))

    def test_scale_manifest_inheritance_and_household_labels(self) -> None:
        out = self.root / "scale"
        scale_fixture.write(out, n=3, per_home=2)
        self.assertEqual(privacy.snapshot_issues(out, "scale"), [])
        self.assertEqual(self.cli("--snapshot", str(out), "--kind", "scale").returncode, 0)
        path = out / "households.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        del rows[0]["is_synthetic"]
        path.write_text("".join(json.dumps(row) + "\n" for row in rows))
        rehash(out)
        self.assertIn(
            "households.jsonl:row-1:missing_synthetic_label",
            privacy.snapshot_issues(out, "scale"),
        )
        self.assertEqual(privacy.pattern_issues({"postcode": "TE1 1ST"}, scale_home=True), [])
        self.assertIn("uk_postcode", privacy.pattern_issues({"notes": "TE1 1ST"}, scale_home=True))

    def test_register_backed_sensor_snapshot_is_checked(self) -> None:
        stock = sensor_stock.select(
            [
                {
                    "synthetic_home_id": "SYN-HOME-1",
                    "is_synthetic": "true",
                    "monitoring_consent": "granted",
                },
                {
                    "synthetic_home_id": "SYN-HOME-2",
                    "is_synthetic": "true",
                    "monitoring_consent": "unknown",
                },
            ],
            2,
        )
        # The existing register-backed generator refuses all repository destinations.
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "stock-sensor"
            sensor_backfill.write(out, stock=stock, days=1, cadence=360)
            self.assertEqual(privacy.snapshot_issues(out, "sensor"), [])
            excluded = sensor_stock.select(
                [
                    {
                        "synthetic_home_id": "SYN-HOME-1",
                        "is_synthetic": "true",
                        "monitoring_consent": "declined",
                    }
                ],
                1,
            )
            empty_out = Path(tmp) / "excluded"
            sensor_backfill.write(empty_out, stock=excluded, days=1, cadence=360)
            self.assertEqual(privacy.snapshot_issues(empty_out, "sensor"), [])
            for snapshot in (out, empty_out):
                path = snapshot / "manifest.json"
                manifest = json.loads(path.read_text())
                for version in ("sensor-backfill-stock-v1", "sensor-backfill-stock-v2"):
                    path.write_text(json.dumps({**manifest, "version": version}))
                    self.assertEqual(privacy.snapshot_issues(snapshot, "sensor"), [])

    def test_integrity_manifest_label_unknown_file_and_malformed_fail_separately(self) -> None:
        out = self.root / "scale"
        scale_fixture.write(out, n=2, per_home=1)
        path = out / "homes.jsonl"
        original = path.read_text()
        path.write_text(" " + original)
        self.assertIn("homes.jsonl:hash_mismatch", privacy.snapshot_issues(out, "scale"))
        path.write_text(original)
        manifest = json.loads((out / "manifest.json").read_text())
        del manifest["source_type"]
        (out / "manifest.json").write_text(json.dumps(manifest))
        self.assertIn("manifest:missing_synthetic_label", privacy.snapshot_issues(out, "scale"))
        self.assertEqual(self.cli("--snapshot", str(out), "--kind", "scale").returncode, 1)
        (out / "extra.jsonl").write_text("{}\n")
        self.assertIn("snapshot:unexpected_or_missing_files", privacy.snapshot_issues(out, "scale"))
        path.write_text("{broken")
        self.assertEqual(self.cli("--snapshot", str(out), "--kind", "scale").returncode, 2)

    def test_checker_refuses_private_location_reclassified_as_public(self) -> None:
        root = self.public_copy()
        path = root / privacy.PACK / "provenance-register.json"
        register = json.loads(path.read_text())
        private = next(d for d in register["datasets"] if d["id"] == "DS-STOCK-REGISTER")
        private["visibility"] = "public"
        path.write_text(json.dumps(register))
        with self.assertRaisesRegex(ValueError, "Public location"):
            privacy.public_issues(root)
        self.assertEqual(self.cli("--public-root", str(root)).returncode, 2)

    def public_copy(self) -> Path:
        root = self.root / "public"
        for source in [PACK, *sorted((ROOT / "src").glob("*/evals"))]:
            destination = root / source.relative_to(ROOT)
            destination.mkdir(parents=True)
            for path in source.iterdir():
                if path.suffix in {".csv", ".json"}:
                    shutil.copyfile(path, destination / path.name)
        return root

    def test_public_exemptions_do_not_exempt_text_scans_or_labelled_collections(self) -> None:
        root = self.public_copy()
        self.assertEqual(privacy.public_issues(root), [])
        path = root / "src/agents/evals/chat_golden.json"
        data = json.loads(path.read_text())
        data["scenarios"][0]["turns"][0]["say"] = SAMPLES["email"]
        path.write_text(json.dumps(data))
        self.assertTrue(any(item.endswith(":email") for item in privacy.public_issues(root)))
        self.assertEqual(self.cli("--public-root", str(root)).returncode, 1)
        path = root / "src/core/evals/document_control_fixtures.json"
        data = json.loads(path.read_text())
        del data["cases"][0]["is_synthetic"]
        path.write_text(json.dumps(data))
        self.assertTrue(
            any(
                "document_control_fixtures.json:row-1:missing_synthetic_label" in item
                for item in privacy.public_issues(root)
            )
        )
        (root / "src/agents/evals/unregistered.json").write_text("{}")
        self.assertTrue(
            any("unregistered_public_payload" in item for item in privacy.public_issues(root))
        )


if __name__ == "__main__":
    unittest.main()
