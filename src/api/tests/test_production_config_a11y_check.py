"""Issue 619: the production-configuration check authenticates; password sign-in is refused."""

import unittest

from checks.production_config_a11y_browser_check import (
    PRODUCTION_ENV,
    horizontal_overflow,
    principal_header,
)

from zava_forward.api import auth


class ProductionConfigA11yCheck(unittest.TestCase):
    def test_header_is_accepted_by_the_trusted_proxy_provider(self) -> None:
        provider = auth.TrustedProxyProvider(None, PRODUCTION_ENV)
        user = provider.authenticate({"X-MS-CLIENT-PRINCIPAL": principal_header()})
        self.assertEqual(user["role"], "Retrofit Coordinator")

    def test_reflow_flags_only_content_wider_than_the_viewport(self) -> None:
        self.assertFalse(horizontal_overflow(320, 320))
        self.assertTrue(horizontal_overflow(321, 320))

    def test_production_environment_refuses_the_password_provider(self) -> None:
        env = {"ZF_ENV": "production", "ZF_AUTH": "password"}
        with self.assertRaises(SystemExit):
            auth.make_provider(None, "synthetic", env)
        self.assertEqual(PRODUCTION_ENV["ZF_ENV"], "production")
        self.assertEqual(PRODUCTION_ENV["ZF_AUTH"], "trusted-proxy")


if __name__ == "__main__":
    unittest.main()
