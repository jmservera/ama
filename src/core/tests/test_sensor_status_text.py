"""Sensor status text: list mirrors map, no readings or ranking claims (Refs #111, AC-067)."""

import re
import unittest
from dataclasses import replace
from datetime import timedelta

from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_status_text as st
from zava_forward.core.synthetic import sensor_scenarios as ss

WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))


class StatusTextTests(unittest.TestCase):
    def signals(self) -> list[sa.Signal]:
        out = []
        for case in (c for c in ss.generate() if c.truth.family == "damp"):
            home = case.rows[0]["home_id"]
            out.append(sa.derive_signal(home, case.rows, WINDOW, WINDOW.end, "granted"))
        home = out[0].home_id
        out.append(sa.derive_signal(home + "X", [], WINDOW, WINDOW.end, "declined"))
        out.append(sa.derive_signal(home + "Y", [], WINDOW, WINDOW.end, "granted"))
        return out

    def test_list_mirrors_map_text(self) -> None:
        signals = self.signals()
        map_entries, list_entries = st.map_and_list(signals)
        expected = [st.status_text(s) for s in sorted(signals, key=lambda s: s.home_id)]
        self.assertEqual(list_entries, expected)
        self.assertEqual(map_entries, expected)
        ids = [e.home_id for e in list_entries]
        self.assertEqual(ids, sorted(ids))
        self.assertTrue(all(e.label and e.text for e in list_entries))

    def test_every_state_is_reachable_and_names_manual_route(self) -> None:
        base = sa.derive_signal("H1", [], WINDOW, WINDOW.end, "granted")
        variants = {
            "review": replace(base, sufficiency=sa.SUFFICIENT, outcome=sa.REVIEW),
            "normal": replace(base, sufficiency=sa.SUFFICIENT, outcome=sa.NO_SIGNAL),
            "declined": replace(base, sufficiency=sa.DECLINED),
            "stale": replace(base, sufficiency=sa.STALE),
            "insufficient": replace(base, sufficiency=sa.SUFFICIENT, outcome=sa.INSUFFICIENT),
        }
        labels = {
            "review": "Check suggested",
            "normal": "No concern seen",
            "declined": "Monitoring is off",
            "stale": "Readings are out of date",
            "insufficient": "Not enough readings",
        }
        for state, sig in variants.items():
            out = st.status_text(sig)
            self.assertEqual(out.state, state)
            self.assertEqual(out.label, labels[state])
            self.assertIn(st.MANUAL_ROUTE, out.text)
            self.assertIn("housing officer", out.text)

    def test_insufficient_declined_stale_never_read_as_normal(self) -> None:
        for s in self.signals():
            if s.sufficiency != sa.SUFFICIENT:
                self.assertNotEqual(st.status_text(s).state, "normal")

    def test_text_has_no_readings_identifiers_or_diagnosis(self) -> None:
        for s in self.signals():
            text = st.status_text(s).text.lower()
            self.assertIsNone(re.search(r"\d", text))
            self.assertNotIn(s.home_id.lower(), text)
            self.assertNotIn("diagnos", text.replace("not a finding", ""))
            self.assertIn("does not change your repairs", text)

    def test_unknown_consent_fails_closed(self) -> None:
        odd = sa.derive_signal("H1", [], WINDOW, WINDOW.end, "unknown")
        self.assertEqual(st.status_text(odd).state, "insufficient")

    def test_unknown_outcome_fails_closed(self) -> None:
        base = sa.derive_signal("H1", [], WINDOW, WINDOW.end, "granted")
        odd = replace(base, sufficiency=sa.SUFFICIENT, outcome="SOMETHING_NEW")
        self.assertEqual(st.status_text(odd).state, "insufficient")


if __name__ == "__main__":
    unittest.main()
