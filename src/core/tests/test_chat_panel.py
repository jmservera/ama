import json
import tempfile
import unittest
from pathlib import Path

import dataset
from zava_forward.core.assistants import REGISTRY
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import (
    ACTION_CLAIM,
    LABEL,
    ChatPanel,
    normalise_policy_text,
    out_of_scope,
    parse_reply,
    permitted_sources,
    skill_sources,
)
from zava_forward.core.chat_privacy import redact
from zava_forward.core.chatthreads import MAX_CONTENT
from zava_forward.core.store import Store


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

    def test_skill_lenses_never_add_case_data_or_unrelated_categories(self) -> None:
        sources = {
            "ZF-1/stage": "Survey",
            "ZF-1/home.epc": "D",
            "ZF-1/resident.adjustment": "WITHHELD-CANARY",
            "ZF-1/funding.route": "FUNDING-CANARY",
        }
        for skill in REGISTRY:
            result = skill_sources(skill, sources)
            self.assertEqual(result["ZF-1/stage"], "Survey")
            self.assertEqual(result["ZF-1/home.epc"], "D")
            self.assertNotIn("WITHHELD-CANARY", result.values())
            if skill != "funding-evidence":
                self.assertNotIn("FUNDING-CANARY", result.values())
            self.assertIn("workflow/boundaries", result)

    def test_general_sources_disclose_missing_record(self) -> None:
        sources = skill_sources("general", {})
        self.assertTrue(all(key.startswith("workflow/") for key in sources))
        self.assertIn("No case or home record", sources["workflow/visibility"])


class OutOfScopeTests(unittest.TestCase):
    def test_actions_are_refused_with_a_route(self) -> None:
        asks = {
            "approve": [
                "Approve case ZF-1 now.",
                "Please sign off the quality check",
                "I need you to approve the case.",
                "I want you to approve it.",
                "I want to approve the work.",
            ],
            "decide": ["Can you decide for me?"],
            "consent": [
                "Record the resident's consent",
                "Please confirm consent for ZF-1",
                "Mark ZF-1 as consented.",
                "I want you to mark Alice as consented.",
            ],
            "contact": [
                "Email the resident today",
                "Could you phone the tenant?",
                "Send the letter",
                "Contact Alice",
                "Phone Mrs Smith",
                "Ring Mr. Jones",
                "Call Ms Patel",
                "Contact Dr Green",
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
            "What should we call this report?",
            "What is the phone number?",
            "Explain how the consent control works.",
        ):
            self.assertIsNone(out_of_scope(question), question)

    def test_unicode_normalisation_precedes_matching(self) -> None:
        for question in (
            "I need you to \u0430\u0440\u0440r\u043eve the case",
            "I want to \u03b1\u03c1\u03c1r\u03bfve the work",
            "a\u200bp\u200cp\u200dr\u2060o\ufeffve this case",
            "\uff21\uff50\uff50\uff52\uff4f\uff56\uff45\u00a0the case",
            "I\twant\n you to\u00a0approve it",
        ):
            hit = out_of_scope(question)
            self.assertIsNotNone(hit, question)
            assert hit
            self.assertEqual(hit[0], "approve", question)
        self.assertEqual(normalise_policy_text(" \tMrs\u200b\u00a0Smith\n"), "Mrs Smith")


class ActionClaimTests(unittest.TestCase):
    def test_lexical_approval_and_consent_claims_are_detected(self) -> None:
        for answer in (
            "I have approved the case.",
            "We signed off the work.",
            "I recorded the resident's consent.",
            "I will confirm consent.",
            "The case has been approved.",
            "Consent has been recorded.",
            "I have \u0430\u0440\u0440r\u043eved the case.",
            "Consent is re\u200bcorded.",
        ):
            self.assertIsNotNone(ACTION_CLAIM.search(normalise_policy_text(answer)), answer)

    def test_non_action_answers_are_preserved(self) -> None:
        for answer in (
            "Survey booked.",
            "I cannot approve the case.",
            "Consent has not been recorded.",
            "Ask the named reviewer for approval.",
            "The resident has not given consent.",
        ):
            self.assertIsNone(ACTION_CLAIM.search(normalise_policy_text(answer)), answer)


class LabelTests(unittest.TestCase):
    def test_label_matches_the_acceptance_criterion(self) -> None:
        self.assertEqual(LABEL, "AI suggestion, not approved")


class StoredQuestionTests(unittest.TestCase):
    def test_expanding_redaction_stays_bounded_across_chat_modes(self) -> None:
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / "synthetic.json"
            path.write_text(json.dumps(dataset.DATA))
            store = Store(str(path))
            user = dataset.DATA["staff"][0]
            isolation = ChatIsolation(
                store,
                env={
                    "CHAT_DPIA_REF": "SYNTH-DPIA",
                    "CHAT_LAWFUL_BASIS_REF": "SYNTH-BASIS",
                    "CHAT_NOTICE_REF": "SYNTH-NOTICE",
                },
            )
            panel = ChatPanel(isolation)
            for identifier in ("NE1 1AA", "a@b.co", "asthma"):
                question = "x" * (MAX_CONTENT - len(identifier) - 1) + " " + identifier
                masked = redact(question)[0]
                self.assertEqual(len(question), MAX_CONTENT)
                self.assertGreater(len(masked), MAX_CONTENT)
                for skill in (None, "general", *REGISTRY):
                    with self.subTest(identifier=identifier, skill=skill):
                        tid = store.chat_create_thread(user)["id"]
                        panel.ask(user, tid, question, skill=skill)
                        messages = store.chat_resume(user, tid)["messages"]
                        self.assertEqual(messages[0]["content"], masked[:MAX_CONTENT])
                        self.assertNotIn(identifier, messages[0]["content"])
                        self.assertEqual([m["seq"] for m in messages], [1, 2])


if __name__ == "__main__":
    unittest.main()
