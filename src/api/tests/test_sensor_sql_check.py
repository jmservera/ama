"""Selector and result validation for the owned sensor SQL harness (Refs #111)."""

import unittest
from unittest.mock import patch

from checks import sensor_sql_check as check

CLEAN = "........\n" + "-" * 70 + "\nRan 8 tests in 4.2s\n\nOK\n"


class SensorSqlCheckTests(unittest.TestCase):
    def test_default_selection_is_unchanged_and_analysis_is_a_fixed_module(self) -> None:
        self.assertEqual(
            check.SELECTORS["default"],
            (
                "test_sensor_ingestion",
                "test_sensor_consistency.SqlHandoverTests."
                "test_composed_joint_query_statistics_and_reopened_window_replay",
            ),
        )
        self.assertEqual(check.SELECTORS["analysis"], ("test_sensor_analysis_mssql",))
        self.assertEqual(set(check.SELECTORS), {"default", "analysis"})

    def test_unknown_selector_is_rejected_before_any_container_starts(self) -> None:
        with (
            patch("subprocess.run") as run,
            patch("sys.stderr"),
            self.assertRaises(SystemExit) as caught,
        ):
            check.main(["--selector", "test_other.SomeTest"])
        self.assertEqual(caught.exception.code, 2)
        run.assert_not_called()

    def test_analysis_result_requires_exact_count_and_no_skips(self) -> None:
        self.assertTrue(check.validate("analysis", 0, CLEAN))
        self.assertFalse(check.validate("analysis", 1, CLEAN))
        self.assertFalse(check.validate("analysis", 0, CLEAN.replace("OK", "OK (skipped=8)")))
        self.assertFalse(check.validate("analysis", 0, CLEAN.replace("Ran 8", "Ran 7")))
        self.assertFalse(check.validate("analysis", 0, "Ran 8 tests in 1s\n\nFAILED (failures=1)"))
        self.assertFalse(check.validate("analysis", 0, ""))

    def test_default_result_keeps_exit_code_semantics(self) -> None:
        self.assertTrue(check.validate("default", 0, ""))
        self.assertFalse(check.validate("default", 1, CLEAN))


if __name__ == "__main__":
    unittest.main()
