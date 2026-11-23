import unittest

from zava_forward.core import continuity


class DemoOwnerOverrideTests(unittest.TestCase):
    def test_override_needs_exact_value_and_never_applies_in_production(self) -> None:
        name = continuity.DEMO_OWNER_OVERRIDE_ENV
        value = "owner-directed-2026-11-23"
        self.assertFalse(continuity.demo_owner_override({}))
        self.assertFalse(continuity.demo_owner_override({name: "1"}))
        self.assertTrue(continuity.demo_owner_override({name: value}))
        self.assertFalse(continuity.demo_owner_override({name: value, "ZF_ENV": "production"}))


if __name__ == "__main__":
    unittest.main()
