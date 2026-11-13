"""Failure notices in app.js state the reason, owner and next action (issue 153, criterion 3)."""

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
APP = (WEB / "app.js").read_text()
REASONS = (
    "Briefing unavailable: ${error.message}",
    "Priority suggestions unavailable: ${error.message}",
    "Cases unavailable: ${error.message}",
    "Map unavailable: ${error.message}",
    "Could not start the workspace: ${error.message}",
)


class AppJsNoticesContentTests(unittest.TestCase):
    def test_reason_prefixes_are_wrapped_with_owner_and_next_action(self) -> None:
        for reason in REASONS:
            with self.subTest(reason=reason):
                pattern = re.escape("ownedNotice(`" + reason + "`") + r', "[^"]*(then|use|choose)'
                self.assertRegex(APP, pattern)

    def test_other_notices_use_the_helper(self) -> None:
        for fragment in (
            'ownedNotice(e.message, "contact application support if it continues.")}',
            'ownedNotice(e.message, "go back to the list and open the case',
            'ownedNotice(error.message, "choose Try loading',
        ):
            self.assertIn(fragment, APP)

    @unittest.skipUnless(shutil.which("node"), "node is required")
    def test_helper_adds_clauses_once_and_keeps_existing_owner(self) -> None:
        found = re.search(r"const SUPPORT_OWNER.*?\n}\n", APP, re.S)
        assert found
        source = found.group(0)
        calls = json.dumps(
            [
                ["Failed", "retry."],
                ["Failed.", "retry."],
                ["Failed. Owner: Finance. Next action: ask them.", "retry."],
            ]
        )
        script = source + f"console.log(JSON.stringify({calls}.map(a => ownedNotice(...a))));"
        out = json.loads(
            subprocess.run(
                ["node", "-e", script], capture_output=True, text=True, check=True
            ).stdout
        )
        self.assertEqual(out[0], "Failed. Owner: application support. Next action: retry.")
        self.assertEqual(out[1], out[0])
        self.assertEqual(out[2], "Failed. Owner: Finance. Next action: ask them.")

    def test_preserved_substrings(self) -> None:
        for text in (
            "Use the case and building screens instead",
            "`Workspace unavailable: ${error.message}`",
            "Tab navigation unavailable",
        ):
            self.assertIn(text, APP)


if __name__ == "__main__":
    unittest.main()
