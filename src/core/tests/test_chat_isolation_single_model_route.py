import unittest

from zava_forward.core import chat_isolation
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import ChatPanel


class SingleModelRouteTests(unittest.TestCase):
    def test_isolation_has_no_model_route_that_skips_admission(self) -> None:
        for name in ("turn", "_ask", "model_name"):
            self.assertFalse(hasattr(ChatIsolation, name), name)
        self.assertFalse(hasattr(chat_isolation, "SYSTEM"))

    def test_chat_panel_is_the_model_route(self) -> None:
        self.assertTrue(hasattr(ChatPanel, "_ask"))


if __name__ == "__main__":
    unittest.main()
