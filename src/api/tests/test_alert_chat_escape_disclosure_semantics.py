"""Escape, expanded-state and focus-return semantics for alert and chat disclosures (#215)."""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()
INDEX = (WEB / "index.html").read_text()


def _function(source: str, name: str, end: str) -> str:
    start = source.index(f"function {name}(")
    return source[start : source.index(end, start)]


class ChatPanelDisclosureTests(unittest.TestCase):
    def test_launcher_state_is_declared_and_kept_in_step_with_the_panel(self) -> None:
        self.assertIn('launcher.setAttribute("aria-controls", id)', WIDGET)
        self.assertIn('const root = node("section", "", { id, class: "chat-widget"', WIDGET)
        open_body = _function(WIDGET, "open", "function bottom")
        hide_body = _function(WIDGET, "hide", "function open")
        self.assertIn('launcher.setAttribute("aria-expanded", "true")', open_body)
        self.assertIn("root.hidden = false", open_body)
        self.assertIn('launcher.setAttribute("aria-expanded", "false")', hide_body)
        self.assertIn("root.hidden = true", hide_body)

    def test_escape_dismisses_from_anywhere_inside_the_panel_and_returns_to_the_launcher(
        self,
    ) -> None:
        # The listener is on the panel root, so every inner control dismisses.
        self.assertRegex(
            WIDGET,
            r'root\.addEventListener\("keydown", event => \{\s*'
            r'if \(event\.key === "Escape"\) \{ event\.preventDefault\(\); hide\(\); \}',
        )
        hide_body = _function(WIDGET, "hide", "function open")
        # A docked panel hides the launcher, so it is revealed before it takes focus.
        self.assertLess(
            hide_body.index("launcher.hidden = false"), hide_body.index("launcher.focus()")
        )
        self.assertIn("close.onclick = () => hide();", WIDGET)

    def test_open_chat_button_and_launcher_share_one_trigger_for_focus_return(self) -> None:
        self.assertIn(
            'h("button", { type: "button", onclick: () => employeeChat.open() }, "Open chat")', CHAT
        )
        self.assertIn('id="employee-chat-launcher" type="button"', INDEX)
        self.assertIn("launcher: launcher()", CHAT)
        self.assertIn("launcher.onclick = () => root.hidden ? open() : hide();", WIDGET)

    def test_panel_has_no_keyboard_trap(self) -> None:
        self.assertNotRegex(WIDGET, r"focustrap|trapFocus|inert\s*=")
        self.assertNotIn("showModal", WIDGET)
        # Moving focus outside dismisses a floating panel without stealing focus back.
        self.assertIn("if (!stayOpen) hide(false);", WIDGET)
        self.assertIn("if (returnFocus && active) launcher.focus()", WIDGET)
        # Escape is never swallowed for other handlers: nothing stops propagation.
        self.assertNotIn("stopPropagation", WIDGET)


class RegulatoryDisclosureEscapeTests(unittest.TestCase):
    def test_lookup_uses_native_details_whose_state_is_exposed_without_aria_overrides(
        self,
    ) -> None:
        self.assertIn(
            'const summary = h("summary", {}, "Cited regulatory lookup (synthetic-demo)");', CHAT
        )
        self.assertIn('const root = h("details", { id: "regulatory-chat" }, summary);', CHAT)
        # Native details/summary expose expanded state; redundant ARIA would risk drift.
        panel = CHAT[CHAT.index("function regulatoryChatPanel") :][:400]
        self.assertNotIn("aria-expanded", panel)

    def test_lookup_escape_closes_and_returns_focus_to_its_own_summary(self) -> None:
        start = CHAT.index('root.addEventListener("keydown"')
        body = CHAT[start : CHAT.index("});", start)]
        self.assertIn('event.key !== "Escape" || !root.open', body)
        self.assertIn("event.preventDefault()", body)
        self.assertLess(body.index("root.open = false"), body.index("summary.focus()"))
        # Escape is a no-op while closed, so it cannot trap or steal focus.
        self.assertLess(body.index("!root.open"), body.index("root.open = false"))

    def test_alert_details_and_citations_are_plain_content_so_they_cannot_trap_focus(
        self,
    ) -> None:
        alert = CHAT[CHAT.index("async function showAlerts") :][:3800]
        self.assertIn('h("article", { class: "regulatory-alert" }', alert)
        self.assertIn("regulatorySources(alert.citations)", alert)
        sources = CHAT[CHAT.index("function regulatorySources") :][:1800]
        self.assertIn('h("ul", { "aria-label": "Provision and fact citations" })', sources)
        for fragment in (alert, sources):
            self.assertNotIn("aria-expanded", fragment)
            self.assertNotIn("aria-controls", fragment)
            self.assertIsNone(re.search(r'h\("(details|dialog)"', fragment))
            self.assertNotIn("hidden", fragment.replace("aria-hidden", ""))

    def test_citation_links_leave_the_page_without_a_trap(self) -> None:
        self.assertIn('target: "_blank", rel: "noopener"', CHAT)
        self.assertIn("source record, opens new tab", CHAT)


if __name__ == "__main__":
    unittest.main()
