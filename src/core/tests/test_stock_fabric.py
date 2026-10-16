"""Stock assumptions and exact-reference linkage, never private geography or unit evidence."""

import contextlib
import csv
import hashlib
import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path
from unittest.mock import patch

from zava_forward.core.synthetic import provenance
from zava_forward.core.synthetic import stock_fabric as fabric

ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / "support/synthetic-data/retrofit-flow/zava-forward-year-one/generator"


def register(n: int = 60000) -> list[dict[str, object]]:
    forms = ("apartments", "bungalow", "terrace", "semidetached_house", "detached")
    return [
        dict(
            synthetic_home_id=f"FICTION-{i:05d}",
            portfolio_category="General needs - social rent",
            postcode="TEST 1",
            address_street_or_place="Fictional Test Street",
            address_house_number=str(i + 1),
            address_locality="Fictional Test Town",
            local_authority="Test Authority",
            locality_theme=f"Locality {'ABC'[i % 3]}",
            building_form_osm=forms[(i // 3) % 5],
            latitude="54.9",
            longitude="-1.5",
        )
        for i in range(n)
    ]


def case(cid: str, anchor: object = None) -> dict[str, object]:
    return dict(id=cid, synthetic_stock_anchor_id=anchor)


class StockFabricTests(unittest.TestCase):
    def test_legacy_seeded_draws_are_unchanged(self) -> None:
        gold = [
            ("A", "apartments", 1900, "pre-1919", "Flat", "Solid brick", "Mains gas boiler"),
            (
                "B",
                "terrace",
                1928,
                "1919-1944",
                "Terraced house",
                "Cavity brick",
                "Mains gas boiler",
            ),
            (
                "C",
                "house",
                1961,
                "1945-1964",
                "Detached house",
                "Cavity brick",
                "Air source heat pump",
            ),
        ]
        for loc, form, year, age, dwelling, wall, heating in gold:
            row = fabric.fabric(
                dict(
                    synthetic_home_id=f"GOLD-{loc}",
                    locality_theme=f"Locality {loc}",
                    building_form_osm=form,
                ),
                7,
            )
            self.assertEqual(
                (
                    row["build_year"],
                    row["age_band"],
                    row["dwelling_type"],
                    row["construction"],
                    row["heating"],
                ),
                (year, age, dwelling, wall, heating),
            )
            self.assertTrue(row["is_synthetic"] and row["fabric_is_synthetic"])
            self.assertEqual(row["fabric_version"], "stock-fabric-v1")

    def test_case_resolution_accounts_for_missing_invalid_ambiguous_and_shared(self) -> None:
        stock: list[dict[str, object]] = [
            dict(synthetic_home_id="ONE"),
            dict(synthetic_home_id="DUP"),
            dict(synthetic_home_id="DUP"),
            dict(synthetic_home_id=None),
        ]
        cases = [
            case("C-1", "ONE"),
            case("C-2", "ONE"),
            case("C-3"),
            case("C-4", ""),
            case("C-5", " "),
            case("C-6", []),
            case("C-7", "UNKNOWN"),
            case("C-8", "DUP"),
        ]
        links = fabric.resolve_cases(cases, stock)
        self.assertEqual(len(links), len(cases))
        self.assertEqual(
            [link["reason"] for link in links],
            [
                None,
                None,
                "missing_stock_anchor",
                "missing_stock_anchor",
                "invalid_stock_anchor",
                "invalid_stock_anchor",
                "stock_anchor_not_found",
                "ambiguous_stock_anchor",
            ],
        )
        self.assertTrue(all(link["shared_anchor"] for link in links[:2]))
        self.assertTrue(all(link["stock_home_id"] is None for link in links[2:]))
        report = fabric.link_report(cases, stock)
        self.assertEqual((report["linked_cases"], report["unlinked_cases"]), (2, 6))
        self.assertEqual(report["distinct_stock_homes"], 1)
        self.assertEqual(report["stock_homes_shared_by_cases"], 1)
        self.assertIn("not verified", str(report["scope"]))
        self.assertIn("not verified dwellings", str(report["note"]))
        self.assertEqual(report, fabric.link_report(list(reversed(cases)), list(reversed(stock))))

    def test_invalid_snapshot_and_case_ids_are_not_repaired_or_collapsed(self) -> None:
        invalid_ids: list[object] = [None, "", " ", 12, [], " padded "]
        for value in invalid_ids:
            with self.subTest(value=value), self.assertRaises(ValueError):
                fabric.fabric_rows([dict(synthetic_home_id=value)])
            with self.subTest(case=value), self.assertRaises(ValueError):
                fabric.resolve_cases([dict(id=value)], [])
        with self.assertRaises(ValueError):
            fabric.fabric_rows([dict(synthetic_home_id="X"), dict(synthetic_home_id="X")])
        with self.assertRaises(ValueError):
            fabric.resolve_cases([case("C"), case("C")], [])
        self.assertEqual(
            fabric.fabric(dict(synthetic_home_id="Opaque:A/1"))["synthetic_home_id"], "Opaque:A/1"
        )
        self.assertEqual(fabric.locality_letter("Locality "), "B")

    def test_enrichment_clears_unlinked_derived_fields_not_operational_evidence(self) -> None:
        cases = [case("C", "DUP")]
        cases[0].update(
            stock_fabric={"stale": True},
            stock_epc={"stale": True},
            history=[{"retained": True}],
            decision={"status": "Waiting"},
            home={"built": 1950},
        )
        fabric.attach_fabric(cases, [dict(synthetic_home_id="DUP")] * 2)
        self.assertNotIn("stock_fabric", cases[0])
        self.assertNotIn("stock_epc", cases[0])
        self.assertEqual(cases[0]["history"], [{"retained": True}])
        self.assertEqual(cases[0]["decision"], {"status": "Waiting"})
        self.assertEqual(cases[0]["home"], {"built": 1950})

    def test_cli_determinism_hashes_defaults_and_explicit_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reg = root / "private-north-east-stock-register.csv"
            rows = register(30)
            with reg.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            seed = root / "cases.json"
            seed.write_text(json.dumps({"cases": [case("C", "FICTION-00000")]}))
            env = dict(os.environ, ZF_DATA=str(root))
            cmd = [sys.executable, "-m", "zava_forward.core.synthetic.stock_fabric"]
            first = subprocess.run(
                cmd + ["--cases", str(seed)], env=env, capture_output=True, text=True, check=True
            )
            self.assertEqual(first.stdout, "")
            one = root / "stock-fabric"
            two = root / "second"
            subprocess.run(
                cmd + ["--out", str(two), "--cases", str(seed)],
                env=env,
                capture_output=True,
                check=True,
            )
            self.assertEqual(
                {p.name: p.read_bytes() for p in one.iterdir()},
                {p.name: p.read_bytes() for p in two.iterdir()},
            )
            summary = json.loads((one / "summary.json").read_text())
            self.assertIn("not a company fact", summary["label"])
            self.assertEqual(summary["homes"], 30)
            self.assertEqual(summary["seed"], fabric.SEED)
            self.assertRegex(summary["generator_revision"], r"^sha256:[0-9a-f]{64}$")
            for name, digest in summary["file_sha256"].items():
                self.assertEqual(hashlib.sha256((one / name).read_bytes()).hexdigest(), digest)
            linked = json.loads((one / "linked-cases.json").read_text())
            self.assertEqual(linked["stock_link"]["linked_cases"], 1)
            before = (one / "summary.json").read_bytes()
            bad = subprocess.run(cmd, env=env, capture_output=True, text=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("not empty", bad.stderr)
            self.assertEqual((one / "summary.json").read_bytes(), before)
            invalid_seeds: list[object] = [{"cases": [case("C"), case("C")]}, {"cases": None}, []]
            for value in invalid_seeds:
                seed.write_text(json.dumps(value))
                dest = root / "invalid"
                bad = subprocess.run(
                    cmd + ["--out", str(dest), "--cases", str(seed)],
                    env=env,
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(bad.returncode, 0)
                self.assertEqual(bad.stdout, "")
                self.assertFalse(dest.exists())
            reg.write_text("synthetic_home_id\nDUP\nDUP\n")
            bad = subprocess.run(
                cmd + ["--out", str(root / "invalid")], env=env, capture_output=True, text=True
            )
            self.assertNotEqual(bad.returncode, 0)
            self.assertFalse((root / "invalid").exists())
            reg.write_text("synthetic_home_id\nONE\n")
            alias = root / "repository-alias"
            alias.symlink_to(ROOT, target_is_directory=True)
            for dest in (
                ROOT / "stock-output-must-not-exist",
                alias / "stock-output-must-not-exist",
            ):
                bad = subprocess.run(
                    cmd + ["--out", str(dest)], env=env, cwd=root, capture_output=True, text=True
                )
                self.assertNotEqual(bad.returncode, 0)
                self.assertIn("outside the repository", bad.stderr)
                self.assertFalse(dest.exists())

    def test_installed_cli_outside_checkout_refuses_destination_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            installed = root / "site-packages"
            package = installed / "zava_forward/core/synthetic"
            package.mkdir(parents=True)
            source = Path(fabric.__file__).parent
            for name in ("__init__.py", "provenance.py", "stock_fabric.py"):
                shutil.copyfile(source / name, package / name)
            reg = root / "register.csv"
            reg.write_text("synthetic_home_id\nFICTION-ONE\n")
            env = dict(os.environ, PYTHONPATH=str(installed))
            cmd = [
                sys.executable,
                "-S",
                "-m",
                "zava_forward.core.synthetic.stock_fabric",
                "--register",
                str(reg),
            ]
            for marker in ("file", "directory"):
                repo = root / marker
                repo.mkdir()
                if marker == "file":
                    (repo / ".git").write_text("gitdir: /fictional/worktree\n")
                else:
                    (repo / ".git").mkdir()
                existing = repo / "empty"
                existing.mkdir()
                alias = root / f"{marker}-alias"
                alias.symlink_to(repo, target_is_directory=True)
                for dest in (
                    repo,
                    existing,
                    repo / "missing" / "nested" / "snapshot",
                    alias / "missing" / "snapshot",
                ):
                    with self.subTest(marker=marker, destination=dest):
                        bad = subprocess.run(
                            cmd + ["--out", str(dest)],
                            env=env,
                            cwd=root,
                            capture_output=True,
                            text=True,
                        )
                        self.assertEqual(bad.returncode, 2)
                        self.assertEqual(bad.stdout, "")
                        self.assertIn("outside the repository", bad.stderr)
                        self.assertEqual(list(existing.iterdir()), [])
                        self.assertFalse((repo / "missing").exists())
                        self.assertFalse((repo / "stock-fabric.csv").exists())
            allowed = root / "allowed" / "snapshot"
            good = subprocess.run(
                cmd + ["--out", str(allowed)],
                env=env,
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(good.stdout, "")
            self.assertTrue((allowed / "stock-fabric.csv").is_file())

    def test_revisions_cover_moved_dependency_and_ignore_physical_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copies = []
            for source in fabric.revision_sources():
                target = root / source.name
                target.write_bytes(source.read_bytes())
                copies.append(target)
            self.assertEqual(
                provenance.source_revision(copies),
                provenance.source_revision(fabric.revision_sources()),
            )
            with patch.object(sys, "path", [str(GENERATOR), *sys.path]):
                manifest = importlib.import_module("zf_manifest")
            before = manifest.generator_revision()
            core_before = provenance.source_revision(copies)
            next(p for p in copies if p.name == "stock_fabric.py").write_text("# changed source\n")
            self.assertNotEqual(core_before, provenance.source_revision(copies))
            with patch.object(fabric, "revision_sources", return_value=tuple(copies)):
                self.assertNotEqual(before, manifest.generator_revision())

    def test_connected_60000_home_980_case_builder_and_closed_sqlite_restart(self) -> None:
        stock = register()
        attrs = fabric.fabric_rows(stock)
        self.assertEqual(len({r["synthetic_home_id"] for r in attrs}), 60000)
        self.assertTrue(all(r["is_synthetic"] and r["fabric_is_synthetic"] for r in attrs))
        self.assertEqual(attrs, fabric.fabric_rows(stock))
        self.assertNotEqual(attrs, fabric.fabric_rows(stock, fabric.SEED + 1))
        for row in attrs:
            lo, hi = fabric.AGE_BANDS[row["age_band"]]
            self.assertLessEqual(lo, row["build_year"])
            self.assertLessEqual(row["build_year"], hi)
        summary = fabric.summary(attrs)
        for key in ("age_band", "dwelling_type", "construction", "heating"):
            counts = summary[f"{key}_counts"]
            self.assertIsInstance(counts, dict)
            if isinstance(counts, dict):
                self.assertEqual(sum(counts.values()), 60000)
        by_id = {r["synthetic_home_id"]: r for r in attrs}
        with patch.object(sys, "path", [str(GENERATOR), *sys.path]):
            builder = importlib.import_module("build_mvp_dataset")
            sqlstore = importlib.import_module("zava_forward.core.sqlstore")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seed.json"
            with (
                patch.object(builder, "load_register", return_value=stock),
                patch.object(
                    sys,
                    "argv",
                    ["builder", "--seed", "20260901", "--as-of", "2026-10-13", "--out", str(path)],
                ),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                builder.main()
            data = json.loads(path.read_text())
            self.assertEqual(len({c["id"] for c in data["cases"]}), 980)
            report = data["stock_link"]
            self.assertEqual(report["stock_register_rows"], 60000)
            self.assertEqual(report["linked_cases"] + report["unlinked_cases"], 980)
            self.assertEqual(len(report["resolutions"]), 980)
            for c in data["cases"]:
                link = c["stock_link"]
                self.assertEqual(link["case_id"], c["id"])
                self.assertEqual(link["scope"], fabric.LINK_SCOPE)
                self.assertTrue(link["is_synthetic"])
                if link["status"] == "linked":
                    expected = dict(by_id[link["stock_home_id"]])
                    expected.pop("synthetic_home_id")
                    self.assertEqual(c["stock_fabric"], expected)
                    self.assertTrue(c["stock_epc"]["epc_is_synthetic"])
                else:
                    self.assertTrue(link["reason"])
                    self.assertNotIn("stock_fabric", c)
            db = Path(tmp) / "cases.sqlite"
            first = sqlstore.SqlStore(str(path), str(db))
            first.db.close()
            reopened = sqlstore.SqlStore(str(path), str(db))
            try:
                keys = (
                    "synthetic_stock_anchor_id",
                    "stock_link",
                    "stock_fabric",
                    "stock_epc",
                    "home",
                    "history",
                    "decision",
                )
                for c in data["cases"]:
                    restored: Mapping[str, object] = reopened.cases[c["id"]]
                    self.assertEqual(
                        {key: c.get(key) for key in keys}, {key: restored.get(key) for key in keys}
                    )
            finally:
                reopened.db.close()


if __name__ == "__main__":
    unittest.main()
