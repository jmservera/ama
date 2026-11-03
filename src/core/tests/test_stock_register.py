"""The fictional stock register is rebuilt byte for byte and feeds the fabric tool."""

import csv
import json
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic import stock_fabric, stock_register


def build(root: Path, name: str, **kw: object) -> Path:
    stock_register.write(root / name, **kw)  # type: ignore[arg-type]
    return root / name


class StockRegisterTests(unittest.TestCase):
    def test_same_seed_and_as_of_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            a = build(Path(tmp), "a", n=50, seed=3, as_of="2026-10-01")
            b = build(Path(tmp), "b", n=50, seed=3, as_of="2026-10-01")
            for name in ("stock-register.csv", "manifest.json"):
                self.assertEqual((a / name).read_bytes(), (b / name).read_bytes())

    def test_other_seed_changes_rows_and_manifest_records_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            a = build(Path(tmp), "a", n=50, seed=3)
            b = build(Path(tmp), "b", n=50, seed=4)
            self.assertNotEqual(
                (a / "stock-register.csv").read_bytes(), (b / "stock-register.csv").read_bytes()
            )
            manifest = json.loads((a / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["seed"], 3)
            self.assertEqual(manifest["version"], stock_register.VERSION)
            self.assertRegex(manifest["generator_revision"], r"^sha256:[0-9a-f]{64}$")
            self.assertEqual(manifest["source_type"], "SYNTHETIC")

    def test_ids_are_unique_and_fabric_accepts_the_register(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = build(Path(tmp), "a", n=40, seed=5)
            with (path / "stock-register.csv").open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len({r["synthetic_home_id"] for r in rows}), 40)
            self.assertEqual(len(stock_fabric.fabric_rows(rows)), 40)

    def test_refuses_non_empty_output_and_bad_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = build(Path(tmp), "a", n=2)
            before = (path / "stock-register.csv").read_bytes()
            with self.assertRaises(FileExistsError):
                stock_register.write(path, n=2, seed=99)
            self.assertEqual((path / "stock-register.csv").read_bytes(), before)
            with self.assertRaises(ValueError):
                stock_register.write(Path(tmp) / "b", n=0)
            with self.assertRaises(ValueError):
                stock_register.write(Path(tmp) / "c", n=1, as_of="20261001")


if __name__ == "__main__":
    unittest.main()
