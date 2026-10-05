import csv
import tempfile
import unittest
from pathlib import Path

from prototype.properwarm.storage import Store


CASE_HEADERS = [
    "candidate_id",
    "property_ref",
    "current_status",
    "owner",
    "locality",
    "archetype_id",
    "lead_supplier",
    "rag_status",
    "is_synthetic",
]
CASE_ROWS = [
    ["CAND-TEST-0001", "SYN-PROP-TEST-0001", "01 Identified", "PM-01", "Locality A", "ARC-01", "SUP-F1", "Green", "true"],
    ["CAND-TEST-0002", "SYN-PROP-TEST-0002", "01 Identified", "PM-01", "Locality B", "ARC-02", "SUP-F2", "Amber", "true"],
]


def write_csv(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "source"
        self.source.mkdir()
        write_csv(self.source / "candidate-lifecycle.csv", CASE_HEADERS, CASE_ROWS)
        write_csv(
            self.source / "safety-holds.csv",
            ["candidate_id", "is_synthetic", "hold_status_in_tracker"],
            [["CAND-TEST-0001", "true", "Open"]],
        )
        self.store = Store(self.root / "data" / "prototype.sqlite3", self.source)

    def test_required_safety_source_is_fail_closed(self) -> None:
        source_without_holds = self.root / "missing-holds"
        source_without_holds.mkdir()
        write_csv(
            source_without_holds / "candidate-lifecycle.csv", CASE_HEADERS, CASE_ROWS
        )

        with self.assertRaisesRegex(FileNotFoundError, "safety-hold data"):
            Store(self.root / "missing.sqlite3", source_without_holds)

    def test_seed_source_row_metadata_is_preserved(self) -> None:
        headers = [*CASE_HEADERS, "source_row"]
        rows = [row + [str(20 + offset * 10)] for offset, row in enumerate(CASE_ROWS)]
        write_csv(self.source / "candidate-lifecycle.csv", headers, rows)
        store = Store(self.root / "lineage.sqlite3", self.source)

        self.assertEqual(store.get_case("CAND-TEST-0001")["source_row"], 20)
        self.assertEqual(store.get_case("CAND-TEST-0002")["source_row"], 30)

    def test_gate_and_safety_hold_block_then_allow_synthetic_progression(self) -> None:
        missing_gate = self.store.advance_case("CAND-TEST-0002", "Local reviewer")
        self.assertFalse(missing_gate["advanced"])
        self.assertIn("Named owner", missing_gate["missing"])

        self.store.update_controls(
            "CAND-TEST-0002", {"named_owner": True}, "Local reviewer"
        )
        self.assertTrue(
            self.store.advance_case("CAND-TEST-0002", "Local reviewer")["advanced"]
        )

        held = self.store.advance_case("CAND-TEST-0001", "Local reviewer")
        self.assertFalse(held["advanced"])
        self.assertIn("Active safety hold", held["missing"])

    def test_close_requires_investigation_and_reopen_resets_counter_not_history(self) -> None:
        results = [
            self.store.record_appointment(
                "CAND-TEST-0001",
                "resident_no_access_verified",
                True,
                "Local reviewer",
            )
            for _ in range(6)
        ]
        self.assertEqual([result["review_required"] for result in results], [False] * 5 + [True])
        with self.assertRaisesRegex(ValueError, "human investigation"):
            self.store.close_case(
                "CAND-TEST-0001", "Local reviewer", "human_review_completed"
            )

        self.store.record_review("CAND-TEST-0001", "Local reviewer")
        self.store.close_case(
            "CAND-TEST-0001", "Local reviewer", "human_review_completed"
        )
        closed = self.store.get_case("CAND-TEST-0001")
        self.assertFalse(closed["active"])
        self.assertEqual(closed["eligible_count"], 0)
        self.assertEqual(len(closed["appointment_events"]), 7)

        self.store.reopen_case("CAND-TEST-0001", "Local reviewer")
        self.store.record_appointment(
            "CAND-TEST-0001",
            "resident_no_access_verified",
            True,
            "Local reviewer",
        )
        reopened = self.store.get_case("CAND-TEST-0001")
        self.assertTrue(reopened["active"])
        self.assertEqual(reopened["eligible_count"], 1)
        self.assertEqual(len(reopened["appointment_events"]), 9)

    def test_commit_time_conflict_rolls_back_all_rows(self) -> None:
        rows = [
            {
                "candidate_id": "CAND-NEW-0001",
                "property_ref": "SYN-PROP-NEW-0001",
                "current_status": "01 Identified",
                "owner": "PM-01",
                "locality": "Locality A",
                "archetype_id": "ARC-01",
                "lead_supplier": "SUP-F1",
                "rag_status": "Green",
                "source_row": 2,
            },
            {
                "candidate_id": "CAND-TEST-0002",
                "property_ref": "SYN-PROP-TEST-0002",
                "current_status": "01 Identified",
                "owner": "PM-01",
                "locality": "Locality B",
                "archetype_id": "ARC-02",
                "lead_supplier": "SUP-F2",
                "rag_status": "Amber",
                "source_row": 3,
            },
        ]

        with self.assertRaisesRegex(ValueError, "nothing was imported"):
            self.store.import_cases(
                rows, "conflict.xlsx", "0" * 64, 0, "Local reviewer"
            )
        self.assertIsNone(self.store.get_case("CAND-NEW-0001"))


if __name__ == "__main__":
    unittest.main()
