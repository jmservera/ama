"""Epic #165: seeded synthetic cohort fixtures round-trip through the importer deterministically."""

import hashlib
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic import scale_fixture, stock_fabric, stock_register

from zava_forward.importer.export import compare
from zava_forward.importer.mapping import Field, Structure, preview_bytes
from zava_forward.importer.quarantine import QuarantineStore
from zava_forward.importer.xlsx import write_workbook

SEED = 165
SIZE = 40
POSTCODE = re.compile(r"[A-Za-z]{1,2}\d[A-Za-z\d]? ?\d[A-Za-z]{2}")

COHORT = Structure(
    name="synthetic-cohort",
    sheet="Cohort",
    key="reference",
    fields=(
        Field("reference", ("ref", "home id")),
        Field("address", ("property address",)),
        Field("postcode", ("post code",), pattern=POSTCODE),
        Field("stage", ()),
        Field("dwelling_type", ("archetype",)),
        Field("age_band", ()),
        Field("construction", ()),
        Field("heating", ()),
        Field("preferred_channel", ("contact channel",)),
        Field("adjustment", ("accessibility adjustment",)),
    ),
)
HEADER = [f.name for f in COHORT.fields]


def cohort_rows(seed: int = SEED, size: int = SIZE) -> list[list[str]]:
    homes = list(scale_fixture.homes(size, seed))
    households = list(scale_fixture.households(size, seed))
    register = [
        {**r, "synthetic_home_id": h["id"]}
        for r, h in zip(stock_register.rows(size, seed), homes, strict=True)
    ]
    fabrics = stock_fabric.fabric_rows(register, seed)
    out = [HEADER]
    for home, hh, fab in zip(homes, households, fabrics, strict=True):
        out.append(
            [
                home["id"],
                home["address"],
                home["postcode"],
                home["stage"],
                fab["dwelling_type"],
                fab["age_band"],
                fab["construction"],
                fab["heating"],
                hh["preferred_channel"],
                hh["adjustment"],
            ]
        )
    return out


def workbook(seed: int = SEED, size: int = SIZE) -> bytes:
    return write_workbook({"Cohort": cohort_rows(seed, size)})


def keyed(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {r["reference"]: r for r in rows}


class SyntheticSeedImporterRoundTripTests(unittest.TestCase):
    def setUp(self) -> None:
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)

    def store(self, name: str = "import.db") -> QuarantineStore:
        conn = sqlite3.connect(self.folder / name)
        self.addCleanup(conn.close)
        store = QuarantineStore(conn)
        store.create_schema()
        return store

    def import_once(self, store: QuarantineStore, data: bytes, n: int) -> str:
        preview = preview_bytes("cohort.xlsx", data, COHORT)
        self.assertEqual((preview.conflicts, len(preview.to_fix)), ([], 0))
        staged = store.stage(preview, f"Stager {n}")
        return store.approve(staged.batch_id, f"Approver {n}").batch_id

    def test_workbook_bytes_are_deterministic_per_seed(self) -> None:
        self.assertEqual(cohort_rows(), cohort_rows())
        self.assertNotEqual(cohort_rows(), cohort_rows(seed=SEED + 1))

    def test_roundtrip_preserves_property_archetype_and_resident_preferences(self) -> None:
        expected = cohort_rows()
        store = self.store()
        batch = self.import_once(store, workbook(), 1)
        rows = store.rows(batch)
        self.assertEqual(len(rows), SIZE)
        for source, stored in zip(expected[1:], rows, strict=True):
            self.assertEqual(list(stored.values()), source)
            self.assertEqual(list(stored), HEADER)
        self.assertTrue(all(r["reference"].startswith("ZF-") for r in rows))
        self.assertTrue(all(r["postcode"].startswith("TE") for r in rows))
        self.assertTrue(all(r["address"].endswith("Test Road") for r in rows))
        self.assertTrue(all(r["dwelling_type"] and r["age_band"] for r in rows))
        self.assertTrue(all(r["construction"] and r["heating"] for r in rows))
        self.assertTrue(all(r["preferred_channel"] and r["adjustment"] for r in rows))
        self.assertGreater(len({r["adjustment"] for r in rows}), 1)
        record = store.get(batch)
        self.assertEqual(record.source_sha256, hashlib.sha256(workbook()).hexdigest())
        self.assertEqual(record.data_label, "synthetic-demo")

    def test_reimport_is_idempotent_for_counts_and_content(self) -> None:
        store = self.store()
        first = self.import_once(store, workbook(), 1)
        second = self.import_once(store, workbook(), 2)
        history = store.history(COHORT.name)
        self.assertEqual([b.version for b in history], [1, 2])
        self.assertEqual([b.status for b in history], ["superseded", "approved"])
        self.assertEqual(history[0].source_sha256, history[1].source_sha256)
        self.assertEqual(store.rows(first), store.rows(second))
        current = store.current(COHORT.name)
        assert current is not None
        self.assertEqual(current.batch_id, second)
        self.assertEqual(len(store.rows(current.batch_id)), SIZE)
        cur = store.conn.cursor()
        cur.execute("SELECT COUNT(DISTINCT row_key), COUNT(*) FROM import_rows")
        self.assertEqual(cur.fetchone(), (SIZE, SIZE * 2))
        diff = compare(keyed(store.rows(first)), keyed(store.rows(second)))
        self.assertEqual((diff.added, diff.removed, diff.changed), ([], [], {}))
        self.assertEqual(len(diff.unchanged), SIZE)

    def test_independent_stores_hold_identical_content_without_sharing_state(self) -> None:
        one, two = self.store("one.db"), self.store("two.db")
        a = self.import_once(one, workbook(), 1)
        self.assertEqual(two.history(COHORT.name), [])
        b = self.import_once(two, workbook(), 1)
        self.assertEqual(one.rows(a), two.rows(b))
        self.assertEqual(len(one.history(COHORT.name)), 1)
        self.assertEqual(len(two.history(COHORT.name)), 1)

    def test_changed_seed_reimport_reports_differences_not_duplicates(self) -> None:
        store = self.store()
        first = self.import_once(store, workbook(), 1)
        second = self.import_once(store, workbook(seed=SEED + 1), 2)
        self.assertEqual(len(store.rows(second)), SIZE)
        diff = compare(keyed(store.rows(first)), keyed(store.rows(second)))
        self.assertEqual((diff.added, diff.removed), ([], []))
        self.assertTrue(diff.changed)


if __name__ == "__main__":
    unittest.main()
