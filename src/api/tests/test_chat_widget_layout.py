"""Gate the employee chat composer layout without the resident leg (#520)."""

import os
import subprocess
import sys
import unittest
from pathlib import Path

API = Path(__file__).resolve().parents[1]
CSS = (API / "src/zava_forward/api/web/chat-widget.css").read_text(encoding="utf-8")


class ChatWidgetLayout(unittest.TestCase):
    def test_sticky_tools_rule_is_employee_scoped(self) -> None:
        self.assertIn("#employee-chat .chat-widget-composer .chat-widget-tools{", CSS)
        self.assertNotIn("\n.chat-widget-composer .chat-widget-tools{position:sticky", CSS)

    def test_employee_send_stays_in_panel_at_short_viewports(self) -> None:
        result = subprocess.run(
            [sys.executable, "checks/chat_widget_browser_check.py", "--employee-layout"],
            cwd=API,
            env={
                **os.environ,
                "PYTHONPATH": os.pathsep.join(
                    [
                        str(API),
                        str(API / "tests"),
                        str(API.parent / "core/tests"),
                        *(str(API.parent / p / "src") for p in ("core", "agents", "api")),
                        *sys.path,
                    ]
                ),
            },
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
        if "Executable doesn't exist" in result.stdout + result.stderr:
            self.skipTest("Chromium is installed by the later browser-check step")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS employee layout", result.stdout)


if __name__ == "__main__":
    unittest.main()
