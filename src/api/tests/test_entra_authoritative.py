"""Entra-authoritative access: validated tenant, object id and app roles, no staff row."""

import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from test_auth import Base, ENV, OID_NEW, TENANT, principal
from zava_forward.api import auth
from zava_forward.api.server import App, make_handler
from zava_forward.core import identity, projection

ADMIN = "ZavaForward.ApplicationAdmin"


class EntraHttpTests(Base):
    def setUp(self):
        super().setUp()
        self.store.staff.clear()
        self.store.data["staff"].clear()
        prov = auth.TrustedProxyProvider(self.store, ENV)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(self.store, provider=prov)))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def call(self, path, roles=(ADMIN,), **kw):
        headers = {"X-MS-CLIENT-PRINCIPAL": principal(roles=roles, **kw)} if roles is not None else {}
        try:
            with urllib.request.urlopen(urllib.request.Request(self.base + path, headers=headers)) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_admin_with_empty_staff_register_signs_in_and_sees_manager_options(self):
        code, me = self.call("/api/me", oid=OID_NEW)
        self.assertEqual(code, 200)
        self.assertEqual(me["user"]["role"], "Retrofit Programme Manager")
        self.assertTrue(me["user"]["app_admin"])
        self.assertEqual(me["user"]["code"], identity.code_for(TENANT, OID_NEW))
        self.assertEqual(self.call("/api/stats", oid=OID_NEW)[0], 200)
        self.assertEqual(self.call("/api/cases", oid=OID_NEW)[0], 200)

    def post(self, path, roles, body=None):
        req = urllib.request.Request(self.base + path, json.dumps(body or {}).encode(), headers={
            "X-MS-CLIENT-PRINCIPAL": principal(roles=roles), "X-ZF-CSRF": "1"})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_admin_alone_is_view_only_but_admin_with_staff_role_keeps_that_role_authority(self):
        code, body = self.post("/api/bulk-edits/apply", (ADMIN,))
        self.assertEqual(code, 403)
        self.assertIn("changes nothing", body["error"])
        self.assertEqual(self.post("/api/logout", (ADMIN,))[0], 200)
        code, body = self.post("/api/bulk-edits/apply", (ADMIN, "ZavaForward.SupportOfficer"))
        self.assertNotIn("changes nothing", json.dumps(body))
        self.assertEqual(self.call("/api/me", roles=(ADMIN, "ZavaForward.SupportOfficer"))[1]["user"]["role"],
                         "Programme Support Officer")

    def test_admin_with_programme_manager_is_not_a_two_role_denial(self):
        self.assertEqual(self.call("/api/me", roles=("ZavaForward.ProgrammeManager", ADMIN))[0], 200)

    def test_anonymous_unassigned_wrong_tenant_and_bad_oid_are_denied(self):
        self.assertEqual(self.call("/api/me", roles=None)[0], 401)
        self.assertEqual(self.call("/api/me", roles=())[0], 401)
        self.assertEqual(self.call("/api/me", roles=("Unmapped.Role",))[0], 401)
        self.assertEqual(self.call("/api/me", tid="99999999-2222-3333-4444-555555555555")[0], 401)
        self.assertEqual(self.call("/api/me", oid="not-a-guid")[0], 401)
        self.assertEqual(self.call("/api/me", oid=None)[0], 401)

    def test_admin_grants_no_approval_or_override_capability(self):
        user = auth.TrustedProxyProvider(self.store, ENV).authenticate({"X-MS-CLIENT-PRINCIPAL": principal(roles=(ADMIN,))})
        self.assertEqual(user["rule_roles"], [])
        self.assertNotIn(user["role"], ("Building Safety Liaison", "Quality Inspector"))
        self.assertFalse(projection.is_contractor(user))

    def test_identity_verification_rejects_tampered_keys(self):
        user = identity.principal(TENANT, OID_NEW, "Retrofit Programme Manager")
        self.assertIsNotNone(identity.verified(user))
        for key, value in (("code", "E-000000000000"), ("email", "sam@example.test"), ("oid", OID_NEW.upper()), ("tid", None)):
            self.assertIsNone(identity.verified(dict(user, **{key: value})))
        self.assertIsNone(identity.verified({"identity_source": "staff"}))


class IdentitySeamTests(unittest.TestCase):
    def test_distinct_people_get_distinct_stable_keys(self):
        a = identity.principal(TENANT, OID_NEW, "Retrofit Coordinator")
        b = identity.principal(TENANT, "bbbbbbbb-0000-0000-0000-000000000002", "Retrofit Coordinator")
        self.assertNotEqual((a["code"], a["email"]), (b["code"], b["email"]))
        self.assertEqual(a, identity.principal(TENANT.upper(), OID_NEW.upper(), "Retrofit Coordinator"))

    def test_display_claims_cannot_inject_controls_or_exceed_limits(self):
        self.assertEqual(identity.display("A\x00B\u202ec" + "z" * 400), "ABc" + "z" * 117)
        self.assertEqual(identity.display(None), "")


if __name__ == "__main__":
    unittest.main()
