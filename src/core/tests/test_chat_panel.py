import json
import unittest

from zava_forward.core.chat_panel import LABEL, out_of_scope, parse_reply, permitted_sources


class PureTests(unittest.TestCase):
    SOURCES = {"ZF-1/stage": "Survey", "ZF-1/status": "Open"}

    def test_parse_keeps_only_permitted_citations(self) -> None:
        text = json.dumps(
            dict(answer="Stage is Survey.", citations=["ZF-1/stage", "ZF-2/stage", 5])
        )
        self.assertEqual(parse_reply(text, self.SOURCES), ("Stage is Survey.", ["ZF-1/stage"]))

    def test_parse_rejects_uncited_or_malformed(self) -> None:
        for text in (
            "plain text",
            "[]",
            json.dumps(dict(answer="x", citations=[])),
            json.dumps(dict(answer="x", citations=["ZF-9/stage"])),
            json.dumps(dict(answer="", citations=["ZF-1/stage"])),
            json.dumps(dict(answer=3, citations=["ZF-1/stage"])),
            json.dumps(dict(answer="x", citations="ZF-1/stage")),
        ):
            self.assertIsNone(parse_reply(text, self.SOURCES), text)

    def test_sources_flatten_projected_case_only(self) -> None:
        found = permitted_sources(
            "ZF-1", dict(stage="Survey", resident=dict(adjustment="None"), empty="")
        )
        self.assertEqual(found, {"ZF-1/stage": "Survey", "ZF-1/resident.adjustment": "None"})


class OutOfScopeTests(unittest.TestCase):
    def test_actions_are_refused_with_a_route(self) -> None:
        asks = {
            "approve": ["Approve case ZF-1 now.", "Please sign off the quality check"],
            "decide": ["Can you decide for me?"],
            "consent": ["Record the resident's consent", "Please confirm consent for ZF-1"],
            "contact": [
                "Email the resident today",
                "Could you phone the tenant?",
                "Send the letter",
            ],
            "diagnose": ["Diagnose the damp in this home"],
        }
        for kind, questions in asks.items():
            for question in questions:
                hit = out_of_scope(question)
                self.assertIsNotNone(hit, question)
                assert hit
                self.assertEqual(hit[0], kind, question)
                self.assertTrue(hit[1])

    def test_ordinary_questions_are_not_refused(self) -> None:
        for question in (
            "What stage is it?",
            "Has the resident given consent?",
            "Which measures are approved?",
            "Who is the named contact?",
            "When was the resident last contacted?",
        ):
            self.assertIsNone(out_of_scope(question), question)


class LabelTests(unittest.TestCase):
    def test_label_matches_the_acceptance_criterion(self) -> None:
        self.assertEqual(LABEL, "AI suggestion, not approved")


if __name__ == "__main__":
    unittest.main()
