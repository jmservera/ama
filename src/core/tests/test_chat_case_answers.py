import unittest

from zava_forward.core import chat_case_answers as cca
from zava_forward.core.chat_case_answers import answer, case_facts, intent


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
        detail: dict[str, object] = dict(
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

    def test_only_explicit_true_reads_as_confirmed_funding(self) -> None:
        for value, expected in (
            (True, "confirmed"),
            (False, "not confirmed"),
            (None, "not confirmed"),
            ("yes", "not confirmed"),
            ("false", "not confirmed"),
            (1, "not confirmed"),
        ):
            with self.subTest(value=value):
                facts = case_facts({"funding_ok": value}, reason_visible=False)
                self.assertEqual(facts["funding_ok"], expected)
        self.assertNotIn("funding_ok", case_facts({}, reason_visible=False))


class UnblockTests(unittest.TestCase):
    BANNED = ("gate", "hold", "provenance", "trace", "snapshot", "envelope")

    def _facts(self) -> dict[str, str]:
        detail = _detail(3)
        detail["hazards"] = [dict(category="Damp", owner="Safety lead", state="open")]
        return case_facts(detail, reason_visible=True)

    def test_unblock_and_safety_questions_list_stops_and_human_route(self) -> None:
        for question in (
            "what can I do to unblock this case?",
            "how can we fix this safety? Should we schedule a visit?",
            "How can we fix this safety issue?",
        ):
            with self.subTest(question=question):
                kind, text, cites = answer("ZF-1", question, self._facts())
                self.assertEqual(kind, "answer")
                self.assertIn("cannot book a visit or approve a safety step", text)
                self.assertIn("Step 0", text)
                self.assertIn("ZF-1/hazards.0.category", cites)
                for word in self.BANNED:
                    self.assertNotIn(word, text.casefold(), word)

    def test_owner_and_status_questions_about_visits_keep_their_intent(self) -> None:
        self.assertEqual(intent("Who owns the safety visit?"), "owner")
        self.assertEqual(intent("What is the status of the scheduled visit?"), "status")

    def test_plain_blocked_question_is_unchanged(self) -> None:
        _, text, _ = answer("ZF-1", "Why is this case blocked?", self._facts())
        self.assertNotIn("cannot book a visit", text)


if __name__ == "__main__":
    unittest.main()
