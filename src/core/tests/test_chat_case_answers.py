import unittest

from zava_forward.core import chat_case_answers as cca
from zava_forward.core.chat_case_answers import answer, case_facts


def _detail(count: int) -> dict[str, object]:
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

    def _assert_supported_prefix(self, question: str, detail: dict[str, object]) -> None:
        facts = case_facts(detail, reason_visible=True)
        kind, text, cites = answer("ZF-1", question, facts)
        self.assertEqual(kind, "answer")
        self.assertLessEqual(len(cites), cca.MAX_CITATIONS)
        self.assertIn(cca.TRUNCATED, text)
        self.assertTrue(cites)
        self.assertIn("* ", text)

    def test_missing_question_keeps_a_cited_prefix(self) -> None:
        detail = dict(
            stage="Survey",
            gate=[f"Gate {i}" for i in range(8)],
            checklist=[dict(kind=f"Item {i}", present=False) for i in range(4)],
            technical_missing=[f"Gap {i}" for i in range(9)],
        )
        self._assert_supported_prefix("What is missing on this case?", detail)

    def test_funding_question_keeps_a_cited_prefix(self) -> None:
        detail = _detail(0)
        detail.update(funding_ok=False, funding=dict(status="Not started"))
        detail["work"] = dict(
            blockers=[
                dict(
                    step=f"Funding {i}",
                    reason=f"R{i}",
                    owner=f"O{i}",
                    source="Funding",
                    next_action=f"N{i}",
                    responsible_role=f"Role{i}",
                )
                for i in range(8)
            ]
        )
        self._assert_supported_prefix("Why is funding not started yet?", detail)


if __name__ == "__main__":
    unittest.main()
