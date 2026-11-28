"""Static accessibility checks for the simulator run-control screen (issue 149)."""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
SRC = (WEB / "simulator-control.js").read_text()
IDS = set(re.findall(r'\bid: "([\w-]+)"', SRC))


class SimulatorControlScreen(unittest.TestCase):
    def test_every_label_targets_an_existing_id(self) -> None:
        targets = re.findall(r'h\("label", \{ for: "([\w-]+)" \}', SRC)
        self.assertGreaterEqual(len(targets), 6)
        for target in targets:
            self.assertIn(target, IDS, target)

    def test_described_by_targets_exist(self) -> None:
        targets = re.findall(r'"aria-describedby": "([\w-]+)"', SRC)
        self.assertTrue(targets)
        for target in targets:
            self.assertIn(target, IDS, target)

    def test_sections_and_forms_are_named_by_headings(self) -> None:
        targets = re.findall(r'"aria-labelledby": "([\w-]+)"', SRC)
        self.assertEqual(len(targets), 4)
        for target in targets:
            self.assertRegex(SRC, rf'h\("h2", \{{ id: "{re.escape(target)}" \}}')

    def test_each_form_has_one_submit_button(self) -> None:
        self.assertEqual(SRC.count('h("form"'), 2)
        self.assertEqual(len(re.findall(r'h\("button", \{ type: "submit" \}', SRC)), 2)

    def test_start_and_stop_send_the_confirmation(self) -> None:
        self.assertRegex(SRC, r"/start`, \{[^}]*confirm: confirm\.checked")
        self.assertRegex(SRC, r"/stop`, \{[^}]*confirm: confirm\.checked")

    def test_start_fields_are_required_and_not_autofilled(self) -> None:
        for field in ("sim-owner", "sim-approval", "sim-expires", "sim-homes"):
            line = next(x for x in SRC.splitlines() if f'id: "{field}"' in x)
            self.assertIn("required: true", line, field)
            self.assertIn('autocomplete: "off"', line, field)

    def test_messages_use_live_roles_and_focusable_heading(self) -> None:
        self.assertIn('h("h1", { tabindex: "-1" }', SRC)
        self.assertIn('role: "alert"', SRC)
        self.assertIn('role: "status"', SRC)
        self.assertEqual(SRC.count('h("h1"'), 1)


if __name__ == "__main__":
    unittest.main()
