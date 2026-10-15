import json
import unittest

from zava_forward.core.chat_panel import LABEL, parse_reply, permitted_sources


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


class LabelTests(unittest.TestCase):
    def test_label_matches_the_acceptance_criterion(self) -> None:
        self.assertEqual(LABEL, "AI suggestion, not approved")


if __name__ == "__main__":
    unittest.main()
