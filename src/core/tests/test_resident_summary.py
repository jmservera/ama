import unittest

from zava_forward.core import resident_summary as rsum
from zava_forward.core.resident_documents import (
    DocumentFacts,
    DocumentRequest,
    PresentedDocument,
)


class TimelineTests(unittest.TestCase):
    def test_current_step_follows_stage(self) -> None:
        steps = rsum.timeline("Funding check", False)
        self.assertEqual(
            [s["state"] for s in steps], ["completed"] * 3 + ["current"] + ["upcoming"] * 2
        )

    def test_unknown_stage_marks_no_current_step(self) -> None:
        self.assertEqual({s["state"] for s in rsum.timeline("Mystery", False)}, {"unknown"})

    def test_closed_case_is_all_completed(self) -> None:
        self.assertEqual({s["state"] for s in rsum.timeline("Closing down", True)}, {"completed"})

    def test_every_known_stage_maps_to_a_step(self) -> None:
        from zava_forward.core.insights import STAGE_ORDER

        self.assertEqual(set(STAGE_ORDER), set(rsum.STAGE_STEP))


class DocumentTests(unittest.TestCase):
    def facts(self) -> DocumentFacts:
        return DocumentFacts(
            requests=(DocumentRequest("REQ-1", "Proof of occupancy", "Show a bill"),),
            documents=(PresentedDocument("DOC-1", "Energy assessment", False, "clean", ()),),
        )

    def test_missing_request_is_an_action_and_summary_counts_it(self) -> None:
        docs = rsum.documents_view(self.facts())
        self.assertEqual(docs["requests"][0]["state"], "missing")
        needed = rsum.needed_from_you("Survey booked", False, docs)
        self.assertEqual([n["kind"] for n in needed], ["document"])
        text = rsum.rules_summary(
            "1 Alder Close", "Survey booked", "p.", "n.", False, ["Loft"], docs, needed
        )
        self.assertIn("1 request recorded, 1 missing", text["text"])
        self.assertIn("Planned improvements: Loft.", text["text"])
        self.assertEqual(text["label"], "Summary by rules. Not an instruction.")

    def test_unknown_documents_are_not_shown_as_empty(self) -> None:
        docs = rsum.documents_view(DocumentFacts())
        self.assertIsNone(docs["requests"])
        self.assertIsNone(docs["presented"])
        text = rsum.rules_summary("", "", "p.", "n.", False, [], docs, [])
        self.assertIn("not shown in this view", text["text"])
        self.assertIn("none listed", text["text"])

    def test_decision_stage_states_reason_owner_and_next_action(self) -> None:
        docs = rsum.documents_view(DocumentFacts(requests=(), documents=()))
        item = rsum.needed_from_you("Waiting for resident decision", False, docs)[0]
        for part in ("Reason:", "Owner:", "Next action:"):
            self.assertIn(part, item["text"])


if __name__ == "__main__":
    unittest.main()
