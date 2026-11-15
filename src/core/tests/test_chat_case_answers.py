import unittest
from unittest.mock import MagicMock

from zava_forward.core import chat_case_answers as cca
from zava_forward.core.chat_case_answers import answer, case_facts, intent, sensor_facts
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import ChatPanel


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


class DomainAnswerTests(unittest.TestCase):
    def test_sensor_answer_cites_documents_only_when_survey_is_listed(self) -> None:
        for documents, cited in (("EPC", False), ("EPC, Survey", True)):
            with self.subTest(documents=documents):
                facts = {"stage": "Survey", "documents": documents}
                _, _, cites = answer("ZF-1", "Is there any damp or sensor evidence?", facts)
                self.assertEqual("ZF-1/documents" in cites, cited)

    def test_claim_without_grants_keeps_the_domain_footer(self) -> None:
        _, text, cites = answer("ZF-1", "What is the grant claim position?", {"stage": "Survey"})
        self.assertIn("A person decides.", text)
        self.assertIn(cca.DOMAIN_BOUNDARY, cites)

    def test_sensor_conflict_preempts_damp_fallback_while_missing_reading_delegates_to_damp(
        self,
    ) -> None:
        detail: dict[str, object] = dict(
            stage="Quality",
            hazards=[dict(category="Damp and mould", owner="Safety lead", state="open")],
            sensor_review_drafts=[dict(task_key="quality.sensor_review", state="pending")],
        )
        base = case_facts(detail, reason_visible=True)
        conflict_facts = {
            **base,
            **sensor_facts(
                dict(
                    state="ok",
                    conflict_notice="Two retained readings at 2026-11-14T10:00:00Z disagree.",
                    grounding=dict(
                        not_retained_text="mould_risk_index is not retained on the case record."
                    ),
                )
            ),
        }
        kind, text, cites = answer("ZF-1", "What are the sensor readings?", conflict_facts)
        self.assertEqual(kind, "answer")
        self.assertIn("Retained sensor readings conflict, so no single value is selected.", text)
        self.assertNotIn("No retained sensor reading is shown", text)
        self.assertNotIn("[Origin: decision_rule]", text)
        self.assertIn("ZF-1/sensor.conflict", cites)
        self.assertIn("ZF-1/sensor.not_retained", cites)
        self.assertNotIn("ZF-1/sensor.detail", cites)
        self.assertNotIn(cca.DOMAIN_BOUNDARY, cites)

        declined_facts = {
            **base,
            **sensor_facts(
                dict(
                    state="withheld",
                    detail="Monitoring consent is declined; no values are shown.",
                    grounding={},
                )
            ),
        }
        kind2, text2, cites2 = answer("ZF-1", "What are the sensor readings?", declined_facts)
        self.assertEqual(kind2, "answer")
        self.assertIn(
            "No retained sensor reading is shown for this case. "
            "Monitoring consent is declined; no values are shown.",
            text2,
        )
        self.assertIn("[Origin: decision_rule]", text2)
        self.assertIn("ZF-1/sensor.detail", cites2)
        self.assertIn("ZF-1/hazards.0.category", cites2)
        self.assertIn("ZF-1/sensor.0.state", cites2)
        self.assertIn(cca.DOMAIN_BOUNDARY, cites2)

    def test_sensor_rules_answer_preserves_skill_lens_and_citation_kinds(self) -> None:
        detail: dict[str, object] = dict(
            stage="Quality",
            hazards=[dict(category="Damp and mould", owner="Safety lead", state="open")],
            sensor_review_drafts=[dict(task_key="quality.sensor_review", state="pending")],
        )
        base = case_facts(detail, reason_visible=True)
        user: dict[str, object] = {"id": "emp-1", "role": "quality"}
        iso = MagicMock(spec=ChatIsolation)
        iso.current_user.return_value = user
        panel = ChatPanel(iso)

        iso.case_facts.return_value = {
            **base,
            **sensor_facts(
                dict(
                    state="ok",
                    conflict_notice="Two retained readings at 2026-11-14T10:00:00Z disagree.",
                    grounding=dict(
                        not_retained_text="mould_risk_index is not retained on the case record."
                    ),
                )
            ),
        }
        conflict_res = panel._rules_answer(
            user, "ZF-1", "What are the sensor readings?", "funding-evidence"
        )
        assert conflict_res is not None
        c_body, c_cites, c_pool = conflict_res
        self.assertIn("Retained sensor readings conflict, so no single value is selected.", c_body)
        self.assertIn("ZF-1/sensor.conflict", c_cites)
        self.assertNotIn("ZF-1/sensor.detail", c_cites)
        self.assertEqual(set(c_cites), set(c_pool))
        self.assertEqual(ChatPanel._source_kind("ZF-1/sensor.conflict"), "decision-rule")

        iso.case_facts.return_value = {
            **base,
            **sensor_facts(
                dict(
                    state="withheld",
                    detail="Monitoring consent is declined; no values are shown.",
                    grounding={},
                )
            ),
        }
        fallback_res = panel._rules_answer(
            user, "ZF-1", "What are the sensor readings?", "funding-evidence"
        )
        assert fallback_res is not None
        f_body, f_cites, f_pool = fallback_res
        self.assertIn("No retained sensor reading is shown for this case.", f_body)
        self.assertIn("ZF-1/sensor.detail", f_cites)
        self.assertIn("ZF-1/hazards.0.category", f_cites)
        self.assertIn("ZF-1/sensor.0.state", f_cites)
        self.assertIn(cca.DOMAIN_BOUNDARY, f_cites)
        self.assertEqual(set(f_cites), set(f_pool))
        self.assertEqual(ChatPanel._source_kind("ZF-1/sensor.detail"), "case-record")
        self.assertEqual(ChatPanel._source_kind("ZF-1/sensor.0.state"), "case-record")
        self.assertEqual(ChatPanel._source_kind("ZF-1/hazards.0.category"), "decision-rule")
        self.assertEqual(ChatPanel._source_kind(cca.DOMAIN_BOUNDARY), "workflow-rule")

        iso.case_facts.return_value = {
            **base,
            **sensor_facts(
                dict(
                    state="ok",
                    grounding=dict(
                        citation="sensor:ZF-1:r1",
                        values=dict(
                            temperature_c="17.4",
                            humidity_pct="72",
                            observed_at="2026-11-14T10:00:00Z",
                        ),
                        source_text="Synthetic living-room logger (uncalibrated).",
                        not_retained_text="mould_risk_index is not retained on the case record.",
                    ),
                )
            ),
        }
        clean_res = panel._rules_answer(
            user, "ZF-1", "What are the sensor readings?", "funding-evidence"
        )
        assert clean_res is not None
        ok_body, ok_cites, ok_pool = clean_res
        self.assertIn("Reading source: Synthetic living-room logger (uncalibrated).", ok_body)
        self.assertIn("ZF-1/sensor.source", ok_cites)
        self.assertEqual(set(ok_cites), set(ok_pool))
        self.assertEqual(ChatPanel._source_kind("ZF-1/sensor.source"), "decision-rule")
        self.assertEqual(ChatPanel._source_kind("ZF-1/sensor.latest.citation"), "case-record")


if __name__ == "__main__":
    unittest.main()
