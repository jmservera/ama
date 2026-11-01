import unittest

from zava_forward.core import chat_case_answers as cca
from zava_forward.core.chat_case_answers import answer, case_facts


def _detail(count: int) -> dict:
    return dict(
        stage="Survey",
        status="Blocked",
        work=dict(
            blockers=[
                dict(
                    step=f"Step {i}",
                    reason=f"Reason {i}",
                    owner=f"Owner {i}",
                    responsible_role="Coordinator",
                    next_action=f"Do {i}",
                    source=f"Source {i}",
                    current_stop=True,
                )
                for i in range(count)
            ]
        ),
    )


class CitationBoundTests(unittest.TestCase):
    def test_many_blockers_keep_citations_within_the_storage_limit(self) -> None:
        facts = case_facts(_detail(6), reason_visible=True)
        kind, text, cites = answer("ZF-1", "Why is this case blocked?", facts)
        self.assertEqual(kind, "answer")
        self.assertLessEqual(len(cites), cca.MAX_CITATIONS)
        self.assertEqual(len(cites), len(set(cites)))
        self.assertIn(cca.TRUNCATED, text)
        shown = [f"Step {i}" for i in range(6) if f"Step {i}:" in text]
        self.assertTrue(shown)
        for i in range(6):
            if f"Step {i}:" in text:
                self.assertIn(f"ZF-1/work.blockers.{i}.step", cites)

    def test_few_blockers_are_not_truncated(self) -> None:
        facts = case_facts(_detail(2), reason_visible=True)
        _, text, cites = answer("ZF-1", "Why is this case blocked?", facts)
        self.assertNotIn(cca.TRUNCATED, text)
        self.assertLessEqual(len(cites), cca.MAX_CITATIONS)


if __name__ == "__main__":
    unittest.main()
