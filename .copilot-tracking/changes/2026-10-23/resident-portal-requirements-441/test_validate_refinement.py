"""Portable issue 441 mapping reconstruction and integrity regressions."""

import difflib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "resident_refinement", Path(__file__).with_name("validate-refinement.py")
)
refinement = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(refinement)


class RefinementTests(unittest.TestCase):
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
