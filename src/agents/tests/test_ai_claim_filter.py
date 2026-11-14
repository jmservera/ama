"""The assistant output filter refuses approval and record-change claims, not recorded status."""

import unittest
from unittest.mock import patch

from zava_forward.core.ai import FORBIDDEN, Ai

CLAIMS = (
    "I have approved the grant",
    "The grant has been approved.",
    "Ranking has been updated",
    "The case record has been changed",
    "We've now updated the case",
    "I have already sent the email",
    "The message has been sent",
)
GROUNDED = (
    "The grant was approved on 3 March by the finance lead.",
    "Status: approved. Ranking: 4 of 12.",
    "I have reviewed the recorded fields; approval is still pending a person.",
    "The record shows the case was updated yesterday.",
)


class ClaimFilterTests(unittest.TestCase):
    def test_claims_are_refused_and_grounded_status_is_kept(self) -> None:
        for text in CLAIMS:
            self.assertTrue(FORBIDDEN.search(text), text)
        for text in GROUNDED:
            self.assertIsNone(FORBIDDEN.search(text), text)

    def test_run_falls_back_to_template_on_a_claim(self) -> None:
        ai = Ai()
        ai.endpoint = "https://example.invalid"
        for text in CLAIMS:
            with patch.object(Ai, "_chat", return_value=text):
                result = ai.run("briefing", "system", "user", "TEMPLATE")
            self.assertEqual(result["source"], "template", text)
            self.assertFalse(result["validated"], text)
            self.assertEqual(result["text"], "TEMPLATE")
        with patch.object(Ai, "_chat", return_value=GROUNDED[0]):
            result = ai.run("briefing", "system", "user", "TEMPLATE")
        self.assertEqual(result["source"], "ai")


if __name__ == "__main__":
    unittest.main()
