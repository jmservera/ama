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

    def test_admin_alone_enters_and_sees_every_option_but_reads_no_business_data(self):
        code, me = self.call("/api/me", oid=OID_NEW)
        self.assertEqual(code, 200)
        self.assertEqual(me["user"]["role"], "Application Administrator")
        self.assertTrue(me["user"]["app_admin"])
        self.assertEqual((me["counts"], me["staff"]), ({}, []))
        labels = {d["label"] for d in me["navigation"]}
        self.assertTrue({"Finance", "Capacity and work orders", "Closed cases", "All cases"} <= labels)
        self.assertTrue(all(d["access"] == "needs a role with this authority" for d in me["navigation"]))
        for path in ("/api/stats", "/api/cases", "/api/cases.csv", "/api/cases/ZF-1", "/api/finance/queue",
                     "/api/audit", "/api/packages", "/api/funding"):
            self.assertEqual(self.call(path, oid=OID_NEW)[0], 403, path)

    def test_admin_with_a_staff_role_sees_every_option_but_data_follows_the_staff_role(self):
        roles = (ADMIN, "ZavaForward.Coordinator")
        code, me = self.call("/api/me", roles=roles, oid=OID_NEW)
        self.assertEqual((code, me["user"]["role"]), (200, "Retrofit Coordinator"))
        access = {d["label"]: d["access"] for d in me["navigation"]}
        self.assertEqual(access["My cases"], "available")
        for label in ("Finance", "Capacity and work orders", "Closed cases"):
            self.assertEqual(access[label], "needs a role with this authority")
        self.assertEqual(self.call("/api/cases", roles=roles, oid=OID_NEW)[0], 200)
        self.assertEqual(self.call("/api/finance/queue", roles=roles, oid=OID_NEW)[0], 403)
        plain = self.call("/api/me", roles=("ZavaForward.Coordinator",), oid=OID_NEW)[1]
        self.assertTrue(all("access" not in d for d in plain["navigation"]))

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

    def test_admin_alone_still_cannot_post_and_gets_no_business_role(self):
        for path in ("/api/cases/ZF-1/call", "/api/finance/budget"):
            self.assertEqual(self.post(path, (ADMIN,), {})[0], 403)

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


class ContinuityTests(Base):
    OID_LEGACY = "dddddddd-0000-0000-0000-0000000000aa"

    def setUp(self):
        super().setUp()
        self.row = dict(code="RC-01", name="Legacy Owner", email="legacy@example.test", role="Retrofit Coordinator", oid=self.OID_LEGACY,
                        financial_authority=dict(marker="scoped"), contract_authorities=[dict(marker="scoped")])
        self.store.staff[self.row["email"]] = self.row
        self.entra = auth.TrustedProxyProvider(self.store, ENV).authenticate(
            {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.Coordinator",), oid=self.OID_LEGACY)})

    def test_verified_oid_keeps_legacy_business_identity_but_role_comes_from_the_claim(self):
        user = identity.bind(self.store, self.entra)
        self.assertEqual((user["code"], user["email"], user["name"]), ("RC-01", "legacy@example.test", "Legacy Owner"))
        self.assertEqual((user["tid"], user["oid"], user["role"]), (TENANT, self.OID_LEGACY, "Retrofit Coordinator"))
        self.assertEqual(user["derived_code"], identity.code_for(TENANT, self.OID_LEGACY))
        self.assertIsNotNone(identity.verified(user))
        self.row["role"] = "Retrofit Programme Manager"
        self.assertEqual(identity.bind(self.store, self.entra)["role"], "Retrofit Coordinator")

    def test_ambiguous_disabled_or_missing_match_keeps_the_derived_identity(self):
        self.store.staff["copy@example.test"] = dict(self.row, email="copy@example.test", code="RC-02")
        self.assertEqual(identity.bind(self.store, self.entra)["code"], identity.code_for(TENANT, self.OID_LEGACY))
        del self.store.staff["copy@example.test"]
        self.row["disabled"] = True
        self.assertEqual(identity.bind(self.store, self.entra)["code"], identity.code_for(TENANT, self.OID_LEGACY))

    def test_bound_identity_cannot_be_forged_or_stale(self):
        user = identity.bind(self.store, self.entra)
        self.assertIsNone(identity.verified(dict(user, code="RC-99")))
        self.assertIsNone(identity.verified(dict(user, bound=dict(code="RC-01", email="other@example.test"))))
        forged = dict(user, bound=None, code="RC-01", email="legacy@example.test")
        self.assertIsNone(identity.verified(forged))

    def test_scoped_authorities_resolve_by_immutable_identity_at_the_protected_operation(self):
        from zava_forward.core import change_provenance
        user = identity.bind(self.store, self.entra)
        actor = change_provenance._actor(self.store, user)
        self.assertEqual(actor["financial_authority"], dict(marker="scoped"))
        self.assertEqual(actor["contract_authorities"], [dict(marker="scoped")])
        self.assertEqual(actor["role"], "Retrofit Coordinator")
        self.row["code"] = "RC-77"
        with self.assertRaises(PermissionError):
            change_provenance._actor(self.store, user)
        derived = identity.bind(self.store, self.entra | dict(oid=self.entra["oid"]))
        self.row["code"] = "RC-01"
        other = auth.TrustedProxyProvider(self.store, ENV).authenticate(
            {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.Coordinator",), oid=OID_NEW)})
        unbound = change_provenance._actor(self.store, identity.bind(self.store, other))
        self.assertNotIn("financial_authority", unbound)
        self.assertIsNotNone(derived)

    def test_new_entra_recipients_are_selectable_only_after_they_sign_in(self):
        other = auth.TrustedProxyProvider(self.store, ENV).authenticate(
            {"X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.Coordinator",), oid=OID_NEW)})
        with self.assertRaises(ValueError):
            self.store._staff_person(other["email"])
        identity.register(self.store, identity.bind(self.store, other))
        self.assertEqual(self.store._staff_person(other["email"])["code"], other["code"])
        self.assertIn(other["code"], [p["code"] for p in identity.people(self.store)])
        identity.register(self.store, identity.bind(self.store, self.entra))
        self.assertNotIn("RC-01", [p["code"] for p in identity.people(self.store)])
        admin = auth.TrustedProxyProvider(self.store, ENV).authenticate({"X-MS-CLIENT-PRINCIPAL": principal(roles=(ADMIN,), oid="eeeeeeee-0000-0000-0000-000000000001")})
        identity.register(self.store, identity.bind(self.store, admin))
        self.assertNotIn(admin["code"], [p["code"] for p in identity.people(self.store)])
