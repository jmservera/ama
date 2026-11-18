"""Issue #159 criterion 6: keyboard, screen-reader and focus behaviour of the chat panel."""

import re
import unittest
from pathlib import Path

import test_chat_widget_focus as focus

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


class ChatPanelAccessibilityTests(unittest.TestCase):
    def test_log_is_a_polite_non_atomic_live_log(self) -> None:
        source = (WEB / "chat-widget.js").read_text(encoding="utf-8")
        log = re.search(r'class: "chat-widget-log"[^}]*', source)
        assert log is not None
        for attribute in (
            'role: "log"',
            '"aria-live": "polite"',
            '"aria-relevant": "additions"',
            '"aria-label"',
        ):
            self.assertIn(attribute, log.group(0))
        self.assertIn('role: "dialog", "aria-labelledby"', source)
        self.assertIn('role: "status", "aria-live": "polite"', source)

    def test_every_control_has_a_visible_focus_indicator(self) -> None:
        css = (WEB / "chat-widget.css").read_text(encoding="utf-8")
        rule = re.search(r"\.chat-widget :is\(([^)]*)\):focus-visible[^{]*\{([^}]*)\}", css)
        assert rule is not None
        for control in ("button", "summary", "textarea", "select", "input"):
            self.assertIn(control, rule.group(1))
        self.assertIn(".chat-widget-launcher:focus-visible", css)
        for token in ("--focus-w", "--focus-ink", "--focus-off", "--focus)"):
            self.assertIn(token, rule.group(2))
        self.assertNotRegex(css, r"outline:\s*(none|0)")

    def test_keyboard_flow_and_message_arrival_keep_focus(self) -> None:
        focus.ChatWidgetFocusTests.run_node(
            self,  # type: ignore[arg-type]
            r"""
const h = harness();
const ui = h.context.window.ChatWidget.create({
  id: "a11y", title: "Chat", launcher: h.launcher,
  questionLabel: "Question", skillLabel: "Skill"
});
ui.open();
assert.equal(h.document.activeElement, ui.heading);
ui.input.focus();
let prevented = false, submitted = 0;
ui.form.requestSubmit = () => { submitted++; };
ui.input.onkeydown({key: "Enter", shiftKey: false, preventDefault() { prevented = true; }});
assert.ok(prevented && submitted === 1);
prevented = false;
ui.input.onkeydown({key: "Enter", shiftKey: true, preventDefault() { prevented = true; }});
assert.ok(!prevented && submitted === 1);

ui.busy(true);
ui.message("assistant", "A new reply");
ui.setStatus("Reply received");
ui.busy(false);
assert.equal(h.document.activeElement, ui.input);
assert.equal(ui.log.children.length, 1);

ui.root.onkeydown({key: "Escape", preventDefault() {}});
assert.equal(ui.root.hidden, true);
assert.equal(h.document.activeElement, h.launcher);
assert.equal(h.launcher.attrs["aria-expanded"], "false");
ui.open();
assert.equal(ui.root.hidden, false);
""",
        )

    def test_focus_moves_off_send_only_to_the_composer(self) -> None:
        focus.ChatWidgetFocusTests.run_node(
            self,  # type: ignore[arg-type]
            r"""
const h = harness();
const ui = h.context.window.ChatWidget.create({
  id: "a11y2", title: "Chat", launcher: h.launcher,
  questionLabel: "Question", skillLabel: "Skill"
});
ui.open();
ui.send.focus();
ui.busy(true);
assert.equal(h.document.activeElement, ui.input);
ui.message("assistant", "Reply");
assert.equal(h.document.activeElement, ui.input);
""",
        )


if __name__ == "__main__":
    unittest.main()
