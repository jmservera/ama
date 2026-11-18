"""#215 criteria 1 and 2: every rendered alert names what was noticed, source and status, safe
action, owner and clock for the seven role groups, with non-colour indicators.

Synthetic fixtures only; no network and no provider calls. Static source checks and API contract
checks, not browser, screen reader, assistive technology, staff comprehension or manual
acceptance evidence, and no WCAG conformance claim.
"""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from typing import Any

from regulatory_fixture import NOW, Fixture
from zava_forward.core.projection import CONTRACTOR, STAFF_ROLES, allowed
from zava_forward.core.rule_engine import AUDIENCES

from zava_forward.api.server import App

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
CSS = (WEB / "style.css").read_text()

# The seven #215 role groups. Data handlers use the staff role that holds the data duty and
# suppliers have no staff role, so they are asserted separately.
ROLE_GROUPS = {
    "repairs and intake": "Resident Liaison Officer",
    "Building Safety": "Building Safety Liaison",
    "assessor": "Quality Inspector",
    "coordinator": "Retrofit Coordinator",
    "programme": "Retrofit Programme Manager",
    "finance and grants": "Grants and Evidence Officer",
    "data handlers": "Programme Support Officer",
}
LABELS = (
    "What was noticed",
    "Safe action",
    "Decision owner",
    "Clock",
    "Source and status",
)
RESULTS = ("breach risk", "attention", "unknown", "clear", "not applicable")
REQUIRED = ("noticed", "safe_action", "decision_owner", "escalation_role", "clock", "citations")
ADS_CARD = "synthetic-ads"
HAZARD_CARD = "synthetic-hazard"


def alert_template() -> str:
    start = CHAT.index('h("article", { class: "regulatory-alert",')
    return CHAT[start : CHAT.index("status.className", start)]


def source_line() -> str:
    start = CHAT.index("function regulatorySources")
    return CHAT[start : CHAT.index("function regulatoryAlertsPanel", start)]


class RenderedAlertContractTests(unittest.TestCase):
    def test_every_alert_renders_the_five_labelled_facts_for_every_role(self) -> None:
        body = alert_template()
        for label in LABELS:
            with self.subTest(label=label):
                self.assertIn(f'"{label}"', body)
        # One shared template, so no role gets a reduced card.
        self.assertEqual(CHAT.count('class: "regulatory-alert"'), 1)
        self.assertIn("regulatoryAlertsPanel(", CHAT)
        self.assertNotRegex(alert_template(), r"me\.user\.role|role ===")

    def test_missing_values_render_an_explicit_held_state_not_a_blank_or_a_default_duty(
        self,
    ) -> None:
        body = alert_template()
        self.assertIn('alert.noticed || "Unknown"', body)
        self.assertIn("Use the human owner route; do not infer an action.", body)
        self.assertIn('alert.decision_owner || "Unassigned"', body)
        self.assertIn("No approved clock held", body)
        self.assertIn("unknown, not calculated here", body)

    def test_source_and_status_show_status_effective_and_retrieved_as_text(self) -> None:
        body = source_line()
        for text in ("Status: ", "Effective: ", "Retrieved/observed: "):
            with self.subTest(text=text):
                self.assertIn(text, body)
        self.assertIn('source.status || "unknown"', body)

    def test_every_result_has_text_status_glyph_and_a_non_colour_border_style(self) -> None:
        self.assertIn("`Status: ${regulatoryStateLabel(alert.result)}`", alert_template())
        self.assertIn(
            "const regulatoryStateLabel = (value) => "
            '(regulatoryStates.has(value) ? value : "unknown");',
            CHAT,
        )
        for result in RESULTS:
            slug = result.replace(" ", "-")
            with self.subTest(result=result):
                self.assertRegex(CSS, rf'\.state-{slug}:before\{{content:"[^"]+" / ""\}}')
        glyphs = re.findall(
            r'\.state-(?:breach-risk|attention|unknown|clear|not-applicable):before\{content:"([^"]+)"',
            CSS,
        )
        self.assertEqual(len(glyphs), len(set(glyphs)), "Each result needs its own glyph")
        self.assertRegex(CSS, r"\.regulatory-state\{border-left:4px solid currentColor")

    def test_alert_card_states_the_human_boundary_beside_the_owner(self) -> None:
        body = alert_template()
        self.assertIn("This panel cannot acknowledge, decide compliance", body)
        self.assertIn("Owner acknowledgement:", body)


class RoleAlertDataTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.f = Fixture(temp.name, sql=True)
        self.addCleanup(self.f.close)
        self.f.card(ADS_CARD, kind="automated-decision-safeguard")
        app: Any = App(self.f.store, "synthetic-local", law=self.f.law)  # type: ignore[no-untyped-call]
        self.engine = app.rule_engine()
        self.engine.run(self.f.store, "ZF-1", now=NOW)

    def alerts_for(self, role: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        user: dict[str, Any] = self.f.store.staff[self.f.user["email"]]
        user["role"] = role
        data: dict[str, Any] = self.engine.alerts(user, "ZF-1")
        return data, [a for home in data["homes"] for a in home["alerts"]]

    def test_the_seven_groups_cover_every_staff_role(self) -> None:
        self.assertEqual(len(ROLE_GROUPS), 7)
        self.assertEqual(set(ROLE_GROUPS.values()), set(STAFF_ROLES))

    def test_every_alert_a_role_can_see_carries_all_five_facts(self) -> None:
        seen = 0
        for group, role in ROLE_GROUPS.items():
            _, alerts = self.alerts_for(role)
            for alert in alerts:
                seen += 1
                with self.subTest(group=group, alert=alert["card_id"]):
                    for key in REQUIRED:
                        self.assertTrue(alert[key], key)
                    self.assertIn(alert["result"], RESULTS)
                    self.assertTrue(alert["at"])
                    # Owner and clock are named; the due time is text, never colour alone.
                    self.assertIn("@", alert["decision_owner"])
                    self.assertRegex(alert["clock"], r"\d+ hours")
                    for source in alert["citations"]:
                        self.assertTrue(source["id"])
                        self.assertTrue(source.get("status"))
        self.assertGreaterEqual(seen, 5)

    def test_roles_reach_exactly_the_alert_kinds_their_audience_allows(self) -> None:
        expected = {
            "Resident Liaison Officer": {HAZARD_CARD},
            "Building Safety Liaison": {HAZARD_CARD},
            "Retrofit Coordinator": {ADS_CARD},
            "Retrofit Programme Manager": {HAZARD_CARD, ADS_CARD},
        }
        for group, role in ROLE_GROUPS.items():
            with self.subTest(group=group):
                _, alerts = self.alerts_for(role)
                self.assertEqual({a["card_id"] for a in alerts}, expected.get(role, set()))
                for allowed_roles in AUDIENCES.values():
                    if role in allowed_roles:
                        self.assertTrue(alerts)

    def test_a_role_with_no_alert_never_gets_a_clear_signal(self) -> None:
        for group, role in ROLE_GROUPS.items():
            data, alerts = self.alerts_for(role)
            if alerts:
                continue
            with self.subTest(group=group):
                self.assertEqual(data["homes"], [])
                self.assertEqual(data["coverage_status"], "unknown")
        self.assertIn(
            "No visible alerts does not mean no risk, complete coverage or compliance.", CHAT
        )

    def test_alerts_are_never_presented_as_clear_when_coverage_is_unknown(self) -> None:
        for group, role in ROLE_GROUPS.items():
            data, alerts = self.alerts_for(role)
            with self.subTest(group=group):
                self.assertNotEqual(data["coverage_status"], "clear")
                for alert in alerts:
                    self.assertNotEqual(alert["result"], "clear")

    def test_suppliers_get_no_alert_and_no_law_route(self) -> None:
        user: dict[str, Any] = self.f.store.staff[self.f.user["email"]]
        user["role"] = CONTRACTOR
        self.assertFalse(allowed(user, "law"))
        with self.assertRaises(PermissionError):
            self.engine.alerts(user, "ZF-1")


if __name__ == "__main__":
    unittest.main()
