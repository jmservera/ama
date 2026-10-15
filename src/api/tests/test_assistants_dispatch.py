"""The API composes the agents worker as its assistant provider (R1, #107)."""
import unittest

from test_assistants import Base, Provider, config
from zava_forward.agents.dispatch import AgentWorker
from zava_forward.core.assistants import Assistants


class DispatchCompositionTests(Base):
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
