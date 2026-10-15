"""Provenance register, PII-free and public/private separation checks for synthetic data."""
import csv
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "docs/reference/research/retrofit-synthetic-data"
REGISTER = json.loads((PACK / "provenance-register.json").read_text())

PII_PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "uk_phone": re.compile(r"(?<!\d)(?:\+44|0)\s?\d{3,4}\s?\d{3}\s?\d{3,4}(?!\d)"),
    "ni_number": re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b"),
    "uk_postcode": re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b"),
}


def scan(text):
    return [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]


def dataset(ds_id):
    return next(d for d in REGISTER["datasets"] if d["id"] == ds_id)


class ProvenanceRegisterTests(unittest.TestCase):
    def test_every_dataset_has_visibility_and_dictionary_entry(self):
        dictionary = (PACK / REGISTER["dictionary"]).read_text()
        for d in REGISTER["datasets"]:
            self.assertIn(d["visibility"], {"public", "private", "not-generated"}, d["id"])
            path, _, anchor = d["data_dictionary"].partition("#")
            self.assertEqual(path, REGISTER["dictionary"], d["id"])
            if anchor:
                headings = {re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-")
                            for h in re.findall(r"^#+ (.+)$", dictionary, re.M)}
                self.assertIn(anchor, headings, d["id"])

    def test_sensor_and_chat_data_are_covered(self):
        self.assertEqual(dataset("DS-SENSOR")["visibility"], "not-generated")
        self.assertTrue(dataset("DS-SENSOR")["open_item"])
        self.assertIn("assistant_events", dataset("DS-ASSISTANT-RUNTIME")["location"])

    def test_external_sources_record_licence_date_and_attribution(self):
        ids = {s["id"] for s in REGISTER["sources"]}
        for s in REGISTER["sources"]:
            self.assertTrue(s["licence"] and s["attribution"] and s["url"], s["id"])
            if s["retrieval_date"] is None:
                self.assertIn("open item", s["verification"], s["id"])
            else:
                self.assertRegex(s["retrieval_date"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(next(s for s in REGISTER["sources"] if s["id"] == "SRC-OSM")["licence"], "ODbL 1.0")
        for d in REGISTER["datasets"]:
            self.assertLessEqual(set(d["sources"]) if "sources" in d else set(), ids, d["id"])
        self.assertTrue(REGISTER["open_items"])

    def test_every_public_csv_is_registered_labelled_and_pii_free(self):
        pack = dataset("DS-OPS-PACK")
        exempt = set(pack["label_exempt"])
        files = sorted(PACK.glob(pack["files_glob"]))
        self.assertGreaterEqual(len(files), 14)
        for f in files:
            with f.open(newline="", encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertTrue(rows, f.name)
            if f.name not in exempt:
                unlabelled = [i for i, r in enumerate(rows, 2) if (r.get(pack["label_field"]) or "").lower() != "true"]
                self.assertEqual(unlabelled, [], f"{f.name} has unlabelled rows")
            for i, r in enumerate(rows, 2):
                hits = scan(" ".join(v or "" for v in r.values()))
                self.assertEqual(hits, [], f"{f.name} line {i}: {hits}")
        for f in [PACK / "manifest.json", *sorted((ROOT / "mvp/evals").glob("*.json"))]:
            self.assertEqual(scan(f.read_text()), [], f.name)

    def test_checker_detects_real_person_patterns(self):
        for sample, kind in [("jo.smith@example.com", "email"), ("call 07700 900123", "uk_phone"),
                             ("AB 12 34 56 C", "ni_number"), ("NE5 2QS", "uk_postcode")]:
            self.assertIn(kind, scan(sample), sample)
        self.assertEqual(scan("SYN-PROP-000123 R-SYN-00001"), [])

    def test_private_register_is_labelled_and_has_no_person_fields(self):
        d = dataset("DS-STOCK-REGISTER")
        path = ROOT / d["location"] / "private-north-east-stock-register.csv"
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            names = reader.fieldnames
            self.assertFalse([n for n in names if re.search(r"resident|tenant|person|email|phone|surname", n, re.I)])
            bad = [r["synthetic_home_id"] for r in reader
                   if r["is_synthetic"].lower() != "true" or r["actual_owner_or_tenure_verified"].lower() != "false"]
        self.assertEqual(bad[:5], [])

    def test_private_and_public_outputs_are_separated(self):
        gitignore = (ROOT / ".gitignore").read_text()
        self.assertIn("/mvp/data/", gitignore)
        self.assertIn("support/synthetic-data/**/answer-key/", gitignore)
        for d in REGISTER["datasets"]:
            loc = d["location"]
            if d["visibility"] == "private" and "/" in loc and not loc.startswith("serving"):
                self.assertTrue(loc.startswith("support/") or loc == "mvp/data/", d["id"])
            if d["visibility"] == "public":
                self.assertTrue(loc.startswith(("docs/", "mvp/evals/")), d["id"])
        stock = dataset("DS-STOCK-REGISTER")["location"]
        self.assertTrue((ROOT / stock / "README-private.txt").read_text().startswith("PRIVATE REPOSITORY DATA"))
        # real map addresses must not leak into public docs
        sample = re.compile(r"SYN-NE-\d{6}")
        for f in list(PACK.glob("*.csv")) + list(PACK.glob("*.md")):
            self.assertIsNone(sample.search(f.read_text()) if f.name != "data-dictionary.md" else None, f.name)
        self.assertFalse(list((ROOT / "mvp/evals").glob("*private*")))


if __name__ == "__main__":
    unittest.main()
