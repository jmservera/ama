import unittest

from zava_forward.core.governance import target_verdict


class TargetVerdictTests(unittest.TestCase):
    def test_missing_mde_is_never_assessed(self):
        self.assertEqual(target_verdict(10, None, 50)["verdict"], "Not assessable")

    def test_mde_above_target_gives_interval_estimate_even_when_observed_would_pass(self):
        out = target_verdict(10, 12.5, 40)
        self.assertEqual(out["verdict"], "Interval estimate only")
        self.assertIn("12.5%", out["reason"])
        self.assertIn("10%", out["reason"])

    def test_mde_equal_to_target_is_assessable(self):
        self.assertEqual(target_verdict(10, 10)["verdict"], "Awaiting result")
        self.assertEqual(target_verdict(10, 10, 10)["verdict"], "Pass")

    def test_pass_and_fail_around_the_target(self):
        self.assertEqual(target_verdict(10, 5, 10)["verdict"], "Pass")
        self.assertEqual(target_verdict(10, 5, 9.99)["verdict"], "Fail")
        self.assertEqual(target_verdict(10, 5, 0)["verdict"], "Fail")


if __name__ == "__main__":
    unittest.main()
