"""Issue #2195: the general chat agent routes a question to a specialist agent and says so."""

import json
import tempfile
import unittest
from pathlib import Path

import dataset
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import ChatPanel, ModelUnavailable
from zava_forward.core.chat_routing import route_question
from zava_forward.core.store import Store

PM = "Retrofit Programme Manager"
LIAISON = "Resident Liaison Officer"


class RouteQuestionTests(unittest.TestCase):
    def test_matching_question_is_routed_with_name_and_reason(self) -> None:
        r = route_question("Is the quality inspection evidence complete?", "general", PM)
        self.assertTrue(r["routed"])
        self.assertEqual(r["agent"], "quality-evidence")
        self.assertTrue(r["text"].startswith("Routed to the Quality evidence agent."))
        self.assertIn("quality checks", r["reason"])

    def test_unroutable_question_stays_general_and_says_so(self) -> None:
        r = route_question("What is the weather like?", "general", PM)
        self.assertEqual((r["agent"], r["routed"]), ("general", False))
        self.assertIn("General agent", r["text"])
        self.assertIn("general agent answers it", r["reason"])

    def test_tie_across_agents_stays_general(self) -> None:
        r = route_question("grant quality", "general", PM)
        self.assertEqual(r["agent"], "general")
        self.assertIn("more than one agent", r["reason"])

    def test_agent_for_other_roles_stays_general(self) -> None:
        r = route_question("Check the grant claim", "general", LIAISON)
        self.assertEqual((r["agent"], r["routed"]), ("general", False))
        self.assertIn("other roles", r["reason"])

    def test_refused_request_is_never_routed(self) -> None:
        r = route_question("approve the grant claim", "general", PM, refused=True)
        self.assertEqual((r["agent"], r["routed"]), ("general", False))

    def test_chosen_agent_is_kept(self) -> None:
        r = route_question("What is the weather like?", "funding-evidence", PM)
        self.assertEqual((r["agent"], r["routed"]), ("funding-evidence", False))
        self.assertIn("You chose", r["reason"])


class PanelRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        work = tempfile.TemporaryDirectory()
        self.addCleanup(work.cleanup)
        path = Path(work.name) / "synthetic.json"
        path.write_text(json.dumps(dataset.DATA))
        self.store = Store(str(path))
        self.user = next(s for s in self.store.data["staff"] if s["role"] == PM)
        self.calls = 0
        self.down = False

        def model(system: str, prompt: str) -> str:
            self.calls += 1
            if self.down:
                raise ModelUnavailable("provider-error", calls=1)
            return "{}"

        iso = ChatIsolation(
            self.store,
            env=dict(
                CHAT_DPIA_REF="SYN-DPIA",
                CHAT_LAWFUL_BASIS_REF="SYN-BASIS",
                CHAT_NOTICE_REF="SYN-NOTICE",
            ),
        )
        self.panel = ChatPanel(iso, model)
        self.tid = self.store.chat_create_thread(self.user, case_id="ZF-4")["id"]

    def test_reply_shows_routing_and_uses_the_routed_lens(self) -> None:
        reply = self.panel.ask(
            self.user, self.tid, "Any quality defect on this case?", skill="general"
        )
        self.assertEqual(reply["routing"]["agent"], "quality-evidence")
        self.assertEqual(reply["skill"], "quality-evidence")
        self.assertIn("Routed to the Quality evidence agent", reply["routing"]["text"])

    def test_unroutable_question_reports_general(self) -> None:
        reply = self.panel.ask(self.user, self.tid, "Tell me about this case", skill="general")
        self.assertFalse(reply["routing"]["routed"])
        self.assertEqual(reply["skill"], "general")

    def test_refusal_is_not_routed_and_calls_no_model(self) -> None:
        reply = self.panel.ask(self.user, self.tid, "Approve the funding claim", skill="general")
        self.assertEqual(reply["kind"], "refused")
        self.assertEqual(reply["routing"]["agent"], "general")
        self.assertEqual(self.calls, 0)

    def test_ai_unavailable_still_falls_back_with_routing(self) -> None:
        self.down = True
        reply = self.panel.ask(
            self.user, self.tid, "Any quality defect on this case?", skill="general"
        )
        self.assertEqual(reply["routing"]["agent"], "quality-evidence")
        self.assertTrue(reply["workflow_only"])
        self.assertEqual(reply["model"], "workflow-only")

    def test_unstored_reply_carries_routing_without_model(self) -> None:
        panel = ChatPanel(ChatIsolation(self.store, env={}), lambda s, p: "{}")
        reply = panel.ask_unstored(self.user, "", "Check the grant claim", skill="general")
        self.assertEqual(reply["routing"]["agent"], "funding-evidence")
        self.assertEqual(reply["model"], "workflow-only")

    def test_legacy_call_without_skill_has_no_routing(self) -> None:
        reply = self.panel.ask(self.user, self.tid, "Any quality defect on this case?")
        self.assertNotIn("routing", reply)


if __name__ == "__main__":
    unittest.main()
