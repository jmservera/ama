"""Offline tests for tools/check-edge-anonymous-401.py (Refs #350). No network access."""

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check-edge-anonymous-401.py")
SPEC = importlib.util.spec_from_file_location("check_edge_anonymous_401", SCRIPT)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class EdgeCheckTests(unittest.TestCase):
    def test_browser_api_redirect_is_a_failure(self):
        def fetcher(base, path, headers):
            return 302 if "Accept" in headers and path.startswith("/api/") else 401

        report = mod.run("https://x", fetcher)
        self.assertEqual(report["verdict"], "fail")
        failed = {(r["path"], r["style"]) for r in report["rows"] if r["result"] == "fail"}
        self.assertIn(("/api/me", "browser-json"), failed)
        self.assertNotIn(("/api/me", "native"), failed)

    def test_all_401_api_and_page_redirect_passes(self):
        report = mod.run("https://x", lambda b, p, h: 401 if p.startswith("/api/") else 302)
        self.assertEqual(report["verdict"], "pass")

    def test_api_200_and_network_error_are_not_passes(self):
        self.assertEqual(mod.classify("/api/me", 200), "fail")
        self.assertEqual(mod.run("https://x", lambda b, p, h: None)["verdict"], "blocked")


if __name__ == "__main__":
    unittest.main()
