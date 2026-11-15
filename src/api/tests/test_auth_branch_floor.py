"""Synthetic branch-floor fixtures for auth error and validation paths (issue #165)."""

import base64
import contextlib
import io
import json
import time
import unittest
from types import SimpleNamespace

from zava_forward.api import auth

TENANT = "11111111-2222-3333-4444-555555555555"
OTHER_TENANT = "99999999-2222-3333-4444-555555555555"
OID = "aaaaaaaa-0000-0000-0000-000000000001"
ENV = dict(ZF_AUTH="trusted-proxy", ZF_TRUSTED_PROXY="1", ZF_ENTRA_TENANT_ID=TENANT)
STAFF = {
    "synthetic@example.invalid": dict(name="Synthetic Staff", email="Synthetic@Example.Invalid")
}


def header(claims: list[dict[str, str]], typ: str = "aad") -> dict[str, str]:
    raw = json.dumps(dict(auth_typ=typ, claims=claims)).encode()
    return {"X-MS-CLIENT-PRINCIPAL": base64.b64encode(raw).decode()}


def claim(typ: str, val: str) -> dict[str, str]:
    return dict(typ=typ, val=val)


class PasswordProviderBranchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = auth.PasswordProvider(SimpleNamespace(staff=STAFF), "synthetic-pw", key="k")

    def cookie(self, value: str) -> dict[str, str]:
        return {"Cookie": f"zf_session={value}"}

    def test_login_rejects_unknown_user_and_wrong_password(self) -> None:
        self.assertIsNone(self.provider.login("nobody@example.invalid", "synthetic-pw"))
        self.assertIsNone(self.provider.login("synthetic@example.invalid", "wrong"))
        self.assertIsNone(self.provider.login(None, None))

    def test_authenticate_rejects_malformed_and_tampered_cookies(self) -> None:
        token = self.provider.login(" Synthetic@Example.Invalid ", "synthetic-pw")
        self.assertIsNotNone(token)
        self.assertEqual(self.provider.authenticate(self.cookie(token))["rule_roles"], [])
        self.assertIsNone(self.provider.authenticate({}))
        self.assertIsNone(self.provider.authenticate(self.cookie("nodot")))
        payload = token.rsplit(".", 1)[0]
        self.assertIsNone(self.provider.authenticate(self.cookie(payload + ".00")))

    def test_authenticate_rejects_undecodable_and_expired_payloads(self) -> None:
        bad = "!!!"
        self.assertIsNone(
            self.provider.authenticate(self.cookie(f"{bad}.{self.provider._sign(bad)}"))
        )
        expired = base64.urlsafe_b64encode(
            json.dumps(dict(e="synthetic@example.invalid", x=int(time.time()) - 5)).encode()
        ).decode()
        self.assertIsNone(
            self.provider.authenticate(self.cookie(f"{expired}.{self.provider._sign(expired)}"))
        )

    def test_account_and_logout(self) -> None:
        user = STAFF["synthetic@example.invalid"]
        self.assertEqual(self.provider.account({}, user)["provider"], "password")
        self.assertEqual(self.provider.logout_response(), {"ok": True})


class TrustedProxyBranchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = auth.TrustedProxyProvider(SimpleNamespace(staff={}), ENV)

    def denied(self, headers: dict[str, str]) -> bool:
        with contextlib.redirect_stdout(io.StringIO()) as out:
            result = self.provider.authenticate(headers)
        self.assertIn("auth denied", out.getvalue())
        return result is None

    def test_construction_requires_tenant_and_proxy_confirmation(self) -> None:
        with self.assertRaises(SystemExit):
            auth.TrustedProxyProvider(SimpleNamespace(), {**ENV, "ZF_ENTRA_TENANT_ID": "nope"})
        with self.assertRaises(SystemExit):
            auth.TrustedProxyProvider(SimpleNamespace(), {**ENV, "ZF_TRUSTED_PROXY": "0"})

    def test_role_map_override_is_applied(self) -> None:
        env = {**ENV, "ZF_ROLE_MAP": json.dumps({"Synthetic.Role": "Contractor"})}
        provider = auth.TrustedProxyProvider(SimpleNamespace(), env)
        self.assertEqual(provider.role_map["Synthetic.Role"], "Contractor")

    def test_parse_principal_rejects_bad_input(self) -> None:
        parse = auth.TrustedProxyProvider.parse_principal
        self.assertIsNone(parse(None))
        self.assertIsNone(parse("x" * (auth.MAX_HEADER + 1)))
        self.assertIsNone(parse("not base64!"))
        self.assertIsNone(parse(base64.b64encode(b'{"claims": 1}').decode()))

    def test_authenticate_denies_each_invalid_principal(self) -> None:
        tid, oid = claim("tid", TENANT), claim("oid", OID)
        self.assertTrue(self.denied({}))
        self.assertTrue(self.denied(header([tid, oid], typ="other")))
        self.assertTrue(self.denied(header([claim("tid", OTHER_TENANT), oid])))
        self.assertTrue(self.denied(header([tid])))
        self.assertTrue(self.denied(header([tid, oid, claim("roles", "Unmapped.Role")])))

    def test_logout_targets(self) -> None:
        self.assertIn("switch=1", self.provider.logout_response(switch=True)["redirect"])
        self.assertIn("/.auth/logout", self.provider.logout_response()["redirect"])

    def test_account_falls_back_to_user_name(self) -> None:
        headers = header([claim("tid", TENANT), claim("oid", OID)])
        account = self.provider.account(headers, dict(name="Fallback Name"))
        self.assertEqual(account["name"], "Fallback Name")
        self.assertEqual(account["email"], "")


class MakeProviderBranchTests(unittest.TestCase):
    def test_unknown_kind_and_production_password_are_refused(self) -> None:
        with self.assertRaises(SystemExit):
            auth.make_provider(None, "pw", {"ZF_AUTH": "magic"})
        with self.assertRaises(SystemExit):
            auth.make_provider(None, "pw", {"ZF_ENV": "production"})

    def test_default_is_password_and_trusted_proxy_is_selected(self) -> None:
        store = SimpleNamespace(staff={})
        self.assertEqual(auth.make_provider(store, "pw", {}).name, "password")
        self.assertEqual(auth.make_provider(store, "pw", ENV).name, "trusted-proxy")


if __name__ == "__main__":
    unittest.main()
