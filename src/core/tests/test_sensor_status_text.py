"""Sensor status text: list mirrors map, no readings or ranking claims (Refs #111, AC-067)."""

import re
import unittest
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
        map_entries, list_entries = st.map_and_list(self.signals())
        self.assertEqual(map_entries, list_entries)
        self.assertTrue(all(e.label and e.text for e in list_entries))

    def test_every_state_is_reachable_and_names_manual_route(self) -> None:
        states = {st.status_text(s).state for s in self.signals()}
        self.assertTrue({"declined", "stale"} <= states)
        for s in self.signals():
            self.assertIn(st.MANUAL_ROUTE, st.status_text(s).text)

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

    def test_unknown_outcome_fails_closed(self) -> None:
        odd = sa.derive_signal("H1", [], WINDOW, WINDOW.end, "unknown")
        self.assertEqual(st.status_text(odd).state, "insufficient")


if __name__ == "__main__":
    unittest.main()
