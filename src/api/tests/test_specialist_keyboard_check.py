"""Pure-helper coverage for the specialist keyboard browser check (Refs #134)."""

import unittest

from checks.specialist_keyboard_browser_check import (
    expected_status,
    status_failures,
    text_markers,
)


class SpecialistKeyboardCheckHelpers(unittest.TestCase):
    def test_status_must_name_role_screen_and_selection_exactly(self) -> None:
        good = expected_status("Quality Inspector", "Quality queue", "ZF-4")
        self.assertEqual(good, "Quality Inspector. Quality queue. Selected home ZF-4.")
        self.assertEqual(status_failures(good, "Quality Inspector", "Quality queue", "ZF-4"), [])
        for wrong in ("", "Quality queue. Selected home ZF-4.", good.replace("ZF-4", "ZF-5")):
            self.assertTrue(status_failures(wrong, "Quality Inspector", "Quality queue", "ZF-4"))
        none = expected_status("Quality Inspector", "Quality queue", None)
        self.assertTrue(none.endswith("No home selected."))
        self.assertTrue(status_failures(good, "Quality Inspector", "Quality queue", None))

    def test_text_markers_report_presence_not_a_pass(self) -> None:
        self.assertEqual(
            text_markers("Cannot confirm readiness. Owner: Retrofit Coordinator"),
            {"endpoint_text": True, "handoff_text": True},
        )
        self.assertEqual(
            text_markers("Recorded evidence only."), {"endpoint_text": False, "handoff_text": False}
        )


if __name__ == "__main__":
    unittest.main()
