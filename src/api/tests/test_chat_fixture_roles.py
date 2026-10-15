"""Keeps the chat fixture role names equal to the auth role map (auth moved to src/api in M5 of #199)."""
import unittest

import chat_fixture  # src/agents/tests, on PYTHONPATH
from zava_forward.api import auth


class ChatFixtureRoleNames(unittest.TestCase):
    def test_role_names_equal_auth_default_role_map(self):
        self.assertEqual(chat_fixture.ROLE_NAMES, auth.DEFAULT_ROLE_MAP)


if __name__ == "__main__":
    unittest.main()
