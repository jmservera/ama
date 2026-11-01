import re
import unittest
from pathlib import Path
from types import SimpleNamespace

from zava_forward.core import chat_privacy as cp

DOC = (
    Path(__file__).resolve().parents[3] / "docs" / "reference" / "research" / "chat-memory-dpia.md"
)
DOC_MARKERS = {
    "message": "chat_message",
    "thread": "chat_thread",
    "memory": "chat_memory",
    "prompt": "Prompts sent to the model",
    "diagnostic_log": "Diagnostic logs",
    "audit_ledger": "Audit ledger",
}
RECORDED_PARTS = (
    re.compile(r"\bowner:\s*[A-Za-z]", re.I),
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\bref:\s*\S", re.I),
)


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}.*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    assert match, heading
    return match.group(1)


class ChatDpiaRecordGuard(unittest.TestCase):
    text: str

    """Keeps the DPIA record tied to the code and free of invented decisions (#163)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8")

    def test_every_data_map_class_is_in_the_dpia_record(self) -> None:
        self.assertEqual({r["id"] for r in cp.DATA_MAP}, set(DOC_MARKERS))
        data_map = section(self.text, "Data map")
        for ident, marker in DOC_MARKERS.items():
            self.assertIn(marker, data_map, ident)

    def test_decision_pack_records_nothing_without_owner_date_and_reference(self) -> None:
        rows = [
            r
            for r in section(self.text, "Decision pack for the DPO and Legal").splitlines()
            if re.match(r"\| D\d ", r)
        ]
        self.assertEqual([r.split("|")[1].strip() for r in rows], [f"D{n}" for n in range(1, 9)])
        for row in rows:
            cell = row.rstrip().rstrip("|").rsplit("|", 1)[1].strip()
            self.assertTrue(
                cell == "Not recorded" or all(p.search(cell) for p in RECORDED_PARTS), row
            )

    def test_unrecorded_decisions_match_unset_references(self) -> None:
        decision = cp.ChatPrivacy(SimpleNamespace(chat_repo=None), env={}).decision()  # type: ignore[no-untyped-call]
        self.assertFalse(decision["approved"])
        self.assertEqual(decision["missing"], ["dpia_ref", "lawful_basis_ref", "notice_ref"])
        self.assertIsNone(decision["retention_days"])
        self.assertIn("Not recorded", section(self.text, "Decision pack for the DPO and Legal"))

    def test_retention_is_unknown_in_the_record(self) -> None:
        for row in cp.DATA_MAP:
            if row["id"] in {"message", "thread", "memory"}:
                self.assertIn("Unknown", row["retention"])
        lines = [
            line for line in section(self.text, "Data map").splitlines() if line.startswith("|")
        ]
        markers = ("chat_message", "chat_thread", "chat_memory")
        for marker in markers:
            found = [line for line in lines if marker in line]
            self.assertTrue(found, marker)
            for line in found:
                cell = line.rstrip().rstrip("|").rsplit("|", 1)[1].strip()
                self.assertTrue(cell.startswith("Unknown"), marker)


if __name__ == "__main__":
    unittest.main()
