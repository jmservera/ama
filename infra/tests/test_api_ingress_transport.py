"""Issue 810: the Easy Auth API ingress is pinned to HTTP/1.1 (transport auto gave empty-body 500s)."""

import re
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "modules" / "containerapps.bicep"


class ApiIngressTransportTests(unittest.TestCase):
    def test_api_ingress_transport_is_http(self) -> None:
        text = MODULE.read_text(encoding="utf-8")
        match = re.search(r"resource api '[^']+' = .*?ingress: \{(.*?)\n      \}", text, re.DOTALL)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertIn("transport: 'http'", match.group(1))
        self.assertNotIn("transport: 'auto'", match.group(1))


if __name__ == "__main__":
    unittest.main()
