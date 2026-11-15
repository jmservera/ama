"""Every model entrypoint reserves metered consumption before any credential or socket use."""

import unittest
from unittest.mock import patch

from zava_forward.core import ai_consumption
from zava_forward.core.ai import Ai


class ReserveGuardTests(unittest.TestCase):
    def test_no_meter_means_no_token_and_no_request(self) -> None:
        ai = Ai()
        ai.endpoint = "https://example.invalid"
        with patch.object(Ai, "_token") as token, patch("urllib.request.urlopen") as send:
            with self.assertRaises(ai_consumption.DispatchHeld):
                ai._request("standard", "system", "user", 100, 5, 0, {})
            envelope = ai.evidence("system", "user", 100, 5)
            result = ai.run("briefing", "system", "user", "TEMPLATE")
        token.assert_not_called()
        send.assert_not_called()
        self.assertEqual(envelope["outcome"], "financial-held")
        self.assertEqual(result["source"], "template")


if __name__ == "__main__":
    unittest.main()
