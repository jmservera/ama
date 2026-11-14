"""Grant, PAS 2035 sign-off and sensor chat questions ground on the case packet (Refs #164)."""

import re
import unittest
from typing import Any

from zava_forward.core.chat_case_answers import RULES_FIRST, answer, case_facts, intent
from zava_forward.core.chat_panel import ChatPanel

DETAIL: dict[str, Any] = dict(
    stage="Technical",
    status="Waiting",
    owner="Sam Case",
    documents=[dict(kind="Survey"), dict(kind="EPC")],
    grants=[
        dict(
            id="GR-1",
            scheme="ECO4",
            state="Claimable",
            eligibility=dict(outcome="Eligible", source="EV-77"),
            pending=dict(to="Claimed"),
        )
    ],
    technical=dict(
        design_version=2,
        signoffs=dict(design=dict(status="Signed off", by="Dee Coord")),
    ),
    hazards=[dict(category="Damp and mould", owner="Hazard Owner", state="Open", released=False)],
    sensor_review_drafts=[dict(task_key="damp-1", state="draft")],
)


class Isolation:
    def current_user(self, user: Any) -> Any:
        return user

    def case_facts(self, user: Any, case_id: str) -> dict[str, str]:
        return dict(case_facts(DETAIL, reason_visible=True))


class CaseDomainGroundingTests(unittest.TestCase):
    facts = case_facts(DETAIL, reason_visible=True)

    def ask(self, question: str) -> tuple[str, str, list[str]]:
        kind, text, cites = answer("ZF-1", question, self.facts)
        return str(kind), str(text), list(cites)

    def test_intents_route_rules_first(self) -> None:
        for question, name in (
            ("Is this grant ready to claim?", "claim"),
            ("Has the PAS 2035 coordinator signed off?", "pas2035"),
            ("What does the damp sensor evidence show?", "sensor"),
        ):
            with self.subTest(question=question):
                self.assertEqual(intent(question), name)
                self.assertIn(name, RULES_FIRST)

    def test_claim_readiness_cites_grant_fields_and_stays_bounded(self) -> None:
        kind, text, cites = self.ask("Is the grant claim ready?")
        self.assertEqual(kind, "answer")
        self.assertIn("[Origin: decision_rule]", text)
        self.assertIn("ECO4: state Claimable. Eligibility: Eligible", text)
        self.assertIn("Change waiting for approval: Claimed", text)
        self.assertIn("ZF-1/grants.0.eligibility", cites)
        self.assertIn("workflow/domain-boundary", cites)
        self.assertIn("cannot submit, claim or approve", text)

    def test_pas2035_signoff_states_role_and_person_without_approving(self) -> None:
        kind, text, cites = self.ask("Who must give the PAS 2035 coordinator sign-off?")
        self.assertEqual(kind, "answer")
        self.assertIn(
            "Design: Signed off by Dee Coord. Responsible role: Retrofit Coordinator", text
        )
        self.assertIn("Coordination: Not given", text)
        self.assertIn("ZF-1/pas2035.signoff.design.status", cites)
        self.assertIn("does not confirm a legal duty", text)

    def test_sensor_question_uses_damp_hazard_and_draft_fields(self) -> None:
        kind, text, cites = self.ask("What sensor or ventilation evidence is there?")
        self.assertEqual(kind, "answer")
        self.assertIn("Damp and mould, Open. Owner: Hazard Owner", text)
        self.assertIn("Sensor review draft damp-1: draft, manual review only", text)
        self.assertIn("ZF-1/sensor.0.state", cites)
        self.assertIn("do not establish a root cause", text)

    def test_missing_domain_records_say_so_and_invent_nothing(self) -> None:
        facts = case_facts(dict(stage="Survey"), reason_visible=True)
        for question, phrase in (
            ("Is the grant claimable?", "No grant record"),
            ("Has the coordinator signed off?", "No design or sign-off"),
            ("Any damp sensor evidence?", "No damp, ventilation or sensor evidence"),
        ):
            with self.subTest(question=question):
                kind, text, _ = answer("ZF-1", question, facts)
                self.assertEqual(kind, "answer")
                self.assertIn(phrase, text)
                self.assertIn("[Origin: decision_rule]", text)
                self.assertFalse(
                    re.search(r"[£\d]{2,}", text.replace("ZF-1", "").replace("PAS 2035", ""))
                )

    def test_panel_labels_domain_rules_answer_as_decision_rule(self) -> None:
        panel = ChatPanel(Isolation())
        found = panel._rules_answer({}, "ZF-1", "Is the grant claim ready?", None)
        assert found is not None
        body, cites, sources = found
        self.assertIn("[Origin: decision_rule]", body)
        self.assertTrue(cites and set(cites) <= set(sources))
        reply = panel._reply("answer", body, cites, "workflow-only", sources, "decision-rules")
        self.assertEqual(reply["answer_origin"], "decision_rule")
        self.assertIn("not generative AI", reply["answer_source_label"])
        generative = panel._reply("answer", "x", cites, "model", sources, "generative-grounded")
        self.assertEqual(generative["answer_origin"], "generative_model")


if __name__ == "__main__":
    unittest.main()
