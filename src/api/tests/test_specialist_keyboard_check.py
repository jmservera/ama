"""Pure-helper coverage for the specialist keyboard browser check (Refs #134)."""

import unittest

from checks.specialist_keyboard_browser_check import (
    NO_REGION_GAPS,
    expected_status,
    focus_failures,
    region_failures,
    status_contract_failures,
    status_failures,
    text_markers,
)

RING = {
    "outlineStyle": "solid",
    "outlineWidth": "3px",
    "outlineColor": "rgb(0, 90, 158)",
    "boxShadow": "none",
}
STATUS = {"role": "status", "aria-live": "polite", "aria-atomic": "true"}
REGION = {"label": "Same-home step states", "tabindex": "0", "role": "region"}


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

    def test_focus_needs_a_measured_visible_indicator(self) -> None:
        self.assertEqual(focus_failures(RING), [])
        shadow = {**RING, "outlineStyle": "none", "boxShadow": "rgb(0, 90, 158) 0px 0px 0px 2px"}
        self.assertEqual(focus_failures(shadow), [])
        ring = "rgb(242, 169, 0) 0px 0px 0px 2px"
        self.assertEqual(focus_failures({**RING, "outlineStyle": "none", "boxShadow": ring}), [])
        for bad_shadow in (
            "rgba(0, 90, 158, 0) 0px 0px 0px 2px",
            "rgb(0, 90, 158) 0px 0px 0px 0px",
            "rgb(0, 90, 158) 400px 0px 0px 2px",
            "rgb(0, 90, 158) 0px 0px 8px 2px",
            "rgb(0, 90, 158) 0px 0px 0px 2px inset",
            f"{ring}, {ring}",
        ):
            self.assertTrue(
                focus_failures({**RING, "outlineStyle": "none", "boxShadow": bad_shadow}),
                bad_shadow,
            )
        for bad in (
            {**RING, "outlineStyle": "none"},
            {**RING, "outlineWidth": "1px"},
            {**RING, "outlineColor": "rgba(0, 0, 0, 0)"},
            {**RING, "outlineStyle": "none", "boxShadow": "rgba(0, 0, 0, 0) 0px 0px 0px 2px"},
        ):
            self.assertTrue(focus_failures(bad), bad)

    def test_status_semantics_are_asserted_independently_of_text(self) -> None:
        text = expected_status("Quality Inspector", "Quality queue", None)
        args = ("Quality Inspector", "Quality queue", None)
        self.assertEqual(status_contract_failures(STATUS, text, *args), [])
        for name in STATUS:
            attrs = {k: v for k, v in STATUS.items() if k != name}
            self.assertTrue(status_contract_failures(attrs, text, *args), name)
        self.assertTrue(status_contract_failures({**STATUS, "aria-live": "off"}, text, *args))

    def test_regions_must_match_the_declared_screen_expectation(self) -> None:
        self.assertEqual(region_failures("programme-queue", [REGION]), [])
        self.assertTrue(region_failures("programme-queue", []))
        self.assertTrue(region_failures("programme-queue", [{**REGION, "label": ""}]))
        self.assertTrue(region_failures("programme-queue", [{**REGION, "tabindex": "-1"}]))
        self.assertTrue(region_failures("programme-queue", [{**REGION, "role": None}]))
        self.assertTrue(region_failures("programme-queue", [REGION, REGION]))
        self.assertTrue(region_failures("safety-lead", [REGION]))
        self.assertTrue(region_failures("unlisted-screen", []))

    def test_declared_gaps_allow_no_table_but_not_an_invented_one(self) -> None:
        gap = sorted(NO_REGION_GAPS)[0]
        self.assertEqual(region_failures(gap, []), [])
        self.assertTrue(region_failures(gap, [REGION]))


if __name__ == "__main__":
    unittest.main()
