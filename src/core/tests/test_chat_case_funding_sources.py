import unittest

from zava_forward.core.chat_panel import permitted_sources
from zava_forward.core.export_fields import chat_case


class ChatCaseFundingSourcesTests(unittest.TestCase):
    DETAIL = {
        "id": "ZF-1",
        "funding": {"route": "ECO4", "status": "not started", "internal": "drop"},
        "funding_ok": False,
        "work": {
            "blockers": [
                {
                    "step": "Funding",
                    "reason": "Grant not claimed",
                    "owner": "finance",
                    "email": "a@b.c",
                }
            ]
        },
    }

    def test_funding_and_blockers_are_citable_and_closed(self) -> None:
        sources = permitted_sources("ZF-1", chat_case(self.DETAIL))
        self.assertEqual(sources["ZF-1/funding.route"], "ECO4")
        self.assertEqual(sources["ZF-1/funding_ok"], "False")
        self.assertEqual(sources["ZF-1/blockers.0.reason"], "Grant not claimed")
        self.assertFalse([k for k in sources if "internal" in k or "email" in k])

    def test_malformed_blocker_field_refuses(self) -> None:
        bad = {"id": "ZF-1", "work": {"blockers": [{"step": {"x": 1}}]}}
        with self.assertRaises(ValueError):
            chat_case(bad)

    def test_malformed_shapes_refuse_instead_of_dropping(self) -> None:
        for bad in (
            {"id": "ZF-1", "funding": "ECO4"},
            {"id": "ZF-1", "work": []},
            {"id": "ZF-1", "work": {"blockers": "none"}},
            {"id": "ZF-1", "work": {"blockers": ["x"]}},
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                chat_case(bad)

    def test_long_blocker_lists_are_capped_with_the_true_total(self) -> None:
        many = {"id": "ZF-1", "work": {"blockers": [{"step": f"s{i}"} for i in range(9)]}}
        sources = permitted_sources("ZF-1", chat_case(many))
        self.assertEqual(sources["ZF-1/blockers_total"], "9")
        self.assertIn("ZF-1/blockers.5.step", sources)
        self.assertNotIn("ZF-1/blockers.6.step", sources)


if __name__ == "__main__":
    unittest.main()
