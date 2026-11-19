"""The API composes the agents worker as its assistant provider (R1, #107)."""

import unittest
import release_support

from test_assistants import Base, Provider, config
from zava_forward.agents.dispatch import AgentWorker
from zava_forward.core.assistants import Assistants
from zava_forward.core import telemetry
from telemetry_support import capture_telemetry


class DispatchCompositionTests(Base):
    def test_in_process_execution_joins_sql_audit_without_business_identifiers(self):
        class Traced(Provider):
            def evidence(self, *args):
                with telemetry.operation("chat"):
                    return super().evidence(*args)

        with capture_telemetry() as captured:
            self.compose(Traced())
            release_support.install(self.store)
            with telemetry.operation("http.server", root=True, method="POST"):
                p = self.run_ready("stock-prioritisation")
            with self.service.transaction() as db:
                bodies = [
                    row[0]
                    for row in db.execute(
                        "SELECT body FROM assistant_events WHERE task_id=?", (p["id"],)
                    ).fetchall()
                ]
            spans = captured.spans.get_finished_spans()
            workflow = next(s for s in spans if s.name == "invoke_workflow stock-prioritisation")
            provider = next(s for s in spans if s.name == "chat")
            self.assertEqual(p["state"], "ready")
            self.assertEqual(provider.parent.span_id, workflow.context.span_id)
            self.assertTrue(any(f"{workflow.context.trace_id:032x}" in body for body in bodies))
            self.assertTrue(any(s.name == "db.transaction" for s in spans))
            exported = " ".join(s.to_json() for s in spans)
            for value in ("ZF-1", self.pm["email"], "SELECT ", "INSERT ", p["id"]):
                self.assertNotIn(value, exported)

    def test_failed_proposal_records_error_without_exception_payload(self):
        class Broken(Provider):
            def evidence(self, *args):
                raise RuntimeError("PRIVATE-PROVIDER-DETAIL")

        with capture_telemetry() as captured:
            self.compose(Broken())
            release_support.install(self.store)
            p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
            self.service.execute(p["id"])
            spans = captured.spans.get_finished_spans()
            workflow = next(s for s in spans if s.name == "invoke_workflow stock-prioritisation")
            self.assertEqual((workflow.attributes or {})["error.type"], "error")
            self.assertNotIn("PRIVATE-PROVIDER-DETAIL", " ".join(s.to_json() for s in spans))
            self.assertNotEqual(self.service.detail(self.pm, p["id"])["state"], "ready")

    def compose(self, provider):
        self.store.ai = provider
        worker = AgentWorker(lambda *args: self.store.ai.evidence(*args))
        self.service = Assistants(self.store, config(), provider=worker.provider_call)

    def test_agents_worker_provider_produces_a_ready_proposal(self):
        self.compose(self.provider)
        p = self.run_ready("stock-prioritisation")
        self.assertEqual(self.provider.calls, 1)
        self.assertIs(p["envelope"]["approved"], False)
        self.assertIsNone(p["review"])

    def test_provider_exception_is_a_safe_failure(self):
        class Broken(Provider):
            def evidence(self, system, prompt, max_tokens, timeout):
                raise RuntimeError("PRIVATE-PROVIDER-DETAIL")

        self.compose(Broken())
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        self.service.execute(p["id"])
        detail = self.service.detail(self.pm, p["id"])
        self.assertNotEqual(detail["state"], "ready")
        self.assertNotIn("PRIVATE-PROVIDER-DETAIL", str(detail))


if __name__ == "__main__":
    unittest.main()
