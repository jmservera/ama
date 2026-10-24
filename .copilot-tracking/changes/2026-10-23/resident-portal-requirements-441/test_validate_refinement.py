"""Portable issue 441 mapping reconstruction and integrity regressions."""

import difflib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "resident_refinement", Path(__file__).with_name("validate-refinement.py")
)
refinement = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(refinement)


class RefinementTests(unittest.TestCase):
    def verify_inventory(self, name, inventory, records):
        field, filename = ("outputs", "output-manifest.json") if name == "prd" else (
            "files", "reconciliation-output-manifest.json")
        manifest = f"{name}/{filename}"
        refinement.verify_manifest_sources(
            name, manifest, field, {manifest: json.dumps({field: inventory}).encode()}, records)

    def test_real_manifest_shapes_accept_matching_selected_sources(self):
        records = json.loads((refinement.EVIDENCE / "source-to-integrated.json").read_text())["files"]
        sources = {record["source"]: refinement.source_bytes(record) for record in records}
        for name, manifest, field in (
                ("prd", "prd/output-manifest.json", "outputs"),
                ("adr", "adr/reconciliation-output-manifest.json", "files")):
            with self.subTest(name=name):
                refinement.verify_manifest_sources(name, manifest, field, sources, records)

    def test_manifest_hash_and_size_mismatches_are_rejected_for_both_shapes(self):
        entry = {"sha256": "a" * 64, "bytes": 3}
        for name in ("prd", "adr"):
            inventory = {"sample.md": entry} if name == "prd" else [{"path": "sample.md", **entry}]
            valid = {"source": f"{name}/sample.md", "source_sha256": "a" * 64, "source_bytes": 3}
            for field, bad, message in (
                    ("source_sha256", "b" * 64, "source hash mismatch"),
                    ("source_bytes", 4, "source byte size mismatch")):
                with self.subTest(name=name, field=field), self.assertRaisesRegex(ValueError, message):
                    self.verify_inventory(name, inventory, [{**valid, field: bad}])

    def test_malformed_manifests_fail_explicitly(self):
        entry = {"sha256": "a" * 64, "bytes": 3}
        for inventory in (
                None, "not an inventory", [], {}, [None], [{}],
                [{"path": ""}], [{"path": "../sample.md", **entry}],
                [{"path": "/sample.md", **entry}], [{"path": "./sample.md", **entry}],
                [{"path": "sample.md", **entry}, {"path": "sample.md", **entry}],
                {"sample.md": None}, {"sample.md": {}},
                {"sample.md": {**entry, "sha256": "invalid"}},
                {"sample.md": {**entry, "bytes": -1}}, {"sample.md": {**entry, "bytes": True}}):
            with self.subTest(inventory=inventory), self.assertRaises(ValueError):
                self.verify_inventory("adr", inventory, [])
        for document in ({}, [], {"files": None}):
            with self.subTest(document=document), self.assertRaises(ValueError):
                refinement.verify_manifest_sources(
                    "adr", "adr/manifest.json", "files",
                    {"adr/manifest.json": json.dumps(document).encode()}, [])

    def test_unlisted_boundaries_do_not_skip_inventoried_sources(self):
        entry = {"sha256": "a" * 64, "bytes": 3}
        records = [{"source": f"adr/{path}", "source_sha256": "a" * 64, "source_bytes": 3}
                   for path in ("reconciliation-output-manifest.json", "capstone-review-boundary.md")]
        self.verify_inventory("adr", [{"path": "sample.md", **entry}], records)
        with self.assertRaisesRegex(ValueError, "selected source not inventoried"):
            self.verify_inventory("adr", [{"path": "sample.md", **entry}],
                                  [{**records[0], "source": "adr/unexpected.md"}])
        with self.assertRaisesRegex(ValueError, "selected source not inventoried"):
            self.verify_inventory("prd", {"sample.md": entry},
                                  [{**records[0], "source": "prd/capstone-review-boundary.md"}])
        with self.assertRaisesRegex(ValueError, "source hash mismatch"):
            self.verify_inventory("adr", [{"path": "capstone-review-boundary.md", **entry}],
                                  [{**records[1], "source_sha256": "b" * 64}])

    def test_actual_main_rejects_consistent_mapping_against_pinned_adr_manifest(self):
        mapping_path = refinement.EVIDENCE / "source-to-integrated.json"
        mapping = json.loads(mapping_path.read_text())
        record = next(row for row in mapping["files"]
                      if row["source"] == "adr/requirement-map-reconciled.json")
        integrated = (refinement.ROOT / record["integrated_path"]).read_bytes()
        source = refinement.source_bytes(record) + b"\n"
        record["source_sha256"] = refinement.v.sha(source)
        record["source_bytes"] = len(source)
        record["source_to_integrated_patch"] = "".join(difflib.unified_diff(
            source.decode().splitlines(keepends=True), integrated.decode().splitlines(keepends=True),
            fromfile="source.json", tofile="integrated.json"))
        self.assertEqual(refinement.source_bytes(record), source)
        original_read = Path.read_text

        def read(path, *args, **kwargs):
            return json.dumps(mapping) if path == mapping_path else original_read(path, *args, **kwargs)

        with patch.object(Path, "read_text", read), patch.object(
                sys, "argv", ["validate-refinement.py", "--markdownlint-cli", "unused", "--out", "unused"]):
            with self.assertRaisesRegex(
                    ValueError, "reconciliation-output-manifest.json: source hash mismatch "
                    "for requirement-map-reconciled.json"):
                refinement.main()

    def test_reversible_mapping_retains_exact_source_and_output(self):
        source = b"---\ntitle: Source\n---\n\n# Duplicate title\n\nText [link](old.md).\n"
        for current in (
            source,
            source.replace(b"# Duplicate title\n\n", b""),
            source.replace(b"(old.md)", b"(portable.md)"),
            source.replace(b"\nText", b"\nEditorial notice.\n\nText"),
        ):
            with self.subTest(current=current), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "candidate.md").write_bytes(current)
                record = {
                    "integrated_path": "candidate.md",
                    "integrated_sha256": refinement.v.sha(current),
                    "source_sha256": refinement.v.sha(source),
                    "source_bytes": len(source),
                    "source_to_integrated_patch": "".join(difflib.unified_diff(
                        source.decode().splitlines(keepends=True),
                        current.decode().splitlines(keepends=True),
                        fromfile="source.md", tofile="candidate.md",
                    )),
                }
                with patch.object(refinement, "ROOT", root):
                    self.assertEqual(refinement.source_bytes(record), source)

    def test_integrated_or_source_pin_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = b"Exact source bytes\n"
            (root / "candidate.md").write_bytes(data)
            record = {
                "integrated_path": "candidate.md",
                "integrated_sha256": refinement.v.sha(data),
                "source_sha256": refinement.v.sha(data),
                "source_bytes": len(data), "source_to_integrated_patch": "",
            }
            with patch.object(refinement, "ROOT", root):
                with self.subTest(boundary="source"), self.assertRaises(AssertionError):
                    refinement.source_bytes({**record, "source_sha256": "0" * 64})
                (root / "candidate.md").write_bytes(data + b"Unmapped change\n")
                with self.subTest(boundary="integrated"), self.assertRaises(AssertionError):
                    refinement.source_bytes(record)


if __name__ == "__main__":
    unittest.main()
