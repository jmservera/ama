"""Demo opt-in for sending captured synthetic readings to a real model (issue 1288).

Local engineering evidence: a pure call of the carrier check, no provider and no network.
"""

import unittest

from zava_forward.core.ai import Ai, may_carry_captured_readings

OPT_IN = {"ZF_DEPLOYMENT_PROFILE": "demo", "ZF_DEMO_SENSOR_MODEL_DISPATCH": "synthetic-demo-only"}


class DemoSensorDispatch(unittest.TestCase):
    real = object.__new__(Ai)

    def test_a_real_client_is_refused_by_default(self) -> None:
        self.assertFalse(may_carry_captured_readings(self.real, {}))

    def test_the_opt_in_needs_the_demo_profile_and_the_exact_value(self) -> None:
        self.assertTrue(may_carry_captured_readings(self.real, OPT_IN))
        production = {**OPT_IN, "ZF_DEPLOYMENT_PROFILE": "production"}
        loose = {**OPT_IN, "ZF_DEMO_SENSOR_MODEL_DISPATCH": "1"}
        self.assertFalse(may_carry_captured_readings(self.real, production))
        self.assertFalse(may_carry_captured_readings(self.real, loose))

    def test_a_silent_carrier_is_unchanged(self) -> None:
        class Silent:
            sends_no_bytes = True

        self.assertTrue(may_carry_captured_readings(Silent(), {}))
        self.assertFalse(may_carry_captured_readings(object(), OPT_IN))


if __name__ == "__main__":
    unittest.main()
